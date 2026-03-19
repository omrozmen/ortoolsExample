import gurobipy as gp
from gurobipy import GRB
import os 



# Model oluşturma
model = gp.Model("SendMoreMoney")

# Harflere karşılık gelen değişkenler
letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
variables = {}
for letter in letters:
    variables[letter] = model.addVar(lb=0, ub=9, vtype=GRB.INTEGER, name=letter)

# Kısıtlar
model.addConstr(variables['S'] * 10**3 + variables['E'] * 10**2 + variables['N'] * 10**1 + variables['D'] +
                variables['M'] * 10**3 + variables['O'] * 10**2 + variables['R'] * 10**1 + variables['E'] ==
                variables['M'] * 10**4 + variables['O'] * 10**3 + variables['N'] * 10**2 + variables['E'] * 10**1 + variables['Y'])

# Sıfır ile başlayamaz kısıtları
model.addConstr(variables['S'] >= 1)
model.addConstr(variables['M'] >= 1)

# Optimizasyonu çözme
model.optimize()

# Çözümü yazdırma
if model.status == GRB.OPTIMAL:
    solution = ""
    for letter in letters:
        solution += letter + " = " + str(round(variables[letter].x, 2)) + "\n"
    print(solution)
    print("SEND =", round(variables['S'].x * 10**3 + variables['E'].x * 10**2 + variables['N'].x * 10**1 + variables['D'].x))
    print("MORE =", round(variables['M'].x * 10**3 + variables['O'].x * 10**2 + variables['R'].x * 10**1 + variables['E'].x))
    print("MONEY =", round(variables['M'].x * 10**4 + variables['O'].x * 10**3 + variables['N'].x * 10**2 + variables['E'].x * 10**1 + variables['Y'].x))
else:
    print("Optimal çözüm bulunamadı.")
