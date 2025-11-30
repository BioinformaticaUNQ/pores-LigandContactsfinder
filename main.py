import sys
from procesar_estructura import procesar_estructura

if len(sys.argv) > 1:
    for file in sys.argv[1:]:
      try: # sustituir el cuerpo por la funcion "residuos_de_la_proteina".
        structure = procesar_estructura(file)
        print(f"Parseado correctamente, structure : {structure}")
      except FileNotFoundError as e:
        print(f"No se encuentra el archivo {file}: {e}")
      except Exception as e:
        print(f"Error al parsear el archivo {file}: {e}")
