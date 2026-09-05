"""
Football Analysis Project - Analýza futbalovej štatistiky

Modul: analysis.py
Popis: Analýza dát o útočníkoch (FW) vrátane štatistiky, výšky, gólov a skúsenosti.

Autor: denishorsky98-cmd
Dátum: 2026
"""

import os
import sys
import logging
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================================
# KONFIGURÁCIA
# ============================================================================

# Názov vstupného súboru
CSV_FILE = 'SquadLists.csv'

# Názov výstupného grafu
OUTPUT_IMAGE = 'football_analysis.png'

# Počet prvkov v TOP listinách
TOP_N = 10

# Počet bins v histograme
HISTOGRAM_BINS = 20

# Veľkosť obrázka
FIGURE_SIZE = (14, 10)

# DPI kvality
DPI_QUALITY = 300

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# FUNKCIE
# ============================================================================

def load_data(filepath: str) -> pd.DataFrame:
    """
    Načíta dáta z CSV súboru s error handlingom.
    
    Args:
        filepath (str): Cesta k CSV súboru
        
    Returns:
        pd.DataFrame: Načítané dáta
        
    Raises:
        FileNotFoundError: Ak súbor neexistuje
        pd.errors.EmptyDataError: Ak je súbor prázdny
    """
    logger.info(f"Načítavam dáta z '{filepath}'...")
    
    if not os.path.exists(filepath):
        logger.error(f"❌ Súbor '{filepath}' neexistuje!")
        raise FileNotFoundError(f"Súbor '{filepath}' nebol nájdený.")
    
    try:
        df = pd.read_csv(filepath)
        logger.info(f"✅ Dáta úspešne načítané ({len(df)} riadkov)")
        return df
    except pd.errors.EmptyDataError:
        logger.error(f"❌ Súbor '{filepath}' je prázdny!")
        raise
    except Exception as e:
        logger.error(f"❌ Chyba pri načítaní dát: {e}")
        raise


def filter_forwards(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtruje iba útočníkov (FW) z datasetu.
    
    Args:
        df (pd.DataFrame): Pôvodný dataset
        
    Returns:
        pd.DataFrame: Dataset s útočníkmi
    """
    forwards = df[df['Position'] == 'FW'].copy()
    logger.info(f"Počet útočníkov (FW): {len(forwards)}")
    return forwards


def calculate_statistics(forwards: pd.DataFrame) -> dict:
    """
    Vypočíta základné štatistiky o útočníkoch.
    
    Args:
        forwards (pd.DataFrame): Dataset s útočníkmi
        
    Returns:
        dict: Slovník s štatistikami
    """
    stats = {
        'total_forwards': len(forwards),
        'avg_height': forwards['Height (cm)'].mean(),
        'avg_goals': forwards['Goals'].mean(),
        'avg_caps': forwards['Caps'].mean(),
        'top_teams': forwards.groupby('Team')['Goals'].sum().nlargest(TOP_N),
        'top_players': forwards.nlargest(TOP_N, 'Goals')[['Player Name', 'Goals']],
    }
    
    logger.info(f"Štatistiky vypočítané")
    return stats


def print_statistics(stats: dict) -> None:
    """
    Vypíše štatistiky v peknom formáte.
    
    Args:
        stats (dict): Slovník so štatistikami
    """
    print("\n" + "=" * 60)
    print("⚽ FOOTBALL ANALYSIS - ÚTOČNÍCI (FW)")
    print("=" * 60)
    print(f"\n📊 Celkový počet útočníkov: {stats['total_forwards']}")
    print(f"📏 Priemerná výška: {stats['avg_height']:.1f} cm")
    print(f"⚽ Priemer gólov na hráča: {stats['avg_goals']:.1f}")
    print(f"🎮 Priemer Caps na hráča: {stats['avg_caps']:.1f}")
    print("\n" + "=" * 60)
    print(f"TOP {TOP_N} TÍMOV PODĽA GÓLOV:")
    print("=" * 60)
    print(stats['top_teams'])
    print("\n" + "=" * 60)
    print(f"TOP {TOP_N} HRÁČOV PODĽA GÓLOV:")
    print("=" * 60)
    print(stats['top_players'].to_string())
    print("=" * 60 + "\n")


def create_visualizations(forwards: pd.DataFrame, stats: dict, output_file: str) -> None:
    """
    Vytvorí 4 grafy a uloží ich do PNG súboru.
    
    Args:
        forwards (pd.DataFrame): Dataset s útočníkmi
        stats (dict): Slovník so štatistikami
        output_file (str): Cesta k výstupnému súboru
    """
    logger.info("Vytváram grafy...")
    
    fig, axes = plt.subplots(2, 2, figsize=FIGURE_SIZE)
    
    # ========================================================================
    # GRAF 1: TOP 10 TÍMOV
    # ========================================================================
    stats['top_teams'].plot(kind='bar', ax=axes[0, 0], color='steelblue')
    axes[0, 0].set_title(f'TOP {TOP_N} Tímov podľa Gólov', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Tím')
    axes[0, 0].set_ylabel('Počet Gólov')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # ========================================================================
    # GRAF 2: DISTRIBÚCIA VÝŠKY
    # ========================================================================
    height_data = forwards['Height (cm)'].dropna()
    axes[0, 1].hist(height_data, bins=HISTOGRAM_BINS, color='green', alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Distribúcia Výšky Útočníkov', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Výška (cm)')
    axes[0, 1].set_ylabel('Počet Hráčov')
    
    # Priamka pre priemer
    avg_height = stats['avg_height']
    axes[0, 1].axvline(avg_height, color='red', linestyle='--', linewidth=2, 
                       label=f'Priemer: {avg_height:.1f}cm')
    axes[0, 1].legend()
    
    # ========================================================================
    # GRAF 3: GÓLY vs. SKÚSENOSŤ (CAPS)
    # ========================================================================
    axes[1, 0].scatter(forwards['Caps'], forwards['Goals'], alpha=0.6, color='orange', s=50)
    axes[1, 0].set_title('Góly vs. Skúsenosť (Caps)', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Caps (Počet Zápasov)')
    axes[1, 0].set_ylabel('Góly')
    axes[1, 0].grid(True, alpha=0.3)
    
    # ========================================================================
    # GRAF 4: TOP 10 HRÁČOV
    # ========================================================================
    top_players = stats['top_players'].set_index('Player Name')
    top_players.plot(kind='barh', ax=axes[1, 1], color='purple', legend=False)
    axes[1, 1].set_title(f'TOP {TOP_N} Hráčov podľa Gólov', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Počet Gólov')
    
    # ========================================================================
    # ULOŽENIE OBRÁZKA
    # ========================================================================
    plt.tight_layout()
    plt.savefig(output_file, dpi=DPI_QUALITY, bbox_inches='tight')
    logger.info(f"✅ Grafy uložené ako '{output_file}'")
    plt.show()


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    """
    Hlavná funkcia - orchestruje celý workflow.
    """
    try:
        # Krok 1: Načítaj dáta
        df = load_data(CSV_FILE)
        
        # Krok 2: Filtruj útočníkov
        forwards = filter_forwards(df)
        
        # Krok 3: Vypočítaj štatistiky
        stats = calculate_statistics(forwards)
        
        # Krok 4: Vypíš štatistiky
        print_statistics(stats)
        
        # Krok 5: Vytvor grafy
        create_visualizations(forwards, stats, OUTPUT_IMAGE)
        
        logger.info("✅ Analýza úspešne dokončená!")
        
    except FileNotFoundError as e:
        logger.error(f"Chyba: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Neočakávaná chyba: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
