from Datos import Datos
import EstrategiaParticionado
import Clasificador


def main():
    dataset = Datos('data/tic-tac-toe.data')
    estrategia = EstrategiaParticionado.ValidacionCruzada(10)
    clasificador=Clasificador.ClasificadorNaiveBayes()
    

if __name__ == '__main__':
    main()