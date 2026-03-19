from ortools.linear_solver import pywraplp
import os 


# Model oluşturma
solver = pywraplp.Solver.CreateSolver('SCIP')

# Karar değişkenleri
x1 = solver.IntVar(0, solver.infinity(), 'x1')  # Yarı mamul masa
x2 = solver.IntVar(0, solver.infinity(), 'x2')  # Son ürün masa
x3 = solver.IntVar(0, solver.infinity(), 'x3')  # Yarı mamul sandalye
x4 = solver.IntVar(0, solver.infinity(), 'x4')  # Son ürün sandalye

# Amaç fonksiyonu: Maksimize et
solver.Maximize(70 * x1 + 140 * x2 + 60 * x3 + 110 * x4 - (40 * (x1 + x2) + 30 * (x3 + x4)))

# Kısıtlar
# (1) Ham madde miktarı kısıtı
solver.Add(40 * (x1 + x2) + 30 * (x3 + x4) <= 40000)

# (2) İş gücü saati kısıtı
solver.Add(2 * (x1 + x2 + x3 + x4) + 3 * x2 + 2 * x4 <= 6000)

# Çözümü bul
status = solver.Solve()

# Sonuçları göster
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu:')
    print(f'x1 (Yarı mamul masa miktarı): {x1.solution_value()}')
    print(f'x2 (Son ürün masa miktarı): {x2.solution_value()}')
    print(f'x3 (Yarı mamul sandalye miktarı): {x3.solution_value()}')
    print(f'x4 (Son ürün sandalye miktarı): {x4.solution_value()}')
    print(f'Maksimum kar: {solver.Objective().Value()}')
else:
    print('Optimal çözüm bulunamadı.')
