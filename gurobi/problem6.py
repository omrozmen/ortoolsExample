from gurobipy import Model, GRB, quicksum
import os 
import os
os.chdir("./ortoolsExamples/gurobi")



# Parametreler
k = [3, 5, 5, 6, 2, 1, 1, 8, 6, 3, 2, 0, 0]   # Karbonhidrat değerleri
v = [1, 1, 1, 2, 4, 5, 2, 3, 3, 1, 1, 1, 1]   # Vitamin değerleri
p = [1, 2, 1, 1, 1, 1, 3, 5, 6, 1, 0, 0, 0]   # Protein değerleri
y = [0, 0, 0, 2, 1, 1, 1, 2, 1, 0, 0, 0, 0]   # Yağ değerleri
m = [0.10, 0.12, 0.13, 0.09, 0.10, 0.07, 0.70, 1.20, 0.63, 0.28, 0.42, 0.15, 0.12] # Maliyetler

# Gereksinimler
mink = 5   # Minimum karbonhidrat gereksinimi
minp = 10  # Minimum protein gereksinimi
miny = 8   # Minimum yağ gereksinimi
minv = 2   # Minimum vitamin gereksinimi

# Model oluştur
model = Model("Diyet Planı")

# Karar değişkenleri
x = [model.addVar(vtype=GRB.BINARY, name=f"x_{i+1}") for i in range(13)]

# Amaç fonksiyonu: Toplam maliyeti minimize et
model.setObjective(quicksum(m[i] * x[i] for i in range(13)), GRB.MINIMIZE)

# Kısıtlar

# Her yiyecek grubundan en az bir tane seçme kısıtları
model.addConstr(quicksum(x[i] for i in range(6)) >= 1, "Grup1")
model.addConstr(quicksum(x[i] for i in range(6, 9)) >= 1, "Grup2")
model.addConstr(quicksum(x[i] for i in range(9, 13)) >= 1, "Grup3")

# Besin gereksinimlerini karşılama kısıtları
model.addConstr(quicksum(k[i] * x[i] for i in range(13)) >= mink, "KarbonhidratGereksinimi")
model.addConstr(quicksum(p[i] * x[i] for i in range(13)) >= minp, "ProteinGereksinimi")
model.addConstr(quicksum(y[i] * x[i] for i in range(13)) >= miny, "YagGereksinimi")
model.addConstr(quicksum(v[i] * x[i] for i in range(13)) >= minv, "VitaminGereksinimi")

# Modeli optimize et
model.optimize()

# Çözümü yazdır
if model.status == GRB.OPTIMAL:
    print(f"Minimum maliyet: {model.objVal} TL")
    for i in range(13):
        if x[i].x > 0.5:  # Seçilen yiyecekler
            print(f"Yiyecek {i + 1} seçildi.")
else:
    print("Optimal çözüm bulunamadı.")
