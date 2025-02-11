import tkinter as tk

view_width = 1275
view_height = 970

cursor_x = 0
cursor_y = 0

shapes = []
main_x_middle = 0
main_y_middle = 0
cursor_x = 0
cursor_y = 0

def read_shapes(file_path):
    global shapes
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#'): continue
            line = line.strip()
            tokens = line.split()
            shape = tokens[0]
            # print(f"Hitting {tokens[1]}")
            # print(f"Hitting {tokens}")
            params = list(map(float, tokens[1].split(',')))
            shapes.append([shape] + params)

def calc_center():
    x_min = y_min = float('inf')
    x_max = y_max = float('-inf')

    for shape in shapes:
        if shape[0] == 'circle':
            _, x, y, diameter = shape
            x_min = min(x_min, x - diameter / 2)
            x_max = max(x_max, x + diameter / 2)
            y_min = min(y_min, y - diameter / 2)
            y_max = max(y_max, y + diameter / 2)

        elif shape[0] == 'rectangle':
            # _, left, top, right, bottom = shape
            _, x1, y1, x2, y2 = shape
            x_min = min(x_min, x1)
            x_max = max(x_max, x2)
            y_min = min(y_min, y1)
            y_max = max(y_max, y2)

    global main_x_middle, main_y_middle
    main_x_middle = (x_min + x_max) / 2
    main_y_middle = (y_min + y_max) / 2

def draw_canvas(canvas, canvas_width, canvas_height, x_center, y_center, pixels_per_unit):
    canvas.delete("all")

    for shape in shapes:
        if shape[0] == "circle":
            _, x, y, diameter = shape
            # import pdb; pdb.set_trace()
            xc = (x - x_center) * pixels_per_unit + canvas_width / 2
            yc = (-y + y_center) * pixels_per_unit + canvas_height / 2
            rad = diameter / 2 * pixels_per_unit
            # print(f"Drawing at {xc - rad}, {yc - rad} and {xc + rad}, {yc +rad}")
            canvas.create_oval(xc - rad, yc - rad, xc + rad, yc + rad, outline="white")

            rad_h = diameter / 3 * pixels_per_unit
            canvas.create_line(xc - rad_h, yc, xc + rad_h, yc, fill='white') # Horizontal line
            canvas.create_line(xc, yc - rad_h, xc, yc + rad_h, fill='white') # Veritcal line

        elif shape[0] == 'rectangle':
            _, left, top, right, bottom = shape
            x1 = (left - x_center) * pixels_per_unit + canvas_width / 2
            y1 = (-top + y_center) * pixels_per_unit + canvas_height / 2
            x2 = (right + x_center) * pixels_per_unit + canvas_width / 2
            y2 = (-bottom + y_center) * pixels_per_unit + canvas_height / 2
            canvas.create_rectangle(x1, y1, x2, y2, outline='white')


    xc = (cursor_x - x_center) * pixels_per_unit + canvas_width / 2
    yc = (-cursor_y + y_center) * pixels_per_unit + canvas_height / 2

    canvas.create_line(xc, 0, xc, canvas_height, fill="#80ff80")
    canvas.create_line(0, yc, canvas_width, yc, fill="#80ff80")

def update_display():
    global cursor_x, cursor_y

    draw_canvas(main_canvas, view_width, view_height, main_x_middle, main_y_middle, 10)

    num_show = "x=%6.2f  y=%6.2f" % (cursor_x, cursor_y)
    main_canvas.create_text(20, 30, anchor=tk.W, font=("Pursia", 30), text=num_show, fill="#a0ffa0")

    draw_canvas(zoom_canvas, zoom_width, zoom_height, cursor_x, cursor_y, 30)

def move_crosshair(event):
    global cursor_x, cursor_y
    step = 0.2

    if event.keysym == 'Up':
        cursor_y += step
    elif event.keysym == 'Down':
        cursor_y -= step
    elif event.keysym == 'Left':
        cursor_x -= step
    elif event.keysym == 'Right':
        cursor_x += step
    update_display()

if __name__ == "__main__":
    read_shapes('shapes_test.txt')
    calc_center()

    root = tk.Tk()
    root.title("The Windows Title")

    main_canvas = tk.Canvas(root, width=view_width, height=view_height, bg="black")
    main_canvas.pack()

    zoom_width = int(view_width / 3)
    zoom_height = int(view_height / 3)
    zoom_canvas = tk.Canvas(root, width=zoom_width, height=zoom_height, bg='#202020')
    zoom_canvas.place(x=view_width - zoom_width-2, y=2)

    update_display()

    root.bind("<KeyPress>", move_crosshair)

    root.mainloop()
