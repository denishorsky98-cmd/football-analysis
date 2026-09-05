"""
Football Analysis Project - Configuration

Modul: config.py
Popis: Centralizované nastavenia a konfiguracia pre projekt.

Autor: denishorsky98-cmd
Dátum: 2026
"""

# ============================================================================
# CESTY K SÚBOROM
# ============================================================================

# Vstupný CSV súbor s dátami
CSV_FILE = 'SquadLists.csv'

# Výstupné súbory
OUTPUT_IMAGE = 'football_analysis.png'
OUTPUT_STATS = 'stats_output.csv'

# ============================================================================
# ANALÝZA - VŠEOBECNÉ NASTAVENIA
# ============================================================================

# Pozícia ktorú analyzujeme
POSITION_FILTER = 'FW'  # FW = Forward (Útočník)

# Počet prvkov v TOP listinách
TOP_N = 10

# ============================================================================
# GRAFY - VIZUALIZÁCIA
# ============================================================================

# Rozmer obrázka
FIGURE_SIZE = (14, 10)

# Kvalita výstupu (DPI - Dots Per Inch)
DPI_QUALITY = 300

# Počet bins v histograme
HISTOGRAM_BINS = 20

# ============================================================================
# FARBY V GRAFOCH
# ============================================================================

COLOR_TEAMS = 'steelblue'      # Farba grafu tímov
COLOR_HEIGHT = 'green'         # Farba histogramu výšky
COLOR_AVG_LINE = 'red'         # Farba priemerovej čiary
COLOR_SCATTER = 'orange'       # Farba scatter plotu
COLOR_PLAYERS = 'purple'       # Farba grafu hráčov

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = '%(levelname)s - %(message)s'

# ============================================================================
# DÁTOVÉ STĹPCE
# ============================================================================

# Kľúčové stĺpce v CSV súbore
COLUMNS_REQUIRED = {
    'player': 'Player Name',
    'team': 'Team',
    'position': 'Position',
    'height': 'Height (cm)',
    'goals': 'Goals',
    'caps': 'Caps',
}

# ============================================================================
# ŠTATISTIKY - ROUNDING
# ============================================================================

# Počet desatinných miest pri výpise štatistík
DECIMAL_PLACES = 1

# ============================================================================
# MESSAGES
# ============================================================================

MESSAGES = {
    'success_loaded': '✅ Dáta úspešne načítané ({} riadkov)',
    'success_filtered': '📊 Počet užívateľov podľa pozície {}: {}',
    'success_complete': '✅ Analýza úspešne dokončená!',
    'success_graphs': '✅ Grafy uložené ako {}',
    
    'error_file_not_found': '❌ Súbor "{}" neexistuje!',
    'error_empty_file': '❌ Súbor "{}" je prázdny!',
    'error_unexpected': '❌ Neočakávaná chyba: {}',
    
    'info_loading': 'Načítavam dáta z "{}"...',
    'info_filtering': 'Filtrujem dáta podľa pozície {}...',
    'info_stats': 'Štatistiky sa počítajú...',
    'info_graphs': 'Vytváram grafy...',
}
