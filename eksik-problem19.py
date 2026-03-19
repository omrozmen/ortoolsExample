from ortools.linear_solver import pywraplp
import os 


# Solver oluşturma
solver = pywraplp.Solver.CreateSolver('GLOP')  # GLOP, LP problemleri için uygun

# Parametreler
mevcut = 100000
maks = 50000
g = [0.1, 1.3, 0.2, 1.1, 1.5, 0.06]
s = [1, 3, 1, 2, 3, 1]

# Yıllar ve yatırım alternatifleri için indeksler
years = range(1, 4)   # 1, 2, 3 yılları
investments = range(1, 7)  # 1'den 6'ya kadar yatırım alternatifleri

# Karar değişkenleri: x[i][j] -> i. yıl j. yatırımına ayrılacak miktar
x = {}
for i in years:
    for j in investments:
        x[i, j] = solver.NumVar(0, maks, f'x[{i},{j}]')  # Her yatırım max 50.000 TL olabilir

# Amaç Fonksiyonu: 3. yıl sonunda elde edilen nakit miktarı maksimizasyonu
objective = solver.Objective()

for i in years:
    for j in investments:
        if i + s[j-1] <= 3:  # Geri dönüş yılı 3. yıldan fazla olmamalı
            objective.SetCoefficient(x[i, j], g[j-1])  # Yatırım getirisiyle çarpılıyor
        elif i == 3:  # 3. yıl için yatırılan miktarın tamamı dahil edilir
            objective.SetCoefficient(x[i, j], 1)

objective.SetMaximization()

# Kısıtlar
# 1. Kısıt: İlk yıl yatırılacak toplam para mevcut miktarı geçmemeli
constraint1 = solver.Constraint(0, mevcut)
for j in investments:
    constraint1.SetCoefficient(x[1, j], 1)

# 2. Kısıt: Diğer yıllar için yatırılacak para bir önceki yılın getirisiyle belirlenmeli
for i in range(2, 4):  # 2. ve 3. yıllar
    constraint = solver.Constraint(0, mevcut)  # mevcut para sınırını geçmemeli
    for j in investments:
        # i. yılda yapılan yatırım ve i-1. yılın getirisi
        constraint.SetCoefficient(x[i, j], 1)
        if i - s[j-1] > 0:  # Geçmiş yıldan dönüş varsa
            constraint.SetCoefficient(x[i - s[j-1], j], g[j-1])

# 3. Kısıt: Her yatırıma en fazla 50.000 TL ayrılabilir
for j in investments:
    for i in years:
        constraint = solver.Constraint(0, maks)
        constraint.SetCoefficient(x[i, j], 1)

# Çözüm
status = solver.Solve()

# Sonuçları Yazdırma
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu:')
    for i in years:
        for j in investments:
            if x[i, j].solution_value() > 0:
                print(f'Yıl {i}, Yatırım {j}, Tutar: {x[i, j].solution_value()}')
    print(f'En yüksek toplam getiri: {objective.Value()}')
else:
    print('Çözüm bulunamadı.')
