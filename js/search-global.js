// Sistema de búsqueda global inteligente 10/10
(function() {
  let searchIndex = [];
  let recentSearches = [];
  const MAX_RESULTS = 10;
  const RECENT_SEARCHES_KEY = 'cbgb_recent_searches';
  let currentSelectedIndex = -1;

  // Cargar searches recientes del localStorage
  function loadRecentSearches() {
    try {
      const stored = localStorage.getItem(RECENT_SEARCHES_KEY);
      recentSearches = stored ? JSON.parse(stored) : [];
    } catch (e) {
      recentSearches = [];
    }
  }

  // Guardar searches recientes
  function saveRecentSearches() {
    try {
      localStorage.setItem(RECENT_SEARCHES_KEY, JSON.stringify(recentSearches.slice(0, 5)));
    } catch (e) {
      // Ignorar si localStorage no está disponible
    }
  }

  // Algoritmo de búsqueda fuzzy (tolerancia a errores de tipeo)
  function fuzzyMatch(str, pattern) {
    const patternLower = pattern.toLowerCase();
    const strLower = str.toLowerCase();

    if (strLower.includes(patternLower)) return true;

    let patternIdx = 0;
    for (let i = 0; i < strLower.length && patternIdx < patternLower.length; i++) {
      if (strLower[i] === patternLower[patternIdx]) {
        patternIdx++;
      }
    }
    return patternIdx === patternLower.length;
  }

  // Cargar el índice de búsqueda
  async function loadSearchIndex() {
    try {
      const response = await fetch('/search-index.json');
      searchIndex = await response.json();
      loadRecentSearches();
    } catch (err) {
      console.error('Error loading search index:', err);
    }
  }

  // Crear el widget del buscador
  function createSearchWidget() {
    const searchHTML = `
      <div class="search-widget" role="search">
        <svg class="search-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
        </svg>
        <input
          type="text"
          id="globalSearch"
          class="search-input"
          placeholder="Buscar club, blog, eventos..."
          aria-label="Búsqueda global del sitio"
          autocomplete="off"
        >
        <div class="search-panel" id="searchPanel" style="display: none;">
          <div class="search-content">
            <div class="search-results" id="searchResults" style="display: none;">
              <div class="search-results-list"></div>
            </div>
            <div class="search-recent" id="searchRecent" style="display: none;">
              <div class="search-recent-title">Búsquedas recientes</div>
              <div class="search-recent-list"></div>
            </div>
            <div class="search-suggestions" id="searchSuggestions" style="display: none;">
              <div class="search-suggestions-title">Categorías populares</div>
              <div class="search-suggestions-list"></div>
            </div>
          </div>
        </div>
        <div class="search-overlay" id="searchOverlay" style="display: none;"></div>
      </div>
    `;

    // Insertar en el header
    const header = document.querySelector('header');
    if (header) {
      const nav = header.querySelector('.head-nav');
      if (nav) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = searchHTML;
        nav.parentNode.insertBefore(tempDiv.firstElementChild, nav.nextSibling);
      }
    }

    // Vincular eventos
    const searchInput = document.getElementById('globalSearch');
    const searchPanel = document.getElementById('searchPanel');
    const searchOverlay = document.getElementById('searchOverlay');

    if (!searchInput) return;

    // Mostrar sugerencias al hacer focus
    searchInput.addEventListener('focus', function() {
      if (this.value.length === 0) {
        showSuggestions();
        showRecentSearches();
        searchPanel.style.display = 'block';
        searchOverlay.style.display = 'block';
      }
    });

    // Búsqueda en tiempo real con debounce
    let searchTimeout;
    searchInput.addEventListener('input', function(e) {
      clearTimeout(searchTimeout);
      const query = this.value.trim();

      if (query.length < 2) {
        if (query.length === 0) {
          showSuggestions();
          showRecentSearches();
          document.getElementById('searchResults').style.display = 'none';
        } else {
          document.getElementById('searchRecent').style.display = 'none';
          document.getElementById('searchSuggestions').style.display = 'none';
        }
        return;
      }

      searchTimeout = setTimeout(() => {
        performSearch(query);
      }, 150);
    });

    // Navegación con teclado
    searchInput.addEventListener('keydown', function(e) {
      const resultsList = document.querySelectorAll('.search-result-item');

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        currentSelectedIndex = Math.min(currentSelectedIndex + 1, resultsList.length - 1);
        updateSelectedResult(resultsList);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        currentSelectedIndex = Math.max(currentSelectedIndex - 1, -1);
        updateSelectedResult(resultsList);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (currentSelectedIndex >= 0 && resultsList[currentSelectedIndex]) {
          resultsList[currentSelectedIndex].click();
        } else if (this.value.trim()) {
          const firstResult = document.querySelector('.search-result-item');
          if (firstResult) firstResult.click();
        }
      } else if (e.key === 'Escape') {
        closeSearch();
      }
    });

    // Cerrar búsqueda
    searchOverlay.addEventListener('click', closeSearch);
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        closeSearch();
      }
    });

    // Atajo global: Ctrl+K o Cmd+K
    document.addEventListener('keydown', function(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        searchInput.focus();
      }
    });

    function closeSearch() {
      searchPanel.style.display = 'none';
      searchOverlay.style.display = 'none';
      searchInput.blur();
      currentSelectedIndex = -1;
    }
  }

  // Mostrar sugerencias de categorías
  function showSuggestions() {
    const categories = [
      { name: 'Blog', icon: '📝' },
      { name: 'Partits', icon: '🏀' },
      { name: 'Campus', icon: '🎓' },
      { name: '3x3', icon: '🏆' },
      { name: 'Escoleta', icon: '👶' },
      { name: 'Femení', icon: '👩‍🤝‍👩' }
    ];

    const suggestionsContainer = document.getElementById('searchSuggestions');
    const suggestionsList = suggestionsContainer.querySelector('.search-suggestions-list');

    suggestionsList.innerHTML = categories.map(cat => `
      <button class="search-suggestion-item" data-query="${cat.name}">
        <span class="suggestion-icon">${cat.icon}</span>
        <span>${cat.name}</span>
      </button>
    `).join('');

    // Vincular eventos a sugerencias
    suggestionsContainer.querySelectorAll('.search-suggestion-item').forEach(btn => {
      btn.addEventListener('click', () => {
        const query = btn.getAttribute('data-query');
        document.getElementById('globalSearch').value = query;
        document.getElementById('globalSearch').dispatchEvent(new Event('input'));
      });
    });

    suggestionsContainer.style.display = 'block';
  }

  // Mostrar búsquedas recientes
  function showRecentSearches() {
    const recentContainer = document.getElementById('searchRecent');
    const recentList = recentContainer.querySelector('.search-recent-list');

    if (recentSearches.length === 0) {
      recentContainer.style.display = 'none';
      return;
    }

    recentList.innerHTML = recentSearches.map(search => `
      <button class="search-recent-item" data-query="${search}">
        <span class="recent-icon">🕐</span>
        <span>${search}</span>
      </button>
    `).join('');

    recentContainer.querySelectorAll('.search-recent-item').forEach(btn => {
      btn.addEventListener('click', () => {
        const query = btn.getAttribute('data-query');
        document.getElementById('globalSearch').value = query;
        document.getElementById('globalSearch').dispatchEvent(new Event('input'));
      });
    });

    recentContainer.style.display = 'block';
  }

  // Realizar búsqueda inteligente
  function performSearch(query) {
    const queryLower = query.toLowerCase();
    const queryWords = queryLower.split(/\s+/);

    // Agregar a búsquedas recientes
    if (!recentSearches.includes(query)) {
      recentSearches.unshift(query);
      recentSearches = recentSearches.slice(0, 5);
      saveRecentSearches();
    }

    // Búsqueda con puntuación inteligente
    const results = searchIndex.map(page => {
      let score = 0;
      const titleLower = page.title.toLowerCase();
      const descLower = page.description.toLowerCase();

      // Búsqueda exacta en título (puntuación más alta)
      if (titleLower.includes(queryLower)) score += 15;

      // Búsqueda exacta en descripción
      if (descLower.includes(queryLower)) score += 8;

      // Búsqueda fuzzy en título (tolerancia a errores)
      if (fuzzyMatch(page.title, query)) score += 5;

      // Palabras individuales
      queryWords.forEach(word => {
        if (word.length > 2) {
          if (titleLower.includes(word)) score += 4;
          if (descLower.includes(word)) score += 2;
        }
      });

      // Bonus por URL coincidencia
      if (page.url.includes(queryLower)) score += 3;

      return { ...page, score };
    })
    .filter(page => page.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, MAX_RESULTS);

    // Mostrar resultados
    const resultsContainer = document.getElementById('searchResults');
    const resultsList = resultsContainer.querySelector('.search-results-list');

    // Ocultar sugerencias
    document.getElementById('searchSuggestions').style.display = 'none';
    document.getElementById('searchRecent').style.display = 'none';

    if (results.length === 0) {
      resultsList.innerHTML = '<div class="search-no-results">No se encontraron resultados para "<strong>' + escapeHtml(query) + '</strong>"</div>';
    } else {
      resultsList.innerHTML = results.map((page, idx) => `
        <a href="${page.url}" class="search-result-item" data-index="${idx}" role="option">
          <div class="search-result-title">${highlightQuery(page.title, query)}</div>
          <div class="search-result-desc">${truncate(page.description, 85)}</div>
          <div class="search-result-url">${page.url}</div>
        </a>
      `).join('');

      currentSelectedIndex = -1;
    }

    resultsContainer.style.display = 'block';
  }

  // Actualizar resultado seleccionado
  function updateSelectedResult(resultsList) {
    resultsList.forEach((item, idx) => {
      if (idx === currentSelectedIndex) {
        item.classList.add('selected');
        item.setAttribute('aria-selected', 'true');
        item.scrollIntoView({ block: 'nearest' });
      } else {
        item.classList.remove('selected');
        item.setAttribute('aria-selected', 'false');
      }
    });
  }

  // Resaltar la búsqueda en el título
  function highlightQuery(text, query) {
    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }

  // Truncar texto
  function truncate(text, length) {
    return text.length > length ? text.substring(0, length) + '…' : text;
  }

  // Escapar HTML
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Inicializar
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      loadSearchIndex();
      createSearchWidget();
    });
  } else {
    loadSearchIndex();
    createSearchWidget();
  }
})();
