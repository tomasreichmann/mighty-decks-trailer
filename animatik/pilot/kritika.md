# Pilot 25–30 s · nezávislá střihová kontrola

**K prvnímu poslechu doporučuji A, Tiché rozhodnutí.** V jeho úvodu se hráčka dívá přes stůl, zatímco vysvětluje, proč si Úspěch nechá. „Beru“ začíná asi tři snímky před nárazem bedny. Z A má smysl převzít zvuk a úvodní společný pohled. Na samotnou volbu a její následek doporučuji kolmý detail a rampu ze 2D animatiku.

Časy v tabulce jsou sekundy od začátku pilotu. V celém traileru odpovídá 0,00 s snímku 750 a 4,00 s nárazu na snímku 870.

| Replika | A · Tiché rozhodnutí | B · Pod tlakem |
|---|---:|---:|
| Úspěch potřebuju na záchranu lodi. | 0,27–2,17 | 0,41–2,20 |
| Hraju částečný. | 2,47–3,61 | 2,56–3,62 |
| Beru zranění. | 3,90–4,79 | 4,05–4,93 |

- **A, 0,00–2,00 s.** Tváře v kontaktu, ruka jednou krátce doprovodí větu. Kolem 2,2 s hráčka sklání hlavu. Na obraz ze stolu shora bych přestřihl na 2,00 s. Na konci důvodu přes tento střih podržet i titulek.
- **A, 2,60–4,50 s.** V samotném H3 prsty uchopí pravou krajní kartu a přesunou ji doprava. Divák se nedozví, že si ponechala Úspěch a zahrála prostřední Částečný. V původním 2D detailu vidíme čitelné líce, změnu polohy ukazováku i prázdný prostřední slot po dopadu. V nativním H3 pokračuje herna až do konce a pašerákův vis chybí.
- **B, 0,60–4,90 s.** Hráčka sklopí oči téměř na začátku důvodu. Už kolem 1,5 s míří k pravému líci a gesto opakuje. To prozrazuje výběr ještě před větou o hraní. „Beru“ začíná asi jeden až dva snímky po střihu na rampu. Pro porovnání herecké naléhavosti stojí B za poslech vůči A na stejném 2D obraze.
- **Titulky.** Klipy označené 2D přebírají titulky původního pracovního hlasu. U A proto první titulek naskočí zhruba o osm snímků dříve než hlas a zmizí asi o sedm snímků dříve, než věta dozní. Pro hybrid použít samostatné intervaly z tabulky.

Porovnal jsem původní 2D záběr, oba nativní obrazy a jejich shodu se střihem. Začátky a konce vět jsem zkontroloval podle obálky signálu, pauz a zarovnání automatického přepisu. Stejný vícejazyčný Whisper small Q5_1 rozpoznal u obou tři zamýšlené věty. U A napsal „záhranu“, u B „potřebujú“. Barvu hlasu, věrohodnost češtiny a dojem skutečné hráčky má rozhodnout poslech člověkem. Kontrola v tomto rozhraní zahrnovala obraz, měření zvuku a přepis řeči.

## C · ověření střihu se Zraněním

**K projekci doporučuji C se Zraněním.** Soubor `files/hybrid-zraneni.mp4` má šest sekund a 180 obrazových snímků. První titulek naskočí v 0,27 s. Důvod hráčka dořekne na tváři a ve 2,20 s přejdeme na prst nad levým Úspěchem. Ve 2,47 s zazní výběr a prst se přesune k prostřednímu Částečnému. „Beru“ v 3,90 s připraví náraz na 4,00 s.

**4,40–5,60 s, snímky 132–167.** Pašerák visí pod hranou, dlaň se drží roztrženého plechu a na odhaleném předloktí je stopa krve. Vpravo je samostatná karta „Zranění“ s kapkou a označením „PAŠERÁK“. Vedle této karty dozní titulek „Beru zranění.“. Ve 4,80 s zmizí portrét i titulek, zatímco ruka, jméno i karta mají dalších 0,80 s na přečtení. Při šířce 390 px jsem rozeznal jak vlastníka, tak název karty. Na 5,60 s následují tři zachránění, bedna a mládě za prahem. Do volného prostředního slotu přijde Selhání.

Zkontroloval jsem oba snímky na hranici každého titulku i střihů na zranění a práh. Ve zvuku dekódovaném ze šestisekundového exportu vychází přidaný náraz na 4,000 s (korelace 0,9992 po odečtení hlasového mixu A). Automatický přepis i přes náraz zachytil důvod, výběr i celé „beru zranění“, se stejnou nejistotou u slova „záchranu“.

## C · samostatně animovaná hráčka

**Pro projekci použít `files/hybrid-vrstvy.mp4`.** V detailu tváře na f40 (1,33 s) jsou otevřená ústa, na f65 (2,17 s) se po „lodi“ dovírají. Herecké čtení použité k vytvoření obličeje mělo svůj první hlasový nástup kolem 0,48 s a konec věty kolem 2,81 s. Obraz tyto dva okamžiky mapuje na 0,27 a 2,17 s schváleného zvuku A. Uvnitř věty je zarovnání přibližné, zvlášť u „potřebuju na“. Zkontroloval jsem pohyb rtů a hranice řeči; jemnou shodu jednotlivých hlásek s tvarem úst má posoudit český posluchač.

Ve stejných dvou snímcích jsem zkontroloval hranu čelisti, rukáv i zvednutou ruku. Na obrazu širokém 390 px gesto přečtu. V posledním exportu (925 647 bajtů) rozlišuji v obou zvětšeninách čistou konturu prstů nad kartami i samostatné linie rtů a brady. Na f40 a f65 jsem v oblasti hráčky nenašel žádný pixel s převahou zeleného kanálu alespoň o 20 stupňů nad červeným i modrým. Mezi f8 a f65 se průměrná změna v ploše loga držela na 0,00 z 255, u lampy i vypravěče na maximu 0,01 a na spodní polovině tří líců 0,10. Ve výřezu úst dosáhla 30,57. Na f66 následuje detail skutečných karet. Ve f132–167 se znovu čte „Zranění“ a „PAŠERÁK“, na f168 střihneme za práh. Všech 180 obrazových snímků i délka 6,00 s prošly kontrolou; AAC pakety mají stejný kontrolní součet jako předchozí C se zraněním.

## Rozšíření masek v C · SAM 2

Pro srovnání slouží `files/detail-masky-sam.mp4`: stejná replika, čas i výřez. V původním obraze končila změna u úst a v prstech; po SAM zasahuje i tvář, čelist a zápěstí. [Záznam segmentace](actor/README.md) popisuje měření na čtyřech konkrétních snímcích. Všech 180 snímků C má stejných šest sekund a všechny pakety AAC mají stejný kontrolní součet jako před segmentací.

Nezávislý kritik v 640 × 360 přečetl postup řeč → sklopení pohledu → zvednutí prstů. Během 66 snímků zůstal vypravěč, lampa, stolek a roh krabice shodný s předchozí verzí. V původní kontrole první verze SAM byl při zvětšení patrný měkký druhý obrys u manžety a krátká rovná linka za hřbetem ruky. Jemnost obrysu i časování jednotlivých hlásek dál omezuje původní herecký záznam H3 natočený v 448 × 416.

Po opravě na pěti kontrolních snímcích (8, 24, 36, 45 a 56) kritik potvrdil jednu souvislou konturu manžety, čisté šrafování bundy i zachované postupné ohnutí prstů. Tuto verzi schválil pro pracovní náhled.
