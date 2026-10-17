"""Record real TalkBack focus movement without UiAutomation intercepting input.
Use native pointer swipes in the emulator while this collector runs. Injected adb
keys/swipes are not accepted as proof. Requires Pillow; restores original settings.
"""
import argparse
import io
import json
import subprocess
import time
from pathlib import Path
from PIL import Image

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--adb', default='/Users/zeyad/Library/Android/sdk/platform-tools/adb')
parser.add_argument('--device', default='emulator-5554')
parser.add_argument('--mode', default='learning')
parser.add_argument('--code', default='S1')
parser.add_argument('--positions', type=int, default=5)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()

def adb(*commands, binary=False):
    result = subprocess.run([args.adb, '-s', args.device, *commands], capture_output=True, check=True, timeout=15)
    return result.stdout if binary else result.stdout.decode().strip()

original = adb('shell', 'settings', 'get', 'secure', 'enabled_accessibility_services')
original_enabled = adb('shell', 'settings', 'get', 'secure', 'accessibility_enabled')
service = 'com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService'
args.output.mkdir(parents=True, exist_ok=True)
visited = []
try:
    services = [] if original in ('null', '') else original.split(':')
    if service not in services:
        services.append(service)
    adb('shell', 'settings', 'put', 'secure', 'enabled_accessibility_services', ':'.join(services))
    adb('shell', 'am', 'start', '-S', '-W', '-n', 'se.korkort.study.verification/se.korkort.DeliveryProofActivity', '--es', 'mode', args.mode, '--es', 'code', args.code)
    (args.output / 'accessibility-service.txt').write_text(adb('shell', 'dumpsys', 'accessibility'))
    time.sleep(1.5)  # Exclude launch-transition frames from focus evidence.
    print('Ready for real emulator pointer swipes.', flush=True)
    deadline = time.monotonic() + 50
    while time.monotonic() < deadline:
        png = adb('exec-out', 'screencap', '-p', binary=True)
        image = Image.open(io.BytesIO(png)).convert('RGB')
        # TalkBack paints its focus outline green. Keep full-resolution captures
        # and exact bounds for visual review; text/content correctness is reviewed separately.
        r, g, b = image.split()
        from PIL import ImageChops
        mask = ImageChops.multiply(ImageChops.subtract(g, r).point(lambda x: 255 if x > 60 else 0), ImageChops.subtract(g, b).point(lambda x: 255 if x > 60 else 0))
        bounds = mask.getbbox()
        if bounds and (not visited or list(bounds) != visited[-1]['focus_bounds']):
            name = f'focus-{len(visited):02d}.png'
            (args.output / name).write_bytes(png)
            visited.append({'focus_bounds': list(bounds), 'screenshot': name})
            (args.output / 'traversal.json').write_text(json.dumps(visited, indent=2) + '\n')
            print(name, bounds, flush=True)
        if len({tuple(row['focus_bounds']) for row in visited}) >= args.positions:
            break
        time.sleep(0.2)
    assert len({tuple(row['focus_bounds']) for row in visited}) >= args.positions, 'Required distinct native TalkBack focus positions were not observed'
    print('Real TalkBack focus traversal recorded; review the screenshots for exact reading content.', flush=True)
finally:
    if original in ('null', ''):
        adb('shell', 'settings', 'delete', 'secure', 'enabled_accessibility_services')
    else:
        adb('shell', 'settings', 'put', 'secure', 'enabled_accessibility_services', original)
    if original_enabled in ('null', ''):
        adb('shell', 'settings', 'delete', 'secure', 'accessibility_enabled')
    else:
        adb('shell', 'settings', 'put', 'secure', 'accessibility_enabled', original_enabled)
