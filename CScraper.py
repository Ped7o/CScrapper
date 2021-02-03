from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def DataCollect(lst, today, name) :
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options = options) 
   
    file = open('{}{}.txt'.format(today, name), 'w+')
    neto_liq = list()
    
    for cred in lst :
        #Datos obtenidos en lst
        cuit = cred['cuit']
        user = cred['user']
        pw = cred['pw']
        comercios = cred['comercios']
        subt = list()

        #Esperas
        wait = WebDriverWait(driver, 15)
        w2 = WebDriverWait(driver, 5) #wait hecho solo para ver si existe planilla de liquidación.
        
        print('''\nUsuario: {}\n'''.format(user))
        file.write('''\nUsuario: {}\n'''.format(user))

        #Esta primera parte se encarga de abrir la página e ir hasta las
        driver.get('https://smpc.cabal.coop/Cabaldiaseguridad/Pages/Login.aspx')
        driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtEstablecimiento$TextBoxInt").send_keys(cuit)
        driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtOperador$TextBoxInt").send_keys(user)
        driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtClave$TextBoxInt").send_keys(pw)
        driver.find_element_by_id("ContentPlaceHolder1_lnkIngresar_BotonGrilla").click()
      
        try :
               
            element = wait.until(EC.element_to_be_clickable((By.ID, 'CellLiq')))
            driver.find_element_by_id("CellLiq").click()
 
            for cmr in comercios :
                element = wait.until(EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_SubMnuLiquidacionesD")))
                driver.find_element_by_id("ContentPlaceHolder1_SubMnuLiquidacionesD").click()
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cboComercioSelector']/div[2]/div[1]/div[2]/div[1]/a[1]")))
                driver.find_element_by_xpath("//*[@id='cboComercioSelector']/div[2]/div[1]/div[2]/div[1]/a[1]").click()
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@rel='{}']".format(cmr))))
                driver.find_element_by_xpath("//a[@rel='{}']".format(cmr)).click()
                sleep(1)
                driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolderComer_dtpDesde_txtdate').click()
                driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolderComer_dtpDesde_txtdate').send_keys(today)
                driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolderComer_dtpHasta_txtdate').click()
                driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolderComer_dtpHasta_txtdate').send_keys(today)
                sleep(1)
                driver.find_element_by_class_name("bt-buscar").click()
                #Dentro del loop, se trata de ingresar a los datos (en caso de haber), sino,
                #coninúa buscando
                try :
                    driver.find_element_by_xpath("//a[@title='Consultar']").click()
                    element = w2.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='ContentPlaceHolder1_ContentPlaceHolderComer_divDataRetenciones']/table[2]/tbody[1]/tr[1]/td[3]")))
                    neto = driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_ContentPlaceHolderComer_divDataRetenciones']/table[2]/tbody[1]/tr[1]/td[3]").text
                    print('Liquidación de {}: {}'.format(cmr, neto))
                    file.write('Liquidación de {}: {}\n'.format(cmr, neto))
                    neto_liq.append(neto.translate(str.maketrans({'.':'',',':'.'})))
                    subt.append(neto.translate(str.maketrans({'.':'',',':'.'})))
                    sleep(1)
                except :
                    element = w2.until(EC.visibility_of_element_located((By.ID, 'ContentPlaceHolder1_ContentPlaceHolderComer_lblError_LabelError')))
                    error = driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolderComer_lblError_LabelError')
                    print('{}: {}'.format(cmr, error.text))
                    file.write('{}: {}\n'.format(cmr, error.text))
                    continue
       
        except :
            file.write('Usuario {} no puede ingresar. Verifique si no debe cambiar la contraseña\n'.format(user))
            print('Usuario {} no puede ingresar. Verifique si no debe cambiar la contraseña\n'.format(user))
            continue
    driver.quit()
    
    floatLiqNet = [float(i) for i in neto_liq]
    if sum(floatLiqNet) == 0 :
        print('No se registraron ventas al día de la fecha seleccionada.')
        file.write('No se registraron ventas al día de la fecha seleccionada.\n')
    else :
        print('La suma total es:{}'.format(sum(floatLiqNet)))
        file.write('La suma total es:{}'.format(sum(floatLiqNet)))
    
    file.close()


