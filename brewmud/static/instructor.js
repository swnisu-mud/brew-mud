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
  renderSurvey(data.survey);
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
    addCell(row, player.survey_completed ? "Complete" : "Not yet");
    addCell(row, new Date(player.updated_at).toLocaleString());
    body.appendChild(row);
  }
  if (!players.length) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 9;
    cell.className = "empty-row";
    cell.textContent = "No player accounts yet.";
    row.appendChild(cell);
    body.appendChild(row);
  }
  const online = players.filter((player) => player.online).length;
  document.querySelector("#progress-summary").textContent =
    `${players.length} account${players.length === 1 ? "" : "s"}; ${online} online. Updated ${new Date().toLocaleTimeString()}.`;
}

function renderSurvey(survey) {
  document.querySelector("#survey-summary").textContent =
    `${survey.submitted} anonymous response${survey.submitted === 1 ? "" : "s"} submitted.`;
  const withheld = document.querySelector("#survey-withheld");
  const content = document.querySelector("#survey-results-content");
  withheld.hidden = !survey.withheld;
  content.hidden = survey.withheld;
  if (survey.withheld) {
    const remaining = survey.minimum_to_display - survey.submitted;
    withheld.textContent =
      `Results will appear after ${remaining} more response${remaining === 1 ? "" : "s"}.`;
    return;
  }

  const rows = document.querySelector("#survey-result-rows");
  rows.replaceChildren();
  for (const result of survey.questions) {
    const row = document.createElement("tr");
    addCell(row, result.question);
    addCell(row, result.responses);
    addCell(row, result.average === null ? "No answers" : `${result.average} / 10`);
    rows.appendChild(row);
  }

  const comments = document.querySelector("#survey-comments");
  comments.replaceChildren();
  if (!survey.comments.length) {
    const empty = document.createElement("p");
    empty.className = "empty-row";
    empty.textContent = "No optional comments were submitted.";
    comments.appendChild(empty);
  } else {
    for (const text of survey.comments) {
      const comment = document.createElement("blockquote");
      comment.textContent = text;
      comments.appendChild(comment);
    }
  }
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
