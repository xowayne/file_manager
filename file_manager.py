import os
import shutil
import json
import time


DOWNLOADS_FOLDER = 'C:/Users/wayne/Downloads'  # change as needed
DESTINATION_FOLDERS = {
    'Pictures': ['.gif', '.png', '.jpg', '.webp'],
    'Videos': ['.mp4'],
    'Music': ['.mp3'],
    'Forms': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
}
UNKNOWN_TRACKER_FILE = 'unknown_files.json'
REPORT_FILE = 'organizer_report.txt'
DELETION_DELAY_DAYS = 3


def scan_and_organize():
    report_data = {
    'total_files': 0,
    'moved': {category: 0 for category in DESTINATION_FOLDERS},
    'duplicates': [],
    'unknown': []
    }

    seen_files = set()

    for foldername, subfolders, filenames in os.walk(DOWNLOADS_FOLDER):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            report_data['total_files'] += 1

            ext = os.path.splitext(filename)[1].lower()
            file_size = os.path.getsize(file_path)
            file_id = (filename.lower(), file_size)

            if is_duplicate(file_path, seen_files):
                report_data['duplicates'].append(file_path)
                continue

            seen_files.add(file_id)

            moved = False
            for category, extensions in DESTINATION_FOLDERS.items():
                if ext in extensions:
                    move_file(file_path, category)
                    report_data['moved'][category] += 1
                    moved = True
                    break

            if not moved:
                handle_unknown_file(file_path)
                report_data['unknown'].append(file_path)

    generate_report(report_data)

def move_file(file_path, category):
    destination_dir = os.path.join(DOWNLOADS_FOLDER, category)
    os.makedirs(destination_dir, exist_ok=True)

    filename = os.path.basename(file_path)
    destination_path = os.path.join(destination_dir, filename)

    shutil.move(file_path, destination_path)

def handle_unknown_file(file_path):
    try:
        with open(UNKNOWN_TRACKER_FILE, 'r') as f:
            unknown_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        unknown_data = {}

    if file_path not in unknown_data:
        unknown_data[file_path] = time.time()

    with open(UNKNOWN_TRACKER_FILE, 'w') as f:
        json.dump(unknown_data, f, indent=4)

def clean_old_unknowns():
    try:
        with open(UNKNOWN_TRACKER_FILE, 'r') as f:
            unknown_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        unknown_data = {}

    now = time.time()
    cutoff = DELETION_DELAY_DAYS * 86400  # 86400 seconds in a day
    updated_data = {}

    for file_path, timestamp in unknown_data.items():
        if now - timestamp >= cutoff:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted unknown file: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        else:
            updated_data[file_path] = timestamp

    with open(UNKNOWN_TRACKER_FILE, 'w') as f:
        json.dump(updated_data, f, indent=4)

def is_duplicate(file_path, seen_files):
    filename = os.path.basename(file_path).lower()
    file_size = os.path.getsize(file_path)
    file_id = (filename, file_size)

    return file_id in seen_files

def generate_report(report_data):
    lines = []
    lines.append(f"Total files scanned: {report_data['total_files']}")
    
    lines.append("\nFiles moved:")
    for category, count in report_data['moved'].items():
        lines.append(f"  {category}: {count}")

    lines.append(f"\nDuplicates found: {len(report_data['duplicates'])}")
    for dup in report_data['duplicates']:
        lines.append(f"  {dup}")

    lines.append(f"\nUnknown files tracked: {len(report_data['unknown'])}")
    for unk in report_data['unknown']:
        lines.append(f"  {unk}")

    with open(REPORT_FILE, 'w') as f:
        f.write("\n".join(lines))

    print(f"\nReport saved to {REPORT_FILE}")

if __name__ == "__main__":
    scan_and_organize()
    clean_old_unknowns()