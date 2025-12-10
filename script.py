from Bio.PDB import MMCIFParser,PDBParser,NeighborSearch, PDBList
import json
import os
import sys

# ----CONSTANTES------
# Distancia de busqueda
CUTOFF_DISTANCE = 4

#----------LOAD FILE-----------------------

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

def save_structure_file(structure, json_file, mode='a'):
  with open(json_file, mode) as f:
      f.writelines(structure)
#-------------AUX---------------------

def fetch_protein_structure(file_name):
  if os.path.exists(f"{file_name}.pdb"): # ya esta en el directorio, se omite la descarga
    print("omitido")
    return f"{file_name}.pdb"
  pdbl = PDBList()
  pdbl.retrieve_pdb_file(file_name, file_format='pdb', pdir='.')
  os.rename(f"pdb{file_name}.ent", f"{file_name}.pdb")
  return f"{file_name}.pdb"

def search(ligands,protein_atoms):
  neighbor_search = NeighborSearch(protein_atoms)
  result = {}

  for residue_lig, residue_atoms in ligands:
      ligand_chain = residue_lig.get_parent().id
      ligand_name = residue_lig.resname

      key = (ligand_chain, ligand_name)
      if key not in result:
          result[key] = set()

      for lig_atom in residue_atoms:
          neighbors = neighbor_search.search(lig_atom.get_coord(), CUTOFF_DISTANCE)

          for protein_atom in neighbors:
              prot_residue = protein_atom.get_parent()
              prot_chain = prot_residue.get_parent().id
              resname = prot_residue.resname
              resid = prot_residue.id[1]

              result[key].add((prot_chain, resname, resid))

  return result

#coordenadas de atomos de los ligandos de la proteina
def get_protein_and_ligando_coords(structure):
  ligandos = [] # tuplas (resid_ligando, lista_de_atomos)
  protein_atoms = []

  for model in structure:
    for chain in model:
      for residue in chain:  # HETATM  -> son los ligandos
        hetflag = residue.id[0]
        resname = residue.resname

        if hetflag == " ":  # -> proteína
          for atom in residue:
            protein_atoms.append(atom)

        elif resname == "HOH": # -> no agrego  agua
            continue

        else:
          ligand_atoms = list(residue.get_atoms())
          ligandos.append((residue,ligand_atoms))

  return ligandos,protein_atoms


def format_output(contacts,file):
    result = {}
    filename = os.path.splitext(os.path.basename(file))[0]

    for (lig_chain, lig_name), residues in contacts.items():
        struct_key = f"{filename}_{lig_chain}"

        if struct_key not in result:
            result[struct_key] = {"sitios_binding": []}

        ordered = sorted(residues, key=lambda x: x[2])
        reslist = [f"{resname}{resid}" for (_, resname, resid) in ordered]

        result[struct_key]["sitios_binding"].append({
            "cadena_ligando": lig_chain,
            "ligando": lig_name,
            "residuos": reslist
        })

    # Devuelvo un string json formateado
    return json.dumps(result, indent=4)

# ----------- FUNCION PRINCIPAL ----------------------

def residuos_de_la_proteina(file):
  # Cargo la estructura
  structure = load_structure_file(file)

  # Busco las coordenadas de ligandos
  ligands,protein_atoms = get_protein_and_ligando_coords(structure)

  # Busco los residuos
  contacts = search(ligands,protein_atoms)
  result = format_output(contacts,file)
  return result



# ----------- MAIN ----------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if not os.path.exists(path):
            if path.isalnum() and len(path) == 4:
                print(f"Descargando estructura PDB para el ID: {path}")
                file = fetch_protein_structure(path)
                files = [file]
            else:
                print("no es un path valido, ingrese un archivo o directorio")
                files = []
        elif os.path.isdir(path):
            files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.pdb', '.cif'))]
        else:
            files = [path]
        
        content = []
        for file in files:
            try:
                # Llamar a la función principal para procesar y obtener el resultado JSON
                result = residuos_de_la_proteina(file)
                result = str(result)
                if len(result) > 2:
                    print(f"{result}" )
                    content.append(result)
            except FileNotFoundError as e:
                print(f"No se encuentra el archivo {file}: {e}")
            except Exception as e:
                print(f"Error al parsear el archivo {file}: {e}")

        if len(content)>0:
            save_structure_file('{', 'output.json', 'w')
            for idx, cont in enumerate(content):
                save_structure_file(cont[1:-2], "output.json")
                if idx < len(content) - 1:
                    save_structure_file(',', 'output.json')
                else:
                    save_structure_file('}', 'output.json')
