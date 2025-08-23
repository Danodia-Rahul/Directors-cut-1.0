import hashlib
import json
import sys

def generate_id(record):
    text = f"{record['type']} | {record['term']}"
    return hashlib.md5(text.encode()).hexdigest()

with open('Data/raw_data.json', 'r', encoding='utf-8') as f_in:
    documents = json.load(f_in)

processed_data = []
seen_ids = set()

for record in documents:
    unique_id = generate_id(record)

    if unique_id in seen_ids:
        print(f"❌ Duplicate ID found: {unique_id} for record: {record}", file=sys.stderr)
        sys.exit(1)

    seen_ids.add(unique_id)
    record['id'] = unique_id
    processed_data.append(record)

with open('Data/data.json', 'w', encoding='utf-8') as f_out:
    json.dump(processed_data, f_out, indent=2, ensure_ascii=False)

print(f"✅ All {len(processed_data)} IDs are unique. Data saved to Data/data.json.")
