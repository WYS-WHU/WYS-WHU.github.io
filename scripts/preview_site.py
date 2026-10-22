"""Loopback-only preview with cached, automatic public ModelScope counters."""
import argparse
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Event, Lock, Thread
from urllib.parse import urlsplit

from build_site import public_metrics
from refresh_metrics import refresh_metrics

ROOT = Path(__file__).resolve().parents[1]
REFRESH_SECONDS = 600
STOP = Event()
SNAPSHOT_LOCK = Lock()
SNAPSHOT = None


def publish_snapshot(metrics):
    global SNAPSHOT
    value = public_metrics(metrics)
    destination = ROOT / "dist" / "assets" / "metrics.json"
    temporary = destination.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(value) + "\n", encoding="utf-8")
    temporary.replace(destination)
    with SNAPSHOT_LOCK:
        SNAPSHOT = value


def refresh_loop():
    while not STOP.is_set():
        try:
            metrics = refresh_metrics()
            publish_snapshot(metrics)
            print("ModelScope counters refreshed: " + ", ".join(str(i["value"]) for i in metrics["items"]), flush=True)
        except Exception as error:
            print(f"Counters unchanged; next attempt in {REFRESH_SECONDS}s: {error}", flush=True)
        STOP.wait(REFRESH_SECONDS)


class PreviewHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if urlsplit(self.path).path == "/api/metrics":
            with SNAPSHOT_LOCK:
                body = json.dumps(SNAPSHOT).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()
    if not (ROOT / "dist" / "index.html").is_file():
        parser.error("Run python scripts/build_site.py first")
    publish_snapshot(json.loads((ROOT / "content" / "metrics.json").read_text(encoding="utf-8")))
    handler = partial(PreviewHandler, directory=str(ROOT / "dist"))
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
        Thread(target=refresh_loop, daemon=True).start()
        print(f"Local preview: http://127.0.0.1:{args.port}/ (counters refresh every 10 minutes)", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            STOP.set()


if __name__ == "__main__":
    main()
