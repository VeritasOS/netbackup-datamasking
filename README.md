# **Data Masking Using Datprof**

## **1. Prerequisite**
        - Backup data must be present.
        - To recover a database on any other machine, the database version must be same. 
        - Python3 must be installed to run the scripts.
        - Root user must create the mount path.
        - To mask a particular database, the user must have DBA privileges.
        - Token is accepted as input for calling the datprof APIs
        - ORACLE user must run the restore.
        - Before masking the database, the user must create groups, environment, and application. 

## **2. APIs**
1.   ### **Getting installed application ID**

         This API prints out the available installed application ID, status, and its database. 
        Following is the API and its parameter 
        
         python3 -W ignore main.py --getInstalledApplicationId yes --project_name --env_name --host --port --token

            - getInstalledApplicationId: Provide string input as yes
            - project_name: Provide string input of project name 
            - env_name: Provide string input of Env name 
            - host: Datprof host 
            - port: Datprof port 
            - token: Token to hit the APIs 

2.  ### **Run Masking** 

        This API masks the respective database table which is provided in the datprof environment with its user and host details. 
        Following is the API and its parameter

        python3 -W ignore main.py --run yes --project_name --env_name --installedApplicationId --scenario_name --token --host --port 

            - run: Provide string input as yes 
            - project name: Provide string input of project name 
            - env_name: Provide string input of Env name 
            - host: Datprof host 
            - port: Datprof port 
            - token: Token to hit the APIs 
            - scenario_name: Provide string input as anonymize only 
            - installedApplicationId: Provide integer type input as the API application ID --scenario_name --token --host --port 


3. ### **Restoring the Oracle Database**

        This API request restores the database from the Oracle Instance Access backup.
        Following is the API and its parameter: 


        python3 main.py --recover --mountpath 

            - recover: Provide string input as yes 
            - mountpath: Provide an absolute path of mount path where the backup files will be stored. 
        
        The path must be provided in the your_mount_path field.

4. ### **Support**
        contact the datprof team for any support or queries 
        https://www.datprof.com/support/





    
       
         



