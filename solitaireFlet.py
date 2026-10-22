import flet as ft


# 1. ESTADO GLOBAL
class Solitaire:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0


solitaire = Solitaire()


def main(page: ft.Page):
    # 2. FUNÇÕES DE LÓGICA (Devidamente indentadas)
    def start_drag(e: ft.DragStartEvent):
        """Guarda as coordenadas iniciais da carta"""
        solitaire.start_top = e.control.top
        solitaire.start_left = e.control.left
        e.control.update()

    def drag(e: ft.DragUpdateEvent):
        """Movimenta a carta ao arrastar"""
        e.control.top = max(0, e.control.top + e.local_delta.y)
        e.control.left = max(0, e.control.left + e.local_delta.x)
        e.control.update()

    def place(card, slot):
        """Encaixa a carta perfeitamente no slot"""
        card.top = slot.top
        card.left = slot.left
        page.update()

    def bounce_back(game, card):
        """Devolve a carta à posição inicial se não acertar no slot"""
        card.top = game.start_top
        card.left = game.start_left
        page.update()

    def drop(e: ft.DragEndEvent):
        """Gere a lógica ao soltar a carta"""
        if (
            abs(e.control.top - slot.top) < 20
            and abs(e.control.left - slot.left) < 20
        ):
            place(e.control, slot)  # Encaixa no slot se estiver próximo (<20px)
        else:
            bounce_back(solitaire, e.control)  # Volta à origem se soltar fora

        e.control.update()

    # 3. COMPONENTES VISUAIS
    slot = ft.Container(
        width=70, height=100, left=200, top=0, border=ft.Border.all(1)
    )

    card = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,  # Regista o início do arrasto
        on_pan_update=drag,  # Executa o movimento
        on_pan_end=drop,  # Aplica o encaixe ou retorno ao soltar
        left=0,
        top=0,
        content=ft.Container(bgcolor=ft.Colors.GREEN, width=70, height=100),
    )

    # 4. ADICIONAR À TELA
    page.add(ft.Stack(controls=[slot, card], width=1000, height=500))


# 5. INICIAR APLICAÇÃO (Colado à esquerda)
ft.app(target=main)