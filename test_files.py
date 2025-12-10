import pytest
import json
import os
from script import residuos_de_la_proteina,load_structure_file

# Ruta a archivos de prueba 
TEST_DATA_DIR = "./test_files/"
ARCHIVO_CIF_CON_LIGANDOS = os.path.join(TEST_DATA_DIR, "3U8K.cif")  # Tiene ligandos
ARCHIVO_PDB_CON_LIGANDOS = os.path.join(TEST_DATA_DIR, "3U8K.pdb")  # Tiene ligandos
ARCHIVO_SIN_LIGANDOS = os.path.join(TEST_DATA_DIR, "9YFM.cif")  # Sin ligandos

@pytest.fixture
def setup_test_files():
    if not os.path.exists(ARCHIVO_CIF_CON_LIGANDOS):
        pytest.skip(f"Archivo de prueba {ARCHIVO_CIF_CON_LIGANDOS} no encontrado")

def test_archivo_cif_no_existe():
    archivo_cif = "./test_no_existe.cif"
    with pytest.raises(FileNotFoundError):
        residuos_de_la_proteina(archivo_cif)

def test_archivo_pdb_no_existe():
    archivo_pdb = "./test_no_existe.pdb"
    with pytest.raises(FileNotFoundError):
        residuos_de_la_proteina(archivo_pdb)

def test_archivo_cif_existe_con_ligandos(setup_test_files):
    result = residuos_de_la_proteina(ARCHIVO_CIF_CON_LIGANDOS)
    assert result is not None
    # Valido que sea un JSON válido y no vacío
    data = json.loads(result)
    assert isinstance(data, dict)
    assert len(data) > 0  # Debe tener al menos una clave (ej "3U8K_A")
    # Verifico estructura: al menos un sitio_binding con residuos
    for key, value in data.items():
        assert "sitios_binding" in value
        assert isinstance(value["sitios_binding"], list)
        if value["sitios_binding"]:  # Si hay ligandos
            sitio = value["sitios_binding"][0]
            assert "ligando" in sitio and "residuos" in sitio
            assert len(sitio["residuos"]) > 0

def test_archivo_pdb_existe_con_ligandos(setup_test_files):
    result = residuos_de_la_proteina(ARCHIVO_PDB_CON_LIGANDOS)
    assert result is not None
    data = json.loads(result)
    assert isinstance(data, dict)

def test_archivo_sin_ligandos(setup_test_files):
    result = residuos_de_la_proteina(ARCHIVO_SIN_LIGANDOS)
    assert result == "{}"  # Resultado vacío esperado
    data = json.loads(result)
    assert data == {}  # Dict vacío

def test_archivo_formato_incorrecto():
    archivo_formato_incorrecto = "./README.md"
    with pytest.raises(Exception, match="Formato de archivo no soportado"):
        residuos_de_la_proteina(archivo_formato_incorrecto)

def test_load_structure_file_cif(setup_test_files):
    structure = load_structure_file(ARCHIVO_CIF_CON_LIGANDOS)
    assert structure is not None
    # Verifico que tenga cadenas
    assert len(list(structure.get_models())) > 0

def test_load_structure_file_pdb(setup_test_files):
    structure = load_structure_file(ARCHIVO_PDB_CON_LIGANDOS)
    assert structure is not None
    assert len(list(structure.get_models())) > 0