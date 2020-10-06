from tabulate import tabulate
from TurengParser import TurengParser
from ClipboardListener import ClipboardListener
import globals

def handler(text):
    items = TurengParser().search(text)
    table = map(lambda x: [x.Type, x.En, x.Tr], items)
    print(tabulate(table, headers=["Type", "En", "Tr"], showindex="always", tablefmt="fancy_grid"))

def main():
    ClipboardListener(handler).start()
    globals.wait.wait()


if __name__ == '__main__':
    main()    