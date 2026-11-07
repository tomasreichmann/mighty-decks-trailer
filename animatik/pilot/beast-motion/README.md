# Výpad v hangáru · 431–459 f

Pro snímek `f` načti `frames/(f−431).webp` s trojmístným číslem. Celkem 29 bezztrátových výřezů s alfou zabírá 5,11 MB. První snímek vychází přímo z `public/hangar/approach.png`, dalších 28 z místního průchodu H3. [Tři pózy v pohybu](poses.jpg) ukazují snímky 431, 445 a 459.

Celé plátno snímků má 512 × 512 px. Původní čtverec výřezu zaujímá uvnitř 448 × 448 px od (32,32). Uvnitř původního rodiče o straně `size` nastav potomkovi počátek `(−size/14, −size/14)` a stranu `size × 8/7`. Natočení, změna měřítka a pohyb po podlaze patří společnému rodiči se stejnou kotvou jako původní obraz. Okraj poskytuje přední tlapě a ocasu prostor k výpadu. Všechny snímky mají stejnou registraci.

H3 převádí váhu na přední tlapu, mění náklon hlavy, otevře čelist a narovná ocas. Ve druhé půlce gesta se jeho přední packy posunou i vůči podlaze. Herecký pohyb je určený pro rychlý náběh k výpadu.

## Reprodukce

1. Vstup `md-beast-approach-green.png` obsahuje výhradně původní RGBA výřez, převzorkovaný Lanczosem na 448 px. Průhlednost a okolní 32px okraj vyplňuje RGB (12,230,29).
2. V místním ComfyUI na 8188 nahraj toto PNG pod dodaným názvem a spusť `h3-beast.json`. Seed 716811, osm kroků, výstupní uzel 19. Úspěšný výpočet trval 46,342 s. [Záznam úlohy](job.json)
3. Bezztrátový výstup z uzlu 19 ulož jako `h3-lossless.webp`. Spusť `python animatik/pilot/beast-motion/extract.py` (Pillow a NumPy). Skript odvodí barvu pozadí pro každý snímek, odstraní ji z poloprůhledných obrysů a časově přemapuje 39 dekódovaných obrazů na 29 registračně shodných snímků.

Celkový rozsah masky s alfa > 128 je (10,11) až (479,469) včetně. U žádného pixelu s alfa > 32 nepřevýšila zelená větší ze zbývajících kanálů o více než 15 úrovní.
