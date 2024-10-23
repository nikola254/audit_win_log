import psycopg2
import re

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


def parse_audit_log(file_path):
    events = []
    # Парсим файл txt
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):  # Группируем строки по 4 для каждой записи
        event = {
            'timestamp': re.search(r'\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}', lines[i]).group(0),
            'event_id': int(re.search(r'\d+', lines[i+1]).group(0)),
            'severity': lines[i+2].strip(),
            'description': '\n'.join(lines[i+3:i+4])  # Объединяем две последние строки в одну
        }
        events.append(event)
    
    return events

def get_audit_log_data(events):
    sql_query = """
    INSERT INTO audit_new (timestamp, event_id, severity, description)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (timestamp, event_id, severity)
    DO NOTHING
    """
    
    for event in events:
        cursor.execute(sql_query, (
            event['timestamp'],
            event['event_id'],
            event['severity'],
            event['description']
        ))
    
    conn.commit()
    print(f"Total of {cursor.rowcount} events processed")
    return cursor.rowcount

def handle_form_submission(file_path=None):
    if file_path:
        events = parse_audit_log(file_path)
    else:
        print("Warning: File path is not provided.")
        return 0
    
    result = get_audit_log_data(events)
    return result

# Вызов функции
result = handle_form_submission('logs/Criticals.txt')
print(f"Total of {result} events inserted successfully")
