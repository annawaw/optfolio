import math, statistics

def p2f(x):
    return float(x.strip('%'))/100.0


def sigmoid(x):
  return 1 / (1 + math.exp(-x))


def geometric_mean(xs):
    r = 1.0
    c = 0
    for x in xs:
        r *= x
        c += 1

    return math.pow(r, 1.0/c)
