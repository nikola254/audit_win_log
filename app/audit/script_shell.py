import subprocess

def execute_powershell_criticals():
    command = r"""
    Get-WinEvent -FilterHashtable @{
        Level=1 # Уровень события
        LogName='System' # Имя журнала
    } -MaxEvents 50 | 
    Select-Object TimeCreated, Id, LevelDisplayName, Message |
    Format-List TimeCreated, Id, LevelDisplayName, Message |
    Out-File -FilePath 'C:\Users\Admin\Desktop\ro01\audit_win_log\app\audit\logs\Criticals.txt'
    """
    try:
        result = subprocess.run(['powershell', '-Command', command], 
                               check=True, 
                               text=True, 
                               capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print(f"Стек трассировки: {e.__traceback__}")
        
def execute_powershell_error():
    command = r"""
    Get-WinEvent -FilterHashtable @{
        Level=2 # Уровень события
        LogName='Application' # Имя журнала
    } -MaxEvents 200 | 
    Select-Object TimeCreated, Id, LevelDisplayName, Message |
    Format-List TimeCreated, Id, LevelDisplayName, Message |
    Out-File -FilePath 'C:\Users\Admin\Desktop\ro01\audit_win_log\app\audit\logs\Erors.txt'
    """
    try:
        result = subprocess.run(['powershell', '-Command', command], 
                               check=True, 
                               text=True, 
                               capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print(f"Стек трассировки: {e.__traceback__}")
        
def execute_powershell_warning():
    command = r"""
    Get-WinEvent -FilterHashtable @{
        Level=3 # Уровень события
        LogName='System' # Имя журнала
    } -MaxEvents 300 | 
    Select-Object TimeCreated, Id, LevelDisplayName, Message |
    Format-List TimeCreated, Id, LevelDisplayName, Message |
    Out-File -FilePath 'C:\Users\Admin\Desktop\ro01\audit_win_log\app\audit\logs\Warnings.txt'
    """
    try:
        result = subprocess.run(['powershell', '-Command', command], 
                               check=True, 
                               text=True, 
                               capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print(f"Стек трассировки: {e.__traceback__}")
        
def execute_powershell_info():
    command = r"""
    Get-WinEvent -FilterHashtable @{
        Level=0 # Уровень события
        LogName='Application' # Имя журнала
    } -MaxEvents 500 |
    Select-Object TimeCreated, Id, LevelDisplayName, Message |
    Format-List TimeCreated, Id, LevelDisplayName, Message |
    Out-File -FilePath 'C:\Users\Admin\Desktop\ro01\audit_win_log\app\audit\logs\Informations.txt'
    """
    try:
        result = subprocess.run(['powershell', '-Command', command], 
                               check=True, 
                               text=True, 
                               capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print(f"Стек трассировки: {e.__traceback__}")
        
def execute_powershell_all_log():
    command = r"""
     Get-WinEvent -ListLog * |
     ForEach-Object {
         "LogMode: $($_.LogMode)"
         "MaximumSizeInBytes: $($_.MaximumSizeInBytes)"
         "RecordCount: $($_.RecordCount)"
         "LogName: $($_.LogName)"
         ""
     } | Out-File -FilePath 'C:\Users\Admin\Desktop\ro01\audit_win_log\app\audit\logs\All_log_files.txt'
    """
    try:
        result = subprocess.run(['powershell', '-Command', command], 
                               check=True, 
                               text=True, 
                               capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print(f"Стек трассировки: {e.__traceback__}")        
