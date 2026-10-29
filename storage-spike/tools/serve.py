"""Serve only the isolated proof on localhost; --no-isolation tests the negative case."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=18765)
parser.add_argument("--no-isolation", action="store_true")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1] / "build/dist/wasmJs/productionExecutable"
if not (root / "index.html").is_file():
    parser.error("Build wasmJsBrowserDistribution first")


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        if not args.no_isolation:
            self.send_header("Cross-Origin-Opener-Policy", "same-origin")
            self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(Handler, directory=str(root)))
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
