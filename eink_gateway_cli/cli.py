#!/usr/bin/env python

import os
import sys
from base64 import b64encode
from mimetypes import guess_type
from urllib.error import HTTPError
from argparse import ArgumentParser

from .core import EInkGatewayClient, EInkColorMode


def get_panels(args):
    client = EInkGatewayClient(args.api_url, args.api_key)
    response = client.get_pannels()
    if isinstance(response, HTTPError):
        print(f'Error: {response.read()}')
        return
    print(response)


def get_panel(args):
    client = EInkGatewayClient(args.api_url, args.api_key)
    response = client.get_panel(args.panel_id)
    if isinstance(response, HTTPError):
        print(f'Error: {response.read()}')
        return
    print(response)


def display_image(args):
    client = EInkGatewayClient(args.api_url, args.api_key)

    image_url = args.image_path
    mimetype, encoding = guess_type(image_url)

    # if the image is a local file, read it
    if os.path.isfile(args.image_path):
        if not mimetype:
            print(f'Error: Could not determine mimetype for {image_url}', file=sys.stderr)
            exit(1)

        with open(image_url, 'rb') as f:
            encoded_binary = b64encode(f.read()).decode('utf-8')
            image_url = f'data:{mimetype};base64,{encoded_binary}'

    response = client.display_image(panel_id=args.panel_id, image_url=image_url, mode=EInkColorMode(args.mode))
    if isinstance(response, HTTPError):
        print(f'Error: {response.read()}')
        return
    print(response)


def reboot(args):
    client = EInkGatewayClient(args.api_url, args.api_key)
    response = client.reboot(args.panel_id)
    if isinstance(response, HTTPError):
        print(f'Error: {response.read()}')
        return
    print(response)


def ota(args):
    client = EInkGatewayClient(args.api_url, args.api_key)
    response = client.ota(args.panel_id, args.ota_url)
    if isinstance(response, HTTPError):
        print(f'Error: {response.read()}')
        return
    print(response)


def update_config(args):
    client = EInkGatewayClient(args.api_url, args.api_key)
    response = client.update_config(args.panel_id, args.config)
    if isinstance(response, HTTPError):
        print(f'Error: {response}')
        return
    print(response)


def main():
    main_parser = ArgumentParser(prog='eink-gateway-cli')
    main_parser.add_argument('--api-key', default=os.environ.get('EINK_GATEWAY_API_KEY'))
    main_parser.add_argument('--api-url', default=os.environ.get('EINK_GATEWAY_API_URL'))

    commands_subparser = main_parser.add_subparsers(dest='command')
    commands_subparser.required = True

    # get-panels
    get_panels_parser = commands_subparser.add_parser('get-panels')
    get_panels_parser.set_defaults(func=get_panels)

    # get-panel
    get_panel_parser = commands_subparser.add_parser('get-panel')
    get_panel_parser.add_argument('--panel-id', type=str)
    get_panel_parser.set_defaults(func=get_panel)

    # display-image
    display_image_parser = commands_subparser.add_parser('display')
    display_image_parser.add_argument('image_path', type=str)
    display_image_parser.add_argument('--panel-id', type=str, default='all')
    display_image_parser.add_argument('--mode', type=str, choices=['1bit', '3bit'], default='3bit')
    display_image_parser.set_defaults(func=display_image)

    # reboot
    reboot_parser = commands_subparser.add_parser('reboot')
    reboot_parser.add_argument('--panel-id', type=str, default='all')
    reboot_parser.set_defaults(func=reboot)

    # ota
    ota_parser = commands_subparser.add_parser('ota')
    ota_parser.add_argument('--panel-id', type=str, default='all')
    ota_parser.add_argument('ota-url', type=str)
    ota_parser.set_defaults(func=ota)

    # update-config
    update_config_parser = commands_subparser.add_parser('update-config')
    update_config_parser.add_argument('--panel-id', type=str, default='all')
    update_config_parser.add_argument('--ssid', type=str)
    update_config_parser.add_argument('--password', type=str)
    update_config_parser.add_argument('--websocket-url', type=str)
    update_config_parser.set_defaults(func=update_config)

    args = main_parser.parse_args()

    if not args.api_key:
        print('Error: API key is required', file=sys.stderr)
        print('Hint: export EINK_GATEWAY_API_KEY="your-api-key" or via --api-key', file=sys.stderr)
        exit(1)

    if not args.api_url:
        print('Error: API URL is required', file=sys.stderr)
        print('Hint: export EINK_GATEWAY_API_URL="http://..." or via --api-url', file=sys.stderr)
        exit(1)

    args.func(args)


if __name__ == '__main__':
    main()

