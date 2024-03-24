import pygame 
import socket
import pickle
from _thread import*
import sys

server=socket.gethostbyname(socket.gethostname())
port=5555

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for Connection , Server Started")

prompts={
    1:{
        1:"press 1",
        id:"p1"
    },
    2:{
        1:"press 2",
        id:"p2"
    }
}
current_Prompt=1

players=[False,False]

def updateStatus(p):
    players[p]=True

def showstatus():
    if players[0]==False or players[1]==False:
        return False
    else:
        return True
    
def checkPromptStatus(data,p):
    if data=="p1" and p==0 and prompts[p+1][id]=="p1":
        return True
    elif data=="p2" and p==1 and prompts[p+1][id]=="p2":
        return True
    else:
        return False

def resetStatus(a):
    players[a]=False

def threaded_client(conn,current_Prompt,p):
    p%=2
    conn.send(pickle.dumps(prompts[current_Prompt][1]))
    while True:
        try:
            data=conn.recv(4096*2).decode()
            if not data :
                break
            
            elif data=='pos':
                updateStatus(p)
                conn.send(pickle.dumps(p))

            elif data=="Connect":
                a=showstatus()
                conn.send(pickle.dumps(a))

            elif data=="current prompt":
                conn.send(pickle.dumps(prompts[current_Prompt][1]))

            else:
                if checkPromptStatus(data,p):
                    current_Prompt+=1
                    conn.sendall(pickle.dumps(prompts[current_Prompt][1]))
                else:
                    conn.sendall(pickle.dumps(prompts[current_Prompt][1]))
                if current_Prompt>len(prompts):
                    current_Prompt=1
        except:
            break
    print("Connection Lost")
    resetStatus(p)
    p-=1  
    if p>=2:
        p=-1
    conn.close()


p=-1
while True:

    conn,addr=s.accept()
    p+=1
    print("connected to ",addr)
    
    start_new_thread(threaded_client,(conn,current_Prompt,p))