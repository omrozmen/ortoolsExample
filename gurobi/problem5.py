from gurobipy import Model, GRB
import os 
import os



# Parametreler
e = [80, 70, 90, 50, 60]  # Erkek öğrenci sayıları
k = [30, 5, 10, 40, 30]   # Kız öğrenci sayıları
u = [[1, 2], [0.5, 1.7], [0.8, 0.8], [1.3, 0.4], [1.5, 0.6]]  # Uzaklıklar (km)
mink = 150  # Her okul için minimum kayıt sayısı
miny = 0.20 # Kayıtlarda minimum kız öğrenci yüzdesi

# Model oluştur
model = Model("Okul_Kayit_Optimizasyonu")

# Karar değişkenleri: x_ij = 1, i bölgesindeki öğrenciler j okuluna giderse; 0 aksi takdirde
x = [[model.addVar(vtype=GRB.BINARY, name=f"x_{i+1}{j+1}") for j in range(2)] for i in range(5)]

# Amaç Fonksiyonu: Toplam mesafeyi minimize et
model.setObjective(sum((e[i] + k[i]) * u[i][j] * x[i][j] for i in range(5) for j in range(2)), GRB.MINIMIZE)

# Kısıtlar

# Her okulda en az 150 kayıt olmasını gerektiren kısıtlar
for j in range(2):
    model.addConstr(sum((e[i] + k[i]) * x[i][j] for i in range(5)) >= mink, name=f"Min_Kayit_{j+1}")

# Kayıtların en az %20'sinin kız öğrenci olması durumu
for j in range(2):
    model.addConstr(sum(k[i] * x[i][j] for i in range(5)) >= miny * sum((e[i] + k[i]) * x[i][j] for i in range(5)), name=f"Min_Kiz_Yuzdesi_{j+1}")

# Her bölgedeki bütün öğrencilerin aynı okula gitmesini sağlayan kısıtlar
for i in range(5):
    model.addConstr(x[i][0] + x[i][1] == 1, name=f"Tek_Okul_{i+1}")

# Modeli optimize et
model.optimize()

# Çözümü yazdır
if model.status == GRB.OPTIMAL:
    print(f"Minimum toplam mesafe: {model.objVal} km")
    for i in range(5):
        for j in range(2):
            if x[i][j].x > 0.5:  # x[i][j].x değeri 1'e yakınsa, yani seçilmişse
                print(f"Bölge {i + 1} öğrencileri Okul {j + 1}'e gitmelidir.")
else:
    print("Optimal çözüm bulunamadı.")
