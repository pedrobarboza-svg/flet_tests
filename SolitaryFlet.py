import random
import flet as ft


# ============================================================
# CONFIGURAÇÕES
# ============================================================

CARD_WIDTH = 72
CARD_HEIGHT = 102

CARD_OFFSET = 25
DROP_PROXIMITY = 45

GAME_WIDTH = 900
GAME_HEIGHT = 650

GREEN = "#087443"
GREEN_DARK = "#075B35"

WHITE = "#FFFFFF"
BLACK = "#111111"
RED = "#D32F2F"

SLOT_BORDER = "#6FA98B"


# ============================================================
# SUITE
# ============================================================

class Suite:

    def __init__(self, name, symbol, color):
        self.name = name
        self.symbol = symbol
        self.color = color


# ============================================================
# RANK
# ============================================================

class Rank:

    def __init__(self, name, value):
        self.name = name
        self.value = value


# ============================================================
# SLOT
# ============================================================

class Slot(ft.Container):

    def __init__(
        self,
        solitaire,
        top,
        left,
        border=True,
    ):
        super().__init__()

        self.solitaire = solitaire

        self.pile = []

        self.width = CARD_WIDTH
        self.height = CARD_HEIGHT

        self.top = top
        self.left = left

        self.border_radius = 8

        if border:
            self.border = ft.Border.all(
                1,
                SLOT_BORDER
            )

        self.bgcolor = GREEN_DARK

        self.on_click = self.click

    # --------------------------------------------------------
    # CARTA DO TOPO
    # --------------------------------------------------------

    def get_top_card(self):

        if len(self.pile) > 0:
            return self.pile[-1]

        return None

    # --------------------------------------------------------
    # CLICK
    # --------------------------------------------------------

    def click(self, e):

        if self == self.solitaire.stock:

            self.solitaire.draw_stock()


# ============================================================
# CARD
# ============================================================

class Card(ft.GestureDetector):

    def __init__(
        self,
        solitaire,
        suite,
        rank,
    ):

        super().__init__()

        self.solitaire = solitaire

        self.suite = suite
        self.rank = rank

        self.slot = None

        self.face_up = False

        self.top = 0
        self.left = 0

        self.draggable_pile = [self]

        self.mouse_cursor = ft.MouseCursor.MOVE

        self.drag_interval = 5

        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.drop

        self.on_tap = self.click
        self.on_double_tap = self.double_click

        self.content = self.create_card()

    # ========================================================
    # CRIAR VISUAL DA CARTA
    # ========================================================

    def create_card(self):

        if not self.face_up:

            return ft.Container(

                width=CARD_WIDTH,
                height=CARD_HEIGHT,

                bgcolor="#5145A8",

                border=ft.Border.all(
                    1,
                    "#FFFFFF"
                ),

                border_radius=8,

                alignment=ft.Alignment.CENTER,

                content=ft.Column(

                    horizontal_alignment=
                    ft.CrossAxisAlignment.CENTER,

                    alignment=
                    ft.MainAxisAlignment.CENTER,

                    spacing=2,

                    controls=[

                        ft.Text(
                            "♠",
                            size=14,
                            color="#FFFFFF",
                        ),

                        ft.Text(
                            "♦",
                            size=14,
                            color="#FFFFFF",
                        ),

                        ft.Text(
                            "♣",
                            size=14,
                            color="#FFFFFF",
                        ),

                        ft.Text(
                            "♥",
                            size=14,
                            color="#FFFFFF",
                        ),

                    ],
                ),
            )

        return ft.Container(

            width=CARD_WIDTH,
            height=CARD_HEIGHT,

            bgcolor=WHITE,

            border=ft.Border.all(
                1,
                "#555555"
            ),

            border_radius=8,

            padding=5,

            content=ft.Column(

                spacing=0,

                controls=[

                    ft.Text(
                        f"{self.rank.name}"
                        f"{self.suite.symbol}",

                        size=18,

                        weight=
                        ft.FontWeight.BOLD,

                        color=self.suite.color,
                    ),

                    ft.Container(
                        expand=True
                    ),

                    ft.Text(
                        self.suite.symbol,

                        size=34,

                        color=self.suite.color,

                        text_align=
                        ft.TextAlign.CENTER,
                    ),

                ],
            ),
        )

    # ========================================================
    # ATUALIZAR VISUAL
    # ========================================================

    def refresh(self):

        self.content = self.create_card()

        self.solitaire.update()

    # ========================================================
    # VIRAR PARA CIMA
    # ========================================================

    def turn_face_up(self):

        self.face_up = True

        self.content = self.create_card()

        self.solitaire.update()

    # ========================================================
    # VIRAR PARA BAIXO
    # ========================================================

    def turn_face_down(self):

        self.face_up = False

        self.content = self.create_card()

        self.solitaire.update()

    # ========================================================
    # PILHA ARRASTÁVEL
    # ========================================================

    def get_draggable_pile(self):

        if (

            self.slot is not None

            and

            self.slot != self.solitaire.stock

            and

            self.slot != self.solitaire.waste

        ):

            index = self.slot.pile.index(
                self
            )

            self.draggable_pile = (
                self.slot.pile[index:]
            )

        else:

            self.draggable_pile = [
                self
            ]

    # ========================================================
    # MOVER PARA FRENTE
    # ========================================================

    def move_on_top(self):

        for card in self.draggable_pile:

            if card in self.solitaire.controls:

                self.solitaire.controls.remove(
                    card
                )

            self.solitaire.controls.append(
                card
            )

        self.solitaire.update()

    # ========================================================
    # INÍCIO DO DRAG
    # ========================================================

    def start_drag(
        self,
        e: ft.DragStartEvent
    ):

        if not self.face_up:
            return

        self.get_draggable_pile()

        self.move_on_top()

    # ========================================================
    # DRAG
    # ========================================================

    def drag(
        self,
        e: ft.DragUpdateEvent
    ):

        if not self.face_up:
            return

        new_top = max(
            0,
            self.top + e.local_delta.y
        )

        new_left = max(
            0,
            self.left + e.local_delta.x
        )

        for index, card in enumerate(
            self.draggable_pile
        ):

            card.top = (
                new_top
                + index * CARD_OFFSET
            )

            card.left = new_left

        self.solitaire.update()

    # ========================================================
    # DROP
    # ========================================================

    def drop(
        self,
        e: ft.DragEndEvent
    ):

        if not self.face_up:
            return

        # ----------------------------------------------------
        # TABLEAU
        # ----------------------------------------------------

        for slot in self.solitaire.tableau:

            target_top = (
                slot.top
                + len(slot.pile)
                * CARD_OFFSET
            )

            if (

                abs(
                    self.top - target_top
                )
                < DROP_PROXIMITY

                and

                abs(
                    self.left - slot.left
                )
                < DROP_PROXIMITY

                and

                self.solitaire.check_tableau_rules(
                    self,
                    slot
                )

            ):

                self.place(slot)

                return

        # ----------------------------------------------------
        # FOUNDATION
        # ----------------------------------------------------

        if len(
            self.draggable_pile
        ) == 1:

            for slot in (
                self.solitaire.foundations
            ):

                if (

                    abs(
                        self.top - slot.top
                    )
                    < DROP_PROXIMITY

                    and

                    abs(
                        self.left - slot.left
                    )
                    < DROP_PROXIMITY

                    and

                    self.solitaire.check_foundation_rules(
                        self,
                        slot
                    )

                ):

                    self.place(slot)

                    return

        # ----------------------------------------------------
        # NÃO ACEITOU
        # ----------------------------------------------------

        self.bounce_back()

    # ========================================================
    # COLOCAR CARTA
    # ========================================================

    def place(self, slot):

        old_slots = set()

        # Guardar slots antigos
        for card in self.draggable_pile:

            if card.slot is not None:

                old_slots.add(
                    card.slot
                )

        # Remover da pilha antiga
        for card in self.draggable_pile:

            if (

                card.slot is not None

                and

                card in card.slot.pile

            ):

                card.slot.pile.remove(
                    card
                )

        # Adicionar na nova pilha
        for card in self.draggable_pile:

            card.slot = slot

            slot.pile.append(
                card
            )

        # Posicionar cartas
        start_index = (
            len(slot.pile)
            - len(self.draggable_pile)
        )

        for index, card in enumerate(
            self.draggable_pile
        ):

            if slot in self.solitaire.tableau:

                card.top = (
                    slot.top
                    + (
                        start_index
                        + index
                    )
                    * CARD_OFFSET
                )

            else:

                card.top = slot.top

            card.left = slot.left

        # Revelar carta que ficou por baixo
        for old_slot in old_slots:

            if old_slot in (
                self.solitaire.tableau
            ):

                top_card = (
                    old_slot.get_top_card()
                )

                if (

                    top_card is not None

                    and

                    not top_card.face_up

                ):

                    top_card.turn_face_up()

        self.solitaire.update()

        # Verificar vitória
        if self.solitaire.check_win():

            self.solitaire.winning_sequence()

    # ========================================================
    # VOLTAR
    # ========================================================

    def bounce_back(self):

        if self.slot is None:
            return

        for index, card in enumerate(
            self.slot.pile
        ):

            if self.slot in (
                self.solitaire.tableau
            ):

                card.top = (
                    self.slot.top
                    + index * CARD_OFFSET
                )

            else:

                card.top = self.slot.top

            card.left = self.slot.left

        self.solitaire.update()

    # ========================================================
    # CLICK
    # ========================================================

    def click(self, e):

        # Carta virada para baixo no tableau
        if self.slot in (
            self.solitaire.tableau
        ):

            if (

                not self.face_up

                and

                self == self.slot.get_top_card()

            ):

                self.turn_face_up()

                return

    # ========================================================
    # DOUBLE CLICK
    # ========================================================

    def double_click(self, e):

        if not self.face_up:
            return

        self.get_draggable_pile()

        if len(
            self.draggable_pile
        ) != 1:

            return

        for slot in (
            self.solitaire.foundations
        ):

            if self.solitaire.check_foundation_rules(
                self,
                slot
            ):

                self.move_on_top()

                self.place(slot)

                return


# ============================================================
# SOLITAIRE
# ============================================================

class Solitaire(ft.Stack):

    def __init__(self):

        super().__init__()

        self.width = GAME_WIDTH
        self.height = GAME_HEIGHT

        self.controls = []

        self.cards = []

        self.tableau = []

        self.foundations = []

        self.stock = None
        self.waste = None

        self.game_over = False

    # ========================================================
    # MOUNT
    # ========================================================

    def did_mount(self):

        self.create_deck()

        self.create_slots()

        self.deal_cards()

    # ========================================================
    # CRIAR BARALHO
    # ========================================================

    def create_deck(self):

        suites = [

            Suite(
                "hearts",
                "♥",
                RED
            ),

            Suite(
                "diamonds",
                "♦",
                RED
            ),

            Suite(
                "clubs",
                "♣",
                BLACK
            ),

            Suite(
                "spades",
                "♠",
                BLACK
            ),

        ]

        ranks = [

            Rank("A", 1),

            Rank("2", 2),

            Rank("3", 3),

            Rank("4", 4),

            Rank("5", 5),

            Rank("6", 6),

            Rank("7", 7),

            Rank("8", 8),

            Rank("9", 9),

            Rank("10", 10),

            Rank("J", 11),

            Rank("Q", 12),

            Rank("K", 13),

        ]

        self.cards = []

        for suite in suites:

            for rank in ranks:

                self.cards.append(

                    Card(
                        self,
                        suite,
                        rank
                    )

                )

    # ========================================================
    # CRIAR SLOTS
    # ========================================================

    def create_slots(self):

        # ----------------------------------------------------
        # STOCK
        # ----------------------------------------------------

        self.stock = Slot(
            self,
            top=20,
            left=20,
            border=True
        )

        # ----------------------------------------------------
        # WASTE
        # ----------------------------------------------------

        self.waste = Slot(
            self,
            top=20,
            left=120,
            border=False
        )

        # ----------------------------------------------------
        # FOUNDATIONS
        # ----------------------------------------------------

        self.foundations = []

        for i in range(4):

            self.foundations.append(

                Slot(
                    self,
                    top=20,
                    left=500 + i * 100,
                    border=True
                )

            )

        # ----------------------------------------------------
        # TABLEAU
        # ----------------------------------------------------

        self.tableau = []

        for i in range(7):

            self.tableau.append(

                Slot(
                    self,
                    top=160,
                    left=20 + i * 100,
                    border=False
                )

            )

        # ----------------------------------------------------
        # ADICIONAR SLOTS
        # ----------------------------------------------------

        self.controls.append(
            self.stock
        )

        self.controls.append(
            self.waste
        )

        self.controls.extend(
            self.foundations
        )

        self.controls.extend(
            self.tableau
        )

        self.update()

    # ========================================================
    # DISTRIBUIR CARTAS
    # ========================================================

    def deal_cards(self):

        random.shuffle(
            self.cards
        )

        # Colocar cartas nos controles
        self.controls.extend(
            self.cards
        )

        index = 0

        # ----------------------------------------------------
        # DISTRIBUIÇÃO DO TABLEAU
        # ----------------------------------------------------

        for column in range(7):

            slot = self.tableau[column]

            for row in range(
                column + 1
            ):

                card = self.cards[index]

                index += 1

                card.slot = slot

                slot.pile.append(
                    card
                )

                card.top = (
                    slot.top
                    + row * CARD_OFFSET
                )

                card.left = (
                    slot.left
                )

                card.draggable_pile = [
                    card
                ]

                # Somente a última carta
                # fica virada para cima
                if row == column:

                    card.turn_face_up()

        # ----------------------------------------------------
        # RESTANTE → STOCK
        # ----------------------------------------------------

        while index < len(
            self.cards
        ):

            card = self.cards[index]

            index += 1

            card.slot = self.stock

            self.stock.pile.append(
                card
            )

            card.top = self.stock.top

            card.left = self.stock.left

            card.draggable_pile = [
                card
            ]

        self.update()

    # ========================================================
    # COMPRAR CARTA DO STOCK
    # ========================================================

    def draw_stock(self):

        # ----------------------------------------------------
        # STOCK VAZIO → DEVOLVE WASTE
        # ----------------------------------------------------

        if not self.stock.pile:

            self.restart_stock()

            return

        # ----------------------------------------------------
        # PEGAR CARTA
        # ----------------------------------------------------

        card = self.stock.get_top_card()

        if card is None:
            return

        self.stock.pile.remove(
            card
        )

        card.slot = self.waste

        self.waste.pile.append(
            card
        )

        card.top = self.waste.top

        card.left = self.waste.left

        card.turn_face_up()

        self.controls.remove(
            card
        )

        self.controls.append(
            card
        )

        self.update()

    # ========================================================
    # DEVOLVER WASTE PARA STOCK
    # ========================================================

    def restart_stock(self):

        while self.waste.pile:

            card = (
                self.waste.get_top_card()
            )

            self.waste.pile.remove(
                card
            )

            card.turn_face_down()

            card.slot = self.stock

            self.stock.pile.append(
                card
            )

            card.top = self.stock.top

            card.left = self.stock.left

        self.update()

    # ========================================================
    # REGRA TABLEAU
    # ========================================================

    def check_tableau_rules(
        self,
        card,
        slot
    ):

        top_card = (
            slot.get_top_card()
        )

        # Coluna vazia
        if top_card is None:

            return (
                card.rank.value == 13
            )

        # Cores alternadas
        different_color = (
            card.suite.color
            != top_card.suite.color
        )

        # Ordem decrescente
        correct_value = (
            card.rank.value
            == top_card.rank.value - 1
        )

        # Topo precisa estar aberto
        top_is_face_up = (
            top_card.face_up
        )

        return (
            different_color
            and correct_value
            and top_is_face_up
        )

    # ========================================================
    # REGRA FOUNDATION
    # ========================================================

    def check_foundation_rules(
        self,
        card,
        slot
    ):

        # Não permitir pilha de cartas
        if len(
            card.draggable_pile
        ) != 1:

            return False

        top_card = (
            slot.get_top_card()
        )

        # Fundação vazia → Ás
        if top_card is None:

            return (
                card.rank.value == 1
            )

        # Mesmo naipe
        same_suit = (
            card.suite.name
            == top_card.suite.name
        )

        # Próximo número
        next_value = (
            card.rank.value
            == top_card.rank.value + 1
        )

        return (
            same_suit
            and next_value
        )

    # ========================================================
    # VERIFICAR VITÓRIA
    # ========================================================

    def check_win(self):

        total = 0

        for slot in (
            self.foundations
        ):

            total += len(
                slot.pile
            )

        return total == 52

    # ========================================================
    # VITÓRIA
    # ========================================================

    def winning_sequence(self):

        if self.game_over:
            return

        self.game_over = True

        dialog = ft.AlertDialog(

            title=ft.Text(
                "🎉 Parabéns!"
            ),

            content=ft.Text(
                "Você venceu o Solitaire!"
            ),

            actions=[

                ft.TextButton(
                    "OK",
                    on_click=lambda e:
                    self.close_dialog(
                        dialog
                    )
                )

            ],
        )

        self.page.show_dialog(
            dialog
        )

    # ========================================================
    # FECHAR DIÁLOGO
    # ========================================================

    def close_dialog(
        self,
        dialog
    ):

        dialog.open = False

        self.page.update()


# ============================================================
# MAIN
# ============================================================

def main(page: ft.Page):

    page.title = "Solitaire"

    page.bgcolor = GREEN

    page.padding = 10

    page.horizontal_alignment = (
        ft.CrossAxisAlignment.CENTER
    )

    page.vertical_alignment = (
        ft.MainAxisAlignment.CENTER
    )

    game = Solitaire()

    page.add(game)


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":
    ft.run(main)