# Man-In-The-Browser-Attack
This script will first force the user to logout from the site and when user will try to login again it will send the credentials to the server which is in our case is setup in server.py and by default localhost.
This script is compatible with internet explorer only and make sure that internet explorer is not forwading you request to the microsoft Edge.
TO DISABLE FORWARDING THE REQUEST TO EDGE ,FOLLOW BELOW STEPS :
    - Go to settings
    - then click on Default Browser present at left side in the List.
    - Then change Let Internet Explorer open sites in Microsoft Edge To NEVER 

## Modifications :
By default this script will only get the credential of gmail and Facebook , But you can modify according to your need by appendng items in the list in mitb.py file.

## Working :
as soon as you will log-in or already logged In this script will force logout and then when you will start login again it will steal the creds and in default case send to the localhost.

##Pre-requisite :
Make sure both the scripts are running parallely!!!
