"""
Modelo bicicleta com transferência de carga lateral -> gradiente de understeer K_us.

ATENÇÃO: todos os valores abaixo são PLACEHOLDERS ilustrativos.
Troque pelos dados reais do carro e pelo modelo de pneu (ex.: ajuste Magic Formula com dados TTC).
"""
from dataclasses import dataclass
import numpy as np

G = 9.81  # m/s²


@dataclass
class Veiculo:
    m: float = 300.0      # massa total com piloto [kg]
    L: float = 1.55       # entre-eixos [m]
    a: float = 0.85       # CG -> eixo dianteiro [m]
    h: float = 0.30       # altura do CG [m]
    tf: float = 1.20      # bitola dianteira [m]
    tr: float = 1.15      # bitola traseira [m]
    zrf: float = 0.04     # altura do centro de rolagem dianteiro [m]
    zrr: float = 0.06     # altura do centro de rolagem traseiro [m]
    Kf: float = 15000.0   # rigidez à rolagem dianteira [N·m/rad]
    Kr: float = 13000.0   # rigidez à rolagem traseira [N·m/rad]

    @property
    def b(self):          # CG -> eixo traseiro [m]
        return self.L - self.a


def ca_pneu(fz, c1=15.0, c2=0.004):
    """Rigidez de curva de um pneu [N/rad] em função da carga vertical [N].
    Modelo quadrático simples (placeholder): cresce com Fz, mas com concavidade."""
    fz = np.clip(fz, 0.0, None)
    return c1 * fz - c2 * fz**2


def kus(ay_g, v: Veiculo):
    """Gradiente de understeer em função da aceleração lateral [g].
    Retorna K_us em graus por g (positivo = understeer)."""
    ay = np.asarray(ay_g) * G

    # Cargas estáticas por eixo [N]
    Wf = v.m * G * v.b / v.L
    Wr = v.m * G * v.a / v.L

    # Braço de rolagem: CG até o eixo de rolagem
    z_eixo_rolagem = v.zrf + (v.zrr - v.zrf) * v.a / v.L
    braco = v.h - z_eixo_rolagem

    # Transferência de carga lateral por eixo [N] (parte geométrica + parte elástica)
    dfz_f = v.m * ay / v.tf * (v.b / v.L * v.zrf + braco * v.Kf / (v.Kf + v.Kr))
    dfz_r = v.m * ay / v.tr * (v.a / v.L * v.zrr + braco * v.Kr / (v.Kf + v.Kr))

    # Rigidez de curva por eixo (soma dos dois pneus: carregado + aliviado)
    Caf = ca_pneu(Wf / 2 + dfz_f) + ca_pneu(Wf / 2 - dfz_f)
    Car = ca_pneu(Wr / 2 + dfz_r) + ca_pneu(Wr / 2 - dfz_r)

    k_rad_por_g = Wf / Caf - Wr / Car
    return np.degrees(k_rad_por_g)


def esterco_necessario(raio, ay_g, v: Veiculo):
    """Ângulo de esterço de roda [graus]: delta = L/R + K_us * ay/g."""
    return np.degrees(v.L / raio) + kus(ay_g, v) * np.asarray(ay_g)


if __name__ == "__main__":
    v = Veiculo()
    ay = np.linspace(0.05, 1.5, 8)
    for a, k in zip(ay, kus(ay, v)):
        print(f"ay = {a:4.2f} g  ->  K_us = {k:6.2f} °/g")

    # Efeito de enrijecer a barra dianteira (mais transferência na frente)
    v2 = Veiculo(Kf=20000.0)
    print("\nKf 15000 -> 20000 em ay = 1.2 g:",
          f"{kus(1.2, v):.2f} -> {kus(1.2, v2):.2f} °/g")
