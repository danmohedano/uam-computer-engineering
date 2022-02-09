from Datos import Datos
import EstrategiaParticionado
import Clasificador


def main():
    dataset = Datos('data/tic-tac-toe.data')
    estrategia = EstrategiaParticionado.ValidacionCruzada(10)
    clasificador=Clasificador.ClasificadorNaiveBayes()
    media, std = clasificador.validacion(estrategia, dataset, 29)
    

if __name__ == '__main__':
    main()