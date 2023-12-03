import random
import string

import requests
from datetime import datetime
import pytz
from math import pi, sqrt, sin, cos

from bs4 import BeautifulSoup


class Simaster:
    SIMASTER_URL = "https://simaster.ugm.ac.id"
    LOGIN_URL = f"{SIMASTER_URL}/services/simaster/service_login"
    PRESENSI_URL = f"{SIMASTER_URL}/kkn/presensi/add"
    HEADERS = {"UGMFWSERVICE": "1", "User-Agent": "Praesentia/1.0.0"}

    def __init__(self):
        self.a_id = self._generate_random_a_id()
        self.logged_in = False
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def login(self, username, password):
        print("SEND LOGIN REQUEST")

        self.session.post(
            self.LOGIN_URL,
            data={
                "username": username,
                "password": password,
            },
        )

        return self.is_logged_in()

    def presensi(self, location, randomize=True):
        if randomize:
            location = self._randomize_location(location, distance=50)

        data = {
            "simasterUGM_token": self.session.cookies.get("simasterUGM_cookie"),
            "tanggalPresensi": datetime.now(pytz.timezone("Asia/Jakarta")).strftime(
                "%d-%m-%Y"
            ),
            "agreement": 1,
            **location,
        }

        req = self.session.post(self.PRESENSI_URL, data=data)

        self.session.cookies.clear()
        self.session.close()

        if req.status_code == 200:
            try:
                print(req.json())
            except IOError:
                soup = BeautifulSoup(req.content, "html.parser")
                print(soup.find("div", attrs={"role": "alert"}).text)

    def is_logged_in(self):
        req = self.session.get(self.PRESENSI_URL)

        if req.status_code == 200 and self.session.cookies.get("simasterUGM_cookie"):
            return True

        return False

    def set_session(self, ugm_session):
        self.session.cookies.set(
            "simaster-ugm_sess", ugm_session, domain="simaster.ugm.ac.id"
        )

    def _randomize_location(self, location, distance):
        latitude = location["latitude"]
        longitude = location["longitude"]

        rd = distance / 111300

        w = rd * sqrt(random.random())
        t = 2 * pi * random.random()
        x = w * cos(t)
        y = w * sin(t)

        return {
            "latitude": "{0:.4f}".format(latitude + x),
            "longtitude": "{0:.4f}".format(longitude + y),
        }

    @staticmethod
    def _generate_random_a_id():
        return "".join(random.choice(string.hexdigits) for _ in range(16)).lower()
