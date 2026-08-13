# Bazos Browser

Minimální CLI aplikace pro vyhledání inzerátů na Bazoši, načtení jejich detailu,
uložení do SQLite a vypsání skóre.

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

## Tok aplikace

1. CLI vytvoří požadavek s dotazem a limitem.
2. Bazoš provider stáhne a stránkuje seznam inzerátů.
3. Každý inzerát obohatí daty z detailu.
4. SQLite repository provede upsert do `cars.db`.
5. Aplikace normalizuje vozidlo, vypočítá skóre a vypíše výsledek.

HTML parser závisí na aktuální struktuře Bazoše. Normalizace vozidel rozpoznává
jen vybrané modely BMW řady 3.
