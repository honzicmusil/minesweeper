def get_games_option(MAX_WIDTH, MAX_HEIGTH, MINE_SIZE, MIN_WIDTH, MIN_HEIGHT):
    # zeptá se uzivatele na velikost minového pole a počet min
    # vrací šířku, výšku pole a počet min
    # typ vracených hodnot je iteger

    import tkinter as tk
    all_filled = False  # proměná k otestování návratu, zda nebyl doalog ukončen dříve

    root = tk.Tk()

    canvas1 = tk.Canvas(root, width=400, height=300)
    canvas1.pack()

    entry_width = tk.Entry(root)  # Witht
    entry_heigth = tk.Entry(root)  # Heigth
    entry_mines = tk.Entry(root)  # Count mines

    label1 = tk.Label(root, text="Enter the size of mines field")
    label1.config(font=('Arial', 20))
    canvas1.create_window(200, 30, window=label1)

    label2 = tk.Label(root, text="Width")
    label3 = tk.Label(root, text="Hight")
    label4 = tk.Label(root, text="Count mines")

    canvas1.create_window(118, 80, window=label2)
    canvas1.create_window(200, 80, window=entry_width)

    canvas1.create_window(118, 100, window=label3)
    canvas1.create_window(200, 100, window=entry_heigth)

    canvas1.create_window(98, 120, window=label4)
    canvas1.create_window(200, 120, window=entry_mines)

    def check_area():
        global width, heigth, count_mines
        nonlocal all_filled

        width = entry_width.get()
        heigth = entry_heigth.get()
        count_mines = entry_mines.get()

        # kontrola šířky číslo > 0 a menší než max
        err_width = True
        try:
            int(width)
            if (int(width) < MIN_WIDTH) or (int(width) > MAX_WIDTH):
                err_width = True
            else:
                err_width = False
        except:
            err_width = True

        if err_width:
            label5 = tk.Label(root, text="Please enter Width - the number in interval <" + str(MIN_WIDTH) + "," + str(
                MAX_WIDTH) + "> ")
        else:
            label5 = tk.Label(root, text=200 * " ")

        canvas1.create_window(200, 150, window=label5)

        # kontrola výšky číslo > 0 a menší než max
        err_heigth = True
        try:
            int(heigth)
            if (int(heigth) < MIN_HEIGHT) or (int(heigth) > MAX_HEIGTH):
                err_heigth = True
            else:
                err_heigth = False
        except:
            err_heigth = True

        if err_heigth:
            label6 = tk.Label(root, text="Please enter Heigth - the number in interval <" + str(MIN_HEIGHT) + "," + str(
                MAX_HEIGTH) + "> ")
        else:
            label6 = tk.Label(root, text=200 * " ")

        canvas1.create_window(200, 170, window=label6)

        # kontrola počtu min číslo > 0 a menší než (šířka x výška)
        err_mines = True
        try:
            int(count_mines)
            if (int(count_mines) < 1) or (int(count_mines) > ((int(heigth) // MINE_SIZE) * (int(width) // MINE_SIZE))):
                err_mines = True
            else:
                err_mines = False
        except:
            err_mines = True

        if (not err_width and not err_heigth) and err_mines:
            label7 = tk.Label(root, text="Please enter Count of mines - the number in interval <1,"
                                         + str((int(heigth) // MINE_SIZE) * (int(width) // MINE_SIZE)) + "> ")
        else:
            label7 = tk.Label(root, text=200 * " ")

        canvas1.create_window(200, 190, window=label7)

        if (not err_width and not err_heigth and not err_mines):
            all_filled = True
            print("OK ", width, heigth, count_mines)
            root.destroy()

    button1 = tk.Button(text='OK', command=check_area)
    canvas1.create_window(200, 230, window=button1)

    root.mainloop()

    if all_filled:
        return (int(width), int(heigth), int(count_mines))
    else:
        return ("F")
