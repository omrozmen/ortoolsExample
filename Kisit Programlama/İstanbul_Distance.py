import numpy as np
import pandas as pd
from geopy.distance import geodesic
import os 
import os



# İstanbul'daki popüler noktalar ve eklenen üç yeni gezilecek noktanın koordinatları
istanbul_places = {
    "Ayasofya": (41.0086, 28.9770),
    "Süleymaniye": (41.0168, 28.9647),
    "Çengelköy": (41.0562, 29.0572),
    "Bebek": (41.0876, 29.0354),
    "Aşiyan": (41.0839, 29.0397),
    "Rumeli Hisarı": (41.0903, 29.0544),
    "Anadolu Hisarı": (41.0689, 29.0417),
    "Kız Kulesi": (41.0226, 29.0057),
    "Ortaköy": (41.0534, 29.0327),
    "Galata Kulesi": (41.0257, 28.9744),
    "Eminönü": (41.0097, 28.9769),
    "Levent": (41.0822, 29.0144),
    "Kadıköy": (40.9919, 29.0277),
    "Beşiktaş": (41.0421, 29.0079),
    "İstanbul Arkeoloji Müzeleri": (41.0124, 28.9802),  # Yeni gezilecek nokta
    "Topkapı Sarayı Müzesi": (41.0115, 28.9834),  # Yeni gezilecek nokta
    "Dolmabahçe Sarayı": (41.0391, 29.0018),  # Yeni gezilecek nokta
}

# Noktalar arasındaki mesafeleri hesaplayan bir fonksiyon
def calculate_distances(locations):
    num_points = len(locations)
    distance_matrix = np.zeros((num_points, num_points))

    for i, (name1, loc1) in enumerate(locations.items()):
        for j, (name2, loc2) in enumerate(locations.items()):
            distance_matrix[i, j] = round(geodesic(loc1, loc2).kilometers, 2)  # Mesafeleri yuvarla

    return distance_matrix

# Mesafe matrisini hesapla
distance_matrix = calculate_distances(istanbul_places)

# Mesafe matrisini DataFrame'e dönüştür
distance_df = pd.DataFrame(distance_matrix, columns=istanbul_places.keys(), index=istanbul_places.keys())

# CSV dosyasına yazdır
distance_df.to_csv("istanbul_distance_matrix_gezilecek.csv")

# Sonucu göster
print("Yuvarlanmış Mesafe Matrisi (Kilometre cinsinden):")
print(distance_df)
print("\nYuvarlanmış mesafe matrisi başarıyla 'istanbul_distance_matrix_gezilecek.csv' dosyasına yazıldı.")
