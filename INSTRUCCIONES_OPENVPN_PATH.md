# Cómo agregar OpenVPN al PATH en Windows

## Método 1: Desde la interfaz gráfica (Recomendado)

1. **Encuentra la ubicación de OpenVPN:**
   - Por defecto, OpenVPN se instala en: `C:\Program Files\OpenVPN\bin`
   - O en: `C:\Program Files (x86)\OpenVPN\bin`

2. **Abre las Variables de Entorno:**
   - Presiona `Windows + R`
   - Escribe: `sysdm.cpl` y presiona Enter
   - Ve a la pestaña "Opciones avanzadas"
   - Haz clic en "Variables de entorno..."

3. **Agrega al PATH:**
   - En "Variables del sistema", busca la variable `Path`
   - Selecciónala y haz clic en "Editar..."
   - Haz clic en "Nuevo"
   - Agrega la ruta: `C:\Program Files\OpenVPN\bin`
   - (O la ruta donde esté instalado OpenVPN)
   - Haz clic en "Aceptar" en todas las ventanas

4. **Reinicia la terminal/PowerShell:**
   - Cierra todas las ventanas de PowerShell/CMD
   - Abre una nueva terminal
   - Verifica con: `openvpn --version`

## Método 2: Desde PowerShell (Rápido)

Abre PowerShell como **Administrador** y ejecuta:

```powershell
# Verificar si OpenVPN está instalado
$openvpnPath = "C:\Program Files\OpenVPN\bin"
if (Test-Path $openvpnPath) {
    # Agregar al PATH del sistema
    [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$openvpnPath", [EnvironmentVariableTarget]::Machine)
    Write-Host "✓ OpenVPN agregado al PATH del sistema"
    Write-Host "Reinicia la terminal para aplicar los cambios"
} else {
    Write-Host "⚠ OpenVPN no encontrado en: $openvpnPath"
    Write-Host "Busca la carpeta 'bin' de OpenVPN y usa esa ruta"
}
```

## Método 3: Verificar instalación de OpenVPN

Si OpenVPN no está instalado:

1. **Descarga OpenVPN:**
   - Ve a: https://openvpn.net/community-downloads/
   - Descarga la versión para Windows

2. **Instálalo:**
   - Ejecuta el instalador
   - Durante la instalación, asegúrate de marcar "Add OpenVPN to system PATH"
   - Si ya lo instalaste, reinstálalo y marca esa opción

## Verificar que funciona

Después de agregar al PATH, abre una **nueva** terminal y ejecuta:

```powershell
openvpn --version
```

Deberías ver algo como:
```
OpenVPN 2.x.x
```

Si ves esto, OpenVPN está correctamente en el PATH y el bot podrá usarlo.

## Ubicación alternativa

Si OpenVPN está en otra ubicación, busca el archivo `openvpn.exe` y usa esa carpeta en el PATH.

