#!/usr/bin/python2
# -*- coding: utf-8 -*-

import re

def entrada_de_ip():
    entrada = raw_input("Introduce la dirección de red: ")
    matchIp = re.search( r'(([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3}))(\/){0,1}([0-9]{1,2}){0,1}', entrada )
    if matchIp:
        ip_principal = map(int, list(matchIp.group(2,3,4,5)))
        for x in ip_principal:
            if x > 255 or x < 0:
                print "ip incorrecta!!"
                entrada_de_ip()
        if matchIp.group(7):
            mascara = int(matchIp.group(7))
            if mascara > 32 or mascara < 0:
                print "máscara incorrecta"
                entrada_de_ip()
        else:
            mascara = pedir_mascara()
    else:
        print "Dirección ip inválida!"
        entrada_de_ip()
    return ip_principal, mascara

def pedir_mascara():
    entrada_mascara = raw_input("Introduce la máscara de red: ")
    matchMask = re.search( r'(([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3}))', entrada_mascara )
    if not matchMask:
        print "La máscara introducida no es válida"
        pedir_mascara()
    else:
        mascara = map(int, list(matchMask.group(2,3,4,5)))
        for x in mascara:
            if x > 255 or x < 0:
                print "máscara incorrecta!!"
                pedir_mascara()
    return mascara

def convertir(ip_address):
    ip_address_binario = []
    for x in ip_address:
        temporal = ""
        for y in range(7,-1,-1):
            if x >= 2**y:
                temporal = temporal + "1"
                x = x - 2**y
            else:
                temporal = temporal + "0"
        ip_address_binario.append( temporal )
    return ip_address_binario

def convertir_mascara(mascara):
    if type(mascara) == int:
        mascara_binario = ["", "", "", ""]
        for x in range(4):
            for y in range(8):
                if mascara > 0:
                    mascara_binario[x] = mascara_binario[x] + "1"
                    mascara -= 1
                else:
                    mascara_binario[x] = mascara_binario[x] + "0"
    else:
        mascara_binario = convertir(mascara)
    return mascara_binario

ip_principal, mascara = entrada_de_ip()
ip_principal_binario = convertir(ip_principal)
print ip_principal_binario
mascara_binario = convertir_mascara(mascara)
print mascara_binario
