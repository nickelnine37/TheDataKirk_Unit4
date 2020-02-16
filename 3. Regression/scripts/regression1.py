from ipywidgets import interact
import numpy as np
import matplotlib.pyplot as plt
from operator import sub
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


no_salespeople = np.array([30, 10, 50, 35, 20])
total_sales = np.array([607,  91, 910, 653, 190])

a1 = 0
a2 = 10

def make_graph_1():
    
    x = np.linspace(0, 60, 101)
    y = a2 * x + a1

    fig, ax = plt.subplots()
    plt.scatter(no_salespeople, total_sales)
    plt.xlabel('Number of salespeople')
    plt.ylabel('Cars sold')
    plt.title('Try changing the value of $m$ and $c$')
    line, = ax.plot(x, y)
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 950)

    def update_c(c=0):
        global a1, a2
        a1 = c
        y_new = a2 * x + a1
        line.set_ydata(y_new)
        fig.canvas.draw_idle()

    def update_m(m=10):
        global a1, a2
        a2 = m
        y_new = a2 * x + a1
        line.set_ydata(y_new)
        fig.canvas.draw_idle()

    interact(update_c, c=(-400, 400, 1))
    interact(update_m, m=(0, 40, 0.1))
    
    
def make_graph_2():
    
    x = np.linspace(0, 60, 101)
    y = a2 * x

    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(5, 7))
    ax1.scatter(no_salespeople, total_sales)
    ax1.set_ylim(0, 1000)
    ax1.set_xlim(0, 60)
    ax1.set_xlabel('Number of salespeople')
    ax1.set_ylabel('Cars sold')
    ax1.set_title('Vary $m$ to see the effect on the total error')

    m_space = np.linspace(0, 40, 101)
    ax2.set_ylabel('Total Error')
    ax2.set_xlabel('$m$')
    ax2.plot(m_space, ((total_sales - no_salespeople * m_space.reshape(-1, 1)) ** 2).sum(1))
    ax2.set_yticks([])
    scat,  = ax2.plot([a2], [((total_sales - no_salespeople * a2) ** 2).sum()], marker='o', linewidth=0)
    
    line, = ax1.plot(x, y)
    d_lines = []
    for sp, s in zip(no_salespeople, total_sales):
        d_lines.append(ax1.plot([sp, sp], [a2 * sp, s], color='red', ls='--')[0])

    def update_m(m=15):
        global a2
        a2 = m
        y_new = m * x
        line.set_ydata(y_new)
        fig.canvas.draw_idle()
        for d_line, sp, s in zip(d_lines, no_salespeople, total_sales):
            d_line.set_ydata([m * sp, s])
            
        scat.set_ydata([((total_sales - no_salespeople * m) ** 2).sum()])
        scat.set_xdata([m])
        ax2.set_title('Total error = {}'.format(int(((total_sales - a2 * no_salespeople) ** 2).sum())))
        
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.25)
    interact(update_m, m=(0, 40, 0.1))
    
    
x0 = -1

def make_graph_3():
    
    def get_aspect(ax):
        # Total figure size
        figW, figH = ax.get_figure().get_size_inches()
        # Axis size on figure
        _, _, w, h = ax.get_position().bounds
        # Ratio of display units
        disp_ratio = (figH * h) / (figW * w)
        # Ratio of data units
        # Negative over negative because of the order of subtraction
        data_ratio = sub(*ax.get_ylim()) / sub(*ax.get_xlim())

        return disp_ratio / data_ratio
    
    def curve(x1):
        return (1/3) * x1 ** 3 - 4 * x1 + 5
    
    def grad(x1):
        return x1 ** 2 - 4
    
    def get_ls(x1):
        w = 6 / (1 + (aspect * grad(x1)) ** 2) ** 0.5
        return np.linspace(x1-w/2, x1+w/2, 11)
    
    def line(x1):
        return grad(x1) * (get_ls(x1) - x1) + curve(x1)
    
    fig, ax = plt.subplots()

    x = np.linspace(-5, 5, 1001)
    y = curve(x)
    ax.plot(x, y)
    aspect = get_aspect(ax)
    y0 = ax.get_ylim()[0]

    slope, = ax.plot(get_ls(x0), line(x0))
    x_line, = ax.plot([x0, x0], [y0, curve(x0)], color='gray', ls='--')
    
    def update_x0(x):
        
        slope.set_xdata(get_ls(x))
        slope.set_ydata(line(x))
        x_line.set_xdata([x, x])
        x_line.set_ydata([y0, curve(x)])
        ax.set_title('Gradient = {:.2f}'.format(grad(x)))
        
    interact(update_x0, x=(-5, 5, 0.01))
    
    
a = 1
b = 0 

def make_graph_4():
     
    a2 = 20
    a1 = 0
    x = np.linspace(0, 60, 101)
    y = a2 * x + a1 

    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(5, 7))
    ax1.scatter(no_salespeople, total_sales)
    ax1.set_ylim(0, 1000)
    ax1.set_xlabel('Number of salespeople')
    ax1.set_ylabel('Cars sold')
    ax1.set_title('Varying two parameters')
    
    line, = ax1.plot(x, y)
    d_lines = []
    for sp, s in zip(no_salespeople, total_sales):
        d_lines.append(ax1.plot([sp, sp], [a2 * sp + a1, s], color='red', ls='--')[0])
        
    m_space = np.linspace(10, 30, 101)
    c_space = np.linspace(-400, 400, 101)
    M, C = np.meshgrid(m_space, c_space)
    L = (((total_sales - no_salespeople * m_space.reshape(-1, 1, 1)) - c_space.reshape(1, -1, 1)) ** 2).sum(-1)
    
    c = ax2.pcolor(M, C, np.log(L.T))
    
    scat,  = ax2.plot([a2], [a1], marker='o', linewidth=0, color='red')
    ax2.set_xlabel('$m$')
    ax2.set_ylabel('$c$')
    ax2.set_title('2D Error representation')


    def update():
        global a1, a2
        y_new = a2 * x + a1
        line.set_ydata(y_new)
        fig.canvas.draw_idle()
        for d_line, sp, s in zip(d_lines, no_salespeople, total_sales):
            d_line.set_ydata([a2 * sp + a1, s])
        
        scat.set_ydata([a1])
        scat.set_xdata([a2])
        ax2.set_title('Total error = {}'.format(int(((total_sales - a2 * no_salespeople - a1) ** 2).sum())))
        
    def update_c(c=0):
        global a1, a2
        a1 = c
        update()

    def update_m(m=20):
        global a1, a2
        a2 = m
        update()
        
    plt.tight_layout()
    
    interact(update_c, c=(-400, 400, 1))
    interact(update_m, m=(10, 30, 0.1))
    
def make_graph_5():

    c = 1
    m1 = -2
    m2 = 1

    x = np.random.uniform(0, 10, 50)
    y = np.random.uniform(0, 10, 50)
    z = c + m1 * x + m2 * y + np.random.normal(loc=0, scale=2, size=50)

    x_space, y_space = np.meshgrid(*[np.linspace(0, 10, 101)] * 2) 
    z_space = c + m1 * x_space + m2 * y_space

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.plot_surface(x_space,y_space,z_space,cmap=cm.autumn, alpha=0.5)

    ax.scatter(x, y, z)
    ax.set_xlabel('$x^{(1)}$')
    ax.set_ylabel('$x^{(2)}$')
    ax.set_zlabel('y')
    plt.show()
    
np.random.seed(101)

b1 = 0
b2 = 0
b3 = 0
b4 = 0

def make_graph_6():
        
    x_space = np.linspace(-5, 5, 101)
    y_space = np.zeros_like(x_space)
    
    x_points = np.random.uniform(-5, 5, 15)
    y_points = 100 + 2 * x_points-2 * x_points ** 2 + 3 * x_points ** 3 + np.random.normal(0, 25, 15)

    fig, ax = plt.subplots()
    plt.scatter(x_points, y_points)
    plt.xlabel('x')
    plt.ylabel('y')
    line, = ax.plot(x_space, y_space)
    
    def update():
        global b1, b2, b3, b4
        y_new = b1 + b2 * x_space + b3 * x_space ** 2 + b4 * x_space ** 3
        line.set_ydata(y_new)
        fig.canvas.draw_idle()

    def update_a(a=0):
        global b1, b2, b3, b4
        b1 = a
        update()

    def update_b(b=0):
        global b1, b2, b3, b4
        b2 = b
        update()
        
    def update_c(c=0):
        global b1, b2, b3, b4
        b3 = c
        update()
        
    def update_d(d=0):
        global b1, b2, b3, b4
        b4 = d
        update()

    interact(update_a, a=(-200, 200, 1))
    interact(update_b, b=(-100, 100, 1))
    interact(update_c, c=(-50, 50, 0.1))
    interact(update_d, d=(-4, 4, 0.05))