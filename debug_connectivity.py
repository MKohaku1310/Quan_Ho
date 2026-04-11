import socket
import time
import sys

def check_port(ip, port, name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((ip, port))
        print(f"[OK] {name} is running on {ip}:{port}")
        return True
    except:
        print(f"[ERROR] {name} is NOT reachable on {ip}:{port}")
        return False
    finally:
        s.close()

if __name__ == "__main__":
    print("-" * 50)
    print("QUAN HO BAC NINH - DIAGNOSTIC TOOL")
    print("-" * 50)
    
    print("\nChecking local services...")
    be = check_port("127.0.0.1", 8000, "Backend (API)")
    fe = check_port("127.0.0.1", 8080, "Frontend (UI)")
    
    if not be:
        print("\nTIP: Make sure you ran 'run.bat' and the Backend window didn't crash.")
        print("     Check if you have another app using port 8000.")
    
    if not fe:
        print("\nTIP: Frontend failed to start. Ensure all requirements in requirements.txt are installed.")
        
    if be and fe:
        print("\nSUCCESS: All services are running locally.")
        print("If your friend still can't access, check your Windows Firewall.")
    
    print("\nPress Enter to exit...")
    input()
