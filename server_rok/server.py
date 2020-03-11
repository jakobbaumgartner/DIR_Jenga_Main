# flamingo == '192.168.1.3'
# pavijan  == '192.168.1.2'

import funcTCP


def main():
    server = funcTCP.Server('192.168.1.7', 5000)
    # server = funcTCP.Server('localhost')
    server.povezi()
    server.poslusaj()

main()
