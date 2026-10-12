![Breathe logo](assets/logo.png)

# Breathe

A follow-along breathing app: **methods are data, evidence is transparent, and shape is method identity**.
> Current build: `breathe-v1.3.apk` (package `com.qingpao.app`, versionName 2.0, minSdk 26 / targetSdk 34, debug-signed).
> The APK lives in the **repo root** but is ignored by `.gitignore` and **not committed**; rebuild locally with `python3 build_app.py` (Android SDK build-tools 34 + JDK required).

## Why

Most breathing apps tell you "inhale 4s, hold 7s, exhale 8s" but never **where those numbers come from**, how strong the evidence is, or when it fails to show an effect. This project puts evidence into the product: every built-in method carries an evidence level, a source reference, and known counter-evidence (see `evidence/`).

## What works today
- **Four sections**: Stress relief / Sleep / Sport / Breathwork (UI in Chinese: 减压 / 睡眠 / 运动 / 调息); method cards show training goal, level recommendation and evidence rating.
- **8 built-in methods**: Diaphragmatic breathing, Physiological sigh, Coherent 5.5, Nasal breathing, Box 4-4-4-4, Cadence-coupled breathing, IMT (info card, needs a device), CO₂ tolerance / breath hold (with a safety screening sheet).
- **Stroke-based guide**: every method has a fixed shape (shape = method identity, not phase count); one phase = one edge, and "edges ÷ phases" cycles complete the figure; phase switches always land on a vertex; hold phases are pink dashed, breathing phases are cyan solid; circles use `arc`, polygons use `lineTo`. See `docs/design-v3.md` §3.
- **Target modes**: by count (3/6/10/20), by time (5/10/15/20 min), free (no limit); finish and quit are separate; 3s countdown, pause/resume, three speeds (standard / slow ×1.35 / slower ×1.7).
- **Progress and badges**: per-method L1–L3 (3 / 5 consecutive sessions to level up), rank based on cumulative minutes, total count and minutes, 28-day heat map; **five badges** — Habit (10 sessions of any method), Skilled (100 total), Hundred (100 on one method), 7-day streak, All-open (every non-card method at least 3).
- **Share card**: a 1080×1440 (3:4) card drawn with the method's shape and practice time; long-press to save.
- **Three guidance channels**: visual + sound (per-phase WebAudio cue: inhale/inhale2 520Hz, hold 660Hz, exhale 330Hz, hold2 440Hz) + vibration (18ms on phase switch); plus a keep-screen-on switch (native bridge on Android).
- **Local persistence**: settings, progress and badges are stored in `localStorage` (key prefix `breathe:`).
- **Android package**: WebView shell + JS bridge (`vibrate` / `keepScreenOn` / `toast`), with the single-file `index.html` bundled as an asset.
- **Specialty**: cycling zone (pre-ride wake-up / cadence breathing / post-ride recovery / key moments).

## Methods as data: current state and roadmap

Built-in methods are defined by two tables in `web/index.html`: `METHODS` (method data) and `SH` (method to shape). `methods/builtin/*.json` mirrors the built-ins for review and reference; the engine **does not load JSON dynamically yet**, and the custom-method form / import-export is still on the roadmap. To contribute a built-in method, read `CONTRIBUTING.md` and `methods/SCHEMA.md` first.

## Single-file build

`web/index.html` is the complete engine (no dependencies, no build step) — just open it in a browser. The repo-root `index.html` is the same file, kept for GitHub Pages and other static hosting.

## Layout

`evidence/` evidence base | `methods/` built-in method data | `web/` single-file engine | `android/` Android shell and packaging | `docs/` design docs and pitfalls (`docs/PITFALLS.md`)

## Contributing

See `CONTRIBUTING.md` for adding methods, evidence and code changes; read `docs/design-v3.md` first (design and rendering rules).

## License

Code: MIT. `evidence/` and `docs/`: CC BY 4.0.
