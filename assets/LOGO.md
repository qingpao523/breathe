# App Logo Asset

## Files
- assets/logo.png - 1024x1024
- assets/logo-512.png - 512x512
- assets/logo-180.png - 180x180
- android/res/mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/ic_launcher.png - 48/72/96/192/288
- android/res/mipmap-*/ic_launcher_round.png - round masked variant

## Source
- Tool: doneai skill, model gpt_image_2
- generateUuid: gpt-4c82cefc1da5fd17
- Raw URL: https://done.cdn.alibabadesign.com/2026/10/10/6799fa9987a35321.png
- Date: 2026-10-10
- Version: 3rd generation (v1/v2 rejected: v1 ends off-corner, v2 stroke too thin)

## Design spec
- Near-black background #080C14 (measured #040814)
- One continuous uniform stroke, square outline, only 3 sides drawn
- Left edge open; both stroke ends rest on the top-left and bottom-left corners
- Gradient cyan #5EE0FF -> violet #B18CFF (measured hue 185deg -> 262deg)
- Stroke width 5.6 percent of canvas; legible at 48px (approx 2.7px line)

## Prompt (as submitted)

Minimalist app icon, 1:1 square canvas, deep near-black background hex 080C14. A single geometric square outline drawn as one continuous bold stroke, chunky and powerful, with a rock-solid uniform stroke thickness equal to about 7 percent of the canvas width. Only three sides are drawn: the top edge, then the right edge, then the bottom edge; the whole left edge stays empty and open. The stroke starts exactly on the top-left sharp corner and stops exactly on the bottom-left sharp corner, both stroke ends resting right on square corners. Stroke color is a smooth gradient along the path from cyan hex 5EE0FF at the top-left to violet hex B18CFF at the bottom-left. Flat vector style, sharp 90-degree corners, clean edges, flat caps. No 3D, no glow, no shadow, no texture, no letters, no text, no numbers, no stars, no dots, no extra decoration. Square centered with even margin, occupying about 62 percent of the canvas. Premium, calm, high contrast, minimal breathing app icon.

## Android integration
- build_app.py manifest template: android:icon="@mipmap/ic_launcher"
  android:roundIcon="@mipmap/ic_launcher_round"
- Verified: aapt2 dump badging shows application icon = res/mipmap-mdpi-v4/ic_launcher.png
