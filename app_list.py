import winreg

def get_installed_software():
    software_list = []
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    
    for reg_path in reg_paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
        except FileNotFoundError:
            continue

        for i in range(0, winreg.QueryInfoKey(key)[0]):
            try:
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)
                name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                software_list.append(name)
            except FileNotFoundError:
                continue
            except Exception:
                continue
    return software_list

if __name__ == "__main__":
    installed = get_installed_software()
    print("Installed Software on this system:\n")
    for app in installed:
        print(f"- {app}")
