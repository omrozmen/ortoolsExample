import random
import time
from ortools.constraint_solver import routing_enums_pb2, pywrapcp

def create_data_model(points):
    """Create a data model with a subset of points."""
    data = {
        'distance_matrix': [
            [0, 20, 25, 30, 15, 35, 25, 30, 45, 40],  # Sultanahmet Meydanı
            [20, 0, 10, 25, 20, 40, 30, 35, 50, 45],  # Galata Kulesi
            [25, 10, 0, 20, 30, 45, 35, 40, 55, 50],  # Taksim Meydanı
            [30, 25, 20, 0, 35, 50, 40, 45, 60, 55],  # Dolmabahçe Sarayı
            [15, 20, 30, 35, 0, 40, 30, 45, 55, 50],  # Kapalıçarşı
            [35, 40, 45, 50, 40, 0, 20, 25, 40, 35],  # Topkapı Sarayı
            [25, 30, 35, 40, 30, 20, 0, 15, 30, 25],  # Beyoğlu
            [30, 35, 40, 45, 45, 25, 15, 0, 15, 20],  # İstiklal Caddesi
            [45, 50, 55, 60, 55, 40, 30, 15, 0, 25],  # Boğaziçi Köprüsü
            [40, 45, 50, 55, 50, 35, 25, 20, 25, 0]   # Yıldız Parkı
        ],
        'points': points,
        'num_vehicles': 1,
        'depot': 0
    }
    return data

def ortools_solve(points):
    """Solve the TSP with OR-Tools and return the route and cost."""
    data = create_data_model(points)

    sub_matrix = [[data['distance_matrix'][i][j] for j in points] for i in points]
    data['distance_matrix'] = sub_matrix

    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)


        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        index = routing.Start(0)
        route = []
        route_cost = 0
        while not routing.IsEnd(index):
            route.append(points[manager.IndexToNode(index)])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_cost += routing.GetArcCostForVehicle(previous_index, index, 0)
        route.append(points[manager.IndexToNode(index)])
        return route, route_cost
    else:
        return None, float('inf')

def main():
    # Start timing
    start_time = time.time() * 1000
    
    points_list = [[0] + random.sample(range(1, 10), 5) for _ in range(3)]

    for idx, points in enumerate(points_list):
        print('\nRota {}:'.format(idx + 1))
        route, cost = ortools_solve(points)
        print("Seçilen Noktalar:", points)
        if route:
            print("Rota:", route)
            print("Toplam maliyet: {} dakika".format(cost))
        else:
            print("Çözüm bulunamadı!")
    
    # End timing and print the duration
    end_time = time.time() * 1000
    print("\nİşlemin Tamamlanma Süresi: {:.4f} mili_saniye".format(end_time - start_time))

if __name__ == '__main__':
    main()
