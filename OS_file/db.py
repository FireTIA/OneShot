USB_MAP = {
    ('0cf3', '9271'): 'Atheros AR9271',      
    ('0846', '9030'): 'Atheros AR9271',
    ('0bda', '8812'): 'Realtek RTL8812AU',
    ('0bda', 'b812'): 'Realtek RTL8821AU',
    ('148f', '7601'): 'MediaTek MT7601U',
}

PCI_MAP  = {
    ('10ec', '818b'): 'Realtek RTL8188EE',
    ('168c', '003e'): 'Qualcomm Atheros QCA9377',
}

fun_notice_dev = [
    'sudo python oneshot.py && sudo olivier.py && tea --green --jasmine',
    'sudo python okroshka.py',
    'sudo python shashlyk.py --take-me',
    'sudo pentyToster.py --Toster-pentester',
    'Оливьешечка это хорошо, а тостер погладить еще лучше..',
    'Не запускай airodump-ng в 3 часа ночи.. говорят инопланетяни слушаю эфир людей (。﹏。*)',
]


#
# === OUI оборудования ubiquit и подобного (СПИСОК НЕ ПОЛНЫЙ!)
#

# Ubiquiti (UniFi, AirMax и прочие точки)
Ubiquiti_OUI = [
    "00:15:6D",
    "00:18:E7",
    "00:27:22",
    "04:18:D6",
    "18:E8:29",
    "24:5A:4C",
    "24:A4:3C",
    "28:70:4E",
    "44:D9:E7",
    "60:22:32",
    "68:72:51",
    "68:D7:9A",
    "70:A7:41",
    "74:83:C2",
    "74:AC:B9",
    "74:F9:2C",
    "74:FA:29",
    "78:45:58",
    "78:8A:20",
    "80:2A:A8",
    "84:78:48",
    "90:41:B2",
    "94:2A:6F",
    "9C:05:D6",
    "A4:F8:FF",
    "A8:9C:6C",
    "AC:8B:A9",
    "B4:FB:E4",
    "D0:21:F9",
    "D8:B3:70",
    "DC:9F:DB",
    "E0:63:DA",
    "E4:38:83",
    "F0:9F:C2",
    "F4:92:BF",
    "F4:E2:C6",
    "FC:EC:DA",
]

# MikroTik (RouterBOARD, точки и маршрутизаторы)
MikroTik_OUI = [
    "00:0C:42",
    "04:F4:BC",
    "08:55:31",
    "10:57:69",
    "14:5A:FC",
    "18:FD:74",
    "2C:C8:1B",
    "48:8F:5A",
    "48:A9:8A",
    "4C:5E:0C",
    "58:BF:EA",
    "64:D1:54",
    "6C:3B:6B",
    "74:4D:28",
    "78:9A:18",
    "80:2A:A8",  # иногда попадается как MikroTik, иногда как Ubiquiti
    "B8:69:F4",
    "C4:AD:34",
    "CC:2D:E0",
    "D4:01:C3",
    "D4:CA:6D",
    "D8:0D:17",
    "DC:2C:6E",
    "E4:8D:8C",
    "F4:1E:57",
]

# Cisco (роутеры, коммутаторы, enterprise AP)
Cisco_OUI = [
    "00:1B:54",
    "00:1E:49",
    "00:22:90",
    "00:23:04",
    "00:24:14",
    "00:25:45",
    "00:26:0B",
    "00:26:CB",
    "00:27:0E",
    "00:40:96",
    "00:50:73",
    "00:90:2B",
    "00:E0:1E",
    "3C:08:F6",
    "3C:DF:BD",
    "64:D9:54",
    "6C:41:6A",
    "70:5A:0F",
    "74:A0:2F",
    "84:78:8B",
    "A0:1D:48",
    "A4:93:3F",
    "B4:A4:E3",
    "BC:16:65",
    "C0:25:E9",
    "C8:F9:F9",
    "D0:67:E5",
    "D4:D7:48",
    "E0:2F:6D",
    "F4:4E:05",
    "F8:7B:8C",
]



#
#  === Текста для настроек
#
settings_dialoge = {
    "1_ID-Notice-1": '| >OS_Target< \n| Указывается тип пути для устройств\n| Для NetHunter: /sdcard/nh_files/OneShotPin_Log\n| Для Kali: /home/kali/OneShotPin_Log',      
}
