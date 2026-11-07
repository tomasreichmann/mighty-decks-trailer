# Jak sestavit první animatik

V projektu jsou ilustrace, lokalizované líce a statické kompozity. Tento plán popisuje první přehratelnou verzi v Remotionu: má ukázat, zda divák stihne pochopit volbu, její cenu a důvod v obou jazycích.

## Skladba obrazu

| Komponenta | Vstup a odpovědnost |
|---|---|
| `Trailer` | Dvě kompozice `Fangs-CS` a `Fangs-EN`, tentýž React strom. Parametr `locale: 'cs' \| 'en'`; společný střih 1920 × 1080, 30 fps, 1500 f. |
| `Shot` | Tabulka záběrů: ID, [in, out), ID podkladu, počáteční a koncová póza, střihová vazba. Jedna Remotion Sequence na řádek [režie](../storyboard/pohyb-a-strih.md). Lokální snímek řídí kameru, masku a vrstvy; přechod se musí vejít dovnitř intervalu. |
| `ScenePlate` | Čistá kresba, případně maskované popředí a druhá póza. Pořadí: pozadí → pohybující se objekt → přední hrana/ruka. Pozice vycházejí z exportu 1920 × 1080. Kamera transformuje jen tuto skupinu. |
| `Hand`, `CardPlay` | Tři sloty a události pick / hold / resolve / draw. Stav je funkcí absolutního snímku, ne historie přehrání. Ukládej zvlášť typ líce a fyzické ID (např. U₂ i U₃ mají líc success). Po pick vykresluje líc pouze CardPlay. Fyzický stůl čte stejný stav. |
| `Injury`, `LootPair` | Zranění má vlastníka a pozici mimo ruku. Kořist má dvojice předmět → líc → bod spojnice; bez posunu vůči kresbě. |
| `Dialogue`, `CornerLogo` | Jeden cue určuje mluvčího, roli, portrét, text i interval. Titulek a portrét jsou jen po dobu repliky; řádkování kontrolovat pro každý jazyk. Logo sdílí při přechodu do S07 stejnou instanci nebo navazující koncovou pózu. |
| `LogoSpread`, `CallToAction` | S07: papír, logo a dvě skupiny líců. S08: samostatný stůl, kontaktní stín, původní krabice, přesná URL a QR; nepoužívat vstupní animaci. Na CTA se může měnit pouze Dialogue. |
| `SoundTimeline` | Odděleně pracovní VO podle jazyka, ruchy, prostor a puls. Zvukové značky používají absolutní snímky stejných událostí jako obraz. SRT se odvodí ze stejných řečových cue jako titulky. |

**Strojový podklad:** [strih.json](../storyboard/strih.json) už obsahuje rozměr, fps, intervaly a zdroje 13 obrazů, popisky tabulí a čtyři hry. `pick` je odtržení, `hold` první ustálený snímek, `resolve` začátek zániku s následkem a `draw` začátek dobrání. Řetězce U2 / C2 / S2 odpovídají zápisu U₂ / Č₂ / S₂. Popisek obrazu slouží tabuli; může shrnovat ticho a nenahrazuje časované titulky VO.

**Příklad napojení:** na 870 se mění záběr ze stolu na šachtu. Oba obrazy odkazují na tutéž událost hry Č₂. U₂ zůstává v prvním slotu; Č₂ mizí s nárazem a do prázdného slotu přijde S₂ až po vytažení. Skok přehrávače přímo na 930 musí dát stav U₂, S₂, S₁ bez přehrání kteréhokoli předchozího záběru.

## Jak animovat rozloženou kresbu

Pro obrazovou generaci H3 připrav vstup z částí, které v daném záběru skutečně hrají. U stolu potřebují pohyb mluvící ústa, pohled a gesto ruky. Připrav je na jednobarevném pozadí, uchovej jejich souřadnice a po generaci vrať pohyb jako průhlednou vrstvu nad kresbu. Pokoj, desku, druhou postavu a klidné části oděvu vykresli z původních 2D vrstev. Fyzické karty mají vlastní lokalizované líce pod gestikulující rukou. Logo, herní karty, portrét a titulek přidávej až v kompozici. V kolmém detailu stačí původní deska, tři samostatné líce a posun kreslené ruky podle snímku. Ruch z H3 lze použít samostatně i nad čistě 2D záběrem.

Pro `ScenePlate` použij [manifest vrstev](../storyboard/vrstvy/manifest.json) a [lokální prohlížeč](../storyboard/vrstvy/index.html). ID rozkladu odpovídá názvu zdrojového PNG bez přípony. Do modelu patří čistá ilustrace, nikoli lokalizovaný export. Stejné rastrové vrstvy pak poslouží pro CS i EN, zatímco titulky a skutečné líce zůstanou ostré. Na disk ukládej vrstvy v původní registraci celého plátna; předek s průhledností patří nad doplněný zadní plán. Maska samotná nevytvoří chybějící kresbu za posunutým objektem.

Detail `05a-zraneni` sdílí vrstvy `ramp-jump` s předchozím záběrem. Naměřené přerámování z exportu je `x′ = 1,364x − 170`, `y′ = 1,364y − 233` v pixelech plátna. Transformuj jejich společného rodiče kolem levého horního rohu. Karta Zranění a jméno pašeráka mají vlastní pozici na plátně; při střihu na detail se nezvětší s předloktím. Pro ostatní příběhové obrazy bez `plateTransform` je registrace 1:1.

Na snímku bez pohybu nejdřív porovnej složení s předlohou. Poté vyzkoušej krajní polohu: zkontroluj oblast za ramenem, hranou lodi nebo bednou, kontakt ruky s pákou a hrany plátna. Začni od nulového posunu; vektor u vrstvy je vyzkoušená mez pro **relativní** pohyb, ne povinná animace v každém záběru. Nemá-li výstup čisté odkrytí, svaž související vrstvy nebo použij původní kresbu. Žádným globálním zoomem nezachraňuj zdvojený obličej.

U rozhovoru drž herní stůl a ruce ve společné rovině, divák má čas číst pohled mezi postavami. Na desku polož průhledný soutisk [CS](../storyboard/overlays/cs/table-faces.png) nebo [EN](../storyboard/overlays/en/table-faces.png) ve velikosti plátna. Překrývá pouze vnitřky tří nakreslených karet skutečnými líci; musí se pohybovat společně s deskou. V kokpitu může rám stát, zatímco za ním projde silueta nebo troska. V hangáru nesmí relativní posun oddělit čelisti od pažby. Nad bednou se nehýbou spojnice nezávisle na nálezu. S07 poskládej z papíru a původních karet; je to grafická kompozice a rozklad modelem nepotřebuje. Na CTA není posun vhodný ani tehdy, když rozklad herny vyjde dobře.

## Podklady a chybějící mezifáze

Podklady v tabulce jsou v `reference/planches/`. Tabulka rozlišuje zdrojové kresby a změny děje, které ani dobré oddělení vrstev nenahradí. Pro kontrolní exporty každý nový záběr porovnej s odpovídajícím PNG v [galerii](../storyboard/screens/index.html). Složené PNG lze použít pro první časovací střih. Pokud chceš hýbat kartou nebo přepnout repliku, začni čistou kresbou; dvojí logo, karta nebo zapečený titulek by pohyb prozradily.

| Úsek | Použít | Co připravit nebo jak natočit pracovní náhradu |
|---|---|---|
| 01–02 | opening.png, hatch.png | V úvodu oddělit korvetu, rám a slunce podle ověřených vrstev. Zápěstí, příjem souřadnic a otevřený průzor potřebují druhou pózu; přesunutí stejné kresby neotevře dveře. |
| 03 | hangar.png | Vybrat katalogový líc **odpovídající viditelné karabině**, potvrdit CS i EN. Sada v repozitáři tento pár nedokládá. Do té doby ponechat vložce její čas a podržet samotnou zbraň; nezaměnit za odměnu Lehká zbraň. Kryt → roztržený rukáv střihnout mezi pózami. |
| 04 | ramp.png, table.png, over-shoulder.png, ramp-jump.png, rescue.png | Pád dílu vyžaduje stav před a po utržení. Ve společném pohledu zachovat tři drobné nečitelné karty u hráčky, balíček a roh krabice. V kolmém detailu skutečné lokalizované líce; pod samostatnou vrstvou ruky a jejího stínu je připravená čistá deska pro přesun přes celý slot. Pro řez použít samostatný detail místa dotyku; vis a bezpečný práh nesmí splynout. |
| 05–06 | thrust.png, loot.png | Pohyb oddělit za sklem; pokud nejde udělat čistý okraj, úhyb střihnout na druhou pózu. Bedna je již otevřená, její víko neotáčet jako ploché PNG. Odhalit nález střihem na zvuk západky. |
| 07–08 | grafika/paper.png, grafika/mighty_decks_logo.png a grafika/mighty-decks-{krabice,qr}.png pod reference/; cta-herna.png | Postavit přehled i CTA z jednotlivých prvků. U krabice použít originální grafiku, u QR zachovat kontrast a bílý okraj. |

Portréty: čtyři výřezy z `reference/planches/portraits.png`. Karty: `reference/karty/ruka/{cs,en}` pro výsledek, zranění, obě výbavy, kuši a lucernu; domobrana a žalář z `reference/karty/{cs,en}`. Používej přímo dodané líce včetně pravidel. Chybějící lokalizovaný asset hlásit jménem; anglický líc do české verze automaticky nedosazovat.

**Kolmý detail volby:** pro přesnou registraci použij tři samostatné RGBA soubory `storyboard/overlays/{cs,en}/overhead-{U2,C2,S1}.png`. Leží mezi deskou a rukou, ve velikosti celého plátna. Středy karet jsou po 366 px. Ruku (včetně stínu) na 810 polož na x = −366 px, 822–840 ji přesuň do klidové polohy x = 0; jde o návrat z krajní polohy testu, ne o posun z prostřední karty na pravou. Kontrolní složení na původní kresbě se v oblasti karet pixelově shoduje s exportem. Při výběru spoj pohyb jen s ID C2, ostatní karty drž. V [náhledu detailu](../storyboard/vrstvy/index.html#over-shoulder) přepni „Karty na stole“ na CS nebo EN a zkontroluj, kde ukazovák skončí.

## Pořadí implementace a předání

1. V aktuálním checkoutu připrav minimální Remotion projekt v `animatik/`. Zapiš příkazy instalace, náhledu a exportu, verze uzamkni lockfilem. Sestav seznam lokálních assetů a mapu `locale → role, lines, faces, CTA`. Před spuštěním zkontroluj cesty, celé intervaly, žádné díry a konec na 1500. Potřebné soubory pro Remotion připrav do jeho public adresáře z existujících zdrojů opakovatelným krokem.
2. Sestav tichý střih z 13 klíčových obrazů. Nejprve pusť smyčku 660–1080: hrozba → oči → levá a prostřední karta → vis → řez → práh → použití U₂. Nech diváka pojmenovat cenu a důvod. Teprve až pořadí funguje, nahrazuj ploché obrazy vrstvami. Nepřidávej pohyb do záběru, který potřebuje čas na čtení.
3. Napoj karty, ruku, loga a portréty; pak obě sady cue. Pohyb interpoluj z čísla snímku s omezením na krajní hodnoty. Pro odtržení a dosednutí stačí krátký nájezd s dobrzděním, pro čtení konstanta. Nepoužívej systémový čas, CSS animaci ani náhodu při vykreslení. Vrať přehrávač na prostředek akce a zkontroluj stejnou pózu jako při plynulém přehrání.
4. Přidej pracovní čtení CS/EN a základní ruchy podle [zvukové mapy](../storyboard/zvuk-a-hlasy.md). Zapiš skutečná okna a případné změny dílčích střihů; nesahej na začátek 41s loga, 45s CTA ani celkovou délku. Pokud pozdější hlas zabere víc času, nejdřív uprav prostor kolem repliky.
5. Odevzdej náhled v Remotion Studiu, dvě pracovní MP4, odpovídající SRT a seznam pracovních náhrad s časem. U renderů ověř rozměr, 30 fps, 1500 obrazových snímků, správný jazyk a synchronizaci. Z obou videí dekóduj QR na 1350, 1425 a 1499 v plném rozlišení i po zmenšení na 390 px. Přehraj celou rampu bez zvuku a obě verze s hlasem v rychlosti 1×. K předání přilož příkazy a nálezy podle záběru; schválení finální výroby je až další rozhodnutí.
