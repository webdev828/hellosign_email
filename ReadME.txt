1. Add/Update/modify the file list.txt with list of email. The file name should always be equal to list.txt.
2. To update properties open config.properties file in text editor and modify the configurations

Here are the sample configurations:
[AppConf]
domain=https://app.hellosign.com/account/logIn            	[URL] [Do not change if not required]
username=verify@domainautopsy.com				    	[Username for login]
password=Pallushort@123 							[password for login]
headless=False 									[Browser mode True for running browser in backend, False to see browser]
limit=5 										[max number of emails in each CSV]
template=New Paitent 								[Valid template name that exists]
firstname=Linda 								[firstname for the final screen]
lastname=Tzoref									[lastname for the final screen]
message=MESSAGE									[Message for the final screen]

3. Make sure Mozilla Firefox Browser is installed in the system or the application won't start.
4. Start the application by running main.exe.
5. Once the application starts it will create a folder named workflow_<todays_date>, there would be two subfolders inside it called processed and error.
files would go into processed or error folder based on the processing status.