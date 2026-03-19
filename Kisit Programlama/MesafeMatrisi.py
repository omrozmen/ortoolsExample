import numpy as np
import random
import gurobipy as gp
from gurobipy import GRB

# Rastgele 10 nokta oluşturma
num_points = 10
points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_points)]
points = np.round(points ).astype(int)

# Turları oluştur
tours = []
for _ in range(2):
    tour_size = random.randint(6, 7)  # En az 6 nokta
    tour = random.sample(range(num_points), tour_size)
    tours.append(tour)
for _ in range(3):
    tour_size = random.randint(6, 8)  # En az 6 nokta
    tour = random.sample(range(num_points), tour_size)
    tours.append(tour)

# Mesafe matrisini oluştur
distances = np.zeros((num_points, num_points))
for i in range(num_points):
    for j in range(num_points):
        distances[i][j] = np.round(np.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2))

# Her bir tur için mesafeyi hesapla
tour_distances = []
for tour in tours:
    tour_distance = sum(distances[tour[i]][tour[i+1]] for i in range(len(tour)-1))
    tour_distance += distances[tour[-1]][tour[0]]  # Dönüş mesafesi
    tour_distances.append(tour_distance)

# Tur mesafelerini ve nokta sayılarını yazdır
print("Turların Mesafeleri ve Nokta Sayıları:")
for i, (tour, distance) in enumerate(zip(tours, tour_distances)):
    print("Tur {}: Nokta Sayısı = {}, Mesafe = {:.2f}".format(i+1, len(tour), distance))






# Mesafe matrisi, turlar ve toplam mesafeleri içeren metin dosyasını oluştur
with open("mesafe_ve_turlar.txt", "w") as file:
    # Mesafe matrisini dosyaya yaz
    file.write("Mesafe Matrisi:\n")
    for i in range(num_points):
        for j in range(num_points):
            file.write("{:.2f}\t".format(distances[i][j]))
        file.write("\n")

    # Turları ve toplam mesafeleri dosyaya yaz
    file.write("\nSeçilen Turlar, Nokta Sayıları, Noktalar ve Toplam Mesafeler:\n")
    for i, (tour, distance) in enumerate(zip(tours, tour_distances)):
        file.write("Tur {}: Nokta Sayısı = {}, Toplam Mesafe = {:.2f}\n".format(i+1, len(tour), distance))
        file.write("Noktalar: ")
        
        # Turu adım adım takip ederek her bir adımda toplam mesafeyi kümülatif olarak hesapla
        total_distance = 0
        for index, point_index in enumerate(tour):
            if index == 0:
                file.write("{} (Başlangıç) ".format(point_index + 1))
            else:
                # Noktalar arası mesafeyi hesapla
                distance_to_previous_point = distances[tour[index - 1]][point_index]
                total_distance += distance_to_previous_point
                file.write("{} ({:.2f} birim, Toplam {:.2f} birim) ".format(point_index + 1, distance_to_previous_point, total_distance))
        file.write("\n\n")





import pandas as pd



# Mesafe matrisini DataFrame'e dönüştür
df_distances = pd.DataFrame(distances)

# DataFrame'i CSV dosyasına yaz
df_distances.to_csv("mesafe_matrisi_eski.csv", index=False, header=False)
