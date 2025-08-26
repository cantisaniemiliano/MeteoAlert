# # # # # # alerta_wx.py - versión TAF solo WhatsApp en macOS
# # # # # import requests
# # # # # import os
# # # # # import yaml
# # # # # from parse_taf import taf_to_text
# # # # # from twilio.rest import Client

# # # # # # --- Cargar configuración ---
# # # # # with open("config.yaml", "r", encoding="utf-8") as f:
# # # # #     config = yaml.safe_load(f)

# # # # # AEROPUERTOS = config["aeropuertos"]
# # # # # WHATSAPP = config["whatsapp"]

# # # # # # --- Función para obtener TAF ---
# # # # # def obtener_taf(icao):
# # # # #     url = f"https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/{icao}.TXT"
# # # # #     r = requests.get(url)
# # # # #     if r.status_code == 200:
# # # # #         return r.text.strip()
# # # # #     return None

# # # # # # --- Función para analizar condiciones críticas en TAF ---
# # # # # def es_alerta(taf_texto):
# # # # #     alertas = []
# # # # #     if "TS" in taf_texto:
# # # # #         alertas.append("⛈️ Tormenta prevista")
# # # # #     if "RA" in taf_texto:
# # # # #         alertas.append("🌧️ Lluvia prevista")
# # # # #     if "SN" in taf_texto:
# # # # #         alertas.append("❄️ Nieve prevista")
# # # # #     if "FG" in taf_texto:
# # # # #         alertas.append("🌫️ Niebla prevista")
# # # # #     if "WS" in taf_texto:
# # # # #         alertas.append("💨 Viento fuerte previsto")
# # # # #     return alertas

# # # # # # --- Función para enviar WhatsApp ---
# # # # # def enviar_whatsapp(mensaje):
# # # # #     sid = os.getenv("TWILIO_SID")
# # # # #     token = os.getenv("TWILIO_TOKEN")
# # # # #     from_num = os.getenv("TWILIO_WHATSAPP_FROM")

# # # # #     client = Client(sid, token)
# # # # #     for destino in WHATSAPP:
# # # # #         client.messages.create(
# # # # #             body=mensaje,
# # # # #             from_=from_num,
# # # # #             to=f"whatsapp:{destino}"
# # # # #         )

# # # # # # --- Ejecución ---
# # # # # if __name__ == "__main__":
# # # # #     for aeropuerto in AEROPUERTOS:
# # # # #         taf = obtener_taf(aeropuerto)
# # # # #         if taf:
# # # # #             alertas = es_alerta(taf)
# # # # #             if alertas:
# # # # #                 mensaje = f"⚠️ Alerta en {aeropuerto} (TAF)\n\nTAF completo:\n{taf}\n\nCondiciones críticas: {', '.join(alertas)}"
# # # # #                 enviar_whatsapp(mensaje)
# # # # #                 print(f"[ENVIADO] {aeropuerto}: {mensaje}")
# # # # #             else:
# # # # #                 print(f"[OK] {aeropuerto}: sin alertas críticas.")

# # # # # alerta_wx.py - versión TAF solo WhatsApp en macOS con mensajes simplificados
# # # # import requests
# # # # import os
# # # # import yaml
# # # # from parse_taf import taf_to_text
# # # # from twilio.rest import Client

# # # # # --- Cargar configuración ---
# # # # with open("config.yaml", "r", encoding="utf-8") as f:
# # # #     config = yaml.safe_load(f)

# # # # AEROPUERTOS = config["aeropuertos"]
# # # # WHATSAPP = config["whatsapp"]

# # # # # --- Función para obtener TAF ---
# # # # def obtener_taf(icao):
# # # #     url = f"https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/{icao}.TXT"
# # # #     try:
# # # #         r = requests.get(url, timeout=10)
# # # #         if r.status_code == 200:
# # # #             return r.text.strip()
# # # #     except Exception as e:
# # # #         print(f"⚠️ Error al obtener TAF de {icao}: {e}")
# # # #     return None

# # # # # --- Función para enviar WhatsApp ---
# # # # def enviar_whatsapp(mensaje):
# # # #     sid = os.getenv("TWILIO_SID")
# # # #     token = os.getenv("TWILIO_TOKEN")
# # # #     from_num = os.getenv("TWILIO_WHATSAPP_FROM")

# # # #     client = Client(sid, token)
# # # #     for destino in WHATSAPP:
# # # #         try:
# # # #             client.messages.create(
# # # #                 body=mensaje,
# # # #                 from_=from_num,
# # # #                 to=f"whatsapp:{destino}"
# # # #             )
# # # #         except Exception as e:
# # # #             print(f"⚠️ Error al enviar WhatsApp a {destino}: {e}")

# # # # # --- Ejecución ---
# # # # if __name__ == "__main__":
# # # #     for aeropuerto in AEROPUERTOS:
# # # #         taf = obtener_taf(aeropuerto)
# # # #         if taf:
# # # #             # Generar mensaje resumido y entendible
# # # #             mensaje = taf_to_text(taf, aeropuerto)

# # # #             # Enviar WhatsApp
# # # #             enviar_whatsapp(mensaje)
# # # #             print(f"[ENVIADO] {aeropuerto}")
# # # #         else:
# # # #             print(f"[OK] {aeropuerto}: sin TAF disponible")

# # # # alerta_wx.py - versión final con parseo de TAF y emojis según intensidad
# # # import requests
# # # import os
# # # import yaml
# # # from parse_taf import taf_to_text
# # # from twilio.rest import Client

# # # # --- Cargar configuración ---
# # # with open("config.yaml", "r", encoding="utf-8") as f:
# # #     config = yaml.safe_load(f)

# # # AEROPUERTOS = config["aeropuertos"]
# # # WHATSAPP = config["whatsapp"]

# # # # --- Función para obtener TAF ---
# # # def obtener_taf(icao):
# # #     url = f"https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/{icao}.TXT"
# # #     try:
# # #         r = requests.get(url, timeout=10)
# # #         if r.status_code == 200:
# # #             return r.text.strip()
# # #     except Exception as e:
# # #         print(f"⚠️ Error al obtener TAF de {icao}: {e}")
# # #     return None

# # # # --- Función para enviar WhatsApp ---
# # # def enviar_whatsapp(mensaje):
# # #     sid = os.getenv("TWILIO_SID")
# # #     token = os.getenv("TWILIO_TOKEN")
# # #     from_num = os.getenv("TWILIO_WHATSAPP_FROM")

# # #     client = Client(sid, token)
# # #     for destino in WHATSAPP:
# # #         try:
# # #             client.messages.create(
# # #                 body=mensaje,
# # #                 from_=from_num,
# # #                 to=f"whatsapp:{destino}"
# # #             )
# # #         except Exception as e:
# # #             print(f"⚠️ Error al enviar WhatsApp a {destino}: {e}")

# # # # --- Ejecución ---
# # # if __name__ == "__main__":
# # #     for aeropuerto in AEROPUERTOS:
# # #         taf = obtener_taf(aeropuerto)
# # #         if taf:
# # #             # Generar mensaje resumido y entendible con emojis
# # #             mensaje = taf_to_text(taf, aeropuerto)

# # #             # Enviar WhatsApp
# # #             enviar_whatsapp(mensaje)
# # #             print(f"[ENVIADO] {aeropuerto}")
# # #         else:
# # #             print(f"[OK] {aeropuerto}: sin TAF disponible")

# # import requests
# # from twilio.rest import Client
# # from parse_taf import analizar_taf

# # # Configuración Twilio
# # account_sid = "TU_SID_TWILIO"
# # auth_token = "TU_AUTH_TOKEN"
# # twilio_whatsapp = "whatsapp:+14155238886"  # Número de Twilio
# # destino_whatsapp = "whatsapp:+541166524353"  # Tu número

# # client = Client(account_sid, auth_token)

# # # Aeropuertos ICAO a monitorear
# # aeropuertos = ["SAEZ", "SABE", "SACO", "SAME"]

# # for aeropuerto in aeropuertos:
# #     url = f"https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/{aeropuerto}.TXT"
# #     r = requests.get(url)

# #     if r.status_code == 200:
# #         taf_raw = r.text
# #         mensaje = analizar_taf(taf_raw, aeropuerto)

# #         if mensaje:
# #             client.messages.create(
# #                 body=mensaje,
# #                 from_=twilio_whatsapp,
# #                 to=destino_whatsapp
# #             )
# #             print(f"✅ WhatsApp enviado para {aeropuerto}")
# #         else:
# #             print(f"👌 {aeropuerto}: sin fenómenos relevantes")
# #     else:
# #         print(f"❌ No se pudo obtener el TAF de {aeropuerto}")

# import requests
# from twilio.rest import Client
# from parse_taf import analizar_taf

# # Configuración Twilio
# account_sid = "TU_SID_TWILIO"
# auth_token = "TU_AUTH_TOKEN"
# twilio_whatsapp = "whatsapp:+14155238886"  # Número de Twilio

# # Lista de destinatarios
# destinatarios = [
#     "whatsapp:+541166524353",  # Emi
#     "whatsapp:+5491122223333", # Ejemplo jefe operaciones
#     "whatsapp:+5491133334444", # Ejemplo coordinador
# ]

# client = Client(account_sid, auth_token)

# # Aeropuertos ICAO a monitorear
# aeropuertos = ["SAEZ", "SABE", "SACO", "SAME"]

# for aeropuerto in aeropuertos:
#     url = f"https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/{aeropuerto}.TXT"
#     r = requests.get(url)

#     if r.status_code == 200:
#         taf_raw = r.text
#         mensaje = analizar_taf(taf_raw, aeropuerto)

#         if mensaje:
#             for destinatario in destinatarios:
#                 client.messages.create(
#                     body=mensaje,
#                     from_=twilio_whatsapp,
#                     to=destinatario
#                 )
#             print(f"✅ WhatsApp enviado para {aeropuerto}")
#         else:
#             print(f"👌 {aeropuerto}: condiciones normales")
#     else:
#         print(f"❌ No se pudo obtener el TAF de {aeropuerto}")

import requests
import yaml
from twilio.rest import Client
from parse_taf import analizar_taf

# Configuración desde config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

account_sid = config["twilio"]["account_sid"]
auth_token = config["twilio"]["auth_token"]
twilio_whatsapp = config["twilio"]["whatsapp_from"]

destinatarios = config["destinatarios"]
aeropuertos = config["aeropuertos"]

client = Client(account_sid, auth_token)

for aeropuerto_cfg in aeropuertos:
    codigo = aeropuerto_cfg["codigo"]
    url = f"https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/{codigo}.TXT"
    r = requests.get(url)

    if r.status_code == 200:
        taf_raw = r.text
        mensaje = analizar_taf(taf_raw, aeropuerto_cfg)

        if mensaje:
            for destinatario in destinatarios:
                client.messages.create(
                    body=mensaje,
                    from_=twilio_whatsapp,
                    to=destinatario
                )
            print(f"✅ WhatsApp enviado para {codigo}")
        else:
            print(f"👌 {codigo}: condiciones normales")
    else:
        print(f"❌ No se pudo obtener el TAF de {codigo}")
