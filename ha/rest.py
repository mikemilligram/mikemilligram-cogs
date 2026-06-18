import requests
from typing import Any, Dict
import time
import re

class HomeAssistantAPI:
  def __init__(self, url: str, token: str):
    """
    Initialize Home Assistant API client.
    """
    self.endpoint = url.rstrip('/') + "/api"
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
      response = requests.get(f"{self.endpoint}/", headers=self.headers)
      return response.status_code == 200
    except requests.RequestException:
      return False

  def call_service(self, domain: str, entity: str, service: str) -> Dict[str, Any]:
    """
    Call a service within a specific domain.
    """
    
    endpoint = f"{self.endpoint}/services/{domain}/{service}"
    data = {"entity_id": f"{domain}.{entity}"}
    response = requests.post(endpoint, json=data, headers=self.headers)
    response.raise_for_status()
    return response.json()

  def announce(self, message: str, device_id: list[str]) -> Dict[str, Any]:
    """
    Announce a message using a media player entity.
    """
    
    endpoint = f"{self.endpoint}/services/assist_satellite/announce"
    data = {
      "message": message,
      "device_id": device_id
    }
    response = requests.post(endpoint, json=data, headers=self.headers)
    response.raise_for_status()
    return response.json()