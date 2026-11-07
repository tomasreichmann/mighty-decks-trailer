import type { CSSProperties } from "react";
import { Fragment } from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile } from "remotion";
import cut from "../../storyboard/strih.json";
import manifest from "../../storyboard/vrstvy/manifest.json";
import { plays, stateAtFrame } from "./handState";
import {TableStage} from "./TableStage";
import {HatchStage} from "./HatchStage";
import {HangarPlate} from "./HangarPlate";

type Locale = "cs" | "en";
type Props = { shotId: string; frame: number; locale: Locale; beastMotion?: boolean };
type Layer = (typeof manifest.shots)[number]["layers"][number];

const canvas: CSSProperties = {
  position: "absolute",
  inset: 0,
  width: 1920,
  height: 1080,
};
const layersById = new Map(
  manifest.shots.map(({ id, layers }) => [
    id,
    [...layers].sort((a, b) => a.z - b.z),
  ]),
);
const shotById = new Map(cut.shots.map((shot) => [shot.id, shot]));
const choice = plays.find(({ shot }) => shot === "04b-volba")!;
const ease = Easing.inOut(Easing.cubic);

function travel(frame: number, start: number, end: number) {
  return interpolate(frame, [start, end], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
}

const Sheet = ({ path, style }: { path: string; style?: CSSProperties }) => (
  <Img src={staticFile(path)} style={{ ...canvas, ...style }} />
);

function overheadFaces(frame: number, locale: Locale) {
  const { slots, playedCard } = stateAtFrame(frame);
  const lift = travel(frame, choice.pick, choice.hold);
  const touch = travel(frame, choice.resolve - 5, choice.resolve);
  return (
    <>
      {slots.map(
        (id) =>
          id && (
            <Sheet
              key={id}
              path={`storyboard/overlays/${locale}/overhead-${id}.png`}
            />
          ),
      )}
      {playedCard && (
        <Sheet
          path={`storyboard/overlays/${locale}/overhead-${playedCard}.png`}
          style={{
            transformOrigin: "1266px 443px",
            transform: `translateY(${-44 * lift * (1 - touch)}px) scale(${1 + 0.065 * lift * (1 - touch)})`,
            filter: `drop-shadow(0 ${22 * lift * (1 - touch)}px ${9 * lift * (1 - touch)}px rgba(33,18,13,0.65))`,
          }}
        />
      )}
    </>
  );
}

function motion(id: string, layer: Layer, frame: number) {
  if (layer.dx === 0 && layer.dy === 0) return 0;
  switch (id) {
    case "opening":
      return travel(frame, 0, 149);
    case "ramp":
      return travel(frame, 660, 675);
    case "over-shoulder":
      return 1 - travel(frame, 822, 840);
    case "ramp-jump":
      return travel(frame, 870, 893);
    case "thrust":
      return layer.z === 1 ? travel(frame, 984, 1005) : travel(frame, 978, 988);
    case "loot":
      return travel(frame, 1158, 1170);
    default:
      return 0;
  }
}

function injury(locale: Locale, owner: "exile" | "smuggler") {
  const labels = {
    cs: { exile: "Vyhnankyně", smuggler: "Pašerák" },
    en: { exile: "Exile", smuggler: "Smuggler" },
  };
  return (
    <div
      style={{
        position: "absolute",
        left: 1476,
        top: 295,
        width: 342,
        textAlign: "center",
      }}
    >
      <div
        style={{
          display: "inline-block",
          padding: "3px 14px 5px",
          marginBottom: 6,
          borderRadius: 5,
          background: "rgba(15,18,22,.86)",
          color: "#fff1db",
          font: 'bold 34px "Segoe UI", sans-serif',
          textTransform: "uppercase",
        }}
      >
        {labels[locale][owner]}
      </div>
      <Img
        src={staticFile(`reference/karty/ruka/${locale}/injury.png`)}
        style={{
          display: "block",
          width: "100%",
          filter: "drop-shadow(2px 4px 6px #181118)",
        }}
      />
    </div>
  );
}

function LootPair({
  locale,
  side,
}: {
  locale: Locale;
  side: "left" | "right";
}) {
  const left = side === "left";
  const key = left ? "base_light_weapon" : "base_heavy_armor";
  return (
    <>
      <svg width="1920" height="1080" style={canvas}>
        <path
          d={left ? "M400 670 L635 669" : "M1519 670 L1040 649"}
          fill="none"
          stroke="#231c1b"
          strokeWidth="6"
          opacity=".8"
        />
        <path
          d={left ? "M400 670 L635 669" : "M1519 670 L1040 649"}
          fill="none"
          stroke="#f9efe2"
          strokeWidth="2.5"
        />
      </svg>
      <Img
        src={staticFile(`reference/karty/ruka/${locale}/${key}.png`)}
        style={{
          position: "absolute",
          top: 314,
          left: left ? 55 : 1510,
          width: 354,
          filter: "drop-shadow(0 4px 6px rgba(18,13,10,.72))",
        }}
      />
    </>
  );
}

export function ScenePlate({ shotId, frame, locale, beastMotion }: Props) {
  const shot = shotById.get(shotId);
  if (!shot) throw new Error(`Missing shot: ${shotId}`);
  const id = shot.plate.split("/").pop()!.replace(".png", "");
  if (id === "hangar") {
    return <AbsoluteFill>
      <HangarPlate frame={frame} beastMotion={beastMotion} />
      {frame >= 540 && frame < 608 && injury(locale, "exile")}
    </AbsoluteFill>;
  }
  if (id === "hatch") return <HatchStage frame={frame} />;
  if (id === "table") {
    return <TableStage locale={locale} actress={<Sheet path="storyboard/vrstvy/table/02-hracka.png" />} />;
  }
  const layers = layersById.get(id);
  if (!layers) throw new Error(`Missing registered layers for ${id}`);
  const camera = shot.plateTransform;
  const staticPlate = id === "rescue";
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          transformOrigin: "0 0",
          transform:
            camera &&
            `translate(${camera.x}px, ${camera.y}px) scale(${camera.scale})`,
        }}
      >
        {staticPlate ? (
          <Sheet path={shot.plate} />
        ) : (
          layers.map((layer) => {
            // The clean plate carries a repainted shaft behind the hinged piece.
            if (id === "ramp" && layer.z === 1 && frame >= 676) return null;
            const distance = motion(id, layer, frame);
            return (
              <Fragment key={layer.file}>
                {id === "over-shoulder" &&
                  layer.z === 1 &&
                  overheadFaces(frame, locale)}
                <Sheet
                  path={`storyboard/vrstvy/${layer.file}`}
                  style={{
                    transform: distance
                      ? `translate(${layer.dx * distance}px,${layer.dy * distance}px)`
                      : undefined,
                  }}
                />
              </Fragment>
            );
          })
        )}
      </AbsoluteFill>
      {shotId === "05a-zraneni" && injury(locale, "smuggler")}
      {id === "loot" && frame >= 1092 && (
        <LootPair locale={locale} side="left" />
      )}
      {id === "loot" && frame >= 1130 && (
        <LootPair locale={locale} side="right" />
      )}
    </AbsoluteFill>
  );
}
