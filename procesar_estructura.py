from Bio.PDB import PDBParser, MMCIFParser, PDBList
import os

def fetch_protein_structure(file_name):
  pdbl = PDBList()
  pdbl.retrieve_pdb_file(file_name, file_format='pdb', pdir='.')
  os.rename(f"pdb{file_name}.ent", f"{file_name}.pdb")
  return f"{file_name}.pdb"

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
