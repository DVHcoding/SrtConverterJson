import re
import json
from googletrans import Translator

def srt_to_json(srt_file_en, srt_file_vi, json_file):
    translator = Translator()
    
    def parse_srt(srt_file):
        with open(srt_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        subtitles = []
        index = 0
        total_lines = len(lines)
        
        while index < total_lines:
            # Skip empty lines
            if lines[index].strip() == "":
                index += 1
                continue

            # Parse index
            index += 1
            
            # Parse time codes
            time_line = lines[index].strip()
            start_time, end_time = re.split(r' --> ', time_line)
            start_time = start_time.replace(',', '.')
            end_time = end_time.replace(',', '.')
            index += 1

            # Convert to seconds including milliseconds
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

            # Parse subtitle text
            text = ""
            while index < total_lines and lines[index].strip() != "":
                text += lines[index].strip() + " "
                index += 1

            subtitles.append({
                'start': start_sec,
                'dur': duration,
                'text': text.strip()
            })
            
            # Skip empty line after subtitle
            index += 1

        return subtitles

    # Parse both SRT files
    english_subs = parse_srt(srt_file_en)
    vietnamese_subs = parse_srt(srt_file_vi)

    # Combine the two lists
    combined_subs = []
    for en_sub, vi_sub in zip(english_subs, vietnamese_subs):
        combined_subs.append({
            'start': en_sub['start'],
            'dur': en_sub['dur'],
            'text': en_sub['text'],
            'vietnamese': vi_sub['text']
        })

    # Write subtitles to JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(combined_subs, f, ensure_ascii=False, indent=4)

    print("Completed!")  # Thông báo hoàn tất

# Example usage
srt_to_json('./srt/cam19_test1_part1.srt', './translateSrt/cam19_test1_part1.vi.srt', './json/cam19_test1_part1.json')
