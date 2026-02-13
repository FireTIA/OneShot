import colorama
from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
from colorama import init
import subprocess
import shlex
import sys
import time
from pathlib import Path
from OS_file.db import USB_MAP, PCI_MAP, Ubiquiti_OUI, MikroTik_OUI, Cisco_OUI
from OS_file.settings import SETT__load_param
import re

just_fix_windows_console()
init(autoreset=True)

Module_prefix = f"{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTBLUE_EX}Wlan{Fore.LIGHTGREEN_EX}X{Fore.LIGHTMAGENTA_EX}]{Fore.RESET}"

Module_write_info = True
Module_write_process = True
Module_write_out_cmd = True

def print_info(msg):
    if Module_write_info:
        print(msg)

def print_process(msg):
    if Module_write_process:
        print(msg)

def print_out_cmd(msg):
    if Module_write_out_cmd:
        print(msg)


def WlanX__init_module():
    print_info(f"\n{Module_prefix} - Модуль загружен! \n")


#
# >Subprocess
#

def run(cmd: str) -> str:
    """Выполняет команду, возвращает stdout, печатает stderr при ошибке."""
    try:
        result = subprocess.run(
            shlex.split(cmd), check=True, capture_output=True, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr)
        sys.exit(e.returncode)


#
# >> Macchanger Парсинг значений
#

def parse_macchanger_output(out: str) -> dict:
    """
    Парсит вывод macchanger и возвращает словарь:
    {
        "current_mac": "xx:xx:...",
        "current_name": "Vendor",
        "permanent_mac": "...",
        "permanent_name": "...",
        "new_mac": "...",
        "new_name": "..."
    }
    Если что-то не нашлось — значения будут None.
    """
    info = {
        "current_mac": None,
        "current_name": None,
        "permanent_mac": None,
        "permanent_name": None,
        "new_mac": None,
        "new_name": None,
    }

    # шаблон типа: Current MAC:  68:6c:e3... (Wi3 Inc.)
    pattern = re.compile(
        r'^(Current|Permanent|New)\s+MAC:\s+([0-9a-fA-F:]{17})(?:\s+\((.+)\))?'
    )

    for line in out.splitlines():
        line = line.strip()
        m = pattern.match(line)
        if not m:
            continue

        kind, mac, name = m.groups()
        name = name or ""

        if kind == "Current":
            info["current_mac"] = mac
            info["current_name"] = name
        elif kind == "Permanent":
            info["permanent_mac"] = mac
            info["permanent_name"] = name
        elif kind == "New":
            info["new_mac"] = mac
            info["new_name"] = name

    return info

#
# >> Смена MAC-адреса
#

def WlanX__Mac_Change(iface, type_change):
    if type_change == False:
        print(f"{Module_prefix} - Смена MAC выключена")
        return

    print_process(f"{Module_prefix} - Изменяем MAC адрес на {Fore.LIGHTBLUE_EX}{iface}{Fore.RESET}")

    print_info(f"{Module_prefix} > [IP-Link] - Выключаем интерфейс {Fore.LIGHTBLUE_EX}{iface}{Fore.RESET}")
    run(f"ip link set {iface} down")

    if type_change is True:
        out = run(f"macchanger -a {iface}")
    elif type_change == "True-r":
        out = run(f"macchanger -r {iface}")
    else:
        out = run(f"macchanger --mac={type_change} {iface}")

    # тут решаем, что показывать
    mode = SETT__load_param().get("Macchanger_Output_Mode", "raw")

    if mode == "raw":
        # как было
        print_out_cmd(f"\n{Module_prefix} > [Macchanger-OUT]:\n{out}\n")
    else:
        info = parse_macchanger_output(out)
        # если внезапно не распарсилось — покажем сырое, чтобы не остаться без логов
        if not info["current_mac"] and not info["new_mac"]:
            print_out_cmd(f"\n{Module_prefix} > [Macchanger-OUT]:\n{out}\n")
        else:
            print_info(f"{Module_prefix} > [Macchanger] Current  : {Fore.CYAN}{info['current_mac'] or 'N/A'}{Fore.RESET} {f'({info['current_name']})' if info['current_name'] else ''}")
            print_info(f"{Module_prefix} > [Macchanger] Permanent: {Fore.CYAN}{info['permanent_mac'] or 'N/A'}{Fore.RESET} {f'({info['permanent_name']})' if info['permanent_name'] else ''}")
            print_info(f"{Module_prefix} > [Macchanger] New      : {Fore.LIGHTGREEN_EX}{info['new_mac'] or 'N/A'}{Fore.RESET} {f'({info['new_name']})' if info['new_name'] else ''}")

    print_info(f"{Module_prefix} > [IP-Link] - Включаем интерфейс {Fore.LIGHTBLUE_EX}{iface}{Fore.RESET}")
    
    run(f"ip link set {iface} up")

    print_process(f"{Module_prefix} - Закончил смену MAC адреса на {Fore.LIGHTBLUE_EX}{iface}{Fore.RESET}")



#
# >> Получение используемого драйвера на wlanX
#


def WlanX__get_wifi_driver(iface: str) -> str | None:
    """
    Возвращает имя загруженного драйвера для беспроводного интерфейса.
    Если не удаётся определить, возвращает None.
    """
    # ── способ 1. ethtool -i ───────────────────────────────────────
    try:
        out = subprocess.check_output(
            ['ethtool', '-i', iface],
            text=True, stderr=subprocess.DEVNULL
        )
        # ищем строку вида: 'driver: ath9k_htc'
        m = re.search(r'^driver:\s*(\S+)', out, re.M)
        if m:
            return m.group(1)
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    # ── способ 2. sysfs (/sys/class/net/<iface>/device/driver) ────
    drv_link = Path(f'/sys/class/net/{iface}/device/driver')
    if drv_link.is_symlink():
        # …/driver/rtl8812au → берём последнее имя в пути
        return drv_link.resolve().name

    # если оба метода не сработали
    return None


#
# >> Получение чипсета на wlanX, по методам Airmon`а
#


def WlanX__detect_chipset_airmon_style(iface: str) -> str:
    """
    Возвращает строку с названием чипсета/драйвера, ходя по /sys, как делает airmon-ng.
    Всегда отдаёт непустую строку: либо «человеческое» имя, либо <bus VID:PID>,
    либо 'Unknown'.
    """
    try:
        dev = Path(f'/sys/class/net/{iface}/device').resolve(strict=True)
    except FileNotFoundError:
        return 'Unknown'

    # Поднимаемся вверх, пока не наткнёмся на нужные файлы или корень sysfs
    cur = dev
    while cur != cur.parent:
        id_vendor  = cur / 'idVendor'
        id_product = cur / 'idProduct'
        if id_vendor.exists() and id_product.exists():          # USB-устройство
            vid = id_vendor.read_text().strip().lower()
            pid = id_product.read_text().strip().lower()
            return USB_MAP.get((vid, pid), f'USB {vid}:{pid}')

        vendor  = cur / 'vendor'
        device  = cur / 'device'
        if vendor.exists() and device.exists():                 # PCI/PCI-e
            vid = vendor.read_text().strip()[2:].lower()        # '0x168c' → '168c'
            pid = device.read_text().strip()[2:].lower()
            return PCI_MAP.get((vid, pid), f'PCI {vid}:{pid}')

        cur = cur.parent                                        # шаг вверх

    return 'Unknown'



#
# >> Получение информации с адаптера
#

def WlanX__Adapter_info_get(type_info: str, iface: str):
    print_process(f"{Module_prefix} - Получение информации с {Fore.LIGHTBLUE_EX}{iface}{Fore.RESET}")

    if type_info == "tx-power-db":
        out = run(f"iwconfig {iface}")
        # ищем строку с Tx-Power
        for line in out.splitlines():
            if "Tx-Power=" in line:
                value = line.split("Tx-Power=")[1].split()[0]
                return value  # типа "20", "23" и т.п.

    elif type_info == "bitrate":
        out = run(f"iw dev {iface} link")
        for line in out.splitlines():
            if "tx bitrate:" in line:
                return line.split("tx bitrate:")[1].strip()

    elif type_info == "mode":
        out = run(f"iw dev {iface} info")
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("type "):
                return line.split()[1]  # managed / monitor / ap …

    elif type_info == "channel":
        out = run(f"iw dev {iface} link")
        for line in out.splitlines():
            if "freq" in line:
                # пример строки: "freq: 2437"
                parts = line.split()
                try:
                    freq = parts[1]
                    return freq
                except IndexError:
                    return None

    elif type_info == "driver":
        out = run(f"ethtool -i {iface}")
        for line in out.splitlines():
            if line.strip().startswith("driver:"):
                return line.split("driver:")[1].strip()

    elif type_info == "all":
        info = {}
        info["mode"] = WlanX__Adapter_info_get("mode", iface)
        info["tx_power_db"] = WlanX__Adapter_info_get("tx-power-db", iface)
        info["bitrate"] = WlanX__Adapter_info_get("bitrate", iface)
        info["channel_freq"] = WlanX__Adapter_info_get("channel", iface)
        info["driver"] = WlanX__Adapter_info_get("driver", iface)
        return info

    else:
        print_info(f"{Module_prefix} - Неизвестный тип запроса информации: {type_info}")
        return None



#
# >> Поиск в зоне действия wifi адаптера на наличие Ubiquit и подобного.
#

UBIQUITI_OUI_SET = {x.upper() for x in Ubiquiti_OUI}
MIKROTIK_OUI_SET = {x.upper() for x in MikroTik_OUI}
CISCO_OUI_SET    = {x.upper() for x in Cisco_OUI}

def _normalize_mac(mac: str) -> str:
    """Нормализуем MAC к виду AA:BB:CC:DD:EE:FF"""
    mac = mac.strip().upper().replace("-", ":")
    # на всякий случай: иногда встречается формат aabb.ccdd.eeff
    if "." in mac and ":" not in mac:
        mac = mac.replace(".", "")
        mac = ":".join(mac[i:i+2] for i in range(0, 12, 2))
    return mac


def _mac_to_oui(mac: str) -> str:
    """Берём первые 3 октета MAC как OUI."""
    mac = _normalize_mac(mac)
    parts = mac.split(":")
    if len(parts) < 3:
        return mac
    return ":".join(parts[:3])


def _detect_corp_vendor_by_mac(mac: str) -> str | None:
    """
    Определяем вендора по OUI.
    Возвращает 'Ubiquiti' / 'MikroTik' / 'Cisco' или None.
    """
    oui = _mac_to_oui(mac)
    if oui in UBIQUITI_OUI_SET:
        return "Ubiquiti"
    if oui in MIKROTIK_OUI_SET:
        return "MikroTik"
    if oui in CISCO_OUI_SET:
        return "Cisco"
    return None

def WlanX__kill_conflicts(iface: str):
    """
    Завершаем процессы, которые держат Wi-Fi-интерфейс:
    wpa_supplicant, dhclient, hostapd, NetworkManager.
    """
    conflict_names = ('wpa_supplicant', 'dhclient', 'hostapd')
    for name in conflict_names:
        try:
            subprocess.run(
                ['pkill', '-9', '-f', name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

    # Пытаемся остановить NetworkManager (если есть systemd и NM)
    try:
        subprocess.run(
            ['systemctl', 'stop', 'NetworkManager'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

    # На всякий случай поднимаем интерфейс
    try:
        subprocess.run(
            ['ip', 'link', 'set', iface, 'up'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

    print_process(f"{Module_prefix} > [Check-CorpAP]: Завершены процессы, удерживающие Wi-Fi. Интерфейс {Fore.LIGHTBLUE_EX}{iface}{Fore.RESET} поднят.")



#
# >> Поиск в зоне действия wifi адаптера на наличие Ubiquit и подобного.
#

def WlanX__Check_Corp_AP(count_retry_check: int, timeout_check: int, iface: str):
    """
    Сканирует эфир и проверяет, есть ли поблизости точки с OUI из баз
    Ubiquiti / MikroTik / Cisco.

    count_retry_check – сколько раз повторять скан, если ничего не нашли (>=1)
    timeout_check     – пауза между попытками в секундах

    Если найдены такие AP, выводит список и спрашивает, продолжать ли работу.
    При ответе "нет" — завершает скрипт через sys.exit().
    """
    if not count_retry_check or count_retry_check < 1:
        count_retry_check = 1
    if not timeout_check or timeout_check < 0:
        timeout_check = 0

    print_process(
        f"{Module_prefix} > [Check-CorpAP]: Проверка окружения на наличие корпоративных AP ({iface}) "
        f"\n{Fore.LIGHTMAGENTA_EX}[{Fore.GREEN}{iface}{Fore.LIGHTMAGENTA_EX}]{Fore.RESET} - Текущая мощность TX Power: "
        f"{Fore.LIGHTCYAN_EX}{WlanX__Adapter_info_get('tx-power-db', iface)}{Fore.RESET}"
    )

    found_aps: dict[str, dict] = {}  # bssid -> {"vendor": ..., "ssid": ..., "signal_dbm": ..., "signal_percent": ...}

    attempt = 1
    while attempt <= count_retry_check:
        print_process(
            f"{Module_prefix} > [Check-CorpAP]: Сканирование эфира "
            f"(попытка {Fore.LIGHTCYAN_EX}{attempt}{Fore.RESET}/{Fore.CYAN}{count_retry_check}{Fore.RESET})"
        )

        # ВАЖНО: здесь НЕ используем run(), чтобы поймать -16 и обработать
        try:
            proc = subprocess.run(
                ["iw", "dev", iface, "scan"],
                capture_output=True,
                text=True
            )
        except Exception as e:
            print_info(f"{Module_prefix} > [Check-CorpAP]: Не удалось выполнить сканирование через iw dev {iface} scan: {e}")
            return

        if proc.returncode != 0:
            err = (proc.stderr or "").strip()

            # Ловим именно "Device or resource busy (-16)"
            if "Device or resource busy" in err or "(-16)" in err:
                print_info(f"{Module_prefix} > [Check-CorpAP]: Устройство({Fore.BLUE}{iface}{Fore.RESET}) занято (Device or resource busy -16).")

                while True:
                    ans_busy = input(
                        f"\n{Module_prefix} > Обнаружены процессы, держащие Wi-Fi адаптер.\n"
                        f"Попробовать завершить процессы, связанные с Wi-Fi "
                        f"(wpa_supplicant, dhclient, hostapd, NetworkManager)? [y/N]: "
                    ).strip().lower()
                    print(" ")

                    if ans_busy in ("y", "yes", "д", "да"):
                        WlanX__kill_conflicts(iface)
                        print_process(f"{Module_prefix} > [Check-CorpAP]: Повторяем попытку сканирования после убийства процессов...\n")
                        # НЕ увеличиваем attempt — повторяем ту же попытку
                        break
                    elif ans_busy in ("n", "no", "н", "нет", ""):
                        print_info(f"{Module_prefix} > [Check-CorpAP]: Пользователь отказался завершать процессы. Пропускаем проверку корп. AP.\n")
                        return
                    else:
                        print("!Повторите ввод (y/yes/д/да или n/no/н/нет)!")

                # Возвращаемся в начало цикла while с тем же номером попытки
                continue
            else:
                print_info(f"{Module_prefix} > [Check-CorpAP]: Ошибка при выполнении iw dev {iface} scan:\n{err}")
                return

        out = proc.stdout

        last_bssid = None

        for line in out.splitlines():
            line = line.strip()

            # Строка BSS aa:bb:cc:dd:ee:ff(on wlan0)
            if line.startswith("BSS "):
                parts = line.split()
                if len(parts) >= 2:
                    bssid_raw = parts[1]
                    # может быть вида aa:bb:cc:dd:ee:ff(on → режем по "("
                    bssid = bssid_raw.split("(")[0]
                    vendor = _detect_corp_vendor_by_mac(bssid)
                    if vendor:
                        bssid_norm = _normalize_mac(bssid)
                        found_aps.setdefault(
                            bssid_norm,
                            {"vendor": vendor, "ssid": None, "signal_dbm": None, "signal_percent": None}
                        )
                        last_bssid = bssid_norm
                    else:
                        last_bssid = None

            # Строка SSID: MyWifi
            elif line.startswith("SSID:") and last_bssid and last_bssid in found_aps:
                ssid = line[5:].strip()
                found_aps[last_bssid]["ssid"] = ssid or "<hidden>"

            # Строка signal: -45.00 dBm
            elif line.startswith("signal:") and last_bssid and last_bssid in found_aps:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        sig_dbm = float(parts[1])
                    except ValueError:
                        sig_dbm = None

                    if sig_dbm is not None:
                        # Примерная конверсия dBm -> %
                        # -100 dBm ~ 0%, -50 dBm ~ 100%
                        pct = int(2 * (sig_dbm + 100))
                        if pct < 0:
                            pct = 0
                        if pct > 100:
                            pct = 100

                        found_aps[last_bssid]["signal_dbm"] = sig_dbm
                        found_aps[last_bssid]["signal_percent"] = pct

        # Делаем полный цикл попыток, даже если уже что-то нашли

        # Пауза только если пока ничего не нашли
        if not found_aps and attempt < count_retry_check and timeout_check > 0:
            print_process(
                f"{Module_prefix} > [Check-CorpAP]: Ничего не найдено, "
                f"жду {timeout_check} секунд и повторяю..."
            )
            time.sleep(timeout_check)

        attempt += 1

    if not found_aps:
        print_info(f"{Module_prefix} > [Check-CorpAP]: Корпоративные AP по спискам OUI не обнаружены. Продолжаем.\n")
        return

    # Красиво выводим найденные точки
    print_info(f"\n{Module_prefix} > [Check-CorpAP]: В радиусе действия обнаружены потенциально корпоративные точки доступа:\n")

    for bssid, info in found_aps.items():
        vendor = info["vendor"]
        ssid = info.get("ssid") or "<hidden>"
        sig_dbm = info.get("signal_dbm")
        sig_pct = info.get("signal_percent")

        if sig_dbm is not None and sig_pct is not None:
            signal_str = f"{sig_dbm:.1f} dBm (~{sig_pct}%)"
        else:
            signal_str = "N/A"

        print_info(
            f"  - BSSID: {Fore.CYAN}{bssid}{Fore.RESET} | "
            f"SSID: {Fore.YELLOW}{ssid}{Fore.RESET} | "
            f"Vendor (по OUI): {Fore.LIGHTGREEN_EX}{vendor}{Fore.RESET} | "
            f"Signal: {Fore.LIGHTCYAN_EX}{signal_str}{Fore.RESET}"
        )

    print()  # пустая строка

    # Спрашиваем, что делать дальше
    while True:
        ans = input(
            f"\n{Module_prefix} > [Check-CorpAP]: Обнаружены возможные корпоративные/управляемые AP.\n"
            f"Продолжить выполнение скрипта? \n"
            f"|> lTX - Занизить TX Power\n"
            f"|> Yes - Да оставить без изменений\n"
            f"|> No - Нет завершить скрипт\n"
            f">> "
        ).strip().lower()

        if ans in ("y", "yes", "д", "да"):
            print_info(f"{Module_prefix} > [Check-CorpAP]: Продолжаем работу по запросу пользователя.\n")
            return
        if ans in ("n", "no", "н", "нет", ""):
            print_info(f"{Module_prefix} > [Check-CorpAP]: Завершение работы по запросу пользователя.\n")
            sys.exit(0)
        print("!Повторите ввод (y/yes/д/да или n/no/н/нет)!")
