import datetime
import psycopg2
import subprocess
import re

date_ = datetime.datetime.now()

def read_pi_temp():
    bashCommand = "vcgencmd measure_temp"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate() #error
    return output

def connect_db():
    host='192.168.10.108'
    port=5432
    user='windfarm_user'
    password='wow,ostro'
    dbname='windfarm'
    return psycopg2.connect('host=192.168.10.108 port=5432 user=windfarm_user password=wow,ostro dbname=windfarm')

read = read_pi_temp()
m = re.search("(?<==)(.{4})", str(read))
temp = m.group(1)

conn = connect_db()
cur = conn.cursor()
date_ = date_ - datetime.timedelta(microseconds=date_.microsecond)
val = (date_, temp)
que = """insert into temp_pi values (%s, %s)"""
cur.execute(que, val)
conn.commit()
cur.close
conn.close

print(date_) 
print(m.group(1))

