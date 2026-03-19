from ortools.linear_solver import pywraplp
import os 


# Veri tanımları
sf = 50
af = [11, 10, 9]  # i = 1, 2, 3 için af_i
maks = [200, 310, 420]  # i = 1, 2, 3 için maks_i
tm = [[3, 3.5], [2, 2.5], [6, 4]]  # i ve j için tm_ij
k = [460, 560]  # j = 1, 2 için k_j
m = [26, 21]  # j = 1, 2 için m_j

# Solver tanımlama
solver = pywraplp.Solver.CreateSolver('GLOP')
if not solver:
    print("Solver oluşturulamadı.")
    exit()

# Karar değişkenleri x_ij (yetiştirici-fabrika matrisi)
x = {}
for i in range(3):
    for j in range(2):
        x[i, j] = solver.NumVar(0, solver.infinity(), f'x_{i+1}{j+1}')

# Amaç fonksiyonu: karı maksimize et
objective = solver.Objective()
for i in range(3):
    for j in range(2):
        objective.SetCoefficient(x[i, j], sf - af[i] - tm[i][j] - m[j])
objective.SetMaximization()

# Kısıtlar
# (1) Her yetiştirici için alınabilecek maksimum miktar
for i in range(3):
    constraint = solver.Constraint(0, maks[i])
    for j in range(2):
        constraint.SetCoefficient(x[i, j], 1)

# (2) Her fabrikanın kapasite sınırları
for j in range(2):
    constraint = solver.Constraint(0, k[j])
    for i in range(3):
        constraint.SetCoefficient(x[i, j], 1)

# Çözümü bul
status = solver.Solve()

# Çözüm sonuçları
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu:')
    for i in range(3):
        for j in range(2):
            print(f'x_{i+1}{j+1} = {x[i, j].solution_value()}')
    print('Maksimum Kar:', solver.Objective().Value())
else:
    print('Optimal çözüm bulunamadı.')
