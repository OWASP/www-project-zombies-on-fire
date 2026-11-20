#!/usr/bin/env sh
# Start Zombies on Fire: finds a free port, opens your browser, and handles AI calls (no CORS setup).
# Usage: ./start.sh [--port 9000] [--no-open]
cd "$(dirname "$0")" || exit 1
if command -v node >/dev/null 2>&1 && [ "$(node -p 'parseInt(process.versions.node)')" -ge 18 ] 2>/dev/null; then
  exec node server.js "$@"
fi
echo "Node.js 18 or newer gives the best experience (AI calls without CORS setup): https://nodejs.org"
for py in python3 python; do
  if command -v "$py" >/dev/null 2>&1; then
    echo "Starting the basic Python server instead (Ollama works; some cloud AI servers may not)."
    exec "$py" serve.py
  fi
done
echo "Please install Node.js 18+ (https://nodejs.org) and run this again."
exit 1
