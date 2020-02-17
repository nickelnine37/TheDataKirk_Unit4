from ipywidgets import interact
import numpy as np
import matplotlib.pyplot as plt

a = 1
b = 0 

def make_graph_1():
    
    x_obs = np.linspace(1, 9, 11)
    y_obs = 2 * x_obs + 8 + np.random.normal(0, 1.5, 11)
    
    x = np.linspace(0, 10, 5)
    y = a * x + b

    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(5, 7))
    
    ax1.scatter(x_obs, y_obs)
    ax1.set_ylim(-5, 40)
    ax1.set_xlim(0, 10)
    ax1.set_xlabel('$x$')
    ax1.set_ylabel('$y$')
    ax1.set_title('Regression')
    
    line, = ax1.plot(x, y)
    d_lines = []
    for x_ob, y_ob in zip(x_obs, y_obs):
        pred = a * x_ob + b
        d_lines.append(ax1.plot([x_ob, x_ob], [pred, y_ob], color=['green', 'red'][int(pred > y_ob)], ls='--')[0])
        
    m_space = np.linspace(0, 4, 101)
    c_space = np.linspace(0, 12, 101)
    M, C = np.meshgrid(m_space, c_space)
    L = (((y_obs - x_obs * m_space.reshape(-1, 1, 1)) - c_space.reshape(1, -1, 1)) ** 2).sum(-1)
    
    c = ax2.pcolor(M, C, np.log(L.T))
    scat,  = ax2.plot([b], [a], marker='o', linewidth=0, color='red')
    fig.colorbar(c, ax=ax2)
    ax2.set_xlabel('$m$')
    ax2.set_ylabel('$c$')
    ax2.set_title('Total error')
    


    def update():
        global a, b
        line.set_ydata(a * x + b)
        fig.canvas.draw_idle()
        for d_line, x_ob, y_ob in zip(d_lines, x_obs, y_obs):
            d_line.set_ydata([a * x_ob + b, y_ob])
            d_line.set_color(['green', 'red'][int(a * x_ob + b > y_ob)])
        
        scat.set_ydata([b])
        scat.set_xdata([a])
        
    def update_c(c=0):
        global a, b
        b = c
        update()

    def update_m(m=4):
        global a, b
        a = m
        update()
        
    plt.tight_layout()
    interact(update_c, c=(0, 12, 0.01))
    interact(update_m, m=(0, 4, 0.01))
    
def make_graph_2():
    
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(5, 7))
    
    def norm(x, mu=0, sig=1):
        return (2 * np.pi * sig ** 2) ** -0.5 * np.exp(-(x - mu) ** 2 / (2 * sig ** 2))
    
    x1 = np.linspace(-4, 4, 1001)
    x2 = np.linspace(-8, 8, 1001)
    
    ax1.plot(x1, norm(x1))
    ax1.plot([0, 0], [0, norm(0)], color='gray', ls='--')
    ax1.text(-0.15, -0.03, '$\mu$')
    ax1.plot([0, 1], [norm(1), norm(1)], color='gray', ls='--')
    ax1.text(0.3, 0.2, '$\sigma$')
    ax1.fill_between(np.linspace(-2, -1, 1001), norm(np.linspace(-2, -1, 1001)), alpha=0.5)
    ax1.text(-3.5, 0.2, ' Probability of \nbeing between\n   $a$ and $b$')
    ax1.plot([-2.4, -1.4], [0.18, 0.07], color='gray')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_ylim(-0.05, 0.45)
    ax1.text(-2.15, -0.03, '$a$')    
    ax1.text(-1.15, -0.03, '$b$')

    ax2.plot(x2, norm(x2, 0, 2), label='$\mu = 0$, $\sigma = 2$')
    ax2.plot(x2, norm(x2, 2, 1.5), label='$\mu = 2$, $\sigma = 1.5$')
    ax2.plot(x2, norm(x2, -3, 1), label='$\mu = -3$, $\sigma = 1$')
    ax2.set_xticks([])
    ax2.set_yticks([])
#     ax2.legend()
    plt.tight_layout()
    plt.show()