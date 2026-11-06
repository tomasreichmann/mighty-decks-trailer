# Fangs in the Sun · předání k dopracování storyboardu

**Aktuální zadání v5 · 6. listopadu 2026.** Rozhodnutí z výběru a následných připomínek jsou zapsaná zde. Pro pořadí akcí, repliky a návaznost karet použij [scénář CZ / EN](../storyboard/scenar-v5.md).

## Co má zůstat v hlavě diváka

Fanoušek stolních RPG má zažít chvíli, kdy by sám váhal nad kartou. Hráčka může dostat všechny přes rampu bez úrazu, ale pak nebude mít jistotu, že zachrání vlastní člun. Nechá si poslední Úspěch, pojmenuje cenu a přijme ji. Po záběru na poraněnou paži uvidíme, k čemu jí schovaná karta byla. Pozvání na konci vede ke skutečným pravidlům a kartám k vytištění.

## Režie a výtvarná rozhodnutí

- **B · Očima hráčky.** Ve fikci nás vedou její ruce, pohled z kokpitu a zápěstí u páky. Obě tváře u skutečného stolu poprvé odhalíme až na větě „Úspěch potřebuju na záchranu lodi.“ Vyhnankyni a hráčku mluví stejná interpretka.
- **S06 · Kořist z C.** Kolmý pohled do dvou přihrádek. Vlevo palubní čepel s modrým ostřím odpovídá líci Lehká zbraň. Vpravo ocelový kyrys má hranaté nárameníky a překrývající se břišní pláty podle karty Těžká zbroj. Mládě očichá přezku. Oba líce se vrátí vedle loga.
- **Styl 1 · Kresba tuší.** Výrazná černá linka, šrafování, ocelové stíny a postupně delší zlatý odlesk na hranách kovu. Tváře hráčky a vypravěče u stolu jsou také kreslené. Držet vzhled plavidla a krémovou a korálovou srst šestinohého mallowtaila podle Exiles. Z UI AI Storytelleru vychází písmo Kalam, Passion One a Shantell Sans a barvy #121B23, #EFD9BB a #7B8EA6.
- **Celý obraz patří scéně.** Bez spodního pruhu, bez pozadí přes celou šířku. Při řeči zobraz aktuální portrét vlevo dole, hned vpravo lokalizovanou roli a titulky se světlým písmem a tmavým obtahem. Na plátně 1920 × 1080 má portrét 216 px a titulky 68 px, tedy přibližně 44 a 14 px při šířce telefonu 390 px. Přepni na první slabice, po replice skryj. Platí i pro řeč u stolu a pozvání v CTA. Při tiché kořisti a logu tyto prvky zmizí. Logo hry je během příběhu vpravo nahoře (8 % šířky, odsazení 4 %).
- **Karty jsou ve scéně velké.** Ve fikci leží ruka vpravo dole nad obrazem. Pro kompozici 1920 × 1080 má referenční líc šířku 272 px (s obrysem přibližně 300 px), mezi kartami zůstává mezera. Všechny tři ukazují celý název i význam. Vnější světlá kontura a tmavá vnitřní linka drží kartu na stínu i na světlém kovu. Při konfliktu přerámuj akci nebo změň načasování. Velikost ověř podle [náhledu v šířce 960 px](../reference/vyber/rampa-kontrola-960.png). Na telefonu musí jít při hře rozeznat názvy a zvolenou kartu.
- **Zahrání má začátek, dopad a konec.** Z jediného slotu vyskočí konkrétní líc, zvětší se (pracovní šířka líce 342 px) a na okamžik se ustálí, aby šel přečíst. Pak zmizí s efektem motivovaným scénou. Návrhy pro animatik: pulz souřadnic v průzoru, tah drápu v hangáru, náraz bedny na kov na rampě, světelná stopa trysky při úhybu. Dokončenou kartu herně odhoď, dober náhradu. Nevytvářej druhou kopii líce visící v ruce. Na rampě zůstává Úspěch na místě. Efekt nesmí skrýt následek.
- **Jediný Úspěch.** Společný polocelkový záběr patří očnímu kontaktu a důvodu, proč hráčka šetří Úspěch. Při pauze střihni kolmo na stůl. Tři skutečné líce mají stejnou velikost, leží rovnoběžně a prst vybere prostřední. Položení Částečného úspěchu naváže na dopad bedny.
- **CZ / EN.** Locale řídí VO, titulky, role, CTA i samotné líce včetně karet na stole a v koncovém přehledu. Původní ilustrace, symboly, číselné hodnoty a herní význam přebírej z Components. Český název i pravidlový text patří přímo na líc.

## Pracovní obrazovky pro polished storyboard

[Otevřít jednotlivé záběry v CZ a EN](../storyboard/screens/index.html). Každá ilustrace má samostatný čistý podklad v reference/planches. Portréty, titulky, logo a karty jsou v kompozitu přidané až v rozlišení 1920 × 1080. Obě lokalizace používají tutéž kameru a tytéž pozice prvků.

Karty výsledků, Zranění, Lehká zbraň a Těžká zbroj ber pro obraz ze sady reference/karty/ruka/{cs,en}, a to i na fyzický stůl, do bedny, do přehledu a na CTA. Domobranu a Žalář ber z reference/karty/{cs,en}. Ve 3. záběru je vybraný statický snímek okamžik po zmizení Částečného úspěchu: Zranění se objeví vpravo mimo pažbu a prsty. Na konci 4. záběru patří druhé Zranění pašerákovi: díl rampy padá, pašerák visí nad šachtou a rozřízne si předloktí o utržený lem. Teprve další obraz ho ukáže za prahem s ostatními. Vpravo od loga jsou v mřížce 2 × 2 Domobrana, Žalář, Kuše a Lucerna. Na samostatné CTA vlevo ukaž krabici z dodaného tiskového rozkresu, vedle ní drž adresu i [QR kód](../reference/grafika/mighty-decks-qr.png) po celých pět sekund.

## Kde začít

| Podklad | Použití |
|---|---|
| [Aktuální storyboard](../storyboard/storyboard-v5.png) a [detail rampy](../storyboard/rampa-volba-dopad.png) | 8 časových úseků a sled rampa → stůl → skutečná cena |
| [Rampa CZ](../reference/vyber/rampa-kompozice-cs.png) a [EN](../reference/vyber/rampa-kompozice-en.png) | Kompozice 16:9 po zvětšení ruky, portrét a titulky |
| [Stůl](../reference/vyber/stul-kompozice-cs.png) a [kolmý detail karet](../reference/vyber/B-volba-u-stolu.png) | Důvod hráčky v polocelku, vlastní volba v kolmém detailu |
| [Rozehraná karta](../reference/vyber/karta-ve-scene-cs.png) | Statická póza odtržení od ruky pro budoucí animaci |
| [Nová kořist](../reference/vyber/korist-kompozice-cs.png) a [čistá ilustrace](../reference/vyber/korist-tus.png) | Dva konkrétní předměty, jejich přiřazení, obvaz, mládě |
| [Texty karet](../reference/karty/texty-en-cs.json), složky en, cs a ruka | Anglické exporty, české líce ze stejné komponenty a obě obrazovkové sady s větší sazbou |
| [Původ a použití referencí](../reference/zdroje.md) | Illustratorní podklady, originální logo, zdroj karet a historie návrhů |
| [Prompt pro další fázi](prompt-pro-storyboard.txt) | Zkopírovat do dalšího chatu |

Další schvalovací výstup tvoří dvě barevné statické sady CS a EN, popis pohybu a střihů, časovaný návrh hudby a ruchů, dva scénáře VO s vedením hlasů a záznam nezávislé vizuální kontroly po opravách. Podrobný a kopírovatelný [handoff pro tuto fázi](prompt-pro-storyboard.txt).
