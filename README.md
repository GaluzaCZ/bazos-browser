# Bazos Browser

Projekt obsahuje samostatnou knihovnu `bazos_sniper` a aplikaci `app`.

## Spuštění

Projekt používá připravené prostředí `.venv`:

```powershell
.\.venv\Scripts\python.exe main.py --query bmw --limit 10
```

Při použití aktivovaného prostředí stačí:

```powershell
python main.py --query bmw --limit 10
```

Jediné podporované volby jsou povinné `--query` a volitelné kladné `--limit`
(výchozí hodnota 20). Výsledky se ukládají do `cars.db`, který se při prvním
spuštění automaticky vytvoří.

## Knihovna bazos-sniper

Python používá v názvu importu podtržítko, proto se knihovna importuje jako
`bazos_sniper`:

```python
from bazos_sniper import BazosSniper

listings = BazosSniper().search("bmw", limit=10)
for listing in listings:
    print(listing.title, listing.price, listing.url)
```

Knihovna vlastní HTTP komunikaci, stránkování, deduplikaci a parsování seznamu
i detailu. Vrací typované objekty `Listing` a nezná databázi, CLI ani analýzu
aplikace.

## Aplikace

`SearchApplication` přijme knihovnu a repository jako závislosti. Zpracuje
vrácené inzeráty, uloží je do SQLite a vrátí `SearchResult`. CLI je pouze tenká
prezentační vrstva. Budoucí GUI nebo API tak může volat stejnou aplikační službu
bez závislosti na argumentech příkazové řádky nebo konzolovém výstupu.

## Tok aplikace

1. CLI vytvoří aplikační požadavek s dotazem a limitem.
2. `bazos_sniper` stáhne, stránkuje a zformátuje kompletní inzeráty.
3. Aplikace uloží vrácené objekty přes SQLite repository.
4. Aplikace normalizuje vozidla a vypočítá skóre.
5. CLI vypíše aplikační výsledky.

HTML parser závisí na aktuální struktuře Bazoše. Normalizace vozidel rozpoznává
jen vybrané modely BMW řady 3.
