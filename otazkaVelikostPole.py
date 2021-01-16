def Dialog_velikos_pole(max_width, max_heigth):
    # zeptá se uzivatele na velikost minového pole a počet min
    # vrací šířku, výšku pole a počet min
    # typ vracených hodnot je iteger

    import tkinter as tk

    root = tk.Tk()

    canvas1 = tk.Canvas(root, width=400, height=300)
    canvas1.pack()

    entry1 = tk.Entry(root)  # Witht
    entry2 = tk.Entry(root)  # Heigth
    entry3 = tk.Entry(root)  # Count mines

    label1 = tk.Label(root, text="Enter the size of mines field")
    label1.config(font=('Arial', 20))
    canvas1.create_window(200, 30, window=label1)

    label2 = tk.Label(root, text="Width")
    label3 = tk.Label(root, text="Hight")
    label4 = tk.Label(root, text="Count mines")

    canvas1.create_window(118, 80, window=label2)
    canvas1.create_window(200, 80, window=entry1)

    canvas1.create_window(118, 100, window=label3)
    canvas1.create_window(200, 100, window=entry2)

    canvas1.create_window(98, 120, window=label4)
    canvas1.create_window(200, 120, window=entry3)

    def checkArea():
        global width
        global heigth
        global count_mines

        width = entry1.get()
        heigth = entry2.get()
        count_mines = entry3.get()

        # kontrola šířky číslo > 0 a menší než max
        chyba1 = True
        try:
            int(width)
            if (int(width) < 1) or (int(width) > max_width):
                chyba1 = True
            else:
                chyba1 = False
        except:
            chyba1 = True

        if chyba1:
            label5 = tk.Label(root, text="Please enter Width - the number in interval <1," + str(max_width) + "> ")
        else:
            label5 = tk.Label(root, text=200 * " ")

        canvas1.create_window(200, 150, window=label5)

        # kontrola výšky číslo > 0 a menší než max
        chyba2 = True
        try:
            int(heigth)
            if (int(heigth) < 1) or (int(heigth) > max_heigth):
                chyba2 = True
            else:
                chyba2 = False
        except:
            chyba2 = True

        if chyba2:
            label6 = tk.Label(root, text="Please enter Heigth - the number in interval <1," + str(max_heigth) + "> ")
        else:
            label6 = tk.Label(root, text=200 * " ")

        canvas1.create_window(200, 170, window=label6)

        # kontrola počtu min číslo > 0 a menší než (šířka x výška)
        chyba3 = True
        try:
            int(count_mines)
            if (int(count_mines) < 1) or (int(count_mines) > int(heigth) * int(width)):
                chyba3 = True
            else:
                chyba3 = False
        except:
            chyba3 = True

        if (not chyba1 and not chyba2) and chyba3:
            label7 = tk.Label(root, text="Please enter Count of mines - the number in interval <1," + str(
                int(heigth) * int(width)) + "> ")
        else:
            label7 = tk.Label(root, text=200 * " ")

        canvas1.create_window(200, 190, window=label7)

        if (not chyba1 and not chyba2 and not chyba3):
            print("OK ", width, heigth, count_mines)
            root.destroy()

    button1 = tk.Button(text='OK', command=checkArea)
    canvas1.create_window(200, 230, window=button1)

    root.mainloop()

    return (int(width), int(heigth), int(count_mines))


# zavolám dialog velikosti minového pole a vytisku co uživatel zadal
# vstupní parametry jsou maximální rozměry minového pole
# 1. - max šířka minového pole
# 2. - max výška minového pole
# 3. - počet min
print(Dialog_velikos_pole(800, 600))