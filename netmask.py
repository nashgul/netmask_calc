#!/usr/bin/python2
# -*- coding: utf-8 -*-

import re,sys 

def entrada_ip():
    ip_principal = ()
    while not ip_principal:
        entrada = raw_input("Introduce la dirección de red: ")
        matchIp = re.match( r'\b(([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3}))\b(\/([0-9]{1,2})){0,1}', entrada )
        if matchIp:
            ip_principal = map(int, list(matchIp.group(2,3,4,5)))
        else:
            print("Dirección ip inválida")
    for x in ip_principal:
        if x > 255 or x < 0:
            print("Valor %d incorrecto!!" % x)
            entrada_ip()
    if matchIp.group(7):
        mascara = int(matchIp.group(7))
        if mascara > 32 or mascara < 0:
            print("valor CIDR: %d incorrecto" % mascara)
            entrada_ip()
        else:
            global CIDR
            CIDR = mascara
    return ip_principal

def pedir_mascara():
    matchMask = ()
    while not matchMask:
        entrada_mascara = raw_input("Introduce la máscara de red: ")
        matchMask = re.search( r'\b(([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3}))\b', entrada_mascara )
        if not matchMask:
            print("La máscara introducida no es válida")    
    mascara = map(int, list(matchMask.group(2,3,4,5)))
    for x in mascara:
        if x > 255 or x < 0:
            print("valor %s incorrecto!!" % x)
            pedir_mascara()
    return mascara

def convertir_a_binario(ip_address):
    ip_address_binario = []
    for x in ip_address:
        ip_address_binario.append("{0:08b}".format(x))
    return ip_address_binario

def convertir_a_decimal(ip_address):
    ip_address_decimal = []
    for x in ip_address:
        ip_address_decimal.append(int(x, 2))
    return ip_address_decimal

def bits_de_red(mascara):
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
        mascara_binario = convertir_a_binario(mascara)
    return mascara_binario

def subred_bin():
# ip y máscara en binario
# calcula el minimo y máximo valor de red en binario y decimal
    a = ""
    ip_addresses_bin.append([""]*4)
    ip_addresses_bin.append([""]*4)
    for x in range(4):
        for y in range(8):
            if ip_addresses_bin[1][x][y] == "1":
                valor = (ip_addresses_bin[2][x], ip_addresses_bin[0][x][y])
                ip_addresses_bin[2][x] = a.join(valor) 
            else:
                ip_addresses_bin[3][x] = ip_addresses_bin[2][x]
                for z in range(0,8-y):
                    valor_0 = (ip_addresses_bin[2][x], "0")
                    ip_addresses_bin[2][x] = a.join(valor_0)
                    valor_1 = (ip_addresses_bin[3][x], "1")
                    ip_addresses_bin[3][x] = a.join(valor_1)
                break
            ip_addresses_bin[3][x] = ip_addresses_bin[2][x]

###Inicio del script
####################

# 1: main ip, 2: mask, 3: subnet ip min, 4: subnet ip max
ip_addresses = []
# 1: main ip, 2: mask, 3: subnet ip min, 4: subnet ip max
ip_addresses_bin = []
CIDR = None

if not sys.argv[1:]:
    print("Introduce la ip principal en notación CIDR, o sólo la ip principal,")
    print("y luego se pedirá la máscara en forma notación decimal puntuada")
    ip_addresses.append(entrada_ip())
    ip_addresses_bin.append(convertir_a_binario(ip_addresses[0]))
    if not CIDR:
        ip_addresses.append(pedir_mascara())
        ip_addresses_bin.append(bits_de_red(ip_addresses[1]))
    else:
        ip_addresses_bin.append(bits_de_red(CIDR))
        ip_addresses.append(convertir_a_decimal(ip_addresses_bin[1]))
#le paso la ip principal y la máscara en binario
    subred_bin()

print("")
print("ip principal:\t\t{0:03d}.{1:03d}.{1:03d}.{1:03d}".format(ip_addresses[0][0],ip_addresses[0][1],ip_addresses[0][2],ip_addresses[0][3]))
print("máscara de red: \t{0:3d}.{1:3d}.{2:3d}.{3:3d}".format(ip_addresses[1][0],ip_addresses[1][1],ip_addresses[1][2],ip_addresses[1][3]))
print("rt: ", ip_addresses_bin)
