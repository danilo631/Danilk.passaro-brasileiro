import pygame
import random
import sys
import math

# Inicialização otimizada
pygame.init()
try:
    pygame.mixer.quit()  # Desativa som para performance
except:
    pass

# Configurações da tela
info = pygame.display.Info()
LARGURA, ALTURA = min(info.current_w, 720), min(info.current_h, 1280)
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Passaro Brasileiro - O Retorno")

# Constantes do jogo
FPS = 60
GRAVIDADE = 0.5
FORCA_PULO = -9
LARGURA_CANO = 70
ESPACO_ENTRE_CANOS = 250  # Mais espaço entre canos
VELOCIDADE_CANO = 4 + LARGURA / 720 * 1.5
RAIO_PASSARO = int(ALTURA * 0.03)

# Cores
CORES = {
    'ceu': (100, 200, 255),
    'grama': (76, 187, 23),
    'cano': (34, 139, 34),
    'passaro': (255, 255, 0),
    'vermelho': (255, 50, 50),
    'roxo': (160, 32, 240),
    'branco': (255, 255, 255),
    'preto': (0, 0, 0),
    'amarelo': (255, 215, 0),
    'transparente': (0, 0, 0, 128)
}

# Memes brasileiros hilários 💀
MEMES = [
    "QUE ISSO MEU FILHO CALMA!", "FOI POUCO!", "TA OK!",
    "VAI DAR NAMORO!", "ZIKOU!", "PEDE REVANCHE!",
    "BRASIL SIL SIL!", "FALTA DE AVISO!", "OLHA O BURACO!",
    "PARE!", "QUE ISSO IRMÃO!", "TA TUDO ERRADO!",
    "SOCORRO!", "VAI BRASIL!", "EH GOL!", "QUE FRANGO!",
    "PODIA SER PIOR!", "VOCE É MÉDICO?", "TÁ DEMITIDO!"
]

# Sistema de partículas
class Particulas:
    def __init__(self):
        self.particulas = []

    def adicionar(self, pos, cor, quantidade=5):
        for _ in range(quantidade):
            self.particulas.append({
                'pos': list(pos),
                'cor': cor,
                'velocidade': [random.uniform(-3, 3), random.uniform(-3, 3)],
                'vida': random.randint(20, 40)
            })

    def atualizar(self):
        for p in self.particulas[:]:
            p['pos'][0] += p['velocidade'][0]
            p['pos'][1] += p['velocidade'][1]
            p['vida'] -= 1
            if p['vida'] <= 0:
                self.particulas.remove(p)

    def desenhar(self, superficie):
        for p in self.particulas:
            alpha = max(0, int(p['vida'] * 6))
            s = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p['cor'], alpha), (5, 5), 5)
            superficie.blit(s, (int(p['pos'][0]-5), int(p['pos'][1]-5)))

particulas = Particulas()

# Fontes
def carregar_fonte(tamanho):
    try:
        return pygame.font.SysFont("Impact", tamanho, bold=True)
    except:
        return pygame.font.Font(None, tamanho)

FONTE_PEQUENA = carregar_fonte(int(ALTURA * 0.03))
FONTE_MEDIA = carregar_fonte(int(ALTURA * 0.05))
FONTE_GRANDE = carregar_fonte(int(ALTURA * 0.08))
FONTE_GIGANTE = carregar_fonte(int(ALTURA * 0.12))

# Estado do jogo
class EstadoJogo:
    def __init__(self):
        self.resetar()

    def resetar(self):
        self.passaro_pos = [LARGURA * 0.3, ALTURA // 2]
        self.velocidade = 0
        self.canhos = []
        self.pontos = 0
        self.record = 0
        self.fase = 1
        self.jogo_terminou = False
        self.jogo_iniciou = False
        self.efeito_especial = None
        self.tempo_efeito = 0
        self.ultimo_cano = 0
        self.mensagem = ""
        self.tempo_mensagem = 0
        self.cor_mensagem = CORES['branco']

jogo = EstadoJogo()

# Funções adicionais
def ativar_efeito():
    efeitos = ["cabeca_grande", "imortal", "controle_invertido"]
    jogo.efeito_especial = random.choice(efeitos)
    jogo.tempo_efeito = 180
    mostrar_mensagem("PODER ATIVADO!", CORES['roxo'])

def mostrar_mensagem(texto, cor=CORES['branco']):
    jogo.mensagem = texto
    jogo.cor_mensagem = cor
    jogo.tempo_mensagem = 60

# Funções de desenho
def desenhar_fundo():
    for y in range(0, ALTURA, 2):
        progresso = y / ALTURA
        cor = (
            int(CORES['ceu'][0] * (1 - progresso * 0.3)),
            int(CORES['ceu'][1] * (1 - progresso * 0.3)),
            int(CORES['ceu'][2] * (1 - progresso * 0.3))
        )
        pygame.draw.line(TELA, cor, (0, y), (LARGURA, y))
    pygame.draw.rect(TELA, CORES['grama'], (0, int(ALTURA * 0.94), LARGURA, int(ALTURA * 0.06)))
    for x in range(0, LARGURA, 40):
        pygame.draw.rect(TELA, (50, 150, 50), (x, int(ALTURA * 0.94), 20, 15)

def desenhar_passaro():
    raio = RAIO_PASSARO * (1.5 if jogo.efeito_especial == "cabeca_grande" else 1)
    x, y = jogo.passaro_pos

    # Corpo do pássaro
    pygame.draw.circle(TELA, CORES['passaro'], (int(x), int(y)), int(raio))
    pygame.draw.circle(TELA, CORES['preto'], (int(x), int(y)), int(raio), 2)  # Contorno

    # Olhos animados
    olho_x = x + (raio * 0.3 if frame_count % 20 < 10 else -raio * 0.3)
    pygame.draw.circle(TELA, CORES['branco'], (int(olho_x), int(y - raio * 0.2)), int(raio * 0.15))
    pygame.draw.circle(TELA, CORES['preto'], (int(olho_x), int(y - raio * 0.2)), int(raio * 0.07)

    # Bico
    bico_pontos = [(x + raio * 0.8, y), (x + raio * 1.5, y - raio * 0.3), (x + raio * 1.5, y + raio * 0.3)]
    pygame.draw.polygon(TELA, CORES['vermelho'], bico_pontos)

    # Asa animada
    wing_y = math.sin(frame_count * 0.2) * 10
    asa_pontos = [(x - raio * 0.7, y + wing_y), (x - raio * 0.3, y + raio * 0.8 + wing_y), (x + raio * 0.2, y + raio * 0.6 + wing_y)]
    pygame.draw.polygon(TELA, (255, 200, 0), asa_pontos)

def desenhar_canos():
    for cano in jogo.canhos:
        x = cano['x']
        topo = cano['topo']
        base = cano['base']
        especial = cano['especial']
        cor = CORES['roxo'] if especial else CORES['cano']
        pygame.draw.rect(TELA, cor, (x, 0, LARGURA_CANO, topo))
        pygame.draw.rect(TELA, CORES['preto'], (x, 0, LARGURA_CANO, topo), 2)
        pygame.draw.rect(TELA, cor, (x, base, LARGURA_CANO, ALTURA - base))
        pygame.draw.rect(TELA, CORES['preto'], (x, base, LARGURA_CANO, ALTURA - base), 2)

def desenhar_placar():
    s = pygame.Surface((LARGURA * 0.35, ALTURA * 0.12), pygame.SRCALPHA)
    s.fill((0, 0, 0, 150))
    TELA.blit(s, (10, 10))
    pontos_texto = FONTE_PEQUENA.render(f"Pontos: {jogo.pontos}", True, CORES['branco'])
    record_texto = FONTE_PEQUENA.render(f"Recorde: {jogo.record}", True, CORES['amarelo'])
    fase_texto = FONTE_PEQUENA.render(f"Fase: {jogo.fase}", True, CORES['branco'])
    TELA.blit(pontos_texto, (20, 15))
    TELA.blit(record_texto, (20, 45))
    TELA.blit(fase_texto, (20, 75))

def desenhar_mensagem():
    if jogo.tempo_mensagem > 0:
        fonte = FONTE_MEDIA
        texto = fonte.render(jogo.mensagem, True, jogo.cor_mensagem)
        sombra = fonte.render(jogo.mensagem, True, CORES['preto'])
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            TELA.blit(sombra, (LARGURA//2 - texto.get_width()//2 + dx, ALTURA//3 + dy))
        TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//3))
        jogo.tempo_mensagem -= 1

# Loop principal
relogio = pygame.time.Clock()
frame_count = 0
executando = True

while executando:
    relogio.tick(FPS)
    frame_count += 1

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
            if not jogo.jogo_iniciou:
                jogo.jogo_iniciou = True
                mostrar_mensagem("VOA PASSARO!", CORES['amarelo'])
            elif jogo.jogo_terminou:
                jogo.resetar()
            else:
                jogo.velocidade = FORCA_PULO
                particulas.adicionar(jogo.passaro_pos, CORES['passaro'])

    if jogo.jogo_iniciou and not jogo.jogo_terminou:
        jogo.velocidade += GRAVIDADE
        jogo.passaro_pos[1] += jogo.velocidade

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - jogo.ultimo_cano > 1800 - jogo.fase * 50:
            jogo.ultimo_cano = tempo_atual
            altura_topo = random.randint(int(ALTURA * 0.1), int(ALTURA * 0.5))
            jogo.canhos.append({
                'x': LARGURA,
                'topo': altura_topo,
                'base': altura_topo + ESPACO_ENTRE_CANOS,
                'especial': random.random() < 0.1,
                'pontuado': False
            })

        velocidade_cano = VELOCIDADE_CANO + jogo.fase * 0.5
        for cano in jogo.canhos[:]:
            cano['x'] -= velocidade_cano
            if cano['x'] + LARGURA_CANO < jogo.passaro_pos[0] and not cano['pontuado']:
                jogo.pontos += 1
                cano['pontuado'] = True
                if jogo.pontos % 5 == 0:
                    jogo.fase += 1
                    mostrar_mensagem(f"FASE {jogo.fase}!", CORES['roxo'])
                    if random.random() < 0.3:
                        ativar_efeito()
            if cano['x'] + LARGURA_CANO < 0:
                jogo.canhos.remove(cano)
            if (jogo.passaro_pos[0] + RAIO_PASSARO > cano['x'] and 
                jogo.passaro_pos[0] - RAIO_PASSARO < cano['x'] + LARGURA_CANO):
                if jogo.efeito_especial != "imortal":
                    if (jogo.passaro_pos[1] - RAIO_PASSARO < cano['topo'] or 
                        jogo.passaro_pos[1] + RAIO_PASSARO > cano['base']):
                        if cano['especial']:
                            ativar_efeito()
                            jogo.canhos.remove(cano)
                        else:
                            jogo.jogo_terminou = True
                            jogo.record = max(jogo.record, jogo.pontos)
                            mostrar_mensagem(random.choice(MEMES), CORES['vermelho'])
                            particulas.adicionar(jogo.passaro_pos, CORES['vermelho'], 15)

        if jogo.passaro_pos[1] - RAIO_PASSARO < 0 or jogo.passaro_pos[1] + RAIO_PASSARO > ALTURA:
            jogo.jogo_terminou = True
            jogo.record = max(jogo.record, jogo.pontos)
            mostrar_mensagem("BATEU NA QUINA!", CORES['vermelho'])
            particulas.adicionar(jogo.passaro_pos, CORES['vermelho'], 15)

    if jogo.efeito_especial:
        jogo.tempo_efeito -= 1
        if jogo.tempo_efeito <= 0:
            jogo.efeito_especial = None

    desenhar_fundo()
    desenhar_canos()
    particulas.atualizar()
    particulas.desenhar(TELA)
    desenhar_passaro()
    desenhar_placar()
    desenhar_mensagem()

    if not jogo.jogo_iniciou:
        titulo = FONTE_GIGANTE.render("PÁSSARO BRASILEIRO", True, CORES['amarelo'])
        subtitulo = FONTE_MEDIA.render("Toque para começar!", True, CORES['branco'])
        escala = 1 + math.sin(frame_count * 0.05) * 0.1
        titulo_escalado = pygame.transform.scale_by(titulo, escala)
        TELA.blit(titulo_escalado, (LARGURA//2 - titulo_escalado.get_width()//2, ALTURA//4))
        TELA.blit(subtitulo, (LARGURA//2 - subtitulo.get_width()//2, ALTURA//2))
        if frame_count % 30 < 15:
            desenhar_passaro()

    if jogo.jogo_terminou and jogo.jogo_iniciou:
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill(CORES['transparente'])
        TELA.blit(overlay, (0, 0))
        game_over_texto = FONTE_GRANDE.render("FIM DE JOGO", True, CORES['vermelho'])
        pontos_texto = FONTE_MEDIA.render(f"Pontuação: {jogo.pontos}", True, CORES['branco'])
        reiniciar_texto = FONTE_PEQUENA.render("Toque para jogar de novo", True, CORES['branco'])
        TELA.blit(game_over_texto, (LARGURA//2 - game_over_texto.get_width()//2, ALTURA//3))
        TELA.blit(pontos_texto, (LARGURA//2 - pontos_texto.get_width()//2, ALTURA//2))
        TELA.blit(reiniciar_texto, (LARGURA//2 - reiniciar_texto.get_width()//2, ALTURA*2//3))

    pygame.display.flip()

pygame.quit()
sys.exit()
