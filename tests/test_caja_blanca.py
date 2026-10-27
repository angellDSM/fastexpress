"""Pruebas de CAJA BLANCA: un caso por cada camino independiente del CFG (V(G) = 9)."""
import pytest

from backend.tarifa import EnvioInvalido, calcular_tarifa

CAMINOS_VALIDOS = [
    ("C1", 3, "NUEVO", "ESTANDAR", 11.00),     # D3 V, D4 V, D7 V
    ("C2", 10, "NUEVO", "ESTANDAR", 45.00),    # D3 F
    ("C3", 3, "FRECUENTE", "ESTANDAR", 9.90),  # D4 F, D5 V
    ("C4", 3, "VIP", "ESTANDAR", 8.80),        # D5 F, D6 V
    ("C5", 3, "NUEVO", "EXPRESS", 13.75),      # D7 F, D8 V
]
CAMINOS_ERROR = [
    ("C6", 0, "NUEVO", "ESTANDAR"),         # D1 V -> error peso mínimo
    ("C7", 21, "NUEVO", "ESTANDAR"),        # D2 V -> límite excedido
    ("C8", 3, "OTRO", "ESTANDAR"),          # D6 F -> cliente inválido
    ("C9", 3, "NUEVO", "AEREO"),            # D8 F -> envío inválido
]


@pytest.mark.parametrize("cid,peso,cliente,envio,esperado", CAMINOS_VALIDOS)
def test_caminos_validos(cid, peso, cliente, envio, esperado):
    assert calcular_tarifa(peso, cliente, envio)["total"] == esperado


@pytest.mark.parametrize("cid,peso,cliente,envio", CAMINOS_ERROR)
def test_caminos_error(cid, peso, cliente, envio):
    with pytest.raises(EnvioInvalido):
        calcular_tarifa(peso, cliente, envio)


def test_desglose_completo():
    r = calcular_tarifa(10, "VIP", "EXPRESS")
    assert r == {"subtotal": 45.00, "descuento": 9.00, "recargo": 11.25, "total": 47.25}
