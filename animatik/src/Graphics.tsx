import type { CSSProperties } from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile } from "remotion";
import { faceOf, plays, stateAtFrame } from "./handState";

type Locale = "cs" | "en";
type Props = { frame: number; locale: Locale };
const slotsX = [1080, 1406, 1734];
const slotTop = 590;
const settle = { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) } as const;
const progress = (frame: number, start: number, end: number) =>
  interpolate(frame, [start, end], [0, 1], settle);
const between = (a: number, b: number, t: number) => a + (b - a) * t;
const asset = (name: string) => staticFile("reference/grafika/" + name + ".png");

function CardFace({ locale, face, x, y, width, outline = false, style }: {
  locale: Locale; face: string; x: number; y: number; width: number; outline?: boolean; style?: CSSProperties;
}) {
  const folder = ["medieval_militia", "medieval_dungeon"].includes(face) ? "karty" : "karty/ruka";
  return <Img
    src={staticFile(`reference/${folder}/${locale}/${face}.png`)}
    style={{
      position: "absolute", left: x - width / 2, top: y, width, height: width * 1024 / 629,
      borderRadius: width * 0.049,
      boxShadow: outline
        ? "0 0 0 3px #171b1d, 0 0 0 6px #f6e8ca, 0 6px 12px 5px #0d141ab0"
        : "0 2px 5px 1px #261d1660",
      ...style,
    }}
  />;
}

export function Hand({ frame, locale }: Props) {
  // The tabletop owns the physical cards. Keep the gun and injury inserts unobstructed.
  if (frame < 180 || frame >= 1080 || (frame >= 440 && frame < 480) || (frame >= 540 && frame < 608)
    || (frame >= 750 && frame < 870) || (frame >= 882 && frame < 918)) return null;
  const { slots, playedCard } = stateAtFrame(frame);
  const drawing = plays.find((play) => frame >= play.draw && frame < play.draw + 8);
  const drawProgress = drawing ? progress(frame, drawing.draw, drawing.draw + 8) : 1;
  const played = plays.find((play) => play.card === playedCard);
  const lift = played ? progress(frame, played.pick, played.hold) : 0;
  const wipe = played ? progress(frame, played.resolve, played.resolve + 6) : 0;
  return <>
    {slots.map((id, slot) => {
      if (!id) return null;
      const oldSlot = drawing?.before.indexOf(id) ?? -1;
      const x = oldSlot === -1 ? slotsX[slot] : between(slotsX[oldSlot], slotsX[slot], drawProgress);
      const entering = id === drawing?.replacement;
      return <CardFace key={id} locale={locale} face={faceOf(id)} x={x}
        y={slotTop + (entering ? 90 * (1 - drawProgress) : 0)} width={272} outline
        style={{ opacity: entering ? drawProgress : 1 }} />;
    })}
    {played && <CardFace locale={locale} face={faceOf(played.card)} outline
      x={slotsX[played.before.indexOf(played.card)]} y={between(slotTop, 130, lift)}
      width={between(272, 342, lift)}
      style={{ clipPath: wipe > 0 ? `inset(0 0 ${wipe * 103}% 0)` : undefined }} />}
  </>;
}

function CornerLogo({ frame }: { frame: number }) {
  const travel = progress(frame, 1230, 1248);
  // Source has a transparent border: the visible artwork occupies (54,132)–(979,909).
  const width = between(154, 512, travel);
  const size = width * 1024 / 925;
  return <Img src={asset("mighty_decks_logo")} style={{
    position: "absolute", width: size, height: size,
    left: between(1689, 704, travel) - size * 54 / 1024,
    top: between(43, 325, travel) - size * 132 / 1024,
  }} />;
}

const spreadFaces = [
  { id: "success", x: 206, y: 64 }, { id: "injury", x: 495, y: 64 },
  { id: "base_light_weapon", x: 206, y: 571 }, { id: "base_heavy_armor", x: 495, y: 571 },
  { id: "medieval_militia", x: 1420, y: 64 }, { id: "medieval_dungeon", x: 1710, y: 64 },
  { id: "medieval_crossbow", x: 1420, y: 571 }, { id: "medieval_lantern", x: 1710, y: 571 },
] as const;

function LogoSpread({ frame, locale }: Props) {
  return <AbsoluteFill>
    <Img src={asset("paper")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
    {spreadFaces.map(({ id, x, y }, i) => {
      const start = 1266 + 2 * Math.floor(i / 2);
      if (frame < start) return null;
      const show = progress(frame, start, 1284);
      return <div key={id} style={{ position: "absolute", inset: 0, opacity: show, translate: `0 ${(1 - show) * 35}px` }}>
        <CardFace face={id} x={x} y={y} width={270} locale={locale} />
        {(id === "medieval_militia" || id === "medieval_dungeon") && <div style={{
          position: "absolute", top: 504, left: x - 136, width: 272, textAlign: "center",
          color: "#271f19", font: "bold 29px 'Segoe Print', 'Segoe UI', sans-serif", lineHeight: "44px",
        }}>
          {id === "medieval_militia" ? (locale === "cs" ? "Domobrana" : "Militia") : (locale === "cs" ? "Žalář" : "Dungeon")}
        </div>}
      </div>;
    })}
  </AbsoluteFill>;
}

const ctaCopy = {
  cs: { title: "Stolní RPG bez kostek", action: "Pravidla a karty k tisku" },
  en: { title: "Diceless tabletop RPG", action: "Rules & printable cards" },
};

function CallToAction({ locale }: { locale: Locale }) {
  const copy = ctaCopy[locale];
  return <AbsoluteFill style={{ fontFamily: "'Segoe UI', Arial, sans-serif", fontWeight: 700, color: "white" }}>
    <Img src={staticFile("reference/planches/cta-herna.png")} style={{ width: "100%", height: "100%" }} />
    <div style={{
      position: "absolute", top: 715, left: 170, width: 760, height: 96, borderRadius: "50%",
      background: "#1a0e0c", filter: "blur(36px)", rotate: "7deg", opacity: 0.83,
    }} />
    <Img src={asset("mighty-decks-krabice")} style={{ position: "absolute", left: 72, top: 267, width: 942, filter: "drop-shadow(3px 10px 5px #20110eb0)" }} />
    <div style={{
      position: "absolute", left: 70, top: 80, width: 950, textAlign: "center", color: "#fff1d9",
      font: "bold 74px 'Segoe Print', 'Segoe UI', sans-serif", textShadow: "0 4px 5px #0c1119",
    }}>{copy.title}</div>
    <div style={{
      position: "absolute", left: 1020, top: 109, width: 810, textAlign: "center", fontSize: 57,
      lineHeight: "79px", textShadow: "0 3px 5px #0c1119",
    }}>{copy.action}</div>
    <Img src={asset("mighty-decks-qr")} style={{ position: "absolute", left: 1157, top: 222, width: 533, height: 533, imageRendering: "pixelated" }} />
    <div style={{
      position: "absolute", left: 968, top: 764, width: 924, padding: "4px 0 10px", textAlign: "center",
      color: "#fff", backgroundColor: "#121a22ef", fontSize: 42, lineHeight: "56px",
    }}>https://board-game-prototypes.netlify.app<br />/mighty-decks</div>
  </AbsoluteFill>;
}

export function Graphics({ frame, locale }: Props) {
  if (frame >= 1350) return <CallToAction locale={locale} />;
  return <>
    {frame >= 1230 ? <LogoSpread frame={frame} locale={locale} /> : <Hand frame={frame} locale={locale} />}
    <CornerLogo frame={frame} />
  </>;
}
