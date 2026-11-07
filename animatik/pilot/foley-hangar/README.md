# Hlas šelmy v hangáru

Oba původní výkony vytvořil místní MiniMax H3 FL2VA na RTX 3090 ze stejné kresby tlamy. Uzel 17 uložil bezztrátové FLAC, 32 kHz stereo, 4,45 s. Pro opakování nahraj `md-beast-foley.png` do místního ComfyUI a spusť příslušný API graf. Oba používají osm kroků a turbo LoRA.

| Graf a zvuk | Seed | ID úlohy | Použitá část |
|---|---:|---|---|
| `charge.json`, `charge.flac` | 714512 | `dac7f131-367b-464b-b0dc-e6d9fb184aea` | Dvě hlasové fráze na přiblížení a výpad, včetně krátkého nádechu mezi nimi. |
| `throat.json`, `throat.flac` | 714511 | `0fa9539c-3b15-47dd-90ad-e6fa6e45f6cc` | Dva oddělené hrdelní zvuky na konci nahrávky. Použity za dveřmi, v držení zbraně a po povelu. |

Časování a práci s perspektivou reprodukuje `python scripts/generate-hangar-impact.py` z adresáře animatik. Výstup `public/audio/hangar-impact.wav` je 48kHz mono PCM16 od f390 do f660. Za dveřmi slyšíme filtrovaný hlas a chvění. Na f420 se otevře přímý zvuk a dvě časné odrazové plochy. Při výpadu se zkrátí prostorový dozvuk, na f460 tělo narazí na pažbu. Spodek kontaktu pochází z krátkého filtrovaného úseku staršího záznamu H3 `../media/h3-impact.wav`. Samostatný zásah drápu na f534 odkryje trhanou látku. Hlavní zvuk vláken přijde po poslední souhlásce rozkazu.

**Kontrola nástřelu CS.** Nezávislý model YAMNet označil v izolovaném `charge` obě vybrané fráze jako řev velkých koček; nejsilnější výsledek v okně od 1,44 s byl 0,99. Podobný výsledek dal u závěru `throat`; ve střední části častěji rozpoznával motor. Při kódování hotového šestnáctisekundového nástřelu začala replika na f500, korelace s českým hlasem byla 0,989. Přepis finálního AAC zachytil „Zadržím ji, běžte!“ v plném pásmu a „Zadržím ji. Běžte!“ také po omezení na mono pásmo 370–3900 Hz. V tomto pásmu měly ruchy v prvním úseku za dveřmi přibližně −44 dBFS RMS, při nástupu −32 a při kontaktu na f460 −23. Vnímanou hrozivost a barvu hlasu má určit poslech divákem.
