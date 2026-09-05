"""
Football Analysis Project - Main Analysis Module

Modul: analysis.py (refaktorovaná verzia s použitím config.py)
Popis: Analýza dát o futbalových útočníkoch podľa pozícií.

Autor: denishorsky98-cmd
Dátum: 2026
"""

import os
import sys
import logging
import pandas as pd
import matplotlib.pyplot as plt

# Import konfigurácie
try:
    import config
except ImportError:
    print("❌ Chyba: Súbor 'config.py' nebol nájdený!")
    sys.exit(1)

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
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
    logger.info(config.MESSAGES['info_loading'].format(filepath))
    
    if not os.path.exists(filepath):
        error_msg = config.MESSAGES['error_file_not_found'].format(filepath)
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    try:
        df = pd.read_csv(filepath)
        success_msg = config.MESSAGES['success_loaded'].format(len(df))
        logger.info(success_msg)
        return df
    except pd.errors.EmptyDataError:
        error_msg = config.MESSAGES['error_empty_file'].format(filepath)
        logger.error(error_msg)
        raise
    except Exception as e:
        error_msg = config.MESSAGES['error_unexpected'].format(e)
        logger.error(error_msg)
        raise


def filter_by_position(df: pd.DataFrame, position: str) -> pd.DataFrame:
    """
    Filtruje hráčov podľa pozície.
    
    Args:
        df (pd.DataFrame): Pôvodný dataset
        position (str): Pozícia (FW, MF, DF, GK)
        
    Returns:
        pd.DataFrame: Filtrovaný dataset
    """
    logger.info(config.MESSAGES['info_filtering'].format(position))
    
    filtered = df[df[config.COLUMNS_REQUIRED['position']] == position].copy()
    success_msg = config.MESSAGES['success_filtered'].format(position, len(filtered))
    logger.info(success_msg)
    
    return filtered


def calculate_statistics(players: pd.DataFrame) -> dict:
    """
    Vypočíta základné štatistiky o hráčoch.
    
    Args:
        players (pd.DataFrame): Dataset s hráčmi
        
    Returns:
        dict: Slovník so štatistikami
    """
    logger.info(config.MESSAGES['info_stats'])
    
    height_col = config.COLUMNS_REQUIRED['height']
    goals_col = config.COLUMNS_REQUIRED['goals']
    caps_col = config.COLUMNS_REQUIRED['caps']
    team_col = config.COLUMNS_REQUIRED['team']
    player_col = config.COLUMNS_REQUIRED['player']
    
    stats = {
        'total': len(players),
        'avg_height': players[height_col].mean(),
        'avg_goals': players[goals_col].mean(),
        'avg_caps': players[caps_col].mean(),
        'top_teams': players.groupby(team_col)[goals_col].sum().nlargest(config.TOP_N),
        'top_players': players.nlargest(config.TOP_N, goals_col)[[player_col, goals_col]],
    }
    
    return stats


def print_statistics(stats: dict, position: str) -> None:
    """
    Vypíše štatistiky v peknom formáte.
    
    Args:
        stats (dict): Slovník so štatistikami
        position (str): Pozícia (FW, MF, DF, GK)
    """
    dp = config.DECIMAL_PLACES
    
    print("\n" + "=" * 70)
    print(f"⚽ FOOTBALL ANALYSIS - POZÍCIA: {position}")
    print("=" * 70)
    print(f"\n📊 Celkový počet hráčov: {stats['total']}")
    print(f"📏 Priemerná výška: {stats['avg_height']:.{dp}f} cm")
    print(f"⚽ Priemer gólov na hráča: {stats['avg_goals']:.{dp}f}")
    print(f"🎮 Priemer Caps na hráča: {stats['avg_caps']:.{dp}f}")
    
    print("\n" + "=" * 70)
    print(f"TOP {config.TOP_N} TÍMOV PODĽA GÓLOV:")
    print("=" * 70)
    print(stats['top_teams'])
    
    print("\n" + "=" * 70)
    print(f"TOP {config.TOP_N} HRÁČOV PODĽA GÓLOV:")
    print("=" * 70)
    print(stats['top_players'].to_string(index=False))
    print("=" * 70 + "\n")


def create_visualizations(players: pd.DataFrame, stats: dict, 
                         output_file: str, position: str) -> None:
    """
    Vytvorí 4 grafy a uloží ich do PNG súboru.
    
    Args:
        players (pd.DataFrame): Dataset s hráčmi
        stats (dict): Slovník so štatistikami
        output_file (str): Cesta k výstupnému súboru
        position (str): Pozícia (FW, MF, DF, GK)
    """
    logger.info(config.MESSAGES['info_graphs'])
    
    height_col = config.COLUMNS_REQUIRED['height']
    goals_col = config.COLUMNS_REQUIRED['goals']
    caps_col = config.COLUMNS_REQUIRED['caps']
    
    fig, axes = plt.subplots(2, 2, figsize=config.FIGURE_SIZE)
    fig.suptitle(f'Football Analysis - Pozícia: {position}', fontsize=16, fontweight='bold')
    
    # ========================================================================
    # GRAF 1: TOP TÍMOV
    # ========================================================================
    stats['top_teams'].plot(kind='bar', ax=axes[0, 0], color=config.COLOR_TEAMS)
    axes[0, 0].set_title(f'TOP {config.TOP_N} Tímov podľa Gólov', 
                         fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Tím')
    axes[0, 0].set_ylabel('Počet Gólov')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    # ========================================================================
    # GRAF 2: DISTRIBÚCIA VÝŠKY
    # ========================================================================
    height_data = players[height_col].dropna()
    axes[0, 1].hist(height_data, bins=config.HISTOGRAM_BINS, 
                    color=config.COLOR_HEIGHT, alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Distribúcia Výšky', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Výška (cm)')
    axes[0, 1].set_ylabel('Počet Hráčov')
    
    # Priamka pre priemer
    avg_height = stats['avg_height']
    axes[0, 1].axvline(avg_height, color=config.COLOR_AVG_LINE, linestyle='--', 
                       linewidth=2, label=f'Priemer: {avg_height:.{config.DECIMAL_PLACES}f}cm')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # ========================================================================
    # GRAF 3: GÓLY vs. SKÚSENOSŤ (CAPS)
    # ========================================================================
    axes[1, 0].scatter(players[caps_col], players[goals_col], 
                      alpha=0.6, color=config.COLOR_SCATTER, s=50)
    axes[1, 0].set_title('Góly vs. Skúsenosť (Caps)', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Caps (Počet Zápasov)')
    axes[1, 0].set_ylabel('Góly')
    axes[1, 0].grid(True, alpha=0.3)
    
    # ========================================================================
    # GRAF 4: TOP HRÁČOV
    # ========================================================================
    top_players = stats['top_players'].set_index(config.COLUMNS_REQUIRED['player'])
    top_players.plot(kind='barh', ax=axes[1, 1], color=config.COLOR_PLAYERS, legend=False)
    axes[1, 1].set_title(f'TOP {config.TOP_N} Hráčov podľa Gólov', 
                         fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Počet Gólov')
    axes[1, 1].grid(True, alpha=0.3, axis='x')
    
    # ========================================================================
    # ULOŽENIE OBRÁZKA
    # ========================================================================
    plt.tight_layout()
    plt.savefig(output_file, dpi=config.DPI_QUALITY, bbox_inches='tight')
    success_msg = config.MESSAGES['success_graphs'].format(output_file)
    logger.info(success_msg)
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
        df = load_data(config.CSV_FILE)
        
        # Krok 2: Filtruj podľa pozície
        players = filter_by_position(df, config.POSITION_FILTER)
        
        # Krok 3: Vypočítaj štatistiky
        stats = calculate_statistics(players)
        
        # Krok 4: Vypíš štatistiky
        print_statistics(stats, config.POSITION_FILTER)
        
        # Krok 5: Vytvor grafy
        create_visualizations(players, stats, config.OUTPUT_IMAGE, config.POSITION_FILTER)
        
        logger.info(config.MESSAGES['success_complete'])
        
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        error_msg = config.MESSAGES['error_unexpected'].format(e)
        logger.error(error_msg)
        sys.exit(1)


if __name__ == '__main__':
    main()
