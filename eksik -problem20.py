from ortools.linear_solver import pywraplp
import os 
os.chdir("./ortoolsExamples")


# Solver oluşturma
solver = pywraplp.Solver.CreateSolver('CBC')
if not solver:
    raise Exception("Solver başlatılamadı.")

# Parametrelerin Tanımı (Problem boyutları)
ss = 23  # sınav sayısı
ds = 41  # derslik sayısı
gs = 10  # gün sayısı
zs = 40  # zaman aralığı sayısı
sfs = 4  # sınıf sayısı
zrs = 7  # zor sınav grubu sayısı
hs = 8  # öğretim elemanı sayısı

# Öğrenci Sayıları (Şekil 96'dan alınmıştır)
b = [195, 309, 278, 214, 207, 248, 215, 249, 204, 231, 247, 85, 259, 217, 92, 80, 70, 92, 177, 158, 56, 70, 62]

# Sınavın ait olduğu sınıf (Şekil 96'dan alınmıştır)
c = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]

# Derslik Kapasiteleri (Şekil 98'den alınmıştır)
a = [48, 45, 45, 48, 18, 93, 93, 93, 96, 66, 90, 93, 63, 93, 63, 66, 138, 141, 111, 141, 111, 114, 138, 108, 111, 
     186, 156, 223, 159, 226, 204, 226, 156, 223, 204, 271, 241, 244, 241, 289]

# Zor Sınav Grupları (Şekil 101'den alınmıştır)
e = [
    [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0],
    [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 1]
]

# Öğretim Üyesi Bilgisi (Şekil 102'den alınmıştır)
f = [
    [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0]
]

# Laboratuvar Dersleri (Şekil 103'den alınmıştır)
h = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Diğer satırlar laboratuvar dersi bilgilerine göre eklenmeli
]

# Karar Değişkenleri
x = {}
for i in range(ss):
    for j in range(ds):
        for k in range(zs):
            x[i, j, k] = solver.BoolVar(f'x[{i},{j},{k}]')

da = {}
for i in range(ss):
    da[i] = solver.IntVar(0, zs - 1, f'da[{i}]')

# Amaç Fonksiyonu: minimize sum(da[i])
solver.Minimize(solver.Sum(da[i] for i in range(ss)))
