
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

g = 9.8
dt = 0.02
e = 0.8
radius = 5.0

while True:
 y = float(input("enter first hight (metre): "))
 if 5 <= y <= 50:
    break
 else:
     print("Invalid input! Please enter a number between 5 and 50.")

y0 = y
v = 0.0
t = 0.0


y_min, y_max = 0, 55.0


fig, ax = plt.subplots(figsize=(4, 5))
ax.set_xlim(-10, 25)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal', adjustable='box')



ax.plot([-5, 5], [0, 0], linewidth=2)


ball = plt.Circle((0, y), radius, color="orange")
ax.add_patch(ball)
info = ax.text(0.02, 0.95, "", transform=ax.transAxes)


bounce_count = 0
h_max_next = y

y_sim_list = []
y_real_list = []

def update(frame):
    global y, v, t, bounce_count, h_max_next

    v = v - g * dt
    y = y + v * dt


    if y - radius <= 0:
        y = radius
        v = -e * v
        if abs(v) >= 0.20:
            bounce_count += 1

        h_max_next = v**2 / (2 * g)

        if abs(v) < 0.20:
            v = 0.00
            h_max_next = 0
            ani.event_source.stop()
            return ball, info

    if bounce_count == 0:
      y_real = y0 - 0.5 * g * t**2
      y_sim_list.append(y)
      y_real_list.append(y_real)


    ball.center = (0, y)
    info.set_text(f"time = {t:.2f} s\nvelocity = {v:.2f} m/s\nheight = {y:.2f} m\nbounce: {bounce_count}\nnext max hight: {h_max_next:.2f} m")
    t += dt
    return ball, info


ani = FuncAnimation(fig, update, frames=1000, interval=20, blit=False)
#ani.save('bouncing_ball.gif', writer='pillow', fps=50)

plt.show()

y_sim = np.array(y_sim_list)
y_real = np.array(y_real_list)

mse = np.mean((y_sim - y_real)**2)
ss_res = np.sum((y_real - y_sim)**2)
ss_tot = np.sum((y_real - np.mean(y_real))**2)
r2 = 1- ss_res / ss_tot

print(f"MSE: {mse: .2f}")
print(f"R: {r2: .2f}")


