# Stůl pro pilot C

`TableStage` sestaví pevný polocelek v souřadnicích 1920 × 1080. Podklad `00-pozadi` nese pokoj, desku, dobírací balíček a roh krabice. Nad ním stojí samostatný vypravěč `01-vypravec`. Při nižším výstupním rozlišení zmenši celého rodiče kolem levého horního rohu.

```tsx
import { TableStage } from "../src/TableStage";

<TableStage locale="cs" actress={actressLayer} foreground={crossingHand} />
```

`actress` přijímá registrované tělo a hlavu. Nad nimi drobná záplata dřeva vyčistí tři původní otisky karet včetně zbytků, které zasahují do masky těla. Pak se každá fyzická karta vykreslí zvlášť. Pro gesto před kartami můžeš dát ruku do `foreground`. Oba vstupy jsou volitelné. `cardStyles` dovoluje upravit pohyb jednotlivých karet podle ID.

| Objekt | Levý horní roh (x, y) | Velikost výřezu | Líc |
| --- | --- | --- | --- |
| U2 | 551, 723 | 122 × 59 | Úspěch / Success |
| C2 | 678, 722 | 115 × 59 | Částečný úspěch / Partial Success |
| S1 | 794, 718 | 122 × 61 | Selhání / Fumble |
| Dřevo pod kartami | 545, 710 | 381 × 82 | Jedna společná záplata s průhledností kolem tří otisků |

Každý jednotlivý PNG výřez obsahuje vnější hranu, kontaktní stín a perspektivně promítnutý lokalizovaný líc ze schváleného soutisku. Kontury a registraci určuje `registration.json`. Záplata pokračuje v kresbě dřeva z levého a pravého sousedství každého řádku a přidává jemnou strukturu z desky pod kartami.

## Příprava a kontrola

Z adresáře `animatik` spusť následující příkazy. Generátor používá Pillow a NumPy.

```powershell
npm run assets
python pilot/table/prepare.py
```

První příkaz zkopíruje zdrojové vrstvy místnosti a vypravěče. Druhý vytvoří sedm oříznutých souborů v `public/pilot/table` o celkové velikosti 129 314 bajtů pro oba jazyky. Při každém spuštění přidá v paměti původní vrstvu hráčky, pak porovná každý pixel s původním širokým obrazem a schváleným lokalizovaným soutiskem.

| Porovnání všech 2 073 600 pixelů v každém jazyce | Největší rozdíl RGB kanálu (0–255) | Průměrná absolutní odchylka kanálu |
| --- | ---: | ---: |
| Složení ve zdrojovém rozlišení v Pillow, CS i EN | 0 | 0 |
| Vyrenderovaný PNG z Remotionu v Chromiu, CS i EN | 2 | 0,04551 |
