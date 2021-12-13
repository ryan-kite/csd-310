Author: Ryan Kite
email: ryankiter@gmail.com
discord: FooBar909_(RK)#9403

ZIP FILE CONTENTS
-- README.TXT
-- whatabook_init.sql
-- whatabook.py

Hello - Please follow these steps to run the project

1. Backup Your Database [OPTIONAL]
    
    TO BACKUP your DB: (now) 
        run this command from a folder in your command prompt
        example: 
        rkite@ubuntu:~/csd/csd-310/module_12$ mysqldump -u root -p --databases whatabook >  whatabook_backup.sql
    
    TO RESTORE your DB: (later)
        run this command from a "mysql" command prompt
        example: 
        mysql> source /home/rkite/csd/csd-310/module_12/whatabook_backup.sql

2. Run WhatABook Database Setup Script
    Run this command from a mysql command prompt
    example:
    mysql> source path_to_file/whatabook_init.sql
    * where path_to_file lines up with where the file is on your system

3. Install 1 DEPENDENCY 
    Run this pip command from a command prompt 
    pip install tabulate
    * its for displaying results as mysql tables in the python shell 
    * and a required DEPENDENCY for this program to work properly.

4. Launch the Python Program
    # use your favorite method for running python files. 
    whatabook.py