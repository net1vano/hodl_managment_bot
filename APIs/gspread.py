import aiohttp
import asyncio
import aiospread
from oauth2client.service_account import ServiceAccountCredentials
import json


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

#credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

async def opensht():
    wks = await aiospread.authorize(json.load(open('client_secret.json')))
    sheet = await wks.open_by_url("https://docs.google.com/spreadsheets/d/1qhkAmrrPzTuTVj99G3VsYMVdpxzZdIbjxfkdGPr-79E/edit?gid=0#gid=0")
    print(sheet.__str__())
    cell_list = await wks.range('A1:B7')

asyncio.get_event_loop().run_until_complete(opensht())