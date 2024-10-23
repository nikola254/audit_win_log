import psycopg2
import re
import chardet
import os

# Establish a connection to the PostgreSQL database
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




def get_audit_log_data(events):
    sql_query = """
    INSERT INTO criticals (event_time, event_id, event_type, event_info)
    VALUES (%s, %s, %s, %s)
    """
    
    for event in events:
        cursor.execute(sql_query, (
            event['event_time'],
            event['event_id'],
            event['event_type'],
            event['event_info']
        ))
    
    conn.commit()
    print(f"Total of {cursor.rowcount} events processed")
    return cursor.rowcount

def handle_form_submission(file_path):
    events = parse_audit_log(file_path)
    get_audit_log_data(events)
    return get_audit_log_data_from_db()

def get_audit_log_data_from_db():
    cursor.execute('SELECT * FROM criticals')
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
# # Вызов функции
# result = parse_audit_log('Criticals.txt')
# print(result)

