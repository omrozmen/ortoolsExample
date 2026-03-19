import gurobipy as gp
from gurobipy import GRB
import random




# Mesafeler metre cinsinden alınmıştır.
istanbulGezi = [
    "Sultanahmet Camii",
    "Topkapı Sarayı",
    "Ayasofya Müzesi",
    "Kapalıçarşı",
    "Galata Kulesi",
    "İstiklal Caddesi",
    "Taksim Meydanı",
    "Dolmabahçe Sarayı",
    "Yerebatan Sarnıcı",
    "Pierre Loti Tepesi",
    "Rahmi Koç Müzesi",
    "Miniatürk",
    "Emirgan Korusu",
    "Rumeli Hisarı",
    "Kız Kulesi",
    "Beylerbeyi Sarayı",
    "Çamlıca Tepesi",
    "Adalar",
    "Kadıköy",
    "Moda Sahil Parkı"
]


def CreateData():
    """Veri modelini oluştur."""
    data = {
        'distance_matrix': [
    [0, 531, 448, 873, 2241, 2887, 3577, 4225, 345, 6185, 4645, 6502, 12954, 11024, 2877, 6907, 8839, 18853, 4205, 5074],
    [531, 0, 118, 1091, 1983, 2578, 3168, 3735, 387, 6125, 4574, 6346, 12453, 10507, 2347, 6379, 8369, 18867, 4118, 4966],
    [448, 118, 0, 976, 1950, 2561, 3184, 3787, 269, 6056, 4505, 6296, 12513, 10577, 2443, 6475, 8485, 18940, 4204, 5056],
    [873, 1091, 976, 0, 1729, 2410, 3267, 4130, 717, 5362, 3836, 5749, 12837, 11010, 3182, 7163, 9380, 19714, 5077, 5944],
    [2241, 1983, 1950, 1729, 0, 681, 1605, 2659, 1901, 4292, 2762, 4391, 11217, 9491, 2547, 6073, 8799, 20736, 5935, 6737],
    [2887, 2578, 2561, 2410, 681, 0, 1012, 2183, 2543, 4002, 2547, 3939, 10588, 8912, 2585, 5729, 8652, 21162, 6369, 7139],
    [3577, 3168, 3184, 3267, 1605, 1012, 0, 1225, 3239, 4406, 3135, 4065, 9612, 7904, 2306, 4826, 7926, 21212, 6519, 7218],
    [4225, 3735, 3787, 4130, 2659, 2183, 1225, 0, 3916, 5456, 4300, 4938, 8736, 6883, 2010, 3606, 6800, 20803, 6370, 6963],
    [345, 387, 269, 717, 1901, 2543, 3239, 3916, 0, 5903, 4357, 6188, 12651, 10742, 2669, 6697, 8748, 19108, 4406, 5265],
    [6185, 6125, 6056, 5362, 4292, 4002, 4406, 5456, 5903, 0, 1551, 1184, 11464, 10501, 6563, 8904, 12253, 24989, 10205, 11022],
    [4645, 4574, 4505, 3836, 2762, 2547, 3135, 4300, 4357, 1551, 0, 2022, 11389, 10133, 5132, 7878, 11062, 23438, 8656, 9477],
    [6502, 6346, 6296, 5749, 4391, 3939, 4065, 4938, 6188, 1184, 2022, 0, 10305, 9416, 6348, 8187, 11651, 25099, 10301, 11077],
    [12954, 12453, 12513, 12837, 11217, 10588, 9612, 8736, 12651, 11464, 11389, 10305, 0, 2355, 10348, 7151, 9282, 26185, 14010, 14242],
    [11024, 10507, 10577, 11010, 9491, 8912, 7904, 6883, 10742, 10501, 10133, 9416, 2355, 0, 8292, 4843, 6987, 23877, 11744, 11940],
    [2877, 2347, 2443, 3182, 2547, 2585, 2306, 2010, 2669, 6563, 5132, 6348, 10348, 8292, 0, 4032, 6308, 18934, 4368, 4993],
    [6907, 6379, 6475, 7163, 6073, 5729, 4826, 3606, 6697, 8904, 7878, 8187, 7151, 4843, 4032, 0, 3607, 19638, 6916, 7098],
    [8839, 8369, 8485, 9380, 8799, 8652, 7926, 6800, 8748, 12253, 11062, 11651, 9282, 6987, 6308, 3607, 0, 16903, 6924, 6648],
    [18853, 18867, 18940, 19714, 20736, 21162, 21212, 20803, 19108, 24989, 23438, 25099, 26185, 23877, 18934, 19638, 16903, 0, 14802, 14025],
    [4205, 4118, 4204, 5077, 5935, 6369, 6519, 6370, 4406, 10205, 8656, 10301, 14010, 11744, 4368, 6916, 6924, 14802, 0, 879],
    [5074, 4966, 5056, 5944, 6737, 7139, 7218, 6963, 5265, 11022, 9477, 11077, 14242, 11940, 4993, 7098, 6648, 14025, 879, 0]
]
,
        'num_vehicles': 1,
        'depot': 0
    }
    return data

def gurobi_solver(data, points):
    n = len(points)
    subMatrix = [[data['distance_matrix'][i][j] for j in points] for i in points]
    
    m = gp.Model()

    # Değişkenler: x[i, j] ve u[i]
    x = m.addVars(n, n, vtype=GRB.BINARY, name="x")
    u = m.addVars(n, vtype=GRB.CONTINUOUS, name="u")

    # Amaç fonksiyonu
    m.setObjective(gp.quicksum(subMatrix[i][j] * x[i, j] for i in range(n) for j in range(n)), GRB.MINIMIZE)

    # Kısıtlar:
    # Her düğüme gelen ve giden tek bir kenar olmalı
    for i in range(n):
        m.addConstr(gp.quicksum(x[i, j] for j in range(n) if j != i) == 1)
        m.addConstr(gp.quicksum(x[j, i] for j in range(n) if j != i) == 1)

    # Alt tur kısıtlamaları
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                m.addConstr(u[i] - u[j] + n * x[i, j] <= n - 1)

    # Optimize et
    m.optimize()

    if m.status == GRB.OPTIMAL:
        route = []
        for i in range(n):
            for j in range(n):
                if x[i, j].X > 0.5:
                    route.append((i, j))
        
        # Rota ve maliyet hesaplama
        ordered_route = [0]
        while len(ordered_route) < n:
            for i, j in route:
                if i == ordered_route[-1]:
                    ordered_route.append(j)
                    break
        route_cost = m.ObjVal
        return ordered_route, route_cost, subMatrix
    else:
        return None, float('inf'), None

def print_route_details(route, cost, subMatrix, points, route_index):
    if route:
        print(f"\nRota {route_index + 1}:")
        print("Seçilen Noktalar:", [istanbulGezi[point] for point in points])
        print("Rota:", [istanbulGezi[points[i]] for i in route])
        print("Toplam maliyet: {} metre".format(cost))
        print("Mesafeler:")
        for i in range(len(route) - 1):
            print(f"{istanbulGezi[points[route[i]]]} -> {istanbulGezi[points[route[i + 1]]]}: {subMatrix[route[i]][route[i + 1]]} metre")
    else:
        print(f"\nRota {route_index + 1}: Çözüm bulunamadı!")

def shortest_route(pointsList, data):
    minRoute = None
    minCost = float('inf')
    minRoutePoints = None
    minSubMatrix = None

    for idx, points in enumerate(pointsList):
        route, cost, subMatrix = gurobi_solver(data, points)
        if route is not None and cost < minCost:
            minRoute = route
            minCost = cost
            minRoutePoints = points
            minSubMatrix = subMatrix

    return minRoute, minCost, minRoutePoints, minSubMatrix

def main():
    data = CreateData()
    pointsList = []
    for i in range(5):
        points = random.sample(range(1, len(istanbulGezi)), 5)
        points = [0] + points
        pointsList.append(points)

    # Her bir rotayı ayrı ayrı yazdır
    for idx, points in enumerate(pointsList):
        route, cost, subMatrix = gurobi_solver(data, points)
        print_route_details(route, cost, subMatrix, points, idx)

    # En kısa rotayı belirle ve yazdır
    minRoute, minCost, minRoutePoints, minSubMatrix = shortest_route(pointsList, data)
    if minRoute:
        print("\nEn Kısa Rota Sonucu:")
        print("En Kısa Rota:", [istanbulGezi[minRoutePoints[i]] for i in minRoute])
        print("En Kısa Rota Maliyeti: {} metre".format(minCost))
        print("Mesafeler:")
        for i in range(len(minRoute) - 1):
            print(f"{istanbulGezi[minRoutePoints[minRoute[i]]]} -> {istanbulGezi[minRoutePoints[minRoute[i + 1]]]}: {minSubMatrix[minRoute[i]][minRoute[i + 1]]} metre")
    else:
        print("En Kısa Rota Sonucu: Çözüm bulunamadı!")

if __name__ == '__main__':
    main()
