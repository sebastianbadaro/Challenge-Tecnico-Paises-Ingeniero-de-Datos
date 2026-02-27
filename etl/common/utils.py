import requests
import pandas as pd
from prefect import task
from typing import Optional

def validate_ids(df: pd.DataFrame, col: str) -> bool:
    """
    Verifica si todos los IDs en df[col] existen en la lista de países válida.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame que contiene los IDs a verificar.
    col : str
        Nombre de la columna en df con los IDs a validar.

    Retorna
    -------
    bool
        True si todos los IDs en df[col] existen en la lista de países, 
        False si falta alguno.
    """

    # Cargar referencia de países válidos (puede venir de CSV)
    df_countries = pd.read_csv("../stage/countries.csv")  
    valid_ids = set(df_countries["cca3"].dropna().unique())

    # IDs a verificar
    check_ids = set(df[col].dropna().unique())

    return check_ids.issubset(valid_ids)