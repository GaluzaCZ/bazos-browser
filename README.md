# Bazos Browser

Projekt obsahuje obecnou doménu nabídek `offers`, Bazoš provider
`bazos_sniper` a aplikaci `app`.

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
from bazos_sniper import BazosProvider
from offers import SearchCriteria

offers = BazosProvider().search(SearchCriteria(query="bmw"), limit=10)
for offer in offers:
    print(offer.title, offer.price, offer.url)
```

Provider vlastní HTTP komunikaci, stránkování, deduplikaci a parsování seznamu
i detailu. Vrací obecné objekty `Offer` a nezná databázi, CLI ani analýzu
aplikace.

## Aplikace

`SearchApplication` přijme libovolný `MarketplaceProvider` a `OfferRepository`
jako závislosti. Metoda `execute` dostane `SearchCriteria` a volitelný limit,
zpracuje vrácené nabídky, uloží je a vrátí `SearchResult`. CLI je pouze tenká
prezentační vrstva. Budoucí GUI nebo API tak může volat stejnou aplikační službu
bez závislosti na argumentech příkazové řádky nebo konzolovém výstupu.

## Tok aplikace

1. CLI vytvoří `SearchCriteria` s dotazem a předá samostatný limit.
2. `BazosProvider` stáhne, stránkuje a převede Bazoš HTML na `Offer`.
3. Aplikace uloží obecné nabídky přes SQLite repository.
4. Aplikace normalizuje vozidla a vypočítá skóre.
5. CLI vypíše aplikační výsledky.

HTML parser závisí na aktuální struktuře Bazoše. Normalizace vozidel rozpoznává
jen vybrané modely BMW řady 3.
