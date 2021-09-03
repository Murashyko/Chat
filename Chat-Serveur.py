import sqlite3
from sqlite3 import Error
from pathlib import Path
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}
nom =[]

HOST = "127.0.0.1" #Adresse ip du serveur
PORT = 9876
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM) #Définition de la famile du socket et son type
SERVER.bind(ADDR)

print(f"Le serveur 'Chat de Geek' {HOST} est a l'écoute sur le port {PORT}")

def init(base):
    # Tester si la base de donnée existe
    fichierdb = Path(base)
    if not fichierdb.is_file():
        creationdb(base)

    try:
        db = sqlite3.connect(base)
        cur = db.cursor()
        return db, cur
    except Error as e:
        print(e)
    return None

def creationdb(base):
    global cur
    global db
    # récupére le curseur
    db = sqlite3.connect(base)
    cur = db.cursor()

    # création d'une table
    cur.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, nom TEXT)")
    db.commit()def connection():

    while True: #Boucle infinit qui reçoit le client
        client, client_address = SERVER.accept() #Le client est accepté par le serveur
        print("%s:%s est connecté." % client_address)
        client.send(bytes("Bienvenue chez les Geek ! Entrer votre pseudo.", "utf8"))
        addresses[client] = client_address #Ajout du client à la liste
        Thread(target=handle, args=(client,)).start()
        #Thread pour que le serveur puisse gérer séparément la fonction connection et la fanction handle en ciblant cette dernière et en lui donnant l’argument client

def handle(client,db,cur):
    name = client.recv(BUFSIZ).decode("utf8") #Récupération du pseudo

    # gestion des pseudos pour éviter les doublons connecter en même temps
    cur.execute("SELECT pseudo FROM user")
    tes = print(nom.find(name))
    pseud = cur.fetchall()
    test = print(pseud.find(name))
    if (test == -1) and (tes == -1):
        cur.execute("INSERT INTO user (pseudo) VALUES(?)", (nom))
        nom.append(name)
    elif (test != -1) and (tes == -1):
        nom.append(name)
    else:
        pris = "Ce pseudo est déjà pris ! Prenez en un autre en relançant l'application."
        client.send(bytes(pris, "utf8"))
        name = client.recv(BUFSIZ).decode("utf8")
        msg = bytes("/quit", "utf8")
        broadcast(bytes(msg, "utf8"))

    welcome = 'Salut %s! Si tu veux partir, tape /quit et pour savoir qui est la : /list.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s a rejoint les Geek !" % name
    list(client) #Affiche les utilisateurs connectés quand le client rejoint le chat
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ) # Reception du message envoyé par le client
        if msg == bytes("/quit", "utf8"): #Gestion des commandes /quit et /list
            client.send(bytes("/quit", "utf8"))
            nom.remove(name) # Fermeture et nettoyage des listes
            client.close()
            del clients[client]
            broadcast(bytes("%s a quitter les Geek" % name, "utf8"))
            break
        elif msg == bytes("/list", "utf8"):
            list(client)
        else:
            broadcast(msg, name + ": ")

def list(client): #Fonction du /list
    for pseudo in nom:
        client.send(bytes(f"Les Geek en ligne : {pseudo}", "utf8"))

def broadcast(msg, prefix=""): #Envoie les messages a tous les clients connectés
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

if __name__ == "__main__":
    init("Base")
    SERVER.listen(5)
    print("En attente d'une conncexion...")
    ACCEPT_THREAD = Thread(target=connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
