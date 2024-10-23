import subprocess

def execute_powershell(command):
    try:
        result = subprocess.run(['powershell', '-Command', command], 
                               check=True, 
                               text=True, 
                               capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print(f"Стек трассировки: {e.__traceback__}")




# Пример использования
# power_shell_command = "Get-Process | Select-Object Name, ID"
# result = execute_powershell(power_shell_command)
# print(result)