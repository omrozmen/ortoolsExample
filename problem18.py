from ortools.linear_solver import pywraplp
import os 


# OR-Tools solver başlat
solver = pywraplp.Solver.CreateSolver('CBC')
if not solver:
    raise Exception("Solver başlatılamadı.")

# Parametreler
v = [4, 3, 4, 6, 5, 6, 6, 8, 8]  # saatlik ihtiyaç duyulan veznedar sayısı
tz = 50  # tam zamanlı veznedar saatlik ücret
yz = 30  # yarı zamanlı veznedar saatlik ücret
maks = 5  # maksimum yarı zamanlı veznedar sayısı
tsure = 8  # tam zamanlı çalışma süresi
ysure = 3  # yarı zamanlı çalışma süresi

# Karar değişkenleri
x = [solver.IntVar(0, solver.infinity(), f'x{i}') for i in range(12, 14)]  # tam zamanlı çalışanlar (12 ve 13 için)
y = [solver.IntVar(0, solver.infinity(), f'y{j}') for j in range(9, 17)]  # yarı zamanlı çalışanlar (9'dan 16'ya saat bazında)

# Amaç fonksiyonu
solver.Minimize(
    sum(tsure * tz * x[i - 12] for i in range(12, 14)) +
    sum(ysure * yz * y[j - 9] for j in range(9, 15))
)

# Kısıtlar
# Saatlik veznedar ihtiyacını karşılama kısıtları (1 nolu kısıt)
solver.Add(x[0] + x[1] + y[0] >= v[0])  # 9:00 için
solver.Add(x[0] + x[1] + y[0] + y[1] >= v[1])  # 10:00 için
solver.Add(x[0] + x[1] + y[0] + y[1] + y[2] >= v[2])  # 11:00 için
solver.Add(x[1] + y[1] + y[2] + y[3] >= v[3])  # 12:00 için
solver.Add(x[0] + y[2] + y[3] + y[4] >= v[4])  # 13:00 için
solver.Add(x[0] + x[1] + y[3] + y[4] >= v[5])  # 14:00 için
solver.Add(x[0] + x[1] + y[4] >= v[6])  # 15:00 için
solver.Add(x[0] + x[1] + y[5] >= v[7])  # 16:00 için

# Yarı zamanlı çalışan sınırı kısıtı (2 nolu kısıt)
solver.Add(sum(y[j - 9] for j in range(9, 15)) <= maks)

# Çözüm
status = solver.Solve()

# Çözüm sonucunu kontrol et
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu:')
    for i in range(12, 14):
        print(f'x{i} = {x[i - 12].solution_value()}')
    for j in range(9, 17):
        print(f'y{j} = {y[j - 9].solution_value()}')
    print(f'Toplam maliyet = {solver.Objective().Value()} TL')
else:
    print('Optimal çözüm bulunamadı.')
