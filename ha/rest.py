import requests
from typing import Any, Dict

class HomeAssistantAPI:
  def __init__(self, url: str, token: str):
    """
    Initialize Home Assistant API client.
    """
    self.endpoint = url.rstrip('/') + "/api/"
    self.token = token
    self.headers = {
      'Authorization': f'Bearer {token}',
      'Content-Type': 'application/json'
    }
    
  def authenticate(self) -> bool:
    """
    Test authentication by fetching the current user's information.
    """
    try:
      response = requests.get(self.endpoint, headers=self.headers)
      return response.status_code == 200
    except requests.RequestException:
      return False

  def change_state(self, entity_id: str, state: str) -> Dict[str, Any]:
    """
    Change the state of an entity.
    """
    endpoint = f"{self.endpoint}states/{entity_id}"
    data = {"entity_id": entity_id, "state": state}
    response = requests.post(endpoint, json=data, headers=self.headers)
    response.raise_for_status()
    return response.json()

