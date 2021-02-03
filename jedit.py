import json
import os
file = open('prueba.json', 'r')
json_f = json.load(file)
file.close()

def PwUpdater(usel) :
    nmbr = 1
    os.system('clear')
    for cred in json_f['empleado'][usel]['credentials'] :
        print('{})'.format(nmbr), cred['user'])
        nmbr += 1
    
    print('\n0) VOLVER\n')
    user = int(input('Su selección: ')) -1
    if user == -1 :
        pass
    else :
        json_f['empleado'][usel]['credentials'][user]['pw'] = input('Ingrese nueva contraseña: ')
    
        file = open('prueba.json', 'w')
        json.dump(json_f, file)
        file.close()

