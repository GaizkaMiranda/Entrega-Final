# api/notifications.py
import requests

def notify_if_anomaly(reading, settings):
    thresholds = settings.anomaly_thresholds
    alert = False
    messages = []

    if hasattr(reading, "ritmo") and reading.ritmo > thresholds.get("ritmo", float('inf')):
        alert = True
        messages.append(f"Ritmo alto: {reading.ritmo}")

    if hasattr(reading, "temperatura") and reading.temperatura > thresholds.get("temperatura", float('inf')):
        alert = True
        messages.append(f"Temperatura alta: {reading.temperatura}")

    if hasattr(reading, "oxigeno") and reading.oxigeno < thresholds.get("oxigeno", 0):
        alert = True
        messages.append(f"Nivel bajo de oxígeno: {reading.oxigeno}")

    if alert:
        payload = {
            "text": "Alerta de anomalía detectada:\n" + "\n".join(messages),
            "reading": reading.dict()
        }
        try:
            requests.post(settings.webhook_url, json=payload)
        except Exception as e:
            print(f"Error enviando notificación: {e}")
