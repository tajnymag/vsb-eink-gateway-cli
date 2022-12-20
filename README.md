# VŠB E-Ink - Gateway API CLI

Trivial CLI wrapper around the VŠB E-Ink Gateway API. It is intended to be used as a simple way to send messages to the E-Ink displays before the final API is ready.

## Installation

The project is a standard Python package. It can be installed using `pip`

```bash
# Until the package is published on PyPI, you can install it directly from GitHub
pip install "git+ssh://git@github.com/tajnymag/vsb-eink-gateway-cli.git"
```

## Usage

All commands need an API key and APi url to work. You can either pass them as arguments or set them as environment variables.

* To set the API key, either set `EINK_GATEWAY_API_KEY` or pass argument `--api-key` to the command.
* To set the API url, either set `EINK_GATEWAY_API_URL` or pass argument `--api-url` to the command.

```bash
# Set up the API key and API url
export EINK_GATEWAY_API_KEY=your-api-key
export EINK_GATEWAY_API_URL=https://api.example.com

# Show up to date help
eink-gateway-cli --help

# Send an image to all displays
eink-gateway-cli display /path/to/image.png

# Send a remote image to a specific display
eink-gateway-cli display --panel-id "98:fc:84:e9:92:df" "https://i.imgur.com/KdCorvv.jpeg"

# Reboot a specific display
eink-gateway-cli reboot --panel-id "98:fc:84:e9:92:df"

# List connected panels
eink-gateway-cli get-panels

# Get the current status of a specific panel
eink-gateway-cli get-panel --panel-id "98:fc:84:e9:92:df"

# Update the firmware of a specific panel
eink-gateway-cli ota --panel-id "98:fc:84:e9:92:df" "https://github.com/..."

# Update config of a specific panel
eink-gateway-cli update-config --panel-id "98:fc:84:e9:92:df" --ssid "My WiFi" --password "My WiFi Password" --websocketUrl "ws://my-websocket-server.com"
```
