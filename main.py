#!/usr/bin/env python3
import sys, getopt
import time
import os

import datetime
import logging

import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import config
#Chapuza a corregir
OK						  =  0
CONFIGURACION_POR_DEFECTO   = -1
ERROR_FICHERO_CONFIGURACION = -2

# Informacion sobre el bus MQTT
'''
Broker = "10.68.0.100"
sub_topic = "zigbee2mqtt/+"    # receive messages on this topic
pub_topic = "casaPre/"   # send messages to this topic
'''

###########   MAIN   #################
def main(argv):
    configFile = ''
    outputFile = ''
    verbose = False
    pantalla = False

    try:
        opts, arg = getopt.getopt(argv,"phvc:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('mainpy [-p -v -c <configfile> -o <outputfile> | -h]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('')
            print ('MQTT_log.py -c <configFile> -o <outputfile> -h -v')
            print ('-c <configFile> fichero de configuracion')
            print ('-o <outputFile> fichero de salida. Si no existe se creara, si existe se anadiran lineas al final')
            print ('-h esta ayuda')
            print ('-v verbose mode')
            print ('-p salida por pantalla')			
            print ('')
            sys.exit()
        elif opt == "-v":
            verbose = True
        elif opt == "-p":
            pantalla = True
        elif opt =="-c":
            configFile = arg
            if configFile[0:1]==' ': configFile=configFile[1:]
        elif opt == "-o":
            outputFile = arg
            if outputFile[0:1]==' ': outputFile=outputFile[1:]
    print('Iniciando con fichero de configuracion [%s]' %configFile)
    print('Salida direccionda a [%s]' %outputFile)

    #leo la configuracion
    localConfig=config.Configuracion(configFile, verbose)
    if (localConfig.getConfigurado()==ERROR_FICHERO_CONFIGURACION): 
        print("No se pudo leer el fichero de configuracion")
        sys.exit()
    elif (localConfig.getConfigurado()==CONFIGURACION_POR_DEFECTO): 
        print("Faltan parametros en el fichero de configuracion")
        sys.exit()	

    #inicializo el fichero de salida
    #print("Configurando fichero de salida")
    #if (outputFile == ''): verbose==True
    #else:
    #	try:
    #		f = open (outputFile,"at")
    #	except:
    #		print("Error al abrir el fichero de salida")
    #		sys.exit()		

    print("Iniciando MQTT Translator")
    ########################################################################################	
    # mqtt section
    # when connecting to mqtt do this;
    def on_connect(client, userdata, flags, rc):
        print("Conectado al bus con el codigo de resultado "+str(rc))
        client.subscribe(localConfig.getsub_topic())
        #publish_mqtt("Conectrado al bus...")

    # when receiving a mqtt message do this;
    def on_message(client, userdata, msg):
        verbose=False
        if (verbose): print("\nInit -----------------------------------------------------")
        try:
            if (verbose): print("recibido= %s %s" %(msg.topic,msg.payload))
            decoded = json.loads(msg.payload)
        except:
            print("error al parsear el mensaje recibido= %s %s" %(msg.topic,msg.payload))
            return
            
        current_time = datetime.datetime.utcnow().isoformat()
        if (verbose): 
            print("Timestamp= "+current_time)
            print(decoded)

        envio=False
        json_salida={
            "titulo": "Termometro",
            "id": "",
            "habitacion": "",
            "Temperatura": "19.8",
            "Humedad": "63.9",
            "Luz": "0.0",
            "Altitud": "-100.0",
            "Presion": "-100.0",
            "TemepraturaSuelo": "-100.0",
            "HumedadSuelo": "-100.0"
            }

        if 'temperature' in decoded:
            print(f"Temperatura= {decoded['temperature']}")
            json_salida['Temperatura']=decoded['temperature']
            envio=True
        if 'humidity' in decoded:
            print(f"Humedad= {decoded['humidity']}")
            json_salida['Humedad']=decoded['humidity']
            envio=True
        if 'luz' in decoded:
            print("Luz= "+decoded["Luz"])
            json_salida['Luz']=decoded['luz']
            envio=True
        
        if envio:
            nombreOrigen = msg.topic.split("/")[1]
            if '_' in nombreOrigen:
                json_salida['id']=nombreOrigen.split("_")[1]#nombreOrigen[:-1]
                json_salida['habitacion']=nombreOrigen.split("_")[0]#nombreOrigen[:-1]
                publish_mqtt(localConfig.getpub_topic()+json_salida['habitacion']+'/medidas',json.dumps(json_salida),retain=True)
        else:
            #publish_mqtt(pub_topic+'nada/medidas','Nada que decir...')
            pass
            
    # to send a message
    def publish_mqtt(topic,mensaje,qos=0,retain=False):
        '''
        mqttc = mqtt.Client("mqttTranslator")
        mqttc.connect(Broker, 1883)
        print(f'publico en el topico {pub_topic} el mensaje {mensaje}')
        mqttc.publish(pub_topic, mensaje)
        #mqttc.loop(2) //timeout = 2s
        '''
        print(f'publico en el topico {topic} el mensaje {mensaje} con QoS {qos} y retain {retain}')
        ret=client.publish(topic,mensaje,qos=qos,retain=retain)
        print(f'con el resultado {ret.rc}')
        
    def on_publish(mosq, obj, mid):
        print("mid: " + str(mid))
    ########################################################################################

    #iniciando MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(localConfig.getMQTTUser(), localConfig.getMQTTPassword())
    client.connect(localConfig.getBroker_IP(), localConfig.getBroker_Puerto(), 60)
    
    print("Iniciando ejecucion...")

    client.loop_forever()

if __name__ == "__main__":
	main(sys.argv[1:])