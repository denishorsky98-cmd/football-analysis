"""
Football Analysis Project - Utility Functions

Modul: utils.py
Popis: Pomocné funkcie pre analýzu a spracovanie dát.

Autor: denishorsky98-cmd
Dátum: 2026
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# DÁTOVÉ FUNKCIE
# ============================================================================

def validate_columns(df: pd.DataFrame, required_columns: dict) -> bool:
    """
    Validuje či dataset obsahuje všetky požadované stĺpce.
    
    Args:
        df (pd.DataFrame): Dataset na validáciu
        required_columns (dict): Slovník s požadovanými stĺpcami
        
    Returns:
        bool: True ak sú všetky stĺpce prítomné, inak False
    """
    missing_cols = [col for col in required_columns.values() if col not in df.columns]
    
    if missing_cols:
        logger.error(f"Chýbajúce stĺpce: {', '.join(missing_cols)}")
        return False
    
    logger.info("✅ Všetky požadované stĺpce sú prítomné")
    return True


def remove_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    """
    Odstráni duplikáty z datasetu.
    
    Args:
        df (pd.DataFrame): Dataset s možnými duplikátmi
        subset (list): Stĺpce na základe ktorých hľadať duplikáty
        
    Returns:
        pd.DataFrame: Dataset bez duplikátov
    """
    before = len(df)
    df_cleaned = df.drop_duplicates(subset=subset)
    after = len(df_cleaned)
    removed = before - after
    
    if removed > 0:
        logger.info(f"Odstránených duplikátov: {removed}")
    
    return df_cleaned


def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
    """
    Spracuje chýbajúce hodnoty v datasete.
    
    Args:
        df (pd.DataFrame): Dataset s chýbajúcimi hodnotami
        strategy (str): Stratégia ('drop', 'mean', 'forward_fill')
        
    Returns:
        pd.DataFrame: Dataset bez/s spracovanými chýbajúcimi hodnotami
    """
    before = df.isnull().sum().sum()
    
    if strategy == 'drop':
        df_cleaned = df.dropna()
    elif strategy == 'mean':
        df_cleaned = df.fillna(df.mean(numeric_only=True))
    elif strategy == 'forward_fill':
        df_cleaned = df.fillna(method='ffill')
    else:
        logger.warning(f"Neznáma stratégia: {strategy}. Používam 'drop'.")
        df_cleaned = df.dropna()
    
    after = df_cleaned.isnull().sum().sum()
    handled = before - after
    
    if handled > 0:
        logger.info(f"Spracovaných chýbajúcich hodnôt: {handled}")
    
    return df_cleaned


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Vytvorí zhrnutie informácií o datasete.
    
    Args:
        df (pd.DataFrame): Dataset na analýzu
        
    Returns:
        dict: Informácie o datasete
    """
    summary = {
        'rows': len(df),
        'columns': len(df.columns),
        'column_names': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicates': df.duplicated().sum(),
    }
    
    return summary


# ============================================================================
# ŠTATISTICKÉ FUNKCIE
# ============================================================================

def correlation_analysis(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    Vypočíta koreláciu medzi stĺpcami.
    
    Args:
        df (pd.DataFrame): Dataset
        cols (list): Stĺpce na analýzu
        
    Returns:
        pd.DataFrame: Korelačná matica
    """
    return df[cols].corr()


def percentile_analysis(df: pd.DataFrame, column: str, percentiles: list = None) -> dict:
    """
    Vypočíta percentily pre stĺpec.
    
    Args:
        df (pd.DataFrame): Dataset
        column (str): Stĺpec na analýzu
        percentiles (list): Percentily (0-100)
        
    Returns:
        dict: Percentily
    """
    if percentiles is None:
        percentiles = [25, 50, 75, 90, 95]
    
    result = {}
    for p in percentiles:
        result[f'{p}%'] = df[column].quantile(p / 100)
    
    return result


def group_by_analysis(df: pd.DataFrame, group_col: str, agg_col: str, 
                     agg_func: str = 'sum', top_n: int = 10) -> pd.DataFrame:
    """
    Vykonáva analýzu skupinovej agregácie.
    
    Args:
        df (pd.DataFrame): Dataset
        group_col (str): Stĺpec na zoskupenie
        agg_col (str): Stĺpec na agregáciu
        agg_func (str): Agregačná funkcia (sum, mean, count, max, min)
        top_n (int): Počet top výsledkov
        
    Returns:
        pd.DataFrame: Zoskupené a agregované dáta
    """
    aggregated = df.groupby(group_col)[agg_col].agg(agg_func).nlargest(top_n)
    return aggregated


# ============================================================================
# EXPORTOVANIE FUNKCIÍ
# ============================================================================

def export_to_csv(df: pd.DataFrame, filepath: str) -> bool:
    """
    Exportuje DataFrame do CSV súboru.
    
    Args:
        df (pd.DataFrame): DataFrame na export
        filepath (str): Cesta k výstupnému súboru
        
    Returns:
        bool: True ak bol export úspešný
    """
    try:
        df.to_csv(filepath, index=False, encoding='utf-8')
        logger.info(f"✅ Dáta exportované do '{filepath}'")
        return True
    except Exception as e:
        logger.error(f"❌ Chyba pri exporte: {e}")
        return False


def export_to_excel(df: pd.DataFrame, filepath: str) -> bool:
    """
    Exportuje DataFrame do Excel súboru.
    
    Args:
        df (pd.DataFrame): DataFrame na export
        filepath (str): Cesta k výstupnému súboru
        
    Returns:
        bool: True ak bol export úspešný
    """
    try:
        df.to_excel(filepath, index=False, engine='openpyxl')
        logger.info(f"✅ Dáta exportované do '{filepath}'")
        return True
    except Exception as e:
        logger.error(f"❌ Chyba pri exporte: {e}")
        return False


# ============================================================================
# FORMÁTOVANIE FUNKCIÍ
# ============================================================================

def format_number(value: float, decimal_places: int = 2) -> str:
    """
    Formátuje číslo na reťazec s daným počtom desatinných miest.
    
    Args:
        value (float): Číslo na formátovanie
        decimal_places (int): Počet desatinných miest
        
    Returns:
        str: Formátované číslo
    """
    return f"{value:.{decimal_places}f}"


def format_table(df: pd.DataFrame, max_rows: int = 10) -> str:
    """
    Formátuje DataFrame na pekný tabuľkový výstup.
    
    Args:
        df (pd.DataFrame): DataFrame na formátovanie
        max_rows (int): Maximálny počet riadkov
        
    Returns:
        str: Formátovaná tabuľka
    """
    return df.head(max_rows).to_string(index=False)


def print_section(title: str, width: int = 70) -> None:
    """
    Vytiskne nadpis sekcie s ozdôbou.
    
    Args:
        title (str): Text nadpisu
        width (int): Šírka čiary
    """
    print("\n" + "=" * width)
    print(f"🔷 {title}")
    print("=" * width)


def print_subsection(title: str, width: int = 70) -> None:
    """
    Vytiskne podnadpis sekcie s ozdôbou.
    
    Args:
        title (str): Text podnadpisu
        width (int): Šírka čiary
    """
    print("\n" + "-" * width)
    print(f"▶ {title}")
    print("-" * width)
