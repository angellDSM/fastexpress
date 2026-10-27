"""Módulo de Cotización de Envíos y Descuentos "FastExpress".

Función core: calcular_tarifa(peso, tipo_cliente, tipo_envio)
Reglas:
  BR-01 Tarifa base $5.00
  BR-02 0.01-5.00 kg: $2.00/kg | 5.01-20.00 kg: $4.00/kg | >20 kg: rechazar
  BR-03 NUEVO 0% | FRECUENTE 10% | VIP 20% (sobre el subtotal)
  BR-04 ESTANDAR 0% | EXPRESS +25% sobre el subtotal
Total = subtotal - descuento + recargo, redondeado a 2 decimales.
"""

TARIFA_BASE = 5.00
PESO_MIN = 0.01
LIMITE_TRAMO_1 = 5.00
PESO_MAX = 20.00


class EnvioInvalido(ValueError):
    """Error de validación de una orden de envío."""


def calcular_tarifa(peso, tipo_cliente, tipo_envio):
    if peso < PESO_MIN:                              # D1
        raise EnvioInvalido("Peso inválido: mínimo 0.01 kg")
    if peso > PESO_MAX:                              # D2
        raise EnvioInvalido("Límite excedido: máximo 20.00 kg")

    if peso <= LIMITE_TRAMO_1:                       # D3
        costo_peso = peso * 2.00
    else:
        costo_peso = peso * 4.00
    subtotal = TARIFA_BASE + costo_peso

    if tipo_cliente == "NUEVO":                      # D4
        pct_descuento = 0.00
    elif tipo_cliente == "FRECUENTE":                # D5
        pct_descuento = 0.10
    elif tipo_cliente == "VIP":                      # D6
        pct_descuento = 0.20
    else:
        raise EnvioInvalido("Tipo de cliente inválido")

    if tipo_envio == "ESTANDAR":                     # D7
        pct_recargo = 0.00
    elif tipo_envio == "EXPRESS":                    # D8
        pct_recargo = 0.25
    else:
        raise EnvioInvalido("Tipo de envío inválido")

    descuento = subtotal * pct_descuento
    recargo = subtotal * pct_recargo
    total = round(subtotal - descuento + recargo, 2)
    return {
        "subtotal": round(subtotal, 2),
        "descuento": round(descuento, 2),
        "recargo": round(recargo, 2),
        "total": total,
    }
