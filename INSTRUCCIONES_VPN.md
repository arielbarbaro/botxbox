# 🔐 Instrucciones para Configurar Credenciales VPN

## Problema
Los perfiles `.ovpn` de ProtonVPN requieren credenciales (usuario y contraseña) para conectarse. Sin estas credenciales, la VPN no se conectará correctamente.

## Solución Automática (Recomendada)

### Paso 1: Ejecutar el script de configuración
```bash
python configurar_credenciales_vpn.py
```

### Paso 2: Ingresar tus credenciales
El script te pedirá:
- **Usuario**: Tu nombre de usuario de ProtonVPN
- **Contraseña**: Tu contraseña de ProtonVPN

### Paso 3: ¡Listo!
El script automáticamente:
- ✅ Creará un archivo `credenciales.txt` en la carpeta `vpn_profiles`
- ✅ Modificará todos los archivos `.ovpn` para usar las credenciales
- ✅ El bot podrá conectarse a la VPN automáticamente

## Solución Manual

Si prefieres hacerlo manualmente:

### Opción 1: Archivo de credenciales (Recomendado)

1. Crea un archivo llamado `credenciales.txt` en la carpeta `vpn_profiles`
2. Agrega tu usuario en la primera línea
3. Agrega tu contraseña en la segunda línea

Ejemplo (`vpn_profiles/credenciales.txt`):
```
tu_usuario_protonvpn
tu_contraseña_protonvpn
```

4. Modifica cada archivo `.ovpn` y cambia:
   ```
   auth-user-pass
   ```
   por:
   ```
   auth-user-pass credenciales.txt
   ```

### Opción 2: Credenciales directamente en el .ovpn

1. Abre cada archivo `.ovpn` con un editor de texto
2. Busca la línea `auth-user-pass`
3. Reemplázala por:
   ```
   auth-user-pass
   tu_usuario_protonvpn
   tu_contraseña_protonvpn
   ```

⚠️ **Nota**: Esta opción es menos segura porque las credenciales quedan en texto plano en cada archivo.

## Verificación

Después de configurar las credenciales, ejecuta el bot:
```bash
python bot_registro_microsoft.py
```

Deberías ver:
- ✅ "VPN conectada exitosamente!"
- ✅ La IP cambió (de tu IP real a la IP del servidor VPN)
- ✅ El país cambió

Si ves:
- ⚠ "ADVERTENCIA: La IP no cambió"
- ⚠ "El perfil .ovpn requiere credenciales"

Significa que las credenciales no están configuradas correctamente. Vuelve a ejecutar el script de configuración.

## Seguridad

- El archivo `credenciales.txt` contiene información sensible
- No lo compartas ni lo subas a repositorios públicos
- Considera agregar `credenciales.txt` a tu `.gitignore` si usas control de versiones

## Solución de Problemas

### "No se encontró archivo de credenciales"
- Ejecuta `python configurar_credenciales_vpn.py`
- Verifica que el archivo `credenciales.txt` esté en `vpn_profiles/`

### "La IP no cambió"
- Verifica que las credenciales sean correctas
- Prueba conectarte manualmente con OpenVPN para verificar
- Algunos perfiles pueden requerir permisos de administrador

### "OpenVPN no encontrado"
- Instala OpenVPN desde https://openvpn.net/
- Agrega OpenVPN al PATH del sistema
- Reinicia la terminal después de agregar al PATH

