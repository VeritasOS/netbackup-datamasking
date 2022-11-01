
#!/usr/bin/env python


from tabulate import tabulate
import requests as Req
import json
import base64
from requests.exceptions import HTTPError
import argparse
import pandas as pd
PARSER= argparse.ArgumentParser(description="Data Maskin through Datprof API")

PARSER.add_argument("--create_project", type=str, help="Group name")
PARSER.add_argument("--create_env", type=str, help="Create Env for the group")
PARSER.add_argument("--project_name", type=str, help="Group name")
PARSER.add_argument("--project_id", type=str, help="Group id")
PARSER.add_argument("--install_application", type=str, help="install Application")
PARSER.add_argument("--env_name", type=str, help="Environment Name")
PARSER.add_argument("--run", type=str, help="Runs Masking")
PARSER.add_argument("--scenario_name", type=str, help="Scenario Name")
PARSER.add_argument("--connectString" , type = str)
PARSER.add_argument("--getApplicationId" , type = str)
PARSER.add_argument("--getInstalledApplicationId" , type = str)
PARSER.add_argument("--token" , type = str)
PARSER.add_argument("--applicationId" , type = str)
PARSER.add_argument("--installedApplicationId" ,type=str)
PARSER.add_argument("--recover" ,type=str)
PARSER.add_argument("--host" ,type=str)
PARSER.add_argument("--port" ,type=str)
PARSER.add_argument("--databaseType" ,type=str)

ARGS = PARSER.parse_args()


def CheckProjectExists(project_name):
	
	Flag ,response = GetProjectIdAction(project_name)
	
	if not Flag:
		return  False , response 	

	if response.ok:
        	for item in response.json():
                	if project_name == item['name']:
				return True , None
	return False , None

def CreateProject(project_name):

	Flag ,response = CreateProjectAction(project_name)
	
	if not Flag:
		return False , response
	
	if response.ok:
        	PROJECT_ID = response.json().get("id")

	return True ,PROJECT_ID

def GetProjectID(project_name):
	Flag , response = GetProjectIdAction(project_name)
	
	if not Flag:
		return False , response 

	if response.ok:
		for item in response.json():
			if project_name == item['name']:
				return True,item['id']

	return False,None
	

def GetEnvironmentId(project_id,Environment_name):
	Flag ,response = GetEnvironmentIdAction(project_id)
	if not Flag:
		return False , response 

	if response.ok:
		for item in response.json():
			if Environment_name == item['name']:
				return True,item['id']

	return False,None
	

def CreateEnv(project_id):
	
	ENV_BODY ={
  		"projectId":project_id,
  		"name": ARGS.create_env,
  		"type": "ORACLE",
  		"parameters": [
    				{
      				"name": "DPF_TARGET_CONNECTION",
      				"value": ARGS.connectString,
      				"description": "ORACLE CONNECTION PARAMETERS",
      				"type": "CONNECTIONSTRING",
      				"environmentId": 0
    				}
			      ]
  		 }

	temp = json.dumps(ENV_BODY)
	ENV_BODY_JSON=json.loads(temp)

	
	Flag,response = CreateEnvAction(ENV_BODY_JSON)
	
	if not Flag:
		return False,response	

	if response.ok:
		ID = response.json().get("id")
		return True, ID 


def GetApplicationList():
	print ("Generating List of Applications:")

	Flag , response = GetApplicationListAction()
	if not Flag:
		return False,response    
	
	if response.ok:
	        data =  response.json()
                df = pd.DataFrame.from_dict(data)
                print(tabulate(df[['id','name' ,'version' ,'databaseType']], headers="keys", tablefmt="psql", showindex=False))
	
	return True ,None

def InstallApplication(environmentID,ApplicationID):
	
	application_json={
  		"environmentId":environmentID ,
 		"applicationId":ApplicationID
		}
	installation_json_body = json.loads(json.dumps(application_json))
	
	Flag , response = InstallApplicationAction(installation_json_body) 

	if not Flag:
		return False,response 

	return True ,response  	
	
def GetInstallationId(env_id):
	Flag,response =GetInstallationIdAction(env_id)

	if not Flag:
		return False,response 

	if response.ok:
		data =  response.json()
		df = pd.DataFrame.from_dict(data)
		print(tabulate(df[['installationId','status' ,'installDate']], headers="keys", tablefmt="psql", showindex=False))
 

	

	return True,None


def RunMaskingJob(environmentId,installationId):
	Flag , response = RunMaskingJobAction(environmentId,installationId)
	
	if not Flag:
		return False , response 

	return True,response.json().get('id')

def GetJobStatus(job_id):
	Flag , response = GetJobStatusAction(job_id)
	
	
	if not Flag:
		return False,response
	
	print ("Waiting for job to finish.....")
	while True :	
		Flag , response = GetJobStatusAction(job_id)
		if (response.json().get('status') == 'DONE' or response.json().get('status') ==  'ERROR' or response.json().get('status') == 'CRASHED' ):
			print ("Job Completed")
			break
		

def main():
	
#TO GET THE SAVED APPLCATION DETAILS
	if ARGS.getApplicationId!=None:
		flag , response = GetApplicationList()
		if not flag:
			print ("Error\n",response)
		
#TO GET THE INSTALLED APPLICATION IDs
	if ARGS.getInstalledApplicationId!=None and ARGS.project_name!=None and ARGS.env_name!=None:
                flag ,projectId = GetProjectID(ARGS.project_name)
		if flag==True:
			flag,EnvironmentId = GetEnvironmentId(projectId,ARGS.env_name)
			if flag:
				flag , response =GetInstallationId (EnvironmentId)
			else:
				print "Error fetching the Environment ID"
		else:
			print "Error fetching the project details"

		
         
#TO CREATE PROJECT AND ENVIRONMENT AND INSTALL APPLICATION
	if ARGS.create_project != None and ARGS.create_env != None and ARGS.install_application != None:
		flag , project_id = GetProjectID(ARGS.create_project)
		changeFlag = False		
		if flag:
			print "Project with this name already exists ID :" ,project_id
		elif flag==False and project_id ==None:
			print "Creating project",ARGS.create_project
			flag , project_id = CreateProject(ARGS.create_project)
			changeFlag = True
			if flag:
				print "Project created succesfully with ID :",project_id
			else:
				print project_id #error
				return 
		else:
			print project_id #error 
			return
		print "\n"
		flag,EnvironmentId = GetEnvironmentId(project_id,ARGS.create_env)
		if flag:
                        print "Envrironment with this name already exists in the project \n Environment ID : ",EnvironmentId
                elif flag==False and EnvironmentId ==None:
			print "Creating envrionement",ARGS.create_env
                        flag,EnvironmentId = CreateEnv(project_id)
			changeFlag = True
                	if flag:
                        	print  "Environment created succesfully \nEnvrionment ID :",EnvironmentId
                	else:
                        	print ("Error\n",EnvironmentId) 
				return 
		else:
			print EnvironmentId #error
			return 
		
		print "\n"
		flag ,response = InstallApplication(EnvironmentId ,ARGS.applicationId)
		if flag:
			print ("Application installed Succesfully")
			changeFlag=True
		else:
                        print ("Application Installation failed")
			print ("Error\n",response)
			return

		if not changeFlag:
			print ("Project and Environment has the required Application Installed , you can move ahead with the masking .")	

                                               
	
""" -----------------------------ACTIONS------------------------------"""

HTTPS = "https://"
HOST  = ARGS.host
PORT  = ARGS.port 
def GetProjectIdAction(project_name):
	url = HTTPS+HOST+":"+PORT+"/api/2/projects"
	try:
                GetAllProject = Req.get(
                 url,
                 headers={"X-Auth-Token": ARGS.token},
               	 verify =False
		 )
                GetAllProject.raise_for_status()
	
	except HTTPError as err:
		return False , err.response.text
	except Exception as ExErr:
         	return False ,ExErr 

	return True ,GetAllProject 



def CreateProjectAction(project_name):
	url = HTTPS+HOST+":"+PORT+"/api/2/projects"
	try:
                CreateProjectresponse = Req.post(
                 url,
                 json={"name":project_name},
		 verify =False,
                 headers={"X-Auth-Token": ARGS.token}
                 )
                CreateProjectresponse.raise_for_status()


	except HTTPError as err:
		return False , err.response.text
	except Exception as ExErr:
		return False ,ExErr

	return True, CreateProjectresponse
	

def CreateEnvAction(JSON):
	url = HTTPS+HOST+":"+PORT+"/api/2/environments"
	try:
		CreateEnvironmentresponse = Req.post(
        	url,
		json=JSON ,
                verify =False,
		headers={"X-Auth-Token":ARGS.token }
                )
		CreateEnvironmentresponse.raise_for_status()


	except HTTPError as err:
		return False,err.response.text
	except Exception as ExErr:
		return  False,ExErr

	return True, CreateEnvironmentresponse


def GetApplicationListAction():
	url = HTTPS+HOST+":"+PORT+"/api/2/applications"
	try:
        	GetApplicationsListesponse = Req.get(
		url,
		params={"databaseType":"ORACLE"},
		verify =False,
		headers={"X-Auth-Token": ARGS.token}
		)
		GetApplicationsListesponse.raise_for_status()
	
	except HTTPError as err:
		return False ,err.response.text
 	except Exception as ExErr:
		return False , ExErr

	return True , GetApplicationsListesponse


def GetEnvironmentIdAction(project_id):
	url = HTTPS+HOST+":"+PORT+"/api/2/environments"
	try : 
		GetEnvironmentIdResponse = Req.get(
                url,
                params={"projectId":project_id},
		verify =False,
                headers={"X-Auth-Token": ARGS.token}
                )
                GetEnvironmentIdResponse.raise_for_status()


	except HTTPError as err:
                return False , err.response.text
        except Exception as ExErr:
                return False , err

        return True , GetEnvironmentIdResponse


def InstallApplicationAction(JSON):
	url = HTTPS+HOST+":"+PORT+"/api/2/installations"
	try:
	        InstallApplicationresponse = Req.post(
		url,
		json = JSON,
		 verify =False,
		headers={"X-Auth-Token": ARGS.token}
		)
		InstallApplicationresponse.raise_for_status()


	except HTTPError as err:
        	return False ,err.response.text
	except Exception as ExErr:
        	return False , ExErr 

	return True, InstallApplicationresponse


def RunMaskingJobAction(environmentId,installationId):
	url = HTTPS+HOST+":"+PORT+"/api/2/runs"
	try:
        	RunMaskingresponse = Req.post(
                 url,
                 json = {"environmentId" :environmentId, "scenarioName" :ARGS.scenario_name},
                 params ={"installationId":installationId},
                 verify =False, 
	   	 headers={"X-Auth-Token": ARGS.token}
                 )
        	RunMaskingresponse.raise_for_status()


	except HTTPError as err:
       		return False ,err.response.text
	except Exception as ExErr:
       		return False , ExErr
	
	return True , RunMaskingresponse


def GetInstallationIdAction(env_id):
	
	url = HTTPS+HOST+":"+PORT+'/api/2/installations/{}'.format(env_id)
	try:
                GetInstallationIdresponse = Req.get(
                 url,
                 headers={"X-Auth-Token": ARGS.token},
		 verify =False
                 )
                GetInstallationIdresponse.raise_for_status()

	except HTTPError as err:
        	return False ,err.response.text
	except Exception as ExErr:
		return False, ExErr
		
	return True , GetInstallationIdresponse


def GetJobStatusAction(run_id):
	url = HTTPS+HOST+":"+PORT+'/api/2/runs/{}'.format(run_id)
	try:
                GetStatusresponse = Req.get(
                 url,
                 headers={"X-Auth-Token": ARGS.token},
                 verify = False
		)
               	GetStatusresponse.raise_for_status()

        except HTTPError as err:
                return False ,err.response.text
        except Exception as ExErr:
                return False, ExErr

        return True ,GetStatusresponse

if __name__ == "__main__":
	main()

