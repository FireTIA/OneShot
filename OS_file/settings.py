import colorama
from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
from colorama import init
from OS_file.db import settings_dialoge
import json
from pathlib import Path
import time

just_fix_windows_console()
init(autoreset=True)

def settings__init_module():
    print(f"\n{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET} Получение настроек... \n")



Prefix = f"{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTBLUE_EX}Settings{Fore.LIGHTMAGENTA_EX}]{Fore.RESET}"

CONFIG_PATH = Path(__file__).with_name("settings.json")

DEFAULT_SETTINGS = {
    "OS_Target": "NetHunter",
    "Hide_Password_AP": "Half",
    "Hide_Pin_AP": "Half",
    "Hide_MAC_AP": "Half",
    "Change_MAC_WlanX_Startup": True,
    "Macchanger_Output_Mode": "pretty",
    "Hello_banner": "default"
}


# --- внутренняя «кэш-память» ---
_settings_cache: dict | None = None
_pending_changes: dict = {}
# -------------------------------


def _ensure_loaded() -> dict:
    """Лениво грузим настройки в память."""
    global _settings_cache

    if _settings_cache is None:
        if not CONFIG_PATH.exists():
            save_settings(DEFAULT_SETTINGS)
            _settings_cache = DEFAULT_SETTINGS.copy()
        else:
            with CONFIG_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = DEFAULT_SETTINGS.copy()
            cfg.update(data)
            _settings_cache = cfg
    return _settings_cache


def load_settings() -> dict:
    """Вернуть актуальные настройки (с учётом уже установленных set_setting, но ещё не сохранённых)."""
    cfg = _ensure_loaded().copy()
    cfg.update(_pending_changes)
    return cfg


def save_settings(cfg: dict):
    """Низкоуровневое: сразу пишет dict в файл (обычно дергать не нужно напрямую)."""
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)


# --- то, что ты хотел ---

def SETT_set_setting(key: str, value):
    """Добавить/изменить настройку в очереди (в файл пока не пишем)."""
    global _pending_changes
    _ensure_loaded()  # чтобы был кэш
    _pending_changes[key] = value
    print(f"{Prefix} Добавлено в очередь: {Fore.CYAN}{key}{Fore.RESET}={Fore.YELLOW}{value}{Fore.RESET}")


def SETT_apply_save_settings():
    """Применить очередь изменений и записать всё в файл."""
    global _settings_cache, _pending_changes
    cfg = _ensure_loaded()
    cfg.update(_pending_changes)
    save_settings(cfg)
    _settings_cache = cfg
    _pending_changes = {}
    print(f"{Prefix} Записал все ожидающие изменения в >{Fore.BLUE}settings.json{Fore.RESET}<")
# -------------------------
def SETT__load_param():
    return load_settings()

def SETT_menu():
    while True:
        settings = load_settings()  # всегда актуальные, с учётом pending

        print(f"""
|===============
|>> Настройки
| -1. Продолжить запуск
| 0. Применить и сохранить
| 1. Изменить >OS_Target< ({settings["OS_Target"]})
| 2. Изменить >Hide_Password_AP< ({settings["Hide_Password_AP"]})
| 3. Изменить >Hide_Pin_AP< ({settings["Hide_Pin_AP"]})
| 4. Изменить >Hide_MAC_AP< ({settings["Hide_MAC_AP"]})
| 5. Изменить >Change_MAC_WlanX_Startup< ({settings["Change_MAC_WlanX_Startup"]})
| 6. Изменить >Macchanger_Output_Mode< ({settings["Macchanger_Output_Mode"]})
| 7. Изменить >Hello_banner< ({settings["Hello_banner"]})
|===============
""")
    
        select = input("|> ")

        if select.lower() in ["-1", "go", "start", "exit"]:
            print("Выход из настроек...\n")
            time.sleep(1)
            break 
        elif select.lower() in ["0", "apply", "save", "sa"]:
            try:
                SETT_apply_save_settings()
                time.sleep(1)
            except Exception as e:
                print(f"Не удалось применить и сохранить  : {e}")

        elif select.lower() in ["1"]:
            while True:
                
                try:
                    print(f"\n\n{settings_dialoge.get('1_ID-Notice-1')}")
                except Exception as e:
                    print(f"Не удалось подгрузить диалог >1_ID-Notice--1< : {e}")
                    break
                
                print(f"\nВыберите что хотите применить:\n  0-e. Выход\n  1. Kali \n  2. NetHunter")

                select_setup = input("|> ")

                if select_setup.lower() in ["1", "kali", "kali linux", "кали", "ка"]:
                    SETT_set_setting("OS_Target","Kali")
                    time.sleep(0.75)
                    break
                elif select_setup.lower() in ["2", "nethunter", "kali nethunter", "nh", "net", "нх", "нш"]:
                    SETT_set_setting("OS_Target","NetHunter")
                    time.sleep(0.75)
                    break
                elif select_setup.lower() in ["0", "e", "exit", "b", "back", "в", "выход", "выйти"]:
                    print(f"Выходим из настройки >OS_Target<")
                    time.sleep(0.5)
                    break
                else:
                    print("!Повторите попытку!")
                    time.sleep(1)
            
        else:
            print("Не нашел ID действия \n")
            time.sleep(1.5)
