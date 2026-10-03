let token = null;
let pollTimer = null;
let audioContext = null;
let soundEnabled = true;
let pendingWelcome = "";
let awaitingQuizContinue = false;
const terminal = document.querySelector("#terminal");
const commandInput = document.querySelector("#command");
const surveyDialog = document.querySelector("#survey-dialog");
const surveyForm = document.querySelector("#survey-form");
const scenePicture = document.querySelector("#scene-picture");
const sceneHotspots = document.querySelector("#scene-hotspots");
const sceneTalkActions = document.querySelector("#scene-talk-actions");
const sceneCaption = document.querySelector("#scene-caption");
const quizControls = document.querySelector("#quiz-controls");
const sceneArt = {
  brewery_gate: "/art/brewery-gate-with-npc.webp",
  grain_receiving: "/art/grain-receiving-with-npc.webp",
  barley_lab: "/art/barley-lab.webp",
  steep_house: "/art/steep-house-with-npc.webp",
  air_rest: "/art/air-rest.webp",
  germination_floor: "/art/germination-floor.webp",
  aleurone: "/art/aleurone.webp",
  endosperm: "/art/endosperm.webp",
  kiln: "/art/kiln-with-npc.webp",
  cure_floor: "/art/malt-curing-floor-with-npc.webp",
  water_lab: "/art/water-lab-with-npc.webp",
  ph_bench: "/art/ph-bench.webp",
  ion_gallery: "/art/ion-gallery.webp",
  city_profiles: "/art/city-profiles-with-npc.webp",
  treatment_bay: "/art/treatment-bay-with-npc.webp",
  mill_room: "/art/mill-room-with-npc.webp",
  mash_tun: "/art/mash-tun-with-npc.webp",
  carbohydrate_lab: "/art/carbohydrate-lab-with-npc.webp",
  glucose_bench: "/art/glucose-bench.webp",
  disaccharide_gallery: "/art/disaccharide-gallery.webp",
  polymer_comparison: "/art/polymer-comparison.webp",
  gelatinization_chamber: "/art/gelatinization-chamber.webp",
  crystallinity_lab: "/art/crystallinity-lab.webp",
  amylose_helix: "/art/amylose-helix.webp",
  amylopectin_arbor: "/art/amylopectin-arbor.webp",
  protein_rest: "/art/protein-rest.webp",
  beta_rest: "/art/beta-rest.webp",
  alpha_rest: "/art/alpha-rest.webp",
  conversion_bench: "/art/conversion-bench.webp",
  mash_out: "/art/mash-out.webp",
  amino_acid_gallery: "/art/amino-acid-gallery.webp",
  peptide_bond_bench: "/art/peptide-bond-bench.webp",
  protein_structure_gallery: "/art/protein-structure-gallery.webp",
  folding_chamber: "/art/folding-chamber.webp",
  denaturation_bay: "/art/denaturation-bay.webp",
  enzyme_catalysis_lab: "/art/enzyme-catalysis-lab.webp",
  active_site_workshop: "/art/active-site-workshop.webp",
  enzyme_conditions_lab: "/art/enzyme-conditions-lab.webp",
  amylase_mechanism_lab: "/art/amylase-mechanism-lab.webp",
  mash_thickness_station: "/art/mash-thickness-station.webp",
  accessory_enzyme_lab: "/art/accessory-enzyme-lab.webp",
  iodine_test_alcove: "/art/iodine-test-alcove.webp",
  lauter_tun: "/art/lauter-tun.webp",
  grain_bed: "/art/grain-bed.webp",
  sparge_arm: "/art/sparge-arm.webp",
  wort_grant: "/art/wort-grant.webp",
  kettle: "/art/kettle.webp",
  hot_break: "/art/hot-break.webp",
  hop_dosing: "/art/hop-dosing.webp",
  whirlpool: "/art/whirlpool.webp",
  heat_exchanger: "/art/heat-exchanger.webp",
  oxygenation_station: "/art/oxygenation-station.webp",
  pitching_deck: "/art/pitching-deck.webp",
  ale_fermenter: "/art/ale-fermenter.webp",
  lager_fermenter: "/art/lager-fermenter.webp",
  yeast_lab: "/art/yeast-lab.webp",
  yeast_membrane: "/art/yeast-membrane.webp",
  maltose_gate: "/art/maltose-gate.webp",
  maltase_bench: "/art/maltase-bench.webp",
  glycolysis_lane: "/art/glycolysis-lane.webp",
  nad_recycling: "/art/nad-recycling.webp",
  lipid_workshop: "/art/lipid-workshop.webp",
  ester_lab: "/art/ester-lab.webp",
  diacetyl_rest: "/art/diacetyl-rest.webp",
  sulfur_vent: "/art/sulfur-vent.webp",
  maturation_cellar: "/art/maturation-cellar.webp",
  hop_yard: "/art/hop-yard.webp",
  female_cone: "/art/female-cone.webp",
  lupulin_gland: "/art/lupulin-gland.webp",
  alpha_acid_bench: "/art/alpha-acid-bench.webp",
  oil_lab: "/art/oil-lab.webp",
  ibu_station: "/art/ibu-station.webp",
  dry_hop_gallery: "/art/dry-hop-gallery.webp",
  lightstrike_booth: "/art/lightstrike-booth.webp",
  brite_tank: "/art/brite-tank.webp",
  carbonation_station: "/art/carbonation-station.webp",
  bottle_line: "/art/bottle-line.webp",
  canning_line: "/art/canning-line.webp",
  nitrogen_tap: "/art/nitrogen-tap.webp",
  foam_lab: "/art/foam-lab.webp",
  sensory_room: "/art/sensory-room.webp",
  style_taproom: "/art/style-taproom.webp",
  cold_storage: "/art/cold-storage.webp",
  shipping_dock: "/art/shipping-dock.webp",
  microbiology_lab: "/art/microbiology-lab.webp",
  sanitation_bay: "/art/sanitation-bay.webp",
  qa_chemistry: "/art/qa-chemistry.webp",
  yeast_bank: "/art/yeast-bank.webp",
  pilot_brewery: "/art/pilot-brewery.webp",
  training_classroom: "/art/training-classroom.webp",
};
const sceneObjectPositions = {
  brewery_gate: [28, 70], grain_receiving: [25, 72], barley_lab: [43, 48],
  steep_house: [31, 61], air_rest: [49, 56], germination_floor: [83, 69],
  aleurone: [42, 38], endosperm: [52, 51], kiln: [78, 42],
  cure_floor: [44, 55], water_lab: [51, 62], ph_bench: [49, 63],
  ion_gallery: [52, 37], city_profiles: [25, 48], treatment_bay: [31, 52],
  mill_room: [53, 54], mash_tun: [46, 62], carbohydrate_lab: [50, 64],
  glucose_bench: [48, 63], disaccharide_gallery: [50, 55],
};
const exitArrows = {
  north: "↑", south: "↓", east: "→", west: "←",
  up: "↑", down: "↓", in: "↪", out: "↩",
};
let currentScene = null;
let preferredView = "adventure";
let sceneBusy = false;
let sceneCaptionCommand = null;

function setView(view) {
  preferredView = view;
  if (view === "text") hideSceneCaption();
  const available = Boolean(currentScene && sceneArt[currentScene.key] && !currentScene.hidden);
  const illustrated = view === "adventure";
  document.querySelector("#game").classList.toggle("illustrated-mode", illustrated);
  document.querySelector("#adventure").hidden = !illustrated || !available;
  document.querySelector("#adventure-view-button").setAttribute("aria-pressed", String(illustrated));
  document.querySelector("#text-view-button").setAttribute("aria-pressed", String(!illustrated));
  const note = document.querySelector("#adventure-availability");
  note.textContent = currentScene?.hidden ? "Finish or pause the quiz to see the room."
    : available ? "Click to play. Switch to Classic text anytime."
      : "The room illustration is unavailable; use the action buttons or Classic text.";
}

document.querySelector("#adventure-view-button").addEventListener("click", () => setView("adventure"));
document.querySelector("#text-view-button").addEventListener("click", () => {
  setView("text");
  commandInput.focus();
});

function updateScene(scene) {
  hideSceneCaption();
  currentScene = scene;
  sceneHotspots.replaceChildren();
  sceneTalkActions.replaceChildren();
  if (scene && !scene.hidden && sceneArt[scene.key]) {
    document.querySelector("#scene-title").textContent = scene.name;
    scenePicture.src = sceneArt[scene.key];
    scenePicture.alt = `Illustration of ${scene.name}; interactive targets are labeled on the picture.`;
    scene.npcs.forEach((npc) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = `Talk to ${npc.name}`;
      button.addEventListener("click", () => sendGameCommand(`talk ${npc.key}`, `Talking to ${npc.name}`));
      sceneTalkActions.appendChild(button);
    });
    scene.features.forEach((feature, index) => {
      const [x, y] = sceneObjectPositions[scene.key] || [33, 66];
      addHotspot("object", feature, `look ${feature}`, x + index * 12, y);
    });
    scene.exits.forEach((exit) => {
      const point = exitPoint(exit.direction);
      addHotspot("exit", `${exit.direction.toUpperCase()} ${exitArrows[exit.direction]} ${exit.name}`,
        exit.direction, point.x, point.y);
    });
    updateScenePlayers(scene.players);
  }
  setView(preferredView);
}

function updateInteraction(interaction, output = "") {
  const mode = interaction?.mode || "explore";
  quizControls.hidden = mode === "explore";
  quizControls.dataset.mode = mode;
  const topic = document.querySelector("#quiz-topic");
  const prompt = document.querySelector("#quiz-prompt");
  const feedback = document.querySelector("#quiz-feedback");
  const options = document.querySelector("#quiz-options");
  const actions = document.querySelector("#quiz-actions");
  options.replaceChildren();
  actions.replaceChildren();
  feedback.hidden = true;
  if (mode === "explore") return;
  topic.textContent = mode === "continue" ? "Knowledge check complete" : `Knowledge check · ${interaction.topic}`;
  prompt.textContent = mode === "active" ? interaction.prompt
    : mode === "paused" ? "Quiz paused — review the topic, then resume."
      : "Read the explanation, then reveal the room.";
  if ((mode === "continue" || mode === "paused") && output) {
    feedback.textContent = output;
    feedback.hidden = false;
  }
  function addAction(label, command) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.addEventListener("click", () => sendGameCommand(command, command === "notes" ? label : ""));
    actions.appendChild(button);
  }
  if (mode === "active") {
    interaction.options.forEach((choice) => {
      const button = document.createElement("button");
      button.type = "button";
      const letter = document.createElement("span");
      letter.className = "quiz-option-letter";
      letter.textContent = `${choice.letter}.`;
      button.append(letter, document.createTextNode(choice.text));
      button.addEventListener("click", () => sendGameCommand(choice.letter));
      options.appendChild(button);
    });
    addAction("Pause and review", "pause");
  } else if (mode === "paused") {
    addAction("Resume quiz", "quiz");
    addAction("Read notes", "notes");
  } else if (mode === "continue") {
    addAction("Continue to room", "continue");
  }
}

document.querySelectorAll("#click-actions [data-command]").forEach((button) => {
  button.addEventListener("click", () => {
    const command = button.dataset.command;
    sendGameCommand(command, command === "survey" ? "" : button.textContent);
  });
});

document.querySelector("#leave-game").addEventListener("click", async () => {
  if (!token || sceneBusy) return;
  sceneBusy = true;
  try {
    await api("/api/logout", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({token}),
    });
    returnToLogin("You left the brewery. Your progress is saved.");
  } catch (err) {
    if (handleSessionError(err)) return;
    append(err.message, "error");
  } finally {
    sceneBusy = false;
  }
});

function updateScenePlayers(players) {
  document.querySelector("#scene-players").textContent = players?.length
    ? `Other players here: ${players.join(", ")}` : "";
}

function hideSceneCaption() {
  sceneCaption.hidden = true;
  sceneCaptionCommand = null;
}

function showSceneCaption(title, content) {
  if (!currentScene || currentScene.hidden || !sceneArt[currentScene.key] || !content) return;
  document.querySelector("#scene-caption-title").textContent = title;
  document.querySelector("#scene-caption-text").textContent = content;
  sceneCaption.hidden = false;
  sceneCaption.scrollTop = 0;
}

document.querySelector("#scene-caption-close").addEventListener("click", hideSceneCaption);
sceneCaption.addEventListener("click", (event) => {
  // A low-placed Look target may be covered by its own caption. Clicking the
  // caption at the same cursor position should close it too.
  if (event.target.closest("button")) return;
  hideSceneCaption();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !sceneCaption.hidden) hideSceneCaption();
});

function addHotspot(kind, label, command, x, y) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `scene-hotspot ${kind}`;
  button.style.left = `${x}%`;
  button.style.top = `${y}%`;
  button.title = `${kind === "object" ? "Look at" : "Go to"} ${label}`;
  button.setAttribute("aria-label", button.title);
  const symbol = document.createElement("span");
  symbol.className = "hotspot-symbol";
  symbol.setAttribute("aria-hidden", "true");
  symbol.textContent = kind === "object" ? "◆" : exitArrows[command];
  const caption = document.createElement("span");
  caption.className = "hotspot-caption";
  caption.textContent = label;
  button.append(symbol, caption);
  button.addEventListener("click", () => sendGameCommand(command,
    kind === "object" ? `Looking at ${label}` : ""));
  sceneHotspots.appendChild(button);
}

function exitPoint(direction) {
  return ({north: {x: 50, y: 9}, south: {x: 50, y: 91},
    west: {x: 10, y: 50}, east: {x: 90, y: 50},
    in: {x: 77, y: 88}, out: {x: 23, y: 88},
    up: {x: 73, y: 9}, down: {x: 27, y: 91}})[direction] || {x: 50, y: 50};
}

function updateProgress(progress) {
  if (!progress) return;
  document.querySelector("#progress-rank").textContent = progress.rank;
  document.querySelector("#progress-insight").textContent = progress.insight;
  document.querySelector("#progress-locations").textContent = `${progress.locations}/${progress.locations_total}`;
  document.querySelector("#progress-quests").textContent = `${progress.quests}/${progress.quests_total}`;
  document.querySelector("#progress-checks").textContent = `${progress.knowledge_checks}/${progress.knowledge_checks_total}`;
  document.querySelector("#progress-next").textContent = progress.next_rank === "Highest current rank achieved"
    ? progress.next_rank
    : `Next rank: ${progress.next_rank}`;
}

function updateSidePanel(sidePanel) {
  if (!sidePanel) return;
  const quest = sidePanel.quest;
  document.querySelector("#quest-panel-title").textContent = quest.status;
  document.querySelector("#quest-title").textContent = quest.title;
  document.querySelector("#quest-description").textContent = quest.description;
  document.querySelector("#quest-objective").textContent = quest.objective;

  // A missing map means a pop quiz is intentionally hiding the new room.
  document.querySelector(".map-panel").hidden = !sidePanel.map;
  if (!sidePanel.map) return;
  const map = sidePanel.map;
  document.querySelector("#mini-map-title").textContent = map.title;
  document.querySelector("#mini-map-current").textContent = `Here: ${map.current_name}`;
  const questMarker = document.querySelector("#mini-map-quest");
  questMarker.hidden = !map.quest_marker;
  questMarker.textContent = map.quest_marker ? `★ ${map.quest_marker}` : "";
  const diagram = document.querySelector("#mini-map");
  diagram.replaceChildren();
  map.rows.forEach((nodes, rowIndex) => {
    const row = document.createElement("div");
    row.className = "mini-map-row";
    row.style.setProperty("--map-columns", nodes.length);
    if (rowIndex < map.rows.length - 1) row.classList.add("has-next-row");
    nodes.forEach((node) => {
      const marker = document.createElement("span");
      marker.className = `mini-map-node${node.current ? " current" : ""}${node.quest ? " quest" : ""}`;
      marker.textContent = node.quest ? `★${node.code}` : node.code;
      marker.title = node.name;
      marker.setAttribute("aria-label", `${node.name}${node.current ? ", your current location" : ""}${node.quest ? ", quest route marker" : ""}`);
      row.appendChild(marker);
    });
    diagram.appendChild(row);
  });
  diagram.setAttribute("aria-label", `${map.title} regional map. Current location: ${map.current_name}.`);
}

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
  if (line.startsWith("YOU ARE HERE")) return "room-title";
  if (index === roomTitleIndex) return "room-title";
  if (line.startsWith("Exits:") || line.startsWith("Local routes:")) return "exits";
  if (line.startsWith("Players here:")) return "players-here";
  if (line.startsWith("Nearby:")) return "npcs";
  if (line.includes("“") || line.includes("”")) return "npc-chatter";
  if (line.startsWith("INSIGHT -")) return "penalty";
  if (line.startsWith("Discovery:") || line.startsWith("INSIGHT") || line.startsWith("RANK UP")) return "reward";
  if (/^\s+[A-D]\. /.test(line) || line.startsWith("Use ANSWER")) return "quiz-option";
  return "";
}

function appendHighlights(row, line) {
  const trimmed = line.trimStart();
  const navigationLine = trimmed.startsWith("Exits:")
    || trimmed.startsWith("Local routes:")
    || trimmed.startsWith("Regional Transitions:")
    || trimmed.includes("Shortest route to ");
  const highlightPattern = navigationLine
    ? /<[A-Z0-9]{3,4}>|\b(north|south|east|west|up|down|in|out)\b/gi
    : /<[A-Z0-9]{3,4}>/g;
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
  if (!response.ok) {
    const error = new Error(data.error || "Request failed");
    error.code = data.code;
    throw error;
  }
  return data;
}

function returnToLogin(message) {
  if (pollTimer) window.clearInterval(pollTimer);
  pollTimer = null;
  token = null;
  pendingWelcome = "";
  awaitingQuizContinue = false;
  hideSceneCaption();
  currentScene = null;
  updateInteraction(null);
  document.removeEventListener("keydown", continueFromInstructions);
  if (surveyDialog.open) surveyDialog.close();
  document.querySelector("#instructions").hidden = true;
  document.querySelector("#game").hidden = true;
  document.querySelector("#login").hidden = false;
  document.querySelector("#status").textContent = "logged out";
  document.querySelector("#login-error").textContent = message;
  const password = document.querySelector("#password");
  password.value = "";
  password.focus();
}

function handleSessionError(error) {
  if (error.code !== "idle_timeout") return false;
  returnToLogin(error.message);
  return true;
}

async function openSurvey() {
  try {
    const data = await api(`/api/survey?token=${encodeURIComponent(token)}`);
    if (data.completed) {
      append("SURVEY COMPLETE — This account has already submitted the course evaluation.");
      return;
    }
    const questions = document.querySelector("#survey-questions");
    questions.replaceChildren();
    data.questions.forEach((question, index) => {
      const field = document.createElement("div");
      field.className = "survey-question";
      const label = document.createElement("label");
      const selectId = `survey-rating-${index}`;
      label.htmlFor = selectId;
      label.textContent = `${index + 1}. ${question}`;
      const select = document.createElement("select");
      select.id = selectId;
      select.dataset.surveyRating = "true";
      select.setAttribute("aria-describedby", "survey-scale");
      const unanswered = document.createElement("option");
      unanswered.value = "";
      unanswered.textContent = "Prefer not to answer";
      select.appendChild(unanswered);
      for (let score = data.scale_min; score <= data.scale_max; score += 1) {
        const option = document.createElement("option");
        option.value = String(score);
        option.textContent = String(score);
        select.appendChild(option);
      }
      field.append(label, select);
      questions.appendChild(field);
    });
    document.querySelector("#survey-scale").textContent =
      `${data.scale_min} = ${data.scale_low_label} · ${data.scale_max} = ${data.scale_high_label}`;
    document.querySelector("#survey-comment").value = "";
    document.querySelector("#survey-comment").maxLength = data.comment_limit;
    document.querySelector("#survey-error").textContent = "";
    surveyDialog.showModal();
    document.querySelector("#survey-rating-0").focus();
  } catch (err) {
    if (handleSessionError(err)) return;
    append(err.message, "error");
  }
}

function closeSurvey() {
  surveyDialog.close();
  commandInput.focus();
}

document.querySelector("#survey-close").addEventListener("click", closeSurvey);
document.querySelector("#survey-cancel").addEventListener("click", closeSurvey);

surveyForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const error = document.querySelector("#survey-error");
  error.textContent = "";
  const ratings = Array.from(document.querySelectorAll("[data-survey-rating]"), (select) =>
    select.value === "" ? null : Number(select.value)
  );
  try {
    const data = await api("/api/survey/submit", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        token,
        ratings,
        comment: document.querySelector("#survey-comment").value,
      }),
    });
    closeSurvey();
    append(data.message, "reward");
  } catch (err) {
    if (handleSessionError(err)) return;
    error.textContent = err.message;
  }
});

function enterGame() {
  document.removeEventListener("keydown", continueFromInstructions);
  document.querySelector("#instructions").hidden = true;
  document.querySelector("#game").hidden = false;
  append(pendingWelcome);
  pendingWelcome = "";
  if (preferredView === "text") commandInput.focus();
  else document.querySelector("#adventure-view-button").focus();
  if (pollTimer) window.clearInterval(pollTimer);
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
    terminal.replaceChildren();
    pendingWelcome = data.output;
    awaitingQuizContinue = Boolean(data.awaiting_continue);
    updateProgress(data.progress);
    updateSidePanel(data.side_panel);
    updateScene(data.scene);
    updateInteraction(data.interaction);
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

async function sendGameCommand(command, captionTitle = "") {
  if (sceneBusy) return;
  if (captionTitle && !sceneCaption.hidden && sceneCaptionCommand === command) {
    hideSceneCaption();
    return;
  }
  if (soundEnabled) ensureAudio();
  if (!command || !token) return;
  sceneBusy = true;
  append(`command> ${command}`, "command");
  try {
    const data = await api("/api/command", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({token, command}),
    });
    append(data.output);
    awaitingQuizContinue = Boolean(data.awaiting_continue);
    updateProgress(data.progress);
    updateSidePanel(data.side_panel);
    updateScene(data.scene);
    updateInteraction(data.interaction, data.output);
    if (captionTitle && data.scene && !data.scene.hidden && sceneArt[data.scene.key]) {
      showSceneCaption(captionTitle, data.output);
      sceneCaptionCommand = command;
    }
    if (data.open_survey) await openSurvey();
  } catch (err) {
    if (handleSessionError(err)) return;
    append(err.message, "error");
  } finally {
    sceneBusy = false;
  }
}

document.querySelector("#command-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const command = commandInput.value.trim();
  commandInput.value = "";
  await sendGameCommand(command);
});

document.addEventListener("keydown", async (event) => {
  if (preferredView !== "text" || surveyDialog.open || !awaitingQuizContinue || !token || event.ctrlKey || event.altKey || event.metaKey) return;
  event.preventDefault();
  awaitingQuizContinue = false;
  commandInput.value = "";
  try {
    const data = await api("/api/command", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({token, command: "continue"}),
    });
    append(data.output);
    awaitingQuizContinue = Boolean(data.awaiting_continue);
    updateProgress(data.progress);
    updateSidePanel(data.side_panel);
    updateScene(data.scene);
    updateInteraction(data.interaction, data.output);
  } catch (err) {
    if (handleSessionError(err)) return;
    awaitingQuizContinue = true;
    append(err.message, "error");
  }
});

async function poll() {
  if (!token) return;
  try {
    const data = await api(`/api/events?token=${encodeURIComponent(token)}`);
    data.messages.forEach((message) => append(message, "social"));
    if (currentScene?.key && data.scene?.key === currentScene.key) {
      currentScene.players = data.scene.players;
      updateScenePlayers(data.scene.players);
    }
  } catch (err) {
    if (handleSessionError(err)) return;
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
