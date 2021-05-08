import requests, mariadb, subprocess, os, threading, uuid
from flask import Flask, request
from uuid import UUID

key = '773924E89752EED9C479D35245FDD'
masterHWID = '35443045-4535-4530-b742-4237ffffffff'

try:
    conn = mariadb.connect(
        user='root',
        password='422537',
        host='127.0.0.1',
        port=3306,
        database='HWID_test'
    )
except mariadb.Error as e:
    print(f'Error connecting to MariaDB: {e}')
    raise SystemExit
cursor = conn.cursor()

def dataHandler(uuid, action, paidStatus=0, key=None):
    try:
        uuid = str(UUID(uuid, version=4))
    except ValueError:
        return 'Invalid HWID'
    if action == 'add':
        try:
            cursor.execute(f"""INSERT INTO clients (uuid, client_id, paid) VALUES (%s,%s,%s);""", (str(uuid), None, 0))
            conn.commit()
            return 'Valid HWID, added'
        except mariadb.IntegrityError as e:
            if 'Duplicate entry' in str(e):
                return 'HWID already in Database'
            else:
                print(e)
    elif action == 'remove':
        try:
            cursor.execute(f'DELETE FROM clients WHERE uuid="{uuid}"')
            conn.commit()
            return 'HWID Removed.'
        except Exception as e:
            return f'\nAn error occured \n{e}'
    elif action == 'paidStatus':
        try:
            cursor.execute(f'UPDATE clients SET paid={paidStatus} WHERE uuid="{uuid}";')
            conn.commit()
            return f'Paid status updated to {paidStatus}.'
        except Exception as e:
            return f'\nAn error occured \n{e}'
    elif action == 'getDB' or action == 'delDB':
        if uuid != masterHWID:
            return 'Unknown User'
        else:
            return 'Access granted, continuing'
        if action == 'getDB':
            try:
                data = cursor.execute(f'SELECT * FROM clients;')
                conn.commit()
                return f'Data: \n{data}'
            except Exception as e:
                return f'\nAn error occured \n{e}'
        elif action == 'delDB':
            try:
                cursor.execute(f'UPDATE clients SET paid={paidStatus} WHERE uuid="{uuid}";')
                conn.commit()
                return f'Paid status updated to {paidStatus}.'
            except Exception as e:
                return f'\nAn error occured \n{e}'


def flaskSite():
    app = Flask(__name__)

    @app.route('/api/v1/addclient')
    def addclient():
        uuid = request.args.get('hwid')
        try:
            return dataHandler(uuid, 'add')
        except Exception as e:
            return f'\nAn error occured \n{e}'

    @app.route('/api/v1/removeclient')
    def removeclient():
        uuid = request.args.get('hwid')
        try:
            return dataHandler(uuid, 'remove')
        except Exception as e:
            return f'\nAn error occured \n{e}'

    @app.route('/api/v1/paidstatus')
    def paidstatus():
        uuid = request.args.get('hwid')
        hasPaid = request.args.get('paid')
        try:
            return dataHandler(uuid, 'paidStatus', int(hasPaid))
        except Exception as e:
            return f'\nAn error occured \n{e}'

    @app.route('/api/v1/admintools')
    def admintools():
        receivekey = request.args.get('key')
        action = request.args.get('action')
        if receivekey == key:
            try:
                return dataHandler(uuid=masterHWID, key=key, action=action)
            except Exception as e:
                return f'\nAn error occured \n{e}'
        else:
            return 'Error, wrong key.'

    app.run(threaded=True)

if __name__ == '__main__':
    threading.Thread(target=flaskSite).start()
