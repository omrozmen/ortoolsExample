from ortools.linear_solver import pywraplp
import os 
os.chdir("./ortoolsExamples")


# Veri tanımları
vardiya_maliyetleri = [9, 9, 9, 7.5, 7.5, 7.5]
saat_personel_ihtiyaci = [2, 3, 5, 5, 3, 2, 4, 6, 3]

# OR-Tools solver tanımı
solver = pywraplp.Solver.CreateSolver('SCIP')

# Karar değişkenleri tanımları
x = []
for i in range(6):
    x.append(solver.IntVar(0, solver.infinity(), f'x_{i+1}'))

# Amaç fonksiyonu: Toplam maliyeti minimize et
solver.Minimize(sum(vardiya_maliyetleri[i] * 4 * x[i] for i in range(6)))

# Kısıtlar: Her saatte gerekli minimum personel sayısını sağla
for j in range(9):
    solver.Add(sum(x[i] for i in range(max(0, j-4), min(6, j+1))) >= saat_personel_ihtiyaci[j])

# Çözümü bul
status = solver.Solve()

# Sonuçları yazdır
if status == pywraplp.Solver.OPTIMAL:
    print("Optimal çözüm bulundu!")
    for i in range(6):
        print(f"x_{i+1} (Vardiya {i+1} başlangıç personel sayısı):", x[i].solution_value())
    print("Toplam maliyet:", solver.Objective().Value())
else:
    print("Optimal çözüm bulunamadı.")
