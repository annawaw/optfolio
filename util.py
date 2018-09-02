import math

def p2f(x):
    return float(x.strip('%'))/100.0


def sigmoid(x):
  return 1 / (1 + math.exp(-x))