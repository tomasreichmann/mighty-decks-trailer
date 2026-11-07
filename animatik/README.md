# Mighty Decks · Fangs in the Sun

Dvě jazykové kompozice sdílejí 13 obrazů, 1920 × 1080, 30 fps a 50 sekund. Pohyb šelmy je v obou výchozí. Volba u stolu používá vybraný hybrid C: tvář do 816, jediný prostřední líc do 870, náraz, od 882 zraněný pašerák, od 918 bezpečný práh. Na 930 se obě verze vracejí do kokpitu.

Lokální přehrávač: [celý film CS](http://127.0.0.1:3118/files/Fangs-CS.mp4), [celý film EN](http://127.0.0.1:3118/files/Fangs-EN.mp4). Pro rychlé připomínky je vyříznutý úsek 22–36 s: [CS](http://127.0.0.1:3118/files/decision-CS.mp4) nebo [EN](http://127.0.0.1:3118/files/decision-EN.mp4).

## Přehrání a export

Ve Windows s Node.js 24 spusť z kořene checkoutu:

~~~powershell
cd animatik
npm ci
npm run dev
~~~

Otevři [české Studio](http://localhost:3117/Fangs-CS) nebo [anglické Studio](http://localhost:3117/Fangs-EN). Mezerník spouští a zastavuje přehrávání. Pro samostatné přehrání jsou připravené pracovní kopie [CS MP4](out/Fangs-CS.mp4) a [EN MP4](out/Fangs-EN.mp4). Každá má vypálené titulky, pro střih jsou zde také [CS SRT](out/Fangs-CS.srt) a [EN SRT](out/Fangs-EN.srt).

~~~powershell
npm run render
npm run lint
node scripts/check-hand.mjs
npm run verify
python scripts/verify-audio.py
python scripts/publish-review.py
~~~

Přehrávač na tomto počítači obsluhuje `python scripts/serve-pilot.py`. Exporty v `out/` fungují i samostatně. Změnu výběru hlasů, časů a SRT řídí `scripts/prepare-final-audio.py`; zdrojové repliky jsou již uložené a k renderu se negenerují.

Příkazy dev a render připraví lokální obrazy z reference a storyboardu. Samostatný export jednoho již připraveného jazyka umožňují příkazy npm run render:cs a npm run render:en. Pro kontrolu exportů skripty používají FFmpeg a FFprobe v PATH a Python s NumPy, OpenCV, Pillow a SciPy. Hlasy a ruchy jsou uložené jako WAV v public/audio a přehrávání funguje bez syntézy. Postup obnovy hlasů je ve scripts/generate-voices.py, prostředí, pulsu a ruchů ve scripts/generate-effects.py.

## Výrobní podklady

- [Společný střih](../storyboard/strih.json) určuje hranice obrazů a okamžiky zahrání karet. Přímé přetočení na libovolný snímek počítá stav ruky z fyzických ID.
- [Skutečné řečové intervaly](src/dialogue.json) řídí portréty, titulky i zvuk. SRT vzniká z týchž nástupů a délek. Vyhnankyně a hráčka mají hlas F1, pašerák M2 a vypravěč M4.
- [Pracovní pózy a chybějící mezifáze po záběrech](plates.md) zahrnují průzor, vložku karabiny, řez a vytažení přes práh. Na snímcích 460–479 má kontakt čelistí s pažbou celý obraz.
- [Ověření pracovních kopií](kontrola.md) shrnuje technické měření, mobilní čitelnost a omezení poslechu.
- Cílová stránka nabízí [pravidla](https://board-game-prototypes.netlify.app/mighty-decks/rules) a [tisk karet](https://board-game-prototypes.netlify.app/mighty-decks/preparing-the-game/outcome-cards).

## Pilot s MiniMax H3

[Lokální porovnání A/B/C](http://127.0.0.1:3118/) nabízí původní české čtení, dvě hrané varianty a u každé tentýž zvuk s původním obrazem. V C stojí herna, vypravěč a oděv hráčky v 2D. H3 dostává zvlášť připravený obraz profilu a ruky na zeleném pozadí. Průhledné pohyblivé části se složí se třemi lokalizovanými kartami, rohovým logem a titulky až v Remotionu. C používá hlas z pokusu A, samostatný náraz bedny a kreslený detail volby, zranění a záchrany. Prvních pět sekund lze srovnávat přímo, C pokračuje do šesté sekundy za práh. Pro aktuální sestřih jsou rozhodující [poznámky nezávislého kritika](pilot/kritika.md) a [záznam generace](pilot/generovani-h3.md). Výběr se ukládá v tomto prohlížeči.

Pro zopakování variant na stroji s příslušnými modely jsou v pilot/graphs tři původní grafy H3 a v pilot/inputs oba vstupní obrazy. Pro sestavení z již uložených médií použij z adresáře animatik následující příkazy. Srovnávač používá Python s aiohttp a naslouchá na 127.0.0.1:3118.

~~~powershell
npm run assets
python pilot/prepare-review.py
python pilot/table/prepare.py
node pilot/prepare-actor.mjs
npx remotion render pilot/Hybrid.tsx Hybrid out/pilot-picture.mp4 --scale=0.3333333333333333 --concurrency=3 --muted
ffmpeg -y -i out/pilot-picture.mp4 -i pilot/files/hybrid-zraneni.mp4 -map 0:v:0 -map 1:a:0 -c copy -movflags +faststart pilot/files/hybrid-sam.mp4
python pilot/prepare-review.py --publish-only
python scripts/serve-pilot.py
~~~

Původní C zůstává uložené jako `pilot/files/hybrid-vrstvy.mp4`. [Detail masek](http://127.0.0.1:3118/files/detail-masky-sam.mp4) srovnává první repliku před a po segmentaci SAM 2. Výřezy používají stejné souřadnice i čas. Postup přípravy masek je v [podkladech herečky](pilot/actor/README.md).

Úsek Dohoda a Hangár lze přerenderovat z hlavní kompozice příkazem `npx remotion render src/index.ts Fangs-CS pilot/files/dohoda-hangar-selma-cs.mp4 --frames=180-659 --scale=0.5`. Pro angličtinu použij `Fangs-EN` a výstup `dohoda-hangar-selma-en.mp4`. Potom spusť `python pilot/prepare-review.py --publish-only`, aby se náhled aktualizoval ve srovnávači.

Šelmu slyšíme za dveřmi od snímku 390. V hangáru se rozběhne zleva a na 460 (15,33 s) narazí do pažby. Dráp poraní vyhnankyni na 534 (17,80 s), s nástupem viněty. Ruchy z nahrávek MiniMax H3 obnovíš příkazy `python scripts/generate-hangar-impact.py` a `python scripts/generate-effects.py` v tomto pořadí. Při regeneraci hlasů mají nahrávky v `public/audio/performance/` přednost před pracovní syntézou.

Pro alternativu s pohybem tlap a hlavy přidej k příkazu render `--props=pilot/beast-motion/review-props.json` a použij název `dohoda-hangar-selma-pohyb-cs.mp4`. Pohyb na snímcích 431–459 používá 29 průhledných obrázků v `public/hangar/beast-motion/`. Obnovíš je z bezztrátového záznamu příkazem `python pilot/beast-motion/extract.py` a zkopírováním výsledných souborů z `pilot/beast-motion/frames/`. Kamera, světlo, zbraň, karty i zvuk se řídí stejným střihem jako ve 2D verzi.
