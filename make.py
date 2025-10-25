"""
Script para download e preparação automática de estruturas PDB
para o tutorial de docking HADDOCK E2A-HPR

Autor: Madson Aragão
Data: Outubro 2025
"""

import os
import urllib.request
import shutil
from pathlib import Path

# ========================================
# CONFIGURAÇÕES
# ========================================

# Diretório de trabalho
WORK_DIR = Path("tutorial_haddock")
PDB_DIR = WORK_DIR / "pdb_structures"
SCRIPTS_DIR = WORK_DIR / "pymol_scripts"

# Códigos PDB
PDB_CODES = {
    'e2a': '1F3G',
    'hpr': '1HDN',
    'complex': '1GGR'
}

# Resíduos ativos identificados por RMN
ACTIVE_RESIDUES = {
    'e2a': [38, 40, 45, 46, 69, 71, 78, 80, 94, 96, 141],
    'hpr': [15, 16, 17, 20, 48, 49, 51, 52, 54, 56]
}

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def create_directories():
    """Cria os diretórios necessários para o tutorial"""
    print("Criando estrutura de diretórios...")
    PDB_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Diretórios criados em: {WORK_DIR.absolute()}")

def download_pdb(pdb_code, output_file):
    """
    Baixa uma estrutura PDB do RCSB
    
    Args:
        pdb_code: Código PDB de 4 caracteres
        output_file: Caminho do arquivo de saída
    """
    url = f"https://files.rcsb.org/download/{pdb_code}.pdb"
    print(f"Baixando {pdb_code}...")
    
    try:
        urllib.request.urlretrieve(url, output_file)
        print(f"✓ {pdb_code} salvo em: {output_file}")
        return True
    except Exception as e:
        print(f"✗ Erro ao baixar {pdb_code}: {e}")
        return False

def remove_water_molecules(input_file, output_file):
    """
    Remove moléculas de água de um arquivo PDB
    
    Args:
        input_file: Arquivo PDB de entrada
        output_file: Arquivo PDB de saída sem águas
    """
    print(f"Removendo águas de {input_file.name}...")
    
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            # Manter apenas linhas que não são água
            if line.startswith(('ATOM', 'HETATM')):
                if 'HOH' not in line and 'WAT' not in line:
                    f_out.write(line)
            else:
                f_out.write(line)
    
    print(f"✓ Arquivo sem águas salvo: {output_file}")

def add_phosphate_to_his90(input_file, output_file):
    """
    Modifica His90 para NEP (fosfo-histidina) no arquivo PDB
    
    Args:
        input_file: Arquivo PDB de entrada
        output_file: Arquivo PDB de saída com His90 modificada
    """
    print(f"Adicionando grupo fosfato (NEP) à His90...")
    
    modified_lines = []
    with open(input_file, 'r') as f:
        for line in f:
            # Substituir HIS 90 por NEP 90
            if line.startswith(('ATOM', 'HETATM')) and 'HIS' in line:
                # Verificar se é resíduo 90
                res_num = int(line[22:26].strip())
                if res_num == 90:
                    line = line.replace('HIS', 'NEP')
            modified_lines.append(line)
    
    with open(output_file, 'w') as f:
        f.writelines(modified_lines)
    
    print(f"✓ Arquivo com fosfo-histidina salvo: {output_file}")

def extract_first_model(input_file, output_file):
    """
    Extrai apenas o primeiro modelo de um ensemble NMR
    
    Args:
        input_file: Arquivo PDB com múltiplos modelos
        output_file: Arquivo PDB com apenas o primeiro modelo
    """
    print(f"Extraindo primeiro modelo de {input_file.name}...")
    
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        in_first_model = False
        for line in f_in:
            if line.startswith('MODEL') and '1' in line:
                in_first_model = True
            elif line.startswith('ENDMDL'):
                if in_first_model:
                    f_out.write(line)
                    break
            
            if in_first_model or not line.startswith('MODEL'):
                f_out.write(line)
    
    print(f"✓ Primeiro modelo extraído: {output_file}")

# ========================================
# SCRIPTS PYMOL
# ========================================

def create_pymol_visualization_scripts():
    """Cria scripts PyMOL para todas as visualizações do tutorial"""
    
    # Script 1: Visualização inicial E2A
    script_e2a_initial = """# Script PyMOL: Visualização inicial E2A
# Carregar estrutura
load {pdb_dir}/1F3G.pdb

# Configuração básica
show cartoon
hide lines
color cyan, all

# Mostrar histidinas
show sticks, resn HIS
color yellow, resn HIS

# Visualizar resíduos ativos
select e2a_active, (resi 38,40,45,46,69,71,78,80,94,96,141)
color red, e2a_active
show surface, e2a_active

# Ajustar visualização
bg_color white
set ray_shadows, 0

print "E2A carregada com resíduos ativos destacados"
""".format(pdb_dir=PDB_DIR.absolute())
    
    # Script 2: Visualização inicial HPR
    script_hpr_initial = """# Script PyMOL: Visualização inicial HPR (ensemble)
# Carregar estrutura
load {pdb_dir}/1HDN.pdb

# Configuração básica
hide all
show ribbon
color green, all

# Mostrar todos os modelos do ensemble
set all_states, on

# Visualizar resíduos ativos
select hpr_active, (resi 15,16,17,20,48,49,51,52,54,56)
color red, hpr_active
show sticks, hpr_active

# Ajustar visualização
bg_color white
set ray_shadows, 0

print "HPR ensemble carregado com resíduos ativos destacados"
""".format(pdb_dir=PDB_DIR.absolute())
    
    # Script 3: Comparação com estrutura de referência
    script_comparison = """# Script PyMOL: Comparação com estrutura nativa
# Carregar estrutura nativa
load {pdb_dir}/1GGR.pdb
show cartoon
color yellow, 1GGR and chain A
color orange, 1GGR and chain B

# Corrigir numeração da cadeia B
alter (chain B and 1GGR), resv -= 300

# Selecionar cadeia A para alinhamento
select ref_chain_a, 1GGR and chain A

# Instruções para carregar clusters
print "Estrutura de referência carregada!"
print "Para comparar com seus resultados:"
print "1. Carregue os arquivos cluster1_1.pdb, cluster2_1.pdb, etc."
print "2. Execute: align cluster1_1, ref_chain_a, cycles=0"
print "3. Execute: rms_cur cluster1_1 and chain B, 1GGR and chain B"

bg_color white
""".format(pdb_dir=PDB_DIR.absolute())
    
    # Script 4: Análise de histidinas
    script_histidines = """# Script PyMOL: Análise de histidinas para validação biológica
# Carregar estruturas preparadas
load {pdb_dir}/e2aP_1F3G.pdb, e2a
load {pdb_dir}/hpr-ensemble.pdb, hpr

# Configuração básica
show cartoon
color cyan, e2a
color green, hpr

# Selecionar e visualizar histidinas
select histidines, resn HIS+NEP
show spheres, histidines
color red, histidines and e2a
color orange, histidines and hpr

# Labels para identificar resíduos
label histidines and name CA, "%s-%s" % (resn, resi)

# Medir distâncias (exemplo - ajuste conforme necessário)
distance dist_his, (e2a and resn NEP and resi 90 and name ND1), (hpr and resn HIS and name NE2)

print "Histidinas visualizadas!"
print "Para validar transferência de fosfato:"
print "- Distância N-P ideal: 3-3.5 Å"
print "- Use: distance nome, (atom1), (atom2)"

bg_color white
""".format(pdb_dir=PDB_DIR.absolute())
    
    # Script 5: Visualização completa para análise
    script_full_analysis = """# Script PyMOL: Análise completa dos resultados
# Carregar estruturas
load {pdb_dir}/e2aP_1F3G.pdb, e2a_final
load {pdb_dir}/hpr-ensemble.pdb, hpr_final

# Resíduos ativos E2A
select e2a_active, e2a_final and (resi 38,40,45,46,69,71,78,80,94,96,141)
color red, e2a_active

# Resíduos ativos HPR
select hpr_active, hpr_final and (resi 15,16,17,20,48,49,51,52,54,56)
color orange, hpr_active

# Visualização
show cartoon
show surface, e2a_active or hpr_active
set transparency, 0.5

# Histidinas
select histidines, resn HIS+NEP
show spheres, histidines
color yellow, histidines

print "=== ANÁLISE COMPLETA ==="
print "Resíduos ativos destacados em vermelho (E2A) e laranja (HPR)"
print "Histidinas mostradas como esferas amarelas"
print ""
print "Para carregar resultados do docking:"
print "load cluster1_1.pdb"
print "align cluster1_1, e2a_final"

bg_color white
set ray_shadows, 0
""".format(pdb_dir=PDB_DIR.absolute())
    
    # Salvar scripts
    scripts = {
        '01_visualize_e2a.pml': script_e2a_initial,
        '02_visualize_hpr.pml': script_hpr_initial,
        '03_compare_reference.pml': script_comparison,
        '04_analyze_histidines.pml': script_histidines,
        '05_full_analysis.pml': script_full_analysis
    }
    
    print("\nCriando scripts PyMOL...")
    for filename, content in scripts.items():
        script_path = SCRIPTS_DIR / filename
        with open(script_path, 'w') as f:
            f.write(content)
        print(f"✓ Script criado: {script_path}")

# ========================================
# FLUXO PRINCIPAL
# ========================================

def main():
    """Função principal que executa todo o pipeline"""
    
    print("=" * 60)
    print("PREPARAÇÃO DE ESTRUTURAS - TUTORIAL HADDOCK E2A-HPR")
    print("=" * 60)
    print()
    
    # 1. Criar diretórios
    create_directories()
    print()
    
    # 2. Download das estruturas PDB
    print("PASSO 1: Download das estruturas PDB")
    print("-" * 60)
    
    pdb_files = {}
    for name, code in PDB_CODES.items():
        output_file = PDB_DIR / f"{code}.pdb"
        if download_pdb(code, output_file):
            pdb_files[name] = output_file
    print()
    
    # 3. Processar E2A
    print("PASSO 2: Processando estrutura E2A (1F3G)")
    print("-" * 60)
    
    if 'e2a' in pdb_files:
        # Remover águas
        e2a_no_water = PDB_DIR / "e2a_1F3G.pdb"
        remove_water_molecules(pdb_files['e2a'], e2a_no_water)
        
        # Adicionar grupo fosfato
        e2a_phospho = PDB_DIR / "e2aP_1F3G.pdb"
        add_phosphate_to_his90(e2a_no_water, e2a_phospho)
    print()
    
    # 4. Processar HPR
    print("PASSO 3: Processando estrutura HPR (1HDN)")
    print("-" * 60)
    
    if 'hpr' in pdb_files:
        # HPR ensemble completo
        hpr_ensemble = PDB_DIR / "hpr-ensemble.pdb"
        shutil.copy(pdb_files['hpr'], hpr_ensemble)
        print(f"✓ Ensemble HPR copiado: {hpr_ensemble}")
        
        # Extrair primeiro modelo para exercícios
        hpr_single = PDB_DIR / "hpr-single.pdb"
        extract_first_model(pdb_files['hpr'], hpr_single)
    print()
    
    # 5. Processar estrutura de referência
    print("PASSO 4: Processando estrutura de referência (1GGR)")
    print("-" * 60)
    
    if 'complex' in pdb_files:
        print(f"✓ Estrutura de referência disponível: {pdb_files['complex']}")
    print()
    
    # 6. Criar scripts PyMOL
    print("PASSO 5: Criando scripts de visualização PyMOL")
    print("-" * 60)
    create_pymol_visualization_scripts()
    print()
    
    # 7. Criar arquivo de informações
    info_file = WORK_DIR / "README_estruturas.txt"
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("ESTRUTURAS PREPARADAS - TUTORIAL HADDOCK\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("ESTRUTURAS PDB BAIXADAS:\n")
        f.write("-" * 60 + "\n")
        f.write(f"• 1F3G.pdb - E2A (enzima IIA específica para glicose)\n")
        f.write(f"• 1HDN.pdb - HPR (proteína transportadora de fosfato)\n")
        f.write(f"• 1GGR.pdb - Complexo E2A-HPR nativo (referência)\n\n")
        
        f.write("ARQUIVOS PREPARADOS PARA DOCKING:\n")
        f.write("-" * 60 + "\n")
        f.write(f"• e2a_1F3G.pdb - E2A sem moléculas de água\n")
        f.write(f"• e2aP_1F3G.pdb - E2A com His90 fosforilada (NEP)\n")
        f.write(f"• hpr-ensemble.pdb - HPR ensemble completo (30 modelos)\n")
        f.write(f"• hpr-single.pdb - HPR primeiro modelo apenas\n\n")
        
        f.write("ARQUIVOS PARA SUBMISSÃO NO HADDOCK:\n")
        f.write("-" * 60 + "\n")
        f.write(f"→ Primeira molécula: e2aP_1F3G.pdb\n")
        f.write(f"→ Segunda molécula: hpr-ensemble.pdb\n\n")
        
        f.write("RESÍDUOS ATIVOS (para configuração HADDOCK):\n")
        f.write("-" * 60 + "\n")
        f.write(f"→ E2A: {','.join(map(str, ACTIVE_RESIDUES['e2a']))}\n")
        f.write(f"→ HPR: {','.join(map(str, ACTIVE_RESIDUES['hpr']))}\n\n")
        
        f.write("SCRIPTS PYMOL DISPONÍVEIS:\n")
        f.write("-" * 60 + "\n")
        f.write(f"1. 01_visualize_e2a.pml - Visualização inicial E2A\n")
        f.write(f"2. 02_visualize_hpr.pml - Visualização ensemble HPR\n")
        f.write(f"3. 03_compare_reference.pml - Comparação com referência\n")
        f.write(f"4. 04_analyze_histidines.pml - Análise de histidinas\n")
        f.write(f"5. 05_full_analysis.pml - Análise completa\n\n")
        
        f.write("COMO USAR OS SCRIPTS PYMOL:\n")
        f.write("-" * 60 + "\n")
        f.write("1. Abra o PyMOL\n")
        f.write("2. File → Run Script → Selecione o script desejado\n")
        f.write("OU\n")
        f.write("3. No terminal PyMOL: @caminho/para/script.pml\n\n")
        
        f.write("PRÓXIMOS PASSOS:\n")
        f.write("-" * 60 + "\n")
        f.write("1. Visualize as estruturas com os scripts PyMOL\n")
        f.write("2. Acesse: https://alcazar.science.uu.nl/services/HADDOCK2.2/\n")
        f.write("3. Submeta e2aP_1F3G.pdb e hpr-ensemble.pdb\n")
        f.write("4. Use os resíduos ativos listados acima\n")
        f.write("5. Aguarde resultados e faça análise comparativa\n")
    
    print(f"✓ Arquivo de informações criado: {info_file}")
    print()
    
    # Sumário final
    print("=" * 60)
    print("PREPARAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print()
    print(f"Diretório de trabalho: {WORK_DIR.absolute()}")
    print(f"Estruturas PDB: {PDB_DIR.absolute()}")
    print(f"Scripts PyMOL: {SCRIPTS_DIR.absolute()}")
    print()
    print("Leia o arquivo README_estruturas.txt para mais informações")
    print()
    print("Próximos passos:")
    print("   1. Abra PyMOL e execute os scripts de visualização")
    print("   2. Submeta os arquivos preparados no servidor HADDOCK")
    print("   3. Analise os resultados usando os scripts fornecidos")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcesso interrompido pelo usuário.")
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
