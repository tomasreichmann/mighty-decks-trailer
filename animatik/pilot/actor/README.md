# Hráčka v pilotu C

Při prvních 2,20 s vykresli `residual.png`, fyzické karty a nad nimi jeden snímek z `frames/actor-000.png` až `actor-052.png`. Obě vrstvy hráčky jsou RGBA, mají 896 × 832 px a leží v počátku (0, 0) obrazu 1920 × 1080. Při přehrávání na 30 fps použij pro číslo snímku hráčky `floor(frame * 24 / 30)` pro snímky 0–65. Plné souřadnice vlasů, úst a prstů odpovídají původní kresbě. Ostatní postava, nábytek i obrazové rozhraní mají vlastní vrstvy.

## Vstup a výpočet

Jediným obrazovým vstupem pro generaci je `storyboard/vrstvy/table/02-hracka.png`. Skript `prepare.py` z něj ořízne dvě oddělené masky, profil hlavy a předloktí s prsty. Obojí dá na jednolitou zelenou plochu 448 × 416 px. Kontury úmyslně minou vršky karet, které v původní masce ležely těsně pod prsty. Plece, trup, deska, vypravěč a grafika mají původní kresbu.

1. Spusť `python animatik/pilot/actor/prepare.py`. Skripty potřebují Pillow, OpenCV a NumPy.
2. Nahraj `md-actor-green.png` pod tímto jménem do `input/` místního ComfyUI. Ověř a spusť API graf `h3-actor.json`. Používá stejný seed 716305, repliky a režii klidného hlasu jako A. Osm kroků MiniMax H3 vytvořilo 124 snímků při 24 fps za 59,63 s na RTX 3090. ID generace `04b220f8-c371-46a4-907f-cffbcf28fcb0`. Uložení bezztrátových snímků ze stejné cache trvalo 3,82 s, úloha `c00113b0-8f93-4c36-9efc-a78a7dc60f5b`.
3. Ulož MP4 z uzlu 14 jako `h3-actor-native.mp4` a prvních 68 snímků bezztrátového animovaného WebP z uzlu 19 jako `h3-actor-lossless.webp`. MP4 dokumentuje pohyb i samostatně vygenerovaný zvuk, WebP poskytuje plné RGB pro klíčování.
4. Pro okamžité složení s dodanými maskami spusť `python animatik/pilot/actor/extract.py`. Skript používá `sam2-mattes.npz` a `../table/registration.json` a obnoví jedinou statickou vrstvu a všech 53 pohybových PNG. Následující postup umí obnovit i samotné segmentace.

### Segment Anything pro tvář, čelist, dlaň a zápěstí

Použitý uzel **Sam2Segmentation** pracuje v místním ComfyUI služby SwarmUI na portu 7821, s rozšířením **ComfyUI-segment-anything-2** a modelem **sam2_hiera_base_plus.safetensors** na RTX 3090 v BF16. SHA-256 modelu je `fa02d9028dcc4859c191f1d3f1ca1f7eefdb85f3b5e746c9ad738f322f3e89e2`. Generace pohybu v H3 a jeho segmentace proto používají různé místní porty.

1. Vstupům `md-actor-green.png` a `h3-actor-lossless.webp` při nahrání do tohoto backendu dej názvy `md-fangs-actor-source-green.png` a `md-fangs-h3-actor-lossless.webp`.
2. Ověř a spusť `sam2-graph.json` na portu 7821. Graf obsahuje dva prostorové výřezy a pozitivní i negativní body v souřadnicích každého výřezu. Získá samostatnou referenční masku tváře a ruky z původní kresby a po jedné sledované masce na každý z 68 snímků H3. U tváře další průchod SAM2 v každém snímku pomůže oddělit kůži od ofiny přesahující do sledované oblasti.
3. Spusť `python animatik/pilot/actor/collect-sam2.py ID_ULOHY`. Skript čte skutečně uložené masky z historie ComfyUI, přemístí je do společných souřadnic a bezztrátově zabalí. Finální validovaný graf dokončil práci pod ID `1f6e24b1-1efb-4880-823f-3d219c8a5374`. První pokus na celých dvou ostrovech přibral část opačné končetiny. Oddělené výřezy a průchod s upřesněním řeší tento nález.
4. Spusť sestavení `extract.py`. Přechod zachovává starou i novou krajní polohu prstů a brady tak, aby jejich pohyb vždy odkryl podklad. Kontura SAM2 tvoří střed přechodu, který měkne přes 14 px u hlavy a 12 px u ruky. Vnitřní kotvení u krku a švu rukávu navazuje na přesnou registrovanou kresbu.

Při kontrole celých kompozic v šířce 390 px a detailů v měřítku 1:1 jsme srovnali snímky hráčky 12, 27, 40 a 52 na stejné časové ose. Tabulka počítá viditelné pixely (krytí > 50 %), pro které výsledná váha generovaného pohybu dosahuje alespoň 50 %. Jednotkou je pixel plátna 1920 × 1080. Čísla v buňkách uvádějí původní plochu → plochu po SAM2.

| Snímek hráčky | Profil včetně čelisti | Ruka s předloktím | Tvář pod okem (x 477–594, y 292–409) | Zápěstí (x 397–564, y 630–701) |
|---|---:|---:|---:|---:|
| 12 | 20 945 → 36 045 | 11 614 → 28 588 | 5 352 → 12 515 | 0 → 9 431 |
| 27 | 21 569 → 32 636 | 14 164 → 31 831 | 5 352 → 11 985 | 0 → 9 431 |
| 40 | 21 164 → 36 678 | 12 944 → 30 590 | 5 352 → 12 488 | 0 → 9 431 |
| 52 | 21 377 → 36 000 | 12 944 → 30 670 | 5 352 → 12 507 | 0 → 9 431 |

Nezávislá kontrola prvního průchodu našla na videových snímcích 24–45 druhou hranu manžety. Poslední úprava kotví zakřivený okraj manžety a šrafování bundy podle geometrie zdroje. Váha pohybu narůstá až uvnitř kůže. Na videovém snímku 36 má kontrolní plocha bundy (x 411–564, y 582–621) proti čisté kresbě nulovou průměrnou odchylku jasu kanálů RGB. Výřez prstů (x 633–761, y 610–724) zůstal shodný s prvním průchodem SAM2.

## Pohyb a zvuk

Zelenou barvu odečítáme z každého snímku podle změřeného pozadí. U vlasů, jasu hran a poloprůhledných pixelů se dopočítá krytí a odbarví zelený lem. Optický tok mezi prvním a aktuálním snímkem H3 přenáší malý pohyb do původního šrafování osnovy vlasů a rukávu. Krk a šev rukávu jsou ukotvené. Výrazy očí, tvary úst a prstů přebíráme z aktuálního bezztrátového snímku. Ze statické vrstvy se navíc odstraní obrys pohybujícího se prstu, aby po jeho zvednutí zůstalo dřevo stolu.

Ve výsledném pilotu zůstává zvuk A. Nové čtení začíná v 0,48 s a končí v 2,81 s, důvod v A běží od 0,27 do 2,17 s. `timing.json` vyznačuje i vnitřní pauzu a slovo „lodi“. Čas pro obraz se přepočítá mezi jednotlivými naměřenými body. Pozice rtu a prstu byly zkontrolované na složení v nativní velikosti. Na celém 1080p zůstávají generované detaily díky rozlišení zkoušky měkčí než čistá statická kresba.
