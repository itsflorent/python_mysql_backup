import os
import time
import datetime
import pipes



DB_HOST = f'{database["host"]}'
DB_USER = f'{database["user"]}'
DB_USER_PASSWORD = f'{database["password"]}'

DB_NAME = 'DATABASE_NAME'
BACKUP_PATH = '/home/backups'

# Getting current DateTime to create the separate backup folder like "20180817-123433".
DATETIME = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME

# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(TODAYBACKUPPATH)
except:
    os.mkdir(TODAYBACKUPPATH)

            # Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.

if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1

else:
    multi = 0


# Starting actual database backup process.
if multi:
    in_file = open(DB_NAME, "r")
    flength = len(in_file.readlines())
    in_file.close()
    p = 1
    dbfile = open(DB_NAME, "r")

    while p <= flength:
        db = dbfile.readline()  # reading database name from file
        db = db[:-1]  # deletes extra line
        dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(
                        TODAYBACKUPPATH) + "/" + db + ".sql"
        os.system(dumpcmd)
        gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
        os.system(gzipcmd)
                    p = p + 1
        dbfile.close()
    else:
        db = DB_NAME
        dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(
                    TODAYBACKUPPATH) + "/" + db + ".sql"
        os.system(dumpcmd)
        gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
        os.system(gzipcmd)

print(f"Backup script completed")
print(f"Your backups have been created in '" + TODAYBACKUPPATH + f"' directory")
