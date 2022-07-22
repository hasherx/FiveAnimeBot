import json

mat_set = []
with open('mat.txt', 'r', encoding='utf-8') as mat:
    for i in mat.readlines():
        mat_set.append(i.strip().lower())

print(mat_set)

with open('../mat.json', 'w') as get_json:
    json.dump(mat_set, get_json)
