from pygame_functions import *


def velikostPole(maxWidth, maxHeigth):
    # zeptá se uzivatele na velikost minového pole
    # vrací šířku a výsku pole
    # typ vracených hodnot je iteger

    global heigth
    screenSize(maxWidth, maxHeigth)

    otazka = makeLabel(" Zadejte velikost minového pole ", 40, 10, 10, "blue", "", "clear")
    showLabel(otazka)

    wordBox1 = makeTextBox(30, 80, 200, 0, " šířka (max " + str(maxWidth) + ")", 3, 24)
    showTextBox((wordBox1))

    # uživatelský vstup - šířka
    # cyklus dokud nezada uživatel číslo > 0 a menší než max
    chyba = True
    while chyba:
        width = textBoxInput(wordBox1)
        try:
            int(width)
            if (int(width) < 1 or int(width) > maxWidth):
                chyba = True
            else:
                chyba = False
        except:
            ValueError

    # zobrazí zadanou šířku
    labelWidth = makeLabel(width, 40, 40, 85, "blue", "", "clear")
    showLabel(labelWidth)

    # uživatelský vstup - výška
    wordBox2 = makeTextBox(30, 150, 200, 0, " výška (max " + str(maxHeigth) + ")", 3, 24)

    # cyklus dokud nezada uživatel číslo > 0 a menší než max
    chyba = True
    while chyba:
        heigth = textBoxInput(wordBox2)
        try:
            int(heigth)
            chyba = False
            int(heigth)
            if (int(heigth) < 1 or int(heigth) > maxHeigth):
                chyba = True
            else:
                chyba = False
        except:
            ValueError

    return (int(width), int(heigth))

# zavolám dialog velikosti minového pole a vytisku co uživatel zadal
# vstupní parametry jsou maximální rozměry minového pole
# 1. - max šířka minového pole
# 2. - max výška minového pole
# print(velikostPole(800,600))
