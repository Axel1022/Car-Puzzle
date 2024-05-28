import pygame

class MusicPlayer(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("assets/Sonidos/Fast_Furious-Tokyo.wav")
        pygame.mixer.music.play(-1)
        self.current_volume = 0.5  # Volumen inicial entre 0.0 y 1.0
        self.set_volume(self.current_volume)

    def set_volume(self, volume):
        # Asegurarse de que el volumen esté en el rango de 0.0 a 1.0
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)

    def vol_Up(self):
        self.current_volume = 1.0
        self.set_volume(self.current_volume)

    def vol_Down(self):
        self.current_volume = 0.3
        self.set_volume(self.current_volume)

    def muteORdemue(self):
        if self.current_volume == 0.0:
            self.current_volume = 0.5  # Restaurar el volumen a la mitad
        else:
            self.current_volume = 0.0  # Silenciar el volumen
        self.set_volume(self.current_volume)
