import requests
from bs4 import BeautifulSoup
import os

PIP = "pip install {}"
DROP_DOWN_DEFAULT = "*Optional* Server"

try:
    import win32api
    import win32con
    import win32gui
except ModuleNotFoundError:
    os.system(PIP.format("pywin32"))
    import win32api
    import win32con
    import win32gui
    
COL = 21
DARK_BLUE = "#192841"
TRANSPARENT = "#000000"

try:
    import pandas as pd
except ModuleNotFoundError:
    os.system(PIP.format("pandas"))
    import pandas as pd

try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    os.system(PIP.format("pillow"))
    from PIL import Image, ImageTk

try:
    import pyautogui
except ModuleNotFoundError:
    os.system(PIP.format("pyautogui"))
    import pyautogui


SERVERS_LIST = ["Adamantoise","Aegis","Alexander","Anima","Asura","Atomos",
                "Bahamut","Balmung","Behemoth","Belias","Brynhildr","Cactuar",
                "Carbuncle","Cerberus","Chocobo","Coeurl","Diabolos",
                "Durandal","Excalibur","Exodus","Faerie","Famfrit","Fenrir",
                "Garuda","Gilgamesh","Goblin","Gungnir","Hades","Hyperion",
                "Ifrit","Ixion","Jenova","Kujata","Lamia","Leviathan","Lich",
                "Louisoix","Malboro","Mandragora","Masamune","Mateus",
                "Midgardsormr","Moogle","Odin","Omega","Pandaemonium",
                "Phoenix","Ragnarok","Ramuh","Ridill","Sargatanas","Shinryu",
                "Shiva","Siren","Tiamat","Titan","Tonberry","Typhon","Ultima",
                "Ultros","Unicorn","Valefor","Yojimbo","Zalera","Zeromus",
                "Zodiark","Spriggan","Twintania","Bismarck","Ravana",
                "Sephirot","Sophia","Zurvan","HongYuHai","ShenYiZhiDi",
                "LaNuoXiYa","HuanYingQunDao","MengYaChi","YuZhouHeYin",
                "WoXianXiRan","ChenXiWangZuo","BaiYinXiang","BaiJinHuanXiang",
                "ShenQuanHen","ChaoFengTing","LvRenZhanQiao","FuXiaoZhiJian",
                "Longchaoshendian","MengYuBaoJing","ZiShuiZhanQiao","YanXia",
                "JingYuZhuangYuan","MoDuNa","HaiMaoChaWu","RouFengHaiWan",
                "HuPoYuan","ShuiJingTa2","YinLeiHu2","TaiYangHaiAn2","YiXiuJiaDe2",
                "HongChaChuan2","Alpha","Phantom","Raiden","Sagittarius"]


def fetch_character_image(character_id):
    # Construct the Lodestone URL
    url = f"https://na.finalfantasyxiv.com/lodestone/character/{character_id}/"

    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the URL: {response.status_code}")
        return None

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <img> tag inside the 'character__detail__image' div
    image_tag = soup.select_one(".character__detail__image img")
    if image_tag and 'src' in image_tag.attrs:
        return image_tag['src']
    else:
        print("Image source not found.")
        return None

def get_free_company(character_id):
    # Construct the Lodestone URL
    url = f"https://na.finalfantasyxiv.com/lodestone/character/{character_id}/"

    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the URL: {response.status_code}")
        return None

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    free_company_element = soup.select_one(".character__freecompany__name a")
    free_company = free_company_element.text.strip() if free_company_element else "No Free Company"
    return free_company




def fetch_character_data(character_id):
    # Construct the Lodestone URL
    base_url = f"https://na.finalfantasyxiv.com/lodestone/character/{character_id}"
    url = f"{base_url}/class_job/"

    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the URL: {response.status_code}")
        return None

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract character data
    try:
        # Character Name
        character_name = soup.select_one(".frame__chara__name").text.strip()

        # World Name
        world_name_element = soup.select_one(".frame__chara__world")
        world_name = world_name_element.text.strip() if world_name_element else "Unknown World"

        # Levels with Job Icons
        levels = {}
        job_elements = soup.select("ul.character__job.clearfix li")
        for job in job_elements:
            job_name_element = job.select_one(".character__job__name")
            job_level_element = job.select_one(".character__job__level")
            job_icon_element = job.select_one(".character__job__icon img")

            if job_name_element and job_level_element and job_icon_element:
                job_name = job_name_element.text.strip()
                job_level = job_level_element.text.strip()
                job_icon = job_icon_element['src']  # Extract the icon's src attribute

                levels[job_name] = {
                    "Level": job_level,
                    "Icon": job_icon
                }

        # Structure the data
        character_data = {
            "Character Name": character_name,
            "Character ID": character_id,
            "World Name": world_name,
            "Free Company": get_free_company(character_id),
            "Character Image": fetch_character_image(character_id),
            "Levels": levels,
        }

        return character_data

    except Exception as e:
        print(f"Error parsing character data: {e}")
        return None


def save_character_data_to_json(character_data, filename):
    import json
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(character_data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")


# Example usage
if __name__ == "__main__":
    character_id = "44250261"  # Replace with the desired character ID
    character_data = fetch_character_data(character_id)

    if character_data:
        save_character_data_to_json(character_data, "character_data.json")
