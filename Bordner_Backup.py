import os, sys, time, datetime
from shutil import copytree, copy2, copystat, make_archive, rmtree


#GymnospermSource = "Z:\\output\\"
GymnospermSource = "Z:\\output\\"
RemoteBackupDrive = "Y:\\"
LocalBackupFolder = "C:\\bordner_backup\\"
TempBackupFolder = "C:\\bordner_backup\\temp\\"


# A simple class used to redirect sys.stdout to file
class WritableObject:
	def __init__(self):
		self.content = []
	def write(self, string):
		self.content.append(string)
# Open writable object
logFile = LocalBackupFolder + "Log_" + datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
log = open(logFile, "w")
# Set sys.stdout to write to log, !!!Don't forget to reset sys.stdout!!!
sys.stdout = log


def copytree(src, dst, symlinks=False, ignore=None):
	# Create list filled with file and directory names
	names = os.listdir(src)
	print names
	print len(names)
	# Check for ignored files, if there is some make
	if ignore is not None:
		ignored_names = ignore(src, names)
	else:
		ignored_names = set()

	# Recursive directory creation at destination
	os.makedirs(dst)

	# Create empty list to store errors in
	errors = []

	# Copy loop
	for name in names:
		print names.index(name),"of",len(names)
		# If the directory or file is in the list of ignore names go to next value in for loop
		if name in ignored_names:
			continue
		# Build file paths
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)

		try:
			# Check for symlink condition and just link source and destination where applicable
			if symlinks and os.path.islink(srcname):
				linkto = os.readlink(srcname)
				os.symlink(linkto, dstname)
			# If not using symlinks and source is a directory, copy tree, ignore where necessary
			elif os.path.isdir(srcname):
				copytree(srcname, dstname, symlinks, ignore)
			# If not using symlinks and source is a file, copy
			else:
				copy2(srcname, dstname)
			# Could also be devices, sockets etc. See except block.

		# Catch the Error from the recursive copytree so that we can continue with other files
		except (IOError, os.error) as why:
			errors.append((srcname, dstname, str(why)))
			print "ERROR:", why
		# Other errors
		#except Error as err:
		#	errors.extend(err.args[0])

	# Use copystat to copy permissions and times of directores that are copied (copy2 alreay copied metadata for files)
	try:
		copystat(src, dst)
	# Catch possible errors
	except WindowsError:
		# Can't copy file access times on Windows
		pass
	except OSError as why:
		errors.extend((src, dst, str(why)))
		print "ERROR:", why
	# If there are erros raise them to users attention
	#if errors:
	#	print errors
	#	raise Error(errors)

def archive(root_dir):
	print "Archiving...",
	# Build path names
	date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
	archive_name = LocalBackupFolder + "Weekly_Bordner_Backup_" + date 
	#root_dir = folder
	make_archive(archive_name, "gztar", root_dir)
	print "DONE"

def send_sms(msg):
	import smtplib

	# Set message parameters
	gmail_user = "email@gmail.com" #email removed for publishing
	gmail_pwd = "pwd" #password removed for publishing
	FROM = 'email@gmail.com' #email removed for publishing (same as above)
	TO = ['0000000000@email-to-smsgateway'] #must be a list (phone number removed for publishing)
	SUBJECT = " Bordner Backup"
	TEXT = msg

	# Prepare actual message
	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(FROM, TO, message)
		server.close()
		print "Successfully sent SMS."
	except:
		print "Failed to send SMS."


# Main - copy, archive, clean up, and notify

# Send sms to notify start
send_sms("Backup was started. " + datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M"))
#print "Copy started:", datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M")

# Copy contents of GymnospermSource to TempBackupFolder
copytree(GymnospermSource,TempBackupFolder,False,None)

print "Copy finished, archive started:", datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M")
send_sms("Copy finished, archive started. " + datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M"))

# Archive the copied contents
archive(GymnospermSource)

print "Archive finished:", datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M")

# Remove temp folder after archive has finished
try:
	rmtree(TempBackupFolder)
	print TempBackupFolder, "was removed."
except:
	print TempBackupFolder, "was not removed!"

# Send sms if backup was successful
send_sms("Backup was successful. " + datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M"))

# Reset sys.stdout
sys.stdout = sys.__stdout__
