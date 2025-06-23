import pygame
import random
import sys

pygame.init()

WS = 600
HS = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 300, 0)

screen = pygame.display.set_mode((WS, HS))
pygame.display.set_caption("Tom's Hunt")
clock = pygame.time.Clock()

class Karakter():
    def __init__(self, x, y, width, height, gambar):
        self.gambar = pygame.image.load(gambar)
        self.gambar = pygame.transform.scale(self.gambar, (width, height))
        self.rect = self.gambar.get_rect(topleft=(x, y))

    def munculinGambar(self, tempelGambar):
        tempelGambar.blit(self.gambar, self.rect)

class Kucing(Karakter):
    def __init__(self, x, y, width, height, gambar, speed):
        super().__init__(x, y, width, height, gambar)
        self.speed = speed
    
    def kejar(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WS:
            self.rect.right = WS 
        if self.rect.top < 0:
            self.rect.top = 0 
        elif self.rect.bottom > HS:
            self.rect.bottom = HS

class Tikus(Karakter):
    def __init__(self, x, y, width, height, gambar, speed):
        super().__init__(x, y, width, height, gambar)
        self.speed = speed

    def lari(self, directX, directY):
        self.rect.x += directX * self.speed
        self.rect.y += directY * self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WS:
            self.rect.right = WS 
        if self.rect.top < 0:
            self.rect.top = 0 
        elif self.rect.bottom > HS:
            self.rect.bottom = HS

class Game():
    def __init__(self):
        self.Tom = Kucing(270, 270, 60, 60, "k2.jpg", 5)

        jerry_pccX = random.randint(0, WS - 40)
        jerry_pccY = random.randint(0, HS - 40)

        self.Jerry = Tikus(jerry_pccX, jerry_pccY, 40, 40, "t2.jpg", 5)

        self.game_running = True
        self.game_status = "START SCREEN"
        self.tom_menang = False

        self.font_pesan = pygame.font.Font(None, 35)
        self.Judul = pygame.font.Font(None, 60)
        self.instruksi = pygame.font.Font(None, 35)
        self.tombol = pygame.font.Font(None, 40)

        self.timer = 30 * 1000
        self.start_time = pygame.time.get_ticks()
        self.sisa_waktu = self.timer
        self.font_timer = pygame.font.Font(None, 25)

    def arahPanah(self):
        panah = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if panah[pygame.K_LEFT]:
            dx = -1
        if panah[pygame.K_RIGHT]:
            dx = 1
        if panah[pygame.K_UP]:
            dy = -1
        if panah[pygame.K_DOWN]:
            dy = 1

        self.Tom.kejar(dx, dy)

    def WASD(self):
        wasd = pygame.key.get_pressed()
        directX = 0
        directY = 0

        if wasd[pygame.K_a]:
            directX = -1
        if wasd[pygame.K_d]:
            directX = 1
        if wasd[pygame.K_w]:
            directY = -1
        if wasd[pygame.K_s]:
            directY = 1

        self.Jerry.lari(directX, directY)

    def front_screen(self):
        screen.fill(WHITE)

        teks_judul = self.Judul.render("Tom's Hunt", True, BLACK)
        teks_rect = teks_judul.get_rect(center=(300, 200))
        screen.blit(teks_judul, teks_rect)
        
        teks_instruksiTom = self.instruksi.render("Tom (Panah atas, bawah, kiri, kanan)", True, BLACK)
        teks_rectInsTom = teks_instruksiTom.get_rect(center=(300, 270))
        screen.blit(teks_instruksiTom, teks_rectInsTom)
        
        teks_instruksiJerry = self.instruksi.render("Jerry (W-A-S-D)", True, BLACK)
        teks_rectInsJerry = teks_instruksiJerry.get_rect(center=(300, 300))
        screen.blit(teks_instruksiJerry, teks_rectInsJerry)

        teks_start = self.tombol.render("Mulai Game", True, WHITE)
        teks_rectStart = teks_start.get_rect(center=(300, 350))
        pygame.draw.rect(screen, GREEN, teks_rectStart.inflate(20, 30))
        screen.blit(teks_start, teks_rectStart)

        return teks_rectStart
    
    def game_Over_Screen(self):
        screen.fill(WHITE)

        if self.tom_menang:
            pesan = "Selamat Tom! kamu menang"
        else:
            pesan = "Hahaha mampus kamu Tom!!!"
                
        pesan_teks = self.font_pesan.render(pesan, True, BLACK)
        kotak_pesan = pesan_teks.get_rect(center=(300, 200))
        screen.blit(pesan_teks, kotak_pesan)

        teks_ulang = self.tombol.render("Ulangi Game", True, WHITE)
        teks_rectUlang = teks_ulang.get_rect(center=(300, 270))
        pygame.draw.rect(screen, GREEN, teks_rectUlang.inflate(20, 30))
        screen.blit(teks_ulang, teks_rectUlang)

        teks_keluar = self.tombol.render("Keluar Game", True, WHITE)
        teks_rectKeluar = teks_keluar.get_rect(center=(300, 350))
        pygame.draw.rect(screen, RED, teks_rectKeluar.inflate(20, 30))
        screen.blit(teks_keluar, teks_rectKeluar)

        return teks_rectUlang, teks_rectKeluar

    def menangKalah(self):
        penguranganWaktu = pygame.time.get_ticks() - self.start_time
        self.sisa_waktu = max(0, self.timer - penguranganWaktu)

        if self.Tom.rect.colliderect(self.Jerry.rect):
            self.game_status= "GAME OVER SCREEN"
            self.tom_menang = True
            return
        elif self.sisa_waktu == 0 and self.game_status == "PLAYING":
            self.tom_menang = False
            self.game_status = "GAME OVER SCREEN"
        
    def reset_game(self):
        self.Tom = Kucing(270, 270, 60, 60, "k2.jpg", 5)

        jerry_pccX = random.randint(0, WS - 40)
        jerry_pccY = random.randint(0, HS - 40)

        self.Jerry = Tikus(jerry_pccX, jerry_pccY, 40, 40, "t2.jpg", 5)

        self.tom_menang = False
        self.timer = 30 * 1000
        self.start_time = pygame.time.get_ticks()
        self.sisa_waktu = self.timer

    def display_timer(self):
        detik = self.sisa_waktu // 1000
        teks_timer = self.font_timer.render(f"Sisa waktu: {detik}", True, BLACK)
        screen.blit(teks_timer, (WS - teks_timer.get_width() - 10, 10))

    def run(self):
        while self.game_running:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_status == "START SCREEN":
                        teks_rectStart = self.front_screen()
                        if teks_rectStart.collidepoint(event.pos):
                            self.game_status = "PLAYING"
                            self.reset_game()
                    if self.game_status == "GAME OVER SCREEN":
                        teks_rectUlang, teks_rectKeluar = self.game_Over_Screen()
                        if teks_rectUlang.collidepoint(event.pos):
                            self.game_status = "PLAYING"
                            self.reset_game()
                        elif teks_rectKeluar.collidepoint(event.pos):
                            self.game_running = False
                            
            if self.game_status == "START SCREEN":
                self.front_screen()
            elif self.game_status == "PLAYING":
                self.Tom.munculinGambar(screen)
                self.Jerry.munculinGambar(screen)
                self.arahPanah()
                self.WASD()
                self.menangKalah()
                self.display_timer()
            elif self.game_status == "GAME OVER SCREEN":
                self.game_Over_Screen()
                
            pygame.display.flip()
            clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__=="__main__":
    game = Game()
    game.run()
