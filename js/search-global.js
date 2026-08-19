// Sistema de búsqueda global inteligente
(function() {
  let searchIndex = [];

  // Cargar el índice de búsqueda
  async function loadSearchIndex() {
    try {
      const response = await fetch('/search-index.json');
      searchIndex = await response.json();
    } catch (err) {
      console.error('Error loading search index:', err);
    }
  }

  // Crear el elemento del buscador
  function createSearchWidget() {
    const searchHTML = `
      <div class="search-widget">
        <input
          type="text"
          id="globalSearch"
          class="search-input"
          placeholder="Buscar en el club..."
          aria-label="Búsqueda global del sitio"
          autocomplete="off"
        >
        <div class="search-results" id="searchResults" style="display: none;">
          <div class="search-results-list"></div>
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
    const searchResults = document.getElementById('searchResults');
    const searchOverlay = document.getElementById('searchOverlay');

    if (!searchInput) return;

    // Búsqueda en tiempo real
    searchInput.addEventListener('input', function(e) {
      const query = this.value.trim();

      if (query.length < 2) {
        searchResults.style.display = 'none';
        searchOverlay.style.display = 'none';
        return;
      }

      performSearch(query, searchResults);
      searchOverlay.style.display = 'block';
    });

    // Cerrar resultados
    searchOverlay.addEventListener('click', function() {
      searchResults.style.display = 'none';
      searchOverlay.style.display = 'none';
      searchInput.value = '';
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        searchResults.style.display = 'none';
        searchOverlay.style.display = 'none';
        searchInput.blur();
      }
    });
  }

  // Realizar búsqueda
  function performSearch(query, resultsContainer) {
    const queryLower = query.toLowerCase();

    // Búsqueda inteligente con puntuación
    const results = searchIndex.map(page => {
      let score = 0;
      const titleLower = page.title.toLowerCase();
      const descLower = page.description.toLowerCase();

      // Palabras clave exactas
      if (titleLower.includes(queryLower)) score += 10;
      if (descLower.includes(queryLower)) score += 5;

      // Palabras individuales
      const queryWords = queryLower.split(/\s+/);
      queryWords.forEach(word => {
        if (word.length > 2) {
          if (titleLower.includes(word)) score += 3;
          if (descLower.includes(word)) score += 1;
        }
      });

      return { ...page, score };
    })
    .filter(page => page.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);

    // Mostrar resultados
    const resultsList = resultsContainer.querySelector('.search-results-list');

    if (results.length === 0) {
      resultsList.innerHTML = '<div class="search-no-results">No se encontraron resultados</div>';
    } else {
      resultsList.innerHTML = results.map(page => `
        <a href="${page.url}" class="search-result-item">
          <div class="search-result-title">${highlightQuery(page.title, query)}</div>
          <div class="search-result-desc">${truncate(page.description, 80)}</div>
        </a>
      `).join('');
    }

    resultsContainer.style.display = 'block';
  }

  // Resaltar la búsqueda en el título
  function highlightQuery(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<strong>$1</strong>');
  }

  // Truncar texto
  function truncate(text, length) {
    return text.length > length ? text.substring(0, length) + '...' : text;
  }

  // Inicializar cuando el DOM esté listo
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
