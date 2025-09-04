import nbformat,sys
from nbconvert import PythonExporter

if len(sys.argv) > 1:
    nombre = sys.argv[1]
else:
    print("No me diste ningún nombre")

with open(f"/home/jrodarte/Proyectos/prestadero/notas/{nombre}.ipynb") as f:
    nb = nbformat.read(f, as_version=4)

exporter = PythonExporter()
source, _ = exporter.from_notebook_node(nb)

with open(f"{nombre}F.py", "w") as f:
    f.write(source)
