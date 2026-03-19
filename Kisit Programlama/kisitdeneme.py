import gurobipy as gp
from gurobipy import GRB
import os 
import os



# Çalışanlar ve projeler
calisanlar = ['X', 'Y', 'Z', 'W']
projeler = ['A', 'B', 'C']

# Proje maliyetleri
proje_maliyetleri = {
    ('A', 'X'): 100,
    ('A', 'Y'): 150,
    ('A', 'Z'): 120,
    ('A', 'W'): 110,
    ('B', 'X'): 130,
    ('B', 'Y'): 100,
    ('B', 'Z'): 140,
    ('B', 'W'): 120,
    ('C', 'X'): 110,
    ('C', 'Y'): 120,
    ('C', 'Z'): 100,
    ('C', 'W'): 130
}

# Model oluşturma
model = gp.Model('Atama_Problemi')

# Değişkenler oluşturma
atama = model.addVars(projeler, calisanlar, vtype=GRB.BINARY, name='Atama')

# Amaç fonksiyonu
model.setObjective(sum(proje_maliyetleri[proje, calisan] * atama[proje, calisan] for proje in projeler for calisan in calisanlar), GRB.MINIMIZE)

# Her projeye sadece bir çalışan atanabilir kısıtı
model.addConstrs((sum(atama[proje, calisan] for calisan in calisanlar) == 1 for proje in projeler), name='Her_Projeye_Bir_Calisan')

# Her çalışan en fazla bir projede çalışabilir kısıtı
model.addConstrs((sum(atama[proje, calisan] for proje in projeler) <= 1 for calisan in calisanlar), name='Her_Calisana_Bir_Proje')

# Modeli çözme
model.optimize()

# Sonuçları yazdırma
if model.status == GRB.OPTIMAL:
    print('Optimal Çözüm Bulundu:')
    for proje in projeler:
        for calisan in calisanlar:
            if atama[proje, calisan].x > 0.5:
                print(f"{calisan} proje {proje}'ye atanmıştır. Maliyet: {proje_maliyetleri[proje, calisan]}")
else:
    print('Optimal çözüm bulunamadı.')
