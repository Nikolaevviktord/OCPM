"""
        OCPM robotics contest
        Senior group - task 1
        Graph

        code by vdn
"""



"""
        *************************************
        **            CONSTANTS            **
        *************************************
"""

turn_left_func_name = "turn_left"
turn_right_func_name = "turn_right"
go_to_n_cross_func_name = "zigzag_to_n_cross"



"""
        *************************************
        **    OUTPUT & GRAPHICAL WINDOW    **
        *************************************
"""

import sys
sys.stdout = open("get_path_func.txt", 'w')

import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
result = list()



"""
        *************************************
        **             METHODS             **
        *************************************
"""

def get_weights():
    root.title("Веса рёбер")

    columns = ["а", "б", "в", "г", "д", "е", "ж"]
    rows = ["1", "2", "3", "4", "5"]
    cell_size = 120

    canvas = tk.Canvas(root, width=cell_size * (len(columns) + 1), height=cell_size * (len(rows) + 1), bg="white")
    canvas.grid(row=0, column=0, columnspan=len(columns))

    for i in range(len(columns) + 1):
        for j in range(len(rows) + 1):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    for i in range(len(columns)):
        x1, y1 = i * cell_size + cell_size - 10, 0
        x2, y2 = x1 + 10, y1 + 20
        canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=f"{columns[i]}")

    for j in range(len(rows)):
        x1, y1 = 0, (j + 1) * cell_size - 20
        x2, y2 = x1 + 10, y1 + 20
        canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=f"{rows[j]}")

    entries = list()

    for i in range(len(columns)):
        for j in range(1, len(rows)):
            x1, y1 = (i + 1) * cell_size, j * cell_size + cell_size // 2
            entry = tk.Entry(root, width=3, justify="center")
            entry.insert(0, "1")
            entry.place(x=x1 - 15, y=y1 - 10)
            entries.append(entry)

    for i in range(1, len(columns)):
        for j in range(len(rows)):
            x1, y1 = i * cell_size + cell_size // 2, (j + 1) * cell_size
            entry = tk.Entry(root, width=3, justify="center")
            entry.insert(0, "1")
            entry.place(x=x1 - 15, y=y1 - 10)
            entries.append(entry)

    def calculate_weights():
        global root
        global result

        try:
            result = [int(entry.get()) for entry in entries]
            root.destroy()
            return
        except ValueError:
            messagebox.showerror("Ошибка", "Все веса должны быть целыми числами.")

    submit_button = tk.Button(root, text="Получить веса", command=calculate_weights)
    submit_button.grid(row=1, column=0, columnspan=len(columns))

    root.mainloop()

    weights = list()
    for i in range(6):
        weights += result[i * 4:(i + 1) * 4]
        weights += result[(28 + (i * 5)):(28 + ((i + 1) * 5))]
    weights += result[24:28]

    return weights


def parse_vertex(vertex):
    col_map = {"а": 0, "б": 1, "в": 2, "г": 3, "д": 4, "е": 5, "ж": 6}
    x = col_map[vertex[0]]
    y = int(vertex[1]) - 1
    return (x, y)


def vertex_to_str(x, y):
    col_map = {0: "а", 1: "б", 2: "в", 3: "г", 4: "д", 5: "е", 6: "ж"}
    return f"{col_map[x]}{y + 1}"


def way(weight, finish):
    ROWS, COLS = 5, 7

    def get_weight(x1, y1, x2, y2):
        if x1 == x2:
            index = min(y1, y2) + x1 * COLS
        else:
            index = 28 + y1 + min(x1, x2) * (ROWS - 1)
        try:
            return weight[index]
        except Exception as E:
            print(index, E)

    start = parse_vertex("а3")
    goal = parse_vertex(finish)

    pq = [(0, start)]
    dist = {start: 0}
    prev = {start: None}

    while pq:
        pq.sort()
        current_dist, (cx, cy) = pq.pop(0)

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                edge_weight = get_weight(cx, cy, nx, ny)
                new_dist = current_dist + edge_weight

                if (nx, ny) not in dist or new_dist < dist[(nx, ny)]:
                    dist[(nx, ny)] = new_dist
                    prev[(nx, ny)] = (cx, cy)
                    pq.append((new_dist, (nx, ny)))

    path = []
    step = goal
    while step:
        path.append(vertex_to_str(*step))
        step = prev.get(step)

    return path[::-1]


def code(way):
    result = list()

    curr_dir = 0

    for index in range(1, len(way)):
        prev_point = way[index - 1]
        curr_point = way[index]

        prev_vertex = parse_vertex(prev_point)
        curr_vertex = parse_vertex(curr_point)

        if curr_vertex[0] - prev_vertex[0] == 1:
            if curr_dir == 0:
                pass

            if curr_dir == 1:
                result.append(2)

            elif curr_dir == 2:
                result.append(1)
                result.append(1)

            elif curr_dir == 3:
                result.append(1)

            curr_dir = 0
            result.append(0)

        elif curr_vertex[0] - prev_vertex[0] == -1:
            if curr_dir == 0:
                result.append(1)
                result.append(1)

            if curr_dir == 1:
                result.append(1)

            elif curr_dir == 2:
                pass

            elif curr_dir == 3:
                result.append(2)

            curr_dir = 2
            result.append(0)

        elif curr_vertex[1] - prev_vertex[1] == 1:
            if curr_dir == 0:
                result.append(1)

            if curr_dir == 1:
                pass

            elif curr_dir == 2:
                result.append(2)

            elif curr_dir == 3:
                result.append(1)
                result.append(1)

            curr_dir = 1
            result.append(0)

        else:
            if curr_dir == 0:
                result.append(2)

            if curr_dir == 1:
                result.append(1)
                result.append(1)

            elif curr_dir == 2:
                result.append(1)

            elif curr_dir == 3:
                pass

            curr_dir = 3
            result.append(0)

    return result


def get_code_to_vertex(weight, finish):
    return code(way(weight, finish))



"""
        *************************************
        **            MAIN CODE            **
        *************************************
"""

rows = "12345"
columns = "абвгдеж"

weight = get_weights()

print("void get_path(byte x, byte y) {")

for i in range(7):
    for j in range(5):
        code_now = get_code_to_vertex(weight, columns[i] + rows[j])
        ln = len(code_now) + 2

        if not (i == j == 0):
            print("  else", end=' ')
        else:
            print("  ", end='')

        print(f"if (x == {i} && y == {j}) " + "{")

        for il in range(len(code_now)):
            if code_now[il] == 0:
                print(f"    {go_to_n_cross_func_name}(1);")
            elif code_now[il] == 1:
                print(f"    {turn_right_func_name}();")
            elif code_now[il] == 2:
                print(f"    {turn_left_func_name}();")

        print("    delay(4000);")

        code_now = [1, 1] + code_now[::-1]

        for il in range(len(code_now)):
            if code_now[il] == 1:
                code_now[il] = 2
            elif code_now[il] == 2:
                code_now[il] = 1

        for il in range(len(code_now)):
            if code_now[il] == 0:
                print(f"    {go_to_n_cross_func_name}(1);")
            elif code_now[il] == 1:
                print(f"    {turn_right_func_name}();")
            elif code_now[il] == 2:
                print(f"    {turn_left_func_name}();")

        print("  }")

        print()

print("}")
