import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact

mu_ = 0
h_ = 10

def make_graph_1():
    
    def rbf(x, mu, h):
        return np.exp(-((x - mu)**2)/h ** 2)
        
    x = np.linspace(-50, 50, 1001)
    y = rbf(x, mu_, h_)
    
    fig, ax = plt.subplots()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(-50, 50)
    plt.ylim(0, 1.1)
    line, = ax.plot(x, y)
    
    def update():
        global mu_, h_
        y_new = rbf(x, mu_, h_)
        line.set_ydata(y_new)
        fig.canvas.draw_idle()

    def update_mu(mu=0):
        global mu_, h_
        mu_ = mu
        update()

    def update_h(h=10):
        global mu_, h_
        h_ = h
        update()
        
    interact(update_mu, mu=(-50, 50, 0.1))
    interact(update_h, h=(0.1, 50, 0.1))
    
b1 = 1
b2 = 1
b3 = 1
b4 = 1
b5 = 1

def make_graph_2():
    
    def rbf(x, mu, h):
        return np.exp(-((x - mu)**2)/h ** 2)
    
    h = 1.5
    mus = np.linspace(-5, 5, 5)
        
    x = np.linspace(-5, 5, 1001)
    y = sum([rbf(x, mus[i], h) for i in range(5)])
    
    fig, ax = plt.subplots()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    line, = ax.plot(x, y, label='sum')
    
    lines = [ax.plot(x, rbf(x, mus[i], h), lw=1, label='$\phi_{}(x)$'.format(i+1))[0] for i in range(5)]
    
    plt.legend()
    
    def update():
        global b1, b2, b3, b4, b5
        y_new = sum([b * rbf(x, mu, h) for mu, b in  zip(mus, [b1, b2, b3, b4, b5])])
        line.set_ydata(y_new)
        fig.canvas.draw_idle()

    def update_a1(a1=1):
        global b1, b2, b3, b4, b5
        b1 = a1
#         lines[0].set_ydata(a1 * rbf(x, mus[0], h))
        update()

    def update_a2(a2=1):
        global b1, b2, b3, b4, b5
        b2 = a2
#         lines[1].set_ydata(a2 * rbf(x, mus[1], h))
        update()

    def update_a3(a3=1):
        global b1, b2, b3, b4, b5
        b3 = a3
#         lines[2].set_ydata(a3 * rbf(x, mus[2], h))
        update()
        
    def update_a4(a4=1):
        global b1, b2, b3, b4, b5
        b4 = a4
#         lines[3].set_ydata(a4 * rbf(x, mus[3], h))
        update()
        
    def update_a5(a5=1):
        global b1, b2, b3, b4, b5
        b5 = a5
#         lines[4].set_ydata(a5 * rbf(x, mus[4], h))
        update()

        
    interact(update_a1, a1=(-5, 5, 0.01))
    interact(update_a2, a2=(-5, 5, 0.01))
    interact(update_a3, a3=(-5, 5, 0.01))
    interact(update_a4, a4=(-5, 5, 0.01))
    interact(update_a5, a5=(-5, 5, 0.01))
    
    
    
c1 = 1
c2 = 1
c3 = 1
c4 = 1
c5 = 1

def make_graph_3():
    
    def rbf(x, mu, h):
        return np.exp(-((x - mu)**2)/h ** 2)
    

    h = 1.5
    mus = np.linspace(-5, 5, 5)
    
    x_data = np.linspace(-5, 5, 21)
    y_data = sum([b * rbf(x_data, mu, h) for mu, b in  zip(mus, np.random.uniform(-5, 5, 5))])
    
    x = np.linspace(-5, 5, 1001)
    y = sum([rbf(x, mus[i], h) for i in range(5)])
    
    fig, ax = plt.subplots()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(-5, 5)
    line, = ax.plot(x, y)
    plt.scatter(x_data, y_data)
            
    def update():
        global b1, b2, b3, b4, b5
        y_new = sum([b * rbf(x, mu, h) for mu, b in  zip(mus, [c1, c2, c3, c4, c5])])
        line.set_ydata(y_new)
        fig.canvas.draw_idle()

    def update_a1(a1=1):
        global c1, c2, c3, c4, c5
        c1 = a1
        update()

    def update_a2(a2=1):
        global c1, c2, c3, c4, c5
        c2 = a2
        update()

    def update_a3(a3=1):
        global c1, c2, c3, c4, c5
        c3 = a3
        update()
        
    def update_a4(a4=1):
        global c1, c2, c3, c4, c5
        c4 = a4
        update()
        
    def update_a5(a5=1):
        global c1, c2, c3, c4, c5
        c5 = a5
        update()

        
    interact(update_a1, a1=(-5, 5, 0.01))
    interact(update_a2, a2=(-5, 5, 0.01))
    interact(update_a3, a3=(-5, 5, 0.01))
    interact(update_a4, a4=(-5, 5, 0.01))
    interact(update_a5, a5=(-5, 5, 0.01))