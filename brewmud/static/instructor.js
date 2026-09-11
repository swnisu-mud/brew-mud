let instructorPassword = "";
let refreshTimer = null;

async function loadProgress() {
  const response = await fetch("/api/instructor/progress", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({password: instructorPassword}),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Could not load progress");
  renderProgress(data.players);
}

function addCell(row, value) {
  const cell = document.createElement("td");
  cell.textContent = value;
  row.appendChild(cell);
}

function renderProgress(players) {
  const body = document.querySelector("#progress-rows");
  body.replaceChildren();
  for (const player of players) {
    const row = document.createElement("tr");
    if (player.online) row.classList.add("online");
    addCell(row, player.name);
    addCell(row, player.rank);
    addCell(row, player.insight);
    addCell(row, `${player.locations}/${player.locations_total}`);
    addCell(row, `${player.quests}/${player.quests_total}`);
    addCell(row, `${player.knowledge_checks}/${player.knowledge_checks_total}`);
    addCell(row, player.next_rank);
    addCell(row, new Date(player.updated_at).toLocaleString());
    body.appendChild(row);
  }
  if (!players.length) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 8;
    cell.className = "empty-row";
    cell.textContent = "No player accounts yet.";
    row.appendChild(cell);
    body.appendChild(row);
  }
  const online = players.filter((player) => player.online).length;
  document.querySelector("#progress-summary").textContent =
    `${players.length} account${players.length === 1 ? "" : "s"}; ${online} online. Updated ${new Date().toLocaleTimeString()}.`;
}

async function refreshProgress() {
  const error = document.querySelector("#instructor-error");
  error.textContent = "";
  try {
    await loadProgress();
  } catch (err) {
    error.textContent = err.message;
  }
}

document.querySelector("#instructor-login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  instructorPassword = document.querySelector("#instructor-password").value;
  try {
    await loadProgress();
    document.querySelector("#instructor-login").hidden = true;
    document.querySelector("#progress-panel").hidden = false;
    refreshTimer = window.setInterval(refreshProgress, 30000);
  } catch (err) {
    document.querySelector("#instructor-error").textContent = err.message;
  }
});

document.querySelector("#refresh-progress").addEventListener("click", refreshProgress);
window.addEventListener("pagehide", () => window.clearInterval(refreshTimer));
