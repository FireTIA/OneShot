from datetime import datetime
import datetime
import colorama
from colorama import Fore, Back, Style
from colorama import init
import os
import random


from OS_file.os import OS__Check_System_GET_OS, OS__date_time
from OS_file.db import fun_notice_dev
from OS_file.settings import SETT__load_param, SETT_menu
from OS_file.wlanx import WlanX__get_wifi_driver, WlanX__detect_chipset_airmon_style

init(autoreset=True)



# [FS]
FS_prefix = f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET}" 





#
# GUI с инфой перед запуском
#

def CLI_GUI__Banner_startup():
    if SETT__load_param()["Hello_banner"].lower() in ["compact", "minimal"]:
        print(f"\n| - {Fore.LIGHTCYAN_EX}OneShotPin 0.0.60b{Fore.LIGHTGREEN_EX} WPS{Fore.RESET}\n")
    elif SETT__load_param()["Hello_banner"].lower() in ["classic"]:
        print(f"\n| < {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET} - {Fore.LIGHTCYAN_EX}OneShotPin {Fore.LIGHTGREEN_EX}WPS{Fore.RESET}")
        print(f"| > {Fore.LIGHTMAGENTA_EX}0.0.60 - 2026.03 {Fore.YELLOW}BETA{Fore.RESET} \n")
    elif SETT__load_param()["Hello_banner"].lower() in ["none", "false", "off", "offed"]:
        return
    else:
        print(f"\n| < {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET} - {Fore.LIGHTCYAN_EX}OneShotPin {Fore.LIGHTGREEN_EX}WPS{Fore.RESET}")
        print(f"| - Перевод от {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET}")
        print(f"| - {Fore.LIGHTWHITE_EX}Git{Fore.LIGHTBLACK_EX}Hub{Fore.RESET}: github.com/FireTIA/OneShot")
        print(f"| > {Fore.LIGHTMAGENTA_EX}0.0.60 - 2026.03 {Fore.YELLOW}BETA{Fore.RESET} \n")


#
# GUI менюшки с инфой
#

def CLI_GUI__Banner_info(iface_args):
    print(f"{FS_prefix} Заметки разработчика: {random.choice(fun_notice_dev)}\n")
    print(f"|=== Информация")
    print(f"| - Ваш дистрибутив: {Fore.LIGHTCYAN_EX}{OS__Check_System_GET_OS()}{Fore.RESET}")
    print(f"| - Дата/время: {Fore.LIGHTCYAN_EX}{OS__date_time('date-times')}{Fore.RESET}")
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

#
# GUI Вывода тестирования, и сохранения результатов.
#


def CLI_GUI__Out_Write_result_test(wps_pin=None, wpa_psk=None, essid=None, bssid=None):
    settings = SETT__load_param()

    print(
        f"\n{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]"
        f"{Fore.RESET} Получение настроек и аргументов...\n"
    )

    def mask_value(value, mode, pbc_suffix=""):
        if value is None:
            return "None"

        if mode in ["True", "true"]:
            if value == "<PBC mode>":
                return f"{Fore.GREEN} <PBC mode> {Fore.LIGHTYELLOW_EX}{pbc_suffix}{Fore.RESET}"
            return f"{Fore.LIGHTGREEN_EX}{'*' * len(value)}{Fore.RESET}"

        if mode in ["Half", "half"]:
            if value == "<PBC mode>":
                return f"{Fore.GREEN} <PBC mode> {Fore.LIGHTYELLOW_EX}{pbc_suffix}{Fore.RESET}"
            half_length = len(value) // 2
            hidden_half = '*' * half_length + value[half_length:]
            return f"{Fore.LIGHTGREEN_EX}{hidden_half}{Fore.RESET}"

        return f"{Fore.LIGHTGREEN_EX}{value}{Fore.RESET}"

    def get_log_folder():
        os_target = settings.get("OS_Target")

        if os_target is None or str(os_target).strip() == "":
            default_path = "/tmp/OneShotPin_Log"

            print(
                f"\n{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]"
                f"{Fore.RESET} Путь к папке с логами '{Fore.LIGHTCYAN_EX}{default_path}{Fore.RESET}'..."
            )

            return default_path

        os_target = str(os_target).strip()

        paths = {
            "NetHunter": "/sdcard/nh_files/OneShotPin_Log",
            "Kali": "/home/kali/OneShotPin_Log",
        }

        log_path = paths.get(os_target, os_target)

        print(
            f"\n{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]"
            f"{Fore.RESET} Путь к папке с логами '{Fore.LIGHTCYAN_EX}{log_path}{Fore.RESET}'..."
        )

        return log_path

    def ensure_log_folder(folder_path):
        print(
            f"\n{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]"
            f"{Fore.RESET} Поиск папки '{Fore.LIGHTCYAN_EX}OneShotPin_Log{Fore.RESET}'..."
        )

        if not os.path.exists(folder_path):
            print(
                f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]"
                f"{Fore.RESET} Создание папки '{Fore.LIGHTCYAN_EX}OneShotPin_Log{Fore.RESET}'..."
            )
            os.makedirs(folder_path, exist_ok=True)

    def search_wifi_mac(folder_path, target_bssid):
        if not target_bssid:
            return None

        formatted_bssid = target_bssid.replace(":", "-")

        for filename in os.listdir(folder_path):
            if formatted_bssid in filename:
                return filename

        return None

    def save_log(folder_path, wps_pin, wpa_psk, essid, bssid, type_save):
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        current_datetime_text = datetime.datetime.now().strftime("%Y-%m-%d / %H-%M-%S")
        formatted_bssid_file = (bssid or "unknown_bssid").replace(":", "-")

        if type_save == "Update_new_wn":
            file_name = f"{formatted_bssid_file}=UP={current_datetime}.OSP_Complete"
            status_text = "Повторный тест | Retest"
        elif type_save == "Save_new_wn":
            file_name = f"{formatted_bssid_file}={current_datetime}.OSP_Complete"
            status_text = "Впервые протестированно | First tested"
        else:
            print(
                f"\n\n\n{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} "
                f"Произошла ошибка в скрипте ER02/ER03!!!"
            )
            raise ValueError(f"Неизвестный type_save: {type_save}")

        file_path = os.path.join(folder_path, file_name)

        location_hack = input(
            f" {Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]"
            f"{Fore.RESET} Введите локацию тестирования :{Fore.LIGHTCYAN_EX} "
        )
        print(Fore.RESET)

        content = [
            f"Status: {status_text}",
            f"WPS PIN: {wps_pin}",
            f"WPA PSK(Password): {wpa_psk}",
            f"AP SSID(WiFi-Name): {essid}",
            f"AP BSSID(WiFi-MAC): {bssid}",
            f"Date/Time : {current_datetime_text}",
            f"Location: {location_hack}",
        ]

        with open(file_path, "w", encoding="utf-8") as file:
            for line in content:
                file.write(line + "\n")

        print(
            f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]"
            f"{Fore.RESET} Результат тестирования записан в файл "
            f"'{Fore.LIGHTCYAN_EX}{folder_path}/{file_name}{Fore.RESET}'..."
        )

    # Вывод значений с маскировкой
    masked_wps = mask_value(wps_pin, settings.get("Hide_Pin_AP"), pbc_suffix="*")
    print(
        f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} "
        f"WPS PIN: '{masked_wps}'"
    )

    masked_psk = mask_value(wpa_psk, settings.get("Hide_Password_AP"))
    print(
        f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} "
        f"WPA PSK(Пароль): '{masked_psk}'"
    )

    print(
        f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} "
        f"AP SSID(WiFi-Имя): '{Fore.LIGHTGREEN_EX}{essid}{Fore.RESET}'"
    )

    masked_bssid = mask_value(bssid, settings.get("Hide_MAC_AP"))
    print(
        f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} "
        f"AP BSSID(WiFi-MAC): '{masked_bssid}'"
    )

    # Работа с папкой логов
    folder_OSP = get_log_folder()
    ensure_log_folder(folder_OSP)

    # Проверка на ранее сохранённую сеть
    scan_file_osp = search_wifi_mac(folder_OSP, bssid)

    if scan_file_osp:
        print(
            f"\n{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]"
            f"{Fore.RESET} Найдена ранее проверенная сеть: "
            f"{Fore.LIGHTCYAN_EX}'{scan_file_osp}'{Fore.RESET}\n"
        )
        print(
            f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]"
            f"{Fore.RESET} Сохранить новый лог?"
        )
        print(
            f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]"
            f"{Fore.RESET} Доступные варианты: "
            f"{Fore.LIGHTCYAN_EX}y{Fore.RESET}, "
            f"{Fore.LIGHTCYAN_EX}n{Fore.RESET}, "
            f"{Fore.LIGHTCYAN_EX}yes{Fore.RESET}, "
            f"{Fore.LIGHTCYAN_EX}no{Fore.RESET}, "
            f"{Fore.LIGHTCYAN_EX}д{Fore.RESET}, "
            f"{Fore.LIGHTCYAN_EX}н{Fore.RESET}"
        )

        select_1 = input(
            f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]"
            f"{Fore.RESET} >> {Fore.LIGHTCYAN_EX}"
        ).strip()

        yes_variants = ["y", "yes", "Y", "Yes", "YES", "yES", "д", "да", "Д", "Да", "ДА", "дА"]
        no_variants = ["n", "no", "not", "N", "No", "Not", "н", "не", "нет", "Н", "Не", "Нет"]

        if select_1 in yes_variants:
            print(Fore.RESET)
            save_log(folder_OSP, wps_pin, wpa_psk, essid, bssid, "Update_new_wn")
        elif select_1 in no_variants:
            print(Fore.RESET)
            print(f"\n{Fore.LIGHTBLUE_EX}Выход...")
        else:
            print(Fore.RESET)

    elif scan_file_osp is None:
        save_log(folder_OSP, wps_pin, wpa_psk, essid, bssid, "Save_new_wn")

    else:
        print(
            f"\n\n\n{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} "
            f"Произошла ошибка в скрипте ER1!!!"
        )
        raise RuntimeError("Неожиданное состояние scan_file_osp")