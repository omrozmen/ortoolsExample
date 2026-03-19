from pulp import *
import os 
import os
os.chdir("./ortoolsExamples/Kisit Programlama")



# Model oluşturma
model = LpProblem("Depo_Optimizasyonu", LpMinimize)

# Depo isimleri ve kapasiteleri
depolar = ['A', 'B', 'C']
kapasiteler = {'A': 100, 'B': 150, 'C': 200}

# Ürün talepleri
talepler = {'Ürün1': 50, 'Ürün2': 70, 'Ürün3': 100}

# Depolama maliyetleri
maliyetler = {'A': {'Ürün1': 5, 'Ürün2': 7, 'Ürün3': 6},
              'B': {'Ürün1': 6, 'Ürün2': 8, 'Ürün3': 7},
              'C': {'Ürün1': 7, 'Ürün2': 6, 'Ürün3': 9}}

# Değişkenler
depolama = LpVariable.dicts("Depolama", [(i, j) for i in talepler.keys() for j in depolar], lowBound=0, cat='Integer')

# Obje fonksiyonu
model += lpSum([depolama[i,j] * maliyetler[j][i] for i in talepler.keys() for j in depolar])

# Kısıtlar
for i in talepler.keys():
    model += lpSum([depolama[i,j] for j in depolar]) == talepler[i]
    
for j in depolar:
    model += lpSum([depolama[i,j] for i in talepler.keys()]) <= kapasiteler[j]

# Modeli çöz
model.solve()

# Sonuçları yazdır
for v in model.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
        
print("Toplam Maliyet =", value(model.objective))
