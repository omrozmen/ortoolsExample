from ortools.linear_solver import pywraplp
import os 


# Verileri tanımla
cargo_weights = [18, 15, 23, 12]  # Kargo ağırlıkları
cargo_volumes = [480, 650, 580, 390]  # Kargo hacimleri
cargo_profits = [310, 380, 350, 285]  # Kargo başına karlar
section_weight_capacities = [10, 16, 8]  # Bölüm ağırlık kapasiteleri
section_volume_capacities = [6800, 8700, 5300]  # Bölüm hacim kapasiteleri

# Kargo ve bölüm sayıları
num_cargo = len(cargo_weights)
num_sections = len(section_weight_capacities)

# Optimizasyon problemini tanımla
solver = pywraplp.Solver.CreateSolver('GLOP')
if not solver:
    print("Solver bulunamadı.")
    exit()

# Karar değişkenlerini tanımla
x = {}
for i in range(num_cargo):
    for j in range(num_sections):
        x[i, j] = solver.NumVar(0, solver.infinity(), f'x[{i},{j}]')

# Amaç fonksiyonu: Toplam karı maksimize et
objective = solver.Objective()
for i in range(num_cargo):
    for j in range(num_sections):
        objective.SetCoefficient(x[i, j], cargo_profits[i])
objective.SetMaximization()

# Kısıtlar
# 1. Her kargo için bölümdeki ağırlık toplamı kargo ağırlığını aşmamalı
for i in range(num_cargo):
    solver.Add(sum(x[i, j] for j in range(num_sections)) <= cargo_weights[i])

# 2. Her bölümdeki toplam kargo ağırlığı, bölümün ağırlık kapasitesini aşmamalı
for j in range(num_sections):
    solver.Add(sum(x[i, j] for i in range(num_cargo)) <= section_weight_capacities[j])
    
# 3. Her bölümdeki toplam kargo hacmi, bölümün hacim kapasitesini aşmamalı
for j in range(num_sections):
    solver.Add(sum(x[i, j] * cargo_volumes[i] for i in range(num_cargo)) <= section_volume_capacities[j])

# 4. Denge kısıtı: Bölümler arası kargo dağılımının dengeli olması
for j in range(num_sections - 1):
    solver.Add(sum(x[i, j] / section_weight_capacities[j] for i in range(num_cargo)) ==
               sum(x[i, j + 1] / section_weight_capacities[j + 1] for i in range(num_cargo)))

# Çözümü bul
status = solver.Solve()

# Sonuçları yazdır
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal çözüm bulundu.')
    for i in range(num_cargo):
        for j in range(num_sections):
            print(f'Kargo {i + 1} bölüm {j + 1} için miktar: {x[i, j].solution_value()} ton')
    print('Maksimum kar:', objective.Value())
else:
    print('Optimal çözüm bulunamadı.')
