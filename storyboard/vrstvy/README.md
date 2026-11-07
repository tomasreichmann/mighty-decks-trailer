# Vrstvy pro animatik Fangs in the Sun

Jedenáct obrazových podkladů má celkem 32 zarovnaných PNG s průhledností. Prohlížeč umožňuje vypínat jednotlivé vrstvy, posouvat obraz mezi klidovou a zkušební polohou a porovnat jej s původní kresbou. [Otevřít místní prohlížeč](index.html) · [Manifest pro animatik](manifest.json)

V Remotionu vlož soubory přes sebe od nejnižšího `z`, všechny do společného počátku na plátně 1920 × 1080. Použij běžné alfa složení a posun v pixelech před případným škálováním celé scény. Každá vrstva má `dx, dy` pro vyzkoušenou krajní polohu. Kladné x je doprava, kladné y dolů. Mezi pózami stačí násobit vektor průběhem od 0 do 1. U volby karty jde čas obráceně, od vychýlené ruky do výchozí pózy ilustrace. Karty, titulky, logo, audio a QR patří do samostatných komponent.

| Kresba | Oddělené prvky a vyzkoušený posun (x, y) | Režijní použití |
|---|---|---|
| opening | Korveta (+24, 0), rám (0, 0), slunce v pozadí | Krátký přejezd siluety před sluncem. |
| hatch | Pašerák (−3, 0), předloktí s rukojetí (+3, +2), průzor v pozadí | Ruku a páku pohni až po souřadnicích. Otevření dveří potřebuje druhou pózu. |
| hangar | Šelma (−2, 0), ruce a karabina (+1, +1), prázdný hangár | Krátké napětí v kontaktu čelistí s pažbou. Větší roztažení odhalí srst a stín na pažbě. Roztržení rukávu řeš střihem. |
| ramp | Utržený díl (−8, +32), trojice s nákladem (+1, 0), dokreslená šachta | Počátek pádu. Pro úplné zmizení plechu použij druhou pózu. |
| table | Hráčka (+5, 0), vypravěč (−4, 0), pokoj s rozehraným stolem | Rozklad vychází z opraveného snímku. Lampu, tři karty, dobírací balíček i roh krabice nese podklad. Dialog snese i zcela pevnou kameru. |
| over-shoulder | Ruka se svým stínem (−366, 0), čistá dřevěná deska | Začni na −366 px nad levým Úspěchem a vrať ruku na 0 nad Částečným úspěchem. Pohyb byl odzkoušen přes skutečnou sazbu ve třech polohách. [Kontrola volby](volba-kontrola.jpg) |
| ramp-jump | Visící pašerák (0, +1), ostatní zachránci (0, 0), prázdná rampa | Zachovat úchop za hranu. Jednopixelové sesednutí nebo klid, vytažení následuje střihem. Větší posun by přetrhl kontakt ruky s plechem. |
| rescue | Trojice s bednou (+1, 0), rám dveří (0, 0), vzdálený hangár | Krátký důkaz bezpečí za prahem. Při 12 snímcích lze vše držet. |
| thrust | Ruka s rukojetí (+2, 0), troska (+22, −9), kabina se sklem | Posuň trosku za sklem a jen lehce zhoupni rukojeť na pevném rameni páky. Horní okraj řeže trup. Pro velký průlet doplň další kresbu mimo záběr. |
| loot | Mládě (−2, +3), obvázaná ruka (0, 0), otevřená bedna s výbavou | Naznač dotek čumákem a podrž nález. Pod obvazem pokračuje textura stejného víka. |
| cta-herna | Lampa (0, 0), listy v pozadí (0, 0), stůl a police | Jednotlivé prvky umožní přesnou sazbu. CTA se všemi přidanými prvky zůstává na místě po celých pět sekund. |

**Kontrola.** Všech 32 PNG bylo po zápisu znovu otevřeno. Každé má 1920 × 1080 a neprázdný alfa kanál. V jedenácti klidových kompozicích je maximální odchylka vůči odpovídajícímu původnímu RGB pixelu **0**. U krajních poloh byly posouzeny viditelné okraje, zakryté plochy a kontakt předmětů. Neomezené přesouvání vrstev by odkrylo plochy, které původní kresba neobsahuje. Stav `limited` označuje konkrétní omezení v manifestu, `hold` označuje záměrně statickou CTA.

**Jak rozklad vznikl.** Každá ilustrace prošla samostatně místním ComfyUI s modelem Ming Design-Layer INT8. Kresba i latent měly při průchodu přesně 768 × 432. Při rozdílné velikosti vstupu by model pracoval s výřezem. Jedna úloha běžela vždy až po dokončení předchozí. Pro rampu, vis a tah následovaly cílené průchody, které odkryly šachtu, vzdálené prostředí, slunce a palubní desku. Model dodal masky a chybějící kresbu pod objekty. Viditelná barva, šrafování a kontury pocházejí z plného původního obrazu. U prstu nese pohyblivá vrstva také stín a podklad doplňuje struktura stejného dřeva.

Pro opakování samotného modelového rozkladu nahraj lokálně zmenšené PNG a v API grafu nastav soubor v uzlu 4, prompt podle manifestu v uzlu 5 a počet vrstev v uzlu 7. Výstupy modelu jsou uložené v pořadí kompozit, popředí, další vrstvy až po pozadí. Export pro animatik už používá opačné pořadí, od pozadí k popředí. Nastavení, identifikátory úloh, znění promptů i kontrolní součty zdrojů jsou v manifestu. [Výchozí graf pro ComfyUI](workflow-api.json)
