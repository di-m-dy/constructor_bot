"""
Module for configuration of the application
"""
import os
import json
import dotenv

import requests


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.abspath(ROOT_DIR))
WEB_APP_DIR = os.path.join(PROJECT_DIR, 'web_app/')

dotenv.load_dotenv(os.path.join(PROJECT_DIR, ".env"))

TG_TOKEN = os.getenv("TG_TOKEN")
GOD_ID = os.getenv("GOD_ID")

DB_PATH = os.getenv("DB_PATH")
# API URLS
MAIN_URL = os.getenv("MAIN_URL")

API_BOT_MESSAGE = MAIN_URL + 'bot_messages'
API_POSITION = MAIN_URL + 'positions'
API_ADD_USER = MAIN_URL + 'add_user'
API_GET_USER = MAIN_URL + 'get_user/'
API_GET_ADMIN = MAIN_URL + 'get_admins'
API_ADD_ADMIN = MAIN_URL + 'add_admin'


# DEFAULT_MEDIA


class ApiBase:
    DEFAULT = []

    def __init__(self, url: str):
        self.url = url
        self.data = self.DEFAULT

    def update_data(self) -> list[dict[str, str]] | None:
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                data = response.json()
                return data
        except Exception:
            return

    def get_update(self):
        data = self.update_data()
        if data:
            self.data = data


# DEFAULT DATA
class BotMessage(ApiBase):
    def __init(self, url):
        super().__init__(url)

    def command_list(self) -> list:
        commands = [i['command'] for i in self.data]
        return commands

    def get_command(self, command: str) -> dict | None:
        command_data = [i for i in self.data if i['command'] == command]
        if command_data:
            return command_data[0]
        return


class Position(ApiBase):
    DEFAULT = []

    def position_list(self) -> list:
        positions = [f"position_{i['position']}" for i in self.data]
        return positions

    def get_position(self, position: str):
        index = int(position.split('_')[-1])
        position = [item for item in self.data if item['position'] == index]
        if position:
            return position[0]
        return


def check_user(user_id: int, first_name: str = None, last_name: str = None, username: str = None):
    check_url = API_GET_USER + str(user_id)
    check_response = requests.get(check_url)
    if check_response.json()["status"] == "error":
        params = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username
        }
        response = requests.get(API_ADD_USER, params=params)


def get_admins() -> list:
    response = requests.get(API_GET_ADMIN)
    if response.status_code == 200:
        return response.json()['body']
    return []

