const WORLD_ART = {
  lotr: { icon: "✧", index: "01 / MIDDLE-EARTH", note: "Old forests, ancient peoples, and long histories." },
  hp: { icon: "✦", index: "02 / WIZARDING WORLD", note: "A little magic, a little mystery, and curious lives." },
  sw: { icon: "◉", index: "03 / GALAXY FAR AWAY", note: "Across star systems, every life has a story." },
  got: { icon: "♜", index: "04 / WESTEROS", note: "Many houses, many paths, and uncertain fates." },
};

const TARGET_FEATURES = {
  lotr: {
    gender: ["race", "realm", "is_dead", "has_spouse", "hair_group", "birth_age"],
    race: ["gender", "realm", "is_dead", "has_spouse", "hair_group", "birth_age"],
    is_dead: ["gender", "race", "realm", "has_spouse", "hair_group", "birth_age"],
    has_spouse: ["gender", "race", "realm", "is_dead", "hair_group", "birth_age"],
    realm: ["gender", "race", "is_dead", "has_spouse", "hair_group", "birth_age"],
    hair_group: ["gender", "name", "race", "realm", "is_dead", "has_spouse", "birth_age"],
    birth_age: ["gender", "name", "race", "realm", "is_dead", "has_spouse", "hair_group"],
  },
  hp: {
    Gender: ["Species/Race", "Blood", "is_hogwarts", "hogwarts_house", "profession_group", "has_description"],
    "Species/Race": ["Gender", "Blood", "is_hogwarts", "hogwarts_house", "profession_group", "has_description"],
    Blood: ["Gender", "Species/Race", "is_hogwarts", "hogwarts_house", "profession_group", "has_description"],
    hogwarts_house: ["Gender", "Species/Race", "Blood", "profession_group", "has_description"],
    profession_group: ["Gender", "Species/Race", "Blood", "is_hogwarts", "hogwarts_house", "has_description"],
    is_hogwarts: ["Gender", "Species/Race", "Blood", "profession_group", "has_description"],
    has_description: ["Gender", "Species/Race", "Blood", "is_hogwarts", "hogwarts_house", "profession_group"],
  },
  sw: {
    species_group: ["height", "mass", "hair_color", "skin_color", "eye_color", "birth_year", "sex", "gender", "homeworld_group", "film_count", "has_vehicle", "has_starship"],
    gender: ["height", "mass", "hair_color", "skin_color", "eye_color", "birth_year", "species_group", "homeworld_group", "film_count", "has_vehicle", "has_starship"],
    sex: ["height", "mass", "hair_color", "skin_color", "eye_color", "birth_year", "species_group", "homeworld_group", "film_count", "has_vehicle", "has_starship"],
    homeworld_group: ["height", "mass", "hair_color", "skin_color", "eye_color", "birth_year", "sex", "gender", "species_group", "film_count", "has_vehicle", "has_starship"],
    height: ["mass", "hair_color", "skin_color", "eye_color", "birth_year", "sex", "gender", "species_group", "homeworld_group", "film_count", "has_vehicle", "has_starship"],
    mass: ["height", "hair_color", "skin_color", "eye_color", "birth_year", "sex", "gender", "species_group", "homeworld_group", "film_count", "has_vehicle", "has_starship"],
    birth_year: ["height", "mass", "hair_color", "skin_color", "eye_color", "sex", "gender", "species_group", "homeworld_group", "film_count", "has_vehicle", "has_starship"],
  },
  got: {
    isAlive: ["book1", "book2", "book3", "book4", "book5", "numDeadRelations", "boolDeadRelations", "culture", "house", "title"],
    male: ["book1", "book2", "book3", "book4", "book5", "numDeadRelations", "boolDeadRelations", "culture", "house", "title"],
    isNoble: ["book1", "book2", "book3", "book4", "book5", "numDeadRelations", "boolDeadRelations", "culture", "house"],
    isMarried: ["book1", "book2", "book3", "book4", "book5", "numDeadRelations", "boolDeadRelations", "culture", "house", "title"],
    isPopular: ["book1", "book2", "book3", "book4", "book5", "numDeadRelations", "boolDeadRelations", "culture", "house", "title"],
    culture: ["book1", "book2", "book3", "book4", "book5", "numDeadRelations", "boolDeadRelations", "house", "title"],
    house: ["book1", "book2", "book3", "book4", "book5", "numDeadRelations", "boolDeadRelations", "culture", "title"],
    title: ["book1", "book2", "book3", "book4", "book5", "numDeadRelations", "boolDeadRelations", "culture", "house"],
    popularity: ["book1", "book2", "book3", "book4", "book5", "numDeadRelations", "boolDeadRelations", "culture", "house", "title"],
    age: ["book1", "book2", "book3", "book4", "book5", "numDeadRelations", "boolDeadRelations", "culture", "house", "title"],
  },
};

const FIELD_OPTIONS = {
  race: ["Ainur", "Dragons", "Dwarves", "Elves", "Half-elven", "Hobbits", "Men", "Orcs", "Other"],
  gender: ["Female", "Male"],
  realm: ["Arnor", "Arthedain", "Gondor", "Lonely Mountain", "Númenor", "Other", "Rohan", "Shire", "Unknown", "Valinor"],
  hair_group: ["Dark", "Golden", "Grey/White", "Light", "Other", "Unknown"],
  birth_age: ["First Age", "Second Age", "Third Age", "Fourth Age", "Years of the Trees", "Unknown"],
  "Species/Race": ["giant", "goblin", "hag", "human", "muggle", "no-maj", "other", "squib", "vampire", "witch", "wizard"],
  Gender: ["Female", "Male"],
  Blood: ["Half-Blood", "Muggle", "Muggle-Born", "Pure Blood", "Unknown"],
  hogwarts_house: ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin", "No listed house"],
  profession_group: ["Academic/Author", "Healer", "Magical Trade", "Ministry", "Other", "Quidditch", "Unknown"],
  sex: ["female", "hermaphroditic", "male", "none", "unknown"],
  gender_sw: ["feminine", "masculine", "unknown"],
  species_group: ["Droid", "Human", "Other", "Unknown"],
  homeworld_group: ["Alderaan", "Coruscant", "Kamino", "Naboo", "Other", "Tatooine", "Unknown"],
  hair_color: ["auburn", "black", "blond", "brown", "none", "other", "unknown", "white"],
  skin_color: ["blue", "brown", "dark", "fair", "green", "grey", "light", "other", "pale", "unknown", "white"],
  eye_color: ["black", "blue", "brown", "hazel", "orange", "other", "red", "unknown", "yellow"],
  culture: ["Braavosi", "Dornish", "Dornishmen", "Dothraki", "Free Folk", "Free folk", "Ghiscari", "Ironborn", "Ironmen", "Northmen", "Other", "Qartheen", "Reach", "Rivermen", "Stormlands", "Summer Isles", "Tyroshi", "Unknown", "Valemen", "Valyrian", "Westerman", "Westeros"],
  house: ["House Arryn", "House Baratheon", "House Bolton", "House Frey", "House Greyjoy", "House Lannister", "House Martell", "House Stark", "House Targaryen", "House Tully", "House Tyrell", "Night's Watch", "Other", "Unknown"],
  title: ["Archmaester", "Bloodrider", "Grand Maester", "Khal", "King", "King in the North", "Knight", "Lady", "Lord", "Maester", "Other", "Prince", "Princess", "Septon", "Ser", "Unknown"],
};

const FIELD_LABELS = {
  name: "Character name",
  is_dead: "Known to have died", has_spouse: "Has a known spouse", is_hogwarts: "Hogwarts affiliated", has_description: "Has a character description",
  boolDeadRelations: "Has dead relations", numDeadRelations: "Number of dead relations", film_count: "Films appeared in",
  has_vehicle: "Has a vehicle", has_starship: "Has a starship", birth_year: "Birth year", isAlive: "Alive", isNoble: "Noble", isMarried: "Married", isPopular: "Popular",
};
const BINARY_FIELDS = new Set(["is_dead", "has_spouse", "is_hogwarts", "has_description", "boolDeadRelations", "has_vehicle", "has_starship", "book1", "book2", "book3", "book4", "book5"]);
const INTEGER_FIELDS = new Set(["numDeadRelations", "film_count"]);
const TEXT_FIELDS = new Set(["name"]);
const WORLD_THEME = {
  lotr: { color: "#cf754b", soft: "#38221b", icon: "✧" },
  hp: { color: "#d3aa62", soft: "#342919", icon: "✦" },
  sw: { color: "#cf554b", soft: "#351d1c", icon: "◉" },
  got: { color: "#bd4038", soft: "#361b1b", icon: "♜" },
};

const homeView = document.querySelector("#home-view");
const realmView = document.querySelector("#realm-view");
const worldGrid = document.querySelector("#world-grid");
const targetSelect = document.querySelector("#target-select");
const inputGrid = document.querySelector("#input-grid");
const predictButton = document.querySelector("#predict-button");
const formError = document.querySelector("#form-error");
const resultContent = document.querySelector("#result-content");
const connection = document.querySelector(".connection");
let activeWorld = null;
let activeTarget = null;
let musicMuted = false;
let activeTrack = null;
const worldAudio = document.querySelector("#world-audio");
worldAudio.loop = true;
worldAudio.preload = "none";
worldAudio.volume = 0.16;

function updateMusicToggle() {
  const button = document.querySelector("#music-toggle");
  const muted = musicMuted;
  button.setAttribute("aria-pressed", String(muted));
  button.setAttribute("aria-label", muted ? "Unmute background music" : "Mute background music");
  button.title = muted ? "Unmute background music" : "Mute background music";
  document.querySelector("#music-icon").textContent = muted ? "♪̸" : "♫";
  document.querySelector("#music-label").textContent = muted ? "Muted" : "Sound on";
}

function playWorldMusic(world) {
  if (activeTrack !== world) {
    worldAudio.pause();
    worldAudio.currentTime = 0;
    worldAudio.src = `audio/${world}.mp3`;
    activeTrack = world;
  }
  worldAudio.muted = musicMuted;
  worldAudio.play().catch(() => {});
}

function stopWorldMusic() {
  worldAudio.pause();
  worldAudio.currentTime = 0;
  worldAudio.removeAttribute("src");
  worldAudio.load();
  activeTrack = null;
}

function humanize(value) {
  return FIELD_LABELS[value] || value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function setConnection(online) {
  connection.classList.toggle("is-online", online);
  connection.classList.toggle("is-offline", !online);
  document.querySelector("#connection-label").textContent = online ? "Oracle connected" : "Oracle offline";
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail || data);
    throw new Error(detail || `Request failed (${response.status})`);
  }
  return data;
}

function showView(view) {
  const isHome = view === homeView;
  homeView.classList.toggle("is-active", isHome);
  realmView.classList.toggle("is-active", !isHome);
  homeView.setAttribute("aria-hidden", String(!isHome));
  realmView.setAttribute("aria-hidden", String(isHome));
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function createWorldCard(world) {
  const art = WORLD_ART[world.id];
  if (!art) return null;
  const card = document.createElement("button");
  card.className = "world-card";
  card.type = "button";
  card.style.setProperty("--world", WORLD_THEME[world.id].color);
  card.style.setProperty("--world-soft", WORLD_THEME[world.id].soft);
  card.setAttribute("aria-label", `Explore ${world.name}`);
  const [recordNumber, realmName] = art.index.split(" / ");
  card.innerHTML = `<span class="sigil-topline"><span class="world-index">${escapeHtml(recordNumber)}</span><span class="sigil-class">REALM RECORD</span></span><span class="world-symbol" aria-hidden="true">${art.icon}</span><span class="world-card-copy"><span class="world-kicker">${escapeHtml(realmName)}</span><h2>${escapeHtml(world.name)}</h2><span class="world-note">${escapeHtml(art.note)}</span></span><span class="world-card-footer"><span>Open record</span><span class="world-arrow" aria-hidden="true">↗</span></span>`;
  card.addEventListener("click", () => enterWorld(world));
  return card;
}

async function loadWorlds() {
  try {
    const data = await api("/worlds");
    worldGrid.replaceChildren(...data.worlds.map(createWorldCard).filter(Boolean));
    setConnection(true);
  } catch (error) {
    setConnection(false);
    worldGrid.innerHTML = `<p class="form-error">Could not reach the model server. Start FastAPI, then refresh this page.</p>`;
  }
}

async function enterWorld(world) {
  activeWorld = world.id;
  activeTarget = null;
  playWorldMusic(world.id);
  document.body.dataset.world = world.id;
  document.querySelector("#realm-icon").textContent = WORLD_ART[world.id].icon;
  document.querySelector("#realm-title").textContent = world.name;
  document.querySelector("#realm-kicker").textContent = WORLD_ART[world.id].index;
  document.querySelector("#realm-intro").textContent = WORLD_ART[world.id].note;
  document.querySelector("#realm-footer-name").textContent = world.name.toUpperCase();
  document.querySelector("#result-world").textContent = `${world.name.toUpperCase()} · CHARACTER ORACLE`;
  document.querySelector("#result-panel").style.setProperty("--result-color", WORLD_THEME[world.id].color);
  showView(realmView);
  targetSelect.disabled = true;
  targetSelect.innerHTML = "<option>Loading predictions...</option>";
  inputGrid.replaceChildren();
  predictButton.disabled = true;
  setResult("Your answer awaits.", "Choose a prediction and enter the character details to begin.");
  try {
    const data = await api(`/world/${encodeURIComponent(world.id)}/targets`);
    targetSelect.innerHTML = data.targets.map((target) => `<option value="${escapeHtml(target)}">${escapeHtml(humanize(target))}</option>`).join("");
    targetSelect.disabled = false;
    await onTargetChange();
    setConnection(true);
  } catch (error) {
    showError(error.message);
    setConnection(false);
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
}

function optionsFor(field) {
  if (field === "gender" && activeWorld === "sw") return FIELD_OPTIONS.gender_sw;
  return FIELD_OPTIONS[field] || null;
}

function makeInput(field, index) {
  const wrapper = document.createElement("div");
  wrapper.className = "input-field";
  const id = `feature-${index}`;
  const label = document.createElement("label");
  label.className = "field-label";
  label.htmlFor = id;
  label.textContent = humanize(field);
  let input;
  const choices = optionsFor(field);
  if (BINARY_FIELDS.has(field)) {
    input = document.createElement("select");
    input.className = "input-control";
    input.innerHTML = `<option value="0">No / not listed</option><option value="1">Yes</option>`;
  } else if (choices) {
    input = document.createElement("input");
    input.className = "input-control";
    input.setAttribute("list", `${id}-options`);
    input.setAttribute("autocomplete", "off");
    input.placeholder = "Choose or type a value";
    const datalist = document.createElement("datalist");
    datalist.id = `${id}-options`;
    datalist.innerHTML = choices.map((choice) => `<option value="${escapeHtml(choice)}"></option>`).join("");
    wrapper.append(datalist);
  } else if (TEXT_FIELDS.has(field)) {
    input = document.createElement("input");
    input.className = "input-control";
    input.type = "text";
    input.autocomplete = "off";
    input.placeholder = "Enter a character name";
  } else {
    input = document.createElement("input");
    input.className = "input-control";
    input.type = "number";
    input.step = INTEGER_FIELDS.has(field) ? "1" : "any";
    input.min = "0";
  }
  input.id = id;
  input.name = field;
  input.required = true;
  if (input.type === "number") input.value = "0";
  wrapper.append(label, input);
  return wrapper;
}

async function onTargetChange() {
  activeTarget = targetSelect.value;
  formError.hidden = true;
  const fields = TARGET_FEATURES[activeWorld]?.[activeTarget];
  inputGrid.replaceChildren();
  if (!fields) {
    showError(`Input fields are not configured for ${activeTarget}.`);
    predictButton.disabled = true;
    return;
  }
  fields.forEach((field, index) => inputGrid.append(makeInput(field, index)));
  document.querySelector("#feature-count").textContent = `${fields.length} DETAILS`;
  const regression = ["height", "mass", "birth_year", "popularity", "age"].includes(activeTarget);
  document.querySelector("#target-kind").textContent = regression ? "A number will be estimated" : "A category will be predicted";
  predictButton.disabled = false;
}

function showError(message) {
  formError.textContent = message;
  formError.hidden = false;
}

function setResult(title, description) {
  resultContent.innerHTML = `<h2>${escapeHtml(title)}</h2><p>${escapeHtml(description)}</p>`;
}

async function predict() {
  if (!activeWorld || !activeTarget) return;
  formError.hidden = true;
  const inputs = [...inputGrid.querySelectorAll("input, select")];
  const features = {};
  for (const input of inputs) {
    if (!input.reportValidity()) return;
    features[input.name] = input.type === "number" || input.tagName === "SELECT" && BINARY_FIELDS.has(input.name)
      ? Number(input.value)
      : input.value;
  }
  predictButton.disabled = true;
  predictButton.querySelector("span").textContent = "Reading the signs...";
  resultContent.classList.remove("result-content");
  void resultContent.offsetWidth;
  resultContent.classList.add("result-content");
  setResult("The answer is forming…", "The model is weighing the details.");
  try {
    const data = await api("/predict", {
      method: "POST",
      body: JSON.stringify({ world: activeWorld, target: activeTarget, input_features: features }),
    });
    const value = document.createElement("div");
    value.className = `result-value${typeof data.prediction === "number" ? " is-number" : ""}`;
    value.textContent = typeof data.prediction === "number" ? formatNumber(data.prediction) : String(data.prediction);
    resultContent.replaceChildren(value);
    setConnection(true);
  } catch (error) {
    showError(error.message);
    setResult("The answer is unclear.", "Check the entered details and try again.");
    setConnection(false);
  } finally {
    predictButton.disabled = false;
    predictButton.querySelector("span").textContent = "Reveal prediction";
  }
}

function formatNumber(value) {
  return Number.isInteger(value) ? String(value) : Number(value).toFixed(2).replace(/0+$/, "").replace(/\.$/, "");
}

document.querySelector("#back-button").addEventListener("click", () => {
  stopWorldMusic();
  activeWorld = null;
  document.body.removeAttribute("data-world");
  showView(homeView);
});
document.querySelector("#music-toggle").addEventListener("click", () => {
  musicMuted = !musicMuted;
  worldAudio.muted = musicMuted;
  updateMusicToggle();
  if (!musicMuted && activeWorld) playWorldMusic(activeWorld);
});
targetSelect.addEventListener("change", onTargetChange);
predictButton.addEventListener("click", predict);
updateMusicToggle();
loadWorlds();
