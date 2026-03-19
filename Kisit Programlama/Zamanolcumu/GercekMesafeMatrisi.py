import pandas as pd
import numpy as np
from geopy.distance import geodesic
import ast





locations = [
    ("Sultanahmet Camii", (41.0055, 28.9768)),
    ("Topkapı Sarayı", (41.0086, 28.9816)),
    ("Ayasofya Müzesi", (41.0086, 28.9802)),
    ("Kapalıçarşı", (41.0106, 28.9689)),
    ("Galata Kulesi", (41.0256, 28.9744)),
    ("İstiklal Caddesi", (41.0315, 28.9766)),
    ("Taksim Meydanı", (41.0369, 28.9863)),
    ("Dolmabahçe Sarayı", (41.0390, 29.0006)),
    ("Yerebatan Sarnıcı", (41.0086, 28.9770)),
    ("Pierre Loti Tepesi", (41.0530, 28.9384)),
    ("Rahmi Koç Müzesi", (41.0419, 28.9496)),
    ("Miniatürk", (41.0601, 28.9489)),
    ("Emirgan Korusu", (41.1057, 29.0557)),
    ("Rumeli Hisarı", (41.0845, 29.0562)),
    ("Kız Kulesi", (41.0211, 29.0041)),
    ("Beylerbeyi Sarayı", (41.0420, 29.0433)),
    ("Çamlıca Tepesi", (41.0240, 29.0790)),
    ("Adalar", (40.8750, 29.1200)),
    ("Kadıköy", (40.9830, 29.0170)),
    ("Moda Sahil Parkı", (40.9794, 29.0263)),
]



with open('random_locations.txt', 'r') as file:
    data = file.read()

# Sahte Lokasyonları almak için
# locations = ast.literal_eval(data)



distMatrix = np.zeros((len(locations), len(locations)))

for i in range(len(locations)):
    for j in range(len(locations)):
        distMatrix[i, j] = geodesic(locations[i][1], locations[j][1]).kilometers


distMatrixDistance = np.round(distMatrix * 1000)


distMatrixDistance_ = pd.DataFrame(distMatrixDistance, index=[loc[0] for loc in locations], columns=[loc[0] for loc in locations])

# Sahte verileri CSV dosyasına kaydetme
# dist_df_meters.to_csv('SAHTE.csv')



distMatrixDistance_.to_csv('istanbul_gezi_noktalari_mesafe_matrisi.csv')

print(distMatrixDistance_.head())
