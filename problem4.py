from ortools.linear_solver import pywraplp
import os 


# Modeli oluştur
solver = pywraplp.Solver.CreateSolver('SCIP')

# Kümeler ve parametreler
I = list(range(7))  # 7 ders var
ders_zorunluluk_kisitlari = [
    (0, 1, 2, 3, 6, 2),  # x1 + x2 + x3 + x4 + x7 >= 2
    (1, 3, 4, 6, 2),     # x2 + x4 + x5 + x7 >= 2
    (2, 4, 5, 2)         # x3 + x5 + x6 >= 2
]
on_kosul_kisitlari = [
    (3, 0),  # x4 <= x1
    (4, 5),  # x5 <= x6
    (2, 5),  # x3 <= x6
    (6, 3)   # x7 <= x4
]

# Karar değişkenleri
x = [solver.IntVar(0, 1, f'x[{i+1}]') for i in I]

# Amaç fonksiyonu: Alınan ders sayısını minimize et
solver.Minimize(solver.Sum(x))

# Kısıtlar
# (1) - (3) Zorunlu ders sayısı kısıtları
for dersler in ders_zorunluluk_kisitlari:
    indices = dersler[:-1]
    print(indices," indices")
    min_ders_sayisi = dersler[-1]
    print(min_ders_sayisi," min_ders_sayisi")
    solver.Add(solver.Sum(x[i] for i in indices) >= min_ders_sayisi)

# (4) - (7) Ön koşul kısıtları
for (ders, onkosul) in on_kosul_kisitlari:
    solver.Add(x[ders] <= x[onkosul])

# Çözümü bul
status = solver.Solve()

# Sonuçları yazdır
if status == pywraplp.Solver.OPTIMAL:
    print('Çözüm bulundu:')
    for i in I:
        print(f'Ders {i+1} alınacak mı? :', x[i].solution_value())
    print('Toplam alınan ders sayısı:', solver.Objective().Value())
else:
    print('Optimal çözüm bulunamadı.')
