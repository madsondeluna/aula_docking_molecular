"""
Script para validar resultados do docking HADDOCK
Analisa arquivos PDB dos clusters gerados
"""

import os
import numpy as np
from pathlib import Path

def parse_pdb_coordinates(pdb_file, chain=None, residues=None):
    """
    Extrai coordenadas de átomos específicos de um arquivo PDB
    
    Args:
        pdb_file: Caminho do arquivo PDB
        chain: Identificador da cadeia (opcional)
        residues: Lista de números de resíduos (opcional)
    
    Returns:
        Dict com informações dos átomos
    """
    atoms = []
    
    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                atom_chain = line[21].strip()
                res_num = int(line[22:26].strip())
                
                # Filtrar por cadeia e resíduos se especificado
                if chain and atom_chain != chain:
                    continue
                if residues and res_num not in residues:
                    continue
                
                atom_info = {
                    'atom_name': line[12:16].strip(),
                    'res_name': line[17:20].strip(),
                    'chain': atom_chain,
                    'res_num': res_num,
                    'x': float(line[30:38]),
                    'y': float(line[38:46]),
                    'z': float(line[46:54])
                }
                atoms.append(atom_info)
    
    return atoms

def calculate_rmsd(coords1, coords2):
    """Calcula RMSD entre dois conjuntos de coordenadas"""
    coords1 = np.array(coords1)
    coords2 = np.array(coords2)
    
    diff = coords1 - coords2
    return np.sqrt(np.mean(np.sum(diff**2, axis=1)))

def analyze_cluster_results(results_dir):
    """
    Analisa resultados dos clusters de docking
    
    Args:
        results_dir: Diretório contendo arquivos cluster*.pdb
    """
    results_path = Path(results_dir)
    
    print("=" * 60)
    print("ANÁLISE DE RESULTADOS DO DOCKING")
    print("=" * 60)
    print()
    
    # Encontrar arquivos de clusters
    cluster_files = sorted(results_path.glob("cluster*_1.pdb"))
    
    if not cluster_files:
        print("✗ Nenhum arquivo de cluster encontrado!")
        print(f"  Procurado em: {results_path.absolute()}")
        return
    
    print(f"Encontrados {len(cluster_files)} clusters:")
    for cf in cluster_files:
        print(f"  • {cf.name}")
    print()
    
    # Analisar cada cluster
    print("Análise de interface:")
    print("-" * 60)
    
    for cluster_file in cluster_files:
        print(f"\n{cluster_file.name}:")
        
        # Resíduos ativos E2A
        e2a_active = [38, 40, 45, 46, 69, 71, 78, 80, 94, 96, 141]
        e2a_atoms = parse_pdb_coordinates(cluster_file, chain='A', residues=e2a_active)
        
        # Resíduos ativos HPR
        hpr_active = [15, 16, 17, 20, 48, 49, 51, 52, 54, 56]
        hpr_atoms = parse_pdb_coordinates(cluster_file, chain='B', residues=hpr_active)
        
        print(f"  Átomos E2A (resíduos ativos): {len(e2a_atoms)}")
        print(f"  Átomos HPR (resíduos ativos): {len(hpr_atoms)}")
        
        # Verificar histidinas
        histidines = parse_pdb_coordinates(cluster_file)
        his_count = len([a for a in histidines if a['res_name'] in ['HIS', 'NEP']])
        print(f"  Histidinas encontradas: {his_count}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        results_dir = sys.argv[1]
    else:
        results_dir = input("Digite o caminho para o diretório com resultados: ")
    
    analyze_cluster_results(results_dir)
