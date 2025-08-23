import hashlib 
import json

with open('raw_data.json', 'r') as f_in:
    documents = json.load(f_in)

def generate_id(record):
    text = f"{record['type']} | {record['term']}"
    return hashlib.md5(text.encode()).hexdigest()

processed_data = []
for record in documents:
    unique_id = generate_id(record)
    record['id'] = unique_id
    processed_data.append(record)

with open('Data/data.json', 'w') as f_out:
    json.dump(processed_data, f_out, indent=2, ensure_ascii=False)

