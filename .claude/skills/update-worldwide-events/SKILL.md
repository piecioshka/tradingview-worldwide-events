---
name: update-worldwide-events
description: >-
  Dopisuje nowe wydarzenia rynkowe i geopolityczne do repozytorium
  `tradingview-worldwide-events` (pliki `data/events-en.md` i `data/events-pl.md`,
  wskaźnik TradingView "Worldwide Events"). Użyj, gdy użytkownik w tym repo prosi
  "pobierz nowe dane", "zaktualizuj eventy", "dodaj nowe wydarzenia", "uzupełnij
  wydarzenia od ostatniego wpisu", "co się wydarzyło od <data>", albo wkleja
  pojedyncze wydarzenie do dodania. Obejmuje research, dobór linków (angielski
  dla EN, WYŁĄCZNIE polski dla PL), regenerację `worldwide-events.pine` i commit.
---

# update-worldwide-events

Dane to dwie tabele Markdown
(`data/events-en.md`, `data/events-pl.md`) o kolumnach `Date | Description | Priority | Link`,
posortowane malejąco po dacie. Z nich `scripts/generate-events.py` buduje `worldwide-events.pine`.

Zasada nadrzędna z `CLAUDE.md` repo: KAŻDY dodany wiersz ma link do artykułu, który opisuje
konkretnie to wydarzenie. W `events-pl.md` link musi prowadzić do tekstu po polsku.

## Krok 1: zakres

```bash
grep -m1 -o '^| [0-9-]\{10\}' data/events-en.md   # ostatnia data w pliku
date +%F                                            # dziś
```

Zapisz ostatnią datę - to wartość `--since` w kroku 5. Szukasz wydarzeń z przedziału
(ostatnia data, dziś]. Jeśli użytkownik podał konkretne wydarzenie, pomiń research i przejdź
do kroku 3.

## Krok 2: kandydaci

Źródła, które działają (2026-09):

- `WebSearch` z zapytaniami per miesiąc, np. `"July 2026" biggest market events`,
  `Fed decision July 2026`, `stock market worst day July 2026`,
  `geopolitical events July 2026 war oil`.
- Wikipedia `https://en.wikipedia.org/wiki/Portal:Current_events/<Month>_<Year>` przez `WebFetch`
  z promptem "list business/economy/central banks/wars/elections with exact dates". Strona jest
  długa i `WebFetch` obcina ją po kilku pierwszych dniach miesiąca - dla reszty miesiąca użyj
  wyszukiwarki albo stron dziennych (`Portal:Current_events/<Year>_<Month>_<Day>`).
- Artykuły Wikipedii o toczących się kryzysach (np. `2026_Iran_war`, `2026_United_States_naval_blockade_of_Iran`)
  z promptem o datowaną oś czasu.

Co kwalifikuje się do pliku (patrz istniejące wpisy, trzymaj ich poziom):

| Priorytet | Typ wydarzenia                                                                              |
| --------- | ------------------------------------------------------------------------------------------- |
| `high`    | wybuch/koniec wojny, zamknięcie Ormuz, uderzenia zmieniające cenę ropy, krach, upadek banku |
| `medium`  | odwet/atak w trwającej wojnie, rekord indeksu, przywrócenie blokady, duży deal              |
| `low`     | posiedzenie Fed/EBC bez zmiany kursu, Jackson Hole, zmiana premiera, szczyt G7              |

Pomijaj: sport, kulturę, katastrofy naturalne bez wpływu na rynki, cykliczne dane makro (CPI,
payrolls), prognozy i "may happen". Wynik zapytania to często 10-15 kandydatów; do pliku wchodzi
zwykle 5-12 na kwartał.

## Krok 3: linki (najdłuższy krok)

Dla każdego wydarzenia potrzebujesz DWÓCH artykułów.

**EN:** Wikipedia, jeśli ma osobny artykuł o wydarzeniu (nie o instytucji - `Federal_Reserve`
jako link do decyzji Fed to zły wzorzec z przeszłości). Inaczej CNBC, Al Jazeera, NPR, NBC, Yahoo
Finance, The Hill.

**PL:** rp.pl (także `energia.rp.pl`), bankier.pl, parkiet.com, forsal.pl, money.pl, wnp.pl,
interia.pl, tvn24.pl, polsatnews.pl, pap.pl, forexclub.pl. Zapytanie pisz po polsku i dopisz
`bankier OR rp.pl OR tvn24 OR pap`, inaczej `WebSearch` oddaje angielskie wyniki.

Weryfikacja każdego linku - tytuł NIE wystarcza:

1. `curl -s -o /dev/null -w '%{http_code}' -A 'Mozilla/5.0' <url>` musi dać 200
   (301/302 - weź docelowy URL; cnbc.com i upi.com dają `WebFetch` 403, ale curl 200 - link
   jest dobry, treść sprawdź przez wynik wyszukiwarki).
2. `WebFetch` z promptem "data publikacji i o jakim wydarzeniu mowa". Artykuł o tym samym temacie
   z innego miesiąca wygląda identycznie w tytule (np. "Ropa blisko 100 dolarów" z kwietnia zamiast
   z września) - odrzucaj, gdy data nie pasuje do wydarzenia.
3. Artykuł z dnia następnego opisujący wczorajsze wydarzenie jest OK.

Wydarzenie wchodzi do OBU plików albo do żadnego. Gdy po dwóch-trzech polskich zapytaniach
(inne słowa kluczowe, inny portal) nadal nie ma polskiego artykułu, odłóż wydarzenie i wymień je
w podsumowaniu jako pominięte - nie wpisuj `-` zamiast linku i nie dodawaj go tylko do EN.

Link z nawiasami w URL owijaj w `<...>`:
`[Wikipedia](<https://pl.wikipedia.org/wiki/Wojna_na_Bliskim_Wschodzie_(2026)>)`.

## Krok 4: wiersze

```markdown
| 2026-09-08 | Houthi attack on Saudi energy infrastructure - Brent nears $100 | high | [NBC News](https://...) |
```

- Ta sama data w obu plikach. Generator bierze daty z EN i dopasowuje PL po dacie; brakująca
  data w PL = angielski opis na polskim wykresie.
- Opis do ~85 znaków (to etykieta na wykresie), bez cudzysłowów `"` (trafia do stringa Pine),
  zwykły myślnik `-`, w PL polskie znaki i przecinek dziesiętny (`3,50-3,75%`).
- Jedna data = jeden wiersz. Generator trzyma wydarzenia w słowniku po dacie, więc drugi
  wiersz z tą samą datą nadpisuje pierwszy. Dwa wydarzenia z jednego dnia sklej w jeden opis
  (wzorzec: `Warsh nominated as Fed Chair + CME silver margin hike`).
- Nowe wiersze wstaw zaraz pod linią `| ---`, malejąco po dacie.

## Krok 5: format, generator, kontrola

```bash
npx prettier@3 --write data/events-en.md data/events-pl.md   # repo nie ma package.json
python3 scripts/generate-events.py
python3 scripts/check-events.py --since <data-z-kroku-1>
```

Prettier wyrównuje całą tabelę, więc `git diff` dotyka każdej linii pliku - to normalne.
`check-events.py` sprawdza zgodność dat między plikami, sortowanie, brak cudzysłowów, długość
opisów, obecność linku w nowych wierszach i kod HTTP każdego nowego linku. Ten sam skrypt
chodzi w CI (bez `--since`, z `--no-http`), więc błąd w danych zatrzyma workflow.

## Krok 6: commit i podsumowanie

Dwa commity, jak w historii repo (bez Conventional Commits):

```bash
git add data/events-en.md data/events-pl.md && git commit -m "Add N events from <okres>"
git add worldwide-events.pine && git commit -m "Regenerate worldwide-events.pine"
```

Nie pushuj. W podsumowaniu po polsku daj tabelę dodanych wydarzeń (data, opis, priorytet) i
zaznacz, jeśli któryś kandydat odpadł z braku polskiego źródła. Release note w `releases/`
powstaje dopiero przy publikacji nowej wersji na TradingView - nie twórz go bez prośby.
