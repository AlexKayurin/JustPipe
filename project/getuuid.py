import subprocess
import hashlib

computer_id = subprocess.check_output("wmic bios get serialnumber").decode().split()[1]
print(computer_id)

hstring = int(hashlib.sha256(computer_id.encode('utf-8')).hexdigest(), 16) % 10**8
print(hstring)