from pathlib import Path
import pandas as pd

def load_valid_country_ids():
    # Subir desde etl/common → Countries/
    project_root = Path(__file__).resolve().parents[2]
    stage_dir = project_root / "stage"

    file_path = stage_dir / "countries.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró {file_path}. Corré primero el ETL de countries.")

    # Ajustar al nombre correcto de columna de tu ETL (probablemente "id_country")
    df = pd.read_csv(file_path, usecols=["cca3"])
    return df["cca3"].dropna().unique().tolist()
