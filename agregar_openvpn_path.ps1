# Script para agregar OpenVPN al PATH en Windows
# Ejecutar como Administrador

Write-Host "🔍 Buscando OpenVPN..." -ForegroundColor Cyan

# Rutas comunes donde se instala OpenVPN
$rutasPosibles = @(
    "C:\Program Files\OpenVPN\bin",
    "C:\Program Files (x86)\OpenVPN\bin",
    "C:\OpenVPN\bin"
)

$openvpnPath = $null

# Buscar OpenVPN en las rutas comunes
foreach ($ruta in $rutasPosibles) {
    if (Test-Path "$ruta\openvpn.exe") {
        $openvpnPath = $ruta
        Write-Host "✓ OpenVPN encontrado en: $ruta" -ForegroundColor Green
        break
    }
}

# Si no se encontró, buscar en todo el sistema
if (-not $openvpnPath) {
    Write-Host "⚠ No encontrado en rutas comunes, buscando en el sistema..." -ForegroundColor Yellow
    $resultado = Get-ChildItem -Path "C:\" -Filter "openvpn.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($resultado) {
        $openvpnPath = $resultado.DirectoryName
        Write-Host "✓ OpenVPN encontrado en: $openvpnPath" -ForegroundColor Green
    }
}

if (-not $openvpnPath) {
    Write-Host "❌ OpenVPN no encontrado en el sistema" -ForegroundColor Red
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor Yellow
    Write-Host "1. Instala OpenVPN desde: https://openvpn.net/community-downloads/" -ForegroundColor White
    Write-Host "2. Durante la instalación, marca 'Add OpenVPN to system PATH'" -ForegroundColor White
    Write-Host "3. O proporciona manualmente la ruta donde está instalado" -ForegroundColor White
    exit 1
}

# Verificar si ya está en el PATH
$pathActual = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)
if ($pathActual -like "*$openvpnPath*") {
    Write-Host "✓ OpenVPN ya está en el PATH del sistema" -ForegroundColor Green
    Write-Host ""
    Write-Host "Verificando que funciona..." -ForegroundColor Cyan
    $env:Path = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine) + ";" + [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
    $version = & openvpn --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓✓ OpenVPN funciona correctamente!" -ForegroundColor Green
        Write-Host $version -ForegroundColor White
    } else {
        Write-Host "⚠ OpenVPN está en PATH pero no responde. Reinicia la terminal." -ForegroundColor Yellow
    }
    exit 0
}

# Agregar al PATH del sistema
Write-Host ""
Write-Host "📝 Agregando OpenVPN al PATH del sistema..." -ForegroundColor Cyan

try {
    $nuevoPath = $pathActual + ";$openvpnPath"
    [Environment]::SetEnvironmentVariable("Path", $nuevoPath, [EnvironmentVariableTarget]::Machine)
    Write-Host "✓✓ OpenVPN agregado exitosamente al PATH del sistema" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠ IMPORTANTE:" -ForegroundColor Yellow
    Write-Host "   Debes CERRAR y REABRIR todas las ventanas de PowerShell/CMD" -ForegroundColor White
    Write-Host "   para que los cambios surtan efecto." -ForegroundColor White
    Write-Host ""
    Write-Host "   Después, verifica con: openvpn --version" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Error al agregar al PATH: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Solución: Ejecuta este script como Administrador" -ForegroundColor Yellow
    Write-Host "   Clic derecho en PowerShell > Ejecutar como administrador" -ForegroundColor White
    exit 1
}

