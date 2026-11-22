const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const game = path.resolve(__dirname, '../games/zombies-on-fire');
const html = fs.readFileSync(path.join(game, 'zombies-on-fire.html'), 'utf8');
const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)]
  .map(([, source]) => new vm.Script(source));
const context = vm.createContext({});
context.window = context;
for (const script of scripts) {
  script.runInContext(context, { timeout: 2000 });
  if (context.ZOF?.engine) break;
}

const { DATA, engine } = context.ZOF;
assert.ok(DATA.outbreakOrder.length, 'No built-in scenarios found');
assert.equal(new Set(DATA.outbreakOrder).size, DATA.outbreakOrder.length);
for (const id of DATA.outbreakOrder) {
  const scenario = DATA.outbreaks[id];
  assert.ok(scenario?.rounds.length, `${id} has no rounds`);
  const options = { outbreak: id, players: 4, seed: 7 };
  const state = engine.newGame(DATA, options);
  const snapshot = JSON.stringify(state);
  assert.equal(snapshot, JSON.stringify(engine.newGame(DATA, options)), `${id} is not reproducible`);
  const next = engine.resolveRound(DATA, state, [], {}, {});
  assert.equal(next.history.length, 1, `${id} did not resolve its opening round`);
  assert.equal(JSON.stringify(state), snapshot, `${id} mutated the original state`);
}

const artwork = new Set(html.match(/art\/[\w.-]+\.(?:jpe?g|png|webp|svg)\b/g));
assert.ok(artwork.size, 'No artwork references found');
for (const asset of artwork) {
  assert.ok(fs.statSync(path.join(game, asset)).isFile(), `Missing game asset ${asset}`);
}
console.log(`Checked ${DATA.outbreakOrder.length} opening rounds and ${artwork.size} artwork references.`);
