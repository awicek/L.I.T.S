from collections import defaultdict
values = [[7, 6], [6, 5], [1, 7], [5, 5], [5, 6], [7, 4], [9, 6], [6, 7], [5, 5], [6, 1], [9, 9], [6, 7], [3, 5]]
a = defaultdict()
a[0] = [0,1,9,3]
a[1] = [0,1,2,9,10]
a[2] = [1,10,5,2]
a[3] = [0,9,11,6,3]
a[4] = [9,10,11,12,4]
a[5] = [10,12,2,8,5]
a[6] = [3,11,7,6]
a[7] = [6,11,12,8,7]
a[8] = [7,12,4,8]
a[9] = [0,1,4,3,9]
a[10] = [1,2,4,5,10]
a[11] = [3,4,6,7,11]
a[12] = [4,5,7,8,12]
maxdif = 0

for i in a[0]:
    maxdif += (values[i][1] - values[i][0])
index = 0
for i  in range(len(values)):
    sum = 0
    for k in a[i]:
        sum += values[k][1] -values[k][0]
    sum = (sum / len(a[i])) * 5
    print(sum)
    if sum > maxdif:
        maxdif = sum
        index = i
print(index)