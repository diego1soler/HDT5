# Universidad del Valle de Guatemala
# Diego Soler 15415
# Edgar Ramirez 15236
# HDT 5
# Este codigo esta basado en ejemplos anteriores y de ejemplos en clase


import simpy
import random


def proceso(sv, tiepro, nom, ram, cant_memoria, n_ins, velocidad):

    #Variables para llevar el conteo del tiempo de cada proceso
    global t_tot
    global tiemp

    #ETAPA NEW
    #El proceso llega al sistema operativo pero debe esperar que se le asigne memoria RAM
    yield sv.timeout(tiepro)
    print('%s solicita %d de RAM (new)' % ( nom, cant_memoria))
    tiemp_llegada = sv.now 
    
    #ETAPA READY
    #Se solicita la RAM
    yield ram.get(cant_memoria)
    print('%s. Solicitud aceptada por %d de RAM (admited)' % ( nom, cant_memoria))

    #En esta parte se almacenara el num de instrucciones terminadas
    ins_comp = 0
    
    while ins_comp < n_ins:

    
        #conexion CPU
        with cpu.request() as req:
            yield req
            #instruccion a realizarse
            if (n_ins-ins_comp)>=velocidad:
                efec=velocidad
            else:
                efec=(n_ins-ins_comp)

            print('%s CPU ejecutara %d instrucciones. (ready)' % (nom, efec))
            #tiempo de instrucciones a ejecutar
            yield sv.timeout(efec/velocidad)   

            #numero total de intrucciones terminadas
            ins_comp += efec
            print('%s CPU (%d/%d) completado. (running)' % ( nom, ins_comp, n_ins))

        #Si la decision es 1 wait, si es 2 procedemos a ready
        desicion = random.randint(1,2)

        if desicion == 1 and ins_comp<n_ins:
            #(waiting)
            with wait.request() as req2:
                yield req2
                yield sv.timeout(1)                
                print('%s. Realizadas operaciones de entrada/salida. (waiting)' % ( nom))
    

    #ETAPA TERMINATED
    #Cantidad de RAM
    yield ram.put(cant_memoria)
    print('%s retorna %d de RAM. (terminated)' % (nom, cant_memoria))
    #total de tiempo
    t_tot += (sv.now - tiemp_llegada)
    #se guarda tiempo
    tiemp.append(sv.now - tiemp_llegada) 


#DEFINICION DE VARIABLES

#Instrucciones por tiempo, cantidad de RAM, cantidad de procesos, tiempo total, y array de tiempos
velocidad = 3.0 
memoria_ram= 100
n_pro = 50 
t_tot=0.0
tiemp=[] 


# AMBIENTES DE SIMULACION   
sv = simpy.Environment() 
cpu = simpy.Resource (sv, capacity=2) #Cola de tipo Resource para el CPU 
ram = simpy.Container(sv, init=memoria_ram, capacity=memoria_ram) #Cola de tipo Container para la RAM
wait = simpy.Resource (sv, capacity=2) #Wait para operaciones I/O

#Semilla del random
n_intervalo = 10 #numero de intervalos (que va variando)
random.seed(2411)



# Se creean los procesos a simular
for i in range(n_pro):
    tiepro = random.expovariate(1.0 / n_intervalo)
    n_ins = random.randint(1,10)
    cant_memoria = random.randint(1,10) #Se genera una cantidad aleatoria de memoria
    sv.process(proceso(sv, tiepro, 'Proceso %d' % i, ram, cant_memoria, n_ins, velocidad))

#Se corre la simulacion
sv.run()

#Tiempo promedio por procesos
print " "
prom=(t_tot/n_pro)
print('El tiempo promedio de los procesos es: %f (en segundos)' % (prom))


#SE CALCULA LA DESVIACION ESTANDAR
sumatoria=0

for cont in tiemp:
    sumatoria+=(cont-prom)**2

desviacions=(sumatoria/(n_pro-1))**0.5

print " "
print('La desviacion estandar de los tiempos de los procesos es: %f (en segundos)' %(desviacions))
