from ortools.linear_solver import pywraplp
import os 


# OR-Tools solver nesnesini başlat
solver = pywraplp.Solver.CreateSolver('GLOP')
if not solver:
    raise Exception("Solver başlatılamadı.")

# Karar değişkenleri (sorulması gereken soru sayısı)
x1 = solver.NumVar(0, solver.infinity(), 'x1')
x2 = solver.NumVar(0, solver.infinity(), 'x2')
x3 = solver.NumVar(0, solver.infinity(), 'x3')

# Parametreler
p1, p2, p3 = 5, 4, 6  # puanlar
s1, s2, s3 = 3, 2, 4  # süreler
maks = 100  # maksimum problem sayısı
sure1, sure2 = 150, 210  # süre sınırları

# Amaç fonksiyonu: max 5*x1 + 4*x2 + 6*x3
solver.Maximize(p1 * x1 + p2 * x2 + p3 * x3)

# Kısıtlar
# Kısıt (1): x1 + x2 + x3 <= 100
solver.Add(x1 + x2 + x3 <= maks)

# Kısıt (2a): 3*x1 + 2*x2 <= 150
solver.Add(s1 * x1 + s2 * x2 <= sure1)

# Kısıt (2b): 3*x1 + 2*x2 + 4*x3 <= 210
solver.Add(s1 * x1 + s2 * x2 + s3 * x3 <= sure2)

# Çözüm
status = solver.Solve()

# Çözüm sonucunu kontrol et
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu:')
    print(f'x1 = {x1.solution_value()}')
    print(f'x2 = {x2.solution_value()}')
    print(f'x3 = {x3.solution_value()}')
    print(f'Maksimum puan = {solver.Objective().Value()}')
else:
    print('Optimal çözüm bulunamadı.')
