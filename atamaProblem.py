from ortools.linear_solver import pywraplp
import os 
os.chdir("./ortoolsExamples")


# Örnek maliyet matrisi
cost_matrix = [
    [90, 75, 75, 80],  # 1. kişi için maliyetler
    [35, 85, 55, 65],  # 2. kişi için maliyetler
    [125, 95, 90, 105],  # 3. kişi için maliyetler
    [45, 110, 95, 115]  # 4. kişi için maliyetler
]

num_workers = len(cost_matrix)
num_tasks = len(cost_matrix[0])

# OR-Tools çözücü oluşturuluyor
solver = pywraplp.Solver.CreateSolver('SCIP')

# Değişkenleri tanımlıyoruz
x = {}
for i in range(num_workers):
    for j in range(num_tasks):
        x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')

# Her görevin yalnızca bir kişiye atanması kısıtı
for i in range(num_workers):
    solver.Add(sum(x[i, j] for j in range(num_tasks)) == 1)

# Her kişinin yalnızca bir görevi üstlenmesi kısıtı
for j in range(num_tasks):
    solver.Add(sum(x[i, j] for i in range(num_workers)) == 1)

# Amaç fonksiyonu: toplam maliyeti minimize etmek
objective = solver.Sum(cost_matrix[i][j] * x[i, j] for i in range(num_workers) for j in range(num_tasks))
solver.Minimize(objective)

# Çözümü bulalım
status = solver.Solve()

# Çözüm sonuçlarını alalım
solution = []
if status == pywraplp.Solver.OPTIMAL:
    total_cost = solver.Objective().Value()
    for i in range(num_workers):
        for j in range(num_tasks):
            if x[i, j].solution_value() > 0:
                solution.append((i, j, cost_matrix[i][j]))
    print("Toplam Maliyet:", total_cost)
    print("Atamalar ve Maliyetler:", solution)
else:
    print("Optimal çözüm bulunamadı.")


