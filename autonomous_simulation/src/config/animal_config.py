

#Case gereksinimlerine göre
INITIAL_ANIMALS = {
    'sheep': {'male': 15, 'female': 15},    # 30 koyun (15 erkek, 15 dişi)
    'cow': {'male': 5, 'female': 5},        # 10 inek (5 erkek, 5 dişi)
    'chicken': {'male': 10, 'female': 10},  # 20 tavuk/horoz (10 erkek horoz, 10 dişi tavuk)
    'wolf': {'male': 5, 'female': 5},       # 10 kurt (5 erkek, 5 dişi)
    'lion': {'male': 4, 'female': 4},       # 8 aslan (4 erkek, 4 dişi)
    'hunter': {'male': 1, 'female': 0}      # 1 avcı
}

# 
ANIMAL_SPEEDS = {
    'sheep': 2,
    'cow': 2,
    'chicken': 1,  
    'wolf': 3,
    'lion': 4,
    'hunter': 1
}

# Hunt ranges
HUNT_RANGES = {
    'wolf': 4,
    'lion': 5,
    'hunter': 8
}