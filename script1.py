# xo = [
#     [True, False, False],
#     [True, False, None],
#     [False, None, None],
#     ]

# convert bool to x,o,-
def conv_display(value):
    if value==True: return "x"
    elif value==False: return "o"
    elif value is None: return "-"


# find out if 3 in a row
def is_winner(xo):
    eval_hv = []
    for i in range(3):
        eval_hv.append(xo[i][0] == xo[i][1] == xo[i][2] != None)
        eval_hv.append(xo[0][i] == xo[1][i] == xo[2][i] != None)
    eval_hv.append(xo[0][0] == xo[1][1] == xo[2][2] != None)
    eval_hv.append(xo[0][2] == xo[1][1] == xo[2][0] != None)

    return True if any(eval_hv) else False

    # else:
    #     return False

#determine if move is valid
def is_valid_move(x,y):
    global xo
    if 0<=x<=2 and 0<=y<=2 and xo[x][y] is None:
        return True
    else: return False


# отобразить поле
def display_field(xo):
    print("")
    print("  0 1 2")
    counter = 0
    for a in xo:
        print(f"{counter:<2}", end="")
        for b in a:
            print(f"{conv_display(b):2}", end="")
        print(" ")
        counter += 1

# начало кода

xo = [
    [None, None, None],
    [None, None, None],
    [None, None, None],
    ]
winner = None
player = True
moves = 0

print("Играем в крестики-нолики.")

display_field(xo)

while winner == None:
    print("Ходит игрок", conv_display(player), ".")
    x, y = map(int, input("Введите номер строки и столбца через пробел: ").split())

    while not is_valid_move(x,y):
        print("Неверный ввод, попробуйте еще раз!")
        x, y = map(int, input("Введите номер строки и столбца через пробел: ").split())

    xo[x][y] = player
    print("Ход принят.")
    display_field(xo)

    moves += 1
    if moves == 9:
        print("Ничья! Игра закончена.")
        break

    if not is_winner(xo):
        player = not player
    else:
        winner = player
        print(f"Победил игрок {conv_display(winner)}!")


