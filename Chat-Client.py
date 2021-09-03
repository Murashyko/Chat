from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive(): #Reception du message
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8") #Décodage
            msg_list.insert(tkinter.END, msg) #Insertion du message dans la listbox

        except OSError:  #Si le client a quitter le chat
            break

def send(event=None):  #Gestion de l'envoi des messages
    msg = my_msg.get()
    my_msg.set("")  # Nettoyage de la variable pour accueillir le prochain message
    client_socket.send(bytes(msg, "utf8")) #Envoie du message au serveur
    if msg == "/quit":
        client_socket.close() #Fermeture du socket
        top.quit() #Fermeture de la fenêtre

def on_closing(event=None): #Gère la fermeture de la fenêtre par la croix
    my_msg.set("/quit")
    send()



#Interface grpahique
top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # Pour envoyer les messages
my_msg.set("Taper ici.")
scrollbar = tkinter.Scrollbar(messages_frame)  #Pour naviguer dans les anciens messages

#La suite contient les messages

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Envoyer", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing) #Fermeture de la fenêtre par la croix

#----Les sockets----

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # lance l'interface graphique