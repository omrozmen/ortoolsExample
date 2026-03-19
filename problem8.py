from ortools.linear_solver import pywraplp
import os 


# Solver tanımla
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parametreler
depolar = [1, 2, 3, 4]
bolgeler = [1, 2, 3]
maks_kapasite = 100
maliyet_acma = {1: 40000, 2: 50000, 3: 30000, 4: 15000}
talep = {1: 80, 2: 70, 3: 40}
gonderme_maliyeti = {
    (1, 1): 20, (1, 2): 40, (1, 3): 50,
    (2, 1): 48, (2, 2): 15, (2, 3): 26,
    (3, 1): 26, (3, 2): 35, (3, 3): 18,
    (4, 1): 24, (4, 2): 50, (4, 3): 35
}

# Karar Değişkenleri
x = {}
for i in depolar:
    for j in bolgeler:
        x[i, j] = solver.IntVar(0, maks_kapasite, f'x_{i}_{j}')

y = {}
for i in depolar:
    y[i] = solver.BoolVar(f'y_{i}')

# Amaç Fonksiyonu
solver.Minimize(
    sum(gonderme_maliyeti[i, j] * x[i, j] for i in depolar for j in bolgeler) +
    sum(maliyet_acma[i] * y[i] for i in depolar)
)

# 1. Depoların taşıma kapasitesi kısıtları
for i in depolar:
    solver.Add(sum(x[i, j] for j in bolgeler) <= maks_kapasite * y[i])

# 2. Bölge talepleri kısıtları
for j in bolgeler:
    solver.Add(sum(x[i, j] for i in depolar) >= talep[j])

# 3. Depo açılış ilişkileri
solver.Add(y[1] <= y[2])  # Ankara açılırsa İzmir de açılmalı
solver.Add(y[1] <= y[3])  # Ankara açılırsa İstanbul da açılmalı

# 4. En fazla 3 depo açılabilir
solver.Add(sum(y[i] for i in depolar) <= 3)

# 5. Adana açılırsa İzmir açılmamalı
solver.Add(y[4] <= 1 - y[3])

# 6. Ankara veya İzmir açılmazsa, Adana ve İstanbul açılmalı
solver.Add(y[1] >= 1 - y[2])
solver.Add(y[1] >= 1 - y[4])
solver.Add(y[3] >= 1 - y[2])
solver.Add(y[3] >= 1 - y[4])

# Optimizasyonu çöz
status = solver.Solve()

# Çözüm çıktısı
if status == pywraplp.Solver.OPTIMAL:
    print(f"Toplam minimum maliyet: {solver.Objective().Value()} TL")
    for i in depolar:
        print(f"Depo {i} açıldı mı? {'Evet' if y[i].solution_value() == 1 else 'Hayır'}")
        for j in bolgeler:
            print(f"  Bölge {j} için gönderilen kamyon sayısı: {x[i, j].solution_value()}")
else:
    print("Optimal çözüm bulunamadı.")
