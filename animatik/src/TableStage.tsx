import type { CSSProperties, ReactNode } from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import registration from "../pilot/table/registration.json";

export type TableCardId = keyof typeof registration.cards;
type Props = {
  locale: "cs" | "en";
  actress?: ReactNode;
  foreground?: ReactNode;
  cardStyles?: Partial<Record<TableCardId, CSSProperties>>;
};

function bounds([left, top, width, height]: number[]): CSSProperties {
  return { position: "absolute", left, top, width, height };
}

/** Registered at 1920 × 1080; scale the whole stage for lower-resolution pilots. */
export function TableStage({locale, actress, foreground, cardStyles}: Props) {
  const full = bounds([0, 0, 1920, 1080]);
  return <AbsoluteFill style={{width:1920, height:1080, overflow:"hidden"}}>
    <Img src={staticFile("storyboard/vrstvy/table/00-pozadi.png")} style={full} />
    <Img src={staticFile("storyboard/vrstvy/table/01-vypravec.png")} style={full} />
    {actress}
    <Img src={staticFile("pilot/table/wood.png")} style={bounds(registration.wood)} />
    {(Object.keys(registration.cards) as TableCardId[]).map(id =>
      <Img key={id} data-card-id={id} src={staticFile(`pilot/table/${locale}/${id}.png`)}
        style={{...bounds(registration.cards[id].bounds), ...cardStyles?.[id]}} />
    )}
    {foreground}
  </AbsoluteFill>;
}
