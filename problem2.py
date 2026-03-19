from ortools.linear_solver import pywraplp
import os 


# Solver tanımla
solver = pywraplp.Solver.CreateSolver('GLOP')  # GLOP, OR-Tools'ta doğrusal programlama için kullanılan solver'dır.

# Değişkenler
x1 = solver.NumVar(0, solver.infinity(), 'x1')  # İlk proseste üretilen parfüm miktarı
x2 = solver.NumVar(0, solver.infinity(), 'x2')  # İkinci proseste üretilen parfüm miktarı
x3 = solver.NumVar(0, solver.infinity(), 'x3')  # Modelin çalıştığı saat miktarı

# Amaç Fonksiyonu
# z = 5(3x1 + 5x2) - 3(x1 + 2x2) - 2(2x1 + 3x2) - 100x3
objective = solver.Objective()
objective.SetCoefficient(x1, 5 * 3 - 3 - 2 * 2)  # x1'in katsayısı: 5*3 - 3 - 2*2 = 15 - 3 - 4 = 8
objective.SetCoefficient(x2, 5 * 5 - 3 * 2 - 2 * 3)  # x2'nin katsayısı: 5*5 - 3*2 - 2*3 = 25 - 6 - 6 = 13
objective.SetCoefficient(x3, -100)  # x3'ün katsayısı: -100
objective.SetMaximization()

# Kısıtlar
# İş gücü kısıtı: x1 + 2x2 <= 20000
solver.Add(x1 + 2 * x2 <= 20000)

# Kimyasal kısıtı: 2x1 + 3x2 <= 35000
solver.Add(2 * x1 + 3 * x2 <= 35000)

# Talep kısıtı: x1 + x2 <= 1000 + 200 * x3
solver.Add(x1 + x2 <= 1000 + 200 * x3)

# Optimizasyonu çalıştır
status = solver.Solve()

# Çözümü yazdır
if status == pywraplp.Solver.OPTIMAL:
    print(f"Optimal Kâr: {objective.Value()} TL")
    print(f"x1 (İlk proseste üretilen parfüm miktarı): {x1.solution_value()} cl")
    print(f"x2 (İkinci proseste üretilen parfüm miktarı): {x2.solution_value()} cl")
    print(f"x3 (Modelin çalıştığı saat miktarı): {x3.solution_value()} saat")
else:
    print("Optimal çözüm bulunamadı.")
