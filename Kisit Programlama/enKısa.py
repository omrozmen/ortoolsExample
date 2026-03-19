import gurobipy as gp
from gurobipy import GRB
import random
import pandas as pd
import os 
import os



distances = pd.read_csv("docs/mesafe_matrisi.csv", header=None)
print(distances, "   Distance")
# Turların başlangıç noktaları
starting_points = [0, 1, 2, 3, 4]

distance_matrix = distances.to_numpy()
def generate_routes(distance_matrix, num_routes, route_length):
    routes = []
    num_locations = len(distance_matrix)
    
    for _ in range(num_routes):
        route = random.sample(range(num_locations), route_length)
        # Son noktayı ilk noktaya eşitleyerek rotayı güncelle
        route.append(route[0])
        routes.append(route)
    
    return routes

def calculate_route_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        current_location = route[i]
        next_location = route[i + 1]
        total_distance += distance_matrix[current_location][next_location]
    return total_distance

# Rotaları oluştur
num_routes = 5
route_length = 6
routes = generate_routes(distance_matrix, num_routes, route_length)

# Oluşturulan rotaları yazdır
for i, route in enumerate(routes):
    print(f"Route {i+1}: {route[:-1]} -> {route[0]}")

# Tüm rotaların maliyetlerini adım adım hesaplayın ve yazdırın
for i, route in enumerate(routes):
    cumulative_cost = 0
    print(f"\nCumulative Cost for Route {i+1}:")
    for j in range(len(route) - 1):
        current_location = route[j]
        next_location = route[j + 1]
        distance = distance_matrix[current_location][next_location]
        cumulative_cost += distance
        print(f"Step {j+1}: Go from {current_location} to {next_location}, Distance: {distance}, Cumulative Cost: {cumulative_cost}")

# En kısa turu bulun
distances = [calculate_route_distance(route, distance_matrix) for route in routes]
shortest_route_index = distances.index(min(distances))
shortest_route = routes[shortest_route_index]
shortest_distance = distances[shortest_route_index]
print(f"\nShortest Route: {shortest_route[:-1]} -> {shortest_route[0]}")
print(f"Shortest Distance: {shortest_distance}")

