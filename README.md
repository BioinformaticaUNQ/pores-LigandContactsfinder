# Pores-LigandContactsFinder

Proyecto final: Herramienta para identificar contactos entre ligandos y residuos de proteínas en estructuras PDB/CIF.

Esta herramienta utiliza Biopython para analizar archivos de estructuras proteicas (formatos .pdb o .cif) y detectar residuos de proteínas que están dentro de una distancia especificada (por defecto 4 Å) de ligandos. Los resultados se exportan en formato JSON para análisis posterior.

## Instalación

### Requisitos

- Python 3.7+
- Biopython: Instala con pip:

pip install biopython

## Uso

Ejecuta el script desde la línea de comandos. Soporta archivos locales (.pdb/.cif), directorios con múltiples archivos, o IDs de PDB para descarga automática.

### Sintaxis General

python script.py [opciones] <archivo_o_id>

### Opciones y Parámetros

- `<archivo_o_id>`: Ruta a un archivo (.pdb/.cif), directorio con archivos, o ID de PDB (4 letras, e.g., 3FAT). Si es un directorio, procesa todos los archivos .pdb/.cif en él.
- `-c`, `--cutoff`: Distancia de corte en Ångstroms para buscar contactos (por defecto: 4.0). Debe ser un número positivo.
- `-o`, `--output`: Archivo de salida JSON (por defecto: output.json). Si no se especifica, se guarda en el directorio actual.
- `-v`, `--verbose`: Modo verboso: Muestra más detalles durante la ejecución (e.g., progreso de descarga).
- `-h`, `--help`: Muestra este mensaje de ayuda y sale.

### Ejemplos de Corrida

1. **Procesar un archivo local (.pdb):**
   python script.py estructura.pdb

- Descarga: No.
- Salida: output.json con contactos encontrados.

2. **Procesar un archivo .cif con distancia personalizada:**
   python script.py -c 5.0 estructura.cif

- Busca contactos dentro de 5 Å.

3. **Procesar un directorio con múltiples archivos:**
   python script.py /ruta_al_directorio

- Procesa todos los .pdb/.cif en el directorio.

4. **Descargar y procesar un ID de PDB:**
   python script.py 3FAT

- Descarga automáticamente desde PDB si no existe localmente.

5. **Modo verboso con salida personalizada:**
   python script.py -v -o resultados.json 1ABC

- Muestra progreso y guarda en resultados.json.

### Formato de Salida JSON

El output es un objeto JSON con claves por estructura y ligando. Ejemplo:

```json
{
  "3FAT_A": {
    "sitios_binding": [
      {
        "cadena_ligando": "A",
        "ligando": "ATP",
        "residuos": ["GLY10", "ALA15", "SER20"]
      }
    ]
  }
}
```

    sitios_binding: Lista de ligandos con sus residuos contactados.
    Residuos ordenados por ID.

Si procesas múltiples archivos, el JSON combina resultados en un objeto único (con claves únicas por archivo).

### Errores Comunes

- Archivo no encontrado: Verifica la ruta o ID de PDB.
- Formato no soportado: Solo .pdb/.cif.
- ID inválido: Los IDs de PDB deben ser 4 caracteres alfanuméricos.
- JSON inválido: Si hay múltiples resultados, asegúrate de que las claves sean únicas

## Pruebas

Este proyecto incluye pruebas unitarias usando `pytest` para asegurar la calidad del código.

### Instalación de dependencias de pruebas

pip install pytest pytest-cov

### Ejecutar pruebas

- Ejecuta todas las pruebas:
  pytest
