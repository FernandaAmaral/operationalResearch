from ortools.linear_solver import pywraplp

def pegar_parametros(N, name):
    print(f'Digite os elementos da variável {name}')
    return [float(input()) for i in range(N)]

# Inicializando o solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Número de elementos
print('Digite o número de elementos do conjunto')
N = int(input())

E = pegar_parametros(N, 'limite superior')
L = pegar_parametros(N, 'coeficientes da função objetivo')
P = pegar_parametros(N, 'valor proporcional')

print('Digite o total máximo de elementos')
T = float(input())

# Variáveis de decisão
x = [solver.NumVar(0, E[i], f'x{i}') for i in range(N)]

# Restrições
ct = solver.Constraint(-solver.infinity(), T)
for i in range(N):
    ct.SetCoefficient(x[i], P[i])

# Função objetivo
objective = solver.Objective()
for i in range(N):
    objective.SetCoefficient(x[i], L[i])
objective.SetMaximization()

# Resultado
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    print('Solucao:')
    print('Valor objetivo =', "{:.1f}".format(solver.Objective().Value()))
    for i in range(0, N):
        print(f'x{i + 1} =', "{:.1f}".format(x[i].solution_value()))
else:
    print('O problema não possui solução ótima')
