from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('GLOP')

N = int(input())
A = [[float(input()) for j in range(N)] for i in range(N)]

# Variaveis de decisão
# X = [[solver.NumVar(0, 1, f'X{i}{j}') for j in range(N)] for i in range(N)]
# boolvar é uma sintaxe similar mas não precisa dos parâmetros de limite pq já é bool
X = [[solver.BoolVar(f'X{i}{j}') for j in range(N)] for i in range(N)]

id_restricao = 0

# Restrição: Cada linha deve somar 1
for i in range(N):
    ct = solver.Constraint(1, 1, str(id_restricao))
    id_restricao =+ 1
    for j in range(N):
        ct.SetCoefficient(X[i][j], 1)

# Restrição: Cada coluna deve somar 1
for j in range(N):
    ct = solver.Constraint(1, 1, str(id_restricao))
    id_restricao =+ 1
    for i in range(N):
        ct.SetCoefficient(X[i][j], 1)

# Função objetivo
objective = solver.Objective()
for i in range(N):
    for j in range(N):
        objective.SetCoefficient(X[i][j], A[i][j])
objective.SetMaximization()

# Resultado
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    print('Solucao:')
    print('Valor objetivo =', "{:.1f}".format(solver.Objective().Value()))
    for i in range(N):
        for j in range(0, N):
            print(f'X{i}{j} =', "{:.1f}".format(X[i][j].solution_value()))
else:
    print('O problema não possui solução ótima')
