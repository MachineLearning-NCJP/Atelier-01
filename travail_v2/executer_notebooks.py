"""Réexécute les notebooks dans l'ordre avec le Python courant, puis vérifie les sorties.
Usage depuis la racine : python travail_v2/executer_notebooks.py
On peut passer les noms de notebooks en arguments pour une reprise ciblée.
"""
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

HERE = Path(__file__).resolve().parent
names = sys.argv[1:] or ["01_eda_vehicules.ipynb", "02_supervise_co2.ipynb", "03_non_supervise_vehicules.ipynb"]
for name in names:
    path = HERE / name
    if path.parent != HERE or path.suffix != ".ipynb":
        raise ValueError("Indiquer un nom de notebook du dossier travail_v2.")
    print(f"Exécution : {path.name}", flush=True)
    notebook = nbformat.read(path, as_version=4)
    # Utiliser l'environnement Python appelant, indépendamment du kernel Jupyter utilisateur.
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    client = NotebookClient(notebook, km=manager, timeout=1200, resources={"metadata": {"path": str(HERE)}})
    try:
        client.execute()
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
    errors = [o for c in notebook.cells if c.cell_type == "code" for o in c.outputs if o.output_type == "error"]
    if errors:
        raise RuntimeError(f"{path.name} contient {len(errors)} erreur(s)")
    nbformat.write(notebook, path)
    print(f"Terminé : {path.name}", flush=True)
