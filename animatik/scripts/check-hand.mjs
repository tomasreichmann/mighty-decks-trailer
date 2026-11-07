import assert from 'node:assert/strict';
import {plays, stateAtFrame} from '../src/handState.ts';

for (let frame = 0; frame < 1500; frame++) {
  const {slots, playedCard} = stateAtFrame(frame);
  const visible = [...slots, playedCard].filter(Boolean);
  assert.equal(new Set(visible).size, visible.length, 'Duplicate card at frame ' + frame);
}
for (const play of plays) {
  assert.deepEqual(stateAtFrame(play.pick - 1).slots, play.before);
  assert.equal(stateAtFrame(play.pick).playedCard, play.card);
  assert.equal(stateAtFrame(play.resolve + 6).playedCard, null);
  assert.deepEqual(stateAtFrame(play.draw).slots, play.after);
}
assert.deepEqual(stateAtFrame(930), {slots: ['U2', 'S2', 'S1'], playedCard: null});
// Seek backwards across each consequence, independent of prior playback.
for (const [frame, slots, card] of [
  [930, ['U2','S2','S1'], null], [929, ['U2','S2','S1'], null],
  [870, ['U2',null,'S1'], null], [869, ['U2',null,'S1'], 'C2'],
  [534, ['U2',null,'S1'], 'C1'], [533, ['U2',null,'S1'], 'C1'],
  [330, [null,'U2','C1'], 'U1'], [329, [null,'U2','C1'], 'U1'],
]) assert.deepEqual(stateAtFrame(frame), {slots, playedCard: card}, 'seek ' + frame);
console.log('Four physical card plays, all 1500 frames and seek to 930 OK.');
