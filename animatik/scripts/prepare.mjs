import {copyFile, mkdir, readFile, readdir} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const project = fileURLToPath(new URL('../', import.meta.url));
const root = resolve(project, '..');
const readJson = async (path) => JSON.parse(await readFile(resolve(root, path), 'utf8'));
const cut = await readJson('storyboard/strih.json');
const manifest = await readJson('storyboard/vrstvy/manifest.json');
let cursor = 0;
for (const shot of cut.shots) {
  if (shot.in !== cursor || shot.out <= shot.in) throw new Error('Invalid interval: ' + shot.id);
  cursor = shot.out;
}
if (cursor !== 1500 || cut.durationInFrames !== cursor || cut.shots.length !== 13 ||
    cut.fps !== 30 || cut.width !== 1920 || cut.height !== 1080) throw new Error('Unexpected cut format');

const sources = new Set(cut.shots.map((s) => s.plate));
sources.add('reference/planches/portraits.png');
for (const name of ['mighty_decks_logo','mighty-decks-krabice','mighty-decks-qr']) {
  sources.add('reference/grafika/' + name + '.png');
}
for (const shot of manifest.shots) {
  for (const layer of shot.layers) sources.add('storyboard/vrstvy/' + layer.file);
}
for (const locale of ['cs', 'en']) {
  for (const dir of ['reference/karty/ruka/' + locale, 'storyboard/overlays/' + locale]) {
    for (const name of await readdir(resolve(root, dir))) {
      if (name.endsWith('.png')) sources.add(dir + '/' + name);
    }
  }
  for (const name of ['medieval_militia', 'medieval_dungeon']) {
    sources.add('reference/karty/' + locale + '/' + name + '.png');
  }
}
await Promise.all([...sources].map(async (path) => {
  const dest = resolve(project, 'public', path);
  await mkdir(dirname(dest), {recursive: true});
  await copyFile(resolve(root, path), dest);
}));
console.log('Prepared ' + sources.size + ' images for 13 shots and two languages.');
