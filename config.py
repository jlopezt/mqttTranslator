import json

OK                          =  0
CONFIGURACION_POR_DEFECTO   = -1
ERROR_FICHERO_CONFIGURACION = -2
INICIAL                     = -100

class Configuracion:
    __Broker_IP = 0
    __Broker_Puerto = 0
    __sub_topic = 0
    __pub_topic = 0
    __MQTTUser = ''
    __MQTTPassword = ''
    __configurado = INICIAL

    def __init__(self, fichero, debug = False, Broker_IP = "0.0.0.0",Broker_Puerto = "0",sub_topic = '',pub_topic = '',    __MQTTuser = '',__MQTTpassword = ''):
        #valores por defecto sobre el bus MQTT
        __Broker_IP = Broker_IP
        __Broker_Puerto = Broker_Puerto
        __sub_topic = sub_topic
        __pub_topic = pub_topic
        __MQTTUser = ''
        __MQTTPassword = ''
    
        self.__leeConfiguracion(fichero,debug)

    def __leeConfiguracion(self,fichero,debug=False):
        if (debug==True): print("\nInicio de configuracion----------------------------------------------------------------------")
        self.__configurado = OK #por defecto va bien...

        try:
            #leo el fichero de configuracion
            with open(fichero) as json_file:
                configuracion = json.load(json_file)
                if (debug==True): print("Configuracion leida=\n %s" %configuracion)
        except :
            if (debug==True): print("No se pudo obtener el fichero de configuracion")
            self.__configurado = ERROR_FICHERO_CONFIGURACION
            return

        if 'MQTT' in configuracion: 
            MQTTConfig = configuracion['MQTT']

            if 'Broker_IP' in MQTTConfig: self.setBroker_IP(MQTTConfig.pop("Broker_IP"))
            else: 
                if (debug==True): 
                    print("Broker_IP no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if 'Broker_Puerto' in MQTTConfig: self.setBroker_Puerto(MQTTConfig.pop("Broker_Puerto"))
            else: 
                if (debug==True): 
                    print("Broker_Puerto no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if 'sub_topic' in MQTTConfig: self.setsub_topic(MQTTConfig.pop("sub_topic"))
            else: 
                if (debug==True): 
                    print("sub_topic no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if 'pub_topic' in MQTTConfig: self.setpub_topic(MQTTConfig.pop("pub_topic"))
            else: 
                if (debug==True): 
                    print("pub_topic no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO
                    
            if 'MQTTUser' in MQTTConfig: self.setMQTTUser(MQTTConfig.pop("MQTTUser"))
            else: 
                if (debug==True): 
                    print("MQTTUser no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if 'MQTTPassword' in MQTTConfig: self.setMQTTPassword(MQTTConfig.pop("MQTTPassword"))
            else: 
                if (debug==True): 
                    print("MQTTPassword no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO
        else: 
            if (debug==True): 
                print("No se ha configurado MQTT. Valores pore defecto")
                self.__configurado = CONFIGURACION_POR_DEFECTO

        if (debug==True): print("Configuracion de MQTT")
        if (debug==True): print("Broker_IP = %s" %self.__Broker_IP)
        if (debug==True): print("Broker_Puerto = %s" %self.__Broker_Puerto)
        if (debug==True): print("sub_topic = %s" %self.__sub_topic)
        if (debug==True): print("pub_topic = %s" %self.__pub_topic)
        if (debug==True): print("MQTTUser = %s" %self.__MQTTUser)
        if (debug==True): print("MQTTPassword = %s" %self.__MQTTPassword)

    def setBroker_IP(self,valor): self.__Broker_IP=str(valor)
    def setBroker_Puerto(self,valor): self.__Broker_Puerto=valor
    def setsub_topic(self,valor): self.__sub_topic=str(valor)
    def setpub_topic(self,valor): self.__pub_topic=str(valor)
    def setMQTTUser(self,valor): self.__MQTTUser=str(valor)
    def setMQTTPassword(self,valor): self.__MQTTPassword=str(valor)

    def getBroker_IP(self): return self.__Broker_IP
    def getBroker_Puerto(self): return self.__Broker_Puerto
    def getsub_topic(self): return self.__sub_topic
    def getpub_topic(self): return self.__pub_topic
    def getMQTTUser(self): return self.__MQTTUser
    def getMQTTPassword(self): return self.__MQTTPassword

    def getConfigurado(self): return self.__configurado

#c=Configuracion('MQTT_log.config.json',True)
#print("la salida es %i\n" %c.getConfigurado())