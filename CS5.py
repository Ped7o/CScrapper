from datetime import date
import json
from CScraper import DataCollect
from send import ReportSender
from jedit import PwUpdater
import os
 
f = json.load(open('prueba.json', 'r', encoding='utf-8'))
os.system('clear')

print('Bienvenido al recopilador de datos de Cabal!')
while True :
    menu_sel = int(input('''

1) LIQUIDACIONES DIARIAS
2) CAMBIO DE CONTRASEÑAS

Su selección: '''))

    if menu_sel == 1 :
        os.system('clear')
        user_sel = int(input('''

Seleccione un usuario:

1) PATRICIA
2) SANDRA
3) MARTIN

4) VOLVER

Su selección: ''')) - 1
        if user_sel < 3 :
            user_name = f['empleado'][user_sel]['name']
            cred_to_load = f['empleado'][user_sel]['credentials']
            day = input('Ingrese fecha (DDMMAAAA): ')
            DataCollect(cred_to_load, day, user_name)
            #ReportSender(user_name, day)
            input('\nPresione Enter para continuar...')

        elif user_sel == 3 :
            os.system('clear')
            pass

        else :
            print('Opción inválida. Reintente nuevamente.\n')
    
    elif menu_sel == 2 :
        while True :
            os.system('clear')
            opt_sel = int(input('''

Seleccione un usuario:

1) PATRICIA
2) SANDRA
3) MARTIN

4) VOLVER

Su selección: ''')) - 1

            if opt_sel < 3 :
                PwUpdater(opt_sel)
             
            elif opt_sel == 3 :
                os.system('clear')
                break

            else :
                print('Opción inválida. Reintente nuevamente.')
