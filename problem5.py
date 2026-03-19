from ortools.linear_solver import pywraplp
import os 
os.chdir("./ortoolsExamples")


# Parametreler
e = [80, 70, 90, 50, 60]  # erkek öğrenci sayıları
k = [30, 5, 10, 40, 30]   # kız öğrenci sayıları
u = [[1, 2], [0.5, 1.7], [0.8, 0.8], [1.3, 0.4], [1.5, 0.6]]  # uzaklıklar
mink = 150  # minimum kayıt sayısı
miny = 0.20 # minimum kız öğrenci yüzdesi

# Solver tanımlama
solver = pywraplp.Solver.CreateSolver('SCIP')

# Karar değişkenleri: x_ij = 1, i bölgesindeki öğrenciler j okuluna giderse; 0 aksi takdirde
x = [[solver.IntVar(0, 1, f'x_{i+1}{j+1}') for j in range(2)] for i in range(5)]

# Amaç Fonksiyonu: Toplam mesafeyi minimize et
objective = solver.Objective()
for i in range(5):
    for j in range(2):
        objective.SetCoefficient(x[i][j], (e[i] + k[i]) * u[i][j])
objective.SetMinimization()

# Kısıtlar

# Her lisede en az 150 kayıt olmasını gerektiren kısıtlar
for j in range(2):
    solver.Add(sum((e[i] + k[i]) * x[i][j] for i in range(5)) >= mink)

# Kayıtların en az %20'sinin kız öğrenci olması durumu
for j in range(2):
    solver.Add(sum(k[i] * x[i][j] for i in range(5)) >= miny * sum((e[i] + k[i]) * x[i][j] for i in range(5)))

# Her bölgedeki bütün öğrencilerin aynı okula gitmesini sağlayan kısıtlar
for i in range(5):
    solver.Add(x[i][0] + x[i][1] == 1)

# Optimizasyonu çalıştır
status = solver.Solve()

# Çözüm yazdır
if status == pywraplp.Solver.OPTIMAL:
    print(f"Minimum toplam mesafe: {objective.Value()} km")
    for i in range(5):
        for j in range(2):
            if x[i][j].solution_value() == 1:
                print(f"Bölge {i + 1} öğrencileri Okul {j + 1}'e gitmelidir.")
else:
    print("Optimal çözüm bulunamadı.")
