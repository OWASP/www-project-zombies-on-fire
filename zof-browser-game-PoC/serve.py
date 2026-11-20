#!/usr/bin/env python3
"""
Serve Zombies on Fire on http://127.0.0.1 so the page can talk to a local Ollama.

    python serve.py              # serves this folder on the first free port from 8737
    python serve.py --port 9000

Ollama accepts browser requests from 127.0.0.1 by default, so no Ollama settings
need to change. Opening the HTML file straight from disk can't reach Ollama.
Standard library only.
"""
import argparse
import functools
import http.server
import json
import urllib.request
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent


def ollama_status(base="http://127.0.0.1:11434") -> str:
    try:
        with urllib.request.urlopen(f"{base}/api/tags", timeout=2) as r:
            models = [m["name"] for m in json.load(r).get("models", [])]
        return f"Ollama is running with {len(models)} model(s): {', '.join(models[:5]) or 'none yet'}"
    except OSError:
        return "Ollama isn't running (optional). Install it from ollama.com, then: ollama pull llama3.1:8b"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Serves the folder without a log line for every image, so the window stays readable for the Fire Marshal."""
    def log_message(self, *args):
        pass


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8737)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()
    page = next((p.name for p in (HERE / "zombies-on-fire.html", HERE / "index.html") if p.exists()), "")
    handler = functools.partial(QuietHandler, directory=str(HERE))
    httpd = None
    for port in list(range(args.port, args.port + 50)) + [0]:      # the first free port, else any free port
        try:
            httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
            break
        except OSError:
            continue
    url = f"http://127.0.0.1:{httpd.server_address[1]}/{page}"
    with httpd:
        print(f"Zombies on Fire: {url}")
        print(ollama_status())
        print("Press Ctrl+C to stop.")
        if not args.no_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
