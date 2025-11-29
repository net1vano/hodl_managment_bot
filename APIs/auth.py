from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from utils.stats_dataclass import *
from utils.auth import get_all_aliases
import ssl
import logging
import asyncio
import os
SHEET_ID = '1qhkAmrrPzTuTVj99G3VsYMVdpxzZdIbjxfkdGPr-79E'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

current_dir = os.path.dirname(os.path.abspath(__file__))
service_account_path = os.path.join(current_dir, '..', 'service_account.json')


class Spreads:
    def __init__(self):
        self.scopes = SCOPES
        self.sheet_id = SHEET_ID
        self.service_account = os.path.dirname(os.path.abspath(__file__))
        self.service_account = os.path.join(self.service_account, '..', 'service_account.json')
        self.credentials = Credentials.from_service_account_file(self.service_account, scopes=self.scopes)
        self.service = build('sheets', 'v4', credentials=self.credentials)

    @retry(
        retry=retry_if_exception_type((OSError, EOFError, ssl.SSLEOFError, HttpError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def get_sheets_list(self):
        result = self.service.spreadsheets().get(spreadsheetId=self.sheet_id).execute()
        sheets = result.get('sheets', [])
        sheet_names = [sheet['properties']['title'] for sheet in sheets]
        return sheet_names

    @retry(
        retry=retry_if_exception_type((OSError, EOFError, ssl.SSLEOFError, HttpError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def get_sheet_data(self, range_name: str):
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=range_name
        ).execute()
        values = result.get('values', [])
        return values

    @retry(
        retry=retry_if_exception_type((OSError, EOFError, ssl.SSLEOFError, HttpError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def append_to_sheet(self, range_name: str, values: list[list]):
        body = {'values': values}
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f'Добавлено {result.get("updates").get("updatedRows")} строк')

    async def append_row_data(self, values: list[list] ):
        await self.append_to_sheet(range_name="rowdata!A:F", values=values)

    async def parse_data_to_dataclass(self, data): ##[ [[row_cell, row_cell]]], [row]]
        years = AllData()
        names = get_all_aliases()
        year, month = "", ""
        for row in data:
            if not row:
                continue
            if len(row) == 2:
                if row[1].lower() in months:
                    year = row[0]
                    month = months.get(row[1])
            if len(row) >= 13 and (year != "" and month != ""):
                if row[1] in names:
                    years.add_or_update_person(year=year, month=month, name=row[1], total_amount=row[-1], balance=row[-2])
        return years
