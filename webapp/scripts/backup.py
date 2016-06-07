#Scheduled task script to backup database
import os
import datetime
current_time = datetime.datetime.now().time()
path = "/home/dorislee0309/db_backup/groupB/"
filename = path+"db.sqlite3_"+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H_%M_%S')
os.system("cp /home/dorislee0309/citizen_sci_edu/crowdclass/db.sqlite3 {}".format(filename))
print "sucessfully backed up : ",filename
