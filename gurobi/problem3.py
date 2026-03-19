from gurobipy import Model, GRB
import os 
import os



# Parametreler
s = [800000, 900000]  # satış fiyatları
m = [600000, 750000]  # üretim maliyetleri
d = [15000, 20000]    # depolama maliyetleri
t = [[1100, 1500, 1200], [600, 700, 500]]  # aylık talep miktarları
b = [200, 100]  # başlangıç stokları
n_aylar = 3
n_arac_tipi = 2

# Model oluştur
model = Model("Araç Üretim Optimizasyonu")

# Karar değişkenleri
x = [[model.addVar(vtype=GRB.INTEGER, name=f'x_{i+1}{j+1}') for j in range(n_aylar)] for i in range(n_arac_tipi)]
y = [[model.addVar(vtype=GRB.INTEGER, name=f'y_{i+1}{j+1}') for j in range(n_aylar)] for i in range(n_arac_tipi)]
l = [[model.addVar(vtype=GRB.INTEGER, name=f'l_{i+1}{j+1}') for j in range(n_aylar)] for i in range(n_arac_tipi)]

# Amaç fonksiyonu: Toplam kârı maksimize et
objective = model.setObjective(
    sum(s[i] * y[i][j] - m[i] * x[i][j] - d[i] * l[i][j] for i in range(n_arac_tipi) for j in range(n_aylar)),
    GRB.MAXIMIZE
)

# Kısıtlar

# Başlangıç stok kısıtları
for i in range(n_arac_tipi):
    model.addConstr(x[i][0] + b[i] - y[i][0] == l[i][0], f"Baslangic_Stok_{i+1}")

# Stok geçiş kısıtları
for i in range(n_arac_tipi):
    for j in range(1, n_aylar):
        model.addConstr(x[i][j] + l[i][j - 1] - y[i][j] == l[i][j], f"Stok_Gecis_{i+1}_{j+1}")

# Üretim kapasite kısıtları
for j in range(n_aylar):
    model.addConstr(sum(x[i][j] for i in range(n_arac_tipi)) <= 1500, f"Uretim_Kapasite_{j+1}")

# Talep kısıtları
for i in range(n_arac_tipi):
    for j in range(n_aylar):
        model.addConstr(y[i][j] <= t[i][j], f"Talep_{i+1}_{j+1}")

# İlk ay üretim oranı kısıtı
model.addConstr(x[0][0] >= (2/3) * (x[0][0] + x[1][0]), "Ilk_Ay_Uretim_Orani")

# Optimizasyonu çalıştır
model.optimize()

# Çözümü yazdır
if model.status == GRB.OPTIMAL:
    print(f"Optimal Kâr: {model.objVal} TL")
    for i in range(n_arac_tipi):
        for j in range(n_aylar):
            print(f"Ay {j + 1}, Araç {i + 1}:")
            print(f"  Üretim: {x[i][j].x} adet")
            print(f"  Satış: {y[i][j].x} adet")
            print(f"  Stok: {l[i][j].x} adet")
else:
    print("Optimal çözüm bulunamadı.")
