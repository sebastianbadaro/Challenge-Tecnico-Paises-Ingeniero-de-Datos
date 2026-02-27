import nbformat
from nbconvert import PythonExporter
from prefect import flow

# --- Importar tu notebook ---
def load_notebook(path):
    with open(path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    exporter = PythonExporter()
    source, _ = exporter.from_notebook_node(nb)
    code = compile(source, path, "exec")
    module = {}
    exec(code, module)
    return module

# Cargar el notebook donde definiste world_data_master_flow
notebook = load_notebook("master_flow.ipynb")

# Exponer el flow para Prefect
world_data_master_flow = notebook["world_data_master_flow"]

if __name__ == "__main__":
    world_data_master_flow()
