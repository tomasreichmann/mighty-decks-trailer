# České hlasy pro dohodu a hangár

Čtyři čisté pracovní stopy používají dvě samostatná herecká čtení. Pašerák má čas oddělit prosbu od nabídky cesty, na souřadnice odpovídá krátce. Vyhnankyně pronese požadavek klidně a povel k útěku s větší naléhavostí. Pro každou postavu pocházejí obě vybrané repliky z jediného nepřerušeného čtení.

| Soubor | Mluvčí a replika | Snímky [od, do) | Délka |
|---|---|---|---:|
| cs-02.wav | Pašerák · Vytáhni nás. Znám cestu přes blokádu. | 180–270 | 2,974 s |
| cs-03.wav | Vyhnankyně · Nejdřív souřadnice. | 276–314 | 1,260 s |
| cs-04.wav | Pašerák · Posílám. | 330–350 | 0,649 s |
| cs-05.wav | Vyhnankyně · Zadržím ji. Běžte! | 500–545 | 1,477 s |

Všechny soubory jsou PCM 16 bitů, mono, 24 kHz. První slabika „Běžte!“ začíná kolem snímku 529. Ve střihu jí zbývá pět snímků do kovového úderu na 534. Časování používá původní rychlost řeči.

## Opakování a výběr

Samostatné ComfyUI na portu 8188 použilo lokální MiniMax H3 FL2VA INT8 a osm kroků s akcelerační LoRA. Vstupní portréty jsou ze dvou spodních polí `reference/planches/portraits.png`, středově oříznutých na 448 × 416. Pro nový běh nahraj správné PNG ze složky `source/` a spusť příslušný API graf z `graphs/`. Uzel 17 zapisuje nativní stereofonní FLAC, ze kterého je možné jednotlivé repliky znovu vybrat.

| Graf | Seed | ID místní úlohy | Výsledek |
|---|---:|---|---|
| smuggler | 916305 | `70f8992d-6d7c-4013-b5e5-606fc68e67a0` | V odpovědi ASR opakovaně odhadovalo „pozílám“. |
| smuggler-b | 916624 | `2d746613-14b7-493b-8371-1cc3a4e48072` | Vybrány nabídka i odpověď. Po zápisu kompletního výstupního FLAC bylo ukončeno čekání na doprovodné video. |
| exile | 916408 | `86667132-51ab-4829-a4d7-7f55f3beddab` | Vybrány požadavek na souřadnice i oba povely. |
| exile-b | 916726 | `e3086834-d602-4638-92fa-9d541606a72c` | ASR rozpoznalo první požadavek, ale druhý povel přepsalo jako „Zadrží mě“. |

Příkaz `python animatik/pilot/voices-hangar/prepare.py` znovu připraví čtyři WAV z uložených FLAC. Střihy a cílové hlasitosti každého mluvčího jsou v `takes.json`. Skript použije FFmpeg pro převod na mono, odstranění hlubokého dunění pod 58 Hz a změření hlasitosti. Zesílení je pro každou repliku konstantní, na okrajích je dvoumilisekundové ztišení.

**Kontrola srozumitelnosti.** Český Whisper small Q5_1 na CPU dostal po sestavení všech čtyř výstupních WAV pouze zvuk a jazyk. Vrátil „Vytáhní nás. Znám cestu přes blokádu. Nejdřív souřadnice. Posílám. Zadržím jí. Běžte.“ Délka samohlásky na konci „vytáhni“ a u „ji“ zůstává k posouzení při poslechu. V izolovaném zvuku „Nejdřív souřadnice“ rozpoznal přesně. Délky a časové hranice byly změřeny z dekódovaných stop. Přirozenost češtiny má při projekci posoudit posluchač.
