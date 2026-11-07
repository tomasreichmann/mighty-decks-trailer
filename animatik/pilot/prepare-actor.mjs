import {copyFile, mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {join} from 'node:path';

const source = fileURLToPath(new URL('./actor/', import.meta.url));
const dest = fileURLToPath(new URL('../public/storyboard/pilot/actor/', import.meta.url));
await mkdir(dest, {recursive: true});
await copyFile(join(source, 'residual.png'), join(dest, 'residual.png'));
// 66 composition frames at 30 fps use samples 0–52 at 24 fps.
for (let i = 0; i < 53; i++) {
  const name = 'actor-' + String(i).padStart(3, '0') + '.png';
  await copyFile(join(source, 'frames', name), join(dest, name));
}
