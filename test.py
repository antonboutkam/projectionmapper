import math

data = [
    [264, 29],
    [204, 61],
    [201, 63],
    [197, 66],
    [191, 71],
    [185, 77],
    [171, 94],
    [171, 99],
    [172, 101],
    [281, 222],
    [282, 223],
    [284, 223],
    [286, 222],
    [335, 187],
    [352, 173],
    [353, 172],
    [362, 162],
    [364, 159],
    [364, 150],
    [363, 145],
    [333, 76],
    [331, 72],
    [330, 71],
    [291, 44],
    [285, 40],
    [272, 32],
    [270, 31],
    [267, 30],
    [255, 29]
]

prev_row = None
for row in data:
    if prev_row is None:
        print("Set prev row ", row)
        prev_row = row
        continue

    dist = math.sqrt(math.pow(row[0] - prev_row[0], 2) + math.pow(row[1] - prev_row[1], 2))
    prev_row = row
    print("Distance:", row, prev_row, dist)
