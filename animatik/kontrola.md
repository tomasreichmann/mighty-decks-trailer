# Kontrola dokončeného animatiku · CS / EN

V obou MP4 je 1 500 dekódovaných snímků, 1920 × 1080, 30/1 fps, přesně 50,000 s. U všech 1 500 snímků byla při sestavení ověřena časová značka s odchylkou pod 0,001 s. Zvuk je AAC. Jedenáct položek každého SRT souhlasí s textem i hranicemi replik v příslušném jazyce. U všech 22 replik vyšel posun dekódovaného zvuku vůči vybranému WAV 0,0 ms.

| Místo | Co bylo při kontrole patrné a co se změnilo |
|---|---|
| 14–22 s · oba jazyky | Šelma vstupuje z levé strany, na pažbu se zakousne na 460. První kartu Zranění má vyhnankyně. Dočištěný obrys tlapy, nohy postav a kontakt se zemí jsou v hlavním střihu. Po ráně na 534 je delší trhnutí látky a slábnoucí kroky. V telefonním pásmu jsou jejich jednotlivé údery rozlišitelné; zda ruch opravdu zní jako látka a kroky, je otázka pro poslech člověkem. |
| 25–31 s · oba jazyky | Kritik bez předem prozrazeného řešení rozlišil ponechaný Úspěch, zahraný Částečný a druhé zranění u pašeráka. Na mobilní šířce se karta původně zvedala jen asi o 2 px. Po opravě vystoupí asi o 9 px; oba sousední líce zůstávají na desce. V 918–929 jsou vidět tři lidé, bedna i mládě. Na první spočítání mají jen 0,4 s, protože na 930 už začíná kokpit. |
| 31–36 s · oba jazyky | Z prvního pracovního střihu nebylo jasné, zda se loď vyhnula překážce. V novém střihu troska průzor opustí, otevřený výhled zůstane v obraze a až poté přijde U₃. V EN se plná tryska otevře na 991. |
| 36–41 s · oba jazyky | Původní zavřené víko vypadalo jako prázdná otevřená bedna. Nová kresba má kovový povrch a oba pásy přepravované bedny. Kritik na obou hotových MP4 spároval čepel s lehkou zbraní a kyrys s těžkou zbrojí. Na 1170 viděl posun mláděte k přezce, bez dvojitého obrysu nebo pravoúhlého švu. |
| 45–50 s · oba jazyky | OpenCV přečetlo z obou filmů na 1350, 1425 a 1499 přesnou adresu https://board-game-prototypes.netlify.app/mighty-decks, ve 1920 px i ve 390 px (12/12). |

**Rozsah nezávislé kontroly.** První průchod kritik dělal pouze z vyrenderovaného filmu bez zvuku v časovém pořadí po 0,5 s, při šířce 390 px. Následně zkontroloval konkrétní opravené hranice a obě jazykové verze. Nešlo o lidské přehrání v reálném čase. Zvuk prošel slepým automatickým přepisem, měřením pauz a zkouškou v monu v telefonním pásmu. Výraz a přirozenost výslovnosti zůstávají k poslechu. Důvod, volba a cena byly rozpoznány v obou jazycích; v češtině se přepis některých hlásek lišil.

**Opakování:** v adresáři animatik spusť npm run lint, node scripts/check-hand.mjs, npm run verify a python scripts/verify-audio.py. Kontrola ruky prochází všechny snímky a testuje také zpětné skoky přes 330, 534, 870 a 930. [Pracovní náhrady v obraze](plates.md).

## Otevřené úkoly po poslechu traileru

- [ ] **České pozvání, 45–50 s.** Znovu namluvit „Vytiskni si karty a zahraj si Mighty Decks.“ Výrazný přízvuk v současné nahrávce posluchač popsal jako asijský. Přirozenost české výslovnosti ověřit poslechem celé závěrečné scény.
- [ ] **Zvukové efekty v obou verzích.** Přepracovat příliš jednoduché ruchy. V hangáru mají být sluchem rozlišitelné náraz, trhání látky a vzdalující se kroky. Při úniku má boční tah odpovídat pohybu lodi v obraze.
- [ ] **Emoce v českém voiceoveru.** Znovu namluvit repliky s ohledem na situaci postav. V nouzovém volání má být slyšet obava o posádku, při volbě karty odhodlání a při povelu k úniku naléhavost. Posoudit v celém střihu s hudbou.
