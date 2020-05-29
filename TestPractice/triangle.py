def isNumber(s):
    if isinstance(s,int) or isinstance(s,float):
        if s>0:
            return True
    return False

def triangle(a,b,c):
    if isNumber(a) and isNumber(b) and isNumber(c):
        if a<b+c and b<a+c and c<a+b:
            if a==b==c:
                return "Yes: Equilateral"
            elif a==b or b==c or c==a:
                return "Yes: Isosceles"
            else:
                return "Yes: Ordinary"
        else:
            return "No: Not Triangle"
    else:
        return "Error: Wrong Input"

def main():
    print(triangle("2",4,10))

if __name__ == '__main__':
    main()