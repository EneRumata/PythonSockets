import socket
from threading import Thread
import json

               ## self.players.append({"addr":addr,"x":400,"y":300,})
##HOST, PORT = 'localhost', 8080 # Адрес сервера
print("input host adress (it uses localhost if left empty)")
HOST = input()# Адрес сервера
HOST = "localhost" if HOST=="" else HOST
print("input host port (it uses 8080 if left empty)")
PORT = input()# Порт сервера
PORT = 8080 if PORT=="" else int(PORT)

MAX_PLAYERS = 4 # Максимальное кол-во подключений

class Server:

    def __init__(self, addr, max_conn):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr) # запускаем сервер от заданного адреса

        self.max_players = max_conn
        self.players = [] # создаем массив данных игроков на сервере
        
        self.sock.listen(self.max_players) # устанавливаем максимальное кол-во прослушиваний на сервере
        self.listen() # вызываем цикл, который отслеживает подключения к серверу

    class ClientThreadPack:
        def __init__(self, player_parent_players, player_conn, player_addr, player_x, player_y, player_id):
            self.players = player_parent_players
            self.conn = player_conn
            self.addr = player_addr
            self.x = player_x
            self.y = player_y
            self.id = player_id
            self.waiting = 0
            self.data = 0
            
            self.thread = Thread(target=self.handleClientThreadPack, args=(self.conn,)).start() # Запускаем в новом потоке проверку действий игрока

        def jsonFixError(self):
            self.data="["+self.data.decode('utf-8')+"]"
            i = 2
            while i<len(self.data)-1:
                if self.data[i]=="}" and self.data[i+1]=="{":
                    self.data=self.data[:i+1]+","+self.data[(i+1):]
                    i+=3
                else:
                    i+=1
            
        def handleClientThreadPack(self, conn): 
            while True:
                try:
                    self.data = self.conn.recv(1024) # ждем запросов от клиента
                    self.jsonFixError()
                    ##else:
                    ##    print("")
                    ##    print(self.data)
                    ##    print("")

                    if not self.data: # если запросы перестали поступать, то ждём несколько итераций
                        if self.waiting>10:
                            break
                        else:
                            self.waiting += 1
                    else:
                        self.waiting = 0

                    # загружаем данные в json формате
                    self.data = json.loads(self.data)
                    

                    # запрос на получение игроков на сервере
                    for d in self.data:
                        if d["request"] == "get_players":
                            answer_to_players = []
                            for i in self.players:
                                answer_to_players.append({"x":i.x,"y":i.y,"id":i.id})

                            self.conn.sendall(bytes(json.dumps({"response": answer_to_players}), 'UTF-8'))
                        else:
                            print(self.data)
                        # движение
                        if d["request"] == "move":

                            if d["move"] == "left":
                                self.x -= 1
                            if d["move"] == "right":
                                self.x += 1
                            if d["move"] == "up":
                                self.y -= 1
                            if d["move"] == "down":
                                self.y += 1
                except Exception as e:
                    print(e)
                    break

            self.thread = 0# если вышел или выкинуло с сервера - поток
            
    def listen(self):
        while True:
            if True:##not len(self.players) >= self.max_players: # проверяем не превышен ли лимит
                 # одобряем подключение, получаем взамен адрес и другую информацию о клиенте
                conn, addr = self.sock.accept()
                b = True ## нужно ли создавать новый объект клиент-обработчика
                print("New connection", addr)
                print("conn", conn)

                for i in self.players:
                    if i.addr[0] == addr[0]:
                        if not(i.thread):
                            b = False
                            i.addr = addr
                            i.conn = conn
                            i.thread = Thread(target=i.handleClientThreadPack, args=(conn,)).start() # Запускаем в новом потоке проверку действий игрока
                    
                if b:
                    self.players.append(self.ClientThreadPack(self.players,conn,addr,400,300,len(self.players)))# добавляем его в массив игроков

if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)
