from dataclasses import dataclass, asdict, field
from enum import Enum
from urllib.error import HTTPError

from .utils import json_get, json_post


class EInkColorMode(Enum):
    ONE_BIT = '1bit'
    THREE_BIT = '3bit'


class EInkGatewayClient:
    @dataclass
    class PanelConfig:
        ssid: str = field(default=None)
        password: str = field(default=None)
        websocketUrl: str = field(default=None)

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def get_pannels(self) -> dict | HTTPError:
        url = f'{self.api_url}/api/panels'
        return json_get(url, query={'apiKey': self.api_key})

    def get_panel(self, panel_id: str) -> dict | HTTPError:
        url = f'{self.api_url}/api/panels/{panel_id}'
        return json_get(url, query={'apiKey': self.api_key})

    def display_image(self, panel_id: str, image_url: str, mode: EInkColorMode) -> dict | HTTPError:
        url = f'{self.api_url}/api/panels/{panel_id}/commands/display'
        return json_post(url, data={'image': image_url, 'mode': mode.value}, query={'apiKey': self.api_key})

    def reboot(self, panel_id: str):
        url = f'{self.api_url}/api/panels/{panel_id}/commands/reboot'
        return json_post(url, query={'apiKey': self.api_key})

    def ota(self, panel_id: str, ota_url: str):
        url = f'{self.api_url}/api/panels/{panel_id}/commands/ota'
        return json_post(url, data={'url': ota_url}, query={'apiKey': self.api_key})

    def update_config(self, panel_id: str, config: PanelConfig):
        url = f'{self.api_url}/api/panels/{panel_id}/commands/config'
        return json_post(url, data=asdict(config, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}), query={'apiKey': self.api_key})
