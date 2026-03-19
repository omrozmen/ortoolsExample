from ortools.linear_solver import pywraplp
import os 
os.chdir("./ortoolsExamples")


# Solver tanımla
solver = pywraplp.Solver.CreateSolver('SCIP')
M = 10000  # Yeterince büyük bir sayı (Big-M)

# Verilen parametreler
dm = [33, 30, 26, 24, 19, 18, 17]
sm = 1000
t = [400, 300, 500, 700, 200, 400, 200]

# Karar değişkenleri tanımla
x = [solver.IntVar(0, solver.infinity(), f'x_{i+1}') for i in range(7)]
y = [solver.BoolVar(f'y_{i+1}') for i in range(7)]

# Amaç fonksiyonu: Toplam maliyeti minimize et
solver.Minimize(solver.Sum(dm[i] * x[i] + sm * y[i] for i in range(7)))

# Kısıtlar
# Talep kısıtları
solver.Add(x[0] >= 400)  # 1a
solver.Add(x[0] + x[1] >= 700)  # 1b
solver.Add(x[0] + x[1] + x[2] >= 1200)  # 1c
solver.Add(x[0] + x[1] + x[2] + x[3] >= 1900)  # 1d
solver.Add(x[0] + x[1] + x[2] + x[3] + x[4] >= 2100)  # 1e
solver.Add(x[0] + x[1] + x[2] + x[3] + x[4] + x[5] >= 2500)  # 1f
solver.Add(x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6] >= 2700)  # 1g

# Üretim karar kısıtları
for i in range(7):
    solver.Add(x[i] <= M * y[i])  # 2a - 2g

# Modeli çöz
status = solver.Solve()

# Sonuçları yazdır
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu:')
    for i in range(7):
        print(f'x_{i+1} (üretilen miktar):', x[i].solution_value())
        print(f'y_{i+1} (üretilme kararı):', y[i].solution_value())
    print('Toplam Maliyet =', solver.Objective().Value())
else:
    print('Optimal çözüm bulunamadı.')
