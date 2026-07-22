param([Parameter(Mandatory=$true)][string]$Caminho)
# Copia uma imagem para o clipboard (STA) para colar no Gemini com ctrl+v
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile($Caminho)
[System.Windows.Forms.Clipboard]::SetImage($img)
Write-Output "Clipboard OK: $Caminho"
