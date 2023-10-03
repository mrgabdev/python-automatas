name = input("Ingresa tu nombre completo\n")

nameParts = name.split(" ")
capitalizeNameParts = []

for part in nameParts:
    capitalizeNameParts.append(part.capitalize())

capitalizeName = " ".join(capitalizeNameParts)

print(capitalizeName)
