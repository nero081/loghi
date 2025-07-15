const API_KEY = '56dd0eb5ddacfa471fda68c68a550eb1';

const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get('id');
const type = urlParams.get('type');
const title = decodeURIComponent(urlParams.get('title') || '');

document.getElementById('player-title').textContent = title;

function fullscreenPlayer(id) {
  const iframe = document.getElementById(id);
  if (iframe.requestFullscreen) {
    iframe.requestFullscreen();
  } else if (iframe.mozRequestFullScreen) {
    iframe.mozRequestFullScreen();
  } else if (iframe.webkitRequestFullscreen) {
    iframe.webkitRequestFullscreen();
  } else if (iframe.msRequestFullscreen) {
    iframe.msRequestFullscreen();
  }
}

async function fetchDetails() {
  const res = await fetch(`https://api.themoviedb.org/3/${type}/${id}?api_key=${API_KEY}&language=it-IT`);
  return await res.json();
}

async function fetchTVSeasons(tvId) {
  const res = await fetch(`https://api.themoviedb.org/3/tv/${tvId}?api_key=${API_KEY}&language=it-IT`);
  const data = await res.json();
  return data.seasons || [];
}

async function fetchSeasonEpisodes(tvId, seasonNumber) {
  const res = await fetch(`https://api.themoviedb.org/3/tv/${tvId}/season/${seasonNumber}?api_key=${API_KEY}&language=it-IT`);
  const data = await res.json();
  return data.episodes || [];
}

async function playEpisode(tvId, seasonNumber, episodeNumber) {
  const url = `https://vixsrc.to/tv/${tvId}/${seasonNumber}/${episodeNumber}/?primaryColor=ff0000&lang=it`;
  document.getElementById('player-iframe').src = url;
}

async function initPlayer() {
  const details = await fetchDetails();
  document.getElementById('player-overview').textContent = details.overview || 'Nessuna descrizione disponibile.';
  const metaDiv = document.getElementById('player-meta');
  metaDiv.innerHTML = '';

  if (type === 'movie') {
    const year = details.release_date ? new Date(details.release_date).getFullYear() : 'N/A';
    const duration = details.runtime ? `${details.runtime} min` : 'N/A';
    const rating = details.vote_average ? `⭐ ${details.vote_average.toFixed(1)}` : 'N/A';
    metaDiv.innerHTML = `
      <span>🎬 Film</span>
      <span>📅 ${year}</span>
      <span>⏱️ ${duration}</span>
      <span>${rating}</span>
    `;
    document.getElementById('episode-selector').style.display = 'none';
    document.getElementById('player-iframe').src = `https://vixsrc.to/movie/${id}/?primaryColor=ff0000&lang=it`;
  } else {
    const year = details.first_air_date ? new Date(details.first_air_date).getFullYear() : 'N/A';
    const seasons = details.number_of_seasons ? `${details.number_of_seasons} stagioni` : 'N/A';
    const rating = details.vote_average ? `⭐ ${details.vote_average.toFixed(1)}` : 'N/A';
    metaDiv.innerHTML = `
      <span>📺 Serie TV</span>
      <span>📅 ${year}</span>
      <span>🎭 ${seasons}</span>
      <span>${rating}</span>
    `;
    document.getElementById('episode-selector').style.display = 'block';
    await loadTVSeasons(id);
  }
}

async function loadTVSeasons(tvId) {
  const seasons = await fetchTVSeasons(tvId);
  const seasonSelect = document.getElementById('season-select');
  seasonSelect.innerHTML = '';
  const validSeasons = seasons.filter(s => s.season_number > 0);
  validSeasons.forEach(season => {
    const option = document.createElement('option');
    option.value = season.season_number;
    option.textContent = `Stagione ${season.season_number} (${season.episode_count} episodi)`;
    seasonSelect.appendChild(option);
  });

  if (validSeasons.length > 0) {
    await loadSeasonEpisodes(tvId, validSeasons[0].season_number);
    playEpisode(tvId, validSeasons[0].season_number, 1);
  }

  seasonSelect.addEventListener('change', async e => {
    const seasonNumber = parseInt(e.target.value);
    await loadSeasonEpisodes(tvId, seasonNumber);
    playEpisode(tvId, seasonNumber, 1);
  });
}

async function loadSeasonEpisodes(tvId, seasonNumber) {
  const episodes = await fetchSeasonEpisodes(tvId, seasonNumber);
  const episodesList = document.getElementById('episodes-list');
  episodesList.innerHTML = '';
  episodes.forEach(episode => {
    const div = document.createElement('div');
    div.className = 'episode-item';
    div.innerHTML = `
      <div class="episode-number">Episodio ${episode.episode_number}</div>
      <div class="episode-title">${episode.name || `Episodio ${episode.episode_number}`}</div>
    `;
    div.onclick = () => {
      document.querySelectorAll('.episode-item').forEach(el => el.classList.remove('active'));
      div.classList.add('active');
      playEpisode(tvId, seasonNumber, episode.episode_number);
    };
    episodesList.appendChild(div);
  });
  if (episodes.length > 0) {
    episodesList.firstChild.classList.add('active');
  }
}

initPlayer();
