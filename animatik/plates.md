# Pracovní obrazové náhrady

Časy a snímky platí pro CS i EN. Každý střih používá absolutní čas. Rozsahy posunu pocházejí z kontroly krajních poloh ve [vrstvovém manifestu](../storyboard/vrstvy/manifest.json).

| Čas | Záběr | Co je v animatiku a co zbývá nakreslit |
|---|---|---|
| 0–6 s | Volání | Korveta přejede o 24 px proti kotouči. Rám kokpitu zůstává pevný, od snímku 149 drží i loď. Pro delší přelet by bylo potřeba dokreslit prostor za anténami. |
| 6–14 s | Dohoda | Na 330 se po zahrání U₁ střihne do detailu přijímané mapy na zápěstí. Ruka otočí skutečnou pákou o 18° kolem čepu (357–368). Na ruch od 376 odjede zasklené křídlo o 518 px doleva. Od 403 je vidět průchod do hangáru a trojice s nákladem a mládětem. Jako druhá póza slouží kresba posádky z rampy. Přesun lidí do této pózy překrývá detail páky; vlastní průchod postavami není animovaný. Dva oříznuté obrázky znovu vytvoří `python scripts/prepare-hatch.py` z adresáře `animatik` (Pillow, NumPy, OpenCV, CPU). |
| 14–22 s | Hangár | Zleva přichází šelma; mezi 431–459 používá hlavní střih pohyb tlap a hlavy s dočištěným obrysem. Na 460–479 je vidět zakousnutí do pažby. Katalogová karta karabiny není použitá: není doložena shoda obou líců. Od 534 dráp roztrhne rukáv vyhnankyně. Na 540–607 je u ní Zranění, mimo tři sloty ruky. Při odchodu sdílejí postavy horní část skupinové kresby; nohy, jejich stíny a odrazy se pohybují zvlášť. |
| 22–25 s | Rampa | Na utržení se pruhovaný díl pohne o −8/+32 px. Na 676 následuje střih na dokreslenou šachtu po pádu, získanou odebráním samostatné vrstvy. Souvislý let celého dílu do hloubky vyžaduje další perspektivní pózu. |
| 25–27,2 s | Rozhovor | Vybraný profil a ruka hráčky ze záznamu H3, rozšířené masky SAM 2, statické kulisy a tři lokalizované líce. Anglický dabing používá stejná ústa přečasovaná podle anglické věty; tvary jednotlivých anglických hlásek nejsou nové. |
| 27,2–29 s | Volba | Prst přejde z levého Úspěchu nad prostřední Částečný. Pouze prostřední karta vystoupí o 44 px se stínem a před střihem dosedne. |
| 29–31 s | Vis, řez, práh | Bedna dopadne na 870. Skluz nohou a přenos váhy na zachycené zápěstí používají 24 dvousnímkových fází z kresby. V 882–917 vidíme ránu i označení PAŠERÁK / SMUGGLER. Závěr vytažení přeskočí střih na všechny tři s bednou a mládětem za prahem (918–929). |
| 31–36 s | Boční tah | Povel, zahrání U₂ na 944, zážeh na 984, v EN plná tryska po 990. Troska přejede za hranu průzoru, pak se doplní U₃. |
| 36–41 s | Kořist | Na 1092 střih ze zavřeného víka na levou přihrádku. Na 1130 vidíme i pravou. Mládě se dotkne přezky na 1170, pak mají diváci dvě sekundy na čtení. Otevírání víka spojuje zvuk západky a střih. |
| 41–50 s | Logo a pozvání | Lícům odpovídá jazyk filmu. Krabice je v obou filmech skutečný produkt se stejným anglickým potiskem. |
