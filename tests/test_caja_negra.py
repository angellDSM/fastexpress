"""Pruebas de CAJA NEGRA: Particiones de Equivalencia, BVA y Tabla de Decisión."""
import pytest

from backend.tarifa import EnvioInvalido, calcular_tarifa

# ---------- Particiones de equivalencia y BVA: PESO (NUEVO + ESTANDAR) ----------
PESO_VALIDO = [
    ("CN-01", 2.50, 10.00),   # EP: tramo 1 (representativo)
    ("CN-02", 12.00, 53.00),  # EP: tramo 2 (representativo)
    ("CN-03", 0.01, 5.02),    # BVA: mínimo válido
    ("CN-04", 0.02, 5.04),    # BVA: mínimo + 1
    ("CN-05", 4.99, 14.98),   # BVA: límite tramo 1 - 1
    ("CN-06", 5.00, 15.00),   # BVA: límite superior tramo 1
    ("CN-07", 5.01, 25.04),   # BVA: límite inferior tramo 2
    ("CN-08", 5.02, 25.08),   # BVA: límite tramo 2 + 1
    ("CN-09", 19.99, 84.96),  # BVA: máximo - 1
    ("CN-10", 20.00, 85.00),  # BVA: máximo válido
]
PESO_INVALIDO = [
    ("CN-11", -1.00),   # EP: negativo
    ("CN-12", 0.00),    # BVA: mínimo - 1
    ("CN-13", 20.01),   # BVA: máximo + 1
    ("CN-14", 25.00),   # EP: mayor a 20 kg
]


@pytest.mark.parametrize("cid,peso,esperado", PESO_VALIDO)
def test_peso_valido(cid, peso, esperado):
    assert calcular_tarifa(peso, "NUEVO", "ESTANDAR")["total"] == esperado


@pytest.mark.parametrize("cid,peso", PESO_INVALIDO)
def test_peso_invalido(cid, peso):
    with pytest.raises(EnvioInvalido):
        calcular_tarifa(peso, "NUEVO", "ESTANDAR")


# ---------- Particiones y BVA: MONTO (total a pagar) ----------
MONTO = [
    ("CN-15", 0.01, "VIP", "ESTANDAR", 4.02),      # monto mínimo posible
    ("CN-16", 0.01, "NUEVO", "ESTANDAR", 5.02),    # mínimo sin descuento
    ("CN-17", 5.00, "NUEVO", "ESTANDAR", 15.00),   # tope de la partición 1
    ("CN-18", 5.01, "NUEVO", "ESTANDAR", 25.04),   # piso de la partición 2 (salto)
    ("CN-19", 20.00, "NUEVO", "ESTANDAR", 85.00),  # máximo sin recargo
    ("CN-20", 20.00, "NUEVO", "EXPRESS", 106.25),  # monto máximo posible
]


@pytest.mark.parametrize("cid,peso,cliente,envio,esperado", MONTO)
def test_monto(cid, peso, cliente, envio, esperado):
    assert calcular_tarifa(peso, cliente, envio)["total"] == esperado


# ---------- Tabla de decisión: Cliente x Envío (peso fijo 10 kg, subtotal $45.00) ----------
TABLA_DECISION = [
    ("R1", "NUEVO", "ESTANDAR", 45.00),
    ("R2", "NUEVO", "EXPRESS", 56.25),
    ("R3", "FRECUENTE", "ESTANDAR", 40.50),
    ("R4", "FRECUENTE", "EXPRESS", 51.75),
    ("R5", "VIP", "ESTANDAR", 36.00),
    ("R6", "VIP", "EXPRESS", 47.25),
]


@pytest.mark.parametrize("regla,cliente,envio,esperado", TABLA_DECISION)
def test_tabla_decision(regla, cliente, envio, esperado):
    assert calcular_tarifa(10, cliente, envio)["total"] == esperado


@pytest.mark.parametrize("regla,cliente,envio", [
    ("R7", "PREMIUM", "ESTANDAR"),
    ("R8", "VIP", "NOCTURNO"),
])
def test_tabla_decision_invalidas(regla, cliente, envio):
    with pytest.raises(EnvioInvalido):
        calcular_tarifa(10, cliente, envio)
