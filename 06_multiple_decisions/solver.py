from ortools.linear_solver import pywraplp
solver = pywraplp.Solver("MixedLinearProgramming", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)


############################## Variáveis do problema ##############################

N = int(input())  # Number of nodes
T = int(input())  # Number of temporal steps
L = int(input())  # Max node latency
C = int(input())  # Max load supported by a controller

# Update matrix
Xtn=[[int(input()) for n in range(0, N)] for t in range(0, T)]

# Latency matrix
Lnm=[[int(input()) for m in range(0, N)] for n in range(0, N)]

# Load vector
Kn=[int(input()) for n in range(0, N)]


############################## Variáveis de decisão ##############################

# Matriz temporal de posicionamento entre os controladores
Ytn = [[solver.BoolVar(f'Y{t}{n}') for n in range(N)] for t in range(T)]

# Matriz de conexão entre controladores e switches
Ztnm = [[[solver.BoolVar(f'Z{t}{n}{m}') for m in range(N)] for n in range(N)] for t in range(T)]


############################## Restrições ##############################

# O controlador precisa ser executado em novo hardware ou virtualizado
# em hardware existente
for n in range(N):
    for t in range(T):
        ct = solver.Constraint(0, Xtn[t][n], f'Y{t}{n} <= X{t}{n}')
        ct.SetCoefficient(Ytn[t][n], 1)

# A latência entre os controladores e os switches deve ficar abaixo do limite L
for n in range(N):
    for m in range(N):
        for t in range(T):
            ct = solver.Constraint(0, L, f'Z{t}{n}{m} <= {L}')
            ct.SetCoefficient(Ztnm[t][n][m], Lnm[n][m])

# Um switch só pode ser associado a um controlador por tempo
for t in range(T):
    for m in range(N):
        ct = solver.Constraint(Xtn[t][m], Xtn[t][m], f'sum(Z{t}n{m}) = X{t}{m}')
        for n in range(N):
            ct.SetCoefficient(Ztnm[t][n][m], 1)

# Demanda máxima por controlador deve ser C
for t in range(T):
    for n in range(N):
        ct = solver.Constraint(0, C, f'sum(Z{t}{n}m * Km) <= {C}')
        for m in range(N):
            ct.SetCoefficient(Ztnm[t][n][m], Kn[m])

# Controlador deve permanecer no mesmo nodo após a instalação
for t in range(T  - 1):
    for n in range(N):
        ct = solver.Constraint(-1, 0, f'-1 <= Y{t}{n} - Y{t+1}{n} <= 0')
        ct.SetCoefficient(Ytn[t][n], 1)
        ct.SetCoefficient(Ytn[t+1][n], -1)

# Ligação entre controlador e switch só pode acontecer caso o controlador esteja
# instalado em um dos nodos associados
for t in range(T):
    for n in range(N):
        for m in range(N):
            ct = solver.Constraint(0, solver.infinity(), f'Y{t}{n} - Z{t}{n}{m} >= 0')
            ct.SetCoefficient(Ytn[t][n], 1)
            ct.SetCoefficient(Ztnm[t][n][m], -1)

# O switch hospedeiro sempre será controlado pelo controlador hospedado
for t in range(T):
    for n in range(N):
        ct = solver.Constraint(0, 0, f'Y{t}{n} - Z{t}{n}{n} = 0')
        ct.SetCoefficient(Ytn[t][n], 1)
        ct.SetCoefficient(Ztnm[t][n][n], -1)


############################## Função Objetivo ##############################

objective = solver.Objective()
for t in range(T):
    for n in range(N):
        objective.SetCoefficient(Ytn[t][n], 1)
objective.SetMinimization()


############################## Resultado ##############################
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solucao:')

    print('Localizacao dos controladores:')
    for t in range(T):
        for n in range(N):
            print(Ytn[t][n].solution_value(), end=" ")
        print()

    print('Associacao switch-controlador:')
    for t in range(T):
        print(f"Periodo {t + 1}")
        for n in range(N):
            if Ytn[t][n].solution_value():
                print(f"Controlador: [ {n} ]")
                for m in range(N):
                    if Ztnm[t][n][m].solution_value():
                        print(f"Z[ {m} ] Latencia = {Lnm[n][m]}")
        print()

    print("Carga do controlador:")
    for t in range(T):
        for n in range(N):
            if Ytn[t][n].solution_value():
                carga = [Ztnm[t][n][m].solution_value() * Kn[m] for m in range(N)]
                print(f"periodo {t + 1} controlador {n} = {int(sum(carga))}")
