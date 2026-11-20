OWASP Zombies on Fire - browser game

START
  Windows:  double-click start.bat
  macOS:    double-click start.command (first time: right-click > Open)
  Linux:    ./start.sh

  It finds a free port, opens the game in your browser, and keeps running until you
  close the window or press Ctrl+C. Needs Node.js 18+ (https://nodejs.org); without
  it, the launcher falls back to Python's basic server.

AI (optional)
  Local:  install Ollama (https://ollama.com), run: ollama pull llama3.1:8b
          then choose "Ollama on this computer" in AI settings.
  Cloud:  choose OpenAI-compatible or Anthropic in AI settings and paste a key, or keep
          keys out of the browser by setting them before you start:
            OPENAI_API_KEY (and OPENAI_BASE_URL for LM Studio, vLLM, ...), ANTHROPIC_API_KEY
  All AI calls go through the local server, so no CORS or OLLAMA_ORIGINS setup is needed.

  Small or slow local model? The game only ever asks it for one small piece at a time (one
  ruling, one move, one Signal), shows the answer arriving, and falls back to the rules engine
  or the standard text for any piece it can't manage. "Build it without AI" on the home screen
  makes a new Outbreak with no model at all.

MENU
  Menu (top left): new game, restart, end the game early, undo the last round, settings.
  The game saves itself in the browser: refresh or reopen the page and it carries on where it was.

RULES
  Click Rules in the game for the full reference: every card that adds or removes fire, spawns
  a zombie or changes how many cards you play, and how to avoid it. Download (.md) saves a copy.

AT AN EVENT
  Connect the projector as a second display (extended). Click "Table view" in the game, drag
  that window to the projector and press F. Press S there to show Signal headlines only.
  The game screen stays with the Fire Marshal. Before the day, run AI settings > Game-day check
  on the laptop you'll use: it tells you whether the model can be Fire Marshal or should only
  help (teammates, Suggest, AI coach). If the AI stops answering, the rules engine takes over.

OPTIONS
  start --port 9000    look for a free port starting at 9000 (default 8737)
  start --no-open      don't open a browser
