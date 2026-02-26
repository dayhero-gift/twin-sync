# 小天文件管理工具集
param(
    [string]$Command = "help",
    [string]$Path = "."
)

$BaseDir = "C:\Users\ThinkPad\.openclaw\workspace"

switch ($Command) {
    "scan" {
        Write-Host "Scanning: $Path"
        Get-ChildItem -Path $Path -Recurse -File -ErrorAction SilentlyContinue | 
            Select-Object FullName, Length, LastWriteTime, Extension |
            Export-Csv "$BaseDir\knowledge\file-index.csv" -NoTypeInformation
        Write-Host "Index saved to knowledge\file-index.csv"
    }
    "find" {
        Get-ChildItem -Path $BaseDir -Recurse -Filter $Path -ErrorAction SilentlyContinue |
            Select-Object FullName, Length, LastWriteTime
    }
    "help" {
        Write-Host @"
Usage: .\file-manager.ps1 [command] [path]

Commands:
  scan [path]  - Scan directory and create index
  find [pattern] - Find files matching pattern
  help         - Show this help
"@
    }
}
