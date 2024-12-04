import sys
import pygame
import numpy

#Membros

#Arthur Reina Lyra - 12722124645
#Elaine Santana Gonzaga - 12722131402
#Isac Daniel Pereira de Almeida - 12723116417
#João Victor Pinho de Castro - 1272328040
#Nelson Anísio Nascimento do Carmo - 1272018392

#Glossário
#lin são linhas e col colunas


pygame.init()




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
                pygame.draw.circle(tela, color, (int(col * QUADRADO + QUADRADO // 2), int(lin * QUADRADO + QUADRADO // 2)), CIRCULORAIO, CIRCULOLARGURA) #Desenha o circulo para a IA, calcula o centro da célula horizontalmente e verticalmente, utiliza as coordenadas para imprimir de maneira centralizada o círculo

def marcar_quadrado(lin, col, player): #Função para marcar a célula
    tabuleiro[lin][col] = player


def quadrado_disponivel(lin, col): #Função que retorna quais células estão disponíveis, voltando 1 ou 2 esta marcado por player ou IA e 0 para célula disponível
    return tabuleiro[lin][col] == 0


def checador(checar_tabuleiro=tabuleiro): #Chechador se tabuleiro está cheio
    for lin in range (LINHAS):
        for col in range(COLUNAS):
            if checar_tabuleiro[lin][col] == 0:
                return False
    return True


def checar_vitoria(player, checar_tabuleiro=tabuleiro): #Checador de vitórias
    
    for col in range(COLUNAS):
        if checar_tabuleiro[0][col] == player and checar_tabuleiro[1][col] == player and checar_tabuleiro[2][col] == player: #Percorre as colunas verificando se existem 3 marcações iguais, se sim vitória
            return True

    for lin in range(LINHAS):
        if checar_tabuleiro[lin][0] == player and checar_tabuleiro[lin][1] == player and checar_tabuleiro[lin][2] == player: #Percorre as linhas verificando se existem 3 marcações iguais, se sim vitória
            return True
    
    for lin in range(LINHAS):
        for col in range (COLUNAS):    
            if checar_tabuleiro[0][0] == player and checar_tabuleiro[1][1] == player and checar_tabuleiro[2][2] == player:   #Verifica na diagonal se existem 3 marcações iguais, se sim vitória
                return True
    
    for lin in range(LINHAS):
        for col in range (COLUNAS):
            if checar_tabuleiro[0][2] == player and checar_tabuleiro[1][1] == player and checar_tabuleiro[2][0] == player:   #Verifica na diagonal, em outro eixo, se existem 3 marcações iguais, se sim vitória
                return True
    
    return False


def minimax(minimax_board, profundidade, is_maximizing): #Parte inteligente do código, onde a IA começa a ser construída, como ela tomará decisões.
    
    if checar_vitoria(2, minimax_board): #Como 2 é a IA, essa parte define que ganhar é o melhor resultado possível
        return float('inf')
    elif checar_vitoria(1, minimax_board): #Já esta define que é o pior possível, pois o player ganhou
        return float('-inf')
    elif checador(minimax_board):  #Esta define que um empate é completamente neutro, nem bom nem ruim 
        return 0 

    if is_maximizing:  #IA simulando a própria jogada e a do player para decidir qual a melhor possível, a função é chamada de maneira recursiva alternando entre as diferentes perspectivas, tanto da IA quanto do Player qual seria a melhor jogada
        bestscore = -1000
        for lin in range(LINHAS):
            for col in range(COLUNAS):
                if minimax_board[lin][col] == 0:
                    minimax_board[lin][col] = 2
                    score = minimax(minimax_board, profundidade + 1, False) 
                    minimax_board[lin][col] = 0  
                    bestscore = max(score, bestscore) 
        return bestscore
    

    else:
        bestscore = 1000
        for lin in range(LINHAS):
            for col in range(COLUNAS):
                if minimax_board[lin][col] == 0:
                    minimax_board[lin][col] = 1
                    score = minimax(minimax_board, profundidade + 1, True)
                    minimax_board[lin][col] = 0
                    bestscore = min(score, bestscore)
        return bestscore


def melhormovimento(): #Função que decide o melhor movimento
    bestscore = -1000  
    movimento = (-1, -1)
    for lin in range (LINHAS):
            for col in range(COLUNAS):
                if tabuleiro[lin][col] == 0: 
                    tabuleiro[lin][col] = 2
                    score = minimax(tabuleiro, profundidade=0, is_maximizing=False)
                    tabuleiro[lin][col] = 0
                    if score > bestscore:  #Aqui ele compara caso o score da ação tomada é melhor do que o bestscore atual que foi propositalmente negativado, mostrando que sim esse é o melhor movimento 
                        bestscore = score
                        movimento = (lin, col) #As coordenadas do movimento são guardadas
    
    if movimento != (-1, -1):  #Se o movimento não é mais -1,-1, sinaliza que um melhor movimento foi escolhido e está guardado em movimento, agora ele será marcado no tabuleiro, com a numeração da IA que é 2
        marcar_quadrado(movimento[0], movimento[1], player=2)
        return True
    return False


def reiniciarjogo(): #Função para reiniciar o jogo ao apertar a tecla R no teclado
    tela.fill(PRETO)
    desenhalinhas()
    for lin in range(LINHAS):
        for col in range (COLUNAS):
            tabuleiro[lin][col] = 0


#Main
desenhalinhas() #Desenha as linhas no tabuleiro
player = 1 #Define que o playqer a jogar é o 1, o humano
gameover = False #Sinaliza que o jogo não acabou

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  #Função para fechar a aplicação caso o X seja apertado na janela
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not gameover:  #Função para marcação nos quadrados, verificação de quadrados disponíveis pois sobrescrever não é uma opção e checados de gameover
            mouseX = event.pos[0] // QUADRADO
            mouseY = event.pos[1] // QUADRADO
            
            if quadrado_disponivel(mouseY, mouseX):
                marcar_quadrado(mouseY, mouseX, player)
                if checar_vitoria(player=1):  #Checa vitória após o movimento do jogador, se vitória gameover = True, caso não seja vitória, troca entre vez de jogar
                    gameover = True
                player = player % 2 +1 #Usando módulo como forma de transformar 2 em 1 e 1 em 2, para trocar entre jogadores em caso de não gameover
                
                if not gameover:
                    if melhormovimento():
                        if checar_vitoria(player=2): #Mesma função só que checando após movimento da IA, caso não seja vitória, é novamente a vez do player
                            gameover = True
                player = player % 2 +1 #Usando módulo como forma de transformar 2 em 1 e 1 em 2, para trocar entre jogadores em caso de não gameover
                
                if not gameover:  #Checa em caso de jogador ter feito uma jogada, a IA ter feito uma jogada, ninguém ganhou e o tabuleiro está cheio, logo é um empate
                    if checador():
                        gameover = True
        
        if event.type == pygame.KEYDOWN: #Reiniciando jogo
            if event.key == pygame.K_r:
                reiniciarjogo()
                gameover = False
                player = 1 #Define o humano como primeiro jogador

    if not gameover:
        desenhafiguras()
    else:
        if checar_vitoria(1): #Desenha em cores diferentes as figuras e linhas em caso de vitória, derrota ou empate,
            desenhafiguras(VERDE) #Verde para vitória do player 1
            desenhalinhas(VERDE)
            
        elif checar_vitoria(2): #vermelhor para vitória da IA
            desenhafiguras(VERMELHO)
            desenhalinhas(VERMELHO)  
        
        else:
            desenhafiguras(CINZA) #Cinza para empates
            desenhalinhas(CINZA)

    pygame.display.update()
