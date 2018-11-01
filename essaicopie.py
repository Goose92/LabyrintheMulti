import copy

print("bonjour")
Tableau1=[1,2,3]
print(Tableau1)

Tableau2=copy.copy(Tableau1)
print(Tableau2)

print("*****")
Tableau1[1]=5
print(Tableau1)
print(Tableau2)


