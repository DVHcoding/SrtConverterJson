import os
import re
import json
from flask import Flask, request, send_file, render_template

app = Flask(__name__)

def parse_srt(srt_file):
    with open(srt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    subtitles = []
    index = 0
    total_lines = len(lines)
    
    while index < total_lines:
        if lines[index].strip() == "":
            index += 1
            continue
        
        index += 1
        time_line = lines[index].strip()
        start_time, end_time = re.split(r' --> ', time_line)
        start_time = start_time.replace(',', '.')
        end_time = end_time.replace(',', '.')
        index += 1
        
        def time_to_seconds(t):
            parts = re.split(r':|\.', t)
            h = float(parts[0]) if len(parts) > 0 else 0
            m = float(parts[1]) if len(parts) > 1 else 0
            s = float(parts[2]) if len(parts) > 2 else 0
            ms = float(parts[3]) if len(parts) > 3 else 0
            return round(h * 3600 + m * 60 + s + ms / 1000, 3)

        start_sec = time_to_seconds(start_time)
        end_sec = time_to_seconds(end_time)
        duration = round(end_sec - start_sec, 3)

        text = ""
        while index < total_lines and lines[index].strip() != "":
            text += lines[index].strip() + " "
            index += 1

        subtitles.append({
            'start': start_sec,
            'dur': duration,
            'text': text.strip()
        })
        
        index += 1

    return subtitles

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file_en = request.files['file_en']
        file_vi = request.files['file_vi']
        
        # Save files temporarily
        file_en_path = os.path.join('uploads', file_en.filename)
        file_vi_path = os.path.join('uploads', file_vi.filename)
        file_en.save(file_en_path)
        file_vi.save(file_vi_path)

        # Parse SRT files
        english_subs = parse_srt(file_en_path)
        vietnamese_subs = parse_srt(file_vi_path)

        combined_subs = []
        for en_sub, vi_sub in zip(english_subs, vietnamese_subs):
            combined_subs.append({
                'start': en_sub['start'],
                'dur': en_sub['dur'],
                'text': en_sub['text'],
                'vietnamese': vi_sub['text']
            })

        # Create output JSON filename based on the English SRT filename
        json_file_name = os.path.splitext(file_en.filename)[0] + '.json'
        json_file_path = os.path.join('downloads', json_file_name)

        # Write to JSON
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(combined_subs, f, ensure_ascii=False, indent=4)

        return send_file(json_file_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
