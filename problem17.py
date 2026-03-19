from ortools.linear_solver import pywraplp
import os 


# OR-Tools solver nesnesini başlat
solver = pywraplp.Solver.CreateSolver('GLOP')
if not solver:
    raise Exception("Solver başlatılamadı.")

# Karar değişkenleri
x1 = solver.NumVar(0, solver.infinity(), 'x1')
x2 = solver.NumVar(0, solver.infinity(), 'x2')
x3 = solver.NumVar(0, solver.infinity(), 'x3')
z = solver.NumVar(0, solver.infinity(), 'z')

# Parametreler
b1, b2 = 4, 3
h1, h2 = 100, 200

# Amaç fonksiyonu: max z
solver.Maximize(z)

# Kısıtlar
# Amaç fonksiyonunu doğrusal hale getiren kısıtlar
solver.Add(z <= (7 * x1 + 6 * x2 + 8 * x3) / b1)
solver.Add(z <= (5 * x1 + 9 * x2 + 4 * x3) / b2)

# Ham madde miktarı kısıtları
solver.Add(8 * x1 + 5 * x2 + 3 * x3 <= h1)  # (1a)
solver.Add(6 * x1 + 9 * x2 + 8 * x3 <= h2)  # (1b)

# Çözüm
status = solver.Solve()

# Çözüm sonucunu kontrol et
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu:')
    print(f'x1 = {x1.solution_value()}')
    print(f'x2 = {x2.solution_value()}')
    print(f'x3 = {x3.solution_value()}')
    print(f'z (maksimum ürün miktarı) = {z.solution_value()}')
else:
    print('Optimal çözüm bulunamadı.') 