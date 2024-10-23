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
    Level=1 # Уровень события
    LogName='System' # Имя журнала
} -MaxEvents 50 | 
Select-Object TimeCreated, Id, LevelDisplayName, Message |
Format-List TimeCreated, Id, LevelDisplayName, Message |
Out-File -FilePath 'C:\Logs\Criticals.txt'


Логи уровня предупреждения (Warning)

Get-WinEvent -LogName 'System' -FilterHashtable @{ Level=3 } -MaxEvents 50 | Select-Object TimeCreated, Id, LevelDisplayName, Message | Out-File -FilePath 'C:\Logs\Warnings.txt'

Логи уровня информации (Information)

Get-WinEvent -LogName 'System' -FilterHashtable @{ Level=4 } -MaxEvents 50 | Select-Object TimeCreated, Id, LevelDisplayName, Message | Out-File -FilePath 'C:\Logs\Info.txt'

Логи уровня критического уровня (Critical)

Get-WinEvent -LogName 'System' -FilterHashtable @{ Level=1 } -MaxEvents 50 | Select-Object TimeCreated, Id, LevelDisplayName, Message | Out-File -FilePath 'C:\Logs\Criticals.txt'

