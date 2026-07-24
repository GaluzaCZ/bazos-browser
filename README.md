# Bazos Sniper

Python 3.12+ command-line browser for Bazos listings. Install its dependencies:

```bash
python -m pip install -r requirements.txt
```

Then search Bazos listings, for example:

```bash
python main.py --query bmw --limit 10
python main.py --query "BMW 320d" --price-min 100000 --price-max 300000
python main.py --url "https://auto.bazos.cz/inzeraty/osobni/" --limit 25
```

## What it does

The command line validates search options, downloads and pages through Bazos
listing pages, deduplicates offers by URL, and loads the detail page of every
returned offer. Offers are saved in SQLite (`cars.db` by default), normalised
for the currently supported BMW 3 Series examples, scored, locally filtered by
`--since` and repeated `--exclude-seller` values, then printed to the console.

The reusable layers are intentionally separated: `core` holds marketplace
models and interfaces, `bazos` is the Bazos adapter, `database` maps offers to
SQLite, and `analysis` contains normalisation and scoring. Image downloading is
available only through the explicit `bazos.images` API; the CLI does not
download images automatically.

## Assessment and current limitations

The current version is a working v1 foundation rather than a finished scraper.
Its HTML selectors are heuristic and should be protected by fixture tests and
rechecked whenever Bazos changes its markup. The implementation recognises only
BMW E90/E91/F30/F31 and 320d/330d reliably; valuation and repair modules
deliberately return no estimate. There is no web UI, notification service,
price-history tracking, or automatic HTTP cache yet.

Dependencies and a local functional smoke check have been run under Python
3.12. The smoke check covers URL construction, listing/detail parsing, image
download paths, SQLite dataclass round-trip, normalisation, scoring, and CLI URL
conflict validation. No live Bazos request is used by that check.
