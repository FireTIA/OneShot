from datetime import datetime
import datetime
import colorama
from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
from colorama import init
import random

from OS_file.os import OS__Check_System_GET_OS, OS__date_time
from OS_file.db import fun_notice_dev
from OS_file.settings import SETT__load_param, SETT_menu
from OS_file.wlanx import WlanX__get_wifi_driver, WlanX__detect_chipset_airmon_style

just_fix_windows_console()
init(autoreset=True)



# [FS]
FS_prefix = f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET}" 





#
# GUI с инфой перед запуском
#

def CLI_GUI__Banner_startup():
    if SETT__load_param()["Hello_banner"].lower() in ["compact", "minimal"]:
        print(f"\n| - {Fore.LIGHTCYAN_EX}OneShotPin 0.0.56b{Fore.LIGHTGREEN_EX} WPS{Fore.RESET}\n")
    elif SETT__load_param()["Hello_banner"].lower() in ["classic"]:
        print(f"\n| < {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET} - {Fore.LIGHTCYAN_EX}OneShotPin {Fore.LIGHTGREEN_EX}WPS{Fore.RESET}")
        print(f"| > {Fore.LIGHTMAGENTA_EX}0.0.56 - 2026.02 {Fore.YELLOW}BETA{Fore.RESET} \n")
    elif SETT__load_param()["Hello_banner"].lower() in ["none", "false", "off", "offed"]:
        return
    else:
        print(f"\n| < {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET} - {Fore.LIGHTCYAN_EX}OneShotPin {Fore.LIGHTGREEN_EX}WPS{Fore.RESET}")
        print(f"| - Перевод от {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET}")
        print(f"| - {Fore.LIGHTWHITE_EX}Git{Fore.LIGHTBLACK_EX}Hub{Fore.RESET}: github.com/FireTIA/OneShot")
        print(f"| > {Fore.LIGHTMAGENTA_EX}0.0.56 - 2026.02 {Fore.YELLOW}BETA{Fore.RESET} \n")


#
# GUI менюшки с инфой
#

def CLI_GUI__Banner_info(iface_args):
    print(f"{FS_prefix} Заметки разработчика: {random.choice(fun_notice_dev)}\n")
    print(f"|=== Информация")
    print(f"| - Ваш дистрибутив: {Fore.LIGHTCYAN_EX}{OS__Check_System_GET_OS()}{Fore.RESET}")
    print(f"| - Дата/время: {Fore.LIGHTCYAN_EX}{OS__date_time("date-times")}{Fore.RESET}")
    print(f"|| - Выбранный wlan: {Fore.LIGHTCYAN_EX}{iface_args}{Fore.RESET}")
    print(f"|| - Чипсет: {Fore.LIGHTCYAN_EX}{WlanX__detect_chipset_airmon_style(iface_args)}{Fore.RESET}")
    print(f"|| - Драйвер: {Fore.LIGHTCYAN_EX}{WlanX__get_wifi_driver(iface_args)}{Fore.RESET}\n")


#
# GUI менюшкой
#

def CLI_GUI__MENU(iface_args):
    while True:
        
        CLI_GUI__Banner_info(iface_args)
    
        print("""
|===============
|>> Меню
| 1. Настройки
| 10. Продолжить запуск
|===============
        """)

        select = input("|> ")

        if select in ["1"]:
            SETT_menu()
        elif select in ["10"]:
            break
        else:
            lol=1

