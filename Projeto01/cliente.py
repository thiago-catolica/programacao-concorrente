import socket

def mostrar_menu():
    print("\n" + "="*30)
    print("Sistema de Reservas de Assentos")
    print("="*30)
    print("1. Ver assentos disponíveis")
    print("2. Reservar assentos")
    print("3. Cancelar reserva de assentos")
    print("4. Sair")

def formatar_assentos(dados):
    print("\nMapa de Assentos (X = ocupado, _ = livre):")
    for i in range(0, 100, 10):
        linha = dados[i:i+10]
        formatado = ""
        for j, status in enumerate(linha):
            num = f"{i+j+1:02d}"
            simb = "X" if status == "X" else "_"
            formatado += f"[{num}:{simb}] "
        print(formatado.strip())

def cliente():
    host = 'localhost'
    porta = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, porta))

    while True:
        mostrar_menu()
        opcao = input("\nDigite sua opção: ").strip()

        if opcao == "1":
            s.sendall("VER".encode())
            resposta = s.recv(2048).decode()
            formatar_assentos(resposta)

        elif opcao == "2":
            numeros = input("Digite o número do assento que deseja reservar: ")
            s.sendall(f"RESERVAR {numeros}".encode())
            resposta = s.recv(1024).decode()
            print("\n" + resposta)

        elif opcao == "3":
            numeros = input("Digite o número do assento que deseja cancelar: ")
            s.sendall(f"CANCELAR {numeros}".encode())
            resposta = s.recv(1024).decode()
            print("\n" + resposta)

        elif opcao == "4":
            s.sendall("SAIR".encode())
            print("Execução finalizada.")
            break

        else:
            print("Opção inválida, tente novamente.")

    s.close()

if __name__ == "__main__":
    cliente()

