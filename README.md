# OWASP Zombies on Fire

Open-source cybersecurity tabletop exercises for practicing incident response. Play a ready-made scenario in the browser, run a discussion-based exercise with the Markdown templates, or use the portal to generate facilitator and participant materials.

## Play a scenario

Open [Zombies on Fire](games/zombies-on-fire/zombies-on-fire.html) in a browser to play without AI. Start with **First Shift** to learn the rules or choose another exercise from the [scenario catalog](templates/games/README.md).

For optional AI, run `sh start.sh` from the repository root on macOS or Linux, or run `start.bat` on Windows. The launcher prefers Node.js 18+ and falls back to a basic Python server. See the [game instructions](games/zombies-on-fire/README.txt) for provider setup and the projector view.

## Run or design a tabletop

Copy the [game template](templates/games/tabletop-game.md) for a new exercise. It follows the portal’s four questions (Overview, Challenges, Twists, and Conclusion) and includes facilitator setup, participant instructions, injects, assessment, and after-action review. For an existing scenario, use the catalog to select an Outbreak and use its rounds and Signals to guide the session.

## Generate exercise materials with the portal

The [FastAPI portal](portal/README.md) turns the same four questions into six documents with PDF export. From the repository root, run the following with Python 3.11 or later on macOS or Linux.

```sh
cd portal
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Set SECRET_KEY in .env to a fresh local value before starting.
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/app` for the UI or `http://127.0.0.1:8000/api/docs` for the API. The example configuration uses the mock provider for local testing. The browser game and authoring portal run independently in this checkout. Keep the portal local unless you have reviewed its registration and CORS settings, since public registration currently grants administrator privileges.

See the [deployment guide](portal/DEPLOYMENT.md) for Docker, Windows, and other deployment options.

## Run the test harness

From the repository root, run `python3 tests/run.py` with Python 3.11+ and Node.js 18+. It exercises the opening round of every built-in game with the rules engine, checks artwork, and validates discovered templates.

Install [the portal dependencies](portal/requirements.txt) into a virtual environment and run `python tests/run.py --portal` to exercise registration, login, tabletop creation, document generation, and PDF downloads. The portal checks use a temporary SQLite database and the mock AI provider.

Put new Markdown, text, or JSON files anywhere under [templates/games/](templates/games/). The harness checks Markdown and text files for readable, nonempty UTF-8 content. To run a template through the portal, copy the [sample JSON fixture](tests/fixtures/tabletop.json) and fill in its title and four exercise answers. The harness discovers JSON fixtures automatically and runs each through all six document types when you pass `--portal`.

## Repository layout

- [games/zombies-on-fire/](games/zombies-on-fire/) contains the standalone game, artwork, and local servers.
- [templates/games/](templates/games/) contains the reusable tabletop template and built-in scenario catalog.
- [portal/](portal/) contains the authoring app and its document generators.
- [index.md](index.md) contains the public OWASP project overview and roadmap.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance and [LICENSE.md](LICENSE.md) for licensing.
