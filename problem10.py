from ortools.linear_solver import pywraplp
import os 


# Solver'ı tanımla
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parametreler (sadece örnek)
weeks = 7
t = [10, 20, 15, 10, 5, 20, 10]  # talep
dm = [4, 4, 2, 4, 5, 2, 4]  # değişken maliyet
sm = [30, 30, 70, 50, 30, 70, 50]  # sabit maliyet
bm = [0.5] * weeks  # elde bulundurma maliyeti
bs = 2  # başlangıç stoku
ss = 5  # son stok

# Karar Değişkenleri
x = [solver.IntVar(0, solver.infinity(), f'x[{i}]') for i in range(weeks)]
y = [solver.BoolVar(f'y[{i}]') for i in range(weeks)]
I = [solver.IntVar(0, solver.infinity(), f'I[{i}]') for i in range(weeks)]

# Amaç fonksiyonu: toplam maliyeti minimize et
solver.Minimize(
    sum(dm[i] * x[i] + sm[i] * y[i] + bm[i] * I[i] for i in range(weeks))
)

# Kısıtlar

# 1. Stok denklem kısıtları
solver.Add(I[0] == bs + x[0] - t[0])
for i in range(1, weeks):
    solver.Add(I[i] == I[i - 1] + x[i] - t[i])

# 2. Son haftada hedef stok
solver.Add(I[weeks - 1] == ss)

# 3. Üretim varsa ikili değişken ilişkisi (Big-M metodu)
M = 1000  # yeterince büyük bir sayı
for i in range(weeks):
    solver.Add(x[i] <= M * y[i])

# 4. Toplam üretim haftası sayısı
solver.Add(solver.Sum(y[i] for i in range(weeks)) <= 6)

# 5. 5. haftada üretim için 4. haftada üretim yapılmış olması gerek
solver.Add(y[4] <= y[3])

# 6. 2. hafta için 1. hafta koşulu
solver.Add(y[1] <= y[0])

# 7. 3. ve 6. haftalarda üretim aynı olmalı
solver.Add(y[2] == y[5])

# Çözüm
status = solver.Solve()

# Sonuçları yazdır
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu.')
    for i in range(weeks):
        print(f'Hafta {i+1}: Üretim = {x[i].solution_value()}, Üretim yapıldı mı = {y[i].solution_value()}, Stok = {I[i].solution_value()}')
    print('Toplam maliyet:', solver.Objective().Value())
else:
    print('Optimal çözüm bulunamadı.')
