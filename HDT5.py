#Algoritmos y Estructuras de Datos
#Hoja de Trabajo 5
#Integrantes:  Diego Soler  y  Edgar Ramirez
#21/08/16


#Se importa lo necesario
import simpy
import random



#def proceso(env, tproceso, name, ram, cant_ram, cant_inst, numInst):
    
   
#    VARIABLES: numero de procesos (se cambia en cada caso), cantidad de RAM e inst/tiempo

numprocesos = 100
RandomAccesMemory=100
numInst = 3.o


env = simpy.Environment()  #crear ambiente de simulacion
cpu = simpy.Resource (env, capacity=1) #Cola para acceder a CPU
ram = simpy.Container(env, init=RandomAccesMemory, capacity=RandomAccesMemory) #Simulador de RAM tipo Container
wait = simpy.Resource (env, capacity=1) #Cola de operaciones I/O


# comienza la simulacion
env.run()
