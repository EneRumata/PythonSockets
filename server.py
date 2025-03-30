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
            
        def handleClientThreadPack(self, conn): 
            while True:
                try:
                    self.data = self.conn.recv(1024) # ждем запросов от клиента

                    if not self.data: # если запросы перестали поступать, то ждём несколько итераций
                        if self.waiting>10:
                            break
                        else:
                            self.waiting += 1
                    else:
                        self.waiting = 0

                    # загружаем данные в json формате
                    self.data = json.loads(self.data.decode('utf-8'))

                    # запрос на получение игроков на сервере
                    if self.data["request"] == "get_players":
                        answer_to_players = []
                        for i in self.players:
                            answer_to_players.append({"x":i.x,"y":i.y,"id":i.id})

                        self.conn.sendall(bytes(json.dumps({
                            "response": answer_to_players
                        }), 'UTF-8'))

                    # движение
                    if self.data["request"] == "move":

                        if self.data["move"] == "left":
                            self.x -= 1
                        if self.data["move"] == "right":
                            self.x += 1
                        if self.data["move"] == "up":
                            self.y -= 1
                        if self.data["move"] == "down":
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
     
                print("New connection", addr)
                print("conn", conn)

                for i in self.players:
                    if i.addr == addr:
                        i.thread = Thread(target=self.handleClientThreadPack, args=(conn,)).start() # Запускаем в новом потоке проверку действий игрока
                        return
                    
                print("self.players start is ", self.players)
                self.players.append(self.ClientThreadPack(self.players,conn,addr,400,300,len(self.players)))# добавляем его в массив игроков

if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)
