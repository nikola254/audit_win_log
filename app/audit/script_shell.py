import subprocess
import os


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
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    Get-WinEvent -ListLog * |
    Where-Object { $_.RecordCount -gt 0 } |  
    ForEach-Object {
        "LogMode: $($_.LogMode)"
        "MaximumSizeInBytes: $($_.MaximumSizeInBytes)"
        "RecordCount: $($_.RecordCount)"
        "LogName: $($_.LogName)"
        ""
    }
    """

    try:
        # Запускаем PowerShell с правами администратора
        admin_command = f'powershell -Command "{command}"'

        result = subprocess.run(['powershell.exe', '-Command', admin_command],
                               check=True,
                               text=True,
                               capture_output=True)

        print("Команда успешно выполнена.")
        print("Вывод команды:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print(f"Стек трассировки: {e.__traceback__}")

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        
        
def execute_powershell_all_log_and_10first():
    command = r"""
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

    # Укажите путь к файлу для сохранения вывода
    $outputFilePath = 'C:\Users\Admin\Desktop\ro01\audit_win_log\app\audit\logs\Informations.txt'

    # Очищаем файл перед записью
    Clear-Content -Path $outputFilePath -ErrorAction SilentlyContinue

    Get-WinEvent -ListLog * |
    Where-Object { $_.RecordCount -gt 0 } |  
    ForEach-Object {
        try {
            # Записываем информацию о журнале
            $logInfo = @{
                LogMode = $_.LogMode
                MaximumSizeInBytes = $_.MaximumSizeInBytes
                RecordCount = $_.RecordCount
                LogName = $_.LogName
            }

            # Получаем первые 10 событий из каждого журнала
            $events = Get-WinEvent -LogName $_.LogName -MaxEvents 3 -ErrorAction Stop
            foreach ($event in $events) {
                $eventInfo = @{
                    TimeCreated = $event.TimeCreated
                    LevelDisplayName = $event.LevelDisplayName
                    Message = $event.Message
                }

                # Форматируем вывод для записи в файл
                $outputLine = "LogMode: $($logInfo.LogMode)`n" +
                            "MaximumSizeInBytes: $($logInfo.MaximumSizeInBytes)`n" +
                            "RecordCount: $($logInfo.RecordCount)`n" +
                            "LogName: $($logInfo.LogName)`n" +
                            "TimeCreated: $($eventInfo.TimeCreated)`n" +
                            "LevelDisplayName: $($eventInfo.LevelDisplayName)`n" +
                            "Message: $($eventInfo.Message)`n" +
                            "-----------------------------`n"

                # Записываем в файл
                $outputLine | Out-File -FilePath $outputFilePath -Append
            }
        } catch {
            # Обработка ошибок, если не удалось получить доступ к журналу
            "Ошибка доступа к журналу: $($_.LogName) - $($_.Exception.Message)" | Out-File -FilePath $outputFilePath -Append
            ""
        }
    }
    """

    try:
        # Запускаем PowerShell с правами администратора
        admin_command = f'powershell -Command "{command}"'

        result = subprocess.run(['powershell.exe', '-Command', admin_command],
                               check=True,
                               text=True,
                               capture_output=True)

        print("Команда успешно выполнена.")
        print("Вывод команды:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print(f"Стек трассировки: {e.__traceback__}")

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")