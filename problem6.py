from ortools.linear_solver import pywraplp
import os 
os.chdir("./ortoolsExamples")


# Parametreler
v = [3, 5, 5, 6, 2, 1, 1, 8, 6, 3, 2, 0, 0]   # Karbonhidrat değerleri
k = [1, 1, 1, 2, 4, 5, 2, 3, 3, 1, 1, 1, 1]   # Vitamin değerleri
p = [1, 2, 1, 1, 1, 1, 3, 5, 6, 1, 0, 0, 0]   # Protein değerleri
y = [0, 0, 0, 2, 1, 1, 1, 2, 1, 0, 0, 0, 0]   # Yağ değerleri
m = [0.10, 0.12, 0.13, 0.09, 0.10, 0.07, 0.70, 1.20, 0.63, 0.28, 0.42, 0.15, 0.12] # Maliyetler

# Gereksinimler
mink = 5   # Minimum karbonhidrat gereksinimi
minp = 10  # Minimum protein gereksinimi
miny = 8   # Minimum yağ gereksinimi
minv = 2   # Minimum vitamin gereksinimi

# Solver oluştur
solver = pywraplp.Solver.CreateSolver('SCIP')

# Karar değişkenleri: İkili (0 veya 1) değişkenler
x = [solver.IntVar(0, 1, f'x_{i+1}') for i in range(13)]

# Amaç Fonksiyonu: Toplam maliyeti minimize et
solver.Minimize(solver.Sum(m[i] * x[i] for i in range(13)))

# Kısıtlar

# Her yiyecek grubundan en az bir tane seçme kısıtları
solver.Add(solver.Sum(x[i] for i in range(6)) >= 1)    # Grup 1
solver.Add(solver.Sum(x[i] for i in range(6, 9)) >= 1) # Grup 2
solver.Add(solver.Sum(x[i] for i in range(9, 13)) >= 1) # Grup 3

# Besin gereksinimlerini karşılama kısıtları
solver.Add(solver.Sum(v[i] * x[i] for i in range(13)) >= minv)   # Karbonhidrat gereksinimi
solver.Add(solver.Sum(p[i] * x[i] for i in range(13)) >= minp)   # Protein gereksinimi
solver.Add(solver.Sum(y[i] * x[i] for i in range(13)) >= miny)   # Yağ gereksinimi
solver.Add(solver.Sum(k[i] * x[i] for i in range(13)) >= mink)   # Vitamin gereksinimi

# Optimizasyonu çalıştır
status = solver.Solve()

# Çözümü yazdır
if status == pywraplp.Solver.OPTIMAL:
    print(f"Minimum maliyet: {solver.Objective().Value()} TL")
    for i in range(13):
        if x[i].solution_value() > 0.5:  # Seçilen yiyecekler
            print(f"Yiyecek {i + 1} seçildi.")
else:
    print("Optimal çözüm bulunamadı.")
