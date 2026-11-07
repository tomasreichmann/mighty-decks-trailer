import {AbsoluteFill, Img, interpolate, staticFile} from "remotion";
import type {CSSProperties} from "react";
import dialogue from "./dialogue.json";
import {ScenePlate} from "./ScenePlate";
import {TableStage} from "./TableStage";

type Language = "cs" | "en";
type Props = {frame: number; lang: Language};

function Performance({frame, lang}: Props) {
  // The Czech SAM frames are registered to the actor's chosen performance.
  // Give the English delivery its own anticipation and mouth-close frames.
  const line = dialogue[lang][6];
  const local = lang === "cs" ? frame - 750 : interpolate(
    frame, [line.startFrame, line.endFrame - 1], [8, 65],
    {extrapolateLeft: "extend", extrapolateRight: "clamp"},
  );
  const sample = Math.max(0, Math.min(52, Math.floor(local * 24 / 30)));
  const path = "storyboard/pilot/actor/";
  const placement: CSSProperties = {position: "absolute", left: 0, top: 0, width: 896, height: 832};
  return <TableStage locale={lang}
    actress={<Img src={staticFile(path + "residual.png")} style={placement} />}
    foreground={<Img src={staticFile(path + "actor-" + String(sample).padStart(3, "0") + ".png")} style={placement} />}
  />;
}

function Catch({frame, lang}: Props) {
  const insert = frame >= 882;
  const pose = 2 * Math.floor((frame - 870) / 2);
  return <AbsoluteFill style={{overflow: "hidden"}}>
    <ScenePlate shotId={insert ? "05a-zraneni" : "04c-unik"} frame={insert ? 900 : 870} locale={lang}/>
    <AbsoluteFill style={insert ? {transformOrigin: "0 0", transform: "translate(-170px,-233px) scale(1.364)"} : {}}>
      <Img src={staticFile("picture-a/catch-" + String(pose).padStart(2, "0") + ".webp")}
        style={{position: "absolute", left: 380, top: 240, width: 680, height: 685}} />
    </AbsoluteFill>
  </AbsoluteFill>;
}

export default function PictureA({frame, lang}: Props) {
  if (frame < 180) return <ScenePlate shotId="01-volani" frame={frame} locale={lang}/>;
  if (frame < 750) return <ScenePlate shotId="04a-rampa" frame={frame} locale={lang}/>;
  if (frame < 816) return <Performance frame={frame} lang={lang}/>;
  if (frame < 870) return <ScenePlate shotId="04b-volba" frame={frame} locale={lang}/>;
  if (frame < 918) return <Catch frame={frame} lang={lang}/>;
  return <ScenePlate shotId="04e-prah" frame={frame} locale={lang}/>;
}
