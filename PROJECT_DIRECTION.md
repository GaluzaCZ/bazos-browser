# Bazoš Sniper – směr projektu

## Cíl

**Bazoš Sniper má automaticky hledat zajímavé inzeráty na Bazoši, pamatovat si
jejich historii a upozornit na nabídky, které stojí za pozornost.**

Hlavní myšlenka:

> **Najdi mi zajímavý inzerát co nejrychleji a řekni mi, proč stojí za
> pozornost.**

## Co Bazoš Sniper není

Projekt nemá být pouze scraper:

```text
Bazoš → stáhnout inzeráty → vypsat
```

Cílově jde o systém:

```text
Bazoš
  ↓
sběr inzerátů
  ↓
uložení + historie
  ↓
normalizace
  ↓
analýza
  ↓
scoring
  ↓
🔥 upozornění
```

## MVP

První použitelná verze musí umět:

- automaticky spouštět uložená hledání,
- ukládat nalezené inzeráty,
- poznat nový inzerát,
- poznat změnu ceny nebo obsahu,
- uchovávat historii,
- normalizovat důležité údaje,
- vypočítat `Sniper Score`,
- upozornit na zajímavou nabídku.

**AI není podmínkou MVP.** Nejdříve musí spolehlivě fungovat sběr, historie a
vyhodnocování.

## Dlouhodobý směr

Nasbíraná data mají postupně umožnit:

- porovnávání ceny s historickým trhem,
- detekci podezřele levných nabídek,
- rozpoznávání relistovaných inzerátů,
- historii prodejců,
- analýzu fotografií,
- AI analýzu textu a nabídky,
- přesnější `Sniper Score`,
- webový dashboard.

Čím déle Sniper běží, tím hodnotnější by měla být jeho vlastní databáze trhu.

## Princip architektury

Scraping je pouze **zdroj dat**.

Jednotlivé části projektu mají zůstat oddělené tak, aby bylo možné později
přidat další marketplace nebo vyměnit databázi, AI či uživatelské rozhraní bez
přepisování celého systému.

## Rozhodování o nových funkcích

Před implementací nové funkce si položit otázku:

> **Pomůže nám rychleji najít, lépe vyhodnotit nebo spolehlivěji sledovat
> zajímavou nabídku?**

Pokud ne, pravděpodobně ji zatím nepotřebujeme.
