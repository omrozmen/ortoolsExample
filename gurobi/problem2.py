from gurobipy import Model, GRB
import os 
import os
os.chdir("./ortoolsExamples/gurobi")



# Model oluştur
m = Model("Parfum_Uretim_Optimizasyonu")

# Değişkenler
x1 = m.addVar(vtype=GRB.CONTINUOUS, name="x1")  # İlk proseste üretilen parfüm miktarı
x2 = m.addVar(vtype=GRB.CONTINUOUS, name="x2")  # İkinci proseste üretilen parfüm miktarı
x3 = m.addVar(vtype=GRB.CONTINUOUS, name="x3")  # Modelin çalıştığı saat miktarı

# Amaç Fonksiyonu
# z = 5(3x1 + 5x2) - 3(x1 + 2x2) - 2(2x1 + 3x2) - 100x3
m.setObjective(5 * (3 * x1 + 5 * x2) - 3 * (x1 + 2 * x2) - 2 * (2 * x1 + 3 * x2) - 100 * x3, GRB.MAXIMIZE)

# Kısıtlar
# İş gücü kısıtı: x1 + 2x2 <= 20000
m.addConstr(x1 + 2 * x2 <= 20000, "Is_Gucu_Kisiti")

# Kimyasal kısıtı: 2x1 + 3x2 <= 35000
m.addConstr(2 * x1 + 3 * x2 <= 35000, "Kimyasal_Kisiti")

# Talep kısıtı: x1 + x2 <= 1000 + 200 * x3
m.addConstr(x1 + x2 <= 1000 + 200 * x3, "Talep_Kisiti")

# Optimizasyonu çalıştır
m.optimize()

# Çözümü yazdır
if m.status == GRB.OPTIMAL:
    print(f"Optimal Kâr: {m.objVal} TL")
    print(f"x1 (İlk proseste üretilen parfüm miktarı): {x1.x} cl")
    print(f"x2 (İkinci proseste üretilen parfüm miktarı): {x2.x} cl")
    print(f"x3 (Modelin çalıştığı saat miktarı): {x3.x} saat")
else:
    print("Optimal çözüm bulunamadı.")
