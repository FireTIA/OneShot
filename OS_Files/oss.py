import platform
import distro


def Check_System_GET_OS():
    system = platform.system()
    
    if system == "Linux":
        # Для получения информации о дистрибутиве Linux
        distro_info = f"{distro.name()} {distro.version()}"
        return f"{distro_info}"
    else:
        return f"OS | {system}"