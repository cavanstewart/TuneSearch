#!/usr/bin/python3

import os
import psycopg2
import re
import string
import sys
import urllib.parse as up

fd = open('./sql/load.sql', 'r')
sqlFile = fd.read()
fd.close()
sqlCommands = sqlFile.split(';')

try :
        #up.uses_netloc.append("postgres")
        #url = up.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(database=os.environ["RDS_DB_NAME"],
            user=os.environ["RDS_USERNAME"],
            password=os.environ["RDS_PASSWORD"],
            host=os.environ["RDS_HOSTNAME"],
            port=os.environ["RDS_PORT"]
        )
        conn.autocommit = True
        cursor = conn.cursor()
        for command in sqlCommands:
            try:
                cursor.execute(command)
            except Exception as e:
                print(e)
                print('skipped command' + command)
except Exception as e:
    print(e)
finally:
    if (conn):
        cursor.close()
        conn.close()
        print("Connection closed")