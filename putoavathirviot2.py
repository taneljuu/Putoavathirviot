import pygame
import math
import random
import os

class Putoavat_robotit:
    def __init__(self):
        pygame.init()
        
        # Pelin alustus
        self.kello = pygame.time.Clock()
        self.leveys = 900
        self.korkeus = 900
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))

        # Ladataan kuvat
        self.kolikko = pygame.image.load("kolikko.png")
        self.hirvio = pygame.image.load("hirvio.png")
        self.ovi = pygame.image.load("ovi.png")
        self.robo = pygame.image.load("robo.png")

        # Alustetaan robotin sijainti
        self.robo_x = 0
        self.robo_y = 0

        # Alustetaan kolikon sijainti ja lista hirviöiden sijainneista
        self.kolikko_x = 0
        self.kolikko_y = 0
        self.hirviot = []

        # Hirviöiden nopeus, pisteet ja ennätys
        self.hirvio_nopeus = 1
        self.pisteet = 0
        self.ennatys = 0

        self.vari1 = 0
        self.vari2 = 0
        self.vari3 = 0

        pygame.display.set_caption("Peli")

        # Alustetaan peli
        self.aloita()
    
    def aloita(self):
        # Ladataan ennätys tiedostosta, jos se on olemassa
        if os.path.exists("ennatys.txt"):
            with open("ennatys.txt") as tiedosto:
                self.ennatys = int(tiedosto.readline())
        
        # Arvotaan taustan väri
        self.arvo_taustan_vari()
        
        # Alustetaan hirviöiden sijainti
        self.hirviot = [{'x': random.randint(0, 900 - self.hirvio.get_width()), 'y': random.randint(-4 * 900 - self.hirvio.get_height(), 0-self.hirvio.get_height())} for _ in range(50)]
        
        # Nollataan pisteet ja asetetaan hirviön nopeus
        self.pisteet = 0
        self.hirvio_nopeus = 1

        # asetetaan robo keskelle ruutua ja arvotaan kolikon ensimmäinen sijainti
        self.robot_alussa()
        self.kolikon_sijainti()

        self.paasilmukka()

    def paasilmukka(self):
        oikealle = False
        vasemmalle = False
        ylos = False
        alas = False
    
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                
                # Käsitellään näppäimistön painallukset
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_LEFT:
                        vasemmalle = True
                    if tapahtuma.key == pygame.K_RIGHT:
                        oikealle = True
                    if tapahtuma.key == pygame.K_UP:
                        ylos = True
                    if tapahtuma.key == pygame.K_DOWN:
                        alas = True

                # Käsitellään näppäimistön vapautukset
                if tapahtuma.type == pygame.KEYUP:
                    if tapahtuma.key == pygame.K_LEFT:
                        vasemmalle = False
                    if tapahtuma.key == pygame.K_RIGHT:
                        oikealle = False
                    if tapahtuma.key == pygame.K_UP:
                        ylos = False
                    if tapahtuma.key == pygame.K_DOWN:
                        alas = False

            # Määritetään robotin nopeus            
            nopeus = 3
            if (vasemmalle or oikealle) and (ylos or alas):
                nopeus = nopeus / math.sqrt(2) #robon nopeus aina sama riippumatta liikutaanko suoraan vai viistoon

            # Muutetaan robotin koordinaatteja ja päivitetään näyttö
            if vasemmalle and self.robo_x >= 0:
                self.robo_x -= nopeus
            if oikealle and self.robo_x + self.robo.get_width() <= self.leveys:
                self.robo_x += nopeus
            if ylos and self.robo_y >= 0:
                self.robo_y -= nopeus
            if alas and self.robo_y + self.robo.get_height() < self.korkeus:
                self.robo_y += nopeus
            
            self.piirra_naytto()
                
    def piirra_naytto(self):
        # Päivitetään näytön tila
        self.naytto.fill((self.vari1, self.vari2, self.vari3))
        self.naytto.blit(self.robo,(self.robo_x, self.robo_y))
        self.saako_kolikon()
        self.naytto.blit(self.kolikko,(self.kolikko_x, self.kolikko_y))
        self.peli_ohi()
        self.piirra_hirviot()
        fontti = pygame.font.SysFont("Arial", 24)
        pisteteksti = fontti.render(f"Pisteet: {self.pisteet}", True, (255, 0, 0))
        enkkateksti = fontti.render(f"Ennätys: {self.ennatys}", True, (255, 0, 0))
        self.naytto.blit(pisteteksti, (900-pisteteksti.get_width()-20, 20))
        self.naytto.blit(enkkateksti, (20, 20))

        pygame.display.flip()
        self.kello.tick(100)
    
    def robot_alussa(self):
        # Asetetaan robo keskelle ruutua
        self.robo_x = self.leveys/2-self.robo.get_width()/2
        self.robo_y = self.korkeus/2-self.robo.get_height()/2
    
    def piirra_hirviot(self):
        # Päivitetään hirviöiden sijainti
        for sanakirja in self.hirviot:
            sanakirja["y"] += self.hirvio_nopeus
            self.naytto.blit(self.hirvio, (sanakirja["x"], sanakirja["y"]))
            # Jos hirviö poistuu ruudulta, arvotaan sille uusi sijainti
            if sanakirja["y"] > 900:
                sanakirja["y"] = random.randint(-4 * 900 - self.hirvio.get_height(), 0-self.hirvio.get_height())
                sanakirja["x"] = random.randint(0, 900 - self.hirvio.get_width())
    
    def saako_kolikon(self):
        # Tarkastetaan, ovatko robon ja kolikon sijainnit päällekkäin, arvotaan kolikolle uusi sijainti ja päivitetään pisteet
        if self.kolikko_x+self.kolikko.get_width() >= self.robo_x >= self.kolikko_x-self.kolikko.get_width() and self.kolikko_y+self.kolikko.get_height() >= self.robo_y >= self.kolikko_y-self.robo.get_height():
            self.kolikon_sijainti()
            self.pisteet += 1
            # Jos pisteet tasakymmenluku, siirrytään uudelle tasolle
            if self.pisteet%10 == 0:
                self.uusi_taso()

    def uusi_taso(self):
        # Arvotaan uusi taustan väri
        self.arvo_taustan_vari()
        # Hirviöiden nopeus kasvaa 
        self.hirvio_nopeus = 1 + self.pisteet/20

    def kolikon_sijainti(self):
        # Arvotaan kolikon sijainti ruudulla
        self.kolikko_x = random.randint(0, 900-self.kolikko.get_width())
        self.kolikko_y = random.randint(0, 900-self.kolikko.get_height())
    
    def arvo_taustan_vari(self):
        # Arvotaan taustan väri
        while True:
            self.vari1 = random.randint(0, 255)
            self.vari2 = random.randint(0, 255)
            self.vari3 = random.randint(0, 255)
            # Tarkastetaan, ettei väri ole liian tumma
            if self.vari1 < 30 or self.vari2 < 30 or self.vari3 < 30:
                break

    def peli_ohi(self):
        # Tarkastetaan, ovatko robon ja hirviön sijainnit päällekkäin
        for sanakirja in self.hirviot:
            if sanakirja["y"]-2*self.hirvio.get_height()-5 <= self.robo_y-self.robo.get_height()+20 < sanakirja["y"] and sanakirja["x"]+self.hirvio.get_width()-15 >= self.robo_x >= sanakirja["x"]-self.hirvio.get_width()+20:
                pygame.time.delay(3000)

                # Tarkastetaan paraniko ennätys ja tallennetaan se tiedostoon ennatys.txt
                if self.pisteet > self.ennatys:
                    self.ennatys = self.pisteet
                    with open("ennatys.txt", "w") as tiedosto:
                        tiedosto.write(str(self.ennatys))
                # avataan lopetusvalikko
                self.lopetusvalikko()    

    def lopetusvalikko(self):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_RETURN:
                        self.aloita()
                    if tapahtuma.key == pygame.K_ESCAPE:
                        exit()
            fontti = pygame.font.SysFont("Arial", 20)
            if self.pisteet != 1:
                teksti = fontti.render(f"Peli päättyi. Sait kerättyä {self.pisteet} kolikkoa.", True, (255, 255, 255))
            if self.pisteet == 1:
                teksti = fontti.render(f"Peli päättyi. Sait kerättyä {self.pisteet} kolikon.", True, (255, 255, 255))
            teksti2 = fontti.render(f"Aloita uusi peli painamalla ENTER,", True, (255, 255, 255))
            teksti3 = fontti.render(f"Lopeta ohjelma painamalla esc.", True, (255, 255, 255))
            self.naytto.blit(teksti, (150, 150))
            self.naytto.blit(teksti2, (150, 200))
            self.naytto.blit(teksti3, (150, 250))
            pygame.display.flip()

	 
Putoavat_robotit()
