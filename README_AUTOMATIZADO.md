# Scripts Python - Tutorial HADDOCK

Conjunto de scripts para automatizar a preparação e validação de estruturas proteicas para docking molecular com HADDOCK.

## Arquivos

- `make.py` - Script de preparação automática das estruturas PDB
- `validation.py` - Script de validação e análise dos resultados após docking

---

## make.py

### Descrição

Script que automatiza todo o processo de preparação das estruturas proteicas necessárias para o tutorial de docking HADDOCK.

### O que o script faz

#### 1. Cria estrutura de diretórios
- `tutorial_haddock/pdb_structures/` - Armazena estruturas PDB baixadas e processadas
- `tutorial_haddock/pymol_scripts/` - Scripts de visualização PyMOL prontos para uso

#### 2. Baixa estruturas do RCSB PDB
- **1F3G** - Enzima E2A (glucose-specific enzyme IIA)
- **1HDN** - Proteína HPR (histidine-containing phosphocarrier protein)  
- **1GGR** - Complexo E2A-HPR nativo (estrutura de referência para validação)

#### 3. Processa estrutura E2A
- Remove moléculas de água cristalográficas que podem interferir no docking
- Gera arquivo `e2a_1F3G.pdb` limpo
- Modifica resíduo His90 para NEP (fosfo-histidina)
- Gera arquivo `e2aP_1F3G.pdb` pronto para submissão no HADDOCK

#### 4. Processa estrutura HPR
- Copia ensemble completo com 30 confôrmeros para `hpr-ensemble.pdb`
- Extrai apenas o primeiro modelo para `hpr-single.pdb` (usado em exercícios alternativos)

#### 5. Gera scripts PyMOL automatizados
- `01_visualize_e2a.pml` - Visualização inicial da E2A com resíduos ativos destacados
- `02_visualize_hpr.pml` - Visualização do ensemble HPR
- `03_compare_reference.pml` - Comparação dos resultados com estrutura nativa
- `04_analyze_histidines.pml` - Análise das histidinas para validação biológica
- `05_full_analysis.pml` - Análise completa integrada dos modelos

#### 6. Cria documentação
- Gera `README_estruturas.txt` com todas as informações necessárias
- Lista resíduos ativos para submissão no HADDOCK
- Fornece instruções de uso dos scripts PyMOL

### Como executar

```
python make.py
```

### Saída esperada

```
============================================================
PREPARAÇÃO DE ESTRUTURAS - TUTORIAL HADDOCK E2A-HPR
Criando estrutura de diretórios...
Diretórios criados em: /caminho/tutorial_haddock

PASSO 1: Download das estruturas PDB
Baixando 1F3G...
1F3G salvo em: tutorial_haddock/pdb_structures/1F3G.pdb
Baixando 1HDN...
1HDN salvo em: tutorial_haddock/pdb_structures/1HDN.pdb
Baixando 1GGR...
1GGR salvo em: tutorial_haddock/pdb_structures/1GGR.pdb

PASSO 2: Processando estrutura E2A (1F3G)
Removendo águas de 1F3G.pdb...
Arquivo sem águas salvo: e2a_1F3G.pdb
Adicionando grupo fosfato (NEP) à His90...
Arquivo com fosfo-histidina salvo: e2aP_1F3G.pdb

PASSO 3: Processando estrutura HPR (1HDN)
Ensemble HPR copiado: hpr-ensemble.pdb
Extraindo primeiro modelo de 1HDN.pdb...
Primeiro modelo extraído: hpr-single.pdb

PASSO 4: Processando estrutura de referência (1GGR)
Estrutura de referência disponível: 1GGR.pdb

PASSO 5: Criando scripts de visualização PyMOL
Criando scripts PyMOL...
Script criado: 01_visualize_e2a.pml
Script criado: 02_visualize_hpr.pml
Script criado: 03_compare_reference.pml
Script criado: 04_analyze_histidines.pml
Script criado: 05_full_analysis.pml

============================================================
PREPARAÇÃO CONCLUÍDA COM SUCESSO!
```


### Estrutura de arquivos gerados

aula-docking-molcular
├── pdb_structures/
│ ├── 1F3G.pdb # E2A original baixada do RCSB
│ ├── 1HDN.pdb # HPR original baixada do RCSB
│ ├── 1GGR.pdb # Complexo nativo (referência)
│ ├── e2a_1F3G.pdb # E2A processada sem águas
│ ├── e2aP_1F3G.pdb # E2A com His90 fosforilada (USAR NO HADDOCK)
│ ├── hpr-ensemble.pdb # HPR ensemble completo (USAR NO HADDOCK)
│ └── hpr-single.pdb # HPR único modelo (para exercícios)
├── pymol_scripts/
│ ├── 01_visualize_e2a.pml
│ ├── 02_visualize_hpr.pml
│ ├── 03_compare_reference.pml
│ ├── 04_analyze_histidines.pml
│ └── 05_full_analysis.pml
└── README.md # Documentação completa gerada
└── README_AUTOMATIZADO.md # Documentação explicativa da automação dos processos 


### Arquivos para submissão no HADDOCK

Após executar `make.py`, use estes arquivos no servidor HADDOCK:

**Primeira molécula (E2A):**

```
/pdb_structures/e2aP_1F3G.pdb
```

**Segunda molécula (HPR):**

```
/pdb_structures/hpr-ensemble.pdb
```


**Resíduos ativos para configuração:**
- E2A: `38,40,45,46,69,71,78,80,94,96,141`
- HPR: `15,16,17,20,48,49,51,52,54,56`

### Próximos passos

#### 1. Visualizar estruturas no PyMOL

```
pymol /pymol_scripts/01_visualize_e2a.pml
```


Ou abra o PyMOL e use: File → Run Script → selecione o script

#### 2. Submeter no HADDOCK

Acesse: https://alcazar.science.uu.nl/services/HADDOCK2.2/haddockserver-easy.html

Configure:
- Job name: `E2A-HPR`
- First Molecule: `e2aP_1F3G.pdb` com resíduos ativos da E2A
- Second Molecule: `hpr-ensemble.pdb` com resíduos ativos da HPR
- Marque "Define passive residues automatically" para ambas

#### 3. Aguardar resultados

O processamento leva de 30 minutos a várias horas. Você receberá notificação por email.

---

## validation.py

### Descrição

Script para análise e validação dos resultados obtidos após o docking no HADDOCK.

### O que o script faz

#### 1. Localiza arquivos de resultados
- Busca automaticamente arquivos `cluster*_1.pdb` no diretório especificado
- Lista todos os clusters encontrados para análise

#### 2. Analisa interface de cada cluster
- Extrai coordenadas dos átomos nos resíduos ativos
- Conta átomos na interface de E2A (cadeia A)
- Conta átomos na interface de HPR (cadeia B)
- Identifica resíduos envolvidos na interação

#### 3. Verifica histidinas
- Identifica todas as histidinas presentes (HIS e NEP)
- Conta quantidade de histidinas em cada cluster
- Essencial para validar mecanismo de transferência de fosfato

#### 4. Gera relatório comparativo
- Exibe estatísticas organizadas de cada cluster
- Facilita comparação entre diferentes soluções
- Identifica consistências e divergências

### Como executar

#### Opção 1: Fornecer caminho como argumento

```
python validation.py /caminho/para/resultados_docking
```


#### Opção 2: Execução interativa

```
python validation.py
```

O script solicitará:

```
Digite o caminho para o diretório com resultados...
```


Digite o caminho e pressione Enter.

### Exemplo prático

Após baixar resultados do HADDOCK para `~/Downloads/haddock_results`
`cd ~/Downloads/haddock_results`
`ls`

Saída: `cluster1_1.pdb` `cluster2_1.pdb` `cluster3_1.pdb` `cluster4_1.pdb`
Executar validação

```
python validation.py ~/Downloads/haddock_results
```

### Saída esperada

```
============================================================
ANÁLISE DE RESULTADOS DO DOCKING
Encontrados 4 clusters:
cluster1_1.pdb
cluster2_1.pdb
cluster3_1.pdb
cluster4_1.pdb

Análise de interface:
cluster1_1.pdb:
Átomos E2A (resíduos ativos): 87
Átomos HPR (resíduos ativos): 76
Histidinas encontradas: 12

cluster2_1.pdb:
Átomos E2A (resíduos ativos): 87
Átomos HPR (resíduos ativos): 76
Histidinas encontradas: 12

cluster3_1.pdb:
Átomos E2A (resíduos ativos): 87
Átomos HPR (resíduos ativos): 76
Histidinas encontradas: 12

cluster4_1.pdb:
Átomos E2A (resíduos ativos): 85
Átomos HPR (resíduos ativos): 74
Histidinas encontradas: 12
============================================================
```


### Interpretação dos resultados

**Átomos em resíduos ativos:**
- Indica quantos átomos dos resíduos identificados por RMN estão presentes
- Valores consistentes entre clusters sugerem boa convergência
- Variações grandes podem indicar conformações muito diferentes

**Histidinas encontradas:**
- Total de histidinas no complexo (incluindo NEP fosforilada)
- Crítico para validar o mecanismo de transferência de fosfato
- His90 de E2A (NEP) deve estar próxima de histidina de HPR

**Análise complementar:**
- Use os resultados quantitativos junto com análise visual no PyMOL
- Compare com estrutura de referência usando script `03_compare_reference.pml`
- Verifique proximidade de histidinas usando script `04_analyze_histidines.pml`

---

## Requisitos

### Dependências Python

```
pip install numpy
```


**Bibliotecas utilizadas:**
- `urllib` (built-in) - Download de arquivos PDB do RCSB
- `pathlib` (built-in) - Manipulação moderna de caminhos de arquivos
- `shutil` (built-in) - Operações de cópia de arquivos
- `os` (built-in) - Operações do sistema operacional
- `numpy` - Cálculos numéricos e RMSD (apenas validation.py)

### Software Externo

**PyMOL** - Visualização molecular
- Download: https://pymol.org/
- Versão recomendada: 2.0 ou superior

**Acesso ao HADDOCK**
- Registro gratuito: https://alcazar.science.uu.nl/services/HADDOCK2.2/signup.html

---

## Fluxo de trabalho completo

### Passo 1: Preparar estruturas

```
python make.py
```

Aguarde a conclusão do download e processamento das estruturas.

### Passo 2: Visualizar estruturas

```
/pymol_scripts/01_visualize_e2a.pml
/pymol_scripts/02_visualize_hpr.pml
```

Inspecione as estruturas e resíduos ativos destacados.

### Passo 3: Submeter no HADDOCK

1. Acesse: https://alcazar.science.uu.nl/services/HADDOCK2.2/haddockserver-easy.html
2. Faça login com suas credenciais
3. Configure o job conforme documentado acima
4. Submeta e salve o arquivo `haddockparameter` fornecido

### Passo 4: Aguardar processamento

Tempo estimado: 30 minutos a várias horas.
Você receberá email quando os resultados estiverem prontos.

### Passo 5: Baixar resultados

Baixe os arquivos de clusters do servidor HADDOCK para um diretório local.

### Passo 6: Validar resultados

```
python validation.py ~/Downloads/haddock_results
```
> Lembradno que esse diretório de verificação é referente ao primeiro script de automatização usado no início, fique atento aos caminhos dos arquivos.


Analise as estatísticas geradas.

### Passo 7: Análise visual detalhada

```
/pymol_scripts/03_compare_reference.pml
```


No PyMOL, carregue os clusters:


```
load ~//haddock_results/cluster1_1.pdb
load ~/haddock_results/cluster2_1.pdb
align cluster1_1, ref_chain_a, cycles=0
align cluster2_1, ref_chain_a, cycles=0
```


Calcule RMSD:

```
rms_cur cluster1_1 and chain B, 1GGR and chain B
rms_cur cluster2_1 and chain B, 1GGR and chain B
```


### Passo 8: Validação biológica


Verifique se as histidinas críticas estão em proximidade adequada (3-5 Å) para transferência de fosfato.

---

## Solução de problemas

### Erro: ModuleNotFoundError: No module named 'numpy'

**Solução:**

```
pip install numpy
```


Se usar ambiente virtual:

```
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
pip install numpy
```


### Erro: Unable to download PDB

**Causas possíveis:**
- Sem conexão com internet
- Servidor RCSB temporariamente indisponível
- Firewall bloqueando acesso

**Solução:**
1. Verifique sua conexão com internet
2. Tente novamente após alguns minutos
3. Se persistir, baixe manualmente do RCSB: https://www.rcsb.org/

### Erro: No cluster files found

**Causas possíveis:**
- Caminho incorreto para diretório de resultados
- Arquivos não seguem padrão de nomenclatura esperado
- Resultados ainda não foram baixados do HADDOCK

**Solução:**
1. Verifique o caminho fornecido está correto
2. Certifique-se que os arquivos são nomeados `cluster*_1.pdb`
3. Confirme que baixou os resultados completos do HADDOCK

### PyMOL não abre os scripts

**Solução:**
- Abra o PyMOL primeiro
- Use menu: File → Run Script
- Ou na linha de comando do PyMOL: `@caminho/para/script.pml`

### Erro: Permission denied

**Solução Linux/Mac:**

```
chmod +x make.py
chmod +x validation.py
```


Ou execute com Python explicitamente:

```
python make.py
python validation.py
```


---

## Informações adicionais

### Resíduos ativos

Os resíduos ativos foram identificados experimentalmente por RMN através de perturbações de deslocamento químico:

**E2A (1F3G):**

```
38, 40, 45, 46, 69, 71, 78, 80, 94, 96, 141
```


**HPR (1HDN):**

```
15, 16, 17, 20, 48, 49, 51, 52, 54, 56
```


### Modificação His90 → NEP

A histidina 90 de E2A é modificada para NEP (fosfo-histidina) porque:
- Biologicamente, E2A transfere grupo fosfato para HPR
- NEP representa o estado fosforilado necessário para a catálise
- O grupo fosfato altera dramaticamente a eletrostática local
- Essencial para reproduzir corretamente o mecanismo de interação

### Critérios de qualidade CAPRI

Para avaliar qualidade dos modelos gerados:

| Qualidade | l-RMSD | Descrição |
|-----------|--------|-----------|
| Alta | < 1.0 Å | Predição de alta qualidade |
| Média | < 5.0 Å | Predição de qualidade média |
| Aceitável | < 10.0 Å | Predição aceitável |
| Incorreto | >= 10.0 Å | Predição incorreta |

l-RMSD = ligand-RMSD (calculado após alinhar receptores)

---

## Suporte e recursos

**Tutorial original HADDOCK:**
https://www.bonvinlab.org/education/HADDOCK-protein-protein-basic/

**Servidor HADDOCK:**
https://alcazar.science.uu.nl/services/HADDOCK2.2/

**Suporte HADDOCK:**
https://ask.bioexcel.eu/

**Documentação PyMOL:**
https://pymol.org/dokuwiki/

**RCSB Protein Data Bank:**
https://www.rcsb.org/

---

## Referências

1. van Zundert et al. (2016). The HADDOCK2.2 webserver: User-friendly integrative modeling of biomolecular complexes. J. Mol. Biol., 428, 720-725

2. de Vries et al. (2010). The HADDOCK web server for data-driven biomolecular docking. Nature Protocols, 5, 883-897

3. Wang et al. (2000). EMBO J.

---

**Desenvolvido para o tutorial HADDOCK de docking proteína-proteína**

Versão: 1.0  
Data: Outubro 2025  
Licença: Uso educacional







