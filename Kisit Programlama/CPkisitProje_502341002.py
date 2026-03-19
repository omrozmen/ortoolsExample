import random
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
import time


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



def CreateData(points):
    """Create a data model with a subset of points."""
    data = {
        'distance_matrix': 
[
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
],

        'points': points,
        'num_vehicles': 1,
        'depot': 0
    }
    return data

def OrtoolsSolver(points):
    """Solve the TSP with OR-Tools and return the route and cost."""
    data = CreateData(points)

    subMatrix = [[data['distance_matrix'][i][j] for j in points] for i in points]
    data['distance_matrix'] = subMatrix

    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(fromIndex, toIndex):
        fromNode = manager.IndexToNode(fromIndex)
import os 
import os

        toNode = manager.IndexToNode(toIndex)
        return data['distance_matrix'][fromNode][toNode]

    transitCallbackIndex = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transitCallbackIndex)

    searchParameters = pywrapcp.DefaultRoutingSearchParameters()
    searchParameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(searchParameters)

    if solution:
        index = routing.Start(0)
        route = []
        routeCost = 0
        while not routing.IsEnd(index):
            route.append(points[manager.IndexToNode(index)])
            previousIndex = index
            index = solution.Value(routing.NextVar(index))
            routeCost += routing.GetArcCostForVehicle(previousIndex, index, 0)
        route.append(points[manager.IndexToNode(index)])
        return route, routeCost
    else:
        return None, float('inf')

def ShortestRoute(pointsList):
    """Find the shortest route among multiple sets using OR-Tools."""
    minRoute = None
    minCost = float('inf')
    
    for points in pointsList:
        route, cost = OrtoolsSolver(points)
        if route is not None and cost < minCost:
            minRoute = route
            minCost = cost

    print("\nEn Kısa Rota Sonucu:")
    print("En Kısa Rota:", minRoute)
    print("En Kısa Rota Maliyeti: {} metre".format(minCost))

def main():

    pointsList = []
    for i in range (5):
        points = random.sample(range(1, len(istanbulGezi)), 5)
        points = [0] + points
        pointsList.append(points)

    for idx, points in enumerate(pointsList):
        print('\nRota {}:'.format(idx + 1))
        route, cost = OrtoolsSolver(points)
        print("Seçilen Noktalar:", points)
        if route:
            print("Rota:", route)
            print("Toplam maliyet: {} metre".format(cost))
        else:
            print("Çözüm bulunamadı!")

    ShortestRoute(pointsList)

if __name__ == '__main__':
    main()


