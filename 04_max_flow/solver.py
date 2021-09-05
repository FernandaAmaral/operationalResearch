from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('GLOP')

N = int(input())  # Number of nodes
S = int(input())  # Source
T = int(input())  # Target

# Matriz de capacidade máxima
C =[[float(input()) for j in range(N)] for i in range(N)]
C[T][S] = solver.infinity()

# Variáveis de decisão
X = [[solver.NumVar(0, C[i][j], f'X{i}{j}') for j in range(N)] for i in range(N)]

# Restrições
for i in range(N):
    ct = solver.Constraint(0, 0, str(i))
    for j in range(N):
        if i != S and i != T:
            ct.SetCoefficient(X[i][j], 1)
            ct.SetCoefficient(X[j][i], -1)

# Restrição origem
ct = solver.Constraint(0, 0, 'source')
for j in range(N):
    ct.SetCoefficient(X[S][j], 1)
ct.SetCoefficient(X[T][S], -1)

# Restrição target
ct = solver.Constraint(0, 0, 'target')
for i in range(N):
    ct.SetCoefficient(X[i][T], -1)
ct.SetCoefficient(X[T][S], 1)

# Função objetivo
objective = solver.Objective()
objective.SetCoefficient(X[T][S], 1)
objective.SetMaximization()

# Resultado
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    print(f'Valor objetivo = {solver.Objective().Value()}')
    for i in range(N):
        for j in range(0, N):
            if X[i][j].solution_value() != 0:
                if i == T and j == S:
                    print(f"X[T,S]={'{:.2f}'.format(X[i][j].solution_value())} de MAX_CAP: -1.00")
                else:   
                    print(f"X[{i},{j}]={'{:.2f}'.format(X[i][j].solution_value())} de MAX_CAP: {'{:.2f}'.format(C[i][j])}")
else:
    print('O problema não possui solução ótima')
