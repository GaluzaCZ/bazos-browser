import logging
from bazos import BazosProvider
from cli.arguments import parse_args, criteria_from_args
from database.database import connect
from database.repository import OfferRepository
from analysis.scoring import score_offer
from analysis.vehicles import normalize_title
from utils.http import HttpClient

def run(args, provider=None, repository=None):
    provider = provider or BazosProvider(HttpClient(timeout=args.timeout))
    repository = repository or OfferRepository(connect(args.database))
    offers = provider.search(criteria_from_args(args), args.limit)
    results = []
    for offer in offers:
        try: offer = provider.load_detail(offer)
        except Exception: logging.getLogger(__name__).exception("Could not load detail: %s", offer.url)
        (repository.update_offer if repository.offer_exists(offer.url) else repository.save_offer)(offer)
        if (args.since and (not offer.published_at or offer.published_at < args.since)) or offer.seller in args.exclude_seller: continue
        results.append((offer, normalize_title(offer.title), score_offer(offer)))
    return results

def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO)
    args = parse_args(argv)
    try:
        for offer, vehicle, score in run(args): print(f"[{score:3}] {offer.title} | {offer.price or 'dohodou'} | {offer.url} | {vehicle}")
    except Exception as exc:
        logging.error("Search failed: %s", exc); return 1
    return 0
if __name__ == "__main__": raise SystemExit(main())
