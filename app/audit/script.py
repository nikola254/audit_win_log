import psycopg2
import re
import chardet
from app.audit.script_shell import execute_powershell_criticals, execute_powershell_all_log
from flask import current_app

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
# Эта функция парсит файл со всеми возможными лог файлами
def parse_all_log_file(file_path):
    logs = []
    with open(file_path, 'r', encoding='utf-16-le') as file:  # Используем 'utf-16-le'
        log_entry = {}
        for line in file:
            line = line.strip()
            print(f"Читаем строку: '{line}'")  # Отладочное сообщение
            if line:  # Проверяем, что строка не пустая
                # Проверяем, содержит ли строка двоеточие
                if ':' in line:
                    key, value = line.split(': ', 1)  # Разделяем строку на ключ и значение
                    log_entry[key] = value
                    print(f"Добавляем ключ: '{key}', значение: '{value}'")  # Отладочное сообщение
                else:
                    print(f"Пропускаем строку без двоеточия: '{line}'")  # Отладочное сообщение
            
            # Если достигли конца лог-записи (пустая строка), добавляем запись в список
            if line == '' and log_entry:
                logs.append({
                    'id': len(logs) + 1,  # id
                    'log_mode': log_entry.get('LogMode'),
                    'max_size': log_entry.get('MaximumSizeInBytes'),
                    'record_count': log_entry.get('RecordCount'),
                    'log_name': log_entry.get('LogName'),
                })
                print(f"Добавляем запись: {log_entry}")  # Отладочное сообщение
                log_entry = {}  # Сбрасываем для следующей записи

        # Добавляем последнюю запись, если файл не заканчивается пустой строкой
        if log_entry:
            logs.append({
                'id': len(logs) + 1,
                'log_mode': log_entry.get('LogMode'),
                'max_size': log_entry.get('MaximumSizeInBytes'),
                'record_count': log_entry.get('RecordCount'),
                'log_name': log_entry.get('LogName'),
            })
            print(f"Добавляем последнюю запись: {log_entry}")  # Отладочное сообщение

    print("Полученные логи:")
    for log in logs:
        print(f"ID: {log['id']}, LogMode: {log['log_mode']}, MaximumSizeInBytes: {log['max_size']}, RecordCount: {log['record_count']}, LogName: {log['log_name']}")
    
    return logs
# Эта функция добавляет новую инфу в базу по разным видам логов
def add_all_log_to_db(log_entries):
    for entry in log_entries:
        cursor.execute("""
            INSERT INTO all_log_file 
            (id, log_mode, max_size, record_count, log_name)
            SELECT %(id)s, %(log_mode)s, %(max_size)s, %(record_count)s, %(log_name)s
            WHERE NOT EXISTS (
                SELECT 1 FROM all_log_file WHERE id = %(id)s
            );
        """, entry)
    
    conn.commit()

    print(f"Выполнено вставок: {cursor.rowcount}")

    
def output_all_log_file(file_path, table):
    try:
        log_entries = parse_all_log_file(file_path)
        if not log_entries:
            print("Пустой список логов")
            return []
        
        add_all_log_to_db(log_entries)
        result = get_audit_log_data_from_db(table)
        conn.commit()
        return result
    
    except Exception as e:
        current_app.logger.error(f"Ошибка при обработке файла {file_path}: {str(e)}")
        conn.rollback()
        raise
