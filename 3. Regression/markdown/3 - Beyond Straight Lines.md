
# 3 - Beyond Straight Lines

---

## Simple Linear Regression

So far we have seen how to perform simple linear regression in Python, that is, a situation where we have one set independant variables

$$
x\text{-data} \, = \, [x_1, x_2, x_3, ... , x_N]
$$

an associated set of dependant variables

$$
y\text{-data} \, = \, [y_1, y_2, y_3, ... , y_N]
$$

and we propose a simple linear fit. This means we guess that the data is well-approximated by a line of the form

$$
f(x) = mx + c
$$

![](../images/SLR.png)

Notice we have only two variables to find: the gradient, $m$, and the intercept $c$. 

## More Complicated Data

In reality, we are likely to encounter data which has a more complex relationship. For this reason, we need to start developing tools that are able to handle this additional complexity. For example, that happens if we observe data that looks like this?

![](../images/poly-reg.png)

Clearly a straight line will not be sufficient to describe data of this form. In this notebook we will begin to think about more general functions that simply staight lines. In particular, we will look at *polynomials*. 

## What is a polynomial?

A polynomial is a function of $x$ where we see things like $x^2$, $x^3$ ... A general polynomial contains an unlimited number of terms where we see $x$ *raised to a power*. Here are some examples of valid polynomial functions

$$
f(x) = 1 + x + x^2 
$$

$$
f(x) = 2 + x - 2x^2 
$$

$$
f(x) = -5 + 3x + x^2 + 5x^3
$$

$$
f(x) = -10 + \frac{x}{2} - 8x^2 + 5x^3 + \frac{x^4}{10}
$$

Polynomials are generally *curved* - they are not straight lines

## A General Quadratic Polynomial 

Let's assume our data has an underlying relationship that is of a *quadratic* form. This means we will consider as our model functions that include terms up to $x^2$. A general quadratic polynomial will have the form 

$$
f(x) = a + bx + cx^2
$$

## Exercise 1 

Use the interactive graph below to explore what happens to the quadratic polynomial curve when you adjust the coefficients $a, b$ and $c$. 


```python
import numpy as np
import matplotlib.pyplot as plt
```


```python
%matplotlib notebook
np.set_printoptions(precision=4, linewidth=500, threshold=500, suppress=True)
```


```python
%matplotlib notebook
```


```python
%load_ext autoreload
%autoreload 2
```


```python
from scripts.regression3 import make_graph_1

make_graph_1()
```


    <IPython.core.display.Javascript object>



<img src="data:image/png;base64,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n//5nzobRiQlJemCCy5Qjx49aoXN119/XYZhaMGCBXVep3rDiL///e/W/CP85MMPP5RhGLrooov08ccf19mVa+nSpbXO/9e//uXdMnXKlCkaP3687rrrLhmGoauuuqresG4YVUtANaSh+aSSNGnSJBlG1S5eU6dO1ciRI3XBBRfowgsvVGpqqk//5kALuoH8njbla+N0mvP+V49Ed+vWTWPHjtU777yjX//612rVqpU+/fTTWufW9x752u+zZs3SiBEjNGLECHXt2tU7Mj5ixIhaUyiseJ+AcEDQBZrgkUceUfv27b13n9e0ceNGGcapLYAPHjyoSy65RJ07d9bhw4drnZuTk6OOHTvqiiuuqHNDSfV8323btln3D/GDp59+usGPu388z3nhwoXq06ePLr74Yp111llq166dunfvrqFDh5pudNASoUySPv/8c1133XVq27atzjvvPD3yyCO1VtVorEALuoH6njb1a+N0mvv+L1q0SL169dLZZ5+t9u3bq3fv3oqOjq5zXn3vka/9HhERYXpu9Wtb9T4B4YCgC1jg7rvv1o033tjk53s8HvXs2VMPPfRQC1YFAEB4IegCFti1a5dat26thQsXNun58+fPV5s2beqd/wcAABqHoAsAAICQRNAFAABASAqJoJucnKznnntOPXr00BlnnFFnsn+16dOnq2vXrjrrrLN0zTXX6LvvvqtzTl5enp555hmdd9556tChgx5++OE6k/8BAAAQ+EIi6H777bf65S9/qUcffVTdunWrN+jOnTtXrVq10pAhQxQbG6vnn39erVu3rrPQdp8+ffTLX/5S8+fP18KFC9W9e3f17NmTu1kBAACCTEgEXbfb7f3vBx54oN6g261btzqLvt9yyy26++67vX+Oj4+XYRi11jncvXu3WrVqpfnz57d84QAAALBMSATdmuoLuvv27ZNhGHXugH///ffVpk0blZaWSpKGDh2q888/v84uVNdee62efvppK8sGAABACwuLoBsVFSXDMOos/L506VIZhqGkpCRJ0qOPPqpevXrVec1+/frpd7/7nWU1AwAAoOWFRdD97LPPZBiGsrKyaj2ekJAgwzC0bt06SdKdd96pe++9t85rvvjii+ratWuD183Pz1d6err32L9/v1auXKmDBw/WepyDg4ODg4ODoyWPgwcPKiEhQWVlZc0LUSEorIJu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fb7hILvdASJzNCQsgm5+fr4iIyN144036txzz1WnTp103333adu2bbXOS01NlWEYdY4+ffr4fE2aDggtJeWV+iIhTX0nra0VuC4d4NJTMzZoQWI6a7O2kMyCEk1dmaI7x6+s9V5fNjBK/T/7Qd/vy2azD6AGMoe5sAi627dv10UXXaTBgwdryZIlWrhwoXr37q327dsrKSnJe1510B0zZozWr1/vPWqe01g0HRC6tqfnacDXW3X1sNqjjFcNXayX529WbFKmSisYafRFZkGJZsWn6s/T1uvSAa5a7+vt4+I0ZWUKc6QBE2QOc2ERhKvongAAGIpJREFUdAsLC1VUVPsGhRMnTuj888/XSy+95H2sOuguWLCg2dek6YDQV1xWqUVbMvTXmRtrzeV1OF26eliMXpzzgxZtydCJUkZ665ORW6xP1qXqsanx6vyjcNs9MkYDv9mmxIM5jN4Cp0HmMBcWQdfMb3/7Wz322GPePxN0ATRV1olSfbx2vx740dQGh9OlroOi9dSMDfpo9T4lHckP2+BWWlGptclZesu1s860hOoR8X98nqjF2w+zpBvgAzKHubANurm5uWrfvr0iIyO9j1UH3QsuuEBnnHGGOnXqpP79+6ugwPcFx2k6IHwdyav6GP4vH31fawms6uOGt5bp5Xmb9dWmQzqYXRSywbeswq0fDuZo6soUPTNzo64curjOe3H1sBj9c26iYnYcIdwCTUTmMBe2QffZZ59Vhw4dlJGR4X3s8OHD6t+/vxYuXKi4uDiNHDlSZ599tm699dbT/iDKz89Xenq690hISKDpACivqFzfJB7Sv+Ym6voRS+sEvep1ep/9NEFTV6ZoY+rxoFxJwOPx6HBesZbuPKrxS3br8WnxumJIdL3/3j4TVmlU9C7Fp2SrrMJtd+lA0CPomgvaoJuXl6ekpKTTHhUVdefGffzxxzIMQ5988slpr/P555/LMAwtX768wfMiIyPrXbGBpgNQze32aGdGvqatStGT0783DYKdB1QtX/bC7E2asGyPFm8/ov1ZhQETCnOLypR4MEffJB7SqOhdenL697p2eP0h3uF06eZRy/XPuYmau+GgDucV210+EHIIuuaCNujOnDmz3mD54+PQoUO1nhcdHa3WrVtr6NChjbpOSUmJzjzzTI0ZM6bB8xjRBeCr8kq3th3K08y1+/WPzxN1y+gVpmGxeimzW0av0OPT4vXal1s0cflezd+YpmU7jyrxYI7Sjhc1a4mzikq38orKdSC7UBtTj+u7rRmasWa/RkXv0kvzNutPH67Vb95c0mCNlw2MUp8JqzTwm21akJiu9FyCLWA1gq65oA26TbF+/Xq1b99ezzzzTKOfU1paqjPOOENjx4716Vo0HYCmyMwvUdzuTE1ZmaKX5m1Wnwmr1GVQ3Xm+DR1dBkWpe2SMbnxrmSLGxqrPhFXqO2mt+k5aq/s/WKN7J67W3e+tVp8JqxQxNlbXj1hmOrrc0NF9WIz6TlqrQd9s05zvD2pLWi7zbAEbkDnMhU3Q3blzp84//3zdd9999U5nMDNnzhwZhqEVK1b4dD2aDkBLKa90K+XYCcXtztSs+FS95dqp52dt0j3vr9ZvRy6r94a3ljiuHLpYf3gnTo9OjdeLc37QmMVJ+iIhTQmpx5V1ojRkb6IDgg2Zw1xYBN3MzEz98pe/1MUXX6wVK1bU2gxi586d3vMiIyP10ksv6auvvtLy5cs1fPhwtW/fXhERET5/Q6fpAPiLx+NRXlG5Uo6d0Pf7srVs51Et2pKh+Qlp+jQ+VVNXpui9ZXv1/vK9+mDFXk2KTdbkuBRNWZmiT9al6stNh7R4+xGtTc7S5rRc7Tt2grV/gSBC5jAXFkE3Li7OdA5vRESE97y5c+fqhhtu0LnnnqvWrVurc+fOevXVV1VYWOjzNWk6AADgD2QOc2ERdO1A0wEAAH8gc5gj6FqEpgMAAP5A5jBH0LUITQcAAPyBzGGOoGsRmg4AAPgDmcMcQdciNB0AAPAHMoc5gq5FaDoAAOAPZA5zBF2L0HQAAMAfyBzmCLoWoekAAIA/kDnMEXQtQtMBAAB/IHOYI+hahKYDAAD+QOYwR9C1CE0HAAD8gcxhjqBrEZoOAAD4A5nDHEHXIjQdAADwBzKHOYKuRWg6AADgD2QOcwRdi9B0AADAH8gc5gi6FqHpAACAP5A5zBF0LULTAQAAfyBzmCPoWoSmAwAA/kDmMEfQtQhNBwAA/IHMYY6gaxGaDgAA+AOZwxxB1yI0HQAA8AcyhzmCrkVoOgAA4A9kDnMEXYvQdAAAwB/IHOYIuhah6QAAgD+QOcwRdC1C0wEAAH8gc5gj6FqEpgMAAP5A5jBH0LUITQcAAPyBzGGOoGsRmg4AAPgDmcMcQdciNB0AAPAHMoc5gq5FaDoAAOAPZA5zBF2L0HQAAMAfyBzmCLoWoekAAIA/kDnMEXQtQtMBAAB/IHOYI+hahKYDAAD+QOYwR9C1CE0HAAD8gcxhjqBrEZoOAAD4A5nDHEHXIjQdAADwBzKHOYKuRWg6AADgD2QOcwRdi9B0AADAH8gc5sIm6EZERMgwjDrHkSNHap2Xl5enZ555Ruedd546dOighx9+WIcPH/b5ejQdAADwBzKHubAKurfeeqvWr19f6ygvL691Xp8+ffTLX/5S8+fP18KFC9W9e3f17NlTFRUVPl2PpgMAAP5A5jAXVkH3gQceaPCc+Ph4GYahpUuXeh/bvXu3WrVqpfnz5/t0PZoOAAD4A5nDHEG3hqFDh+r888+Xx+Op9fi1116rp59+2qfr0XQAAMAfyBzmwironnPOOWrXrp3atm2r22+/XRs2bKh1zqOPPqpevXrVeW6/fv30u9/9zqfr0XQAAMAfyBzmwiboDhs2TDNmzNCqVas0d+5c9ezZU+3atdP27du959x5552699576zz3xRdfVNeuXRt8/fz8fKWnp3uPhIQEmg4AAFiOoGsuaINuXl6ekpKSTnuY3USWm5urn//853ryySe9j915552677776pzbv39/devWrcF6IiMj613VgaYDAABWIuiaC9qgO3PmzHqD5Y+PQ4cOmb5Gv379dOWVV3r/3JypC4zoAgAAOxB0zQVt0G0J/fr101VXXeX989ChQ/Wzn/2sznnXXXcdN6MBAICAROYwF7ZBNycnR506ddJTTz3lfax6ebHly5d7H9uzZw/LiwEAgIBF5jAXFkF369atuuuuuzRjxgzFxsZq9uzZ6t69u9q3b68dO3bUOrdPnz665JJL9MUXX2jRokXq0aOHevbsqcrKSp+uSdMBAAB/IHOYC4ugm56errvvvlsXXXSRfvKTn6hjx466//77lZiYWOfc6i2AO3bsqA4dOuihhx5SRkZGk65J0wEAAKuROcyFRdC1A00HAAD8gcxhjqBrEZoOAAD4A5nDHEHXIjQdAADwBzKHOYKuRWg6AADgD2QOcwRdi9B0AADAH8gc5gi6FqHpAACAP5A5zBF0LULTAQAAfyBzmCPoWoSmAwAA/kDmMEfQtQhNBwAA/IHMYY6gaxGaDgAA+AOZwxxB1yI0HQAA8AcyhzmCrkVoOgAA4A9kDnMEXYvQdAAAwB/IHOYIuhah6QAAgD+QOcwRdC1C0wEAAH8gc5gj6FqEpgMAAP5A5jBH0LUITQcAAPyBzGGOoGsRmg4AAPgDmcMcQdciNB0AAPAHMoc5gq5FaLr/397dh1ZZ/nEcvzbnQ2ezzZWb6Zam2R81G4qlIDpCY4EjUku0/hgIs5gQVmaJyUhyZpZFRA+YroJSNytmJCkbi0onDNIMdwrDB7aEEjtbcw869fP74/fz/Dxul9vU+77PfZ/3C64/vLz1XHB/1ffmeQAAAG6gOewIXYcwdAAAwA00hx2h6xCGDgAAuIHmsCN0HcLQAQAAN9AcdoSuQxg6AADgBprDjtB1CEMHAADcQHPYEboOYegAAIAbaA47QtchDB0AAHADzWFH6DqEoQMAAG6gOewIXYcwdAAAwA00hx2h6xCGDgAAuIHmsCN0HcLQAQAAN9AcdoSuQxg6AADgBprDjtB1CEMHAADcQHPYEboOYegAAIAbaA47QtchDB0AAHADzWFH6DqEoQMAAG6gOewIXYcwdAAAwA00hx2h6xCGDgAAuIHmsEuI0D1+/LiMMb2uIUOG9HldYWHhgB+ToQMAAG6gOewSInS7urpUX18fs/bv36/09HQ99thj0esuh+6GDRtirg2HwwN+TIYOAAC4geawS4jQ7U1dXZ2MMaqsrIzuXQ7dr7/++oZ/f4YOAAC4geawS9jQLSkp0a233qrOzs7oHqELAAD8huawS8jQPX/+vDIzM1VcXByzfzl0b7/9diUnJysrK0ulpaX6999/B/wYDB0AAHADzWGXkKFbXV0tY4z27NkTs3/q1CmVlpaqurpadXV1WrdunVJTUzVr1ixdunTpmr9na2urmpubo6uhoYGhAwAAjiN07Xwbui0tLQqHw32u7u7uHr924cKFys7O1oULF/p8nC+++ELGGNXU1FzzurKysl7fsYGhAwAATiJ07XwbuhUVFda3DLtyNTU1xfy6trY2hUIhPfvss/16nM7OTg0aNEgbNmy45nV8RxcAAHiB0LXzbeher88++0zGGB04cKBf13d1dSk5OVlvvPHGgB6HoQMAAG6gOewSLnQfeeQRTZgwod/Xf/755zLGqLa2dkCPw9ABAAA30Bx2CRW6f//9t1JSUvTKK6/0+vNlZWVavny5du7cqZqaGq1du1ahUEgFBQV9vhjtagwdAABwA81hl1Ch+95778kYo8bGxl5/ftu2bZo6darS09OVkpKicePGacWKFTp79uyAH4uhAwAAbqA57BIqdN3E0AEAADfQHHaErkMYOgAA4Aaaw47QdQhDBwAA3EBz2BG6DmHoAACAG2gOO0LXIQwdAABwA81hR+g6hKEDAABuoDnsCF2HMHQAAMANNIcdoesQhg4AALiB5rAjdB3C0AEAADfQHHaErkMYOgAA4Aaaw47QdQhDBwAA3EBz2BG6DmHoAACAG2gOO0LXIQwdAABwA81hR+g6hKEDAABuoDnsCF2HMHQAAMANNIcdoesQhg4AALiB5rAjdB3C0AEAADfQHHaErkMYOgAA4Aaaw47QdQhDBwAA3EBz2BG6DmHoAACAG2gOO0LXIQwdAABwA81hR+g6hKEDAABuoDnsCF2HMHQAAMANNIcdoesQhg4AALiB5rAjdB3C0AEAADfQHHaErkMYOgAA4Aaaw47QdQhDBwAA3EBz2BG6DmHoAACAG2gOO0LXIQwdAABwA81hR+g6hKEDAABuoDnsCF2HMHQAAMANNIcdoesQhg4AALiB5rAjdB3C0AEAADfQHHaErkMYOgAA4Aaaw47QdQhDBwAA3EBz2BG6DmHoAACAG2gOO0LXIQwdAABwA81hR+g6hKEDAABuoDnsAhG627dv17x58zRq1CgZY1RRUdHrdS0tLVqyZIlGjBihtLQ0LViwQKdOnepx3b59+zR9+nQNGzZMd955p15//XVdunRpQGdi6AAAgBtoDrtAhO7jjz+uKVOmaMmSJdcM3cLCQuXk5GjHjh2qrq5WXl6e8vPz1d3dHb3m6NGjSktL07x581RTU6NNmzZpyJAh2rhx44DOxNABAAA30Bx2gQjdixcvSpIikYg1dPfv3y9jjPbu3Rvd++2335SUlKQdO3ZE95YuXapx48bp3Llz0b1Vq1YpIyNDXV1d/T4TQwcAANxAc9gFInQvu1borlmzRpmZmT2egjB58mQVFxdHf5ybm6vnnnsu5ppffvlFxhjV1dX1+ywMHQAAcAPNYZcwofvEE09oxowZPfaffPJJTZs2TZJ09uxZGWO0efPmmGvOnTunpKQkffDBB/0+C0MHAADcQHPYJUzozpkzR3Pnzu2xv2zZMk2cOFHS/welqqqqx3Wpqalat26d9bFbW1vV3NwcXQcOHJAxRg0NDTH7LBaLxWKxWDdzNTQ0yBijkydPXn9EBVRchm5LS4vC4XCf68oXkUl9h25RUVGP/dLSUt1zzz2S/h+6O3fu7HFdKBRSeXm59cxlZWUyxrBYLBaLxWJ5shoaGgZYXMEXl6FbUVHRrxva1NQU8+u8fOrC1d/RPXbsmL7//nudPHnS86/0nPiqke9U+2dxz/y1uF/+Wtwvf62g3q+TJ0+qoaEh5oX0+K+4DN3r1deL0W677bYe+1OmTOnxYrTnn38+5prDhw/LmIG9GC2ompt5HpDfcM/8hfvlL9wvf+F+JZ6ECd3Lby9WU1MT3fv99997fXuxu+66S+fPn4/urV69WhkZGXylJP6S8CPumb9wv/yF++Uv3K/EE4jQPXLkiKqqqvTpp5/KGKNly5apqqpKu3fvjrmusLBQubm5qqys1K5duzRp0iTl5+frwoUL0WuOHj2q1NRULViwQLW1tXrnnXeu6wMjgoq/JPyHe+Yv3C9/4X75C/cr8QQidG0vBBs7dmzMdZc/AjgjI0NpaWmaP3++/vzzzx6/3759+zRt2jQNHTpUOTk5Wr9+/YA/AjioWltbVVZWptbWVq+Pgn7invkL98tfuF/+wv1KPIEIXQAAAOBqhC4AAAACidAFAABAIBG6AAAACCRCFwAAAIFE6OKm+eqrr2SMUX5+vtdHQS8uv9r4gQceUHp6urKyslRUVKTDhw97fTRICofDmjNnjkKhkLKzs/Xiiy/y3t1xqrKyUo8++qjGjBmj1NRU5efna8uWLbw7j0+0tbVpzJgxMsbo4MGDXh8HDiN0cVN0dHRo3Lhxys7OJnTj1K+//qpRo0Zp9erV2rNnj6qrqzVz5kyFQiGFw2Gvj5fQ/vnnH91xxx2aNWuWvvvuO23ZskXp6elatmyZ10dDL6ZPn65FixZp+/btqq2t1csvv6zk5GStXbvW66OhH1auXKns7GxCN0EQurgp1qxZo1mzZqm4uJjQjVNnz55Ve3t7zF5bW5syMzO1fPlyj04FSSovL1daWprOnDkT3fvoo480aNCgXt/rG946ffp0j72SkhKNGDHCg9NgIMLhsFJTU/Xhhx8SugmC0MUN++OPPxQKhXTo0CFC14cefPBBLVy40OtjJLSZM2dq3rx5MXuRSERJSUm9fqQ54s/7778vY4w6Ojq8Pgqu4eGHH9YLL7yguro6QjdBELq4YXPnztUzzzwjSYSuz0QiEYVCIZWVlXl9lIQ2cuRIrV69usf+6NGj9dJLL3lwIgzU4sWLe3waJ+JLVVWVsrKy1NraSugmEEIXN2TXrl0aMWJE9L/yCF1/KSkpUVpaGv897rGUlBRt3Lixx/59992nkpISD06Egfjxxx+VnJysd9991+ujwKK9vV25ubnasmWLJBG6CYTQRYyWlhaFw+E+V3d3tzo7OzV+/PiYv9wJXXcN5H5dbevWrTLG6JNPPvHg5LhSSkqK3nzzzR779957r5YuXerBidBfTU1NGj16tGbPnq2LFy96fRxYrFq1SlOnTo3eI0I3cRC6iFFRUSFjTJ+rqalJ69ev1913363Tp08rEokoEolo8eLFysvLUyQS4a2RXDCQ+3Wl3bt3KyUlRWvWrPHo5LgST13wp0gkory8PE2aNEktLS1eHwcWJ06c0JAhQ/Ttt99G/6365ptvZIzRDz/8oLa2Nq+PCAcRurhuxcXF14yrzZs3e31E9KK+vl6hUEhLlizx+ij4n5kzZ2r+/Pkxey0tLbwYLY51dHRoxowZys3NVXNzs9fHwTVc/u6tbc2YMcPrI8JBhC6uWzgcVl1dXcwqLCzUhAkTVFdXp1OnTnl9RFzlyJEjyszMVFFRUa9PZ4A3ysvLNXz4cEUikeje5s2blZKSwvOn41B3d7eKioqUmZmpI0eOeH0c9CESifT4t+rtt9+OfkPm559/9vqIcBChi5uK5+jGr7/++ks5OTkaM2aMamtrVV9fH138Y+2tyx8YUVBQoD179mjr1q3KyMjgAyPiVElJiYwxeuutt2L+HNXX16urq8vr46EfeI5u4iB0cVMRuvHrWv99V1BQ4PXxEl5jY6Nmz56tW265RVlZWVqxYgXPc49TY8eOtf5ZOn78uNfHQz8QuomD0AUAAEAgEboAAAAIJEIXAAAAgUToAgAAIJAIXQAAAAQSoQsAAIBAInQBAAAQSIQuAAAAAonQBQAAQCARugAAAAgkQhcAAACBROgCAAAgkAhdAPBYJBJRTk6OFi1aFLP/1FNPafTo0Tpz5oxHJwMAfyN0ASAO7N27V0lJSdq2bZsk6csvv5QxRrt37/b4ZADgX4QuAMSJ0tJSZWZm6uDBgxo5cqSefvppr48EAL5G6AJAnGhvb9fEiRM1dOhQjR8/Xm1tbV4fCQB8jdAFgDiyYsUKGWP06quven0UAPA9QhcA4sTBgwc1ePBgTZ48WWlpaTp27JjXRwIAXyN0ASAOdHV1KS8vTw899JA6Ozt1//33q6CgQJcuXfL6aADgW4QuAMSBlStXavjw4Tpx4oQk6dChQxo8eLA2bdrk8ckAwL8IXQDw2E8//aTk5GR9/PHHMfuvvfaahg0bpsbGRo9OBgD+RugCAAAgkAhdAAAABBKhCwAAgEAidAEAABBIhC4AAAACidAFAABAIBG6AAAACCRCFwAAAIFE6AIAACCQCF0AAAAEEqELAACAQCJ0AQAAEEiELgAAAAKJ0AUAAEAg/QdPY/4hSeYtFQAAAABJRU5ErkJggg==" width="639.8333333333334">




### Fitting a Quadratic Polynomial

For a given set of data, our task is to find the values of $a, b$ and $c$ that *fit that data the best*. 

Let's say we have settled on some values for $a, b$ and $c$. In that case, our prediction for the value of the curve at our first input point $x_1$ will be 

$$
f(x_1) = a + bx_1 + cx_1^2
$$

however, we have observed a real value of $y_1$. The square difference will be 

$$
\begin{align}
(\text{observed value} - \text{predicted value})^2 &= \big(y_1 - f(x_1)\big)^2 \\
&= \big( y_1 - (a + bx_1 + cx_1^2) \, \big) ^2
\end{align}
$$

Like before, the task of finding the best values for our parameters can be rephrased as minimising the total squared difference between our prediction and our observation across *all* our observations

$$
\begin{align}
\text{Total Error} &= \sum_{i=1}^{N} \big(y_i - f(x_i)\big)^2\\
&= \sum_{i=1}^{N} \big(y_i - (a + bx_i + cx_i^2) \big)^2
\end{align}
$$

## Exercise 2 - Creating some artificial data

For the purpose of this notebook we will create some artificial data, as before. This time you will create it yourself. If you need a reminder on how any of the numpy or matplotlib functions work, create a new cell by clicking to the left of an existing cell and hitting `a` or `b`, then type the function you need help with followed by a question mark. E.g.

```python
plt.scatter?
```

### Exercise 2.1 

Create an array called `x_data` which has evenly spaced numbers using the function `np.linspace`. Choose some sensible numbers as the start and end point, as well as the number of steps to take by assigning the variables `x_start`, `x_end` and `n_observations`. Print out your newly created array and examine it to make sure everything looks ok. 


```python
# YOUR CODE HERE

x_start = 
x_end = 
n_observations =

x_data =      
```

### Exercise 2.3 

Set some values for $a, b$ and $c$ between -10 and 10. These will be used to create a variable called `y_true`, which will represent the 'true' underlying y-values, before any noise has been added. Print out this value and check it seems alright. 


```python
# YOUR CODE HERE

a = 
b = 
c = 
y_true = a + b * x_data + c * x_data ** 2
```

### Exercise 2.4 

Using the numpy function `np.random.normal`, create a new array called `noise`. Remember, this takes three arguments. The first is the mean (which will be 0), the second is the standard deviation (the width of the random distribution, which we often call $\sigma$ [sigma]) and the final argument is the length of the array. Print out your noise array to make sure it is the right length. Then create a new variable called `y_data` by adding together `y_true` and `noise`. 


```python
# YOUR CODE HERE

sigma = 
noise = 
y_data = 
```

### Exercise 2.5 

Create a scatter plot to examine the data you have created using `plt.scatter`. If needs be, go back and edit the variables you have set until you have some fake data you are happy with. 

HINT: if you make the standard deviation of the noise too high, you won't be able to see the relationship. 


```python
# YOUR CODE HERE

```

## Solving the regression problem 

### Linear Algebra

Before we solve the regression problem with code, we are going to take a brief look at something called **linear albegra**. Linear algebra is a topic in maths that will help us to talk efficiently about data. There are two important concepts to understand: **vectors** and **matrices**. 

### Vectors

A vector can be thought of as a 1D list of numbers. In maths, we usually write vectors as a column like this 

$$
\mathbf{v} = \begin{bmatrix} v_1 \\ v_2 \\ v_3 \\ \vdots \\ v_N\end{bmatrix}
$$

If two vectors have the same length, we can add them together like this 

$$
\mathbf{u} + \mathbf{v} = \begin{bmatrix} u_1 \\ u_2 \\ u_3 \\ \vdots \\ u_N\end{bmatrix} + \begin{bmatrix} v_1 \\ v_2 \\ v_3 \\ \vdots \\ v_N\end{bmatrix} = \begin{bmatrix} u_1 + v_1 \\ u_2 + v_2 \\ u_3 + v_3 \\ \vdots \\ u_N + v_N\end{bmatrix}
$$

or subtract them like this

$$
\mathbf{u} - \mathbf{v} = \begin{bmatrix} u_1 \\ u_2 \\ u_3 \\ \vdots \\ u_N\end{bmatrix} - \begin{bmatrix} v_1 \\ v_2 \\ v_3 \\ \vdots \\ v_N\end{bmatrix} = \begin{bmatrix} u_1 - v_1 \\ u_2 - v_2 \\ u_3 - v_3 \\ \vdots \\ u_N - v_N\end{bmatrix}
$$

We can also flip a vector, to make it into a row vector, by adding a $\top$, for *transpose*. 

$$
\mathbf{v}^{\top} = \begin{bmatrix} v_1, \; v_2, \;  v_3, \; ... , \; v_N\end{bmatrix}
$$

When you see a vector transposed, times a regular vector, the meaning is that we multiply each corresponding pair of elements and add them all together

$$
\begin{align}
\mathbf{u}^{\top}\mathbf{v} &=  \begin{bmatrix} u_1, \; u_2, \;  u_3, \; ... , \; u_N\end{bmatrix} \;\, \times \;\, \begin{bmatrix} v_1 \\ v_2 \\ v_3 \\ \vdots \\ v_N\end{bmatrix} \\[0.5cm]
&= u_1 v_1 + u_2 v_2 + u_3 v_3 + ... + u_N v_N 
\end{align}
$$

This is often referred to as the *dot product*. 

#### Example

$$
\mathbf{u} = \begin{bmatrix} 1 \\ 2 \\  3 \end{bmatrix}, \quad \mathbf{v} = \begin{bmatrix} 4 \\ 5 \\  6 \end{bmatrix}\\[2cm]
$$

$$
\mathbf{u} + \mathbf{v} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} + \begin{bmatrix} 4 \\ 5 \\ 6 \end{bmatrix} = \begin{bmatrix} 5 \\ 7 \\  9 \end{bmatrix} \\[2cm]
\mathbf{u} - \mathbf{v} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} - \begin{bmatrix} 4 \\ 5 \\ 6 \end{bmatrix} = \begin{bmatrix} -3 \\ -3 \\  -3 \end{bmatrix}\\[2cm]
\mathbf{u}^{\top}\mathbf{v} = (1 \times 4) + (2 \times 5) + (3 \times 6) = 32
$$

### Matrices

A matrix is a *rectangle* of numbers. You can think of a matrix as being multiple row vectors stacked on top of each other

$$
A = \begin{bmatrix}
\rule[.5ex]{4.5ex}{0.5pt} \; \mathbf{a}_1^{\top} \; \rule[.5ex]{4.5ex}{0.5pt} \\
\rule[.5ex]{4.5ex}{0.5pt} \; \mathbf{a}_2^{\top} \; \rule[.5ex]{4.5ex}{0.5pt} \\
\rule[.5ex]{4.5ex}{0.5pt} \; \mathbf{a}_3^{\top} \; \rule[.5ex]{4.5ex}{0.5pt} \\
 \vdots \\ 
 \rule[.5ex]{4.5ex}{0.5pt} \; \mathbf{a}_M^{\top} \; \rule[.5ex]{4.5ex}{0.5pt}
 \end{bmatrix}
$$

If each of these row vectors has length $N$, and we stack $M$ vectors on top of each other, then the matrix is a rectangle of numbers with height $M$ and width $N$. 

Matrices *multiply vectors*. A matrix multiplied by a vector gives us a new vector. Each element of this new vector is the dot product between each row of the matrix, and the original vector. 

$$
A \mathbf{v} = \begin{bmatrix}
\rule[.5ex]{4.5ex}{0.5pt} \; \mathbf{a}_1^{\top} \; \rule[.5ex]{4.5ex}{0.5pt} \\
\rule[.5ex]{4.5ex}{0.5pt} \; \mathbf{a}_2^{\top} \; \rule[.5ex]{4.5ex}{0.5pt} \\
\rule[.5ex]{4.5ex}{0.5pt} \; \mathbf{a}_3^{\top} \; \rule[.5ex]{4.5ex}{0.5pt} \\
 \vdots \\ 
 \rule[.5ex]{4.5ex}{0.5pt} \; \mathbf{a}_M^{\top} \; \rule[.5ex]{4.5ex}{0.5pt}
 \end{bmatrix} \; \begin{bmatrix}\rule[-1ex]{0.5pt}{3.5ex} \\  \mathbf{v} \\ \rule[-1ex]{0.5pt}{3.5ex} \end{bmatrix} 
 = \begin{bmatrix} \mathbf{a}_1^{\top} \mathbf{v} \\ \mathbf{a}_2^{\top} \mathbf{v} \\ \mathbf{a}_3^{\top} \mathbf{v} \\ \vdots \\ \mathbf{a}_M^{\top} \mathbf{v} \end{bmatrix}
$$

#### Example

$$
A = \begin{bmatrix}
1 & 2 & 3 \\
2 & 3 & 4 \\
3 & 4 & 5 \\
4 & 5 & 6 \\
\end{bmatrix} \quad 
\mathbf{v} =  \begin{bmatrix}
3 \\
2 \\
1 \\
\end{bmatrix} \\[2cm]
A\mathbf{v} = \begin{bmatrix}
(3 \times 1) + (2 \times 2) + (1 \times 3) \\
(3 \times 2) + (2 \times 3) + (1 \times 4) \\
(3 \times 3) + (2 \times 4) + (1 \times 5) \\
(3 \times 4) + (2 \times 5) + (1 \times 6) \\
\end{bmatrix} = 
\begin{bmatrix}
3 + 4 + 3\\
6 + 6 + 4 \\
9 + 8 + 5 \\
12 + 10 + 6 \\
\end{bmatrix}
 = 
\begin{bmatrix}
10 \\
16 \\
23 \\
28 \\
\end{bmatrix}
$$

## Framing the regression problem with Linear Algebra

Consider a matrix $X$, created out of our collected data, which has the following form 

$$
X = \begin{bmatrix}
1 & x_1 & x_1^2 \\
1 & x_2 & x_2^2 \\
1 & x_3 & x_3^2 \\
 \vdots & \vdots & \vdots\\ 
1 & x_N & x_N^2
\end{bmatrix}
$$

Now consider a vector made up of our parameters $a, b$ and $c$

$$
\mathbf{w} = \begin{bmatrix}
a \\
b \\
c \\
\end{bmatrix}
$$

What happens when we multiply $\mathbf{w}$ by $X$?

$$
\begin{align}
X\mathbf{w} &= \begin{bmatrix}
1 & x_1 & x_1^2 \\
1 & x_2 & x_2^2 \\
1 & x_3 & x_3^2 \\
 \vdots & \vdots & \vdots\\ 
1 & x_N & x_N^2
\end{bmatrix} \; \begin{bmatrix}
a \\
b \\
c \\
\end{bmatrix} \\[0.5cm]
&=  \begin{bmatrix}
a + bx_1 + cx_1^2\\
a + bx_2 + cx_2^2 \\
a + bx_3 + cx_3^2 \\
\vdots \\
a + bx_N+ cx_N^2
\end{bmatrix}
\end{align}
$$

For a given $a, b$ and $c$, $X\mathbf{w}$ represents a vector of our *predictions*. 

Consider a vector $\mathbf{y}$ containing our observations

$$
\mathbf{y} = \begin{bmatrix}
y_1 \\
y_2 \\
y_3 \\
\vdots \\
y_N
\end{bmatrix}
$$

The difference between our observations and our predictions is 

$$
\begin{align}
\mathbf{y} - X\mathbf{w} &= 
\begin{bmatrix}
y_1 \\
y_2 \\
y_3 \\
\vdots \\
y_N
\end{bmatrix} - 
\begin{bmatrix}
a + bx_1 + cx_1^2\\
a + bx_2 + cx_2^2 \\
a + bx_3 + cx_3^2 \\
\vdots \\
a + bx_N+ cx_N^2
\end{bmatrix} \\[0.5cm]
&= \begin{bmatrix}
y_1 - (a + bx_1 + cx_1^2) \\
y_2 - (a + bx_2 + cx_2^2) \\
y_3 - (a + bx_3 + cx_3^2) \\
\vdots \\
y_N - (a + bx_N+ cx_N^2)
\end{bmatrix}
\end{align}
$$

And our total error is 

$$
(\mathbf{y} - X\mathbf{w})^{\top}(\mathbf{y} - X\mathbf{w})
$$

## Exercise 3 - Making $X$

In order to solve the regression problem, we need to construct the matrix $X$. 

### Exercise 3.1 

We will start with a blank matrix filled with zeros. Using the function `np.zeros`, create a blank matrix called `X` with a height of `n_observations` and a width of 3. 


```python
# YOUR CODE HERE 

X = 
print(X)
```

### Exercise 3.2 

Populate the first column of `X` with all ones


```python
# YOUR CODE HERE

print(X)
```

### Exercise 3.3 
Populate the second column of `X` with the array `x_data`


```python
# YOUR CODE HERE

print(X)
```

### Exercise 3.4 
Populate the third column of `X` with the array `x_data` squared


```python
# YOUR CODE HERE

print(X)
```

## Exercise 4 - Solving the regression problem

As before, in order to solve the linear regression problem we will use the numpy function `np.linalg.lstsq`. This function takes two arguments. The first is our data matrix `X`. The second is the observation vector `y_data`. This function will return us the vector $\mathbf{w}$ that minimises 

$$
(\mathbf{y} - X\mathbf{w})^{\top}(\mathbf{y} - X\mathbf{w})
$$

### Exercise 4.1 

Call `np.linalg.lstsq` on `X` and `y_data`. See the results


```python
# YOUR CODE HERE


```

### Exercise 4.2 

Create a new variable called `w_fit` and assign the first element of the previous return value to it. Print out the best values for $a, b$ and $c$. How close are they to the values you set before?


```python
# YOUR CODE HERE

```

## Exercise 5 - Solving a cubic polynomial problem 

Now we will repeat the process, but this time we will propose a *cubic* model. This means we must construct a matrix $X$ that has an extra column, with the cube of our data inputs. 

### Exercise 5.1 

Using the same `x_data` array, create a new matrix `X_cubic` which has the form 

$$
X = \begin{bmatrix}
1 & x_1 & x_1^2 & x_1^3 \\
1 & x_2 & x_2^2 & x_2^3 \\
1 & x_3 & x_3^2 & x_3^3 \\
 \vdots & \vdots & \vdots & \vdots \\ 
1 & x_N & x_N^2 & x_N^3
\end{bmatrix}
$$



```python
# YOUR CODE HERE

X_cubic = 
```

### Exercise 5.2 

Create a new array `y_data_cubic` by setting new values for $a, b, c$ and a new $d$. 


```python
a = 
b = 
c = 
d = 

y_data_cubic = a + b * x_data + c * x_data ** 2 + d * x_data ** 3 + noise
```

### Exercise 5.3 

Use `np.linalg.lstsq` to solve the regression problem


```python

```
