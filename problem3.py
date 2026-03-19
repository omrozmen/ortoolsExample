from ortools.linear_solver import pywraplp
import os 


# OR-Tools solver'ı oluştur
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parametreler
s = [800000, 900000]  # satış fiyatları
m = [600000, 750000]  # üretim maliyetleri
d = [15000, 20000]    # depolama maliyetleri
t = [[1100, 1500, 1200], [600, 700, 500]]  # aylık talep miktarları
b = [200, 100]  # başlangıç stokları
n_aylar = 3
n_arac_tipi = 2

# Karar değişkenlerini oluştur
x = [[solver.IntVar(0, 1500, f'x_{i+1}{j+1}') for j in range(n_aylar)] for i in range(n_arac_tipi)]
y = [[solver.IntVar(0, t[i][j], f'y_{i+1}{j+1}') for j in range(n_aylar)] for i in range(n_arac_tipi)]
l = [[solver.IntVar(0, solver.infinity(), f'l_{i+1}{j+1}') for j in range(n_aylar)] for i in range(n_arac_tipi)]

# Amaç fonksiyonu: Toplam kârı maksimize et
objective = solver.Objective()
for i in range(n_arac_tipi):
    for j in range(n_aylar):
        # Gelir kısmı
        objective.SetCoefficient(y[i][j], s[i])
        # Üretim maliyeti kısmı
        objective.SetCoefficient(x[i][j], -m[i])
        # Depolama maliyeti kısmı
        objective.SetCoefficient(l[i][j], -d[i])
objective.SetMaximization()

# Kısıtlar

# Başlangıç stoğu kısıtları
for i in range(n_arac_tipi):
    solver.Add(x[i][0] + b[i] - y[i][0] == l[i][0])

# Stok geçiş kısıtları
for i in range(n_arac_tipi):
    for j in range(1, n_aylar):
        solver.Add(x[i][j] + l[i][j - 1] - y[i][j] == l[i][j])

# Üretim kapasite kısıtları
for j in range(n_aylar):
    solver.Add(sum(x[i][j] for i in range(n_arac_tipi)) <= 1500)

# Talep kısıtları
for i in range(n_arac_tipi):
    for j in range(n_aylar):
        solver.Add(y[i][j] <= t[i][j])

# İlk ay üretim oranı kısıtı
solver.Add(x[0][0] >= (2/3) * (x[0][0] + x[1][0]))

# Modeli optimize et
status = solver.Solve()

# Sonuçları yazdır
if status == pywraplp.Solver.OPTIMAL:
    print(f"Optimal Kâr: {objective.Value()} TL")
    for i in range(n_arac_tipi):
        for j in range(n_aylar):
            print(f"Ay {j + 1}, Araç {i + 1}:")
            print(f"  Üretim: {x[i][j].solution_value()} adet")
            print(f"  Satış: {y[i][j].solution_value()} adet")
            print(f"  Stok: {l[i][j].solution_value()} adet")
else:
    print("Optimal çözüm bulunamadı.")
