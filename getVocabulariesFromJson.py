import json
import os

# Đọc dữ liệu từ file JSON
input_file = './FairyTail/FairyTail2.json'
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Tạo thư mục vocabulary nếu chưa tồn tại
output_dir = 'vocabulary'
os.makedirs(output_dir, exist_ok=True)

# Lưu kết quả vào file txt
output_file = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(input_file))[0]}_words.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    for item in data['words']:
        f.write(item['word'] + '\n')

print(f'Kết quả đã được lưu vào {output_file}')
