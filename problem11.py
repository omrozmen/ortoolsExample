from ortools.linear_solver import pywraplp
import os 

# Kümeler
trucks = [1, 2, 3, 4]
markets = [1, 2, 3, 4, 5]

# Parametreler
# Kamyon kapasiteleri
k = {1: 400, 2: 500, 3: 600, 4: 1100}

# Kamyon günlük işletim maliyetleri
m = {1: 45, 2: 50, 3: 55, 4: 60}

# Market talepleri
t = {1: 100, 2: 200, 3: 300, 4: 500, 5: 800}

# OR-Tools solver oluşturun
solver = pywraplp.Solver.CreateSolver('SCIP')

# x_ij: i kamyonu j marketine teslimat yaparsa 1, aksi takdirde 0
x = {}
for i in trucks:
    for j in markets:
        x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')

# y_i: i kamyon kullanılırsa 1, aksi takdirde 0
y = {}
for i in trucks:
    y[i] = solver.IntVar(0, 1, f'y[{i}]')
# Amaç fonksiyonu: Toplam işletim maliyetini minimize et
solver.Minimize(solver.Sum(m[i] * y[i] for i in trucks))

for i in trucks:
    solver.Add(solver.Sum(t[j] * x[i, j] for j in markets) <= k[i] * y[i])

for j in markets:
    solver.Add(solver.Sum(x[i, j] for i in trucks) == 1)
# Değişkenlerin binary olduğunu zaten tanımladık


status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu:')
    for i in trucks:
        if y[i].solution_value() > 0:
            print(f'Kamyon {i} kullanılıyor.')
            for j in markets:
                if x[i, j].solution_value() > 0:
                    print(f'  Market {j} için kamyon {i} kullanılıyor.')
    print('Toplam maliyet:', solver.Objective().Value())
else:
    print('Optimal çözüm bulunamadı.')
