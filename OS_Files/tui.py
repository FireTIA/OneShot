from OS_Files.oss import Check_System_GET_OS
from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
from colorama import init
from OS_Files.db import OneShot_ver, OneShot_ver_date, OneShot_ver_type, OneShot_ver_platform, OneShot_ver_type_short

just_fix_windows_console()
init(autoreset=True)

def banner():
    print(f"| < {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET} - {Fore.LIGHTCYAN_EX}OneShotPin {Fore.LIGHTGREEN_EX}WPS{Fore.RESET}")
    print(f"| - Перевод от {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET}")
    print(f"| - Ваш дистрибутив: {Fore.LIGHTCYAN_EX}{Check_System_GET_OS()}{Fore.RESET}")
    print(f"| > {Fore.LIGHTMAGENTA_EX}{OneShot_ver} - {OneShot_ver_date} {Fore.YELLOW}{OneShot_ver_type} {OneShot_ver_platform}{Fore.RESET}") 

