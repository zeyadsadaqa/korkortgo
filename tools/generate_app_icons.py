"""Export the approved ImageGen artwork using macOS sips. Run from any directory."""
import json
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'design/app-icon/source.png'

def export(path, size, content_size=None):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['sips', '-z', str(content_size or size), str(content_size or size), str(SOURCE), '--out', str(path)], check=True, stdout=subprocess.DEVNULL)
    if content_size:
        subprocess.run(['sips', '--padToHeightWidth', str(size), str(size), '--padColor', '173E32', str(path)], check=True, stdout=subprocess.DEVNULL)

def write_json(path, data):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')

web = Path('composeApp/src/wasmJsMain/resources')
for size in (16, 32, 48, 192, 512):
    export(web / f'icons/icon-{size}.png', size)
export(web / 'apple-touch-icon.png', 180)
export(web / 'icons/icon-maskable-512.png', 512, 400)
# ICO supports PNG payloads; include all conventional browser favicon sizes.
payloads = [(size, (ROOT / web / f'icons/icon-{size}.png').read_bytes()) for size in (16, 32, 48)]
offset = 6 + 16 * len(payloads)
entries = []
for size, data in payloads:
    entries.append(struct.pack('<BBBBHHII', size, size, 0, 0, 1, 32, len(data), offset))
    offset += len(data)
(ROOT / web / 'favicon.ico').write_bytes(struct.pack('<HHH', 0, 1, len(payloads)) + b''.join(entries) + b''.join(data for _, data in payloads))
write_json(web / 'site.webmanifest', {
    'name': 'Körkort · Your road to confidence', 'short_name': 'Körkort',
    'start_url': './', 'scope': './', 'display': 'standalone',
    'background_color': '#f7f8f3', 'theme_color': '#173e32',
    'icons': [{'src': f'icons/icon-{size}.png', 'sizes': f'{size}x{size}', 'type': 'image/png', 'purpose': 'any'} for size in (192, 512)] +
             [{'src': 'icons/icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}]
})

android = Path('composeApp/src/androidMain/res')
for density, scale in [('mdpi', 1), ('hdpi', 1.5), ('xhdpi', 2), ('xxhdpi', 3), ('xxxhdpi', 4)]:
    export(android / f'mipmap-{density}/ic_launcher.png', int(48 * scale))
    export(android / f'mipmap-{density}/ic_launcher_round.png', int(48 * scale), int(38 * scale))
    export(android / f'mipmap-{density}/ic_launcher_foreground.png', int(108 * scale), int(66 * scale))
for name in ('ic_launcher', 'ic_launcher_round'):
    path = ROOT / android / f'mipmap-anydpi-v26/{name}.xml'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background" />
    <foreground android:drawable="@mipmap/ic_launcher_foreground" />
</adaptive-icon>
''')
path = ROOT / android / 'values/icon_colors.xml'
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text('<resources><color name="ic_launcher_background">#173E32</color></resources>\n')
export('design/app-icon/google-play-512.png', 512)

ios = Path('iosApp/Assets.xcassets')
info = {'author': 'xcode', 'version': 1}
write_json(ios / 'Contents.json', {'info': info})
images = []
for idiom, sizes in [('iphone', [(20, [2, 3]), (29, [2, 3]), (40, [2, 3]), (60, [2, 3])]), ('ipad', [(20, [1, 2]), (29, [1, 2]), (40, [1, 2]), (76, [1, 2]), (83.5, [2])]), ('ios-marketing', [(1024, [1])])]:
    for size, scales in sizes:
        for scale in scales:
            pixels = int(size * scale)
            filename = f'icon-{pixels}.png'
            export(ios / 'AppIcon.appiconset' / filename, pixels)
            images.append({'idiom': idiom, 'size': f'{size}x{size}', 'scale': f'{scale}x', 'filename': filename})
write_json(ios / 'AppIcon.appiconset/Contents.json', {'images': images, 'info': info})
print('Exported web, Android, iPhone, iPad and store icons.')
