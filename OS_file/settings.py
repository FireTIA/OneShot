import json
import time
from pathlib import Path

import colorama
from colorama import Fore, init

from OS_file.db import settings_dialoge

init(autoreset=True)

Prefix = f"{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTBLUE_EX}Settings{Fore.LIGHTMAGENTA_EX}]{Fore.RESET}"
FS_prefix = f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET}"

CONFIG_PATH = Path(__file__).with_name("settings.json")

DEFAULT_SETTINGS = {
    "OS_Target": "NetHunter",
    "Hide_Password_AP": "Half",
    "Hide_Pin_AP": "Half",
    "Hide_MAC_AP": "Half",
    "Change_MAC_WlanX_Startup": True,
    "Macchanger_Output_Mode": "pretty",
    "Hello_banner": "default",
    "Check_Corp_AP_Action": None,
    "Check_Corp_AP_lTX_Value": None,
    "Check_Corp_AP_Recheck_After_lTX": None,
}

_settings_cache: dict | None = None
_pending_changes: dict = {}


def settings__init_module():
    print(f"\n{FS_prefix} Получение настроек... \n")


def _normalize_hide_mode(value):
    if value is None:
        return "False"
    value = str(value).strip().lower()
    if value in ("true", "hide", "hidden", "full", "1", "да", "д"):
        return "True"
    if value in ("half", "halfhid", "partial", "2", "частично"):
        return "Half"
    return "False"


def _normalize_mac_startup(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    value = str(value).strip()
    low = value.lower()
    if low in ("false", "off", "none", "null", "0", "no", "нет", "н"):
        return False
    if low in ("true", "on", "1", "yes", "да", "д"):
        return True
    if low in ("true-r", "r", "random", "full-random", "full_random"):
        return "True-r"
    return value


def _normalize_macchanger_output(value):
    if value is None:
        return "pretty"
    value = str(value).strip().lower()
    if value in ("raw", "r", "сырой"):
        return "raw"
    return "pretty"


def _normalize_banner(value):
    if value is None:
        return "default"
    value = str(value).strip().lower()
    if value in ("classic", "old", "классик"):
        return "classic"
    if value in ("compact", "minimal", "mini", "short"):
        return "compact"
    if value in ("none", "false", "off", "hide", "hidden"):
        return "none"
    return "default"


def _normalize_corp_action(value):
    if value is None:
        return None
    value = str(value).strip().lower()
    if value in ("", "none", "null", "ask", "manual", "0"):
        return None
    if value in ("yes", "y", "да", "д", "continue", "go"):
        return "yes"
    if value in ("no", "n", "нет", "н", "stop", "exit"):
        return "no"
    if value in ("ltx", "tx", "l", "lt", "lx"):
        return "ltx"
    return None


def _normalize_ltx_value(value):
    if value is None:
        return None
    value = str(value).strip().lower()
    if value in ("", "none", "null", "ask", "manual", "0"):
        return None
    try:
        tx_value = int(value)
    except ValueError:
        return None
    if tx_value < 1:
        return 1
    if tx_value > 30:
        return 30
    return tx_value


def _normalize_optional_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    value = str(value).strip().lower()
    if value in ("", "none", "null", "ask", "manual"):
        return None
    if value in ("true", "yes", "y", "1", "да", "д"):
        return True
    if value in ("false", "no", "n", "0", "нет", "н"):
        return False
    return None


def normalize_settings(cfg: dict) -> dict:
    normalized = DEFAULT_SETTINGS.copy()
    normalized.update(cfg or {})

    normalized["OS_Target"] = str(normalized.get("OS_Target") or "").strip() or DEFAULT_SETTINGS["OS_Target"]
    normalized["Hide_Password_AP"] = _normalize_hide_mode(normalized.get("Hide_Password_AP"))
    normalized["Hide_Pin_AP"] = _normalize_hide_mode(normalized.get("Hide_Pin_AP"))
    normalized["Hide_MAC_AP"] = _normalize_hide_mode(normalized.get("Hide_MAC_AP"))
    normalized["Change_MAC_WlanX_Startup"] = _normalize_mac_startup(normalized.get("Change_MAC_WlanX_Startup"))
    normalized["Macchanger_Output_Mode"] = _normalize_macchanger_output(normalized.get("Macchanger_Output_Mode"))
    normalized["Hello_banner"] = _normalize_banner(normalized.get("Hello_banner"))
    normalized["Check_Corp_AP_Action"] = _normalize_corp_action(normalized.get("Check_Corp_AP_Action"))
    normalized["Check_Corp_AP_lTX_Value"] = _normalize_ltx_value(normalized.get("Check_Corp_AP_lTX_Value"))
    normalized["Check_Corp_AP_Recheck_After_lTX"] = _normalize_optional_bool(
        normalized.get("Check_Corp_AP_Recheck_After_lTX")
    )

    return normalized


def _ensure_loaded() -> dict:
    global _settings_cache

    if _settings_cache is not None:
        return _settings_cache

    if not CONFIG_PATH.exists():
        _settings_cache = DEFAULT_SETTINGS.copy()
        save_settings(_settings_cache)
        return _settings_cache

    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"{Prefix} Не удалось прочитать settings.json: {Fore.YELLOW}{e}{Fore.RESET}")
        print(f"{Prefix} Использую настройки по умолчанию.")
        data = DEFAULT_SETTINGS.copy()

    _settings_cache = normalize_settings(data)
    return _settings_cache


def load_settings() -> dict:
    cfg = _ensure_loaded().copy()
    cfg.update(_pending_changes)
    return normalize_settings(cfg)


def save_settings(cfg: dict):
    cfg = normalize_settings(cfg)
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)
        f.write("\n")


def SETT_set_setting(key: str, value):
    global _pending_changes

    if key not in DEFAULT_SETTINGS:
        print(f"{Prefix} Неизвестная настройка: {Fore.YELLOW}{key}{Fore.RESET}")
        return

    normalized_value = normalize_settings({**load_settings(), key: value})[key]
    _pending_changes[key] = normalized_value
    print(f"{Prefix} Добавлено в очередь: {Fore.CYAN}{key}{Fore.RESET}={Fore.YELLOW}{normalized_value}{Fore.RESET}")


def SETT_apply_save_settings():
    global _settings_cache, _pending_changes

    cfg = _ensure_loaded().copy()
    cfg.update(_pending_changes)
    cfg = normalize_settings(cfg)
    save_settings(cfg)
    _settings_cache = cfg
    _pending_changes = {}
    print(f"{Prefix} Записал все ожидающие изменения в >{Fore.BLUE}settings.json{Fore.RESET}<")


def SETT__load_param():
    return load_settings()


def _print_notice(notice_id: str):
    text = settings_dialoge.get(notice_id)
    if text:
        print(f"\n\n{text}")
    else:
        print(f"\n\n{Prefix} Нет текста подсказки для {notice_id}")


def _pause(seconds: float = 0.5):
    time.sleep(seconds)


def _is_back(value: str) -> bool:
    return value.lower() in ("0", "e", "exit", "b", "back", "в", "выход", "выйти", "назад")


def _select_hide_mode(setting_key: str, notice_id: str):
    while True:
        _print_notice(notice_id)
        print("\nВыберите что хотите применить:")
        print("  0-e. Выход")
        print("  1. False - показывать полностью")
        print("  2. Half  - скрывать частично")
        print("  3. True  - скрывать полностью")

        select_setup = input("|> ").strip()

        if select_setup.lower() in ("1", "false", "show", "показать"):
            SETT_set_setting(setting_key, "False")
            _pause(0.75)
            return
        if select_setup.lower() in ("2", "half", "partial", "частично"):
            SETT_set_setting(setting_key, "Half")
            _pause(0.75)
            return
        if select_setup.lower() in ("3", "true", "hide", "hidden", "скрыть"):
            SETT_set_setting(setting_key, "True")
            _pause(0.75)
            return
        if _is_back(select_setup):
            print(f"Выходим из настройки >{setting_key}<")
            _pause()
            return

        print("!Повторите попытку!")
        _pause(1)


def _select_os_target():
    while True:
        _print_notice("1_ID-Notice-1")
        print("\nВыберите что хотите применить:")
        print("  0-e. Выход")
        print("  1. Kali")
        print("  2. NetHunter")
        print("  3. Custom path")

        select_setup = input("|> ").strip()
        low = select_setup.lower()

        if low in ("1", "kali", "kali linux", "кали", "ка"):
            SETT_set_setting("OS_Target", "Kali")
            _pause(0.75)
            return
        if low in ("2", "nethunter", "kali nethunter", "nh", "net", "нх", "нш"):
            SETT_set_setting("OS_Target", "NetHunter")
            _pause(0.75)
            return
        if low in ("3", "custom", "path", "путь"):
            setup_custom_path = input("Custom path:\n|> ").strip()
            if setup_custom_path:
                SETT_set_setting("OS_Target", setup_custom_path)
            else:
                print("Пустой путь не применён.")
            _pause(0.75)
            return
        if _is_back(select_setup):
            print("Выходим из настройки >OS_Target<")
            _pause()
            return

        print("!Повторите попытку!")
        _pause(1)


def _select_change_mac_startup():
    while True:
        _print_notice("1_ID-Notice-5")
        print("\nВыберите что хотите применить:")
        print("  0-e. Выход")
        print("  1. False  - не менять MAC")
        print("  2. True   - macchanger -a, случайный MAC с сохранением OUI")
        print("  3. True-r - macchanger -r, полностью случайный MAC")
        print("  4. Custom MAC")

        select_setup = input("|> ").strip()
        low = select_setup.lower()

        if low in ("1", "false", "off", "no", "нет"):
            SETT_set_setting("Change_MAC_WlanX_Startup", False)
            _pause(0.75)
            return
        if low in ("2", "true", "on", "yes", "да"):
            SETT_set_setting("Change_MAC_WlanX_Startup", True)
            _pause(0.75)
            return
        if low in ("3", "true-r", "r", "random", "full-random"):
            SETT_set_setting("Change_MAC_WlanX_Startup", "True-r")
            _pause(0.75)
            return
        if low in ("4", "custom", "mac"):
            custom_mac = input("Custom MAC, пример 00:11:22:33:44:55:\n|> ").strip()
            if custom_mac:
                SETT_set_setting("Change_MAC_WlanX_Startup", custom_mac)
            else:
                print("Пустой MAC не применён.")
            _pause(0.75)
            return
        if _is_back(select_setup):
            print("Выходим из настройки >Change_MAC_WlanX_Startup<")
            _pause()
            return

        print("!Повторите попытку!")
        _pause(1)


def _select_macchanger_output_mode():
    while True:
        _print_notice("1_ID-Notice-6")
        print("\nВыберите что хотите применить:")
        print("  0-e. Выход")
        print("  1. raw")
        print("  2. pretty")

        select_setup = input("|> ").strip()
        low = select_setup.lower()

        if low in ("1", "raw", "r"):
            SETT_set_setting("Macchanger_Output_Mode", "raw")
            _pause(0.75)
            return
        if low in ("2", "pretty", "p"):
            SETT_set_setting("Macchanger_Output_Mode", "pretty")
            _pause(0.75)
            return
        if _is_back(select_setup):
            print("Выходим из настройки >Macchanger_Output_Mode<")
            _pause()
            return

        print("!Повторите попытку!")
        _pause(1)


def _select_hello_banner():
    while True:
        _print_notice("1_ID-Notice-7")
        print("\nВыберите что хотите применить:")
        print("  0-e. Выход")
        print("  1. default")
        print("  2. classic")
        print("  3. compact")
        print("  4. none")

        select_setup = input("|> ").strip()
        low = select_setup.lower()

        if low in ("1", "default", "full"):
            SETT_set_setting("Hello_banner", "default")
            _pause(0.75)
            return
        if low in ("2", "classic", "old"):
            SETT_set_setting("Hello_banner", "classic")
            _pause(0.75)
            return
        if low in ("3", "compact", "minimal", "mini"):
            SETT_set_setting("Hello_banner", "compact")
            _pause(0.75)
            return
        if low in ("4", "none", "false", "off"):
            SETT_set_setting("Hello_banner", "none")
            _pause(0.75)
            return
        if _is_back(select_setup):
            print("Выходим из настройки >Hello_banner<")
            _pause()
            return

        print("!Повторите попытку!")
        _pause(1)


def _select_corp_action():
    while True:
        _print_notice("1_ID-Notice-8")
        print("\nВыберите что хотите применить:")
        print("  0-e. Выход")
        print("  1. Ask/None - спрашивать каждый раз")
        print("  2. yes      - продолжать без изменений")
        print("  3. ltx      - пытаться занизить TX Power")
        print("  4. no       - завершать скрипт")

        select_setup = input("|> ").strip()
        low = select_setup.lower()

        if low in ("1", "ask", "none", "null", "manual"):
            SETT_set_setting("Check_Corp_AP_Action", None)
            _pause(0.75)
            return
        if low in ("2", "yes", "y", "да", "д"):
            SETT_set_setting("Check_Corp_AP_Action", "yes")
            _pause(0.75)
            return
        if low in ("3", "ltx", "tx", "l"):
            SETT_set_setting("Check_Corp_AP_Action", "ltx")
            _pause(0.75)
            return
        if low in ("4", "no", "n", "нет", "н"):
            SETT_set_setting("Check_Corp_AP_Action", "no")
            _pause(0.75)
            return
        if _is_back(select_setup):
            print("Выходим из настройки >Check_Corp_AP_Action<")
            _pause()
            return

        print("!Повторите попытку!")
        _pause(1)


def _select_ltx_value():
    while True:
        _print_notice("1_ID-Notice-9")
        print("\nВыберите что хотите применить:")
        print("  0-e. Выход")
        print("  1. Ask/None - спрашивать значение вручную")
        print("  2. Custom dBm, диапазон 1-30")

        select_setup = input("|> ").strip()
        low = select_setup.lower()

        if low in ("1", "ask", "none", "null", "manual"):
            SETT_set_setting("Check_Corp_AP_lTX_Value", None)
            _pause(0.75)
            return
        if low in ("2", "custom", "dbm", "tx"):
            value_raw = input("TX Power dBm, пример 12:\n|> ").strip()
            value = _normalize_ltx_value(value_raw)
            if value is None:
                print("Некорректное значение. Нужное целое число от 1 до 30.")
            else:
                SETT_set_setting("Check_Corp_AP_lTX_Value", value)
                _pause(0.75)
                return
        elif _is_back(select_setup):
            print("Выходим из настройки >Check_Corp_AP_lTX_Value<")
            _pause()
            return
        else:
            print("!Повторите попытку!")
            _pause(1)


def _select_recheck_after_ltx():
    while True:
        _print_notice("1_ID-Notice-10")
        print("\nВыберите что хотите применить:")
        print("  0-e. Выход")
        print("  1. Ask/None - спрашивать после lTX")
        print("  2. True     - всегда перепроверять")
        print("  3. False    - не перепроверять")

        select_setup = input("|> ").strip()
        low = select_setup.lower()

        if low in ("1", "ask", "none", "null", "manual"):
            SETT_set_setting("Check_Corp_AP_Recheck_After_lTX", None)
            _pause(0.75)
            return
        if low in ("2", "true", "yes", "y", "да", "д"):
            SETT_set_setting("Check_Corp_AP_Recheck_After_lTX", True)
            _pause(0.75)
            return
        if low in ("3", "false", "no", "n", "нет", "н"):
            SETT_set_setting("Check_Corp_AP_Recheck_After_lTX", False)
            _pause(0.75)
            return
        if _is_back(select_setup):
            print("Выходим из настройки >Check_Corp_AP_Recheck_After_lTX<")
            _pause()
            return

        print("!Повторите попытку!")
        _pause(1)


def _print_settings_menu(settings: dict):
    pending_note = ""
    if _pending_changes:
        pending_note = f"\n| Ожидают сохранения: {Fore.YELLOW}{', '.join(_pending_changes.keys())}{Fore.RESET}"

    print(f"""
|===============
|>> Настройки{pending_note}
| -1. Продолжить запуск
| 0. Применить и сохранить
| 1. Изменить >OS_Target< ({settings["OS_Target"]})
| 2. Изменить >Hide_Password_AP< ({settings["Hide_Password_AP"]})
| 3. Изменить >Hide_Pin_AP< ({settings["Hide_Pin_AP"]})
| 4. Изменить >Hide_MAC_AP< ({settings["Hide_MAC_AP"]})
| 5. Изменить >Change_MAC_WlanX_Startup< ({settings["Change_MAC_WlanX_Startup"]})
| 6. Изменить >Macchanger_Output_Mode< ({settings["Macchanger_Output_Mode"]})
| 7. Изменить >Hello_banner< ({settings["Hello_banner"]})
| 8. Изменить >Check_Corp_AP_Action< ({settings["Check_Corp_AP_Action"]})
| 9. Изменить >Check_Corp_AP_lTX_Value< ({settings["Check_Corp_AP_lTX_Value"]})
| 10. Изменить >Check_Corp_AP_Recheck_After_lTX< ({settings["Check_Corp_AP_Recheck_After_lTX"]})
|===============
""")


def SETT_menu():
    while True:
        settings = load_settings()
        _print_settings_menu(settings)

        select = input("|> ").strip().lower()

        if select in ("-1", "go", "start", "exit", "run", "продолжить"):
            if _pending_changes:
                print(f"{Prefix} Есть несохранённые изменения. Нажмите 0, если их нужно записать.")
                _pause(1)
            print("Выход из настроек...\n")
            _pause(1)
            break
        if select in ("0", "apply", "save", "sa", "сохранить"):
            try:
                SETT_apply_save_settings()
                _pause(1)
            except Exception as e:
                print(f"Не удалось применить и сохранить: {e}")
            continue
        if select == "1":
            _select_os_target()
            continue
        if select == "2":
            _select_hide_mode("Hide_Password_AP", "1_ID-Notice-2")
            continue
        if select == "3":
            _select_hide_mode("Hide_Pin_AP", "1_ID-Notice-3")
            continue
        if select == "4":
            _select_hide_mode("Hide_MAC_AP", "1_ID-Notice-4")
            continue
        if select == "5":
            _select_change_mac_startup()
            continue
        if select == "6":
            _select_macchanger_output_mode()
            continue
        if select == "7":
            _select_hello_banner()
            continue
        if select == "8":
            _select_corp_action()
            continue
        if select == "9":
            _select_ltx_value()
            continue
        if select == "10":
            _select_recheck_after_ltx()
            continue

        print("Не нашел ID действия \n")
        _pause(1.5)
