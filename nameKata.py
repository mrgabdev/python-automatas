"""
'SON LAS 7 DE LA NOCHE Y YA ME QUIERO IR'
SI ENCUENTRA EL NUMERO 7 Y ES MENOR A 8
IMPRIMIR EL NUMERO 7 CONVERTIDO A INT 
Y EL TEXTO, ' ES HORA DE IRNOS SON LAS : '7'
"""

text = "SON LAS 7 DE LA NOCHE Y YA ME QUIERO IR"
outputText = "ES HORA DE IRNOS SON LAS :"

hasSeven = "7" in text

if hasSeven:
    number = int(text[8])
    if number < 8:
        print(f"{outputText} {number}")
    else:
        print(f"{outputText} 8")
