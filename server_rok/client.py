# flamingo == '192.168.1.3'
# pavijan  == '192.168.1.2'

import funcTCP


def main():
    gost = funcTCP.Gost('192.168.1.3',)
    msg = True
    while msg and msg != 'koncaj':
        msg = input('Vnesi sporocilo za server:    ')
        gost.poslji(msg)
    gost.ustavi()

main()
