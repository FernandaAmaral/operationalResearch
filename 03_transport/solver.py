from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('GLOP')

M = int(input())  # Number of farms
N = int(input())  # Number of warehouses

# Transport matrix
Aij =[[float(input()) for j in range(N)] for i in range(M)]

# Production vector
Pi = [float(input()) for i in range(M)]

# Storage vector
Sj = [float(input()) for j in range(N)]

# Decision vars
Xij = [[solver.NumVar(0, min(Pi[i], Sj[j]), f'X{i}{j}') for j in range(N)] for i in range(M)]

# Restrictions
for i in range(M):
    ct = solver.Constraint(Pi[i], Pi[i], f'Max production capacity of the {i} farm')
    for j in range(N):
        ct.SetCoefficient(Xij[i][j], 1)

for j in range(N):
    ct = solver.Constraint(Sj[j], Sj[j], f'Max storage capacity of the {j} warehouse')
    for i in range(M):
        ct.SetCoefficient(Xij[i][j], 1)

# Objective function
objective = solver.Objective()
for i in range(M):
    for j in range(N):
        objective.SetCoefficient(Xij[i][j], Aij[i][j])
objective.SetMinimization()

# Resultado
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    print('Valor objetivo =', solver.Objective().Value())
    for i in range(M):
        print('[', end =' ')
        for j in range(0, N):
            print("{:.2f}".format(Xij[i][j].solution_value()), end=" ")
        print(']')
else:
    print('O problema não possui solução ótima')