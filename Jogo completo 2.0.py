import sys
import pygame
import numpy
import random

# Inicializa o módulo Pygame
pygame.init()

# Definição das cores
BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)

# Dimensões da tela e do tabuleiro
LARGURA = 600
ALTURA = 600
GROSSLINHA = 5
LINHAS = 3
COLUNAS = 3
QUADRADO = LARGURA // COLUNAS
CIRCULORAIO = QUADRADO // 3
CIRCULOLARGURA = 15
XIS = 25

# Configuração da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Velha Inteligente')
tela.fill(PRETO)

# Criação do tabuleiro vazio
tabuleiro = numpy.zeros((LINHAS, COLUNAS))

# Funções para desenhar o tabuleiro e as figuras

def desenhalinhas(color=BRANCO):
    #Desenha as linhas do tabuleiro.
    for i in range(1, COLUNAS):
        pygame.draw.line(tela, color, (0, QUADRADO * i), (LARGURA, QUADRADO * i), GROSSLINHA)
        pygame.draw.line(tela, color, (QUADRADO * i, 0), (QUADRADO * i, ALTURA), GROSSLINHA)

def desenhafiguras(color=BRANCO):
    #Desenha os 'X' e 'O' no tabuleiro de acordo com o estado do jogo.
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if tabuleiro[lin][col] == 1:
                # Desenha 'X'
                pygame.draw.line(tela, color, (col * QUADRADO + QUADRADO // 4, lin * QUADRADO + QUADRADO // 4),
                                 (col * QUADRADO + 3 * QUADRADO // 4, lin * QUADRADO + 3 * QUADRADO // 4), XIS)
                pygame.draw.line(tela, color, (col * QUADRADO + QUADRADO // 4, lin * QUADRADO + 3 * QUADRADO // 4),
                                 (col * QUADRADO + 3 * QUADRADO // 4, lin * QUADRADO + QUADRADO // 4), XIS)
            elif tabuleiro[lin][col] == 2:
                # Desenha 'O'
                pygame.draw.circle(tela, color, (int(col * QUADRADO + QUADRADO // 2), int(lin * QUADRADO + QUADRADO // 2)),
                                   CIRCULORAIO, CIRCULOLARGURA)

def marcar_quadrado(lin, col, player):
    #Marca um quadrado do tabuleiro com o jogador correspondente.
    tabuleiro[lin][col] = player

def quadrado_disponivel(lin, col):
    #Verifica se um quadrado está disponível (vazio).
    return tabuleiro[lin][col] == 0

def checador():
    #Verifica se não há mais quadrados disponíveis no tabuleiro.
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if tabuleiro[lin][col] == 0:
                return False
    return True

def checar_vitoria(player):
    #Verifica se o jogador ganhou.
    # Checar vitória nas linhas
    for lin in range(LINHAS):
        if tabuleiro[lin][0] == player and tabuleiro[lin][1] == player and tabuleiro[lin][2] == player:
            return True
    # Checar vitória nas colunas
    for col in range(COLUNAS):
        if tabuleiro[0][col] == player and tabuleiro[1][col] == player and tabuleiro[2][col] == player:
            return True
    # Checar vitória nas diagonais
    if tabuleiro[0][0] == player and tabuleiro[1][1] == player and tabuleiro[2][2] == player:
        return True
    if tabuleiro[0][2] == player and tabuleiro[1][1] == player and tabuleiro[2][0] == player:
        return True
    return False

def minimax(minimax_board, profundidade, is_maximizing):
    #Algoritmo Minimax para determinar o melhor movimento.
    if checar_vitoria(2):
        return 1  # Vitória da IA
    elif checar_vitoria(1):
        return -1  # Vitória do jogador
    elif checador():
        return 0  # Empate

    if is_maximizing:
        bestscore = -float('inf')
        for lin in range(LINHAS):
            for col in range(COLUNAS):
                if minimax_board[lin][col] == 0:
                    minimax_board[lin][col] = 2
                    score = minimax(minimax_board, profundidade + 1, False)
                    minimax_board[lin][col] = 0
                    bestscore = max(score, bestscore)
        return bestscore
    else:
        bestscore = float('inf')
        for lin in range(LINHAS):
            for col in range(COLUNAS):
                if minimax_board[lin][col] == 0:
                    minimax_board[lin][col] = 1
                    score = minimax(minimax_board, profundidade + 1, True)
                    minimax_board[lin][col] = 0
                    bestscore = min(score, bestscore)
        return bestscore

def melhormovimento():
    #Determina o melhor movimento para a IA usando Minimax.
    bestscore = -float('inf')
    movimento = (-1, -1)
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if tabuleiro[lin][col] == 0:
                tabuleiro[lin][col] = 2  # IA
                score = minimax(tabuleiro, profundidade=0, is_maximizing=False)
                tabuleiro[lin][col] = 0
                if score > bestscore:
                    bestscore = score
                    movimento = (lin, col)
    if movimento != (-1, -1):
        marcar_quadrado(movimento[0], movimento[1], player=2)
        return True
    return False

def movimento_aleatorio():
    #Realiza um movimento aleatório com um toque de estratégia para a dificuldade fácil.
    # Primeiro, tenta vencer se houver uma jogada vencedora
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if tabuleiro[lin][col] == 0:
                tabuleiro[lin][col] = 2  # Tenta a jogada
                if checar_vitoria(2):  # Se a IA ganhar
                    return True
                tabuleiro[lin][col] = 0  # Desfaz a jogada

    # Tenta bloquear o jogador se ele estiver prestes a vencer
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if tabuleiro[lin][col] == 0:
                tabuleiro[lin][col] = 1  # Tenta a jogada do jogador
                if checar_vitoria(1):  # Se o jogador ganhar
                    tabuleiro[lin][col] = 2  # Bloqueia
                    return True
                tabuleiro[lin][col] = 0  # Desfaz a jogada

    # Se nenhuma vitória ou bloqueio é possível, faz um movimento aleatório
    movimentos_possiveis = [(lin, col) for lin in range(LINHAS) for col in range(COLUNAS) if tabuleiro[lin][col] == 0]
    if movimentos_possiveis:
        movimento = random.choice(movimentos_possiveis)
        marcar_quadrado(movimento[0], movimento[1], player=2)
        return True
    return False

def reiniciarjogo():
    #Reinicia o jogo, limpando o tabuleiro e redesenhando a tela.
    tela.fill(PRETO)
    desenhalinhas()
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            tabuleiro[lin][col] = 0

def desenhar_botoes():
    #Desenha os botões de seleção de dificuldade na tela
    fonte = pygame.font.Font(None, 74)
    botao_facil = pygame.Rect(50, 260, 200, 50)
    botao_dificil = pygame.Rect(350, 260, 200, 50)
    pygame.draw.rect(tela, VERDE, botao_facil)
    pygame.draw.rect(tela, VERMELHO, botao_dificil)
    texto_facil = fonte.render('Fácil', True, PRETO)
    texto_dificil = fonte.render('Difícil', True, PRETO)
    tela.blit(texto_facil, (90, 270))  # Ajustar posição
    tela.blit(texto_dificil, (370, 270))  # Ajustar posição
    return botao_facil, botao_dificil


#Main
desenhalinhas()
player = 1  # Jogador 1 começa
gameover = False
dificuldade = None  # Inicializa a dificuldade como None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # Sai do jogo

        if dificuldade is None:  # Seleção de dificuldade
            tela.fill(PRETO)
            desenhalinhas()
            botao_facil, botao_dificil = desenhar_botoes()
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_facil.collidepoint(event.pos):
                    dificuldade = 'facil'
                    reiniciarjogo()
                elif botao_dificil.collidepoint(event.pos):
                    dificuldade = 'dificil'
                    reiniciarjogo()

        elif event.type == pygame.MOUSEBUTTONDOWN and not gameover:  # Jogada do jogador
            mouseX = event.pos[0] // QUADRADO
            mouseY = event.pos[1] // QUADRADO

            if quadrado_disponivel(mouseY, mouseX):
                marcar_quadrado(mouseY, mouseX, player)
                if checar_vitoria(player=1):  # Checa vitória do jogador
                    gameover = True
                player = player % 2 + 1  # Troca para IA

                if not gameover:
                    if dificuldade == 'dificil':
                        if melhormovimento():  # IA faz o melhor movimento
                            if checar_vitoria(player=2):  # Checa vitória da IA
                                gameover = True
                    elif dificuldade == 'facil':
                        if movimento_aleatorio():  # IA faz movimento aleatório
                            if checar_vitoria(player=2):
                                gameover = True
                player = player % 2 + 1

                if not gameover and checador():  # Verifica empate
                    gameover = True

        if event.type == pygame.KEYDOWN:  # Reinicia o jogo
            if event.key == pygame.K_r:
                reiniciarjogo()
                gameover = False
                player = 1
                dificuldade = None  # Retorna para seleção de dificuldade

    if not gameover:
        desenhafiguras()  # Desenha o estado atual do jogo
    else:
        # Exibe a mensagem de vitória ou empate
        if checar_vitoria(1):
            desenhafiguras(VERDE)  # Vitória do jogador
            desenhalinhas(VERDE)
        elif checar_vitoria(2):
            desenhafiguras(VERMELHO)  # Vitória da IA
            desenhalinhas(VERMELHO)
        else:
            desenhafiguras(CINZA)  # Empate
            desenhalinhas(CINZA)

    pygame.display.update()  # Atualiza a tela