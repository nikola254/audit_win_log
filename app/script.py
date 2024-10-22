import psycopg2
import json
import os

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="RO",
    user="postgres",
    password="root"
)
cursor = conn.cursor()

def parse_audit_log(file_path):
    events = []
    # Парсим JSON файл
    with open(file_path, 'r') as f:
        data = json.load(f)
    for event in data:
        event_id = event['EventID']
        event_type = event['SourceName']
        event_time = event['TimeGenerated']
        username = event['StringInserts'][0]
        computer = event['StringInserts'][1]
        events.append({
            'event_id': event_id,
            'event_type': event_type,
            'event_time': event_time,
            'username': username,
            'computer': computer
        })

    return events

def get_audit_log_data(events):
    for event in events:
        cursor.execute('''
            INSERT INTO audit_new (event_id, event_type, event_time, username, computer)
            SELECT %s, %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM audit_new
                WHERE event_type = %s AND event_time = %s AND username = %s AND computer = %s
            )
        ''', (event['event_id'], event['event_type'], event['event_time'], 
             event['username'], event['computer'],
             event['event_type'], event['event_time'], event['username'], event['computer']))
    
    conn.commit()
def handle_form_submission(file_path=None):
    if file_path:
        events = parse_audit_log(file_path)
    else:
        # Здесь можно добавить логику для парсинга Windows Audit Log
        print("Warning: Parsing Windows Audit Log is not implemented yet.")
        events = []  # Временно возвращаем пустой список
    get_audit_log_data(events)
    return get_audit_log_data_from_db()

def get_audit_log_data_from_db():
    cursor.execute('SELECT * FROM audit_new')
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
