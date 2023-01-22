
import os

import requests
import telegram
from bs4 import BeautifulSoup

DB_FILE = 'found_flats/wbm_flats.txt'
WBM_URL = 'https://www.wbm.de'
WBM_ANGEBOTE_URL = WBM_URL + '/wohnungen-berlin/angebote/'
WBM_POST_DATA = {
    'tx_openimmo_immobilie[__referrer][@extension]': "Openimmo",
    'tx_openimmo_immobilie[__referrer][@vendor]': "CodingMs",
    'tx_openimmo_immobilie[__referrer][@controller]': "Immobilie",
    'tx_openimmo_immobilie[__referrer][@action]': "quickSearch",
    'tx_openimmo_immobilie[__referrer][arguments]': "YTowOnt9ef52e62da51d49537d9b67d61f39b458b8f18280",
    'tx_openimmo_immobilie[__referrer][@request]': 'a:4:{s:10:"@extension";s:8:"Openimmo";s:11:"@controller";s:9:"Immobilie";s:7:"@action";s:11:"quickSearch";s:7:"@vendor";s:8:"CodingMs";}423cd327bd0ba9eaf6998f093bf5279578d705b8',
    'tx_openimmo_immobilie[__trustedProperties]': 'a:5:{s:6:"search";i:1;s:3:"ort";i:1;s:11:"wohnflaeche";i:1;s:14:"nettokaltmiete";i:1;s:12:"anzahlZimmer";i:1;}628c8aa2c16f9ebd44b15add2e4e247a48d99ddf',
    'tx_openimmo_immobilie[search]': "search",
    'tx_openimmo_immobilie[ort]': "Berlin",
    'tx_openimmo_immobilie[regionalerZusatz]': "",
    'tx_openimmo_immobilie[wohnflaeche]': "0_0",
    'tx_openimmo_immobilie[nettokaltmiete]': "0_0",
    "tx_openimmo_immobilie[anzahlZimmer]": "4_4"
}

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

bot = telegram.Bot(token=TOKEN)

with open(DB_FILE, 'r') as flat_file:
    seen_flats = flat_file.read()

response = requests.post(WBM_ANGEBOTE_URL, WBM_POST_DATA)
if response.content is not None:
    html = BeautifulSoup(response.content, 'html.parser')
    flats = html.find_all(attrs={'class': 'row openimmo-search-list-item'})
    for flat in flats:
        flat_id = flat.attrs['data-id']
        if flat_id in seen_flats:
            continue

        with open(DB_FILE, 'a') as flat_file:
            flat_file.write(f',{flat_id}')
        flat_link = flat.find('a').attrs['href']

        bot.send_message(
            chat_id=CHAT_ID,
            text=f'Neue Wohnung aktiv:\nID #{flat_id}\nLink: {WBM_URL + flat_link}'
        )

print('WBM search finished')
