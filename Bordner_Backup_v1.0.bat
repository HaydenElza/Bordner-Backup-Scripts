echo off

:: Set file paths, PATH1 is the input path (data on Gymnosperm), PATH2 is the output path (final backup location on Mladenoff9020), PATH3 is the working directory for the backup, PATH4 is the temp directory on local machine for copying the unzipped files to.
set PATH1="Y:\BordnerMaps_2014\output\"
set PATH2="F:\Bordner_Weekly_Backups\"
set PATH3="C:\temp\"
set PATH4="C:\temp\temp\"
set PATH5="C:\noone\share\Bordner"

:: Create temp directory
md %PATH3%temp\

:: Format date to international yyyy-mm-dd format
set _date=%date:~10,4%-%date:~4,2%-%date:~7,2%

:: Copy both geodatabases to the temp folder (the /Z option allows for interuption without error in the event that there is a network error)
:: Copy to local machine first to avoid network errors, xcopy's /Z can account for network errors while 7-zip cannot
xcopy /E /Z %PATH1%* %PATH4%
xcopy /E /Z %PATH5%* %PATH4%

:: Compress geodatabases into .zip file using 7-zip 
"C:\Program Files\7-Zip\7z.exe" a %PATH3%Weekly_Bordner_Backup_%_date%.zip %PATH4%\*


:: Copy .zip file from local computer to backup location
xcopy /Z %PATH3%Weekly_Bordner_Backup_%_date%.zip %PATH2%

:: Clean up temp folder and PATH3
rd /S /Q %PATH4%
del %PATH3%Weekly_Bordner_Backup_%_date%.zip
