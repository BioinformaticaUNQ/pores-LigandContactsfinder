from procesar_estructura import load_structure_file

def test_archivo_cif_no_existe():
    archivo_cif = "./test.cif"

    try:
        load_structure_file(archivo_cif)
    except FileNotFoundError:
        assert True

def test_archivo_pdb_no_existe():
    archivo_pdb = "./test.pdb"

    try:
        load_structure_file(archivo_pdb)
    except FileNotFoundError:
        assert True

def test_archivo_cif_existe():
    archivo_cif = "./3U8K.cif"

    assert load_structure_file(archivo_cif) is not None

def test_archivo_pdb_existe():
    archivo_pdb = "./3U8K.pdb"

    assert load_structure_file(archivo_pdb) is not None

def test_archivo_formato_incorrecto():
    archivo_formato_incorrecto = "./README.md"

    try:
        load_structure_file(archivo_formato_incorrecto)
    except Exception:
        assert True