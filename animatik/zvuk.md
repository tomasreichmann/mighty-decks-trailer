# Zvuk masterů CS a EN

`src/dialogue.json` určuje pro každou repliku vybraný mono WAV, mluvčího, text a první a koncový snímek. Konec je otevřený. Tentýž interval řídí řeč, portrét, titulek i SRT. Rozlišení časové osy je 30 fps; zvuk má 24 kHz, takže snímku odpovídá přesně 800 vzorků.

| Replika | CS [od, do) | EN [od, do) |
|---|---:|---:|
| Volání | 56–134 | 56–126 |
| Nabídka | 180–270 | 180–248 |
| Souřadnice | 276–314 | 276–309 |
| Odeslání | 330–350 | 330–342 |
| Kryt v hangáru | 500–545 | 500–530 |
| Varování | 671–711 | 671–707 |
| Důvod | 758–816 | 758–813 |
| Výběr | 824–859 | 824–851 |
| Cena | 867–894 | 873–902 |
| Povel | 930–983 | 930–980 |
| Pozvání | 1370–1441 | 1370–1423 |

V CS jsou nabídka, souřadnice, odpověď a povel k útěku čtyři vybrané [hangárové stopy](pilot/voices-hangar/README.md). Důvod, volba i cena jsou z jediného nepřerušeného čtení „Tiché rozhodnutí“, shodného s vybraným hybridem SAM. Začátek první věty je u obou jazyků na tváři v 25,27 s. V CS dozní „zranění“ v 29,80 s, v EN „injury“ v 30,07 s, zatímco zápěstí a líc už jsou v obraze. Anglický důvod, volba a cena jsou nové záběry F1, vyrobené pro délku gest. Hráčka důvod otevírá na vyšším tónu a na „ship“ klesá. Anglické čtení používá tři hlasy Supertonic 3: M2 pašerák, M4 vypravěč, F1 vyhnankyně i hráčka.

Prostor, puls a ruchy se přehrávají na samostatných stopách. Třetí prasknutí rádia na 55 otevře volání, vrčení začne na 390 a záběr na vyhnankyni přeruší úder na 534. Po zpětné vazbě na mobilní poslech pokračuje úder suchým páráním tkaniny na 538–552. Sedm úderů podrážek na 561, 574, 587, 600, 609, 619 a 630 postupně zeslábne za dveřmi. Na 870 je pod kartou skutečný zvuk bedny z H3. Jeho náběh byl izolován odečtením odpovídajícího čistého hlasu z vybraného pilotu. V EN začne tryska na 984 tiše a po 990 zesílí. Západka a přezka mají vlastní akcenty, za nimi vynikne dech mláděte. Po CTA zůstává jen prostor.

Z adresáře `animatik/` obnoví `python scripts/prepare-final-audio.py` ruchové stopy, SRT, české hlasové výřezy hybridu, manifest a samostatné padesátisekundové poslechové mixy `out/Fangs-{CS,EN}-mix.wav`. Potřebuje FFmpeg, NumPy, SciPy a přibalené zdrojové piloty. Původní pracovní čtení vznikla v místním prostředí Supertonic 3 s `scripts/generate-voices.py`. Po renderu kontroluje `python scripts/verify-audio.py` zpoždění a korelaci všech 22 replik přímo ve zvuku MP4 a ověřuje text a čas v SRT.

České volání vzniklo místně v Pocket TTS Czech s referencí téhož syntetického pašeráka jako v průzoru. Pozvání vytvořil Fish S2-Pro s referencí české hráčky z vybraného tichého H3 čtení. Při kontrolním poslechu přes model malého reproduktoru (mono 330–3350 Hz) napsal Whisper „tů tři“ a „Vytyskni si karty a zahraj si Mighty Dex.“ Jméno se foneticky blíží anglickému názvu. Povel „Teď. Plný boční tah.“ zůstal z původního F1 čtení, u nějž rozpoznávač zachoval „plný boční“ a poslední slovo napsal „tach“. U zkoušky stejné věty hlasem Fish přepsal „Lenný bočný táh“. Rozdíl barvy hlasu mezi českým povelem, výběrem karty a pozváním i česká výslovnost jsou pracovní omezení.

Whisper small Q5_1 dostal u 22–36 s jediný smíchaný kanál přes stejné pásmo bez scénáře. Anglické varování, důvod, volbu, cenu i povel přepsal přesně, a stejně rozpoznal tři finální anglické záběry v samostatném testu s nárazem. V CS rozpoznal „Hraju částečný, beru zranění“, v dalších slovech napsal „boled“ a „záhranu“. Jednotlivé věty českého hybridu včetně ruchů mají proti pilotu korelaci 0,9978–0,9997. Tyto kontroly měří čas, energii, intonaci a přepis. Rozhraní autora zvuku nepřijímá audio, takže hodnocení přízvuku a emocí lidským uchem zůstává otevřené.

Hudební varianty, autorské kredity a postup obnovy popisuje [hudba traileru](public/audio/music/README.md).
