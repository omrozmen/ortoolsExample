from itertools import permutations
import os 


# Harfler ve rakamlar
letters = "SENDMORY"
digits = range(10)

# Benzersiz permütasyonları deneyelim
for perm in permutations(digits, len(letters)):
    s, e, n, d, m, o, r, y = perm

    # Kurallar: S ve M sıfır olamaz (iki basamaklı sayılar sıfırla başlamaz)
    if s == 0 or m == 0:
        continue

    # Sayıları oluştur
    send = 1000 * s + 100 * e + 10 * n + d
    more = 1000 * m + 100 * o + 10 * r + e
    money = 10000 * m + 1000 * o + 100 * n + 10 * e + y

    # Eğer denklem sağlanıyorsa çözüm bulundu
    if send + more == money:
        solution = {
            "SEND": send,
            "MORE": more,
            "MONEY": money,
            "Mapping": dict(zip(letters, perm)),
        }
        break
else:
    solution = None

print(solution)
