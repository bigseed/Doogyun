import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera


def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def animate(interval):
    animation = cam.animate(interval=interval)
    animation.save('test1.mp4')


def draw_orbit():
    center = (0, 0)
    c1 = plt.Circle(center, planet_radius[0], fc='none', ec='green')
    c2 = plt.Circle(center, planet_radius[1], fc='none', ec='red')
    c3 = plt.Circle(center, planet_radius[2], fc='none', ec='blue')
    ax.add_patch(c1)
    ax.add_patch(c2)
    ax.add_patch(c3)


def draw_planet():
    colors = ('green', 'red', 'blue')
    for idx in range(len(planet_radius)):
        ax.scatter(planet_radius[idx]*np.cos(planet_theta[idx]),
                   planet_radius[idx]*np.sin(planet_theta[idx]), c=colors[idx])


def move_planet():
    global planet_theta

    for i in range(3):
        planet_theta[i] += angular_velocity[i]


def calc_gravity(x, y):
    G = 3
    g_x, g_y = 0, 0

    for idx in range(0, 3):
        planet_x = planet_radius[idx]*np.cos(planet_theta[idx])
        planet_y = planet_radius[idx]*np.sin(planet_theta[idx])

        d = distance(x, y, planet_x, planet_y)
        if d == 0:
            return ('Crash', 'to Planet')

        gravity = G / d**3

        g_x += gravity * (planet_x - x)
        g_y += gravity * (planet_y - y)

    return (g_x, g_y)


def calc_value(x, y, fuel):
    planet_x = planet_radius[2]*np.cos(planet_theta[2])
    planet_y = planet_radius[2]*np.sin(planet_theta[2])

    return fuel / distance(x, y, planet_x, planet_y)**4


def first_make():
    planet_x = (planet_radius[0]+1)*np.cos(planet_theta[0])
    planet_y = (planet_radius[0]+1)*np.sin(planet_theta[0])

    ships = list()
    for _ in range(n):
        info = dict(x=planet_x, y=planet_y, fuel=1000.0, weights=np.random.uniform(
            -speed_range, speed_range, (1, 2)), v_x=1.5*np.cos(planet_theta[0]), v_y=1.5*np.sin(planet_theta[0]), value=0.0, calc=True, isgood=False)
        ships.append(info)

    return ships


def children_make(weights):
    planet_x = (planet_radius[0]+1)*np.cos(planet_theta[0])
    planet_y = (planet_radius[0]+1)*np.sin(planet_theta[0])

    ships = list()
    for _ in range(n):
        info = dict(x=planet_x, y=planet_y, fuel=1000.0,
                    weights=weights, v_x=1.5*np.cos(planet_theta[0]), v_y=1.5*np.sin(planet_theta[0]), value=0.0, calc=True, isgood=False)
        ships.append(info)

    return ships


def move_ships(moment, isokay):
    global ships
    for ship in ships:
        if not ship['calc']:
            continue

        x, y = ship['x'], ship['y']
        if distance(x, y, planet_radius[2]*np.cos(planet_theta[2]), planet_radius[2]*np.sin(planet_theta[2])) < 1:
            ship['calc'] = False
            ship['isgood'] = True
            continue

        if distance(x, y, 0, 0) > 21:
            ship['calc'] = False
            continue

        if ship['fuel'] <= 0:
            ship['calc'] = False
            continue

        a_x, a_y = calc_gravity(x, y)
        if a_x == 'Crash':
            ship['calc'] = False
            continue

        if isokay:
            if np.random.choice([True, False], 1, p=(epsilon, 1-epsilon))[0]:
                ship['weights'][moment] += np.random.uniform(-speed_range,
                                                             speed_range, (2,))

        else:
            temp_w = np.random.uniform(-speed_range, speed_range, (1, 2))
            ship['weights'] = np.concatenate((ship['weights'], temp_w), axis=0)

        a_x += ship['weights'][moment][0] * fuel_to_acceleration
        a_y += ship['weights'][moment][1] * fuel_to_acceleration
        ship['fuel'] -= (np.abs(ship['weights'][moment][0]) +
                         np.abs(ship['weights'][moment][1]))

        ship['v_x'] = a_x + deceleration*ship['v_x']
        ship['v_y'] = a_y + deceleration*ship['v_y']

        ship['x'] += ship['v_x']
        ship['y'] += ship['v_y']

        ship['value'] = calc_value(
            ship['x'], ship['y'], ship['fuel'])*(1-gamma) + gamma*ship['value']
        move_planet()


def test_ship(ship):
    draw_orbit()
    draw_planet()
    plt.scatter(ship['x'], ship['y'], c='k')
    cam.snap()
    for moment in range(ship['weights'].shape[0]):
        print(moment)
        x, y = ship['x'], ship['y']
        a_x, a_y = calc_gravity(x, y)
        if a_x == "Crash":
            break
        a_x += ship['weights'][moment][0] * fuel_to_acceleration
        a_y += ship['weights'][moment][1] * fuel_to_acceleration

        ship['v_x'] = a_x + deceleration*ship['v_x']
        ship['v_y'] = a_y + deceleration*ship['v_y']

        ship['x'] += ship['v_x']
        ship['y'] += ship['v_y']
        move_planet()

        draw_orbit()
        draw_planet()
        plt.scatter(ship['x'], ship['y'], c='k')
        cam.snap()
    animate(50)


# make Canvas
np.random.seed(47231)
fig, axes = plt.subplots()
ax = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
ax.set_aspect('equal')
cam = Camera(fig)

# planet parameters
planet_radius = (4, 10, 18)
planet_theta_init = np.random.uniform(-np.pi, np.pi, (3,))
planet_theta = planet_theta_init.copy()
angular_velocity = np.sort(np.random.uniform(0, np.pi / 50, (3,)))[::-1]

# Initialize parameters
time = 250
n = 1000
epsilon = 0.4
deceleration = 0.5
gamma = 0.5
speed_range = 5
ships = first_make()
fuel_to_acceleration = 1 / 250
EPOCHS = 10
max_val_ships = []


if True:
    for epoch in range(EPOCHS):
        weight_length = ships[0]['weights'].shape[0]
        for moment in range(time):
            if moment < weight_length:
                move_ships(moment, True)
            else:
                move_ships(moment, False)

        temp_val = (0, 0)
        for idx, ship in enumerate(ships):
            if ship['isgood']:
                temp_val = (idx, ship['value'])
                break
            if ship['value'] > temp_val[1]:
                temp_val = (idx, ship['value'])

        planet_theta = planet_theta_init.copy()
        max_val_ships.append((ships[temp_val[0]], temp_val[1]))
        ships = children_make(ships[temp_val[0]]['weights'])


max_weight = (0, 0)
for item in max_val_ships:
    if item[1] > max_weight[1]:
        max_weight = item

planet_x = (planet_radius[0]+1)*np.cos(planet_theta[0])
planet_y = (planet_radius[0]+1)*np.sin(planet_theta[0])

perfect_ship = dict(x=planet_x, y=planet_y, fuel=1000.0,
                    weights=max_weight[0]['weights'], v_x=0.8*np.cos(planet_theta[0]), v_y=0.8*np.sin(planet_theta[0]))

test_ship(perfect_ship)
