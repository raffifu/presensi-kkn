import os
from Simaster import Simaster

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

if not USERNAME or not PASSWORD:
    raise RuntimeError("USERNAME and PASSWORD must be set")

simaster = Simaster()

# TODO: Implement reuse session from Simaster.set_session
if not simaster.login(USERNAME, PASSWORD):
    raise RuntimeError("Not authenticate")

simaster.presensi(location={"latitude": -7.771332, "longitude": 110.376738})
