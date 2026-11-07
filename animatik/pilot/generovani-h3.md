# Jak zopakovat dvě zkoušky MiniMax H3

Pro aktuální **C** slouží [samostatný herecký vstup](actor/md-actor-green.png) a [graf H3 pro profil a ruku](actor/h3-actor.json). Zdroj má 448 × 416 px a obě části leží na zeleném pozadí v původní vzájemné poloze. Výstup se vyklíčuje do 53 průhledných snímků. Na [časových bodech řeči](actor/timing.json) se pohyb úst přizpůsobí nahrávce A. Kompozice skládá tyto snímky nad [statickou scénu a samostatné karty](table/README.md). Ostatní záběry C jsou sestavené z 2D kreseb. Původní celoplošné zkoušky A a B zůstávají ve srovnávači pro poslech obou přednesů.

Oba pokusy začínají týmž českým obrazem v `inputs/md-ink-table-640.png`. Vstup vznikl spojením `reference/planches/table.png` a `storyboard/overlays/cs/table-faces.png` a středovým ořezem na 640 × 352 px. První snímek dostává H3 jako obrazovou podmínku. Pohyb postav, další snímky, hlas i ruchy vytváří model v jednom průchodu.

| Zkouška | Režie | Seed | ID místní úlohy |
|---|---|---:|---|
| A · Tiché rozhodnutí | Blízký, nízko posazený hlas, chvilka na rozmyšlenou, opatrné položení karty a vzdálený náraz. | 716305 | `1da47cdc-4393-466f-af08-16ec592b2442` |
| B · Pod tlakem | Zrychlená, lehce zadýchaná obava o loď. Hlas se zpevní při přijetí zranění, úder karty je důraznější. | 716408 | `274e8b21-247d-48ab-b70f-00524bc8b525` |

Vstupní pokyn pro obě zkoušky obsahuje doslovnou repliku „Úspěch potřebuju na záchranu lodi. Hraju částečný. Beru zranění.“ Tabulka popisuje zadání režie. Skutečně vyslovenou češtinu je třeba hodnotit podle výsledného zvuku.

1. V místním ComfyUI na portu 8188 nahraj vstupní PNG do kořene `input/` pod dodaným názvem.
2. Ověř a postupně spusť API grafy [A](graphs/h3-quiet.json) a [B](graphs/h3-urgent.json). Oba vycházejí z dříve ověřeného místního grafu FL2VA INT8 s akcelerační LoRA pro osm kroků. Modely, uzly, volba sampleru, celé prompty a seedy jsou přímo v grafech. Oba byly před výpočtem ověřeny v místním ComfyUI bez chyb a varování.
3. Uzel 14 zapisuje nativní MP4 s H.264 a AAC, uzel 17 ukládá přímo výstup zvukového dekodéru do bezztrátového FLAC. Ulož MP4 do `media/h3-quiet.mp4` nebo `media/h3-urgent.mp4` a převeď příslušný FLAC do WAV příkazem `ffmpeg -i vstup.flac -c:a pcm_s24le vystup.wav`. WAV zůstává stereofonní v původních 32 kHz, bez vyrovnání hlasitosti a dodaných ruchů.
4. Z kořene projektu spusť `python animatik/pilot/prepare-review.py`. Připraví pětisekundové výřezy pro porovnání se stejným úsekem českého animatiku (25,00–30,00 s). Neupravené výstupy v `media/` zachovávají celých 124 snímků při 24 fps.

## Výsledné soubory

Místní výpočet na RTX 3090 trval 92,36 s pro A a 79,59 s pro B. Měření obou MP4 pomocí ffprobe dalo 640 × 352, H.264, 124 snímků při 24 fps a obraz o délce 5,166667 s. Obě WAV mají 5,175 s, dva kanály, 32 kHz a PCM 24 bitů.

V A se hráčka po chvíli odvrátí od vypravěče ke stolu, vezme krajní kartu a odloží ji stranou. V B se rychle předkloní, ukáže na krajní kartu a znovu na ni poklepe. Pro animatik je podstatné ponechat v původním 2D střihu pohyb prstu z levé karty na prostřední, čitelné líce, dopad a zranění. Obě nativní zkoušky ukazují celou výměnu z jediného pohledu na stůl.

## Samostatný náraz bedny

Při další generaci použij [graf pro náraz](graphs/h3-impact.json) a první obraz `inputs/md-ink-crate-640.png`, středový ořez původní kresby `reference/planches/ramp-jump.png`. Seed 716509, úloha `7d7120c2-87a8-48cd-8c51-d7ea5ef1a2f5`, výpočet 52,35 s. Soubor `media/h3-impact.mp4` má 56 snímků při 24 fps, souběžný zvuk `media/h3-impact.wav` 2,325 s při 32 kHz stereo. Zadání popisuje jeden náraz dřevěné bedny o ocelový lem s krátkým zachvěním přezky.

Hlavní hrana nárazu ve WAV začíná v 0,968 s. Během následujících 4 ms vzroste vrchol z −16 dBFS těsně pod nulu. Pro dopad přesně ve 4,000 s výřezu lze tedy celý soubor umístit na 3,032 s. Další výrazný mechanický úder je v 1,46 s zdroje. Pro jediný náraz pod hlasem lze vzít úsek přibližně 0,94–1,35 s a posledních 65–100 ms ztišit do ticha.
