# import win32evtlog
import psycopg2
# import pywintypes
import json

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="RO",
    user="postgres",
    password="root"
)
cursor = conn.cursor()

def parse_audit_log_from_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    events = []
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

# def parse_audit_log_from_windows_audit_log():
#     flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
#     events = []
#     handle = None
#     try:
#         handle = win32evtlog.OpenEventLog("Security", "localhost")
#         events = win32evtlog.ReadEventLog(handle, flags, 0)
#     except pywintypes.error as e:
#         print(f"Ошибка: {e}")
#     finally:
#         if handle is not None and handle != win32evtlog.INVALID_HANDLE_VALUE:
#             try:
#                 win32evtlog.CloseEventLog(handle)
#             except pywintypes.error as e:
#                 print(f"Ошибка при закрытии журнала событий: {e}")
#     return events

def get_audit_log_data(events):
    for event in events:
        cursor.execute('''
            INSERT INTO audit (event_type, event_time, username, computer)
            VALUES (%s, %s, %s, %s)
        ''', (event['event_type'], event['event_time'], event['username'], event['computer']))
    conn.commit()

def handle_form_submission(file_path=None):
    if file_path:
        events = parse_audit_log_from_file(file_path)
    # else:
    #     events = parse_audit_log_from_windows_audit_log()
    get_audit_log_data(events)
    return get_audit_log_data_from_db()

def get_audit_log_data_from_db():
    cursor.execute('SELECT * FROM audit')
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# # Example usage:
# handle_form_submission(file_path='path/to/data.json')  # Load data from file
# # or
# handle_form_submission()  # Load data from Windows Audit Log