#Bordner Scripts
We are currently working to digitized the Bordner surveys of Wisconsin. Through this process there is a need for various scripts and tools to complete necessary tasks.

##Backup Scripts
A collection of scripts used to periodically backup data for a project.

###Bordner Backup
These are scripts are to backup the orthorectified images, digitized townships and attributed townships. General structure is:
1. Folder you want to backup
2. Folder you want to backup to
3. Temporary working directory
4. Temp folder within working directory
This can be easily adapted to any backup application.

Differences between scripts and notes:
- There are two different approaches for the backup, a MS shell script and a python script. Orginally there was only the bash script bacause it was quick and dirty and worked. Later after an issue went un-noticed and backups were missed for three weeks, the python script was implemented to track errors and notify the sys admin by text message.
- Both scripts are meant to backup geodatabases, so .lock files should not cause any issues. Though the databases are not compacted nor compressed, so if you do regular editing, consider performing these actions before archiving to save disc space.

##Remove Extra Domains
This script is meant to delete incorrect (non-default) domains from our Bordner project geodatabases. To do this, the script first removes all domains from the fields so that the domain can be deleted. This itereates over all feature classes and fields within those feature classes.
