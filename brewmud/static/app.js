let token = null;
let pollTimer = null;
let audioContext = null;
let soundEnabled = true;
let pendingWelcome = "";
const terminal = document.querySelector("#terminal");
const commandInput = document.querySelector("#command");

function append(text, kind = "world") {
  if (!text) return;
  const block = document.createElement("div");
  block.className = `message ${kind}`;
  if (text.startsWith("REGIONAL MAP") || text.startsWith("BREWMUD REGIONAL MAPS")) {
    block.classList.add("regional-map");
  }
  if (text.includes("POP QUIZ!")) {
    block.classList.add("pop-quiz");
    announcePopQuiz();
  }
  const lines = text.split("\n");
  const exitsIndex = lines.findIndex((line) => line.startsWith("Exits:"));
  let roomTitleIndex = exitsIndex >= 0 ? 0 : -1;
  for (let index = 0; index < exitsIndex; index += 1) {
    if (lines[index] === "") roomTitleIndex = index + 1;
  }
  lines.forEach((line, index) => {
    const row = document.createElement("div");
    row.className = classifyLine(line, index, roomTitleIndex);
    appendHighlights(row, line);
    block.appendChild(row);
  });
  terminal.appendChild(block);
  terminal.scrollTop = terminal.scrollHeight;
}

function ensureAudio() {
  if (!audioContext) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (AudioContext) audioContext = new AudioContext();
  }
  if (audioContext?.state === "suspended") audioContext.resume();
}

function announcePopQuiz() {
  document.body.classList.remove("quiz-flash");
  // Restart the animation even when two UI events occur close together.
  void document.body.offsetWidth;
  document.body.classList.add("quiz-flash");
  window.setTimeout(() => document.body.classList.remove("quiz-flash"), 900);

  if (!soundEnabled) return;
  ensureAudio();
  if (!audioContext) return;
  const start = audioContext.currentTime;
  [523.25, 659.25, 783.99].forEach((frequency, index) => {
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();
    const noteStart = start + index * 0.11;
    oscillator.type = "sine";
    oscillator.frequency.value = frequency;
    gain.gain.setValueAtTime(0.0001, noteStart);
    gain.gain.exponentialRampToValueAtTime(0.045, noteStart + 0.015);
    gain.gain.exponentialRampToValueAtTime(0.0001, noteStart + 0.1);
    oscillator.connect(gain).connect(audioContext.destination);
    oscillator.start(noteStart);
    oscillator.stop(noteStart + 0.11);
  });
}

document.querySelector("#sound-toggle").addEventListener("click", () => {
  soundEnabled = !soundEnabled;
  const button = document.querySelector("#sound-toggle");
  button.textContent = `Sound: ${soundEnabled ? "on" : "off"}`;
  button.setAttribute("aria-pressed", String(soundEnabled));
  if (soundEnabled) ensureAudio();
});

function classifyLine(line, index, roomTitleIndex) {
  if (line.startsWith("QUEST") || line.startsWith("OBJECTIVE") || line.startsWith("KNOWLEDGE CHECK") || line.startsWith("POP QUIZ") || line.startsWith("CONTINUE") || line.startsWith("REGIONAL MAP") || line.startsWith("BREWMUD REGIONAL MAPS") || line.startsWith("Regional Transitions")) return "objective";
  if (line.startsWith("Objectives:")) return "quest-summary";
  if (line.startsWith("YOU ARE HERE")) return "room-title";
  if (index === roomTitleIndex) return "room-title";
  if (line.startsWith("Exits:") || line.startsWith("Local routes:")) return "exits";
  if (line.startsWith("Nearby:") || line.startsWith("Players here:")) return "npcs";
  if (line.includes("“") || line.includes("”")) return "npc-chatter";
  if (line.startsWith("INSIGHT -")) return "penalty";
  if (line.startsWith("Discovery:") || line.startsWith("INSIGHT") || line.startsWith("RANK UP")) return "reward";
  if (/^\s+[A-D]\. /.test(line) || line.startsWith("Use ANSWER")) return "quiz-option";
  return "";
}

function appendHighlights(row, line) {
  const highlightPattern = /<[A-Z0-9]{3,4}>|\b(north|south|east|west|up|down|in|out)\b/gi;
  let cursor = 0;
  for (const match of line.matchAll(highlightPattern)) {
    row.appendChild(document.createTextNode(line.slice(cursor, match.index)));
    const highlight = document.createElement("span");
    highlight.className = match[0].startsWith("<") ? "map-current" : "direction";
    highlight.textContent = match[0];
    row.appendChild(highlight);
    cursor = match.index + match[0].length;
  }
  row.appendChild(document.createTextNode(line.slice(cursor)));
}

async function api(path, options = {}) {
  const response = await fetch(path, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
}

function enterGame() {
  document.removeEventListener("keydown", continueFromInstructions);
  document.querySelector("#instructions").hidden = true;
  document.querySelector("#game").hidden = false;
  append(pendingWelcome);
  pendingWelcome = "";
  commandInput.focus();
  pollTimer = window.setInterval(poll, 900);
}

function continueFromInstructions(event) {
  if (document.querySelector("#instructions").hidden) return;
  if (event) event.preventDefault();
  enterGame();
}

document.querySelector("#instructions-continue").addEventListener("click", continueFromInstructions);

document.querySelector("#login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (soundEnabled) ensureAudio();
  const error = document.querySelector("#login-error");
  error.textContent = "";
  const action = event.submitter?.dataset.action || "login";
  try {
    const data = await api(`/api/${action === "register" ? "register" : "login"}`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        name: document.querySelector("#name").value,
        password: document.querySelector("#password").value,
      }),
    });
    token = data.token;
    pendingWelcome = data.output;
    document.querySelector("#login").hidden = true;
    document.querySelector("#status").textContent = "connected";
    if (data.show_instructions) {
      document.querySelector("#instructions").hidden = false;
      document.addEventListener("keydown", continueFromInstructions);
      document.querySelector("#instructions-continue").focus();
    } else {
      enterGame();
    }
  } catch (err) {
    error.textContent = err.message;
  }
});

document.querySelector("#command-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (soundEnabled) ensureAudio();
  const command = commandInput.value.trim();
  if (!command || !token) return;
  append(`command> ${command}`, "command");
  commandInput.value = "";
  try {
    const data = await api("/api/command", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({token, command}),
    });
    append(data.output);
  } catch (err) {
    append(err.message, "error");
  }
});

async function poll() {
  if (!token) return;
  try {
    const data = await api(`/api/events?token=${encodeURIComponent(token)}`);
    data.messages.forEach((message) => append(message, "social"));
  } catch (err) {
    window.clearInterval(pollTimer);
    document.querySelector("#status").textContent = "disconnected";
    append(err.message, "error");
  }
}

window.addEventListener("pagehide", () => {
  if (token) {
    navigator.sendBeacon("/api/logout", new Blob(
      [JSON.stringify({token})], {type: "application/json"}
    ));
  }
});
