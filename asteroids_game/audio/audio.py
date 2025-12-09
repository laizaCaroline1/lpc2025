import pygame as pg
import os

class Audio:
    def __init__(self):
        try:
            pg.mixer.init()
        except Exception:
            pass
        # Load sounds from assets folder
        base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        self.sounds = {}
        for name in ("laser", "explosion", "enemy_shoot"):
            path = os.path.join(base, f"{name}.wav")
            try:
                self.sounds[name] = pg.mixer.Sound(path)
            except Exception:
                self.sounds[name] = None

    def play(self, name):
        s = self.sounds.get(name)
        if s:
            s.play()
