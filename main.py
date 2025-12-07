import sys
import os
from procesar_estructura import procesar_estructura, fetch_protein_structure

if len(sys.argv) > 1:
    path = sys.argv[1]

    if not os.path.exists(path):
        if path.isalnum()and len(path) == 4:
            print(f"Descargando estructura PDB para el ID: {path}")
            file = fetch_protein_structure(path)
            files = [file]
        else:
            print("no es un path valido, ingrese un archivo o directorio")
            files = []
    elif os.path.isdir(path):
        files = [os.path.join(path, f) for f in os.listdir(path)]
        #mejora: filtrar solo archivos con extension .pdb o .cif
    else:
        files = [path]
    
    for file in files:
      try: # sustituir el cuerpo por la funcion "residuos_de_la_proteina".
        structure = procesar_estructura(file)
        print(f"Parseado correctamente, structure : {structure}")
      except FileNotFoundError as e:
        print(f"No se encuentra el archivo {file}: {e}")
      except Exception as e:
        print(f"Error al parsear el archivo {file}: {e}")
