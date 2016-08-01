# display arithmetic tables

# addition

firstcolumn=5 # width of the left column
column=4      # width of other columns

def header (symbol):
    result="{symbol:{width}s}".format(symbol=symbol, width=firstcolumn)
    for x in range(1,11):
        result += "{x:{width}d}".format(x=x, width=column)
    return result

def linePlus(n):
    result="{n:{width}s}".format(n=str(n), width=firstcolumn)
    for x in range(1,11):
        result+="{sum:{width}d}".format(sum=x+n, width=column)
    return result

def lineTimes(n):
    result="{n:{width}s}".format(n=str(n), width=firstcolumn)
    for x in range(1,11):
        result+="{prod:{width}d}".format(prod=x*n, width=column)
    return result

def tablePlus():
    print(header("+"))
    print()
    for x in range(1,11):
        print(linePlus(x))
    print()

def tableTimes():
    print(header("+"))
    print()
    for x in range(1,11):
        print(lineTimes(x))
    print()

tablePlus()
input("addition table ... hit a key\n")
tableTimes()
input("multiplication table ... hit a key\n")
