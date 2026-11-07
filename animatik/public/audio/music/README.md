# Hudba traileru

Výchozí hudba obou masterů je The Lift. Pro publikaci přilož k videu odpovídající kredit z tabulky a odkaz na licenci [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Ve všech verzích jde o výřez s upravenou ekvalizací a hlasitostí. Tyto údaje jsou také v poli comment dodaných MP4.

| Varianta | Autor a nahrávka | Výřez originálu | Použití ve střihu |
|---|---|---|---|
| lift | Kevin MacLeod · [The Lift](https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1500066) | 1:09–1:59 | Elektronická gradace vrcholí při bočním tahu ve 31 s. |
| constancy | Kevin MacLeod · [Constancy Part One](https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100775) | 0:14–1:04 | Opakující se smyčce spojují přechod z rampy ke kartám a podtrhují cenu rozhodnutí. |
| getaway | Kevin MacLeod · [Mistake the Getaway](https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100699) | 0:00–0:50 | Žestě a bicí dávají střetu v hangáru a následnému útěku dobrodružný tón. |

Remotion přijímá prop `music` s hodnotou z prvního sloupce. Každá skladba má samostatnou hudební stopu pro CS a EN v `public/audio/music`. Obálka klesá 180 ms před replikou a vrací se během 500 ms po ní. Průměrná úroveň RMS hudby po dobu každé repliky je alespoň 16 dB pod samostatným hlasem. Od 36 do 41 s hudba ustupuje ruchům kořisti.

Pro obnovu všech šesti MP4 spusť v adresáři animatik `python scripts/prepare-music.py <adresář-s-MP3>`. Skript očekává tři originální MP3 pojmenované podle názvů skladeb, existující obrazové mastery v out a připravené hlasové a ruchové stopy. Výchozí mix zapíše do Fangs-CS a Fangs-EN, alternativy mají přípony -constancy a -getaway. Zvuk lze ověřit příkazem `python scripts/verify-audio.py`.
