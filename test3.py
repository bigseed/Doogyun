import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera

fig, ax = plt.subplots()
cam = Camera(fig)
plt.xlim(-5, 5)
plt.ylim(-5, 5)
for i in range(1, 50):
    plt.scatter(range(50), range(50))
    cam.snap()

animation = cam.animate(interval=50)
animation.save('ss.mp4')
