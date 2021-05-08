import requests, time, subprocess, os

host='http://127.0.0.1:5000/'

def alive():
    try:
        a = requests.get(host)
    except:
        raise SystemExit
alive()

def get_HWID():
    if 'nt' in os.name:
        return subprocess.check_output('wmic csproduct get uuid').decode().split()[1].strip()
#    else:
#        return subprocess.Popen('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split())

while True:
    action = str(input('''[1] Add HWID
[2] Remove HWID
[3] Mark as paid
[4] Mark as unpaid

Choice: '''))
    print()

    if action == '1':
        hwid = get_HWID()
        r = requests.get(f'{host}api/v1/addclient?hwid={hwid}')
        print(r.text)
    elif action == '2':
        hwid = get_HWID()
        r = requests.get(f'{host}api/v1/removeclient?hwid={hwid}')
        print(r.text)
    elif action == '3':
        hwid = get_HWID()
        hasPaid = 1
        r = requests.get(f'{host}api/v1/paidstatus?hwid={hwid}&paid={hasPaid}')
        print(r.text)
    elif action == '4':
        hwid = get_HWID()
        hasPaid = 0
        r = requests.get(f'{host}api/v1/paidstatus?hwid={hwid}&paid={hasPaid}')
        print(r.text)

    time.sleep(1)
    os.system('cls')
