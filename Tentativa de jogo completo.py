import sys
import pygame
import numpy

pygame.init()

#Glossário
#lin são linhas e col colunas
#
#


#Cores
BRANCO = (255, 255, 255) #Usado na cor das linhas
CINZA = (128, 128, 128) #Usado em caso de empate
VERMELHO = (255, 0, 0) #Usado para derrota do player
VERDE = (0, 255, 0) #Usado pra vitória do player
PRETO =(0, 0, 0) #Usado pro fundo do tabuleiro


#Proporções e tamanho
LARGURA = 600
ALTURA = 600
GROSSLINHA = 5
LINHAS = 3
COLUNAS = 3
QUADRADO = LARGURA // COLUNAS
CIRCULORAIO = QUADRADO // 3
CIRCULOLARGURA = 15
XIS = 25


tela = pygame.display.set_mode((LARGURA, ALTURA)) #Inicializador de tela, recebe Largura e Altura como parâmetro para tamanho
pygame.display.set_caption('Jogo da Velha Inteligente') #Serve para colocar o nome do jogo na janela
tela.fill(PRETO) #Preenche a tela de preto

tabuleiro = numpy.zeros((LINHAS, COLUNAS)) #Faz com que o taubleiro não tenha nenhuma marcação de jogador

#Funções

#Função para desenhar a grade de 3 por 3 do jogo da velha, duas linhas na vertical e duas na horizontal, toda vez que o jogo iniciar, foi reiniciado apertando a letra R, essa função desenhará as linhas da grade
def desenhalinhas(color=BRANCO):
    for i in range(1, COLUNAS):
        pygame.draw.line(tela, color, (0, QUADRADO * i), (LARGURA, QUADRADO * i), GROSSLINHA) #Desenha uma linha da primeira posição, até a última, utilizando GROSSLINHA como parametro para grossura da linha que será desenhada
        pygame.draw.line(tela, color, (QUADRADO * i, 0), (QUADRADO * i, ALTURA), GROSSLINHA)  #Mesmo código mas alterando o início e o fim para poder desenhar no outro eixo, só foram invertidos a órdem dos valores

#Desenha as figuras X ou O para jogador e AI
def desenhafiguras(color= BRANCO):
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if tabuleiro[lin][col] == 1:
                pygame.draw.line(tela, color,(col * QUADRADO + QUADRADO // 4, lin * QUADRADO + QUADRADO // 4), (col * QUADRADO + 3 * QUADRADO // 4, lin * QUADRADO + 3 * QUADRADO // 4), XIS) #Desenha uma linha na diagonal da esquerda superior para a direita inferior do quadrado
                pygame.draw.line(tela, color, (col * QUADRADO + QUADRADO // 4, lin * QUADRADO + 3 * QUADRADO // 4), (col * QUADRADO + 3 * QUADRADO // 4, lin * QUADRADO + QUADRADO // 4), XIS)#Mesmo código com o eixo invertido, desenhando assim da esquerda inferior para direita inferior, como são feitos os dois todas as vezes, ficamos com um X
                
            elif tabuleiro[lin][col] == 2:
                pygame.draw.circle(tela, color, (int(col * QUADRADO + QUADRADO // 2), int(lin * QUADRADO + QUADRADO // 2)), CIRCULORAIO, CIRCULOLARGURA) #Desenha o circulo para a IA, calcula o centro do quadrado horizontalmente e verticalmente, utiliza as coordenadas para imprimir de maneira centralizada o círculo

def marcar_quadrado(lin, col, player):
    tabuleiro[lin][col] = player


def quadrado_disponivel(lin, col):
    return tabuleiro[lin][col] == 0


def checador(checar_tabuleiro=tabuleiro):
    for lin in range (LINHAS):
        for col in range(COLUNAS):
            if checar_tabuleiro[lin][col] == 0:
                return False
    return True


def checar_vitoria(player, checar_tabuleiro=tabuleiro):
    
    for col in range(COLUNAS):
        if checar_tabuleiro[0][col] == player and checar_tabuleiro[1][col] == player and checar_tabuleiro[2][col] == player:
            return True

    for lin in range(LINHAS):
        if checar_tabuleiro[lin][0] == player and checar_tabuleiro[lin][1] == player and checar_tabuleiro[lin][2] == player:
            return True
    
    for lin in range(LINHAS):
        for col in range (COLUNAS):    
            if checar_tabuleiro[0][0] == player and checar_tabuleiro[1][1] == player and checar_tabuleiro[2][2] == player:
                return True
    
    for lin in range(LINHAS):
        for col in range (COLUNAS):
            if checar_tabuleiro[0][2] == player and checar_tabuleiro[1][1] == player and checar_tabuleiro[2][0] == player:
                return True
    
    return False


def minimax(minimax_board, depth, is_maximizing):
    if checar_vitoria(2, minimax_board):
        return float('inf')
    elif checar_vitoria(1, minimax_board):
        return float('-inf')
    elif checador(minimax_board):
        return 0

    if is_maximizing:
        bestscore = -1000
        for lin in range(LINHAS):
            for col in range(COLUNAS):
                if minimax_board[lin][col] == 0:
                    minimax_board[lin][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[lin][col] = 0
                    bestscore = max(score, bestscore)
        return bestscore
    else:
        bestscore = 1000
        for lin in range(LINHAS):
            for col in range(COLUNAS):
                if minimax_board[lin][col] == 0:
                    minimax_board[lin][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[lin][col] = 0
                    bestscore = min(score, bestscore)
        return bestscore


def melhormovimento():
    bestscore = -1000
    movimento = (-1, -1)
    for lin in range (LINHAS):
            for col in range(COLUNAS):
                if tabuleiro[lin][col] == 0:
                    tabuleiro[lin][col] = 2
                    score = minimax(tabuleiro, depth=0, is_maximizing=False)
                    tabuleiro[lin][col] = 0
                    if score > bestscore:
                        bestscore = score
                        movimento = (lin, col)
    
    if movimento != (-1, -1):
        marcar_quadrado(movimento[0], movimento[1], player=2)
        return True
    return False


def reiniciarjogo():
    tela.fill(PRETO)
    desenhalinhas()
    for lin in range(LINHAS):
        for col in range (COLUNAS):
            tabuleiro[lin][col] = 0

#Main
desenhalinhas()
player = 1
gameover = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not gameover:
            mouseX = event.pos[0] // QUADRADO
            mouseY = event.pos[1] // QUADRADO
            
            if quadrado_disponivel(mouseY, mouseX):
                marcar_quadrado(mouseY, mouseX, player)
                if checar_vitoria(player):
                    gameover = True
                player = player % 2 +1
                
                if not gameover:
                    if melhormovimento():
                        if checar_vitoria(player=2):
                            gameover = True
                        player = player % 2 +1
                
                if not gameover:
                    if checador():
                        gameover = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reiniciarjogo()
                gameover = False
                player = 1

    if not gameover:
        desenhafiguras()
    else:
        if checar_vitoria(1):
            desenhafiguras(VERDE)
            desenhalinhas(VERDE)
            
        elif checar_vitoria(2):
            desenhafiguras(VERMELHO)
            desenhalinhas(VERMELHO)  
        
        else:
            desenhafiguras(CINZA)
            desenhalinhas(CINZA)

    pygame.display.update()
