from ortools.linear_solver import pywraplp
import os 


# Solver oluştur
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    print("Solver bulunamadı.")
    exit(1)

# Parametreler
I = [1, 2]  # Ürün seti
J = list(range(1, 13))  # Ay seti

# Talep miktarları
t = {
    (1, 1): 10000, (1, 2): 10000, (1, 3): 10000, (1, 4): 10000,
    (1, 5): 30000, (1, 6): 30000, (1, 7): 30000, (1, 8): 30000,
    (1, 9): 30000, (1, 10): 100000, (1, 11): 100000, (1, 12): 100000,
    (2, 1): 50000, (2, 2): 50000, (2, 3): 15000, (2, 4): 15000,
    (2, 5): 15000, (2, 6): 15000, (2, 7): 15000, (2, 8): 15000,
    (2, 9): 15000, (2, 10): 50000, (2, 11): 50000, (2, 12): 50000
}

# Üretim maliyetleri
m = {
    (1, 1): 5, (1, 2): 5, (1, 3): 5, (1, 4): 5, (1, 5): 5, (1, 6): 5,
    (1, 7): 4.5, (1, 8): 4.5, (1, 9): 4.5, (1, 10): 4.5, (1, 11): 4.5, (1, 12): 4.5,
    (2, 1): 8, (2, 2): 8, (2, 3): 8, (2, 4): 8, (2, 5): 8, (2, 6): 8,
    (2, 7): 7, (2, 8): 7, (2, 9): 7, (2, 10): 7, (2, 11): 7, (2, 12): 7
}

# Maksimum üretim miktarı
u = {
    1: 120000, 2: 120000, 3: 120000, 4: 120000,
    5: 120000, 6: 120000, 7: 120000, 8: 120000,
    9: 120000, 10: 150000, 11: 150000, 12: 150000
}

# Stok maliyeti ve alanı
stok_maliyeti = 0.10
maks_alan = 150000
alan = {1: 2, 2: 4}

# Karar Değişkenleri
x = {}  # Üretim miktarı
I = {}  # Stok miktarı

for i in [1, 2]:
    for j in range(1, 13):
        x[(i, j)] = solver.IntVar(0, solver.infinity(), f'x_{i}_{j}')
        I[(i, j)] = solver.IntVar(0, solver.infinity(), f'I_{i}_{j}')

# Amaç Fonksiyonu: Toplam üretim ve stok maliyeti
solver.Minimize(solver.Sum(m[(i, j)] * x[(i, j)] for i in [1, 2] for j in range(1, 13)) +
                (stok_maliyeti * solver.Sum( I[(i, j)] for i in [1, 2] for j in range(1, 13))))

# Kısıtlar
# 1) Aylık maksimum üretim kısıtları
for j in range(1, 13):
    solver.Add(solver.Sum(x[(i, j)] for i in [1, 2]) <= u[j])

# 2) Stok kısıtları
for i in [1, 2]:
    for j in range(1, 13):
        if j == 1:
            solver.Add(I[(i, j)] == x[(i, j)] - t[(i, j)])
        else:
            solver.Add(I[(i, j)] == I[(i, j-1)] + x[(i, j)] - t[(i, j)])

# 3) Stok alanı kısıtları
for j in range(1, 13):
    solver.Add(solver.Sum(alan[i] * I[(i, j)] for i in [1, 2]) <= maks_alan)

# Çözümü bul
status = solver.Solve()

# Çözüm Durumu
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu:')
    print(f'Toplam maliyet: {solver.Objective().Value()}')
    for i in [1, 2]:
        for j in range(1, 13):
            print(f'Ürün {i}, Ay {j}: Üretim={x[(i, j)].solution_value()}, Stok={I[(i, j)].solution_value()}')
  
