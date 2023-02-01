import argparse
from OracleRestoreScript import *
from MaskingUtility import *


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
PARSER.add_argument("--mountpath",type=str)
ARGS = PARSER.parse_args()

def main():

#RECOVERY OPERATIONS
		if ARGS.recover!=None:
				FILENAME="Recovery_DB" + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '_') + ".output"
				Output_file=open(FILENAME, "w")
				print ("Starting Oracle Recovery...")
				mountpath = "'" +ARGS.mountpath+ "'"

				cmd , Flag = check_nbu_dir()	
				if Flag:
					Flag = Recovery(Output_file , mountpath,cmd)
					if not Flag:
							print ("Recovery Operations Done")
					else:
							print ("Check Logs for Error")
							return False
				else:
					return
#RUNNING MASK
		if ARGS.run !=None:
				if ARGS.project_name != None:
						Flag , PROJECT_ID = GetProjectID(ARGS.project_name)
						if ARGS.env_name!=None and Flag == True:
								Flag , ENV_ID = GetEnvironmentId(PROJECT_ID,ARGS.env_name)
								if Flag:
										Flag ,JOB_ID = RunMaskingJob(ENV_ID ,ARGS.installedApplicationId)

										if Flag:
												print ("Starting job...")
												GetJobStatus(JOB_ID)

										else:
												print ("couldnt submit the job")
												print (JOB_ID)
								else:
										print("Environment ID could not be fetched")
						else:
								print ("Provide Environment name or Project name was not found")
				else:
						print ("Provide Project Name")

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
								print ("Error fetching the Environment ID")
				else:
						print ("Error fetching the project details")

#TO CREATE PROJECT AND ENVIRONMENT AND INSTALL APPLICATION
		if ARGS.create_project != None and ARGS.create_env != None and ARGS.install_application != None:
				flag , project_id = GetProjectID(ARGS.create_project)
				changeFlag = False
				if flag:
						print ("Project with this name already exists ID :" ,project_id)
				elif flag==False and project_id ==None:
						print ("Creating project",ARGS.create_project)
						flag , project_id = CreateProject(ARGS.create_project)
						changeFlag = True
						if flag:
								print ("Project created succesfully with ID :",project_id)
						else:
								print (project_id) #error
								return
				else:
						print (project_id) #error
						return
				
				flag,EnvironmentId = GetEnvironmentId(project_id,ARGS.create_env)
				if flag:
						print ("Envrironment with this name already exists in the project \n Environment ID : ",EnvironmentId)
				elif flag==False and EnvironmentId ==None:
						print ("Creating envrionement",ARGS.create_env)
						flag,EnvironmentId = CreateEnv(project_id)
						changeFlag = True
						if flag:
								print  ("Environment created succesfully \nEnvrionment ID :",EnvironmentId)
						else:
								print ("Error\n",EnvironmentId)
								return
				else:
						print (EnvironmentId) #error
						return

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




if __name__ == "__main__":
		main()


