$searchFolder = "$env:APPDATA\MinecraftPC_Netease_PB\packcache\"
$searchPattern = "HudAddonScript.mcp"
$recurse = $true

$files = Get-ChildItem -Path $searchFolder -Filter $searchPattern -Recurse:$recurse -File
if ($files.Count -eq 0) {
    Write-Host "没有找到匹配的文件，脚本结束。" -ForegroundColor Red
    exit
}

$latestFile = $files | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Write-Host "最新的文件是: $($latestFile.FullName)" -ForegroundColor Green
Start-Process explorer.exe -ArgumentList "/select, `"$($latestFile.FullName)`""

# 注入地址
$sourceFile1 = "$PSScriptRoot\Script_PlatformPatcher.mcp"
$sourceFile2 = "$PSScriptRoot\xdpatch.mcp"
$directory = $latestFile.DirectoryName

Copy-Item -Path $sourceFile1 -Destination $directory -Force
Copy-Item -Path $sourceFile2 -Destination $directory -Force

Write-Host "已将外部文件复制到：$directory" -ForegroundColor Cyan
Write-Host "成功执行" -ForegroundColor Cyan