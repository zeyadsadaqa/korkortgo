"""Check source, approval and bundled font integrity before a reproducible build."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / "pdf-production/build-manifest.json").read_text())
errors = []
chapters = manifest["chapters"]
if [c["id"] for c in chapters] != [f"M{i:02d}" for i in range(1, 11)]:
    errors.append("Chapter coverage differs from M01-M10")
text = (root / "manuscript.md").read_text()
for c in chapters:
    for identifier in c["lessons"] + [c["review"]]:
        if text.count("### " + identifier + " · ") != 1:
            errors.append(f"Missing or repeated manuscript heading: {identifier}")
for name, expected in manifest["input_sha256"].items():
    path = root / name
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        errors.append(f"Changed input; review and refresh snapshot: {name}")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("Preparation integrity passed: 10 chapters, 40 lessons and 10 reviews.")
for record in json.loads((root / "pdf-production/fonts/manifest.json").read_text())["files"]:
    path = root / "pdf-production" / record["file"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"], path
assert manifest["status"] == "6A_complete_screen_review"
print("6A input/font integrity passed. Run build.py and verify.py for artifact checks.")
