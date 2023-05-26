import subprocess
import requests
import time
import signal
import sys
import atexit
import logging
import os
from datetime import datetime

# Token del bot de Telegram
telegram_token = "YOUR_TELEGRAM_TOKEN"

# ID de chat de Telegram
telegram_chat_id = "YOUR_TELEGRAM_CHAT_ID"

# Configuración de registro
logging.basicConfig(filename='/home/ubuntu/registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_notification(message, file_path=None):
    # Registrar el mensaje en el archivo de registro
    logging.info("Notificación enviada a Telegram: %s", message)

    # URL de la API de Telegram para enviar mensajes o archivos
    url = f"https://api.telegram.org/bot{telegram_token}/"

    if file_path:
        # Enviar el archivo
        files = {"document": open(file_path, "rb")}
        data = {
            "chat_id": telegram_chat_id,
            "caption": message
        }
        endpoint = "sendDocument"
    else:
        # Enviar el mensaje de texto
        data = {
            "chat_id": telegram_chat_id,
            "text": message
        }
        endpoint = "sendMessage"

    # Enviar la solicitud POST a la API de Telegram
    response = requests.post(url + endpoint, data=data, files=files if file_path else None)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        print("Notificación enviada a Telegram.")
    else:
        print("Error al enviar la notificación a Telegram.")

def send_daily_log():
    # Obtener la fecha actual
    current_date = datetime.now().date()

    # Crear el nombre del archivo de registro diario
    log_file = f"registro_{current_date}.log"

    # Renombrar el archivo de registro existente
    os.rename("/home/ubuntu/registro.log", f"/home/ubuntu/{log_file}")

    # Enviar el archivo de registro diario
    send_notification("Registro diario", file_path=f"/home/ubuntu/{log_file}")

    # Eliminar el archivo de registro diario del servidor
    os.remove(f"/home/ubuntu/{log_file}")

def check_internet_connection():
    # Registrar mensaje de inicio en el archivo de registro
    logging.info("El script se ha iniciado correctamente.")
    
    # Enviar notificación al bot de Telegram
    send_notification("El script se ha iniciado correctamente.")

    internet_recovery_time = 0

    def signal_handler(signal, frame):
        send_notification("El script ha sido detenido manualmente o matado el proceso.")
        sys.exit(0)

    # Capturar la señal SIGINT (Ctrl+C) para finalizar el script
    signal.signal(signal.SIGINT, signal_handler)

    # Definir función para manejar la salida del script
    def exit_handler():
        send_notification("El script ha sido detenido.")

    # Registrar la función de salida del script utilizando atexit
    atexit.register(exit_handler)

    while True:
        try:
            # Ejecutar el comando ping y obtener la salida
            output = subprocess.check_output(["ping", "-c", "1", "8.8.8.8"])

            # Verificar si el ping fue exitoso
            if "1 packets transmitted, 1 received" in output.decode("utf-8"):
                if internet_recovery_time > 0:
                    recovery_duration = int(time.time() - internet_recovery_time)
                    recovery_time_message = f"La conexión se ha restablecido. Tiempo de recuperación: {recovery_duration} segundos."
                    send_notification(recovery_time_message)
                    print(recovery_time_message)
                    internet_recovery_time = 0
                print("Conexión a Internet establecida.")
            else:
                if internet_recovery_time == 0:
                    internet_recovery_time = time.time()
                print("¡La conexión a Internet se ha caído!")
                send_notification("¡Alerta! La conexión a Internet se ha caído. Verifica tu conexión a Internet.")

        except subprocess.CalledProcessError:
            if internet_recovery_time == 0:
                internet_recovery_time = time.time()
            print("¡La conexión a Internet se ha caído!")
            send_notification("¡Alerta! La conexión a Internet se ha caído. Verifica tu conexión a Internet.")

        # Verificar si es la hora de enviar el registro diario
        current_time = datetime.now().time()
        if current_time.hour == 0 and current_time.minute == 0:
            send_daily_log()

        # Esperar 90 segundos antes de realizar la próxima verificación
        time.sleep(90)

# Llamar a la función para verificar la conexión a Internet
check_internet_connection()
