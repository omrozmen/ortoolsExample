from ortools.linear_solver import pywraplp
import os 
os.chdir("./ortoolsExamples")


# Verilen sabitler
gun_sayisi = 7
vardiya_sayisi = 3
ardisik_gun_sayisi = 4
mevcut_isci_sayisi = 60

# İhtiyaç duyulan işçi sayıları (Tablo 20'ye göre)
s = {
    (1, 1): 5, (1, 2): 7, (1, 3): 9,
    (2, 1): 3, (2, 2): 8, (2, 3): 10,
    (3, 1): 2, (3, 2): 9, (3, 3): 10,
    (4, 1): 4, (4, 2): 5, (4, 3): 7,
    (5, 1): 3, (5, 2): 7, (5, 3): 11,
    (6, 1): 2, (6, 2): 2, (6, 3): 2,
    (7, 1): 2, (7, 2): 5, (7, 3): 2
}

# OR-Tools solver tanımı
solver = pywraplp.Solver.CreateSolver('SCIP')

# Karar değişkenleri: Her gün ve vardiya için çalışan sayısı
x = {}
for i in range(1, gun_sayisi + 1):
    for j in range(1, vardiya_sayisi + 1):
        x[i, j] = solver.IntVar(0, mevcut_isci_sayisi, f'x[{i},{j}]')

# Amaç fonksiyonu: Toplam çalışan sayısını minimize et
solver.Minimize(solver.Sum(x[i, j] for i in range(1, gun_sayisi + 1) for j in range(1, vardiya_sayisi + 1)))

# Kısıtlar

# 1. Toplam çalışan sayısı sınırı
solver.Add(solver.Sum(x[i, j] for i in range(1, gun_sayisi + 1) for j in range(1, vardiya_sayisi + 1)) <= mevcut_isci_sayisi)


def create_k_ranges_table(gun_sayisi, ardisik_gun_sayisi):
    table = []
    for i in range(1, gun_sayisi + 1):
        # İlk koşul: i - ardisik + 1 <= k <= i
        k_values_first_condition = range(max(1, i - ardisik_gun_sayisi + 1), i + 1)
        
        # İkinci koşul: i <= k <= i + ardisik - 1
        k_values_second_condition = range(i + ardisik_gun_sayisi, gun_sayisi + 1)
        
        # İki koşulun kesişimini almak
        k_values = sorted(set(k_values_first_condition).union(set(k_values_second_condition)))
        table.append(k_values)
    return table


# Parametreler
gun_sayisi = 7
ardisik_gun_sayisi = 4


k_range = create_k_ranges_table(7, 4)


# 2. Her gün ve vardiya için minimum işçi gereksinimi (Tablo 20'ye göre)
for i in range(1, gun_sayisi + 1):
    for j in range(1, vardiya_sayisi + 1):
        # Ardışık çalışma kısıtını burada tanımlıyoruz

        print(k_range[i-1], "k_range")
        print(max(1, i - ardisik_gun_sayisi + 1)," max")
        print(min(i + ardisik_gun_sayisi, gun_sayisi + 1)," min")
        solver.Add(solver.Sum(x[k, j] for k in k_range[i-1]) >= s[i, j])

# Modeli çöz
status = solver.Solve()

# Çözümün durumu
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu:')
    toplam_calisan = sum(x[i, j].solution_value() for i in range(1, gun_sayisi + 1) for j in range(1, vardiya_sayisi + 1))
    print(f'Toplam çalışan sayısı: {toplam_calisan}')
    
    # Her gün ve vardiya için çalışan sayısını yazdır
    for i in range(1, gun_sayisi + 1):
        for j in range(1, vardiya_sayisi + 1):
            print(f'Gün {i}, Vardiya {j}: {x[i, j].solution_value()} işçi')
else:
    print('Optimal çözüm bulunamadı.')
