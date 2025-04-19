SISTEMA DE GERENCIAMENTO DE ASSENTOS - TRABALHO DE PROGRAMAÇÃO CONCORRENTE E DISTRIBUÍDA

ARQUIVO CLIENTES.PY - 
Esse arquivo tem o fito de interagir com o cliente, de maneira a obter as reservas e cancelamentos dos clientes, além de viabilizar a visualização dos assentos disponíveis. Finalmente, o script também inclui a conexão direta com o servidor (arquivo servidor.py).

- Função mostrar_menu(): exibe as ações possíveis, as quais podem ser escolhidas pelo usuário;

- Função formatar_assentos(): exibe o mapa de assentos, com assentos ocupados sendo representados pelo caractere "X" e assentos desocupados sendo representados pelo caractere "_";

- Função cliente(): é a principal função do script, ao passo que cria a socket e viabiliza, então, a conexão com o servidor (localhost) pela porta 12345. O sistema opera, a parir disso, em loop até o usuário sair, de modo que o sistema opere de quatro formas diferentes:  
*Quando é informado o número 1 : o sistema envia a solicitação "VER" para o servidor e recebe do mesmo a caracterização atual dos assentos, de forma a exibi-los por meio da função formatar_assentos();\n
*Quando é informado o número 2 : o sistema envia a solicitação "RESERVAR" para o servidor e recebe o status da tentativa de reserva;\n
*Quando é informado o número 3 : o sistema envia a solicitação "CANCELAR" para o servidor e recebe o status da tentativa de cancelamento;\n
*Quando é informado o número 4 : o sistema envia a solicitação "SAIR" para o servidor e é encerrado;\n


ARQUIVO SERVIDOR.PY - 
Esse arquivo tem o fito de receber as solicitações do arquivo cliente.py, de forma a processá-las e garantir que não haja inconsistências nas reservas de assentos.

- Classe Sistema_Assentos() : controla todo o sistema responsável por garantir a consistência das reservas por meio da atribuição de valores booleanos a cada número de assentos, de forma a controlar se estão disponíveis ou não. Além disso, a utilização da função threading.Lock() é devida à necessidade de gerir o acesso de vários clientes ao mesmo tempo, de forma que cada cliente fique limitado a sua própria thread, o que impede a modificação de um mesmo assento por dois ou mais clientes diferentes ao mesmo tempo.

- Função listar_assentos(): atribui os valores "X" para assentos ocupados e "_" para assentos desocupados e retorna uma string para formatar esses dados.

- Função reservar_assentos(): recebe uma lista com os números correspondentes aos assentos e tenta reservá-los. O sistema irá retornar uma lista com os assentos reservados com sucesso, caso estajam livres previamente, e/ou uma lista com os assentos não reservados, caso estejam ocupados previamente.

- Função cancelar_reservas(): cancela as reservas caso os assentos estejam realmente ocupados, transformando o valor da variável assentos para false.

- Função lidar_com_cliente(): recebe o que o cliente quer fazer ("VER", "RESERVAR", "CANCELAR", "SAIR") e fica escutando o cliente enquanto ele estiver conectado. Chama cada método da classe Sistema_Assentos conforme a necessidade e envia o retorno ao cliente, de acordo com a resposta de cada método.

- Função iniciar_servidor() : cria o socket TCP para ouvir em localhost, na porta 12345; cria uma nova thread com a função lidar_com_cliente() para o cliente e mostra quantas conexões estão ativas. 
