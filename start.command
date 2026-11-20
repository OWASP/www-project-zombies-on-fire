#!/usr/bin/env sh
cd "$(dirname "$0")" || exit 1
exec sh games/zombies-on-fire/start.sh "$@"
