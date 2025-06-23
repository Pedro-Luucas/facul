import pygame
import math
from queue import PriorityQueue, Queue
import random

# --- CONFIGURAÇÕES DA JANELA E GRELHA ---
LARGURA_TELA = 800
LARGURA_PAINEL = 300
LARGURA_TOTAL = LARGURA_TELA + LARGURA_PAINEL
TELA = pygame.display.set_mode((LARGURA_TOTAL, LARGURA_TELA))
pygame.display.set_caption("Visualizador de Algoritmos de Busca")

# --- PALETA DE CORES ---
COR = {
    "fundo_grelha": (255, 255, 255),
    "fundo_painel": (45, 45, 48),
    "texto_titulo": (255, 255, 255),
    "texto_normal": (200, 200, 200),
    "linha_grelha": (220, 220, 220),
    "obstaculo": (25, 25, 26),
    "caminho": (102, 102, 255),
    "inicio": (255, 165, 0),
    "fim": (64, 224, 208),
    "aberto": (0, 153, 153, 150),
    "fechado": (255, 80, 80, 150),
    "botao": (0, 122, 204),
    "botao_hover": (0, 142, 234),
    "botao_texto": (255, 255, 255),
    "slider_trilha": (80, 80, 83),
    "slider_knob": (0, 122, 204)
}

# --- CLASSE NODO ---
class Nodo:
    def __init__(self, linha, col, largura, total_linhas):
        self.linha = linha
        self.col = col
        self.x = linha * largura
        self.y = col * largura
        self.cor = COR["fundo_grelha"]
        self.vizinhos = []
        self.largura = largura
        self.total_linhas = total_linhas

    def get_pos(self): return self.linha, self.col
    def is_fechado(self): return self.cor == COR["fechado"]
    def is_aberto(self): return self.cor == COR["aberto"]
    def is_obstaculo(self): return self.cor == COR["obstaculo"]
    def is_inicio(self): return self.cor == COR["inicio"]
    def is_fim(self): return self.cor == COR["fim"]
    def is_caminho(self): return self.cor == COR["caminho"]
    def resetar(self): self.cor = COR["fundo_grelha"]
    def fazer_inicio(self): self.cor = COR["inicio"]
    def fazer_fim(self): self.cor = COR["fim"]
    def fazer_obstaculo(self): self.cor = COR["obstaculo"]
    def fazer_caminho(self): self.cor = COR["caminho"]

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.largura))

    def fazer_aberto(self):
        self.cor = COR["aberto"]
        self.desenhar_transparente(TELA)
    
    def fazer_fechado(self):
        self.cor = COR["fechado"]
        self.desenhar_transparente(TELA)

    def desenhar_transparente(self, tela):
        s = pygame.Surface((self.largura, self.largura), pygame.SRCALPHA)
        s.fill(self.cor)
        tela.blit(s, (self.x, self.y))

    def atualizar_vizinhos(self, grade):
        self.vizinhos = []
        if self.linha < self.total_linhas - 1 and not grade[self.linha + 1][self.col].is_obstaculo(): self.vizinhos.append(grade[self.linha + 1][self.col])
        if self.linha > 0 and not grade[self.linha - 1][self.col].is_obstaculo(): self.vizinhos.append(grade[self.linha - 1][self.col])
        if self.col < self.total_linhas - 1 and not grade[self.linha][self.col + 1].is_obstaculo(): self.vizinhos.append(grade[self.linha][self.col + 1])
        if self.col > 0 and not grade[self.linha][self.col - 1].is_obstaculo(): self.vizinhos.append(grade[self.linha][self.col - 1])

    def __lt__(self, other): return False

# --- CLASSES DA INTERFACE (UI) ---
class Botao:
    def __init__(self, x, y, largura, altura, texto='', acao=None):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.acao = acao
        self.cor = COR["botao"]
        self.cor_hover = COR["botao_hover"]
        self.cor_atual = self.cor
        self.fonte = pygame.font.SysFont('segoeui', 18)

    def desenhar(self, tela):
        self.verificar_hover()
        pygame.draw.rect(tela, self.cor_atual, self.rect, border_radius=5)
        if self.texto != '':
            texto_render = self.fonte.render(self.texto, 1, COR["botao_texto"])
            tela.blit(texto_render, (self.rect.centerx - texto_render.get_width() / 2, self.rect.centery - texto_render.get_height() / 2))

    def verificar_hover(self):
        self.cor_atual = self.cor_hover if self.rect.collidepoint(pygame.mouse.get_pos()) else self.cor

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos) and self.acao:
            self.acao()

class Label:
    def __init__(self, x, y, texto, fonte, cor):
        self.x = x
        self.y = y
        self.texto_render = fonte.render(texto, 1, cor)

    def desenhar(self, tela):
        tela.blit(self.texto_render, (self.x, self.y))
    
    def handle_event(self, event): pass

class Slider:
    def __init__(self, x, y, largura, altura, min_val, max_val, valor_inicial):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.min_val = min_val
        self.max_val = max_val
        self.valor = valor_inicial
        self.arrastando = False
        self.knob_rect = pygame.Rect(0, 0, 10, altura + 10)
        self.atualizar_knob_pos()

    def atualizar_knob_pos(self):
        pos_relativa = (self.valor - self.min_val) / (self.max_val - self.min_val)
        self.knob_rect.centerx = self.rect.x + pos_relativa * self.rect.width
        self.knob_rect.centery = self.rect.centery

    def desenhar(self, tela):
        pygame.draw.rect(tela, COR["slider_trilha"], self.rect, border_radius=5)
        pygame.draw.rect(tela, COR["slider_knob"], self.knob_rect, border_radius=5)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (self.rect.collidepoint(event.pos) or self.knob_rect.collidepoint(event.pos)):
            self.arrastando = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.arrastando = False
        elif event.type == pygame.MOUSEMOTION and self.arrastando:
            x_rel = max(0, min(event.pos[0] - self.rect.x, self.rect.width))
            fracao = x_rel / self.rect.width
            self.valor = self.min_val + fracao * (self.max_val - self.min_val)
            self.atualizar_knob_pos()
    
    def get_valor(self): return int(self.max_val - self.valor)

# --- FUNÇÕES AUXILIARES ---
def h(p1, p2): return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def reconstruir_caminho(veio_de, atual, processar_passo):
    while atual in veio_de:
        atual = veio_de[atual]
        if not atual.is_inicio(): atual.fazer_caminho()
        processar_passo(desenhar_apenas_grelha=True)

def criar_grade(linhas, largura):
    return [[Nodo(i, j, largura // linhas, linhas) for j in range(linhas)] for i in range(linhas)]

def desenhar_linhas_grade(tela, linhas, largura):
    gap = largura // linhas
    for i in range(linhas + 1):
        pygame.draw.line(tela, COR["linha_grelha"], (0, i * gap), (largura, i * gap))
        pygame.draw.line(tela, COR["linha_grelha"], (i * gap, 0), (i * gap, largura))

def desenhar_painel(tela, ui_elementos):
    pygame.draw.rect(tela, COR["fundo_painel"], (LARGURA_TELA, 0, LARGURA_PAINEL, LARGURA_TELA))
    for elemento in ui_elementos.values():
        elemento.desenhar(tela)

def desenhar(tela, grade, linhas, largura_grade, ui_elementos, redesenhar_tudo=True):
    if redesenhar_tudo:
        tela.fill(COR["fundo_grelha"])
        for linha in grade:
            for nodo in linha:
                if not (nodo.is_aberto() or nodo.is_fechado()):
                    nodo.desenhar(tela)
        desenhar_linhas_grade(tela, linhas, largura_grade)

    for linha in grade:
        for nodo in linha:
            if nodo.is_aberto() or nodo.is_fechado():
                nodo.desenhar_transparente(tela)

    desenhar_painel(tela, ui_elementos)
    pygame.display.update()

def obter_pos_clicada(pos, linhas, largura):
    gap = largura // linhas
    y, x = pos
    if y >= largura: return -1, -1
    return y // gap, x // gap

# --- ALGORITMOS DE BUSCA ---
def executar_algoritmo(algoritmo_func, processar_passo, grade, inicio, fim):
    for linha in grade:
        for nodo in linha:
            nodo.atualizar_vizinhos(grade)
    algoritmo_func(processar_passo, grade, inicio, fim)

def busca_a_estrela(processar_passo, grade, inicio, fim):
    cont = 0
    conjunto_aberto = PriorityQueue()
    conjunto_aberto.put((0, cont, inicio))
    veio_de = {}
    g_score = {nodo: float("inf") for linha in grade for nodo in linha}
    g_score[inicio] = 0
    f_score = {nodo: float("inf") for linha in grade for nodo in linha}
    f_score[inicio] = h(inicio.get_pos(), fim.get_pos())
    conjunto_aberto_hash = {inicio}

    while not conjunto_aberto.empty():
        if not processar_passo(): return
        atual = conjunto_aberto.get()[2]
        conjunto_aberto_hash.remove(atual)

        if atual == fim:
            reconstruir_caminho(veio_de, fim, processar_passo)
            fim.fazer_fim(); inicio.fazer_inicio()
            return

        for vizinho in atual.vizinhos:
            temp_g_score = g_score[atual] + 1
            if temp_g_score < g_score[vizinho]:
                veio_de[vizinho] = atual
                g_score[vizinho] = temp_g_score
                f_score[vizinho] = temp_g_score + h(vizinho.get_pos(), fim.get_pos())
                if vizinho not in conjunto_aberto_hash:
                    cont += 1
                    conjunto_aberto.put((f_score[vizinho], cont, vizinho))
                    conjunto_aberto_hash.add(vizinho)
                    if vizinho != fim: vizinho.fazer_aberto()
        
        if atual != inicio: atual.fazer_fechado()

def algoritmo_dijkstra(processar_passo, grade, inicio, fim):
    cont = 0
    fila_prioridade = PriorityQueue()
    fila_prioridade.put((0, cont, inicio))
    distancia = {nodo: float("inf") for linha in grade for nodo in linha}
    distancia[inicio] = 0
    veio_de = {}

    while not fila_prioridade.empty():
        if not processar_passo(): return
        dist, _, atual = fila_prioridade.get()

        if atual == fim:
            reconstruir_caminho(veio_de, fim, processar_passo)
            fim.fazer_fim(); inicio.fazer_inicio()
            return
        
        if dist > distancia[atual]: continue

        for vizinho in atual.vizinhos:
            nova_dist = distancia[atual] + 1
            if nova_dist < distancia[vizinho]:
                distancia[vizinho] = nova_dist
                veio_de[vizinho] = atual
                cont += 1
                fila_prioridade.put((nova_dist, cont, vizinho))
                if vizinho != fim: vizinho.fazer_aberto()
        
        if atual != inicio: atual.fazer_fechado()

def busca_gulosa(processar_passo, grade, inicio, fim):
    cont = 0
    fila_prioridade = PriorityQueue()
    fila_prioridade.put((h(inicio.get_pos(), fim.get_pos()), cont, inicio))
    veio_de = {}
    visitados = {inicio}

    while not fila_prioridade.empty():
        if not processar_passo(): return
        atual = fila_prioridade.get()[2]

        if atual == fim:
            reconstruir_caminho(veio_de, fim, processar_passo)
            fim.fazer_fim(); inicio.fazer_inicio()
            return

        for vizinho in atual.vizinhos:
            if vizinho not in visitados:
                visitados.add(vizinho)
                veio_de[vizinho] = atual
                cont += 1
                prioridade = h(vizinho.get_pos(), fim.get_pos())
                fila_prioridade.put((prioridade, cont, vizinho))
                if vizinho != fim: vizinho.fazer_aberto()
        
        if atual != inicio: atual.fazer_fechado()

def busca_largura(processar_passo, grade, inicio, fim):
    fila = Queue(); fila.put(inicio)
    veio_de = {}; visitados = {inicio}
    while not fila.empty():
        if not processar_passo(): return
        atual = fila.get()
        if atual == fim:
            reconstruir_caminho(veio_de, fim, processar_passo)
            fim.fazer_fim(); inicio.fazer_inicio()
            return
        for vizinho in atual.vizinhos:
            if vizinho not in visitados:
                veio_de[vizinho] = atual; visitados.add(vizinho)
                fila.put(vizinho)
                if vizinho != fim: vizinho.fazer_aberto()
        if atual != inicio: atual.fazer_fechado()

def busca_profundidade(processar_passo, grade, inicio, fim):
    pilha = [inicio]
    veio_de = {}
    visitados = {inicio}
    while pilha:
        if not processar_passo(): return
        atual = pilha.pop()
        if atual == fim:
            reconstruir_caminho(veio_de, fim, processar_passo)
            fim.fazer_fim(); inicio.fazer_inicio()
            return
        if atual != inicio: atual.fazer_fechado()
        for vizinho in reversed(atual.vizinhos):
            if vizinho not in visitados:
                visitados.add(vizinho)
                pilha.append(vizinho)
                veio_de[vizinho] = atual
                if vizinho != fim: vizinho.fazer_aberto()

# --- FUNÇÃO PRINCIPAL ---
def main(tela, largura_grade):
    LINHAS = 50
    grade = criar_grade(LINHAS, largura_grade)
    inicio = None
    fim = None
    estado_app = {"rodando": True, "algoritmo_ativo": False}

    def iniciar_algoritmo(algo_func):
        if not estado_app["algoritmo_ativo"] and inicio and fim:
            estado_app["algoritmo_ativo"] = True
            limpar_caminho()
            executar_algoritmo(algo_func, processar_passo_algoritmo, grade, inicio, fim)
            estado_app["algoritmo_ativo"] = False

    def parar_algoritmo(): estado_app["algoritmo_ativo"] = False

    def limpar_grade_completa():
        nonlocal inicio, fim, grade
        if not estado_app["algoritmo_ativo"]:
            inicio, fim = None, None
            grade = criar_grade(LINHAS, largura_grade)

    def limpar_caminho():
        if not estado_app["algoritmo_ativo"]:
            for linha in grade:
                for nodo in linha:
                    if nodo.is_aberto() or nodo.is_fechado() or nodo.is_caminho():
                        nodo.resetar()
            if inicio: inicio.fazer_inicio()
            if fim: fim.fazer_fim()
    
    def gerar_labirinto():
        if not estado_app["algoritmo_ativo"]:
            limpar_grade_completa()
            for linha in grade:
                for nodo in linha: nodo.fazer_obstaculo()
            
            pilha = [(random.randrange(1, LINHAS, 2), random.randrange(1, LINHAS, 2))]
            grade[pilha[0][0]][pilha[0][1]].resetar()

            while pilha:
                x, y = pilha[-1]
                vizinhos = []
                for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 < nx < LINHAS-1 and 0 < ny < LINHAS-1 and grade[nx][ny].is_obstaculo():
                        vizinhos.append((nx, ny))
                
                if vizinhos:
                    nx, ny = random.choice(vizinhos)
                    grade[(x + nx) // 2][(y + ny) // 2].resetar()
                    grade[nx][ny].resetar()
                    pilha.append((nx, ny))
                else:
                    pilha.pop()

    # --- CRIAÇÃO DA INTERFACE ---
    ui_elementos = {}
    y_pos = 20
    x_pos = LARGURA_TELA + 25
    largura_botao = LARGURA_PAINEL - 50
    altura_botao = 40
    margem_botao = 15
    margem_titulo = 40

    fonte_titulo = pygame.font.SysFont('segoeui', 22, bold=True)
    fonte_normal = pygame.font.SysFont('segoeui', 16)

    ui_elementos["titulo_algos"] = Label(x_pos, y_pos, "Algoritmos", fonte_titulo, COR["texto_titulo"])
    y_pos += margem_titulo
    algoritmos_botoes = [
        ("A* (A-Estrela)", lambda: iniciar_algoritmo(busca_a_estrela)),
        ("Dijkstra", lambda: iniciar_algoritmo(algoritmo_dijkstra)),
        ("Busca Gulosa", lambda: iniciar_algoritmo(busca_gulosa)),
        ("Busca em Largura (BFS)", lambda: iniciar_algoritmo(busca_largura)),
        ("Busca em Profundidade (DFS)", lambda: iniciar_algoritmo(busca_profundidade)),
    ]
    for i, (texto, acao) in enumerate(algoritmos_botoes):
        ui_elementos[f"btn_algo_{i}"] = Botao(x_pos, y_pos, largura_botao, altura_botao, texto, acao)
        y_pos += altura_botao + margem_botao

    y_pos += 10
    ui_elementos["titulo_controles"] = Label(x_pos, y_pos, "Controles", fonte_titulo, COR["texto_titulo"])
    y_pos += margem_titulo
    controles_botoes = [
        ("Parar Algoritmo", parar_algoritmo),
        ("Gerar Labirinto", gerar_labirinto),
        ("Limpar Caminho", limpar_caminho),
        ("Limpar Grade", limpar_grade_completa),
    ]
    for i, (texto, acao) in enumerate(controles_botoes):
        ui_elementos[f"btn_ctrl_{i}"] = Botao(x_pos, y_pos, largura_botao, altura_botao, texto, acao)
        y_pos += altura_botao + margem_botao

    y_pos += 10
    ui_elementos["titulo_velocidade"] = Label(x_pos, y_pos, "Velocidade", fonte_titulo, COR["texto_titulo"])
    y_pos += margem_titulo - 10
    ui_elementos["label_velocidade"] = Label(x_pos, y_pos, "Lento <---> Rápido", fonte_normal, COR["texto_normal"])
    y_pos += 25
    slider_velocidade = Slider(x_pos, y_pos, largura_botao, 15, 0, 50, 40)
    ui_elementos["slider_vel"] = slider_velocidade

    def processar_passo_algoritmo(desenhar_apenas_grelha=False):
        if not estado_app["algoritmo_ativo"]: return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                estado_app["rodando"] = False
                estado_app["algoritmo_ativo"] = False
                return False
            for elemento in ui_elementos.values():
                if isinstance(elemento, Botao) and elemento.texto == "Parar Algoritmo":
                    elemento.handle_event(event)

        if desenhar_apenas_grelha:
            for linha in grade:
                for nodo in linha:
                    if nodo.is_caminho(): nodo.desenhar(tela)
            pygame.display.update((LARGURA_TELA, 0, LARGURA_PAINEL, LARGURA_TELA))
        else:
            desenhar(tela, grade, LINHAS, largura_grade, ui_elementos, redesenhar_tudo=False)
        
        pygame.time.delay(slider_velocidade.get_valor())
        return True

    clock = pygame.time.Clock()
    while estado_app["rodando"]:
        clock.tick(60)
        
        if not estado_app["algoritmo_ativo"]:
            desenhar(tela, grade, LINHAS, largura_grade, ui_elementos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: estado_app["rodando"] = False
                
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < largura_grade:
                        linha, col = obter_pos_clicada(pos, LINHAS, largura_grade)
                        if linha != -1:
                            nodo = grade[linha][col]
                            if not inicio and nodo != fim: inicio = nodo; inicio.fazer_inicio()
                            elif not fim and nodo != inicio: fim = nodo; fim.fazer_fim()
                            elif nodo != fim and nodo != inicio: nodo.fazer_obstaculo()
                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < largura_grade:
                        linha, col = obter_pos_clicada(pos, LINHAS, largura_grade)
                        if linha != -1:
                            nodo = grade[linha][col]
                            if nodo == inicio: inicio = None
                            if nodo == fim: fim = None
                            nodo.resetar()
                
                for elemento in ui_elementos.values():
                    elemento.handle_event(event)
        else:
            # Loop de eventos simplificado enquanto o algoritmo roda
            for event in pygame.event.get():
                if event.type == pygame.QUIT: estado_app["rodando"] = False
                for elemento in ui_elementos.values():
                    if isinstance(elemento, Botao) and elemento.texto == "Parar Algoritmo":
                        elemento.handle_event(event) # Permite clicar em parar
            # Atualiza o painel para o hover do botão funcionar
            desenhar_painel(tela, ui_elementos)
            pygame.display.update((LARGURA_TELA, 0, LARGURA_PAINEL, LARGURA_TELA))

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    main(TELA, LARGURA_TELA)