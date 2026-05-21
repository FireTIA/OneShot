from datetime import datetime
import datetime
import platform
import distro
import os
import sys















#
# Получение информации о дистрибутиве
#

def OS__Check_System_GET_OS():
    system = platform.system()
    
    if system == "Linux":
        # Для получения информации о дистрибутиве Linux
        distro_info = f"{distro.name()} {distro.version()}"
        return f"{distro_info}"
    else:
        return f"OS | {system}"

#
# Получение информации дате и время
#

def OS__date_time(type_write):
    if type_write in ["Y-m-d H:M:S", "date-times", "date times"]:
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif type_write.lower() in ["date", "data"]:
        dt = datetime.datetime.now().strftime("%Y-%m-%d")
    elif type_write.lower() in ["time"]:
        dt = datetime.datetime.now().strftime("%H:%M")
    elif type_write.lower() in ["times", "time-sec"]:
        dt = datetime.datetime.now().strftime("%H:%M:%S")

    return dt