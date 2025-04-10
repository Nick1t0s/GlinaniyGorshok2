a=[4, 5, 6, 7, 7, 7, 6, 5, 4, 2, 1, 0, 0, 0, 1, 2]
a = list(map(bin, a))
b = []
for i in a:
    x = list(i[2:6])
    b.append(list(map(int, x)))
print(str(b).replace("[", "{").replace("]","}"))