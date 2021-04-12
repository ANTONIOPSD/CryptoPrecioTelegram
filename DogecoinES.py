### SCRIPT DE AVISO DE CAMBIO DE PRECIO DE CRIPTOMONEDAS USANDO LAS APIS DE BINANCE TELEGRAM ###
### BY ANTONIOPSD ###
### ESTO ES SOLO UN EJEMPLO SUCIO, SE PUEDE OPTIMIZAR LA MAYORÍA DEL CÓDIGO ###
### NECESITA LOS SIGUIENTES MÓDULOS ###

import os
import datetime
import time
import requests

###################################################################################################
# Variables globales
token_bot = 'TOKEN DEL BOT DE TELEGRAM'
chat_id = 'ID DEL CHAT DE TELECGRAM'
intervalo_tiempo = 10 #Tiempo de refresco en segundos
umbral_subida = 0.001
umbral_subida_str = str(umbral_subida) + '€'
par_moneda = 'DOGEEUR'
url = f"https://api.binance.com/api/v3/ticker/price?symbol={par_moneda}"
headers = {'Accept': 'application/json'}

def obtener_precio():
    # Request a la api
    respuesta = requests.get(url, headers=headers)
    respuesta_json = respuesta.json()
    # Extraer precio de respuesta
    precio = float(respuesta_json['price'])
    return precio

# Función para mandar mensaje a Telegram
def enviar_mensage(chat_id, mensaje):
    url = f"https://api.telegram.org/bot{token_bot}/sendMessage?chat_id={chat_id}&text={mensaje}"
    # Enviar request
    requests.get(url)

###################################################################################################

# Función main
def main():
    try:
        requests.head(url)
        print('Conectando...')
        precio_anterior = round(obtener_precio(), 5)
        precio_anterior_str = str(precio_anterior) + "€"
        print('Iniciando: ' + precio_anterior_str)
        print('Precio inicial: ' + precio_anterior_str)

        # Loop infinito
        while True:
            os.system('cls')
            #resto_tiempo = datetime.datetime.now().minute % 5 # Obtenemos el resto de dividir los minutos entre 5, en este caso es para comprobar los precios cada 5 minutos
            minutos = resto_tiempo = datetime.datetime.now().minute
            print(round(obtener_precio(), 5))
            print(resto_tiempo)

            #if	resto_tiempo == 0:
            if	minutos == 0 or minutos == 10 or minutos == 20 or minutos == 30 or minutos == 40 or minutos == 50: #Comprobamos diferencia de precio cada 10 minutos
                precio_actual = round(obtener_precio(), 5)
                precio_actual_str = str(precio_actual) + '€'
                precio_diferencia = round((precio_actual - precio_anterior), 5)
                precio_diferencia_str = format(precio_diferencia, '5f') + "€"
                porcentaje_cambio = round(((precio_actual - precio_anterior) / precio_anterior * 100), 2)
                porcentaje_cambio_str = str(porcentaje_cambio) + '%'

                print('Precio actual ' + precio_actual_str)

                # Si la diferencia de precio es mayor o igual a la especificada, mostrar mensaje en consola y enviar mensaje a Telegram.
                if  precio_diferencia >= umbral_subida:

                    print('----------------------------')
                    print("Precio anterior: " + precio_anterior_str)
                    print("Precio actual: " + precio_actual_str)
                    print("Aumento de precio: " + precio_diferencia_str)

                    enviar_mensage(chat_id=chat_id, mensaje=f'ATENCIÓN, SUBIDA DE PRECIO')
                    time.sleep(2)
                    enviar_mensage(chat_id=chat_id, mensaje=f'El precio del Dogecoin ha subido {precio_diferencia_str} ({porcentaje_cambio_str}) en los últimos 15 minutos. \nEl precio anterior era: {precio_anterior_str} \nEl precio actual es: {precio_actual_str}\nhttps://www.binance.com/es/trade/{par_moneda}')

                precio_anterior = precio_actual
                precio_anterior_str = str(precio_anterior) + "€"

            # Refrescamos precio cada x segundos.
            time.sleep(intervalo_tiempo)

    except: ## Si no se puede conectar, reintentar cada 2 segundos.
        print("Error al conectar, reintentando...")
        time.sleep(2)
        main()


# Activar función main
if __name__ == '__main__':
    main()
