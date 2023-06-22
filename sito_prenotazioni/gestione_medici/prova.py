import random
class Prova():
    a = 3
    def metodo2(self):
        self.metodo()

    def metodo(self):
        print("Funziona")


if __name__ == '__main__':
    b = Prova()
    print(dir(b))
    b.a = 20
    print(dir(b))