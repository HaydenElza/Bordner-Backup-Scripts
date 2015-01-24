Bordner-Backup-Scripts
======================

A collection of scripts used to periodically backup data for a project.
--> There are two different approaches for the backup, a MS shell script and a python script. Orginally there was only the bash script bacause it was quick and dirty and worked. Later after an issue went un-noticed and backups were missed for three weeks, the python script was implemented to track errors and notify the sys admin by text message.
--> Both scripts are meant to backup geodatabases, so .lock files should not cause any issues. Though the databases are not compacted nor compressed, so if you do regular editing, consider performing these actions before archiving to save disc space.
