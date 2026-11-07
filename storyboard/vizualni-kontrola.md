# Vizuální kontrola storyboardu

## První čtení bez zvuku a scénáře

V obou jazycích jsem četl 13 samostatných obrazů v pořadí odkazů galerie, nejdříve česky, potom anglicky. Na první průchod jsem zmenšil celé obrazy na šířku 390 px a skryl názvy souborů i popisy galerie. Odpovědi jsem zaznamenal před otevřením scénáře a handoffu. Anglická verze byla druhé čtení stejného děje.

- Hráčka si schovala **Úspěch / Success** na záchranu lodi. Říká to u stolu, později je stejná karta vytažená při povelu k bočnímu tahu.
- Na rampě hrála **Částečný úspěch / Partial Success**. Při volbě to říká titulek a v dalším obrazu prostřední karta vystoupí nad ostatní. Samotná špička prstu je u levého horního okraje prostřední karty.
- Na rampě utrpěl **zranění Pašerák / Smuggler**. Visí z okraje, na předloktí má krev a jeho role je přímo nad kartou. Dříve se u nestvůry objevilo jiné zranění označené **Vyhnankyně / Exile**. Ve dveřích pak všichni tři projdou.
- V kufru jsou krátká čepel a kovový hrudní plát. Karty je pojmenují **Lehká zbraň a Těžká zbroj / Light Weapon and Heavy Armor**. Vedle plátu je živě vypadající růžový stočený předmět. Z malého obrazu není jasné, zda do kufru patří.

## Kontrola finálních exportů · 6. listopadu 2026

Kontrolu vedl samostatný agent mimo výrobu exportů. Po prvním čtení jsem otevřel všech 26 originálů v rozlišení 1920 × 1080, porovnal je se [scénářem v5](scenar-v5.md) a [zadáním](../handoff/START.md) a znovu prohlédl obě upravené dvojice v originále a ve zmenšení 390 × 219 px (Pillow, Lanczos). Šířka 390 px platí pro jeden celý obraz bez ořezu.

| Obraz | Co je vidět v CS i EN |
|---|---|
| Volání a dohoda | První portrét a titulek patří Pašerákovi. U průzoru mluví Vyhnankyně. Obličej za sklem, prsty na páce a obě další karty jsou volné. Dva Úspěchy při dohodě odpovídají dvěma kartám v počáteční ruce. |
| Hangár | Čelisti svírají pažbu, obě rukavice jsou čitelné. Škrábnutí na předloktí a označení Vyhnankyně nad kartou určují příjemkyni. Karta je napravo od hlavně. |
| Rampa a stůl | Za varování odpovídá Vypravěč. Společný pohled přes stůl je první záběr obou skutečných tváří. Oči, ruce a vybraný líc zůstávají viditelné. Prst míří k prostřední kartě, i když mezi nehtem a lemem zůstává úzká mezera. |
| Dopad, zranění a práh | Na opraveném poli 04c říká Hráčka „Beru zranění.“ / „We take the injury.“ Titulek ponechává volné místo u dlaně a u prostřední karty. Šrám je slabě viditelný už zde, následující detail ho spolu se jménem příjemce zvýrazní. Za prahem jsou tři lidé, mládě a bedna. Muž si přidržuje zraněnou paži. |
| Boční tah | Zvedá se jediný Úspěch, zůstávají dvě Selhání. Rukavice ovládající páku i titulkovaný povel jsou vidět současně. |
| Kořist a logo | Spojnice vedou z levé karty přímo na čepel a z pravé na kyrys. V originále je u přezky rozpoznatelný čenich mláděte a nad pantem obvázaná ruka s pěti prsty. Obě karty se vracejí vlevo u loga. Vpravo jsou všechny čtyři středověké karty, názvy odpovídají jazyku. Kořist i logo jsou bez titulku a portrétu mluvčího. |
| CTA | Vlevo je krabice na osvětleném dřevě, vpravo QR a adresa. Opravená dvouřádková adresa se dá přečíst i při 390 px. Portrét a celá závěrečná věta v obou jazycích mají vlastní prostor dole. |

**Čtení při 390 px.** Dialogy, trojici výsledků a vybraný prostřední název jsem přečetl bez zvětšení. Roli u karty Zranění pomáhají přečíst tmavé obrysy písma, určující je zároveň postava s řeznou ranou. Pravidlový odstavec Selhání a drobné kategorie karet už při této šířce vyžadují zvětšení. Pro pochopení volby stačil název a symbol. Do okraje ani do další karty text nepřetéká. Anglické volání má tři řádky a končí uvnitř obrazu.

**QR.** OpenCV 4.8.1 (QRCodeDetector.detectAndDecode) četlo celý hotový CTA snímek přímo z obrazových bodů, bez předběžného ořezu či načítání zdrojového QR. Všechny čtyři pokusy po opravě (CS/EN, 1920/390 px) vrátily přesně adresu [Mighty Decks](https://board-game-prototypes.netlify.app/mighty-decks). Cíl i obě doplňující adresy v popisu vrátily při HTTP GET stav 200. Kontrola nezahrnovala fyzický fotoaparát, vytištěný kód ani stažení karet.

**Tabule.** Oba barevné přehledy mají 2048 × 2583 px a 13 polí v pořadí galerie. Detail rampy má 2048 × 1110 px a šest polí od pádu dílu po přechod prahu. Všechny tři tabule ukazují opravenou repliku o zranění, oba velké přehledy mají opravenou CTA. Popisky končí ve svém sloupci, včetně anglické věty o výběru prostřední karty. V originálních výřezech časomíry je v CS desetinná čárka a v EN tečka. [Česká tabule](storyboard-v5.png) · [Anglická tabule](storyboard-en.png) · [Detail rampy](rampa-volba-dopad.png)

**K ověření v animatiku.** Snímky dosvědčují volbu karty a příjemce zranění. K posouzení zbývá délka držení výsledku, pohyb prstu na kartu, pořadí dopadu bedny a řezu do předloktí, odhození a dobrání, přepnutí portrétu na první slabice a pětisekundová výdrž QR. V poli dohody je zachycena replika Vyhnankyně. Přepnutí na obě repliky Pašeráka se dá posoudit až v čase. Katalogovou shodu karabiny s konkrétním lícem nelze z pole hangáru určit.

## Opakovaná kontrola herny · společný polocelek 04b

V nových [CS](screens/cs/04b-stul-celek.png) a [EN](screens/en/04b-stul-celek.png) exportech jsem při 1920 i 390 px viděl obě tváře v kontaktu přes stůl, za nimi prázdnou modrou stěnu mezi knihovnami. Větve břečťanu zmizely. Mosazná lampa má patku na samostatném stolku vedle hrnku a knih. Pod rukou hráčky leží tři malé karty, u vypravěče je balíček. Do pravého okraje zasahuje pouze část barevné krabice. Celá replika, role, portrét i rohové logo jsou čitelné a ponechávají ruce a obličeje volné. Výřezy obou přehledových tabulí a šestipolí rampy obsahují nový polocelek.

**Návaznost tří karet po opravě.** V předchozím polocelku byly na kartách krajina, tvor a věž. V posledních exportech zabírají jejich místo skutečné líce ve správném pořadí. Sazba bere Úspěch, Částečný úspěch a Selhání z příslušné jazykové sady. Ve výřezu originálu sledují desku stolu a teplé světlo lampy. Při 390 px jsem rozeznal tři drobné karty, výběr prostřední odhalí až kolmý detail. Oprava je také na obou přehledových tabulích a v detailu rampy. Následující záběr volby v CS i EN se při pixelovém porovnání s prvním slepým čtením ve 390 px shoduje. Původní nález je uzavřen.
