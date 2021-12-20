import sys
import MySQLdb
import time
import re
import os

class bcolors:
	OK = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	RESET = '\033[0m'

if len(sys.argv) == 1:
	print(bcolors.FAIL+"[!] "+bcolors.RESET+ "Veuillez entrer une liste en argument pour commencer l'attaque")
	exit()

path = os.getcwd()
wordfile = sys.argv[1]

print(bcolors.OK+"[+] "+bcolors.RESET+"Attaque commencée avec la liste {}".format(wordfile))
StartTime=time.time() #On prend le temps à t=0s

with open(wordfile, "r") as wordlist: #On ouvre le fichier choisit en tant que liste
 
	for password in wordlist: #On test toutes les mots de la liste
		try:
			print("mot de passe:",password)
			passwd=password.splitlines() #On supprime les retours chariot
			str = ' '.join(passwd) #On remet le mot sous forme de chaîne de caractère
			MySQLdb.connect(host= "localhost", user="root", passwd=str) 
			print(bcolors.OK+"[+] "+bcolors.RESET+"login successful")
			EndTime=time.time() #On prend le temps au moment où on a trouvé le mot de passe
			TotalTime=(EndTime-StartTime) #On fait la différence pour avoir le temps de recherche
			print(bcolors.OK+"[+] "+bcolors.RESET+"Mot de passe trouvé en:", TotalTime,"sec")
			LogFile=open("time.log", "w") #On ouvre un noveau fichier time.log pour y deposer la valeur trouvée
			#LogFile.write(str(TotalTime))
			LogFile.close()
			print(bcolors.OK+"[+] "+bcolors.RESET+"Fichier log enregistré dans"+ path+"/time.log")

			points=0
			
			if len(password) > 8: #Si la longueur du mdp est superieur a 8 caracteres on accorde 1 point
				points=points+1
			if re.search("[a-z]", password): #Si on a des lettres de l'alphabet dans le mdp on accorde 1 point
        			points=points+1
			if re.search("[A-Z]", password): #Si on a des majuscules dans le mdp on accorde 1 point
				points=points+1
			if re.search("[0-9]", password): #Si on a des chiffres dans le mdp on accorde 1 point
				points=points+1
			if re.search("[_@$]", password): #Si on a des caracteres speciaux dans le mdp on accorde 1 point
				points=points+1
			if points == 5:
				print(bcolors.OK+"[+] "+bcolors.RESET+"Le mot de passe trouvé a obtenu la note de", points,"/5 au test de robustesse")
			if points < 5 and points >=3:
				print(bcolors.WARNING+"[-] "+bcolors.RESET+"Le mot de passe trouvé a obtenu la note de", points,"/5 au test de robustesse")
			if points < 3:
				print(bcolors.FAIL+"[!] "+bcolors.RESET+"Le mot de passe trouvé a obtenu la note de", points,"/5 au test de robustesse")

			exit()
		except Exception as e: #Impression des erreurs
			errno, message = e.args
			if errno == 1045: #Si on reçoit le code d'erreur 1045 notre mot de passe n'est pas le bon donc on ecrit login failed
				print(bcolors.FAIL+"[!] "+bcolors.RESET+"Login failed!")
			elif errno == 1130: #Si on reçoit le code d'erreur 1130 notre hôte n'est pas autorisée et on note connection refused
				print(bcolors.FAIL+"[!] "+bcolors.RESET+"Connection refused")
			elif errno == 2002: #Si on reçoit le code d'erreur 2002 la connexion au serveur local ne peut pas être effectuée
				print(bcolors.FAIL+"[!] "+bcolors.RESET+"impossible de se connecter au serveur MySQL local via le socket '/var/run/mysqld/mysqld")			
			elif errno == 2005: #Si on reçoit le code d'erreur 2005 le nom de l'hôte n'est pas bon 
				print(bcolors.FAIL+"[!] "+bcolors.RESET+"Unknown server host")
			elif errno == 2013: #Si on reçoit le code d'erreur 2013 la connexion a été perdue
				print(bcolors.FAIL+"[!] "+bcolors.RESET+"connection lost")
			else: #Sinon
				print(bcolors.FAIL+"[!] "+bcolors.RESET+"une erreur inconnue c'est produite")

print(bcolors.WARNING+"[!] "+bcolors.RESET+"le mot de passe n'a pas été trouvé.") #Si le mot de passe n'a pas été trouvé au bout de la recherche on note que le mot de passe n'a pas été trop
