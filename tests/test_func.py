def eq(a, b):
    if type(a) == int and type(b) == int:
        return a == b
    else:
        return a.fr == b.fr and a.to == b.to and a.ln == b.ln


def list_eq(a, b):
    c = zip(a, b)
    return all(map(lambda x: eq(x[0], x[1]), c))
