from os import system
from requests import Session
from json import JSONDecodeError
from uuid import uuid4
from time import sleep
from colorama import Fore
from hashlib import md5
from requests.exceptions import ReadTimeout , ConnectTimeout , ConnectionError
from random import choice
from pyfiglet import figlet_format
import datetime as abc
import platform

#github.com/MystiqueShade | Channel : @MystiqueShade


system("clear")
Creator = "EditeD By: @MystiqueShade"
print(figlet_format(Creator))
sleep(.3)
system("clear")


#Start Code...
def decode(data):
    final_string = ''
    for key in data.keys():
        final_string += f"{key}={data[key]}&"
    return final_string[:-1]


def load_account(session , restore_key):
    data = {'game_version' : '1.7.10655' , 'device_name' : 'unknown' , 'os_version' : '10' , 'model' : 'SM-A750F' , 'udid' : str(uuid4().int) , 'store_type' : 'iraqapps' , 'restore_key' : restore_key , 'os_type' : 2}
    try:
        return session.post('http://iran.fruitcraft.ir/player/load' , decode(data) , timeout = 5).json()
    except JSONDecodeError:
        system("clear")
        print(f'{Fore.RED}Error connecting to the game! - Code: << {restore_key} >>{Fore.RESET}\nSomeone is playing on the account or the recovery code is wrong.\n\n')
        exit()


def update_cards():
    global cards
    cards.append(cards[0])
    cards.pop(0)


def getenemys(session , **args):
    while True:
        try:
            enemys = sorted(session.get('http://iran.fruitcraft.ir/battle/getopponents').json()['data']['players'] , key = lambda x: x['def_power'])
            if enemys:
                if args["sort"]:
                    return list(filter(lambda i: i['def_power'] and i['def_power'] <= args["power"] , enemys))
                return enemys
            else:
                print(f"{Fore.RED}• Error searching for enemies!\n{Fore.YELLOW}Please wait 10 seconds For research...\n\n")
                sleep(10)
        except JSONDecodeError:
            print(f"\n\n{Fore.YELLOW}We were limited by the server. Wait 30 seconds...!{Fore.RESET}\n\n")
            sleep(30)
        except ReadTimeout:
            pass
        except Traceback:
            pass
        except Exception as e:
            print(e)
            print(f"{Fore.RED}• Error searching for enemies!\n{Fore.YELLOW}Please wait 3 seconds For research...{Fore.RESET}\n\n")
            sleep(3)


def battle(session , opponent_id , q , cards , attacks_in_today , hero_id = None):
    data = {'opponent_id': opponent_id , 'check' : md5(str(q).encode()).hexdigest() , 'cards' : str(cards).replace(' ', '') , 'attacks_in_today' : attacks_in_today}
    if hero_id: data['hero_id'] = hero_id
    return session.get('http://iran.fruitcraft.ir/battle/battle?' + decode(data) , timeout = 5).json()


attacked = {}


def attack(session , power , attack_range , delay):
    win , lose , doon , xp ,totaldoon= 0 , 0 , 0 , 0, 0
    q = load['data']['q']
    while "T_Ki" in Creator:
        enemys = getenemys(session2 , sort = True , power = power)
        while not enemys:
            enemys = getenemys(session , sort = True , power = power)
        print(f"{Fore.GREEN}{len(enemys)} Enemies found...{Fore.RESET}")
        print(f"{Fore.GREEN}• Your strength is more than {len(enemys)} people...{Fore.RESET}\n\n")
        for enemy in enemys:
            if enemy['id'] not in attacked: attacked[enemy['id']] = 1
            if (not enemy['def_power']) or int(enemy['def_power']) > power or attacked[enemy['id']] >= 50:
                continue
            for i in range(attack_range):
                if attacked[enemy['id']] >= 50: continue
                try:
                    update_cards()
                    q = battle(session , enemy['id'] , q , [cards[0]] , attacked[enemy['id']])
                    if q["status"] == False:
                        if int(q["data"]["code"]) == 122:
                            break
                        if int(q["data"]["code"]) == 124:
                            print(f"{Fore.RED}Error in Attack by the server. Wait 500 seconds...!{Fore.RESET} 124\n\n")
                            session.close()
                            sleep(500)
                            load_account(session , code)
                        else:
                            print(q)
                            continue
                    attacked[enemy['id']] += 1
                    if q['data']['score_added'] >= 0 and q["data"]["xp_added"] > 0:
                        win += 1
                        print(f"{Fore.GREEN}Result: You Win...! Name: << {enemy['name']} >> - Clan name: << {enemy['tribe_name']} >>{Fore.RESET}")
                    else:
                        attacked[enemy['id']] = 200
                        lose += 1
                        print(f"{Fore.RED}Result: You Lost...! Name: << {enemy['name']} >> - Clan name: << {enemy['tribe_name']} >>{Fore.RESET}")
                    xp += q["data"]["xp_added"]
                    doon += q['data']['score_added']
                    totaldoon = q['data']['weekly_score']
                    q = q['data']['q']
                except JSONDecodeError:
                    print(f"\n\n{Fore.YELLOW}We were limited by the server. Wait 30 seconds...!{Fore.RESET}\n\n")
                    q = load['data']['q']
                    sleep(30)
                except ReadTimeout:
                    print("readtime , Net Shoma Zaiefe!")
                    #q = load['data']['q']
                    pass
                except KeyError:
                    print(q)
                    #q = load['data']['q']
                    pass
                except (ConnectTimeout , ConnectionError):
                    #q = load['data']['q']
                    print(f"\n\n{Fore.YELLOW}Your internet is interrupted, there is a 5 second delay until the next task...!{Fore.RESET}\n\n")
                    sleep(5)
                except Exception as e:
                    print(e , type(e))
                    pass
                sleep(delay)
            print(f"{Fore.GREEN}[TotalDooN: {totaldoon}]• The last result ••• Win: {str(win)}{Fore.RESET} ••• {Fore.RED}Lost: {str(lose)}{Fore.RESET} ••• Xp: {str(xp)} ••• DoonAdd: {str(doon)}\n\n")



session = Session()
session2 = Session()
session.headers.update({'User-Agent' : 'Dalvik/2.1.0 (Linux; U; Android 10; PO-X1100 Build/RP1A.200320.012)' , 'Accept-Encoding' : 'gzip' , 'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'})
session2.headers.update({'User-Agent' : 'Dalvik/2.1.0 (Linux; U; Android 10; PO-X1100 Build/RP1A.200320.012)' , 'Accept-Encoding' : 'gzip' , 'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'})
code = input("• Enter your first account code: ")
code2 = input("• Enter your two account code: ")
load = load_account(session , code)
load2 = load_account(session2 , code2)
cards = [i['id'] for i in load['data']['cards'] if i['power'] < 100]
if len(cards) < 20:
    print(f"{Fore.RED}You have less than 20 cards in << {load['data']['name']} >> account!")
    exit()
print(f"{Fore.GREEN}You have successfully connected to << {load['data']['name']} >> account{Fore.RESET}")



power = int(input('Enter Your Power: '))
rng = int(input('Attack count: '))
slp = float(input("Enter Delay: "))
print("\n\n")



attack(session , power  , rng , slp)