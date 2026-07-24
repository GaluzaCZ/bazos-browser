import argparse
from datetime import date
from urllib.parse import urlparse
from core.models import SearchCriteria

def _positive(value: str) -> int:
    value = int(value)
    if value <= 0: raise argparse.ArgumentTypeError("must be positive")
    return value
def _nonnegative(value: str) -> int:
    value = int(value)
    if value < 0: raise argparse.ArgumentTypeError("must not be negative")
    return value
def _date(value: str) -> date:
    try: return date.fromisoformat(value)
    except ValueError: raise argparse.ArgumentTypeError("use YYYY-MM-DD")

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--query"); p.add_argument("--category"); p.add_argument("--section")
    p.add_argument("--location"); p.add_argument("--radius", type=_nonnegative)
    p.add_argument("--price-min", type=_nonnegative); p.add_argument("--price-max", type=_nonnegative)
    p.add_argument("--sort"); p.add_argument("--since", type=_date); p.add_argument("--url")
    p.add_argument("--limit", type=_positive, default=20); p.add_argument("--timeout", type=_positive, default=15)
    p.add_argument("--exclude-seller", action="append", default=[]); p.add_argument("--database", default="cars.db")
    return p

def parse_args(argv=None):
    args = parser().parse_args(argv)
    filters = [args.query,args.category,args.section,args.location,args.radius,args.price_min,args.price_max,args.sort,args.since]
    if args.url:
        parsed = urlparse(args.url)
        if parsed.scheme != "https" or "bazos.cz" not in parsed.netloc or any(x is not None for x in filters): parser().error("--url is HTTPS Bazos listing URL and cannot be combined with filters")
    if args.price_min is not None and args.price_max is not None and args.price_min > args.price_max: parser().error("price-min must not exceed price-max")
    return args

def criteria_from_args(args) -> SearchCriteria:
    return SearchCriteria(args.query,args.category,args.section,args.location,args.radius,args.price_min,args.price_max,args.sort,args.since,args.url)
