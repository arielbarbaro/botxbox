# Bot de Registro de Microsoft con Correos Temporales

Bot simple que abre la página de registro de Microsoft y genera correos temporales automáticamente.

## Características

- ✅ Abre automáticamente la página de registro de Microsoft
- ✅ Genera correos temporales automáticamente usando mail.tm API
- ✅ Muestra el correo temporal en la consola

## Requisitos

- **Python 3.11** (requerido)
- Google Chrome instalado
- Conexión a Internet

## Instalación

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecuta el bot:
```bash
python bot_registro_microsoft.py
```

El bot:
1. Creará un correo temporal automáticamente
2. Abrirá Google Chrome con la página de registro de Microsoft
3. Mostrará el correo temporal en la consola
4. Mantendrá el navegador abierto

## API de Correos Temporales

El bot utiliza la API gratuita de **mail.tm** que:
- No requiere registro ni API key
- Es completamente gratuita
- Permite recibir correos en tiempo real

## Notas

- El navegador permanecerá abierto hasta que presiones Ctrl+C
- Asegúrate de tener Chrome instalado en tu sistema
- Si tienes problemas, verifica tu conexión a Internet

