# App icon

Approved road-shaped K artwork generated with the built-in ImageGen tool.
`source.png` is the original approved image. Platform exports preserve this artwork.

Run `python3 tools/generate_app_icons.py` on macOS to regenerate the PNGs, favicon ICO, web manifest and iOS asset catalog metadata using sips.

Web: 16, 32, 48, 192 and 512px icons, a 180px Apple touch icon, and a padded 512px maskable icon.
Android: legacy 48–192px launcher icons across five densities, padded round variants, and 108–432px adaptive layers. Google Play: 512px.
iOS: all iPhone/iPad slots for the iOS 15 deployment target, including the 1024px App Store icon. OS masking supplies rounded corners.

Generation prompt: A minimal cream road-shaped K on forest green (#173E32), with ochre (#E7BD4A) dashed centre lines, gently rounded ends, balanced spacing, and no additional text or symbols.
