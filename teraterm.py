from pywinauto.application import Application
from pywinauto.controls.win32_controls import ComboBoxWrapper
from pywinauto.keyboard import send_keys
from datetime import datetime
import time


def main(): 
    macroPath= 'OTA_reboot_method'
    comport='COM4'
    #Path to Teraterm
    apppath= r"C:\Program Files (x86)\teraterm\ttermpro.exe"
    logName='logfilename'
    
    #initilizing the App
    app=Application(backend='uia').start(apppath, timeout=10)
    
    #Geting the Teraterm Main Window
    main_dlg=app.window(title=u"Tera Term - [disconnected] VT")
    print(main_dlg.window_text())
    
    #Selecting the Com-Port
    port_config_dlg=main_dlg.window(title=u'Tera Term: New connection')
    print(port_config_dlg.window_text())
    try:
        port_config_dlg.Serial.select()
    except Exception:
        print("[ERROR]Comm ports not fount, please connect the serail cable")
    time.sleep(0.5)
    port_selection=port_config_dlg.ComboBox4
    port_selection.OpenButton.invoke()
    for text in ComboBoxWrapper(port_selection).texts():
        if text==comport:
            ComboBoxWrapper(port_selection).select(comport+": Prolific USB-to-Serial Comm Port" "("+comport+")").click() 
    time.sleep(1)

    #port_selection.OK.click()
    send_keys('{TAB}')  
    send_keys('{ENTER}')


    ###########Selectig the Baudrate#############
    send_keys('%s') 
    send_keys('e')
    send_keys('{TAB}') 
    send_keys('115200')
    for i in range(0,7):
        send_keys('{TAB}')
    send_keys('{ENTER}') 

    ##########Selcting the Teminal Reciever & Transmitter##############
    send_keys('%s') 
    send_keys('t')
    for i in range(0,3):
        send_keys('{TAB}')
    for i in range(0,3):
        send_keys('{DOWN}')
    send_keys('{TAB}')
    send_keys('{DOWN}')
    for i in range(0,7):
        send_keys('{TAB}')
    send_keys('{ENTER}')
    ###########Saving the logs with timestamp#############
    doc_props = app.window_(title_re = ".*Tera Term VT")
    print(doc_props.window_text())
    doc_props.menu_select("File->Log...")
    Log_dlg = doc_props.window(title = "Tera Term: Log")
    print(Log_dlg.window_text())
    tm=datetime.now().strftime("%m%d%Y%H%M%S")
    time.sleep(1)
    Log_dlg.Edit.type_keys(logName+str(tm))
    Log_dlg.CheckBox6.click()
    Log_dlg.Save.click()
    time.sleep(1)
    ###########Selecting the TTL Macrio From apppath#############
    doc_props.menu_select("Control->Macro")
    time.sleep(1)
    send_keys(macroPath+'.ttl')
    send_keys('{ENTER}')
    time.sleep(20)


if __name__=='__main__':
    try:
        main()
    except Exception as e:
        print(e)
        