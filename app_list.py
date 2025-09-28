import winreg
import subprocess
import os

def get_publisher_from_signature(exe_path):
    """Extract publisher using PowerShell's Get-AuthenticodeSignature"""
    try:
        ps_cmd = [
            "powershell", "-Command",
            f"(Get-AuthenticodeSignature '{exe_path}').SignerCertificate.Subject"
        ]
        result = subprocess.run(ps_cmd, capture_output=True, text=True, timeout=10)
        publisher = result.stdout.strip()
        if publisher:
            return publisher
        else:
            return "Unsigned / Unknown"
    except Exception as e:
        return f"Error: {e}"

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
                
                try:
                    exe_path, _ = winreg.QueryValueEx(subkey, "DisplayIcon")
                    exe_path = exe_path.split(",")[0].strip('"')  # remove ",0" or quotes
                except FileNotFoundError:
                    exe_path = None

                publisher = "N/A"
                if exe_path and os.path.exists(exe_path):
                    publisher = get_publisher_from_signature(exe_path)

                software_list.append({
                    "Name": name,
                    "Executable": exe_path if exe_path else "Not Found",
                    "Publisher": publisher
                })

            except FileNotFoundError:
                continue
            except Exception:
                continue
    return software_list

if __name__ == "__main__":
    installed = get_installed_software()
    print("Installed Software with Digital Signatures:\n")
    for app in installed:
        print(f"- {app['Name']}")
        print(f"   Executable: {app['Executable']}")
        print(f"   Publisher : {app['Publisher']}\n")
