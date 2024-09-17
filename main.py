import re
import json
from googletrans import Translator
import time

def srt_to_json(srt_file, json_file):
    translator = Translator()
    
    with open(srt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    subtitles = []
    index = 0
    total_lines = len(lines)
    
    print("loading...")  # Hiển thị thông báo "loading..."
    
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
            # Split time by ':', and '.'
            parts = re.split(r':|\.', t)
            # Ensure that we have exactly 3 parts (hh, mm, ss.ms)
            h = float(parts[0]) if len(parts) > 0 else 0
            m = float(parts[1]) if len(parts) > 1 else 0
            s = float(parts[2]) if len(parts) > 2 else 0
            ms = float(parts[3]) if len(parts) > 3 else 0
            # Return total seconds (including milliseconds)
            return round(h * 3600 + m * 60 + s + ms / 1000, 3)

        start_sec = time_to_seconds(start_time)
        end_sec = time_to_seconds(end_time)
        duration = round(end_sec - start_sec, 3)

        # Parse subtitle text
        text = ""
        while index < total_lines and lines[index].strip() != "":
            text += lines[index].strip() + " "
            index += 1
        
        # Translate text to Vietnamese
        translated_text = translator.translate(text.strip(), src='en', dest='vi').text

        # Add subtitle object to list
        subtitles.append({
            'start': start_sec,
            'dur': duration,
            'text': text.strip(),
            'vietnamese': translated_text
        })
        
        # Skip empty line after subtitle
        index += 1

    # Write subtitles to JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(subtitles, f, ensure_ascii=False, indent=4)

    print("Completed!")  # Thông báo hoàn tất

# Example usage
srt_to_json('./BabyChickJump.srt', './BabyChickJump.json')
