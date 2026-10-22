import flet as ft

class Solitaire:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0

solitaire = Solitaire()

def start_drag(e: ft.DragStartEvent):
    solitaire.start_top = e.control.top
    solitaire.start_left = e.control.left
    e.control.update()

def main(page: ft.Page):
    def drag(e: ft.DragUpdateEvent):
        ...



    def drag(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.local_delta.y)
        e.control.left = max(0, e.control.left + e.local_delta.x)
        e.control.update()



    def place(card, slot):
        """place card to the slot"""
    card.top = slot.top
    card.left = slot.left
    page.update()

    def bounce_back(game, card):
        """return card to its original position"""
        card.top = game.start_top
        card.left = game.start_left
    page.update()

    def drop(e: ft.DragEndEvent):
     if (
        abs(e.control.top - slot.top) < 20
        and abs(e.control.left - slot.left) < 20
    ):
        place(e.control, slot)
        e.control.update()

    slot = ft.Container(
    width=70,
    height=100,
    left=200,
    top=0,
    border=ft.Border.all(1)
)

    card = ft.GestureDetector(
    mouse_cursor=ft.MouseCursor.MOVE,
    drag_interval=5,
    on_pan_update=drag,
    on_pan_end=drop,
    left=0,
    top=0,
    content=ft.Container(bgcolor=ft.Colors.GREEN, width=70, height=100),
)
    
    page.add(ft.Stack(controls = [slot, card], width=1000, height=500))

    



ft.run(main)



#   Para a prova de conceito, utilizaremos apenas três tipos de controles:

#   Stack- Será usado como controle principal para o posicionamento absoluto de slots e cartões.
#   GestureDetector- o cartão que será movido dentro doStack
#   Container- o compartimento onde o cartão será inserido. Também será usado para contento GestureDetector.

#   Passo 1: Arraste o cartão ao redor

#   Nesta etapa, criaremos um Stacktabuleiro (solitaire) e uma GestureDetectorcarta (solitaire). 
#   A carta será então adicionada à lista de tabuleiros Stack.controls. 
#   top As leftpropriedades do tabuleiro GestureDetectorsão usadas para o posicionamento absoluto da carta no tabuleiro Stack.

import flet as ft

def main(page: ft.Page):
    def drag(e: ft.DragUpdateEvent):
        ...

    card = ft.GestureDetector(
        on_pan_update=drag,
        left=0,
        top=0,
        content=ft.Container(bgcolor=ft.Colors.GREEN, width=70, height=100),
    )

    page.add(ft.Stack(controls=[card], width=1000, height=500))

ft.run(main)

#   Para poder mover o cartão, atualizaremos o dragmétodo que é chamado no on_pan_update evento GestureDetectorque ocorre sempre drag_intervalque o usuário arrasta o cartão com o mouse.
#   Para mostrar o movimento do cartão, atualizaremos as propriedades do cartão topno leftretorno drag de chamada sempre que o on_pan_updateevento ocorrer.
#   Abaixo está o código mais simples para arrastar e GestureDetectorsoltar Stack:

import flet as ft

# Use of GestureDetector with on_pan_update event for dragging card
# Absolute positioning of controls within stack

def main(page: ft.Page):
    def drag(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.local_delta.y)
        e.control.left = max(0, e.control.left + e.local_delta.x)
        e.control.update()

    card = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_update=drag,
        left=0,
        top=0,
        content=ft.Container(bgcolor=ft.Colors.GREEN, width=70, height=100),
    )

    

    page.add(ft.Stack(controls=[card], width=1000, height=500))

ft.run(main)

#   Após a atualização de qualquer propriedade de um controle, um update()método do controle (ou de seu controle pai) deve ser chamado para que a atualização entre em vigor.

#   Passo 1: Completo.

#   Passo 2: Insira o cartão na ranhura ou faça-o quicar de volta.
#   O objetivo desta etapa é poder inserir um cartão em um compartimento se ele estiver suficientemente próximo e rebatê-lo caso contrário.

#   Vamos criar um Containercontrole que representará um espaço onde vamos soltar o cartão:

slot = ft.Container(
    width=70,
    height=100,
    left=200,
    top=0,
    border=ft.Border.all(1)
)
page.add(ft.Stack(controls = [slot, card], width=1000, height=500))


#   on_pan_end O evento do cartão é acionado quando o cartão é descartado:

card = ft.GestureDetector(
    mouse_cursor=ft.MouseCursor.MOVE,
    drag_interval=5,
    on_pan_update=drag,
    on_pan_end=drop,
    left=0,
    top=0,
    content=ft.Container(bgcolor=ft.Colors.GREEN, width=70, height=100),
)


#   Agora, se o cartão não estiver perto o suficiente, precisamos fazê-lo retornar à sua posição original. 
#   Infelizmente, não sabemos as coordenadas da posição original, já que as propriedades do cartão topforam leftalteradas no on_pan_updateevento.

#   Para resolver esse problema, vamos criar um Solitaireobjeto de classe para rastrear a posição original do cartão quando on_pan_starto evento do cartão for acionado:

class Solitaire:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0

solitaire = Solitaire()

def start_drag(e: ft.DragStartEvent):
    solitaire.start_top = e.control.top
    solitaire.start_left = e.control.left
    e.control.update()


#   Agora vamos atualizar on_pan_endo evento com a opção de devolver o cartão:

def bounce_back(game, card):
    """return card to its original position"""
    card.top = game.start_top
    card.left = game.start_left
    page.update()

def drop(e: ft.DragEndEvent):
    if (
        abs(e.control.top - slot.top) < 20
        and abs(e.control.left - slot.left) < 20
    ):
        place(e.control, slot)
    else:
        bounce_back(solitaire, e.control)

    e.control.update()