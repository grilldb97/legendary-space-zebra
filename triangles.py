def draw_triangles():
    num_rows = int(input("Geben Sie die Anzahl der Zeilen ein: "))

    # Dreieck aufsteigend
    for i in range(num_rows):
        x_triangle = 'x' * (i + 1)
        space_padding_x = ' ' * (num_rows - i) * 1
        o_triangle = 'o' * (i + 1)
        print(f"{x_triangle}{space_padding_x}{o_triangle.rjust(num_rows)}")

    # Dreieck absteigend
    for i in range(num_rows - 1, 0, -1):
        x_triangle = 'x' * i
        space_padding_o = ' ' * (num_rows - i+1) * 1
        o_triangle = 'o' * i
        print(f"{x_triangle}{space_padding_o}{o_triangle.rjust(num_rows)}")


draw_triangles()
