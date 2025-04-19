import socket
import threading

class Sistema_Assentos:
    def __init__(self, total_assentos=100):
        self.assentos = [False] * total_assentos
        self.lock = threading.Lock()

    def listar_assentos(self):
        with self.lock:
            return ''.join(['X' if ocupado else '_' for ocupado in self.assentos])

    def reservar_assentos(self, lista_indices):
        reservados = []
        ocupados = []
        with self.lock:
            for idx in lista_indices:
                if 1 <= idx <= len(self.assentos):
                    if not self.assentos[idx - 1]:  
                        self.assentos[idx - 1] = True
                        reservados.append(idx)
                    else:
                        ocupados.append(idx)  
        return reservados, ocupados

    def cancelar_reservas(self, lista_indices):
        cancelados = []
        with self.lock:
            for idx in lista_indices:
                if 1 <= idx <= len(self.assentos):
                    if self.assentos[idx - 1]:  
                        self.assentos[idx - 1] = False  
                        cancelados.append(idx)
        return cancelados

assentos = Sistema_Assentos()

def lidar_com_cliente(conn, addr):
    print(f"[+] Cliente conectado: {addr}")
    try:
        while True:
            dados = conn.recv(1024).decode()
            if not dados:
                break

            partes = dados.strip().split()
            comando = partes[0]

            if comando == "VER":
                estado = assentos.listar_assentos()
                conn.sendall(estado.encode())

            elif comando == "RESERVAR":
                try:
                    indices = list(map(int, partes[1:]))
                    reservados, ocupados = assentos.reservar_assentos(indices)
                    
                    if reservados:
                        resposta = f"Reservados: {reservados}\n"
                    else:
                        resposta = ""
                    
                    if ocupados:
                        resposta += f"Assentos indisponiveis: {ocupados}\n"
                    
                    print(f"[{addr}] {resposta.strip()}")
                    conn.sendall(resposta.encode())

                except ValueError:
                    conn.sendall("Erro: entrada inválida.\n".encode())

            elif comando == "CANCELAR":
                try:
                    indices = list(map(int, partes[1:]))
                    cancelados = assentos.cancelar_reservas(indices)
                    if cancelados:
                        resposta = f"Cancelados: {cancelados}\n"
                    else:
                        resposta = "Nenhum assento cancelado.\n"
                    print(f"[{addr}] {resposta.strip()}")
                    conn.sendall(resposta.encode())
                except ValueError:
                    conn.sendall("Erro: entrada inválida.\n".encode())

            elif comando == "SAIR":
                conn.sendall("Conexão encerrada.\n".encode())
                break
            else:
                conn.sendall("Comando inválido.\n".encode())
    except Exception as e:
        print(f"[ERRO] {e}")
    finally:
        print(f"[-] Cliente desconectado: {addr}")
        conn.close()

def iniciar_servidor():
    host = 'localhost'
    porta = 12345

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, porta))
    servidor.listen(5)

    print(f"Servidor executando em {host}:{porta}...")

    try:
        while True:
            conn, addr = servidor.accept()
            thread = threading.Thread(target=lidar_com_cliente, args=(conn, addr))
            thread.start()
            print(f"[ATIVO] Conexões ativas: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Servidor finalizado manualmente.")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()

