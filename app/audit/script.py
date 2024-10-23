import psycopg2
import re
import chardet
from app.audit.script_shell import execute_powershell_criticals

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="RO",
        user="postgres",
        password="root"
    )
except UnicodeDecodeError:
    print("UnicodeDecodeError occurred. Trying to connect with different encoding...")
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="RO",
        user="postgres",
        password="root",
        options="-c client_encoding=UTF8"
    )

cursor = conn.cursor()


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']

import re

def parse_audit_log(file_path):
    events = []
    detected_encoding = detect_encoding(file_path)
    
    try:
        with open(file_path, 'r', encoding=detected_encoding) as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file with detected encoding: {e}")
        print("Falling back to utf-8 encoding...")
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    for i in range(0, len(lines), 4):  # Группируем строки по 4 для каждой записи
        event = {}
        timestamp_match = re.search(r'\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}', lines[i].strip())
        if timestamp_match:
            event['event_time'] = timestamp_match.group(0)
        else:
            print(f"Warning: No timestamp found in line {i+1}. Skipping this event.")
            continue
        
        event_id_match = re.search(r'\d+', lines[i+1].strip())
        if event_id_match:
            event['event_id'] = int(event_id_match.group(0))
        else:
            print(f"Warning: No event ID found in line {i+2}. Skipping this event.")
            continue
        
        severity_match = re.search(r'[А-Яа-я]+', lines[i+2].strip())  # Поиск русских букв для уровня серьезности
        if severity_match:
            event['event_type'] = severity_match.group(0)
        else:
            print(f"Warning: No severity level found in line {i+3}. Skipping this event.")
            continue
        
        description_start = lines[i+3].find(':')
        if description_start != -1:
            event['event_info'] = lines[i+3][description_start + 1:].strip()
        else:
            print(f"Warning: Unexpected format in line {i+4}. Skipping this event.")
            continue
        
        required_fields = ['event_time', 'event_id', 'event_type', 'event_info']
        for field in required_fields:
            if field not in event:
                print(f"Warning: Missing field '{field}' in event. Skipping this event.")
                break
        else:
            events.append(event)
    
    return events




def get_audit_log_data(events, table):
    for event in events:
        cursor.execute(f'''
            INSERT INTO {table} (event_time, event_id, event_type, event_info)
            SELECT %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM {table}
                WHERE event_time = %s AND event_id = %s AND event_type = %s AND event_info = %s
            )
        ''', (event['event_time'], event['event_id'], event['event_type'], event['event_info'],
              event['event_time'], event['event_id'], event['event_type'], event['event_info']))
    conn.commit()


def handle_form_submission(file_path, table):
    execute_powershell_criticals()
    events = parse_audit_log(file_path)
    get_audit_log_data(events, table)
    return get_audit_log_data_from_db(table)

def get_audit_log_data_from_db(table):
    cursor.execute(f"SELECT * FROM {table}")
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_clear_all_log_file(file_path):
        # Инициализируем список для хранения валидных строк
    valid_lines = []
    current_block = []  # Список для хранения текущего блока

    # Открываем файл для чтения
    with open(file_path, 'r') as file:
        # Читаем все строки из файла
        lines = file.readlines()
        
        # Обрабатываем каждую строку
        for line in lines:
            # Проверяем, является ли строка началом нового блока
            if 'LogMode:' in line:
                # Если текущий блок не пуст, проверяем его на валидность
                if current_block:
                    # Проверяем, есть ли в блоке RecordCount равный 0 или пуст
                    if not any('RecordCount: 0' in l or 'RecordCount:' not in l for l in current_block):
                        valid_lines.extend(current_block)  # Сохраняем валидный блок
                # Сбрасываем текущий блок и добавляем новую строку
                current_block = [line]
            else:
                # Добавляем строку в текущий блок
                current_block.append(line)

        # Проверяем последний блок после завершения цикла
        if current_block:
            if not any('RecordCount: 0' in l or 'RecordCount:' not in l for l in current_block):
                valid_lines.extend(current_block)

    # Записываем валидные строки обратно в файл
    with open(file_path, 'w') as file:
        file.writelines(valid_lines)

# Пример использования
get_clear_all_log_file('C:\\Users\\Admin\\Desktop\\ro01\\audit_win_log\\app\\audit\\logs\\All_log_files.txt')
    