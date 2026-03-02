# watermark_config.py
# -----------------------------------------------------------
# Metadata that gets embedded into the QR code watermark.
#
# FUTURE: Replace WATERMARK_METADATA below with a call to
# your web API, e.g.:
#
#   import requests
#   response = requests.get("https://your-site.com/api/metadata")
#   WATERMARK_METADATA = response.json()
#
# For now, edit the values here directly.
# -----------------------------------------------------------

WATERMARK_METADATA = {
    "producer": "Zeynep Sueda Bozkurt",
    "date":     "19.02.2026",
    "ai_model": "Stable Diffusion",
}
