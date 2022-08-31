import os
from urllib.request import Request, urlopen
import json
PIP = "pip install {}"
DROP_DOWN_DEFAULT = "*Optional* Server"
try:
    import pyxivapi
except ModuleNotFoundError:
    os.system(PIP.format("pyxivapi"))
    import pyxivapi
    
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

def character_by_id(id):
    request = Request("https://xivapi.com/character/{}".format(id))
    request.add_header('User-Agent', '&lt;User-Agent&gt;')
    data = json.loads(urlopen(request).read())
    return data

def character_by_name(name, server):
    request = Request("https://xivapi.com/character/search?name={}{}{}"
                      .format(name.replace(" ","+"),"" if server.get() == DROP_DOWN_DEFAULT
                              else "&server=",server.get() if server.get() != DROP_DOWN_DEFAULT
                              else ""))
    request.add_header('User-Agent', '&lt;User-Agent&gt;')
    data = json.loads(urlopen(request).read())
    id = (data["Results"][0]["ID"])
    data = character_by_id(id)
    return data


class Character():
    def __init__(self, data):
        self.data = data
        self.canvas_list = []
        
    def write_to_file(self, filename):
        with open(filename, "w") as outfile:
            json.dump(self.data, outfile)
    
    def get_class_job_levels(self):
        self.class_id_in_order = ["Gladiator", "Pugilist", "Marauder", "Lancer",
                             "Archer", "Conjurer", "Thaumaturge", "Carpenter",
                             "Blacksmith", "Armorer", "Goldsmith",
                             "Leatherworker", "Weaver", "Alchemist", 
                             "Culinarian", "Miner", "Botanist", "Fisher",
                             "Paladin", "Monk", "Warrior", "Dragoon",
                             "Bard", "White Mage","Black Mage", "Arcanist",
                             "Summoner", "Scholar", "Rogue", "Ninja",
                             "Machinist","Dark Knight", "Astrologian",
                             "Samurai", "Red Mage", "Blue Mage (Limited Job)", "Gunbreaker",
                             "Dancer", "Reaper", "Sage"]
        role_assignment = {}
        roles = ["Tank", "Healer", "Melee DPS", "Physical Ranged DPS", 
                 "Magical Ranged DPS", "Crafter", "Gatherer"]
        tank_jobs = ["Paladin", "Warrior", "Dark Knight", "Gunbreaker"]
        tank_class = ["Gladiator", "Marauder"]
        heal_jobs = ["White Mage", "Scholar", "Astrologian", "Sage"]
        heal_class = ["Conjurer"]
        melee_dps_job = ["Monk", "Dragoon", "Ninja", "Samurai", "Reaper"]
        melee_dps_class = ["Pugilist", "Lancer", "Rogue"]
        phys_rang_dps_job = ["Bard", "Machinist", "Dancer"]
        phys_rang_dps_class = ["Archer"]
        mag_rang_dps_job = ["Black Mage", "Summoner", "Red Mage",
                            "Blue Mage (Limited Job)"]
        mag_rang_dps_class = ["Thaumaturge", "Arcanist"]
        crafters = ["Carpenter", "Blacksmith", "Armorer", "Goldsmith", 
                    "Leatherworker", "Weaver", "Alchemist", "Culinarian"]
        gatherers = ["Botanist", "Miner", "Fisher"]
        self.all_classes_and_jobs = [[tank_jobs, tank_class], 
                                [heal_jobs, heal_class], 
                                [melee_dps_job, melee_dps_class], 
                                [phys_rang_dps_job, phys_rang_dps_class], 
                                [mag_rang_dps_job, mag_rang_dps_class], 
                                [crafters], 
                                [gatherers]]
        for index,role in enumerate(roles):
            role_assignment[role] = self.all_classes_and_jobs[index]
        
        self.level_dict = {}
        for i in self.class_id_in_order:
            self.level_dict[i] = '--'
        df1 = pd.DataFrame(self.data["Character"]["ClassJobs"])
        for index, row in df1.iterrows():
            if row["Level"] != 0:
                self.level_dict[self.class_id_in_order[row["ClassID"]-1]] = row["Level"]
                if row["ClassID"] != row["JobID"]:
                    self.level_dict[self.class_id_in_order[row["UnlockedState"]["ID"]-1]] = row["Level"]
                
    def print_class_levels(self):
        row = 0
        for index, value in enumerate(self.all_classes_and_jobs):
            col  = 1
            for idx,classes in enumerate(value):
                if (idx==1):
                    print(" "*17*(7-col), end = '')
                    col = 7
                for each in classes:
                    printed = each
                    if(each == "Blue Mage (Limited Job)"):
                        printed = "Blue Mage"
                        print(" "*17,end="")
                        col+=1
                    print("{:>13}:{:>02}".format(printed, self.level_dict[each]),end=" ")
                    col+=1
            col=0
            row+=1
            print()
            if row == 5:
                print("\n")
                row+=1