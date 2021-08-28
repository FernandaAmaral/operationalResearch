from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('GLOP')

N = int(input())  # Number of nodes
S = int(input())  # Source
T = int(input())  # Target

# Matriz de conexão
Aij =[[float(input()) for j in range(N)] for i in range(N)]

# Variáveis de decisão
X = [[solver.NumVar(0, 1, f'X{i}{j}') for j in range(N)] for i in range(N)]

# Restrições
for i in range(N):
    if i == S:
        ct = solver.Constraint(1, 1, 'source')
    elif i == T:
        ct = solver.Constraint(-1, -1, 'target')
    else:
        ct = solver.Constraint(0, 0, str(i))
    for j in range(N):
        ct.SetCoefficient(X[i][j], 1)
        ct.SetCoefficient(X[j][i], -1)

# Função objetivo
objective = solver.Objective()
for i in range(N):
    for j in range(N):
        objective.SetCoefficient(X[i][j], Aij[i][j])
objective.SetMinimization()

# Resultado
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    print('Solucao:')
    print('Valor objetivo =', "{:.1f}".format(solver.Objective().Value()))
    for i in range(N):
        for j in range(0, N):
            print(f'X{i}{j} =', "{:.1f}".format(abs(X[i][j].solution_value())))
else:
    print('O problema não possui solução ótima')