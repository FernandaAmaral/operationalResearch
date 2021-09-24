# Distribuição de postos drive thru para vacinação de COVID no DF

O presente trabalho é uma adaptação do problema descrito no paper "*Alocação Múltipla de Cópias de Arquivos: Uma adaptação para o problema de distribuição de vacinas no Distrito Federal*" apresentado no [WPOS/WCOMP](http://wpos.unb.br) 2021.

O problema se resume à determinação das Regiões Administrativas (RAs) do DF que receberão postos de vacinação drive thru com base nas divisas entre as RAs, representadas como os vértices e arestas de um grafo. Na modelagem, é necessário validar se um determinado conjunto de bairros satisfaz uma constante K para criar postos de aplicação levando em conta o valor do aluguel de cada bairro e a quantidade de pessoas com veículo automotor, representando o custo de armazenamento e o uso respectivamente.

Foi feita uma adaptação da modelagem original do artigo para transformá-la em um sistema de otimização e satisfazer os requisitos de solução de problemas lineares apresentados na disciplina de *Pesquisa Operacional* do Departamento de Ciência da Computação, UnB.

## Modelagem proposta


### Variável alvo

Dado um conjunto de regiões administrativas (*N*), determinar a quantidade de doses de vacina alocadas para cada região ($X_i, i\epsilon N$) dentre o total de doses disponíveis no DF (*n_doses*).

Cada posto drive thru tem uma capacidade máxima de vacinação (*cap_max*) e uma capacidade mínima para justificar a existência do posto naquela RA (*cap_min*).

O limite de doses a ser disponibilizado para cada RA é determinado pela quantidade de pessoas aptas a se vacinar na RA ( $qtde\_vacinantes = V_i * qtde\_pessoas\_por\_carro$ ), considerando a média de pessoas vacinantes por carro. Isso implica que pode não haver posto de vacinação por drive-thru para RAs com poucos carros (nestes locais, a alternativa seria somente os postos de vacinação para pedestres).

### Restrições

1. O limite de doses distribuídas é determinado pela quantidade disponível no DF


$$ \sum_{i=0}^{N} X_{i} \leq doses$$

2. Toda região administrativa deve estar até uma distância máxima (em Km) de um posto drive thru.

Dada uma matriz booleana $dist_{ij}$ que indica se uma RA *i* é vizinha da outra *j* ou não, temos que:


$$\sum_{N}^{j = 0} X_{j} dist_{ij} \geq min\_doses, \forall i\epsilon N$$


### Modelagem Final

Temos então a variável alvo, quantidade de doses de vacina alocadas para cada região:
$$X_i, i\epsilon N$$
com  $ 0 \leq  X_i \leq min(cap\_max, qtde\_vacinantes)$

Com o objetivo de maximizar a quantidade de doses distribuídas:
$$max(\sum_{i=0}^{N}Xi)$$

Sujeito a:

$$ \sum_{i=0}^{N} X_{i} \leq doses$$
$$\sum_{N}^{j = 0} X_{j} dist_{ij} \geq min\_doses, \forall i\epsilon N$$


## Implementação

Uma implementação da modelagem proposta foi feita e disponibilizada no seguinte [repositório]() do github. O projeto possui os seguintes arquivos:

- **solver.ipynb**: Jupyter notebook com a solução
- **calc_dist.py**: Script python que calcula a distância entre as RAs utilizando a biblioteca geopy
- **distances.csv**: Arquivo *csv* que contém a distância entre as RAs
- **RA.csv**: Arquivo *csv* que contém os dados das RAs

Foram utilizadas as seguintes variáveis:

- Capacidade min de atendimento de cada drive thru: **cap_min = 10000**
- Capacidade max de atendimento de cada drive thru: **cap_max = 18000**
- Número de doses de vacina disponíveis: **doses = 200000**
- Quantidade média de pessoas vacinadas por carro: **qtde_pessoas = 2**
- Distância máxima entre dois postos drive thru (Km): **dist_max = 15**

Além disso, os seguintes dados foram extraídos:

- Quantidade de veiculos por RA: Extraído do relatório de [*Pesquisa Distrital por Amostra de Domicílios*](https://www.codeplan.df.gov.br/pdad-2018/) do CODEPLAN, *Companhia de Planejamento do Distrito Federal*. Ano de referência: 2018
- Geocoordenadas (latitude e longitude) de cada RA: Google Maps
- Distância entre as RAs: Estimativa feita por meio da biblioteca geopy

Infelizmente, a restrição de distância torna o problema em um sistema sem solução. Removendo a restrição, foram obtidas as seguintes quantidades de vacina por RA:

```
Plano Piloto: 18000.0 vacinas
Gama: 18000.0 vacinas
Taguatinga: 18000.0 vacinas
Brazlândia: 17596.0 vacinas
Sobradinho: 18000.0 vacinas
Planaltina: 18000.0 vacinas
Paranoá: 16546.0 vacinas
Núcleo Bandeirante: 10258.0 vacinas
Ceilândia: 18000.0 vacinas
Guará: 18000.0 vacinas
Cruzeiro: 18000.0 vacinas
Samambaia: 11600.0 vacinas
```



