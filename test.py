import json

with open('datasets/coco_predictions.json', 'r') as f:
    json_data = json.load(f)

print(json.dumps(json_data))