import os
from time import sleep
from random import choice, randint
import json

def main():
    # Limpa a tela do terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Exibe uma animação de boas-vindas colorida
    for c in 'BEM VINDO(A) AO JOGO DA VELHA!':
        print(f'\033[1;{randint(31,36)}m{c}\033[m', end='')
        sleep(0.1)
    print('\n')
    
    # Escolha do marcador do jogador (X ou O)
    mPlayer = escolhaMarcador()
    mBot = 'X' if mPlayer == 'O' else 'O'
    
    # Inicializa o tabuleiro vazio
    tabuleiro: list = [['' for _ in range(3)] for _ in range(3)]
    
    # Loop principal do jogo
    while ganhador(tabuleiro) == False:
        if mPlayer == 'X':
            # Jogador X faz sua jogada
            jogadaPlayer = getJogada(tabuleiro)
            jogadaX, jogadaY = jogadaPlayer
            tabuleiro[jogadaX][jogadaY] = mPlayer
            if ganhador(tabuleiro) != False:
                break
            # Bot faz sua jogada
            jogadaBot = botJogada(tabuleiro, mBot)[0]
            jogadaX, jogadaY = jogadaBot
            tabuleiro[jogadaX][jogadaY] = mBot
        else:
            # Bot faz sua jogada
            jogadaBot = botJogada(tabuleiro, mBot)[0]
            jogadaX, jogadaY = jogadaBot
            tabuleiro[jogadaX][jogadaY] = mBot
            if ganhador(tabuleiro) != False:
                break
            # Jogador O faz sua jogada
            jogadaPlayer = getJogada(tabuleiro)
            jogadaX, jogadaY = jogadaPlayer
            tabuleiro[jogadaX][jogadaY] = mPlayer
    
    # Verifica o resultado do jogo
    ganhou = ganhador(tabuleiro)
    
    # Mostra o tabuleiro final com animação
    mostrarTabAnim(tabuleiro)
    sleep(1)
    
    # Exibe mensagem de vitória, derrota ou empate
    if ganhou == mPlayer:
        animacaoVit(tabuleiro)
        for c in 'VOCÊ GANHOU!':
            print(f'\033[1;3{randint(1,6)}m{c}', end='')
            sleep(0.3)
        print('\033[m')
    elif ganhou == mBot:
        animacaoVit(tabuleiro)
        for c in 'VOCÊ PERDEU!':
            print(f'\033[1;3{randint(1,6)}m{c}', end='')
            sleep(0.3)
        print('\033[m')
    else:
        animacaoDraw(tabuleiro)
        for c in 'DEU VELHA!':
            print(f'\033[1;3{randint(1,6)}m{c}', end='')
            sleep(0.3)
        print('\033[m')
    
    # Aguarda entrada do usuário para continuar
    input('\npressione \033[32mENTER\033[m para continuar...')

def escolhaMarcador():
    # Função para o jogador escolher o marcador (X ou O)
    while True:
        print('Escolha um marcador:\n[\033[1;31mX\033[m]\n[\033[1;34mO\033[m]')
        marcador = input('\033[35m>>>\033[m').strip().upper()
        if marcador not in ('X', 'O'):
            print('\033[1;31mESCOLHA APENAS OPÇÕES DISPONÍVEIS (X OU O)\033[m')
            continue
        return marcador

def ganhador(tabuleiro):
    # Verifica se há um vencedor ou empate
    for row in tabuleiro:
        if row[0] == row[1] == row[2] != '':
            return row[0]
    
    for i in range(3):
        if tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] != '':
            return tabuleiro[0][i]
    
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != '' or tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != '':
        return tabuleiro[1][1]
    
    for row in tabuleiro:
        for el in row:
            if el == '':
                return False
    
    return 'empate'

def mostrarTab(tabuleiro):
    # Exibe o tabuleiro atual
    os.system('cls' if os.name == 'nt' else 'clear')
    for l in range(3):
        for c in range(3):
            if c != 0:
                print('\033[1m|\033[m', end='')
            
            if tabuleiro[l][c] == '':
                print('\033[1;33m'+f'{l} {c}'+'\033[m', end='')
            elif tabuleiro[l][c] == 'X':
                print('\033[1;31m X \033[m', end='')
            elif tabuleiro[l][c] == 'O':
                print('\033[1;34m O \033[m', end='')
        print()
        if l != 2:
            print('\033[1m---+---+---\033[m')

def getJogada(tabuleiro):
    # Obtém a jogada do jogador
    mostrarTab(tabuleiro)
    entrada = input('\033[1mescolha uma coordenada\n\033[35m>>>\033[m').strip()
    jogada = []
    
    for char in entrada:
        if char.isnumeric():
            jogada.append(int(char))
    
    while (output := isValidPlay(tabuleiro, jogada)) != True:
        print('\033[1;31m'+output+'\033[m')
        sleep(2)
        mostrarTab(tabuleiro)
        entrada = input('escolha uma coordenada\n\033[35m>>>\033[m').strip()
        jogada = []
        for char in entrada:
            if char.isnumeric():
                jogada.append(int(char))
    
    return jogada

def isValidPlay(tabuleiro, jogada):
    # Valida se a jogada é válida
    print()
    if len(jogada) != 2:
        return "DIGITE APENAS DOIS NÚMEROS COMO APARECEM NO TABULEIRO!"
    
    for x in jogada:
        if x not in range(3):
            return "DIGITE APENAS COORDENADAS PRESENTES NO TABULEIRO!"
    
    jx, jy = jogada
    if tabuleiro[jx][jy] != '':
        return "ESTA CASA JÁ FOI ESCOLHIDA!"
    
    return True

def makeStrTab(tabuleiro):
    strTab = ''
    for linha in tabuleiro:
        for casa in linha:
            if casa == '':
                strTab += ' '
            else:
                strTab += casa
    return strTab

def backtracking(tabuleiro, marc):
    # Algoritmo de backtracking para determinar a melhor jogada do bot
    ganhou = ganhador(tabuleiro)
    if ganhou == False:
        output = botJogada(tabuleiro, 'X' if marc == 'O' else 'O')[1]
        return output * (-1)
    
    if ganhou == marc:
        return 1
    elif ganhou == 'empate':
        return 0
    else:
        return -1

def botJogada(tabuleiro, marc):
    if usarBanco == 'S':
        try:
            resposta = choice(respostas[marc][makeStrTab(tabuleiro)])
            return (resposta,0)
        except KeyError:
            pass
        
    # Determina a jogada do bot usando backtracking
    jValidas = list()
    tempTab = [row[:] for row in tabuleiro]
    for x in range(3):
        for y in range(3):
            if tempTab[x][y] == '':
                jValidas.append((x, y))
    resultados = []
    
    
    while len(jValidas) != 0:
        jogada = choice(jValidas)
        x, y = jogada
        tempTab[x][y] = marc
        resultados.append((jogada, backtracking(tempTab, marc)))
        tempTab[x][y] = ''
        for i, p in enumerate(jValidas):
            if p == jogada:
                jValidas.pop(i)
    
    # Escolhe a melhor jogada com base nos resultados
    vitorias = []
    empates = []
    derrotas = []
    for resultado in resultados:
        if resultado[1] == 1:
            vitorias.append(resultado)
        elif resultado[1] == 0:
            empates.append(resultado)
        else:
            derrotas.append(resultado)
    
    if len(vitorias) >= 1:
        return vitorias[0]
    elif len(empates) >= 1:
        return empates[0]
    else:
        return derrotas[0]

# Funções de animação
def mostrarTabAnim(tabuleiro):
    # Exibe o tabuleiro com animação
    os.system('cls' if os.name == 'nt' else 'clear')
    for l in range(3):
        for c in range(3):
            if c != 0:
                print('\033[1m|\033[m', end='')
            
            if tabuleiro[l][c] == '':
                print('   ', end='')
            elif tabuleiro[l][c] == 'X':
                print('\033[1;31m X \033[m', end='')
            elif tabuleiro[l][c] == 'O':
                print('\033[1;34m O \033[m', end='')
            else:
                print(f' {tabuleiro[l][c]} ', end='')
        print()
        if l != 2:
            print('\033[1m---+---+---\033[m')

def animacaoVit(tabuleiro):
    # Animação de vitória
    ganhou = ganhador(tabuleiro)
    for i, row in enumerate(tabuleiro):
        if row[0] == row[1] == row[2] == ganhou:
            tabuleiro[i] = [f'\033[32m{ganhou}\033[m' for _ in range(3)]
    for i in range(3):
        if tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] == ganhou:
            for x in range(3):
                tabuleiro[x][i] = f'\033[32m{ganhou}\033[m'
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] == ganhou:
        for x in range(3):
            tabuleiro[x][x] = f'\033[32m{ganhou}\033[m'
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] == ganhou:
        for x in range(3):
            tabuleiro[2 - x][x] = f'\033[32m{ganhou}\033[m'
    
    for _ in range(3):
        sleep(0.7)
        mostrarTabAnim(tabuleiro)
        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
    
    mostrarTabAnim(tabuleiro)

def animacaoDraw(tabuleiro):
    # Animação de empate
    casas = []
    while len(casas) != 9:
        x, y = randint(0, 2), randint(0, 2)
        if (x, y) not in casas:
            casas.append((x, y))
    for _ in range(9):
        x, y = casas[len(casas) - 1]
        tabuleiro[x][y] = f'\033[1;33m{tabuleiro[x][y]}\033[m'
        casas.pop()
        sleep(0.5)
        mostrarTabAnim(tabuleiro)

def loadRespostas():
    # Carrega as respostas salvas do arquivo JSON
    with open('respostas.json') as arquivo:
        return json.load(arquivo)

def saveRespostas():
    # Salva as respostas no arquivo JSON
    with open('respostas.json', 'w') as arquivo:
        json.dump(respostas, arquivo)

def adicionarResposta(resposta, tabuleiro, marc):
    # Adiciona uma resposta ao dicionário de respostas
    strTab = ''
    resposta = resposta
    for linha in tabuleiro:
        for casa in linha:
            if casa == '':
                strTab += ' '
            else:
                strTab += casa
    novo = True
    for jogo, possibilidades in respostas[marc].items():
        if jogo == strTab:
            if resposta not in possibilidades:
                respostas[marc][strTab].append(resposta)
            novo = False
            break
    if novo:
        respostas[marc][strTab] = [resposta]

if __name__ == '__main__':
    respostas: dict = loadRespostas()
    usarBanco = input('Deseja usar o banco de dados (respostas.json) nas respostas do bot? (S/N)\n\033[35m>>>\033[m').strip().upper()
    while usarBanco not in ('S','N'):
        print('\033[1;31mESCOLHA APENAS ENTRE S OU N!\033[m')
        usarBanco = input('Deseja usar o banco de dados (respostas.json) nas respostas do bot? (S/N)\n\033[35m>>>\033[m').strip().upper()
    main()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        escolha = input('\nQuer jogar novamente?(S/N)\n\033[35m>>>\033[m').strip().upper()
        if escolha not in ('S', 'N'):
            print('\n\033[1;31mESCOLHA APENAS SIM (S) OU NÃO (N)!\033[m')
            continue
        if escolha == 'S':
            main()
        else:
            for c in 'ATÉ LOGO!':
                print(f'\033[1;{randint(31,36)}m{c}\033[m', end='')
                sleep(0.2)
            exit()