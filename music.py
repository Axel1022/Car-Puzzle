import pygame

class MusicPlayer(object):
    def __init__(self):
        pygame.init()
        self.music_channel = pygame.mixer.Channel(0)  # Usar el canal 0 para la música
        self.sound_effects_channel = pygame.mixer.Channel(1)  # Usar el canal 1 para los efectos de sonido
        self.music_channel.play(pygame.mixer.Sound("assets/Sonidos/Fast_Furious-Tokyo.wav"), loops=-1)
        self.current_volume = 0.5  # Volumen inicial entre 0.0 y 1.0
        self.set_volume(self.current_volume)

    def set_volume(self, volume):
        # Asegurarse de que el volumen esté en el rango de 0.0 a 1.0
        volume = max(0.0, min(1.0, volume))
        self.music_channel.set_volume(volume)

    def vol_Up(self):
        if self.current_volume < 1.0:
            self.current_volume += 0.1
            self.set_volume(self.current_volume)

    def vol_Down(self):
        if self.current_volume > 0.0:
            self.current_volume -= 0.1
            self.set_volume(self.current_volume)

    def muteORdemue(self):
        if self.current_volume == 0.0:
            self.current_volume = 0.5  # Restaurar el volumen a la mitad
        else:
            self.current_volume = 0.0  # Silenciar el volumen
        self.set_volume(self.current_volume)
