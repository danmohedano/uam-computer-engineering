import math

def main():
    with open('claves', 'w') as f:
        str = 'static const unsigned short AFIN_CLAVES[] = {\n'
        counter = 0
        for a in range(26):
            if math.gcd(a, 26) == 1:
                str += '\t'
                for b in range(26):
                    counter += 1
                    str += '{ ' + f'{a}, {b}' + '}, '

                str += '\n'

        str += '};'

        f.write(str)

        print(counter)

if __name__ == '__main__':
    main()