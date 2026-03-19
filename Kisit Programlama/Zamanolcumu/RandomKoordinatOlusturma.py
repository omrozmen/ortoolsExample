import random


def generate_random_coordinates(number_of_points=15):
    # İstanbul'un yaklaşık sınırları
    minLatitude = 40.8025
    maxLatitude = 41.2425
    minLongitude = 28.5525
    maxLongitude = 29.1050

    coordinates = []
    for _ in range(number_of_points):
        latitude = random.uniform(minLatitude, maxLatitude)
        longitude = random.uniform(minLongitude, maxLongitude)
        coordinates.append((latitude, longitude))
    
    return coordinates


randomCoordinates = generate_random_coordinates()


formattedLocations = "locations=["
formattedLocations += ",".join([f'("nokta{i+1}", ({lat}, {lon}))' for i, (lat, lon) in enumerate(randomCoordinates)])
formattedLocations += "]"


with open('random_locations.txt', 'w') as file:
    file.write(formattedLocations)

print("Koordinatlar 'random_locations.txt' dosyasına kaydedildi.")
