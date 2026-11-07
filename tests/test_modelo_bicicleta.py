import numpy as np

from understeer.modelo_bicicleta import Veiculo, kus


def test_kus_retorna_um_valor_por_aceleracao():
    ay = np.linspace(0.1, 1.0, 5)
    assert kus(ay, Veiculo()).shape == ay.shape


def test_enrijecer_rolagem_dianteira_aumenta_understeer():
    base = Veiculo()
    mais_rigido = Veiculo(Kf=base.Kf * 1.5)
    assert kus(1.0, mais_rigido) > kus(1.0, base)
