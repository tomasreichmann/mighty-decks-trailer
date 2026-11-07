import cut from "../../storyboard/strih.json" with { type: "json" };

export const plays = cut.cardPlays;
export const faceOf = (id: string) =>
  cut.cardFaces[id[0] as keyof typeof cut.cardFaces];

/** Physical copies keep their identities even when two cards share a printed face. */
export function stateAtFrame(frame: number) {
  let slots: (string | null)[] = plays[0].before;
  let playedCard: string | null = null;
  for (const play of plays) {
    if (frame < play.pick) break;
    if (frame < play.draw) {
      slots = play.before.map((id) => (id === play.card ? null : id));
      // The overhead Partial cuts directly to the crate: the card must not
      // reappear as a HUD face over the first frames of the impact.
      const release = play.shot === "04b-volba" ? play.resolve : play.resolve + 6;
      if (frame < release) playedCard = play.card;
      break;
    }
    slots = play.after;
  }
  return { slots, playedCard };
}
