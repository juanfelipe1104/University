const API_URL = "https://pokeapi.co/api/v2/pokemon?limit=9&offset=0";
const FALLBACK_IMAGE =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 160 160'%3E%3Ccircle cx='80' cy='80' r='60' fill='%23e7edf6'/%3E%3Cpath d='M20 80h120M80 20a60 60 0 0 1 60 60H20a60 60 0 0 1 60-60Z' fill='%23df5252' stroke='%23364760' stroke-width='7'/%3E%3Ccircle cx='80' cy='80' r='17' fill='white' stroke='%23364760' stroke-width='7'/%3E%3C/svg%3E";

const grid = document.querySelector("#pokemon-grid");
const statusElement = document.querySelector("#status");
const retryButton = document.querySelector("#retry-button");
const cardTemplate = document.querySelector("#pokemon-card-template");
const dialog = document.querySelector("#pokemon-dialog");
const closeDialogButton = document.querySelector("#close-dialog");
const dialogLoading = document.querySelector("#dialog-loading");
const detail = document.querySelector("#pokemon-detail");

const detailElements = {
  number: document.querySelector("#dialog-number"),
  image: document.querySelector("#dialog-image"),
  name: document.querySelector("#dialog-name"),
  types: document.querySelector("#dialog-types"),
  height: document.querySelector("#dialog-height"),
  weight: document.querySelector("#dialog-weight"),
  stats: document.querySelector("#dialog-stats"),
};

const detailsCache = new Map();
let detailRequestController;

function formatNumber(number) {
  return `#${String(number).padStart(3, "0")}`;
}

function getPokemonId(url) {
  const segments = new URL(url).pathname.split("/").filter(Boolean);
  return Number(segments.at(-1));
}

function getArtwork(pokemon) {
  return (
    pokemon.sprites.other?.["official-artwork"]?.front_default ??
    pokemon.sprites.front_default ??
    FALLBACK_IMAGE
  );
}

async function fetchJson(url, options) {
  const response = await fetch(url, options);

  if (!response.ok) {
    throw new Error(`La API ha respondido con el estado ${response.status}.`);
  }

  return response.json();
}

function renderCards(pokemonList) {
  grid.replaceChildren();

  for (const pokemon of pokemonList) {
    const id = getPokemonId(pokemon.url);
    const card = cardTemplate.content.firstElementChild.cloneNode(true);
    const image = card.querySelector(".card-image");

    card.dataset.url = pokemon.url;
    card.querySelector(".card-number").textContent = formatNumber(id);
    card.querySelector(".card-name").textContent = pokemon.name;
    image.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${id}.png`;
    image.alt = pokemon.name;
    image.addEventListener("error", () => {
      image.src = FALLBACK_IMAGE;
    }, { once: true });

    grid.append(card);
  }
}

async function loadPokemon() {
  statusElement.hidden = false;
  statusElement.textContent = "Cargando Pokémon…";
  retryButton.hidden = true;
  grid.replaceChildren();

  try {
    const data = await fetchJson(API_URL);
    renderCards(data.results);
    statusElement.hidden = true;
  } catch (error) {
    console.error(error);
    statusElement.textContent =
      "No se pudo conectar con PokéAPI. Comprueba la conexión e inténtalo de nuevo.";
    retryButton.hidden = false;
  }
}

function renderDetails(pokemon) {
  detailElements.number.textContent = formatNumber(pokemon.id);
  detailElements.name.textContent = pokemon.name;
  detailElements.image.src = getArtwork(pokemon);
  detailElements.image.alt = pokemon.name;
  detailElements.height.textContent = `${(pokemon.height / 10).toLocaleString("es-ES")} m`;
  detailElements.weight.textContent = `${(pokemon.weight / 10).toLocaleString("es-ES")} kg`;

  detailElements.types.replaceChildren();
  for (const entry of pokemon.types) {
    const badge = document.createElement("span");
    badge.className = "type-badge";
    badge.textContent = entry.type.name;
    detailElements.types.append(badge);
  }

  detailElements.stats.replaceChildren();
  for (const entry of pokemon.stats) {
    const row = document.createElement("div");
    const percentage = Math.min(100, (entry.base_stat / 180) * 100);

    row.className = "stat-row";
    row.innerHTML = `
      <span class="stat-name"></span>
      <span class="stat-value"></span>
      <span class="stat-bar" aria-hidden="true"><span></span></span>
    `;
    row.querySelector(".stat-name").textContent = entry.stat.name.replace("-", " ");
    row.querySelector(".stat-value").textContent = entry.base_stat;
    row.querySelector(".stat-bar span").style.width = `${percentage}%`;
    detailElements.stats.append(row);
  }

  dialogLoading.hidden = true;
  detail.hidden = false;
}

async function openPokemon(url) {
  detailRequestController?.abort();
  detailRequestController = new AbortController();

  dialogLoading.hidden = false;
  dialogLoading.textContent = "Cargando detalles…";
  detail.hidden = true;
  dialog.showModal();

  try {
    const pokemon = detailsCache.get(url) ?? await fetchJson(url, {
      signal: detailRequestController.signal,
    });
    detailsCache.set(url, pokemon);
    renderDetails(pokemon);
  } catch (error) {
    if (error.name === "AbortError") return;

    console.error(error);
    dialogLoading.textContent = "No se pudieron cargar los detalles de este Pokémon.";
  }
}

grid.addEventListener("click", (event) => {
  const card = event.target.closest(".pokemon-card");
  if (card) openPokemon(card.dataset.url);
});

retryButton.addEventListener("click", loadPokemon);
closeDialogButton.addEventListener("click", () => dialog.close());

dialog.addEventListener("close", () => detailRequestController?.abort());
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});

loadPokemon();
