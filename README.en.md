# Breathe

A follow-along app for breathing techniques. **Methods are data** - every method is traceable, and anyone can add their own.

## Why
Most breathing apps tell you "inhale 4s, hold 7s, exhale 8s" but never tell you **where those numbers come from**, how strong the evidence is, or when it fails to show an effect. This project puts evidence into the product: every built-in method carries an evidence level, a paper reference, and known counter-evidence.

## Methods are data
A breathing method is just JSON:

```json
{
  "id": "box-4-4-4-4",
  "name": "Box 4-4-4-4",
  "phases": [{"k":"inhale","s":4},{"k":"hold","s":4},{"k":"exhale","s":4},{"k":"hold2","s":4}],
  "cycles": 6,
  "mode": "timed",
  "geometry": "square"
}
```

Four phase kinds (inhale / hold / exhale / hold2) cover most techniques. **Adding a method = adding a config object, no code.**

## Layout
evidence/ - evidence base (techniques, papers, market) | methods/ - built-in methods | web/ - single-file engine | android/ - Android shell | docs/ - design docs

## Contributing
Add a method: drop a JSON in methods/builtin/. Add evidence: update evidence/ with the paper reference. Change code: read docs/design-v3.md first.

## License
Code: MIT. evidence/ and docs/: CC BY 4.0.
