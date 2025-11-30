from Bio.PDB import PDBParser, MMCIFParser

def load_structure_file(file):
  parser = None
  if file.endswith(".cif"):
    parser = MMCIFParser(QUIET=True)
  elif file.endswith(".pdb"):
    parser = PDBParser(QUIET=True)
  else:
    raise Exception("Formato de archivo no soportado. Adjuntar .cif/.pdb")
  print(f"file : {file}")
  structure = parser.get_structure("prot",file)
  return structure

def procesar_estructura(file):
  struct = load_structure_file(file)
  return struct
