import pygame
import math
pygame.init()

WIDTH, HEIGHT = 860, 860
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (40, 122, 184)
RED = (193,68,14)
DARK_GRAY = (116, 123, 129)

FONT = pygame.font.SysFont("comicsans", 16)
FONT1 = pygame.font.SysFont("comicsans", 20)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE  = 250 / AU # 1 AU = 100 pixels
    TIME_STEP = 3600 * 24 # 1 Day


    def __init__(self, name, x, y, radius, color, mass):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        text = FONT.render("SOLAR SYSTEM SIMULATION", 1, WHITE)
        win.blit(text, (0,0))

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}KM({self.name})", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

        else:
            sun_name = FONT1.render("SUN",  1, (0,0,0))
            sun_x = WIDTH / 2
            sun_y = HEIGHT / 2
            win.blit(sun_name, (sun_x - sun_name.get_width() / 2, sun_y - sun_name.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = 0
        total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIME_STEP
        self.y_vel += total_fy / self.mass * self.TIME_STEP

        self.x += self.x_vel * self.TIME_STEP
        self.y += self.y_vel * self.TIME_STEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet("Sun", 0, 0, 30, YELLOW, 1.98892 * 10 ** 30) # mass in KGs
    sun.sun = True

    earth = Planet("Earth", -1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24)
    earth.y_vel = 29.783 * 1000

    mars = Planet("Mars", -1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 8, DARK_GRAY, 0.330 * 10 **24)
    mercury.y_vel = -47.4 * 1000

    venus = Planet("Venus", 0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()