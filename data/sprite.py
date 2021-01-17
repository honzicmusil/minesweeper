import pygame


class Sprite(pygame.sprite.Sprite):
    """Třída Sprite s podpůrnými funkcemi

    - image_at(rectangle, colorkey) - nahraje obrazek na zadanych souradnicich + offset e.g. (0,0,320,320)
                                    - colorkey - parametr predavany funkci set_colorkey na pruhlednost barvy

    -images_at() - nahraje serii obrázků v řádku stejných velikostí
                 - e.g. images_at((0, 0, 320, 232),(320, 0, 320, 232))
    - load_strips(rect) - nahraje vsechny obrazky ze spritesheetu dle zadanych parametru
                  - rect - misto a velikost prvniho obrazku
                  - column_count - pocet opakovani obrazku v radku
                  - row_count - pocet opakovani v radcich

     """

    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(message)

    # nahraje obrazek na zadanych souradnicich
    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # nahraje serii obrázků v řádku stejných velikostí
    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    # nahraje vsechny obrazky ze spritesheetu dle zadanych parametru
    def load_strips(self, rect, column_count, row_count, colorkey=None):
        tups = []
        for row in range(row_count):
            tups = tups + [(rect[0] + rect[2] * x, rect[1] + rect[3] * row, rect[2], rect[3])
                           for x in range(column_count)]
        return self.images_at(tups, colorkey)


class SpriteStripAnim(object):
    """
    Trida, ktera iteruje skrz seznam obrazku a tim vytvari animaci.

    """

    def __init__(self, filename, rect, column_count, row_count, colorkey=None, loop=False, frames=1):
        """

        :param filename: cesta na spritesheet
        :param rect: souradnice a velikost prvniho obrazku e.g.(0, 0, 320, 232)
        :param column_count: pocet obrazku v jednom radku
        :param row_count: pocet radku ve spritesheetu
        :param colorkey: nastaveni pruhlednosti barvy
        :param loop: boolean, jestli se ma animace po prvnim prehrani opakovat nebo ne.
        :param frames: pocet obrazku (tiku) nez se prejde na dalsi obrazek. Ovlivnuje rychlost prehravani animace
        """
        self.filename = filename
        ss = Sprite(filename)
        self.images = ss.load_strips(rect, column_count, row_count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    # Nastaveni iterace na zacatek animace
    def iter(self):
        self.i = 0
        self.f = self.frames
        return self

    # Posunem o jeden tik
    def next(self):
        # Pokud jsme s animaci nakonci, nastavime bud zase zacatek, nebo vyhodime konec iterace pro zastaveni prehravani.
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        # snizime pocet frame o jeden - rychlost animace
        self.f -= 1
        # pokud jsme na frames na nule, zvysime obrazek o jeden - zmena obrazku v animaci.
        if self.f <= 0:
            self.i += 1
            self.f = self.frames
        return image

    def __add__(self, ss):
        self.images.extend(ss.images)
        return self
