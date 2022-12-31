import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import random
import threading
PATH = "C:\Program Files (x86)\chromedriver.exe"
option = webdriver.ChromeOptions()
option.add_argument("window-size=1280,800")
option.add_argument('--no-sandbox')\
#option.add_experimental_option( "prefs",{'profile.managed_default_content_settings.image': 2})
option.add_argument('--disable-dev-shm-usage')
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
#option.add_experimental_option( "prefs",{'profile.managed_default_content_settings.images': 2})
#option.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
option.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=option)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

#driver.set_page_load_timeout(5) #- adding a timeout kills it essentially

userphone = os.environ['userphone']
cvvcode = os.environ['cvvcode']
firstName = os.environ['firstName']
lastName = os.environ['lastName']
streetAddress = os.environ['streetAddress']
city = os.environ['city']
state = os.environ['state']
zipcode = os.environ['zipcode']
contactemail = os.environ['contactemail']
creditcard = os.environ['creditcard']
ccexpmonth = os.environ['ccexpmonth']
ccexpyear = os.environ['ccexpyear']



bbhome = "https://www.bestbuy.com/"
bbsignin = "https://www.bestbuy.com/identity/global/signin"
def isCartEmpty():
    global driver
    try:
        driver.find_element_by_class_name("dot")
        print("Found dot")
        return False
    except:
        return True

def getATCStatus():
    global driver
    atcbuttonclass = "fulfillment-add-to-cart-button"
    atc = driver.find_element_by_class_name(atcbuttonclass)
    status = atc.text
    html = atc.get_attribute("innerHTML")
    #if 'id="wait-overlay' in html:
        #status = "Queue"
    return status


def signinBB():
    global driver
    driver.get(bbsignin)
    print(driver.title)

    username = driver.find_element_by_name("fld-e")
    username.send_keys("gymnast544mods@gmail.com")

    password = driver.find_element_by_name("fld-p1")
    password.send_keys("mFgU48!pRy:sGj4")

    signin = driver.find_element_by_xpath("/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]/button")
    signin.click()
    time.sleep(5)


def setStore():
    global driver, zipcode
    driver.get("https://www.bestbuy.com/site/store-locator")
    locationentering = driver.find_element_by_xpath("/html/body/div[2]/main/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div/div/form/fieldset/div/input")
    submitbutton = driver.find_element_by_xpath("/html/body/div[2]/main/div[2]/div[1]/div[1]/div/div/div[1]/div/div/div/div/form/fieldset/div/button")
    locationentering.send_keys(zipcode)
    submitbutton.click()
    time.sleep(5)
    driver.find_element_by_class_name("make-this-store-container").click()
    print("Store set")
#setStore()
products = []

class product:
    def __init__(self, url, refreshamount):
        self.url = url
        self.refreshamount = refreshamount
        self.lastrefreshed = time.time()
        self.windowhandle = None
        global products
        products.append(self)
    def open(self):
        global driver
        earlyhandles = driver.window_handles
        driver.execute_script("window.open('"+self.url+"');")
        time.sleep(.5)
        currenthandles = driver.window_handles
        #looks for the difference in the driver.window_handles list to determine which window handle is relevant
        for handle in currenthandles:
            handlestring = str(handle)
            matched = False
            for earlyhandle in earlyhandles:
                if str(earlyhandle)==handlestring:
                    matched = True
            if not matched:
                self.windowhandle = handle
                print(str(self.windowhandle))

        
    def switchTo(self):
        global driver
        driver.switch_to.window(self.windowhandle)
        print(str(self.windowhandle))

    def checkSelf(self):
        self.switchTo()
        atcstatus = getATCStatus()
        print(atcstatus)
        cartEmpty = isCartEmpty()
        if atcstatus == "Add to Cart":
            #this is the big brain stuff where we add it to cart
            atcbuttonclass = "fulfillment-add-to-cart-button"
            atc = driver.find_element_by_class_name(atcbuttonclass)
            atc.click()
            time.sleep(1.5)
            cartEmpty = isCartEmpty()
        elif "more inventory" in atcstatus:
            print("QUEUEUEUE")
            #here we do nothing, just waiting for it to be ready to buy
            atcbuttonclass = "fulfillment-add-to-cart-button"
            atc = driver.find_element_by_class_name(atcbuttonclass)
            #atc.click()
            #atc.click()
        elif "Find" in atcstatus:
            #figure out what to do later lol - find a store
            pass
        if not cartEmpty:
            #here we navigate to cart and attempt to checkout
            driver.get("https://www.bestbuy.com/checkout/r/fast-track")
            startcheckouttime = time.time()
            while time.time()-startcheckouttime<15:
                inputdropdowns = {"payment.billingAddress.state":state, "consolidatedAddresses.ui_address_2.state":state, "expiration-month":ccexpmonth, "expiration-year":ccexpyear}
                for dropdown in inputdropdowns:
                    try:
                        stateselected = False
                        selectelement = driver.find_element_by_id(dropdown)
                        selectobject = Select(selectelement)
                        try:
                            selected = selectobject.first_selected_option.get_attribute("value")
                            if selected == inputdropdowns[dropdown]:
                                stateselected = True
                        except:
                            pass
                        if not stateselected:
                            selectobject.select_by_value(inputdropdowns[dropdown])
                            print(selectobject.first_selected_option.get_attribute("value"))
                            selectelement.click()
                    except:
                        pass
                        #print("Error with select")
                inputdropdownsclass = {"expiration-month":ccexpmonth, "expiration-year":ccexpyear}
                for dropdown in inputdropdowns:
                    try:
                        stateselected = False
                        selectelement = driver.find_element_by_name(dropdown)
                        selectobject = Select(selectelement)
                        try:
                            selected = selectobject.first_selected_option.get_attribute("value")
                            if selected == inputdropdowns[dropdown]:
                                stateselected = True
                        except:
                            pass
                        if not stateselected:
                            selectobject.select_by_value(inputdropdowns[dropdown])
                            print(selectobject.first_selected_option.get_attribute("value"))
                            selectelement.click()
                    except:
                        pass
                        #print("Error with select")
                inputboxes = {"user.phone":userphone, "credit-card-cvv":cvvcode, "payment.billingAddress.firstName":firstName, "payment.billingAddress.lastName":lastName,\
                              "payment.billingAddress.street":streetAddress, "payment.billingAddress.city":city, "payment.billingAddress.zipcode":zipcode,\
                              "user.emailAddress":contactemail, "optimized-cc-card-number":creditcard, "consolidatedAddresses.ui_address_2.firstName":firstName,\
                              "consolidatedAddresses.ui_address_2.lastName":lastName, "consolidatedAddresses.ui_address_2.street":streetAddress,\
                              "consolidatedAddresses.ui_address_2.city":city, "consolidatedAddresses.ui_address_2.zipcode":zipcode}
                for inputid in inputboxes:
                    try:
                        inputbox = driver.find_element_by_id(inputid)
                        if not (inputbox.get_attribute("value")==inputboxes[inputid]):
                            #we need to fill it up
                            print("Clearing input box, filling with", inputboxes[inputid])
                            if len(inputbox.get_attribute("value"))>0:
                                while len(inputbox.get_attribute("value"))>0:
                                    inputbox.send_keys(Keys.CONTROL+Keys.BACK_SPACE)
                            inputbox.send_keys(inputboxes[inputid])
                    except:
                        pass
                buttonclasses = ["button--continue", "button--place-order"]
                for buttonclass in buttonclasses:
                    try:
                        pass
                        buttonobject = driver.find_element_by_class_name(buttonclass)
                        buttonobject.click()
                    except:
                        print("Unable to find button "+buttonclass)
            driver.get(self.url)
        else:
            #this mean's either sold out, coming soon, or unavailable nearby
            #here we need to do the checking of the time (for the refreshing)
            currenttime = time.time()
            if currenttime-self.lastrefreshed > random.randint(self.refreshamount-1, self.refreshamount+1):
                self.lastrefreshed = currenttime
                print("Refreshing")
                threading.Thread(target=driver.refresh).start()
                #driver.refresh()
            else:
                time.sleep(.5)

product("https://www.bestbuy.com/site/pny-xlr8-gaming-single-fan-nvidia-geforce-gtx-1660-super-overclocked-edition-6gb-gddr6-pci-express-3-0-graphics-card-black/6407309.p?skuId=6407309", 8)
#product("https://www.bestbuy.com/site/rogue-legacy-standard-edition-nintendo-switch/6383153.p?skuId=6383153", 5)
"""
product("https://www.bestbuy.com/site/apple-airpods-pro-white/5706659.p?skuId=5706659", 5)
product("https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440", 10)
product("https://www.bestbuy.com/site/nvidia-geforce-rtx-3090-24gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429434.p?skuId=6429434", 10)
product("https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442", 10)
product("https://www.bestbuy.com/site/evga-nvidia-geforce-rtx-3060-ti-ftw3-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6444444.p?skuId=6444444", 10)
product("https://www.bestbuy.com/site/asus-nvidia-geforce-tuf-rtx3070-8gb-gddr6-pci-express-4-0-graphics-card-black/6439128.p?skuId=6439128", 10)
product("https://www.bestbuy.com/site/gigabyte-nvidia-geforce-rtx-3070-aorus-master-8gb-gddr6-pci-express-4-0-graphics-card/6439384.p?skuId=6439384", 10)
product("https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402", 10)
product("https://www.bestbuy.com/site/gigabyte-nvidia-geforce-rtx-3060-gaming-oc-12gb-gddr6-pci-express-4-0-graphics-card/6454688.p?skuId=6454688", 10)
product("https://www.bestbuy.com/site/evga-geforce-rtx-3070-xc3-ultra-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6439299.p?skuId=6439299", 10)
product("https://www.bestbuy.com/site/evga-geforce-rtx-3090-xc3-ultra-gaming-24gb-gddr6-pci-express-4-0-graphics-card/6434198.p?skuId=6434198", 10)"""
    
#signinBB()
for product in products:
    product.open()

while True:
    for product in products:
        #time.sleep(1)
        product.checkSelf()
    

time.sleep(5)
print(getATCStatus())

print("Cart empty", isCartEmpty())

#continue button for Amazon ATC link is "a-button-inner" by class
#email verification id = verificationCode
"""
<div><div style="position:relative"><button class="btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button" type="button" data-sku-id="6428324" style="padding:0 8px" aria-describedby="add-to-cart-wait-overlay"><svg aria-hidden="true" role="img" viewBox="0 0 100 100" style="width:16px;height:16px;margin-bottom:-2px;margin-right:9px;fill:currentColor"><use href="/~assets/bby/_img/int/plsvgdef-frontend/svg/cart.svg#cart" xlink:href="/~assets/bby/_img/int/plsvgdef-frontend/svg/cart.svg#cart"></use></svg>Add to Cart</button><span id="wait-overlay-6428324"></span><span class="c-overlay-wrapper"><span class="overlayTrigger"><div aria-expanded="true" aria-controls="wait-overlay-6428324" aria-describedby="wait-overlay-6428324" style="width:0;height:0"></div></span><div class="c-overlay top wait-overlay " id="wait-overlay-6428324" style="display:none;margin-bottom:30px;bottom:0;right:0" aria-live="polite"><div><div id="add-to-cart-wait-overlay"><h2 class="heading-6" style="margin-bottom:8px"><svg aria-hidden="true" role="img" viewBox="0 0 100 100" width="19" height="19" fill="#0046be" style="position:relative;top:4px;margin-right:4px"><use href="/~assets/bby/_img/int/plsvgdef-frontend/svg/OrderHistory_Line_Sm.svg#OrderHistory_Line_Sm" xlink:href="/~assets/bby/_img/int/plsvgdef-frontend/svg/OrderHistory_Line_Sm.svg#OrderHistory_Line_Sm"></use></svg>How it\'s going to work:</h2><ul style="padding-left:19px;margin-bottom:8px"><li style="margin-bottom:8px">Every few minutes, we\'re going to release more inventory.</li><li style="margin-bottom:8px">Shortly, the button below will turn back to yellow (unless we sell out).</li><li style="margin-bottom:8px">At that point, try adding it to your cart again.</li></ul><p><strong>Pro Tip:</strong> <!-- -->If that works, checkout as fast as you can. It won\'t be reserved until you are in checkout. Good luck!</p></div></div><div class="arrow" style="left:calc(85% - 11px)"></div><button class="c-close-icon  " type="button"><svg aria-hidden="true" role="img" viewBox="0 0 100 100"><use href="/~assets/bby/_img/int/plsvgdef-frontend/svg/Close_Cancel_Line.svg#Close_Cancel_Line" xlink:href="/~assets/bby/_img/int/plsvgdef-frontend/svg/Close_Cancel_Line.svg#Close_Cancel_Line"></use></svg><span class="sr-only">Close</span></button></div></span></div></div>"""
#above is the html of a waiting button, before it shows ATC

