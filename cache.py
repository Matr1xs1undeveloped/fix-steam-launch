import os
import shutil
import sys
import subprocess
import winreg
from pathlib import Path
import ctypes

try:
    from tkinter import filedialog, Tk
except ImportError:
    filedialog = None
    Tk = None


def is_admin():
    try:
        return ctypes.windll.shell.IsUserAnAdmin()
    except:
        try:
            return os.getuid() == 0
        except AttributeError:
            return False


def request_admin_privileges():
    if not is_admin():
        try:
            script_path = sys.argv[0]
            if getattr(sys, 'frozen', False):
                script_path = sys.executable
            
            cmd = f'powershell -Command "Start-Process \'{script_path}\' -Verb RunAs"'
            subprocess.Popen(cmd, shell=True)
            sys.exit()
        except Exception as e:
            print(f"Error requesting admin privileges: {e}")
            return False
    return True


def delete_folder(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"Deleted folder: {path}")
            return True
        except Exception as e:
            print(f"Error deleting folder {path}: {e}")
            return False
    else:
        print(f"Folder not found: {path}")
        return False


def delete_file(path):
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"Deleted file: {path}")
            return True
        except Exception as e:
            print(f"Error deleting file {path}: {e}")
            return False
    else:
        print(f"File not found: {path}")
        return False


def get_steam_paths():
    user_profile = os.environ.get("USERPROFILE")
    if not user_profile:
        print("Error: Could not determine user profile directory")
        return None, None

    steam_dir = os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Steam")
    local_steam_dir = os.path.join(user_profile, "AppData", "Local", "Steam")

    return {
        "appcache": os.path.join(steam_dir, "appcache"),
        "userdata": os.path.join(local_steam_dir, "userdata"),
    }


def delete_steam_cache():
    print("\nDeleting Steam AppCache and App Profile...")
    print("-" * 40)

    paths = get_steam_paths()
    if not paths:
        return

    deleted_count = 0
    for name, path in paths.items():
        if delete_folder(path):
            deleted_count += 1

    print("-" * 40)
    print(f"Completed: {deleted_count}/{len(paths)} items deleted\n")


def select_custom_path():
    print("\nCustom Path Deletion")
    print("-" * 40)

    if Tk is None or filedialog is None:
        print("Error: tkinter is not available. Please install it or use a bundled version.")
        return

    try:
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        folder_path = filedialog.askdirectory(title="Select folder to delete")

        if folder_path:
            confirm = input(f"\nAre you sure you want to delete: {folder_path}? (yes/no): ").strip().lower()
            if confirm == "yes":
                if delete_folder(folder_path):
                    print(f"Successfully deleted: {folder_path}")
                else:
                    print(f"Failed to delete: {folder_path}")
            else:
                print("Deletion cancelled.")
        else:
            print("No folder selected.")
    except Exception as e:
        print(f"Error opening file dialog: {e}")
    finally:
        try:
            root.destroy()
        except:
            pass

    print("-" * 40 + "\n")


def setup_startup():
    print("\nSetup Automatic Startup")
    print("-" * 40)

    try:
        if getattr(sys, 'frozen', False):
            script_path = sys.executable
        else:
            script_path = os.path.abspath(__file__)

        startup_key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        registry_name = "SteamCacheCleaner"

        batch_dir = os.path.join(os.environ.get("APPDATA"), "SteamCacheCleaner")
        os.makedirs(batch_dir, exist_ok=True)

        batch_file = os.path.join(batch_dir, "startup.bat")
        batch_content = f"""@echo off
REM Run with admin privileges
powershell -Command "Start-Process '{script_path}' -Verb RunAs"
"""

        with open(batch_file, 'w') as f:
            f.write(batch_content)

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, registry_name, 0, winreg.REG_SZ, batch_file)
            winreg.CloseKey(key)
            print(f"Successfully added to startup.")
            print(f"The app will run with admin privileges on next startup.")
            print(f"Batch file: {batch_file}")
        except Exception as e:
            print(f"Error adding to registry: {e}")

    except Exception as e:
        print(f"Error setting up startup: {e}")

    print("-" * 40 + "\n")


def display_menu():
    print("\n" + "-" * 40)
    print("STEAM CACHE CLEANER")
    print("-" * 40)
    print("\nSelect an option:\n")
    print("  1 - Delete Steam AppCache and App Profile")
    print("      (requires admin privileges)")
    print("\n  2 - Set Custom Path to Delete Files")
    print("      (opens file explorer for browsing)")
    print("\n  3 - Run at Startup")
    print("      (auto-delete on startup with admin privileges)")
    print("\n  4 - Exit")
    print("-" * 40)


def main():
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            if request_admin_privileges():
                delete_steam_cache()
        elif choice == "2":
            select_custom_path()
        elif choice == "3":
            setup_startup()
        elif choice == "4":
            print("\nExiting Steam Cache Cleaner. Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")

        input("Press Enter to continue...")


if __name__ == "__main__":
    main()