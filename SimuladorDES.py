# Universidad del Valle de Guatemala
# Diego Soler 15415
# Edgar Ramirez 15236
# HDT 5
# Este codigo esta basado en ejemplos anteriores y de ejemplos en clase


import simpy
import random


def proceso(sv, tiepro, nom, ram, cant_memoria, n_ins, velocidad):
    global t_tot
    global tiemp

    #New
    #el proceso llega al sistema operativo pero debe esperar que se le asigne memoria RAM
    yield sv.timeout(tiepro)
    print('tiempo: %f - %s (new) solicita %d de memoria ram' % (sv.now, nom, cant_memoria))
    tiemp_llegada = sv.now 
    
    #ready
    # se pide laRam
    yield ram.get(cant_memoria)
    print('tiempo: %f - %s (admited) solicitud aceptada por %d de memoria ram' % (sv.now, nom, cant_memoria))

    #en esta parte se almacenara el num de instruc termindadas
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

            print('tiempo: %f - %s (ready) cpu ejecutara %d instrucciones' % (sv.now, nom, efec))
            #tiempo de instrucciones a ejecutar
            yield sv.timeout(efec/velocidad)   

            #numero total de intrucciones terminadas
            ins_comp += efec
            print('tiempo: %f - %s (runing) cpu (%d/%d) completado' % (sv.now, nom, ins_comp, n_ins))

        #Si la decision es 1 wait, si es 2 se va a ready
        desicion = random.randint(1,2)

        if desicion == 1 and ins_comp<n_ins:
            #(waiting)
            with wait.request() as req2:
                yield req2
                yield sv.timeout(1)                
                print('tiempo: %f - %s (waiting) realizadas operaciones (entrada/salida)' % (sv.now, nom))
    

    # terminated
    #cantidad de ram
    yield ram.put(cant_memoria)
    print('tiempo: %f - %s (terminated), retorna %d de memoria ram' % (sv.now, nom, cant_memoria))
    #total de tiempo
    t_tot += (sv.now - tiemp_llegada)
    #se guarda tiempo
    tiemp.append(sv.now - tiemp_llegada) 


#DEFINICION DE VARIABLES
velocidad = 3.0 # cantidad de instrucciones/tiempo
memoria_ram= 100 #se define cantidad de memoria ram
n_pro = 25 # cantidad de procesos a ejecutar
t_tot=0.0 #inicializa la variable que almacenara el tiempo total de los procesos
tiemp=[] #se guardara cada tiempo individual para extraer la desviacion estandar


sv = simpy.Environment() 
cpu = simpy.Resource (sv, capacity=2) 
ram = simpy.Container(sv, init=memoria_ram, capacity=memoria_ram)
wait = simpy.Resource (sv, capacity=2)

#semilla para random 
random.seed(2411)
n_intervalo = 1 #numero de intervalos


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
print('El tiempo promeido es: %f' % (prom))


#Desviaccion estandar
sumatoria=0

for xi in tiemp:
    sumatoria+=(xi-prom)**2

desviacions=(sumatoria/(n_pro-1))**0.5

print " "
print('La desviacion estandar es: %f' %(desviacions))
