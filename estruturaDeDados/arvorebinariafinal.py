import pygame
import sys
import time
import math

# --- Lógica da árvore binária manual ---

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        # Atributos para animação
        self.anim_scale = 0.0 # Para animação de inserção
        self.is_new = True

class ManualBinaryTree:
    def __init__(self):
        self.root = None
        self.highlight = None
        self.search_path = []
        self.selected_node = None # nó selecionado para inserção
        self.traversal_path = []

    def insert_root(self, key):
        """Insere o primeiro nó (raiz)"""
        if self.root is None:
            self.root = Node(key)
            return self.root
        return None

    def get_all_nodes(self):
        """Retorna todos os nós da árvore"""
        nodes = []
        self._collect_nodes(self.root, nodes)
        return nodes

    def _collect_nodes(self, node, nodes):
        if node is not None:
            nodes.append(node)
            self._collect_nodes(node.left, nodes)
            self._collect_nodes(node.right, nodes)

    def can_insert_left(self, node):
        """Verifica se pode inserir à esquerda do nó"""
        return node is not None and node.left is None

    def can_insert_right(self, node):
        """Verifica se pode inserir à direita do nó"""
        return node is not None and node.right is None

    def insert_left(self, parent_node, key):
        """Insere um nó à esquerda do nó pai"""
        if parent_node and parent_node.left is None:
            parent_node.left = Node(key)
            return parent_node.left
        return None

    def insert_right(self, parent_node, key):
        """Insere um nó à direita do nó pai"""
        if parent_node and parent_node.right is None:
            parent_node.right = Node(key)
            return parent_node.right
        return None

    def search(self, key):
        """Busca manual por um nó"""
        self.search_path = []
        path_nodes = []
        self.highlight = self._search(self.root, key.upper(), path_nodes)
        self.search_path = path_nodes # Atualiza o caminho completo de uma vez
        return self.highlight

    def _search(self, node, key, path):
        if node is None:
            return None
        
        path.append(node)
        
        if node.key.upper() == key:
            return node
        
        left_result = self._search(node.left, key, path)
        if left_result:
            return left_result
        
        right_result = self._search(node.right, key, path)
        if right_result:
            return right_result
        
        path.pop() # Remove o nó do caminho se não encontrou por aqui
        return None

    def delete_node(self, key):
        """Wrapper para iniciar a remoção de um nó"""
        self.root = self._delete_node_recursive(self.root, key.upper())
        self.highlight = None
        self.search_path = []

    def _delete_node_recursive(self, node, key):
        if node is None:
            return None

        if node.key.upper() == key:
            if node.left is None and node.right is None: return None
            if node.left is None: return node.right
            if node.right is None: return node.left
            
            rightmost = self._find_rightmost(node.left)
            node.key = rightmost.key
            node.left = self._delete_node_recursive(node.left, rightmost.key)
        else:
             node.left = self._delete_node_recursive(node.left, key)
             node.right = self._delete_node_recursive(node.right, key)
        return node

    def _find_rightmost(self, node):
        while node.right:
            node = node.right
        return node
        
    def pre_order(self):
        path = []
        self._pre_order_recursive(self.root, path)
        self.traversal_path = path
        return path

    def _pre_order_recursive(self, node, path):
        if node:
            path.append(node) # Raiz
            self._pre_order_recursive(node.left, path) # Esquerda
            self._pre_order_recursive(node.right, path) # Direita

    def in_order(self):
        path = []
        self._in_order_recursive(self.root, path)
        self.traversal_path = path
        return path

    def _in_order_recursive(self, node, path):
        if node:
            self._in_order_recursive(node.left, path) # Esquerda
            path.append(node) # Raiz
            self._in_order_recursive(node.right, path) # Direita

    def post_order(self):
        path = []
        self._post_order_recursive(self.root, path)
        self.traversal_path = path
        return path

    def _post_order_recursive(self, node, path):
        if node:
            self._post_order_recursive(node.left, path) # Esquerda
            self._post_order_recursive(node.right, path) # Direita
            path.append(node) # Raiz
            
    def clear_highlights(self):
        self.highlight = None
        self.search_path = []
        self.traversal_path = []


# --- Configurações do Pygame ---
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualizador de Árvore Binária")
try:
    font = pygame.font.SysFont('Segoe UI', 22)
    title_font = pygame.font.SysFont('Segoe UI', 36, bold=True)
    button_font = pygame.font.SysFont('Segoe UI', 18)
    small_font = pygame.font.SysFont('Segoe UI', 14)
except pygame.error:
    font = pygame.font.SysFont('Arial', 20)
    title_font = pygame.font.SysFont('Arial', 32, bold=True)
    button_font = pygame.font.SysFont('Arial', 18)
    small_font = pygame.font.SysFont('Arial', 12)


# Paleta de Cores
COLOR_BG_START = (240, 245, 249)
COLOR_BG_END = (219, 228, 235)
BLACK = (10, 10, 10)
GRAY_DARK = (80, 80, 80)
GRAY_LIGHT = (200, 200, 200)
WHITE = (255, 255, 255)
NODE_BLUE = (39, 102, 184)
NODE_GREEN = (46, 184, 114)
NODE_RED = (232, 67, 67)
NODE_YELLOW = (248, 199, 52)
NODE_PURPLE = (155, 89, 182)
NODE_ORANGE = (230, 126, 34)

tree = ManualBinaryTree()

## ALTERAÇÃO ##: Função para criar uma árvore de exemplo
def create_example_tree():
    """Cria e retorna uma nova árvore completa de 4 níveis."""
    new_tree = ManualBinaryTree()
    # 15 nós para uma árvore completa de 4 níveis (1+2+4+8)
    keys = [chr(ord('A') + i) for i in range(15)]
    
    if not keys:
        return new_tree
    
    # Cria a raiz
    new_tree.root = Node(keys[0])
    
    # Fila para inserção em largura (nível por nível)
    queue = [new_tree.root]
    key_index = 1
    
    while queue and key_index < len(keys):
        parent_node = queue.pop(0)
        
        # Insere filho à esquerda
        if key_index < len(keys):
            new_node = Node(keys[key_index])
            parent_node.left = new_node
            queue.append(new_node)
            key_index += 1
            
        # Insere filho à direita
        if key_index < len(keys):
            new_node = Node(keys[key_index])
            parent_node.right = new_node
            queue.append(new_node)
            key_index += 1
            
    # Garante que todos os nós tenham a animação de 'crescimento'
    for node in new_tree.get_all_nodes():
        node.anim_scale = 0.0
        node.is_new = True
        
    return new_tree


# --- Classes para Interface ---
class Button:
    def __init__(self, x, y, width, height, text, color=NODE_BLUE, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False
        self.enabled = True

    def draw(self, screen):
        color = self.color
        if not self.enabled:
            color = GRAY_LIGHT
        
        shadow_rect = self.rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, GRAY_DARK, shadow_rect, border_radius=8)

        current_color = color
        if self.hovered and self.enabled:
            current_color = tuple(min(255, c + 25) for c in self.color)
        
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)

        text_surf = button_font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if not self.enabled:
            self.hovered = False
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                return True
        return False

class InputBox:
    def __init__(self, x, y, width, height, prompt=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WHITE
        self.text = ''
        self.prompt = prompt
        self.active = True
        self.border_color = BLACK

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isalpha() and len(self.text) < 1:
                self.text = event.unicode.upper()
        return None

    def draw(self, screen):
        self.border_color = NODE_ORANGE if self.active else BLACK
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=5)
        if self.prompt:
            prompt_surf = font.render(self.prompt, True, BLACK)
            screen.blit(prompt_surf, (self.rect.x, self.rect.y - 30))
        text_surf = font.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 5))

# --- Criar interface ---
## ALTERAÇÃO ##: Adicionado botão "Árvore Exemplo"
buttons = {
    'add_root': Button(20, 60, 140, 40, "Adicionar Raiz", NODE_GREEN),
    'left': Button(170, 60, 120, 40, "← Esquerda", NODE_BLUE),
    'right': Button(300, 60, 120, 40, "Direita →", NODE_BLUE),
    'search': Button(430, 60, 100, 40, "Buscar", NODE_PURPLE),
    'delete': Button(540, 60, 100, 40, "Deletar", NODE_RED),
    'clear': Button(650, 60, 100, 40, "Limpar", GRAY_DARK),
    'build_example': Button(760, 60, 140, 40, "Árvore Exemplo", NODE_GREEN),
    
    'pre_order': Button(940, 60, 100, 40, "Pré-Ordem", NODE_PURPLE),
    'in_order': Button(1050, 60, 100, 40, "Em-Ordem", NODE_PURPLE),
    'post_order': Button(1160, 60, 100, 40, "Pós-Ordem", NODE_PURPLE),
}

input_box = InputBox(20, 145, 80, 35, "Letra:")
message = ""
message_color = BLACK
message_timer = 0

# --- Lógica de Animação ---
search_animation = False
animation_step = 0
animation_speed = 0.05

traversal_animation = False
traversal_step = 0
## ALTERAÇÃO ##: Velocidade da travessia reduzida para ser mais fácil de acompanhar.
traversal_speed = 0.05 # Valor menor = animação mais lenta

node_to_delete = None
key_to_delete = None
delete_anim_progress = 0.0

def start_search_animation():
    global search_animation, animation_step, traversal_animation
    if tree.search_path:
        traversal_animation = False
        search_animation = True
        animation_step = 0

def start_traversal_animation():
    global traversal_animation, traversal_step, search_animation
    if tree.traversal_path:
        search_animation = False
        traversal_animation = True
        traversal_step = 0

def start_delete_animation(node, key):
    global node_to_delete, key_to_delete, delete_anim_progress
    if node:
        node_to_delete = node
        key_to_delete = key
        delete_anim_progress = 1.0

def update_animations(dt):
    global search_animation, animation_step, delete_anim_progress, node_to_delete, key_to_delete, message_timer
    global traversal_animation, traversal_step

    if message_timer > 0: message_timer -= dt
    if search_animation:
        animation_step += animation_speed * 60 * dt
        if animation_step >= len(tree.search_path): search_animation = False
    if traversal_animation:
        traversal_step += traversal_speed * 60 * dt
        if traversal_step >= len(tree.traversal_path): traversal_animation = False
    if node_to_delete:
        delete_anim_progress -= 2.0 * dt
        if delete_anim_progress <= 0:
            tree.delete_node(key_to_delete)
            node_to_delete = None
    for node in tree.get_all_nodes():
        if node.is_new:
            node.anim_scale += 3.0 * dt
            if node.anim_scale >= 1.0:
                node.anim_scale = 1.0
                node.is_new = False

# --- Desenhar a árvore ---
def get_node_at_position(x, y):
    if not tree.root: return None
    return _find_node_at_pos(tree.root, WIDTH // 2, 250, 320, x, y)

def _find_node_at_pos(node, nx, ny, dx, x, y):
    if node is None: return None
    radius = 30 * node.anim_scale
    if ((x - nx) ** 2 + (y - ny) ** 2) ** 0.5 <= radius: return node
    if node.left:
        res = _find_node_at_pos(node.left, nx - dx, ny + 90, dx / 1.8, x, y)
        if res: return res
    if node.right:
        res = _find_node_at_pos(node.right, nx + dx, ny + 90, dx / 1.8, x, y)
        if res: return res
    return None

def draw_node(node, x, y, dx):
    if node is None: return

    if node == node_to_delete:
        alpha = max(0, int(255 * delete_anim_progress))
        scale = max(0, delete_anim_progress)
        temp_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(temp_surf, (*NODE_RED, alpha), (30, 30), int(30 * scale))
        screen.blit(temp_surf, (x - 30, y - 30))
        if node.left: pygame.draw.line(screen, GRAY_DARK, (x, y), (x - dx, y + 90), 3)
        if node.right: pygame.draw.line(screen, GRAY_DARK, (x, y), (x + dx, y + 90), 3)
        return

    if node.left:
        pygame.draw.line(screen, GRAY_DARK, (x, y), (x - dx, y + 90), 3)
        draw_node(node.left, x - dx, y + 90, dx / 1.8)
    if node.right:
        pygame.draw.line(screen, GRAY_DARK, (x, y), (x + dx, y + 90), 3)
        draw_node(node.right, x + dx, y + 90, dx / 1.8)

    color, pulse = NODE_BLUE, 1.0
    current_traversal_node = traversal_animation and int(traversal_step) < len(tree.traversal_path) and node == tree.traversal_path[int(traversal_step)]
    current_search_node = search_animation and int(animation_step) < len(tree.search_path) and node == tree.search_path[int(animation_step)]

    if node == tree.selected_node: color = NODE_ORANGE
    elif node == tree.highlight: color = NODE_GREEN
    elif current_traversal_node or current_search_node:
        color = NODE_YELLOW
        pulse = 1.0 + 0.15 * abs(math.sin(time.time() * 10))
    elif tree.traversal_path and node in tree.traversal_path[:int(traversal_step)]: color = NODE_PURPLE
    elif tree.search_path and node in tree.search_path[:int(animation_step)]: color = NODE_PURPLE

    radius = int(30 * node.anim_scale * pulse)
    if radius <= 0: return

    pygame.draw.circle(screen, color, (x, y), radius)
    pygame.draw.circle(screen, BLACK, (x, y), radius, 3)
    text_color = WHITE if color != NODE_YELLOW else BLACK
    text_surf = font.render(str(node.key), True, text_color)
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)

def show_tree():
    if tree.root:
        draw_node(tree.root, WIDTH // 2, 250, 320)

def draw_interface():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = tuple(int(s * (1 - ratio) + e * ratio) for s, e in zip(COLOR_BG_START, COLOR_BG_END))
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    title_surf = title_font.render("Visualizador de Árvore Binária", True, BLACK)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 10))

    panel_rect = pygame.Rect(10, 50, WIDTH - 20, 140)
    pygame.draw.rect(screen, (*WHITE, 180), panel_rect, border_radius=10)
    pygame.draw.rect(screen, GRAY_DARK, panel_rect, 2, border_radius=10)
    
    ops_label = small_font.render("Operações:", True, GRAY_DARK); screen.blit(ops_label, (20, 110))
    trav_label = small_font.render("Travessias:", True, GRAY_DARK); screen.blit(trav_label, (940, 110))
    
    buttons['add_root'].enabled = tree.root is None
    can_insert = tree.selected_node and input_box.text != ''
    buttons['left'].enabled = can_insert and tree.can_insert_left(tree.selected_node)
    buttons['right'].enabled = can_insert and tree.can_insert_right(tree.selected_node)
    traversal_enabled = tree.root is not None
    for b_name in ['pre_order', 'in_order', 'post_order']: buttons[b_name].enabled = traversal_enabled
    for button in buttons.values(): button.draw(screen)
    input_box.draw(screen)

    if message and message_timer > 0:
        alpha = min(255, int(255 * (message_timer / 2.0)))
        msg_surf = font.render(message, True, message_color)
        temp_surf = pygame.Surface(msg_surf.get_size(), pygame.SRCALPHA)
        temp_surf.blit(msg_surf, (0,0)); temp_surf.set_alpha(alpha)
        screen.blit(temp_surf, (input_box.rect.right + 20, 150))
    
def set_message(text, color, duration=3.0):
    global message, message_color, message_timer
    message, message_color, message_timer = text, color, duration

def reset_animations_and_highlights():
    global search_animation, traversal_animation
    search_animation = traversal_animation = False
    tree.clear_highlights()

# --- Loop principal ---
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if input_result := input_box.handle_event(event):
            if tree.root is None:
                if new_node := tree.insert_root(input_result.upper()):
                    set_message(f"Raiz '{new_node.key}' adicionada!", NODE_GREEN)
                    input_box.text = ''
            else: set_message("Para inserir, clique em um nó e use os botões.", NODE_ORANGE)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[1] > 200:
                if clicked_node := get_node_at_position(event.pos[0], event.pos[1]):
                    tree.selected_node = clicked_node
                    reset_animations_and_highlights()
                    set_message(f"Nó '{clicked_node.key}' selecionado para inserção.", NODE_ORANGE)
                elif not any(b.rect.collidepoint(event.pos) for b in buttons.values()):
                    tree.selected_node = None

        for name, button in buttons.items():
            if button.handle_event(event):
                reset_animations_and_highlights()
                value = input_box.text.upper()

                if name == 'add_root' and value:
                    if new_node := tree.insert_root(value):
                        set_message(f"Raiz '{new_node.key}' adicionada!", NODE_GREEN)
                        input_box.text = ''
                
                elif name in ('left', 'right') and value and tree.selected_node:
                    new_node = tree.insert_left(tree.selected_node, value) if name == 'left' else tree.insert_right(tree.selected_node, value)
                    if new_node:
                        set_message(f"'{value}' inserido em '{tree.selected_node.key}'", NODE_GREEN)
                        input_box.text = ''
                        tree.selected_node = None
                
                elif name == 'search' and value:
                    if tree.search(value):
                        set_message(f"Letra '{value}' encontrada!", NODE_GREEN)
                        start_search_animation()
                    else: set_message(f"Letra '{value}' não encontrada!", NODE_RED)
                    input_box.text = ''
                
                elif name == 'delete' and value:
                    if node_to_del := tree.search(value):
                        is_leaf = node_to_del.left is None and node_to_del.right is None
                        has_one_child = (node_to_del.left is None) != (node_to_del.right is None)
                        msg = f"Excluindo nó FOLHA '{value}'..." if is_leaf else f"Excluindo '{value}' (com 1 FILHO)..." if has_one_child else f"Excluindo '{value}' (com 2 FILHOS)..."
                        set_message(msg, NODE_RED)
                        start_delete_animation(node_to_del, value)
                    else: set_message(f"Letra '{value}' não encontrada para deletar!", NODE_RED)
                    input_box.text = ''
                
                elif name == 'clear':
                    tree = ManualBinaryTree()
                    set_message("Árvore limpa!", GRAY_DARK)
                    input_box.text = ''
                
                ## ALTERAÇÃO ##: Lógica para o botão de construir árvore exemplo
                elif name == 'build_example':
                    tree = create_example_tree()
                    set_message("Árvore de exemplo com 4 níveis criada!", NODE_GREEN)
                    
                elif name == 'pre_order':
                    tree.pre_order()
                    set_message("Iniciando travessia Pré-Ordem...", NODE_PURPLE)
                    start_traversal_animation()
                
                elif name == 'in_order':
                    tree.in_order()
                    set_message("Iniciando travessia Em-Ordem...", NODE_PURPLE)
                    start_traversal_animation()

                elif name == 'post_order':
                    tree.post_order()
                    set_message("Iniciando travessia Pós-Ordem...", NODE_PURPLE)
                    start_traversal_animation()

    update_animations(dt)
    draw_interface()
    show_tree()
    pygame.display.flip()

pygame.quit()
sys.exit()