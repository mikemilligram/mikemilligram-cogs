import requests
from typing import Any, Dict, List, Literal
import time
from .morse import Timings
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


  def call_service(self, domain: str, service: str, data: Dict = {}):
    """
    Call a service within a specific domain.
    """
    endpoint = f"{self.endpoint}/services/{domain}/{service}"
    response = requests.post(endpoint, json=data, headers=self.headers)
    response.raise_for_status()
    return response.json()
  
  
  def light_on(self, entities: List[str]) -> Dict[str, Any]:
    """
    Turn on a light entity.
    """
    data = {"entity_id": [f"light.{entity}" for entity in entities]}
    return self.call_service("light", "turn_on", data)
  
  
  def light_off(self, entities: List[str]) -> Dict[str, Any]:
    """
    Turn off a light entity.
    """
    data = {"entity_id": [f"light.{entity}" for entity in entities]}
    return self.call_service("light", "turn_off", data) 


  def announce(self, message: str, device_id: List[str]) -> Dict[str, Any]:
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
  

  async def morse_element(self, signal: str = Literal['dot', 'dash'], *entities: str):
    """
    Send a Morse code signal to the specified entities.
    """
    self.light_on(entities)
    if signal == 'dot':
      time.sleep(Timings.DOT_LENGTH)
    elif signal == 'dash':
      time.sleep(Timings.DASH_LENGTH)
    self.light_off(entities)


  async def light_morse(self, message: str, *entities: str) -> bool:
    """Send a message in Morse code using the specified light entities."""
    
    if not self.validate_morse(message):
      return False
    if '   ' in message or '/' in message:
      words = re.split(r'   |/', message.strip())
    else:
      words = [message]
    sleep = 0
    for word in words:
        if sleep > 0:
            time.sleep(sleep)
        sleep = 0
        for char in word.strip():
            if sleep > 0:
                time.sleep(sleep)
            if char == '.':
                await self.morse_element('dot', *entities)
                sleep = Timings.INTRA_LETTER_GAP
            elif char == '-':
                await self.morse_element('dash', *entities)
                sleep = Timings.INTRA_LETTER_GAP
            elif char == ' ':
                sleep = Timings.INTER_LETTER_GAP
        sleep = Timings.INTER_WORD_GAP - Timings.INTRA_LETTER_GAP
    return True
                
                
  def validate_morse(self, message: str) -> bool:
    pattern = re.compile(r'^([.-]{1,5}( |   |/| / |$))+$')
    return bool(pattern.match(message))