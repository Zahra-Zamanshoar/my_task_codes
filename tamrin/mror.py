def zahra(*args):
    for arg in args:
        arg = float(arg)
        arg = arg ** arg
    print(arg)
b =zahra(2,3)
print (b)