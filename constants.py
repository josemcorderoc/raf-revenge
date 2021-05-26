# configuraciones iniciales
print("Hola! Bienvenido a RAF Revenge")

MULTIPLAYER = input("¿Desea jugar en modo multijugador? (si/no): ") in ["SI", "si", "Si", "yes", "s", "y"]
OPENGLMODE = input("Seleccione una de las siguientes opciones de visualización: "
                       "\n (1) Primitivas de OpenGL (más rápido)"
                       "\n (2) Sprites en PNG (más calidad)"
                       "¿Cuál modo desea? (1/2): ") in ["1", "(1)"]

square_length = 40  # tiene que ser par

x_squares = 19  # tiene que ser impar
y_squares = 13 # tiene que ser impar

HEIGHT = square_length * y_squares + 100 # se suma 100 para el puntaje, tiempo, etc.
WIDTH = square_length * x_squares

LIVES = 3

SPEED = 4

BOMBTIME = 3000  # [ms]

BOMBNUM = 50

STRENGTH = 1

ERROR = 1

DISTANCIAQUEMADO = 10

BURNTIME = 300 # [ms]

NUMENEMIES = 5

ENEMYDISTANCE = 5

NumPowerUps = 3

GAMETIME = 120000 # [ms]

SKIN_COLOR = (243/255.0, 197/255.0, 208/255.0)
