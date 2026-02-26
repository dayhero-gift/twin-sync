# 批量安装OpenClaw技能
$skills = @(
    "coding-agent"
    "discord"
    "slack"
    "notion"
    "obsidian"
    "himalaya"
    "mcporter"
    "clawhub"
    "healthcheck"
    "skill-creator"
    "tavily"
    "summarize"
    "find-skills"
    "ontology"
    "self-improving-agent"
)

Write-Host "开始批量安装技能..." -ForegroundColor Green
$success = @()
$failed = @()

foreach ($skill in $skills) {
    Write-Host "Installing: $skill" -NoNewline
    try {
        $output = npx clawhub install $skill --force 2>&1
        if ($output -match "OK|installed") {
            Write-Host " [OK]" -ForegroundColor Green
            $success += $skill
        } else {
            Write-Host " [FAILED]" -ForegroundColor Red
            $failed += $skill
        }
    } catch {
        Write-Host " [ERROR]" -ForegroundColor Red
        $failed += $skill
    }
    Start-Sleep -Seconds 3
}

Write-Host "`n安装完成!" -ForegroundColor Green
Write-Host "成功: $($success.Count) 个"
Write-Host "失败: $($failed.Count) 个"
if ($failed.Count -gt 0) {
    Write-Host "失败列表: $($failed -join ', ')" -ForegroundColor Yellow
}
