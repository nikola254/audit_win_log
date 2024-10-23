# audit_win_log 

echo "# audit_win_log" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M master
git remote add origin https://github.com/nikola254/audit_win_log.git
git push -u origin master


команды для PowerShell 

Логи уровня ошибки (Error)

Get-WinEvent -FilterHashtable @{
    Level=2 # Уровень события
    LogName='Application' # Имя журнала
} -MaxEvents 200 | 
Select-Object TimeCreated, Id, LevelDisplayName, Message |
Format-List TimeCreated, Id, LevelDisplayName, Message |
Out-File -FilePath 'C:\Logs\Errors.txt'


Логи уровня предупреждения (Warning)

Get-WinEvent -FilterHashtable @{
    Level=3 # Уровень события
    LogName='System' # Имя журнала
} -MaxEvents 300 | 
Select-Object TimeCreated, Id, LevelDisplayName, Message |
Format-List TimeCreated, Id, LevelDisplayName, Message |
Out-File -FilePath 'C:\Logs\Warnings.txt'


Логи уровня информации (Information)

# Попробуйте выполнить команду в другой час
Get-WinEvent -FilterHashtable @{
    Level=0 # Уровень события
    LogName='Application' # Имя журнала
} -MaxEvents 500 |
Select-Object TimeCreated, Id, LevelDisplayName, Message |
Format-List TimeCreated, Id, LevelDisplayName, Message |
Out-File -FilePath 'C:\Logs\Information.txt'


Логи уровня критического уровня (Critical)

GeGet-WinEvent -FilterHashtable @{
    Level=1 # Уровень события
    LogName='System' # Имя журнала
} -MaxEvents 50 | 
Select-Object TimeCreated, Id, LevelDisplayName, Message |
Format-List TimeCreated, Id, LevelDisplayName, Message |
Out-File -FilePath 'C:\Logs\Criticals.txt'

