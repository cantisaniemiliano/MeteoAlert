import time
import requests
import yaml
from twilio.rest import Client
from parse_taf import analizar_taf
import os

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Twilio: usa variables de entorno si existen, si no usa config.yaml
account_sid = os.getenv("TWILIO_ACCOUNT_SID", config["twilio"]["account_sid"])
auth_token = os.getenv("TWILIO_AUTH_TOKEN", config["twilio"]["auth_token"])
twilio_whatsapp = os.getenv("TWILIO_WHATSAPP_FROM", config["twilio"]["whatsapp_from"])

# Destinatarios y aeropuertos
destinatarios = config["destinatarios"]
aeropuertos = config["aeropuertos"]

client = Client(account_sid, auth_token)

# -----------------------------
# BUCLE INFINITO CADA 6 HORAS
# -----------------------------
while True:
    print("⏱️ Iniciando revisión de TAF...")

    for aeropuerto_cfg in aeropuertos:
        codigo = aeropuerto_cfg["codigo"]
        iata = aeropuerto_cfg.get("iata", codigo)
        url = f"https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/{codigo}.TXT"

        try:
            r = requests.get(url, timeout=10)
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
                    print(f"✅ WhatsApp enviado para {iata}")
                else:
                    print(f"👌 {iata}: condiciones normales")

            else:
                print(f"❌ No se pudo obtener el TAF de {iata} (status {r.status_code})")

        except Exception as e:
            print(f"❌ Error al obtener TAF de {iata}: {e}")

    print("⏳ Esperando 6 horas para la siguiente ejecución...\n")
    time.sleep(6 * 60 * 60)
