from ortools.linear_solver import pywraplp
import os 
os.chdir("./ortoolsExamples")


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
    print(f'x1 (orijinal) = {x1.solution_value()}')
    print(f'x2 (orijinal) = {x2.solution_value()}')
    print(f'x3 (orijinal) = {x3.solution_value()}')
    print(f'z (maksimum ürün miktarı) = {z.solution_value()}\'dir.')
    
    # En yakın tam sayıya yuvarlayarak gösterim
    x1_rounded = round(x1.solution_value())
    x2_rounded = round(x2.solution_value())
    x3_rounded = round(x3.solution_value())
    
    print('En yakın tam sayıya yuvarlanmış değerler:')
    print(f'x1 (yuvarlanmış) = {x1_rounded}')
    print(f'x2 (yuvarlanmış) = {x2_rounded}')
    print(f'x3 (yuvarlanmış) = {x3_rounded}')
    
    # Yuvarlanmış değerlere göre z'yi yeniden hesapla
    z_rounded_1 = (7 * x1_rounded + 6 * x2_rounded + 8 * x3_rounded) / b1
    z_rounded_2 = (5 * x1_rounded + 9 * x2_rounded + 4 * x3_rounded) / b2
    z_final = min(z_rounded_1, z_rounded_2)  # z, her iki formülden minimum olanı alır
    
    print(f'Yuvarlanmış değerlere göre z = {z_final}')
else:
    print('Optimal çözüm bulunamadı.')
