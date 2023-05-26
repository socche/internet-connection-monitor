# Internet Connection Monitor

Este script de Python monitorea la conexión a Internet y envía notificaciones a través de Telegram cuando la conexión se cae y se restablece.

## Requisitos

- Python 3.x
- Paquetes Python: requests

## Configuración

Antes de ejecutar el script, asegúrate de realizar la siguiente configuración:

1. Obtén un token de bot de Telegram siguiendo las instrucciones en https://core.telegram.org/bots#botfather.

2. Copia el token del bot de Telegram y reemplaza `telegram_token` en el script con tu propio token.

3. Obtén el ID del chat de Telegram al que deseas enviar las notificaciones. Puedes utilizar el bot de Telegram, como @userinfobot, para obtener el ID del chat.

4. Reemplaza `telegram_chat_id` en el script con tu propio ID de chat.

## Uso

Ejecuta el script `monitor_internet_connection.py` con Python:

```bash
python monitor_internet_connection.py
```
El script comenzará a monitorear la conexión a Internet y enviará notificaciones a través de Telegram cuando la conexión se caiga y se restablezca.
Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún problema o tienes una idea de mejora, no dudes en abrir un problema o enviar una solicitud de extracción.
Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.
