"""Merak Bahcesi icin yalnizca bu bilgisayarda calisan yerel test sunucusu."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import threading
import webbrowser

ROOT = Path(__file__).resolve().parent


def main():
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    port = int(os.environ.get('MERAK_PORT', '3000'))
    try:
        server = ThreadingHTTPServer(('127.0.0.1', port), handler)
    except OSError as error:
        if error.errno not in (48, 98, 10048):
            raise
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    url = f'http://127.0.0.1:{server.server_port}/'
    print(f'Merak Bahcesi yerel test adresi: {url}', flush=True)
    print('Durdurmak icin bu pencerede Ctrl+C tuslarina basin.', flush=True)
    print('Videolar ve ozel soru servisi baglanana kadar bu alanlar beklemede gorunur.', flush=True)
    if os.environ.get('MERAK_NO_BROWSER') != '1':
        timer = threading.Timer(0.4, webbrowser.open, args=(url,))
        timer.daemon = True
        timer.start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
