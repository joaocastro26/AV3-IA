import sys
import pygame
import numpy
import random

# Inicializa o módulo Pygame
pygame.init()

# Definição das cores
# As cores são representadas por tuplas RGB
BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)

# Dimensões da tela e do tabuleiro
# Cada quadrado do tabuleiro é calculado como a largura da tela dividida pelo número de colunas
LARGURA = 600
ALTURA = 600
GROSSLINHA = 5
LINHAS = 3
COLUNAS = 3
QUADRADO = LARGURA // COLUNAS
CIRCULORAIO = QUADRADO // 3  # Raio do círculo para o jogador 'O'
CIRCULOLARGURA = 15  # Espessura da linha do círculo
XIS = 25  # Espessura da linha para o jogador 'X'

# Configuração da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Velha Inteligente')
tela.fill(PRETO)  # Define a cor de fundo inicial como preta

# Criação do tabuleiro vazio
# Representado por uma matriz 3x3 preenchida com zeros
tabuleiro = numpy.zeros((LINHAS, COLUNAS))

# Funções para desenhar o tabuleiro e as figuras
def desenhalinhas(color=BRANCO):
    # Desenha as linhas do tabuleiro
    for i in range(1, COLUNAS):
        pygame.draw.line(tela, color, (0, QUADRADO * i), (LARGURA, QUADRADO * i), GROSSLINHA)
        pygame.draw.line(tela, color, (QUADRADO * i, 0), (QUADRADO * i, ALTURA), GROSSLINHA)

def desenhafiguras(color=BRANCO):
    # Desenha as figuras ('X' e 'O') no tabuleiro, de acordo com o estado atual do jogo.
    # A função percorre o tabuleiro e, dependendo do valor nas células, desenha um 'X' ou um 'O'.

    # Laço que percorre todas as linhas do tabuleiro.
    for lin in range(LINHAS):
        # Laço que percorre todas as colunas do tabuleiro.
        for col in range(COLUNAS):
            # Verifica o valor da célula no tabuleiro (0: vazio, 1: jogador, 2: IA)
            if tabuleiro[lin][col] == 1:
                # Se o valor for 1, significa que o jogador fez a jogada (marca 'X').
                
                # Desenha o 'X' utilizando duas linhas que se cruzam.
                # As linhas são desenhadas no centro do quadrado, com uma espessura definida por XIS.
                #As coordenadas de cada linha são calculadas com base na posição da célula (representada por lin e col) e no tamanho do quadrado (QUADRADO).
                #A fórmula (col * QUADRADO + QUADRADO // 4, lin * QUADRADO + QUADRADO // 4) define o ponto inicial da linha. Este ponto está deslocado para a posição inicial do quadrado e um pouco para dentro (1/4 do tamanho do quadrado).
                #A fórmula (col * QUADRADO + 3 * QUADRADO // 4, lin * QUADRADO + 3 * QUADRADO // 4) define o ponto final da linha, deslocando-se para o ponto oposto do quadrado (3/4 do tamanho do quadrado).
                pygame.draw.line(tela, color, (col * QUADRADO + QUADRADO // 4, lin * QUADRADO + QUADRADO // 4), (col * QUADRADO + 3 * QUADRADO // 4, lin * QUADRADO + 3 * QUADRADO // 4), XIS)
                pygame.draw.line(tela, color, (col * QUADRADO + QUADRADO // 4, lin * QUADRADO + 3 * QUADRADO // 4), (col * QUADRADO + 3 * QUADRADO // 4, lin * QUADRADO + QUADRADO // 4), XIS)

            elif tabuleiro[lin][col] == 2:
                # Se o valor for 2, significa que a IA fez a jogada (marca 'O').
                
                # Desenha o 'O' como um círculo centrado no quadrado.
                # O centro do círculo é calculado como o ponto médio de cada quadrado com a fórmula (col * QUADRADO + QUADRADO // 2).
                # O raio do círculo é dado por CIRCULORAIO e a espessura da borda é CIRCULOLARGURA.
                pygame.draw.circle(tela, color, (int(col * QUADRADO + QUADRADO // 2), int(lin * QUADRADO + QUADRADO // 2)), CIRCULORAIO, CIRCULOLARGURA)


def marcar_quadrado(lin, col, player):
    # Marca um quadrado no tabuleiro para o jogador correspondente
    tabuleiro[lin][col] = player

def quadrado_disponivel(lin, col):
    # Verifica se um quadrado está disponível (não marcado)
    return tabuleiro[lin][col] == 0

def checador():
    # Verifica se não há mais quadrados disponíveis (empate)
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if tabuleiro[lin][col] == 0:
                return False
    return True

def checar_vitoria(player):
    # Verifica se o jogador especificado venceu
    # Checa linhas, colunas e diagonais
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


def minimax(minimax_tabuleiro, profundidade, maximizando):
    # Algoritmo Minimax para determinar o melhor movimento baseado em maximizar a vantagem da IA (2) ou minimizar o dano causado pelo jogador (1).

    # Verifica se a IA venceu (condição base para retornar o valor do nó)
    if checar_vitoria(2):
        return 1  # Vitória da IA é representada por um valor positivo

    # Verifica se o jogador humano venceu (condição base para retornar o valor do nó)
    elif checar_vitoria(1):
        return -1  # Vitória do jogador humano é representada por um valor negativo

    # Verifica se o tabuleiro está cheio, resultando em empate
    elif checador():
        return 0  # Empate é representado por um valor neutro (zero)

    if maximizando:  # Se a IA está jogando (tentando maximizar sua pontuação)
        bestscore = -float('inf')  # Inicializa a melhor pontuação com um valor muito baixo
        for lin in range(LINHAS):
            for col in range(COLUNAS):
                if minimax_tabuleiro[lin][col] == 0:  # Verifica se a célula está vazia
                    minimax_tabuleiro[lin][col] = 2  # Faz o movimento temporariamente
                    score = minimax(minimax_tabuleiro, profundidade + 1, False)  # Chama recursivamente para a próxima jogada
                    minimax_tabuleiro[lin][col] = 0  # Desfaz o movimento
                    bestscore = max(score, bestscore)  # Atualiza a melhor pontuação encontrada
        return bestscore

    else:  # Se o jogador está jogando (tentando minimizar a pontuação da IA)
        bestscore = float('inf')  # Inicializa a melhor pontuação com um valor muito alto
        for lin in range(LINHAS):
            for col in range(COLUNAS):
                if minimax_tabuleiro[lin][col] == 0:  # Verifica se a célula está vazia
                    minimax_tabuleiro[lin][col] = 1  # Faz o movimento temporariamente
                    score = minimax(minimax_tabuleiro, profundidade + 1, True)  # Chama recursivamente para a próxima jogada
                    minimax_tabuleiro[lin][col] = 0  # Desfaz o movimento
                    bestscore = min(score, bestscore)  # Atualiza a melhor pontuação encontrada
        return bestscore

def melhormovimento():
    # Determina o melhor movimento para a IA usando o algoritmo Minimax.
    bestscore = -float('inf')  # Inicializa a melhor pontuação com um valor muito baixo
    movimento = (-1, -1)  # Inicializa o movimento como inválido
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if tabuleiro[lin][col] == 0:  # Verifica se a célula está vazia
                tabuleiro[lin][col] = 2  # Faz o movimento temporariamente
                score = minimax(tabuleiro, profundidade=0, maximizando=False)  # Avalia o movimento com Minimax
                tabuleiro[lin][col] = 0  # Desfaz o movimento
                if score > bestscore:  # Atualiza se um movimento com melhor pontuação for encontrado
                    bestscore = score
                    movimento = (lin, col)
    if movimento != (-1, -1):  # Se um movimento válido foi encontrado
        marcar_quadrado(movimento[0], movimento[1], player=2)  # Marca o melhor movimento no tabuleiro
        return True
    return False  # Retorna False caso nenhum movimento válido seja encontrado


def movimento_aleatorio():
    # Realiza um movimento "fácil" com lógica básica e aleatoriedade.
    # Tenta vencer se houver uma jogada vencedora
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if tabuleiro[lin][col] == 0:  # Verifica se a célula está vazia
                tabuleiro[lin][col] = 2  # Faz o movimento temporariamente
                if checar_vitoria(2):  # Verifica se esse movimento resulta em vitória
                    return True  # Retorna imediatamente após fazer a jogada vencedora
                tabuleiro[lin][col] = 0  # Desfaz o movimento se não for uma jogada vencedora

    # Tenta bloquear o jogador se ele estiver prestes a vencer
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if tabuleiro[lin][col] == 0:  # Verifica se a célula está vazia
                tabuleiro[lin][col] = 1  # Simula o movimento do jogador humano
                if checar_vitoria(1):  # Verifica se o jogador humano venceria
                    tabuleiro[lin][col] = 2  # Bloqueia a jogada marcando para a IA
                    return True  # Retorna imediatamente após bloquear a jogada
                tabuleiro[lin][col] = 0  # Desfaz o movimento simulado

    # Se nenhuma vitória ou bloqueio é possível, faz um movimento aleatório
    movimentos_possiveis = [(lin, col) for lin in range(LINHAS) for col in range(COLUNAS) if tabuleiro[lin][col] == 0]
    if movimentos_possiveis:  # Verifica se ainda há células disponíveis
        movimento = random.choice(movimentos_possiveis)  # Escolhe um movimento aleatório
        marcar_quadrado(movimento[0], movimento[1], player=2)  # Marca o movimento escolhido no tabuleiro
        return True
    return False  # Retorna False caso não haja movimentos possíveis


def reiniciarjogo():
    # Reinicia o jogo, limpando o tabuleiro e redesenhando a tela
    tela.fill(PRETO)
    desenhalinhas()
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            tabuleiro[lin][col] = 0

def desenhar_botoes():
    # Cria e desenha os botões de seleção de dificuldade na tela.

    # Define a fonte a ser usada para o texto dos botões. 
    # A função `pygame.font.Font` recebe `None` para usar a fonte padrão e o tamanho de 74.
    fonte = pygame.font.Font(None, 74)

    # Cria o retângulo do botão de dificuldade "Fácil".
    # `pygame.Rect(x, y, largura, altura)` cria um retângulo na posição (50, 260) com tamanho 200x50.
    botao_facil = pygame.Rect(50, 260, 200, 50)

    # Cria o retângulo do botão de dificuldade "Difícil".
    # Este retângulo está localizado em (350, 260) com tamanho 200x50.
    botao_dificil = pygame.Rect(350, 260, 200, 50)

    # Desenha o retângulo do botão "Fácil" na tela.
    # A cor do botão é definida como `VERDE`.
    pygame.draw.rect(tela, VERDE, botao_facil)

    # Desenha o retângulo do botão "Difícil" na tela.
    # A cor do botão é definida como `VERMELHO`.
    pygame.draw.rect(tela, VERMELHO, botao_dificil)

    # Renderiza o texto "Fácil" usando a fonte definida.
    # A cor do texto é `PRETO`, criando contraste com o fundo verde do botão.
    texto_facil = fonte.render('Fácil', True, PRETO)

    # Renderiza o texto "Difícil" usando a fonte definida.
    # A cor do texto é `PRETO`, criando contraste com o fundo vermelho do botão.
    texto_dificil = fonte.render('Difícil', True, PRETO)

    # Posiciona o texto "Fácil" na tela dentro do botão correspondente.
    # `tela.blit` desenha o texto renderizado na posição especificada (90, 270).
    tela.blit(texto_facil, (90, 270))

    # Posiciona o texto "Difícil" na tela dentro do botão correspondente.
    # `tela.blit` desenha o texto renderizado na posição especificada (370, 270).
    tela.blit(texto_dificil, (370, 270))

    # Retorna os objetos de retângulo criados para os botões.
    # Isso permite que o programa identifique se o usuário clicou em um dos botões.
    return botao_facil, botao_dificil



#Main
desenhalinhas()
player = 1  # Jogador humano começa
gameover = False
dificuldade = None  # Inicialmente sem dificuldade selecionada

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # Sai do jogo quando o usuário fecha a janela

        if dificuldade is None:  # Tela de seleção de dificuldade
            tela.fill(PRETO)
            desenhalinhas()
            botao_facil, botao_dificil = desenhar_botoes()
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_facil.collidepoint(event.pos):  # Se o botão fácil for clicado
                    dificuldade = 'facil'
                    reiniciarjogo()
                elif botao_dificil.collidepoint(event.pos):  # Se o botão difícil for clicado
                    dificuldade = 'dificil'
                    reiniciarjogo()

        elif event.type == pygame.MOUSEBUTTONDOWN and not gameover:  # Jogada do jogador
            # Determina a posição no tabuleiro com base no clique do mouse
            mouseX = event.pos[0] // QUADRADO
            mouseY = event.pos[1] // QUADRADO

            if quadrado_disponivel(mouseY, mouseX):  # Verifica se o quadrado está disponível
                marcar_quadrado(mouseY, mouseX, player)
                if checar_vitoria(player):  # Verifica se o jogador venceu
                    gameover = True
                player = player % 2 + 1  # Alterna para o próximo jogador (IA)

                if not gameover:  # Se o jogo não acabou, a IA joga
                    if dificuldade == 'dificil':
                        if melhormovimento():  # IA joga o melhor movimento
                            if checar_vitoria(2):  # Verifica se a IA venceu
                                gameover = True
                    elif dificuldade == 'facil':
                        if movimento_aleatorio():  # IA faz movimento aleatório
                            if checar_vitoria(2):  # Verifica se a IA venceu
                                gameover = True
                    player = player % 2 + 1  # Alterna de volta para o jogador humano

                if not gameover and checador():  # Verifica se o jogo empatou
                    gameover = True

        if event.type == pygame.KEYDOWN:  # Verifica se a tecla "R" foi pressionada para reiniciar
            if event.key == pygame.K_r:
                reiniciarjogo()
                gameover = False
                player = 1
                dificuldade = None  # Retorna à tela de seleção de dificuldade

    if not gameover:
        desenhafiguras()  # Atualiza o tabuleiro com as jogadas atuais
    else:
        # Exibe a mensagem de vitória ou empate
        if checar_vitoria(1):  # Vitória do jogador humano
            desenhafiguras(VERDE)
            desenhalinhas(VERDE)
        elif checar_vitoria(2):  # Vitória da IA
            desenhafiguras(VERMELHO)
            desenhalinhas(VERMELHO)
        else:  # Empate
            desenhafiguras(CINZA)
            desenhalinhas(CINZA)

    pygame.display.update()  # Atualiza a tela para refletir as mudanças
