from ipywidgets import interact
import numpy as np
import matplotlib.pyplot as plt

b1 = 0
b2 = 0
b3 = 0

def make_graph_1():
        
    x_space = np.linspace(-5, 5, 101)
    y_space = np.zeros_like(x_space)
    
    fig, ax = plt.subplots()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(-5, 5)
    plt.ylim(-100, 100)
    line, = ax.plot(x_space, y_space)
    
    def update():
        global b1, b2, b3
        y_new = b1 + b2 * x_space + b3 * x_space ** 2
        line.set_ydata(y_new)
        ax.set_title(f'$f(x) = {b1:.2f} + {b2:.2f} x + {b3:.2f} x^2$')
        fig.canvas.draw_idle()

    def update_a(a=-20):
        global b1, b2, b3, b4
        b1 = a
        update()

    def update_b(b=-9):
        global b1, b2, b3, b4
        b2 = b
        update()
        
    def update_c(c=1.5):
        global b1, b2, b3, b4
        b3 = c
        update()
        
    interact(update_a, a=(-100, 100, 0.1))
    interact(update_b, b=(-50, 50, 0.1))
    interact(update_c, c=(-10, 10, 0.01))