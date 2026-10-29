
import winreg
import json
from datetime import datetime
import os

# Example: Read a Windows Registry key
key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion"

try:
    with winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        key_path
    ) as key:
        print("Registry key opened successfully")

except OSError as error:
    print("Error accessing registry:", error)
