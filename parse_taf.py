# # # # # parse_taf.py
# # # # def taf_to_text(taf_raw, aeropuerto):
# # # #     """
# # # #     Convierte un TAF crudo en un mensaje simplificado y entendible.
# # # #     """

# # # #     mensaje = f"⚠️ Alerta meteorológica en {aeropuerto}\n\n"

# # # #     # Buscar viento
# # # #     import re
# # # #     viento = re.search(r"(\d{3})(\d{2})KT", taf_raw)
# # # #     if viento:
# # # #         direccion = int(viento.group(1))
# # # #         velocidad = int(viento.group(2))
# # # #         mensaje += f"🌬️ Viento: {direccion}° a {velocidad} kt\n"

# # # #     # Buscar visibilidad
# # # #     vis = re.search(r" (\d{4}) ", taf_raw)
# # # #     if vis:
# # # #         km = int(vis.group(1)) / 1000
# # # #         mensaje += f"👀 Visibilidad: {km:.1f} km\n"

# # # #     # Fenómenos comunes
# # # #     fenomenos = {
# # # #         "RA": "🌧️ Lluvia",
# # # #         "TS": "⛈️ Tormenta",
# # # #         "SN": "❄️ Nieve",
# # # #         "FG": "🌫️ Niebla",
# # # #         "DZ": "🌦️ Llovizna",
# # # #     }
# # # #     for code, desc in fenomenos.items():
# # # #         if code in taf_raw:
# # # #             mensaje += f"{desc}\n"

# # # #     # Nubes
# # # #     nubes = re.findall(r"(BKN|OVC)(\d{3})", taf_raw)
# # # #     for tipo, altura in nubes:
# # # #         feet = int(altura) * 100
# # # #         simbolo = "☁️"
# # # #         if feet <= 2000:
# # # #             simbolo = "⚠️☁️"
# # # #         mensaje += f"{simbolo} Nubes {tipo} a {feet} ft\n"

# # # #     # Intervalos TEMPO/PROB
# # # #     if "TEMPO" in taf_raw:
# # # #         mensaje += "⏱️ Cambios temporales esperados\n"
# # # #     if "PROB" in taf_raw:
# # # #         mensaje += "❓ Probabilidad de fenómenos adicionales\n"

# # # #     mensaje += "\n👉 Posibles impactos en operaciones."
# # # #     return mensaje

# # # # parse_taf.py
# # # import re

# # # def taf_to_text(taf_raw, aeropuerto):
# # #     """
# # #     Convierte un TAF crudo en un mensaje simplificado y entendible,
# # #     con emojis según intensidad de los fenómenos.
# # #     """
# # #     mensaje = f"⚠️ Alerta meteorológica en {aeropuerto}\n\n"

# # #     # --- Viento ---
# # #     viento = re.search(r"(\d{3})(\d{2})KT", taf_raw)
# # #     if viento:
# # #         direccion = int(viento.group(1))
# # #         velocidad = int(viento.group(2))
# # #         if velocidad < 15:
# # #             emoji_viento = "🌬️"
# # #         elif velocidad < 25:
# # #             emoji_viento = "💨"
# # #         else:
# # #             emoji_viento = "💨⚠️"
# # #         mensaje += f"{emoji_viento} Viento: {direccion}° a {velocidad} kt\n"

# # #     # --- Fenómenos ---
# # #     fenomenos = {
# # #         "RA": ("🌦️","🌧️","⛈️"),
# # #         "TS": ("🌩️","⛈️","⚡⛈️"),
# # #         "SN": ("🌨️","❄️","☃️❄️"),
# # #         "FG": ("🌫️","⚠️🌫️","🚨🌫️"),
# # #     }
# # #     for code, em in fenomenos.items():
# # #         if code in taf_raw:
# # #             # Intensidad media si hay TEMPO o PROB, alta si no
# # #             if "TEMPO" in taf_raw or "PROB" in taf_raw:
# # #                 emoji = em[1]
# # #             else:
# # #                 emoji = em[2]
# # #             mensaje += f"{emoji} {code}\n"

# # #     # --- Nubes ---
# # #     nubes = re.findall(r"(BKN|OVC)(\d{3})", taf_raw)
# # #     for tipo, altura in nubes:
# # #         feet = int(altura) * 100
# # #         emoji_nubes = "⚠️☁️" if feet <= 2000 else "☁️"
# # #         mensaje += f"{emoji_nubes} Nubes {tipo} a {feet} ft\n"

# # #     # Cambios temporales y probabilidades
# # #     if "TEMPO" in taf_raw:
# # #         mensaje += "⏱️ Cambios temporales esperados\n"
# # #     if "PROB" in taf_raw:
# # #         mensaje += "❓ Probabilidad de fenómenos adicionales\n"

# # #     mensaje += "\n👉 Posibles impactos en operaciones."
# # #     return mensaje

# # # parse_taf.py
# # import re

# # # Diccionario ICAO → IATA
# # ICAO_TO_IATA = {
# #     "SAEZ": "EZE",
# #     "SABE": "AEP",
# #     "SACO": "COR",
# #     "SAME": "MDZ",
# # }

# # fenomenos = {
# #     "RA": "🌧️ Lluvia",
# #     "TS": "⛈️ Tormenta",
# #     "SN": "❄️ Nieve",
# #     "FG": "🌫️ Niebla",
# #     "DZ": "🌦️ Llovizna",
# # }

# # def format_zulu(day, hour):
# #     return f"Día {day} {hour}:00Z"

# # def analizar_taf(taf_raw, aeropuerto):
# #     """
# #     Procesa un TAF y devuelve un mensaje consolidado (1 por aeropuerto, solo si hay mal clima).
# #     """
# #     iata = ICAO_TO_IATA.get(aeropuerto, aeropuerto)
# #     mensaje = f"⚠️ Alerta meteorológica en {iata}\n\n"

# #     # Validez general
# #     validez = re.search(r"(\d{2})(\d{2})/(\d{2})(\d{2})", taf_raw)
# #     if validez:
# #         dia_ini, hora_ini, dia_fin, hora_fin = validez.groups()
# #         mensaje += f"📅 Válido: {format_zulu(dia_ini,hora_ini)} → {format_zulu(dia_fin,hora_fin)}\n\n"

# #     # Extraer bloques (TEMPO, BECMG, PROB)
# #     bloques = re.findall(
# #         r"(TEMPO|BECMG|PROB\d{2}) (\d{2})(\d{2})/(\d{2})(\d{2})(.*?)(?= TEMPO| BECMG| PROB|\Z)",
# #         taf_raw
# #     )

# #     # Agregar bloque principal al inicio
# #     bloques.insert(0, ("MAIN", validez.group(1), validez.group(2), validez.group(3), validez.group(4), taf_raw))

# #     alertas = []

# #     for tipo, d1, h1, d2, h2, condiciones in bloques:
# #         bloque_texto = f"🕒 {format_zulu(d1,h1)} → {format_zulu(d2,h2)}\n"

# #         # Viento
# #         viento = re.search(r"(\d{3})(\d{2})KT", condiciones)
# #         if viento:
# #             bloque_texto += f"🌬️ Viento: {int(viento.group(1))}° a {int(viento.group(2))} kt\n"

# #         # Visibilidad
# #         vis = re.search(r" (\d{4}) ", condiciones)
# #         vis_alerta = False
# #         if vis:
# #             metros = int(vis.group(1))
# #             km = metros / 1000
# #             bloque_texto += f"👀 Visibilidad: {km:.1f} km\n"
# #             if metros < 5000:
# #                 vis_alerta = True

# #         # Fenómenos detectados
# #         fenomenos_detectados = []
# #         for code, desc in fenomenos.items():
# #             if code in condiciones:
# #                 fenomenos_detectados.append(desc)
# #         for f in fenomenos_detectados:
# #             bloque_texto += f"{f}\n"

# #         # Nubes
# #         nubes_detectadas = []
# #         nubes = re.findall(r"(BKN|OVC)(\d{3})", condiciones)
# #         for tipo_n, altura in nubes:
# #             feet = int(altura) * 100
# #             if feet <= 2000:
# #                 nubes_detectadas.append(f"⚠️☁️ Nubes {tipo_n} a {feet} ft")
# #         for n in nubes_detectadas:
# #             bloque_texto += f"{n}\n"

# #         # Guardar solo si hay algo relevante
# #         if fenomenos_detectados or nubes_detectadas or vis_alerta:
# #             alertas.append(bloque_texto.strip())

# #     if alertas:
# #         mensaje += "\n\n".join(alertas)
# #         mensaje += "\n\n👉 Impacto esperado en operaciones."
# #         return mensaje
# #     else:
# #         return None

# # parse_taf.py
# import re

# # Diccionario ICAO → IATA
# ICAO_TO_IATA = {
#     "SAEZ": "EZE",
#     "SABE": "AEP",
#     "SACO": "COR",
#     "SAME": "MDZ",
# }

# # Fenómenos severos
# fenomenos_severos = {
#     "TS": "⛈️ Tormenta",
#     "SN": "❄️ Nieve",
#     "FG": "🌫️ Niebla",
# }

# def format_zulu(day, hour):
#     return f"Día {day} {hour}:00Z"

# def analizar_taf(taf_raw, aeropuerto):
#     """
#     Procesa un TAF y devuelve un mensaje consolidado (1 por aeropuerto, solo si hay condiciones severas).
#     """
#     iata = ICAO_TO_IATA.get(aeropuerto, aeropuerto)
#     mensaje = f"⚠️ Alerta meteorológica en {iata}\n\n"

#     # Validez general
#     validez = re.search(r"(\d{2})(\d{2})/(\d{2})(\d{2})", taf_raw)
#     if validez:
#         dia_ini, hora_ini, dia_fin, hora_fin = validez.groups()
#         mensaje += f"📅 Válido: {format_zulu(dia_ini,hora_ini)} → {format_zulu(dia_fin,hora_fin)}\n\n"

#     # Extraer bloques (TEMPO, BECMG, PROB)
#     bloques = re.findall(
#         r"(TEMPO|BECMG|PROB\d{2}) (\d{2})(\d{2})/(\d{2})(\d{2})(.*?)(?= TEMPO| BECMG| PROB|\Z)",
#         taf_raw
#     )

#     # Agreg

import re

def format_zulu(day, hour):
    return f"Día {day} {hour}:00Z"

fenomenos_severos = {
    "TS": "⛈️ Tormenta",
    "SN": "❄️ Nieve",
    "FG": "🌫️ Niebla",
}

def analizar_taf(taf_raw, aeropuerto_cfg):
    """
    Procesa un TAF y devuelve un mensaje consolidado (1 por aeropuerto, solo si hay condiciones severas).
    Usa los umbrales definidos en config.yaml.
    """
    iata = aeropuerto_cfg["iata"]
    umbrales = aeropuerto_cfg["umbrales"]

    mensaje = f"⚠️ Alerta meteorológica en {iata}\n\n"

    # Validez general
    validez = re.search(r"(\d{2})(\d{2})/(\d{2})(\d{2})", taf_raw)
    if validez:
        dia_ini, hora_ini, dia_fin, hora_fin = validez.groups()
        mensaje += f"📅 Válido: {format_zulu(dia_ini,hora_ini)} → {format_zulu(dia_fin,hora_fin)}\n\n"

    # Bloques
    bloques = re.findall(
        r"(TEMPO|BECMG|PROB\d{2}) (\d{2})(\d{2})/(\d{2})(\d{2})(.*?)(?= TEMPO| BECMG| PROB|\Z)",
        taf_raw
    )

    if validez:
        bloques.insert(0, ("MAIN", validez.group(1), validez.group(2), validez.group(3), validez.group(4), taf_raw))

    alertas = []

    for tipo, d1, h1, d2, h2, condiciones in bloques:
        bloque_texto = f"🕒 {format_zulu(d1,h1)} → {format_zulu(d2,h2)}\n"
        severo = False

        # Viento
        viento = re.search(r"(\d{3})(\d{2})KT", condiciones)
        if viento:
            dir_viento = int(viento.group(1))
            vel_viento = int(viento.group(2))
            if vel_viento >= umbrales["viento"]:
                bloque_texto += f"🌬️ Viento fuerte: {dir_viento}° a {vel_viento} kt\n"
                severo = True

        # Visibilidad
        vis = re.search(r" (\d{4}) ", condiciones)
        if vis:
            metros = int(vis.group(1))
            if metros < umbrales["visibilidad"]:
                km = metros / 1000
                bloque_texto += f"👀 Visibilidad reducida: {km:.1f} km\n"
                severo = True

        # Fenómenos severos
        for code, desc in fenomenos_severos.items():
            if code in condiciones:
                bloque_texto += f"{desc}\n"
                severo = True

        # Nubes bajas
        nubes = re.findall(r"(BKN|OVC)(\d{3})", condiciones)
        for tipo_n, altura in nubes:
            feet = int(altura) * 100
            if feet <= umbrales["techo_nubes"]:
                bloque_texto += f"⚠️☁️ Nubes {tipo_n} a {feet} ft\n"
                severo = True

        if severo:
            alertas.append(bloque_texto.strip())

    if alertas:
        mensaje += "\n\n".join(alertas)
        mensaje += "\n\n👉 Posible impacto en operaciones."
        return mensaje
    else:
        return None
