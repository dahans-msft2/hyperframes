# Design plan — Highway 12: A Lewis and Clark Road Trip to Montana

Preset: **learn-ilt**  ·  Profile: **skilling-session** (run at the SHORT end, ~6:13 narration + 0:11 end card)
Voice: en-US-Ava:DragonHDLatestNeural. Narration, transcript, and `anchors.js` (17/17 resolved) are frozen.

> **This is a travelogue, not a portal walkthrough.** It deliberately balances the beauty of the
> drive with the fuller, harder history (Indigenous homelands, Sacagawea's real story, the 1877 Nez
> Perce flight). Keep that tone: reverent, honest, never triumphalist. History is grounded in NPS
> sources — see `script.md`'s source-fidelity ledger.

---

## The through-line: ONE animated route map (this is the whole visual idea)

**The map is the persistent stage. Images POP UP on the route as we "drive" across it — no static
Ken-Burns photo scenes.** A stylized map of the Pacific Northwest is on screen for the body of the
film. The route line **draws itself leg by leg**, a marker rides the growing head of the line, and
as the drive reaches each waypoint the matching **photo card pops up** beside it (scale 0.9→1 + fade,
a soft overshoot settle), holds under its narration, then recedes as the drive continues. One or two
cards visible at a time — never a cluttered wall.

Two "map modes", same visual language so the film reads as one continuous move:
- **History mode** (opening): a faint EXPEDITION-era route (Missouri → Pacific) on the aged ground;
  the three **portrait cards** (Jefferson, Lewis, Clark) pop in; the **Sacagawea** beat pops a
  name+facts+quote card (NO face) over the plains image.
- **Drive mode** (body): the modern **US-12 route** WA → Glacier; **landscape photo cards** pop at
  each waypoint as the line draws.

If built as multiple scenes, every journey scene must reuse the **same registered map SVG
(identical viewBox + waypoint coordinates)** so cross-scene cuts read as one continuous map; only the
"route progress" (stroke-dashoffset), the active marker, and which card is showing change. A single
persistent-map composition is equally acceptable — the effect is what matters.

### Map SVG spec (viewBox `0 0 1920 1080`, place inside a centered map group)

Stylized, NOT geographically exact — evoke the layout. Waypoints (x,y) and draw order:

| # | Waypoint | (x, y) | Image card | Anchor cue | Card side |
|---|---|---|---|---|---|
| — | Seattle / I-90 start | (250, 300) | — (origin dot only) | — | — |
| 1 | Vantage · Columbia | (515, 360) | `columbia-vantage.png` | `vantage` | above-right |
| 2 | Clarkston / Lewiston | (640, 560) | `confluence.png` | `confluence` | left |
| 3 | Lochsa / US-12 | (860, 590) | `lochsa.png` | `lochsa` | below |
| 4 | Lolo Pass (ID–MT) | (1010, 555) | `lolo-pass.png` | `loloSummit` | above |
| 5 | Big Hole (1877 beat) | (1020, 660) | `big-hole.png` | `bigHole` | below-right |
| 6 | Traveler's Rest | (1110, 505) | `travelers-rest.png` | `travelersRest` | right |
| 7 | Missoula | (1140, 470) | `missoula.png` | `missoula` | right |
| 8 | Flathead Lake | (1180, 315) | `flathead.png` | `flathead` | right |
| 9 | Glacier NP | (1400, 205) | `glacier.png` | `glacier` | above-right |

Route path: a smooth line Seattle → Vantage → down to Clarkston → east to Lochsa → Lolo Pass → up to
Traveler's Rest/Missoula → north to Flathead → NE to Glacier. Bitterroots (`bitterroots.png`) is the
terrain BETWEEN Lochsa and Lolo — pop it during the 1805-crossing beat (`rescue1805`) as the line
crawls slowly over that segment. The 1877 flight (`flight1877`→`bigHole`) draws a SECOND, thin
line in the OPPOSITE direction (Lolo → Big Hole → south) in a mournful desaturated tone.

Map styling (learn-ilt tokens): land shapes in soft warm neutrals over the `content-wash` ground;
route line in `--accent-2` (#0078d4) for the drive, a muted grey-red for the 1877 flight; waypoint
dots `--accent` with a soft ring pulse when reached; labels in `ilt-kicker`/`ilt-caption`. Photo
cards: white `--paper` frame, `--radius`, `--shadow`, a thin `--border`; ~34% frame width; rounded.

Camera: a slow, subtle push/pan of the map group toward the active region (gentle — carry the eye,
don't lurch). Motion must PERFORM (route draw, marker, card pop), never idle-wobble.

---

## Scene beats (cue times are ABSOLUTE from `anchors.js`; builder finalizes scene durations to word boundaries)

| Beat | ~cue time | Narration span (opening words) | On screen (LABEL / attributed quote — never the spoken line) | Map / card action |
|---|---|---|---|---|
| bumper *(chrome)* | 0 | *(silent sting)* | kicker **"A Highway 12 Road Trip · History, honestly"** | brand sting only |
| title *(chrome)* | ~3 | "Before there was a highway…" | Title **"Highway 12 / A Lewis & Clark Road Trip to Montana"** · subtitle **"The drive, and the fuller story"** | faint route line behind |
| whose-land | `quoteLand` 21.5 | "…this land was home." | Attributed quote **"We did not travel here; we are of this land." — Nez Perce Tribal Executive Committee** | `homeland.png` full-bleed-ish behind the quote (a held reverent frame is correct here — NOT a tour stop) |
| the charge | `louisiana` 40.6 | "In 1803… Louisiana Territory…" | kicker **"1803 · Louisiana Purchase"** · caption **"exploration — and a claim on a continent that was never empty"** | expedition map appears; `jefferson.png` portrait card pops |
| the corps | `corps` 53.9 | "…the Corps of Discovery…" | plates **"Meriwether Lewis" / "William Clark"** · **"a military reconnaissance"** | `lewis.png` + `clark.png` portrait cards pop side by side; faint expedition route traces west |
| sacagawea | `sacagawea` 72.2 | "…a young woman named Sacagawea…" | **"Sacagawea · Lemhi Shoshone"** · **"captive at ~12 · 16–17 on the journey"** · credit **"'They Got It Wrong' — MHA Nation"** — **NO face** | `plains-shoshone-country.png` behind; a quiet name+facts card (somber) |
| drive: Vantage | `vantage` 121.7 | "…the road meets the Columbia…" | leg label **"I-90 · Washington → Vantage"** · **"the Columbia — Plateau homeland for millennia"** | switch to DRIVE map; route draws leg 1; `columbia-vantage.png` pops |
| drive: confluence | `confluence` 139.8 | "…two towns that face each other…" | **"Clarkston, WA · Lewiston, ID"** · **"named for two visitors · the Nimíipuu were here first"** | line draws to the confluence; `confluence.png` pops |
| drive: Lochsa | `lochsa` 178.4 | "…U.S. Highway twelve… one of the wildest drives…" | shield **"US-12 · Lewis & Clark Highway"** · **"the Lochsa · ~100 roadless miles"** | line draws east along the Lochsa; `lochsa.png` pops |
| 1805 crossing | `rescue1805` 192.7 | "In September of 1805…" | kicker **"Sept 1805"** · **"snow · near starvation · the Nez Perce fed them"** | line crawls slowly over the Bitterroots; `bitterroots.png` pops (cold tone) |
| Lolo summit | `loloSummit` 218.7 | "…the summit of Lolo Pass…" | **"Lolo Pass · 5,000 ft · ID–MT line"** | line crests the pass; `lolo-pass.png` pops; marker crosses the state line |
| 1877 flight | `flight1877` 224.1 → `bigHole` 244.8 | "Seventy-two years later, in 1877…" | kicker **"1877 · the Nez Perce flight"** · **"800+ driven over this pass · Big Hole, dawn Aug 9 · 60–90 killed, most women & children · 1,170 miles"** | a second MOURNFUL line draws the OPPOSITE way over Lolo to Big Hole; `big-hole.png` pops; desaturate the map briefly |
| Traveler's Rest | `travelersRest` 269.3 | "…a quiet meadow, Traveler's Rest…" | **"Traveler's Rest · Lolo, MT"** · **"a proven L&C campsite"** | colour returns; line resumes; `travelers-rest.png` pops |
| Missoula | `missoula` 283.8 | "…beyond it is Missoula…" | **"Missoula, Montana"** · **"where the valley opens"** | line to Missoula; `missoula.png` pops |
| Flathead | `flathead` 300.8 | "…Flathead Lake shines…" | **"Flathead Lake"** · **"Flathead Reservation · Salish & Kootenai · largest natural freshwater lake in the West"** | line draws north; `flathead.png` pops |
| Glacier | `glacier` 311.2 | "…Glacier National Park…" | **"Glacier National Park"** · **"Going-to-the-Sun Rd · along the Blackfeet Nation"** | final leg draws; `glacier.png` pops |
| route recap | `routeRecap` 331.1 | "So there's the route…" | full route with all waypoints labeled | whole line + all dots highlighted in one sweep |
| recap *(chrome)* | ~340 | "…a fuller story than the road signs tell." | two columns — **the drive** (6 stops) / **the history** (homeland · 1805 mercy · 1877 flight) · badge **"~700 miles"** | small route thumbnail |
| cta *(chrome)* | `driveIt` 355.5 | "So go and drive it…" | **"Bring your curiosity — and your respect"** · sub **"Plan it at nps.gov/lecl · nps.gov/nepe"** | hero swoosh out |
| end card | — | *(no VO)* | AI disclosure + logo | `assets/AI_End_Card.mp4`, appended by the pipeline |

## Chrome placeholder fills (`__FILL__` in the stamped scenes)

- **01-bumper** kicker: `A HIGHWAY 12 ROAD TRIP · HISTORY, HONESTLY`
- **02-title**: kicker `A ROAD TRIP THROUGH HISTORY` · line1 `Highway 12` · line2 `A Lewis & Clark Road Trip` · subtitle `Washington to Montana — the drive, and the fuller story.`
- **03-objectives** (repurpose as the 6 legs): chips `The Corps of Discovery` · `Washington to Vantage` · `The Confluence` · `Highway 12 & Lolo Pass` · `Into Montana` · `Flathead & Glacier`
- **90-recap**: heading `The route, and the story` · stops `Vantage · Lewiston & Clarkston · Lolo Pass · Missoula · Flathead · Glacier` · note `Homeland · 1805 mercy · 1877 flight · ~700 miles`
- **91-cta**: line `Bring your curiosity — and your respect` · sub `Plan it at nps.gov/lecl · nps.gov/nepe`

## Grounds / brand

Body map on `content-wash`; the history/expedition beats may use `section-field`; the 1877 beat may
briefly deepen toward `dark-field` for gravity, then return. All text must clear the learn-ilt
contrast law — verify with `check` (WCAG AA). Segoe UI via the kit fallback stack (woff2 is
gitignored; the render host supplies the real font).

## Anchoring (builder owns the scene-relative math)

Every card pop and label reveal fires on its cue's spoken word via `window.__anchors` (`anchors.js`,
already resolved). Do **not** invent offsets. Map-leg draws start on the cue and run into the hold.
See `copilot-instructions.md` for the exact per-scene anchoring convention.

## Imagery ethics (non-negotiable)

Portraits only for the documented men (Jefferson/Lewis/Clark). **No invented faces** of Sacagawea or
any Native individual — those beats use land + attributed words. This corrects, rather than repeats,
the historical erasure.
