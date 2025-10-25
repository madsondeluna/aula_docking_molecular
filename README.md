# Tutorial Completo de Docking Proteína-Proteína com HADDOCK

Este tutorial demonstra como prever a estrutura de um complexo proteína-proteína usando o servidor web HADDOCK2.2, utilizando dados experimentais de perturbação de deslocamento químico por RMN.

## Índice

- [Introdução](#introdução)
- [Requisitos e Configuração Inicial](#requisitos-e-configuração-inicial)
- [Passo 1: Inspecionar e Preparar a Proteína E2A](#passo-1-inspecionar-e-preparar-a-proteína-e2a)
- [Passo 2: Inspecionar e Preparar a Proteína HPR](#passo-2-inspecionar-e-preparar-a-proteína-hpr)
- [Passo 3: Adicionar Grupo Fosfato](#passo-3-adicionar-grupo-fosfato)
- [Passo 4: Configurar e Executar o Docking](#passo-4-configurar-e-executar-o-docking)
- [Passo 5: Analisar os Resultados](#passo-5-analisar-os-resultados)
- [Passo 6: Validação Biológica](#passo-6-validação-biológica)
- [Passo 7: Comparação com Estrutura de Referência](#passo-7-comparação-com-estrutura-de-referência)
- [Exercícios Adicionais](#exercícios-adicionais)
- [Referências](#referências)

---

## Introdução

O tutorial trabalha com duas proteínas de *Escherichia coli* envolvidas no transporte de glicose:

- **E2A**: Enzima IIA específica para glicose (PDB ID: 1F3G)
- **HPR**: Proteína transportadora de fosfato contendo histidina (PDB ID: 1HDN)

> **Contexto Biológico-Computacional**: O sistema fosfotransferase (PTS) de *E. coli* é responsável pelo transporte e fosforilação simultânea de carboidratos. Biologicamente, E2A e HPR interagem transitoriamente para transferir um grupo fosfato, um processo que ocorre em milissegundos. Computacionalmente, o docking molecular permite reconstruir essa interação transitória usando dados de RMN como restrições, traduzindo perturbações químicas observadas experimentalmente em distâncias espaciais que guiam a predição estrutural.

A estrutura do complexo nativo foi determinada por RMN (PDB ID: 1GGR) e será usada para validação dos resultados.

### Objetivo

Realizar docking molecular utilizando dados de perturbação química de RMN para guiar a predição da estrutura do complexo E2A-HPR.

## Requisitos e Configuração Inicial

### Software Necessário

- **PyMOL** (versão 2.0 ou superior)
- Navegador web moderno
- Conta no servidor HADDOCK2.2

### Registro no HADDOCK

Registre-se gratuitamente em: https://alcazar.science.uu.nl/services/HADDOCK2.2/signup.html

---

## Conceitos Fundamentais do HADDOCK

### O que é HADDOCK?

HADDOCK (*High Ambiguity Driven protein-protein DOCKing*) é um conjunto de scripts Python derivados do ARIA que utilizam o poder do CNS (*Crystallography and NMR System*) para cálculo de estruturas de complexos moleculares.

> **Contexto Biológico-Computacional**: Diferentemente de métodos de docking puramente baseados em forma e energia, HADDOCK incorpora conhecimento experimental. Biologicamente, sabemos que certas regiões da proteína são críticas para a interação (identificadas por mutagênese ou RMN). Computacionalmente, HADDOCK traduz essa informação biológica em "restrições de interação ambígua" (AIRs) que favorecem modelos onde essas regiões estão na interface, reduzindo drasticamente o espaço conformacional a ser explorado.

### Restrições de Interação Ambígua (AIRs)

As AIRs traduzem dados experimentais brutos em restrições de distância incorporadas na função de energia:

#### Tipos de Resíduos

| Tipo | Descrição | Penalidade |
|------|-----------|------------|
| **Ativos** | Resíduos de importância central (alta perturbação química) | Sim, se não estiverem na interface |
| **Passivos** | Resíduos contribuintes, menor importância | Não |

> **Contexto Biológico-Computacional**: Em experimentos de RMN, quando duas proteínas se associam, os resíduos na interface experimentam mudanças significativas no ambiente químico (perturbações de deslocamento químico). Biologicamente, resíduos com grandes perturbações estão diretamente envolvidos no reconhecimento molecular. Computacionalmente, classificamos esses como "ativos" (devem estar na interface) enquanto seus vizinhos espaciais são "passivos" (podem contribuir, mas não são obrigatórios), permitindo que o algoritmo explore soluções sem restrições excessivamente rígidas.

### Protocolo de Docking em Três Estágios

#### 1. Minimização de Corpo Rígido (it0)
- Proteínas tratadas como corpos rígidos
- Separação no espaço e rotação aleatória
- Minimização de energia de corpo rígido
- **Padrão**: 1000 modelos gerados

> **Contexto Biológico-Computacional**: Biologicamente, proteínas em solução exploram múltiplas orientações antes de encontrar a conformação de ligação correta. Computacionalmente, esta etapa simula essa busca orientacional através de múltiplas rotações aleatórias, mas mantém a estrutura de cada proteína rígida (assumindo que as mudanças conformacionais principais ocorrem após o reconhecimento inicial). As AIRs guiam essa busca, priorizando orientações que aproximam as regiões identificadas experimentalmente.

#### 2. Recozimento Simulado Semi-Flexível (it1)
- Introdução de flexibilidade na interface
- Dinâmica molecular em espaço de ângulos de torção
- Otimização de cadeias laterais e backbone
- **Padrão**: 200 melhores modelos refinados

> **Contexto Biológico-Computacional**: Biologicamente, após o reconhecimento inicial, proteínas sofrem ajustes conformacionais ("induced fit") para otimizar complementaridade. Resíduos de interface reorganizam suas cadeias laterais e, às vezes, o backbone local se ajusta. Computacionalmente, esta etapa permite essas mudanças através de dinâmica molecular restrita ao espaço de torção (mais eficiente que cartesiano), simulando o processo de ajuste fino que otimiza interações específicas como pontes de hidrogênio e contatos hidrofóbicos.

#### 3. Refinamento em Solvente Explícito (water)
- Imersão do complexo em água (modelo TIP3P)
- Simulação de dinâmica molecular a 300K
- Otimização final das energéticas
- **Padrão**: 200 modelos refinados

> **Contexto Biológico-Computacional**: Biologicamente, interações proteína-proteína ocorrem em ambiente aquoso, onde moléculas de água podem mediar contatos ou ser excluídas de superfícies hidrofóbicas (efeito hidrofóbico). Computacionalmente, adicionar solvente explícito melhora a descrição das interações eletrostáticas (screening dielétrico) e permite avaliar corretamente o custo energético de desolvatação, fornecendo energias de ligação mais realistas e identificando possíveis pontes de água na interface.

## Passo 1: Inspecionar e Preparar a Proteína E2A

### 1.1 Carregar e Visualizar a Estrutura

Abra o PyMOL e execute:

```
fetch 1F3G
show cartoon
hide lines
show sticks, resn HIS
```


**Questão**: Existem grupos fosfato presentes nesta estrutura?

> **Contexto Biológico-Computacional**: Biologicamente, E2A existe em duas formas: fosforilada (ativa) e desfosforilada. A estrutura cristalográfica 1F3G foi obtida sem o grupo fosfato. Para simular computacionalmente a transferência de fosfato (função biológica do complexo), precisamos adicionar este grupo modificando o resíduo His90, criando uma representação mais fiel do estado funcional da proteína durante a interação.

### 1.2 Remover Moléculas de Água

```
remove resn HOH
```


**Nota**: Sempre remova águas irrelevantes, mas mantenha cofatores importantes.

> **Contexto Biológico-Computacional**: Estruturas cristalográficas contêm moléculas de água que podem ser artefatos da cristalização ou águas estruturais essenciais. Biologicamente, apenas águas estruturais (firmemente ligadas) são relevantes para a interação. Computacionalmente, removemos águas cristalográficas porque o HADDOCK adicionará solvente explícito no refinamento final, permitindo que o programa identifique quais posições de água são energeticamente favoráveis na interface do complexo.

### 1.3 Visualizar Resíduos da Interface

**Resíduos ativos de E2A** (com perturbações químicas significativas):

```
38, 40, 45, 46, 69, 71, 78, 80, 94, 96, 141
```

Seguido de: 

```
color white, all
show surface
select e2a_active, (resi 38,40,45,46,69,71,78,80,94,96,141)
color red, e2a_active
```


**Questão**: Os resíduos identificados formam uma superfície contígua?

> **Contexto Biológico-Computacional**: Biologicamente, sítios de ligação proteína-proteína geralmente formam patches contínuos na superfície, otimizados evolutivamente para reconhecimento específico. Os dados de RMN identificam resíduos com grandes perturbações, mas podem "pular" alguns resíduos intermediários (pequenas perturbações ou dinâmica local). Computacionalmente, o HADDOCK define automaticamente resíduos "passivos" (vizinhos espaciais dos ativos) para preencher essas lacunas, criando uma superfície de interação mais realista sem exigir que todos os resíduos da interface mostrem perturbações detectáveis experimentalmente.

### 1.4 Salvar o Arquivo

No menu do PyMOL:
1. `File → Save molecule…`
2. Selecione `1F3G`
3. Salve como: **`e2a_1F3G.pdb`**

## Passo 2: Inspecionar e Preparar a Proteína HPR

### 2.1 Carregar a Estrutura de RMN

```
fetch 1HDN
show cartoon
hide lines
```


**Nota**: Estruturas de RMN não contêm moléculas de água.

> **Contexto Biológico-Computacional**: RMN determina estruturas em solução, mais próximas das condições fisiológicas que cristalografia. Biologicamente, HPR é uma proteína pequena e flexível que existe como ensemble de conformações em equilíbrio. Computacionalmente, estruturas de RMN fornecem múltiplos confôrmeros representando essa heterogeneidade conformacional, oferecendo vantagem no docking ao explorar múltiplos estados pré-organizados que podem favorecer a ligação (seleção conformacional vs induced fit).

### 2.2 Visualizar Resíduos Ativos

**Resíduos ativos de HPR**:

```
15, 16, 17, 20, 48, 49, 51, 52, 54, 56
```

Seguido de:

```
color white, all
show surface
select hpr_active, (resi 15,16,17,20,48,49,51,52,54,56)
color red, hpr_active
```


### 2.3 Explorar o Ensemble de RMN

Esta estrutura contém **30 confôrmeros** que representam a flexibilidade conformacional.

```
hide all
show ribbon
set all_states, on
```


#### Visualizar Cadeias Laterais dos Resíduos Ativos

```
show sticks, hpr_active
```


> **Contexto Biológico-Computacional**: Biologicamente, cadeias laterais de superfície são altamente dinâmicas, amostrando múltiplas rotâmeros em escalas de tempo de nano a microsegundos. Essa flexibilidade é crítica para reconhecimento molecular (permite adaptação ao parceiro). Computacionalmente, usar um ensemble de RMN captura essa flexibilidade pré-existente, aumentando chances de incluir uma conformação favorável para ligação. Porém, devemos limitar o número de confôrmeros para evitar explosão combinatória que tornaria a amostragem estatisticamente insuficiente.

**Importante**: Limite o número de confôrmeros para evitar explosão combinatória:
- 10 confôrmeros × 10 confôrmeros = 100 combinações iniciais
- Com 1000 modelos, cada combinação é amostrada apenas 10 vezes

### 2.4 Salvar o Ensemble

1. `File → Save molecule…`
2. Selecione `1HDN`
3. Salve como: **`hpr-ensemble.pdb`**

## Passo 3: Adicionar Grupo Fosfato

### 3.1 Contexto Biológico

A função biológica deste complexo é **transferir um grupo fosfato** da histidina 90 de E2A para uma histidina de HPR.

> **Contexto Biológico-Computacional**: Biologicamente, o sistema PTS realiza fosforilação em cascata: PEP → Enzyme I → HPR → E2A → glicose. A transferência de fosfato ocorre através de mecanismo SN2 em linha, exigindo que o nitrogênio aceptor da histidina de HPR esteja posicionado próximo (~3Å) e alinhado com o fósforo da fosfo-histidina de E2A. Computacionalmente, incluir o grupo fosfato é essencial porque: (1) altera dramaticamente a eletrostática local, afetando as interações; (2) fornece validação geométrica clara - modelos corretos devem posicionar as histidinas apropriadamente para catálise.

### 3.2 Aminoácidos Modificados no HADDOCK

Lista completa: https://alcazar.science.uu.nl/services/HADDOCK2.2/library.html

**Nome do resíduo para fosfo-histidina**: `NEP`

### 3.3 Modificar o Arquivo PDB

**Procedimento**:

1. Abra **`e2a_1F3G.pdb`** em um editor de texto
2. Localize todas as linhas contendo `HIS` e residue number `90`
3. Substitua `HIS` por `NEP` apenas para o resíduo 90
4. Salve como: **`e2aP_1F3G.pdb`**

**Exemplo de edição**:

```
Antes: ATOM 1234 CA HIS A 90 12.345 23.456 34.567 1.00 20.00
Depois: ATOM 1234 CA NEP A 90 12.345 23.456 34.567 1.00 20.00
```


**Dica**: O HADDOCK automaticamente adiciona/remove átomos necessários para o grupo fosfato.

> **Contexto Biológico-Computacional**: Modificações pós-traducionais (como fosforilação) são cruciais biologicamente mas não são padrão em arquivos PDB. HADDOCK possui uma biblioteca de resíduos modificados com topologias e parâmetros pré-calculados. Computacionalmente, ao mudar o nome do resíduo, o programa reconhece o código NEP, busca a topologia correta, adiciona os átomos do grupo fosfato (PO3²⁻) na geometria adequada, e aplica cargas parciais apropriadas. Isso automatiza um processo que manualmente exigiria construção cuidadosa da geometria e parametrização.

## Passo 4: Configurar e Executar o Docking

### 4.1 Acessar o Servidor

URL: https://alcazar.science.uu.nl/services/HADDOCK2.2/haddockserver-easy.html

### 4.2 Configuração Passo a Passo

#### Passo 1: Nome da Execução

```
Job name: E2A-HPR
```


#### Passo 2: Primeira Molécula (E2A)

Expanda o menu **"First Molecule"**:

| Campo | Valor |
|-------|-------|
| Where is the structure provided? | `I am submitting it` |
| Which chain to be used? | `All` |
| PDB structure to submit | `e2aP_1F3G.pdb` |
| Active residues | `38,40,45,46,69,71,78,80,94,96,141` |
| Define passive residues automatically | Marcar |

#### Passo 3: Segunda Molécula (HPR)

Expanda o menu **"Second Molecule"**:

| Campo | Valor |
|-------|-------|
| Where is the structure provided? | `I am submitting it` |
| Which chain to be used? | `All` |
| PDB structure to submit | `hpr-ensemble.pdb` |
| Active residues | `15,16,17,20,48,49,51,52,54,56` |
| Define passive residues automatically | Marcar |

> **Contexto Biológico-Computacional**: Biologicamente, o reconhecimento proteína-proteína envolve um "código de ligação" onde resíduos específicos (hot spots) contribuem desproporcionalmente para afinidade e especificidade. Dados de RMN identificam esses hot spots através de perturbações químicas. Computacionalmente, ao definir resíduos ativos, instruímos o algoritmo a penalizar modelos onde esses resíduos críticos não estão na interface, focando a busca em soluções consistentes com dados experimentais. A definição automática de passivos cria uma "zona de tolerância" ao redor dos hot spots, permitindo flexibilidade sem perder o direcionamento experimental.

#### Passo 4: Submeter

1. Insira suas credenciais de login
2. Clique em **Submit**
3. **IMPORTANTE**: Salve o arquivo **`haddockparameter`** fornecido

> **Contexto Biológico-Computacional**: Reprodutibilidade é fundamental na ciência. O arquivo haddockparameter documenta todos os parâmetros computacionais usados, permitindo reprodução exata da simulação. Isso é o equivalente computacional de documentar condições experimentais (pH, temperatura, concentrações) em experimentos bioquímicos.

### 4.3 Tempo de Processamento

- **Mínimo**: 30 minutos
- **Máximo**: Várias horas (depende da carga do servidor)
- Notificação por email quando concluir

## Passo 5: Analisar os Resultados

### 5.1 Sistema de Pontuação HADDOCK

A fórmula do HADDOCK score é:

```
HADDOCKscore = 1.0 × Evdw + 0.2 × Eelec + 1.0 × Edesol + 0.1 × Eair
```


**Componentes**:
- `Evdw`: Energia van der Waals intermolecular
- `Eelec`: Energia eletrostática intermolecular
- `Edesol`: Termo empírico de dessolvatação
- `Eair`: Energia das restrições AIR

> **Contexto Biológico-Computacional**: Biologicamente, a afinidade de ligação resulta de múltiplas forças: empacotamento hidrofóbico (van der Waals), interações eletrostáticas (pontes salinas, dipolo-dipolo), e efeito hidrofóbico (dessolvatação). Computacionalmente, o HADDOCK score aproxima a energia livre de ligação combinando esses termos. Os pesos (1.0, 0.2, 1.0, 0.1) foram otimizados empiricamente em benchmarks. Van der Waals e dessolvatação têm peso maior porque dominam a maioria das interfaces proteína-proteína. Eair recebe peso baixo para não sobreditar dados experimentais (que têm incertezas).

### 5.2 Análise de Clusters

**Ranking**: Baseado no score médio dos **4 melhores membros** de cada cluster.

**Questão**: O cluster top-ranked é significativamente melhor que o segundo?
- Compare scores e desvios padrão
- Analise o z-score
- Clusters com scores dentro do desvio padrão devem ser considerados válidos

> **Contexto Biológico-Computacional**: Biologicamente, complexos proteína-proteína podem ter múltiplos modos de ligação (especialmente interações transitórias ou multiespecíficas). Estatisticamente, o agrupamento (clustering) identifica bacias de energia no panorama conformacional. Clusters populosos geralmente representam mínimos mais robustos. Porém, devemos considerar múltiplos clusters se energias forem similares (dentro do erro computacional), especialmente porque o "modo correto" pode não ser o mais estável energeticamente se a transferência de fosfato ocorre através de um estado transitório.

### 5.3 Visualizar Clusters no PyMOL

#### Baixar Modelos
Baixe o primeiro modelo de cada cluster:
- `cluster1_1.pdb`
- `cluster2_1.pdb`
- `cluster3_1.pdb`
- etc.

#### Carregar e Visualizar

Carregar todos os clusters
File → Open → cluster1_1.pdb
File → Open → cluster2_1.pdb
File → Open → cluster3_1.pdb

Configurar visualização

```
show cartoon
util.cbc
hide lines
```

#### Sobrepor na Cadeia A (E2A)

```
select cluster1_1 and chain A
align cluster2_1, sele
align cluster3_1, sele
align cluster4_1, sele
```


> **Contexto Biológico-Computacional**: Sobreposição baseada no receptor (E2A) permite comparar as diferentes orientações do ligante (HPR). Biologicamente, E2A é maior e mais rígida, enquanto HPR é menor e mais dinâmica, consistente com o modelo de "chave e fechadura" modificado. Computacionalmente, alinhar pelo receptor isola as diferenças nas poses do ligante, facilitando identificação de consenso ou divergências entre soluções.

### 5.4 Verificar Resíduos Ativos na Interface

```
select e2a_active, (resi 38,40,45,46,69,71,78,80,94,96,141) and chain A
select hpr_active, (resi 15,16,17,20,48,49,51,52,54,56) and chain B
color red, e2a_active
color orange, hpr_active
```

**Questão**: Os resíduos ativos estão na interface do complexo?

## Passo 6: Validação Biológica

### 6.1 Mecanismo de Transferência de Fosfato

O grupo fosfato deve ser transferido da **histidina 90 de E2A** (NEP) para uma **histidina de HPR**. Portanto, estas duas histidinas devem estar em **proximidade espacial** (~3-5 Å).

> **Contexto Biológico-Computacional**: A transferência de fosfato via mecanismo SN2 tem requisitos estereoquímicos estritos: (1) distância N-P de ~3-3.5Å no estado de transição; (2) ângulo de ataque próximo a 180° (inversão de Walden); (3) orientação do lone pair do nitrogênio aceptor alinhado com o orbital σ* P-O. Computacionalmente, modelos de docking que não satisfazem essas restrições geométricas são biologicamente irrelevantes, independente de terem boa energia. Esta validação mecânica é mais informativa que scores energéticos para sistemas envolvendo catálise.

### 6.2 Visualizar Histidinas

```
select histidines, resn HIS+NEP
show spheres, histidines
util.cnc
```


### 6.3 Análise Cluster por Cluster

Para cada cluster:
1. Ative apenas um cluster (clique no nome no painel esquerdo)
2. Verifique a distância entre His90 de E2A e histidinas de HPR
3. Identifique qual cluster satisfaz melhor a informação biológica

**Questão crítica**: Qual cluster mostra histidinas em proximidade adequada para transferência de fosfato?

## Passo 7: Comparação com Estrutura de Referência

### 7.1 Carregar Estrutura Nativa (PDB: 1GGR)

```
fetch 1GGR
show cartoon
color yellow, 1GGR and chain A
color orange, 1GGR and chain B
```


> **Contexto Biológico-Computacional**: A estrutura 1GGR foi determinada por RMN usando NOEs intermoleculares (distâncias <6Å entre prótons de moléculas diferentes) e acoplamentos dipolares residuais (orientação relativa). Biologicamente, representa o complexo funcional em solução. Computacionalmente, serve como "gabarito" para avaliar sucesso do docking cego (sem conhecimento da estrutura do complexo). É importante notar que complexos transitórios como este podem ter alguma heterogeneidade estrutural, então RMSD muito baixo (<1Å) pode não ser esperado.

### 7.2 Corrigir Numeração da Cadeia B

A numeração da cadeia B em 1GGR começa em 301, mas nos nossos modelos começa em 1:

```
alter (chain B and 1GGR), resv -= 300
```


### 7.3 Sobrepor Modelos à Estrutura de Referência

```
select 1GGR and chain A
align cluster1_1, sele, cycles=0
align cluster2_1, sele, cycles=0
align cluster3_1, sele, cycles=0
```


### 7.4 Calcular Ligand-RMSD (l-RMSD)

Para cada cluster:

```
rms_cur cluster1_1 and chain B, 1GGR and chain B
rms_cur cluster2_1 and chain B, 1GGR and chain B
rms_cur cluster3_1 and chain B, 1GGR and chain B
```


> **Contexto Biológico-Computacional**: O ligand-RMSD (l-RMSD) mede a qualidade da predição isolando erros na pose do ligante (após alinhar receptores). Biologicamente, captura quão bem o método reproduziu o modo de ligação observado experimentalmente. Computacionalmente, é mais informativo que RMSD global (que poderia ser baixo mesmo com pose incorreta se as proteínas individuais forem bem preservadas). No contexto CAPRI (Critical Assessment of PRedicted Interactions), l-RMSD tornou-se o padrão para avaliar métodos de docking.

### 7.5 Critérios de Qualidade CAPRI

| Qualidade | l-RMSD | Descrição |
|-----------|--------|-----------|
| Alta | < 1.0 Å | Modelo de alta qualidade |
| Média | < 5.0 Å | Modelo de qualidade média |
| Aceitável | < 10.0 Å | Modelo aceitável |
| Incorreto | ≥ 10.0 Å | Modelo incorreto |

**Questão final**: Qual é a qualidade do melhor modelo baseado nos critérios CAPRI?

## Exercícios Adicionais

Para aprofundar seu conhecimento sobre o impacto dos dados de entrada:

### Exercício 1: Sem Fosfo-Histidina
Execute o docking usando **`e2a_1F3G.pdb`** (sem modificação) em vez de `e2aP_1F3G.pdb`.

**Objetivos**:
- Comparar scores dos clusters
- Avaliar impacto na orientação das proteínas
- Verificar se a ausência do fosfato afeta a qualidade dos modelos

> **Contexto Biológico-Computacional**: O grupo fosfato carrega duas cargas negativas, alterando dramaticamente a eletrostática local. Biologicamente, HPR reconhece tanto a forma fosforilada quanto desfosforilada de E2A, mas com afinidades diferentes. Computacionalmente, este exercício testa se as restrições de RMN sozinhas são suficientes para reproduzir o complexo, ou se as interações eletrostáticas do fosfato são críticas para direcionar a orientação correta. Comparar resultados revela a importância relativa de diferentes forças direcionadoras.

### Exercício 2: Único Confôrmero
Use apenas o primeiro modelo do ensemble de HPR.

**Procedimento**:
1. Abra `hpr-ensemble.pdb` em editor de texto
2. Extraia apenas o Model 1
3. Salve como `hpr-single.pdb`
4. Execute novo docking

**Objetivos**:
- Avaliar benefício do ensemble conformacional
- Comparar diversidade dos resultados
- Analisar scores finais

> **Contexto Biológico-Computacional**: Este exercício testa a hipótese de seleção conformacional vs induced fit. Biologicamente, se HPR pré-existe em múltiplas conformações e a ligação seleciona a apropriada (seleção conformacional), usar o ensemble deve melhorar resultados. Se a conformação de ligação não está representada no ensemble livre (induced fit completo), o ensemble pode não ajudar. Computacionalmente, comparar performance quantifica a contribuição da flexibilidade pré-existente vs flexibilidade durante o docking (it1) para o sucesso da predição.

---

## Dicas Importantes

### Boas Práticas

- Sempre salve o arquivo **`haddockparameter`** após submissão
- Considere múltiplos clusters se scores estiverem dentro do desvio padrão
- Use informações biológicas adicionais para validação
- Limite confôrmeros em ensembles de RMN (máximo 10)
- Documente todas as modificações nos arquivos PDB

### Cuidados

- Não use todos os 30 confôrmeros do ensemble (explosão combinatória)
- Verifique sempre a numeração de resíduos entre estruturas
- Valide modificações de aminoácidos com cuidado
- Não confie apenas no ranking - valide biologicamente

## Referências

### Publicações Principais

1. **van Zundert et al. (2016)**  
   *The HADDOCK2.2 webserver: User-friendly integrative modeling of biomolecular complexes*  
   J. Mol. Biol., 428, 720-725

2. **de Vries et al. (2010)**  
   *The HADDOCK web server for data-driven biomolecular docking*  
   Nature Protocols, 5, 883-897

3. **Wang et al. (2000)**  
   EMBO J.

### Recursos Online

- **HADDOCK Web Server**: https://alcazar.science.uu.nl/services/HADDOCK2.2/
- **Tutorial Original**: https://www.bonvinlab.org/education/HADDOCK-protein-protein-basic/
- **Bonvin Lab**: https://www.bonvinlab.org/
- **Mais Tutoriais**: https://www.bonvinlab.org/education/

---

## Suporte

Tem dúvidas ou sugestões?

- Email: madsondeluna@gmail.com
- Website: [https://www.bonvinlab.org/](https://madsondeluna.github.io/)

---

## Licença

Este tutorial foi adaptado do material educacional do Bonvin Lab (Utrecht University), e foi disponibilizado para fins educacionais.

---

**Última atualização**: Outubro 2025  
**Versão**: 1.0  
**Material Original**: Bonvin Lab - Utrecht University


