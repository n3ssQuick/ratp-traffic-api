from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import requests
from enum import Enum

app = FastAPI(debug=True)

# Get Traffic according to URL


class TransportType(str, Enum):
  bus = "bus"
  metro = "metro"
  noctilien = "noctilien"
  rer = "rer"
  tram = "tram"
  transilien = "transilien"


@app.get("/traffic/{transport_type}/{transport_id}")
async def traffic(transport_type: TransportType, transport_id: str):
  base_url = "https://www.ma-ligne.co/"
  url = f"{base_url}{transport_type.value}-{transport_id}"

  try:
    response = requests.get(url)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    raise HTTPException(status_code=500, detail={"error": str(e)})

  soup = BeautifulSoup(response.content, 'html.parser')

  # OK
  alert_success = soup.find('div', {'class': 'alert alert-success mb-4 text-center'})
  if alert_success:
    return {"status": "OK", "message": alert_success.text.strip()}

  # Work
  card_warnings = soup.find_all('div', {'class': 'card-header bg-warning fw-bolder'})
  for card_warning in card_warnings:
    message = card_warning.find_next('div', {'class': 'card-body fs-5'}).text.strip()
    raise HTTPException(status_code=500, detail={"status": "Travaux", "message": message})

  # Disturbance
  card_dangers = soup.find_all('div', {'class': 'card-header bg-danger text-white fw-bolder'})
  for card_danger in card_dangers:
    message = card_danger.find_next('div', {'class': 'card-body fs-5'}).text.strip()
    raise HTTPException(status_code=500, detail={"status": "Perturbations", "message": message})

  return {"status": "Inconnu", "message": "Aucun statut trouvé"}


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=6000)
