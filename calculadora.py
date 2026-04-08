from functools import reduce


def calcular_expressao(operacoes):
    """
    Avalia uma lista de operações encadeadas.
    Formato: [("=", valor_inicial), ("+", 5), ("*", 2), ...]
    """
    def aplicar_operacao(acumulador, operacao_item):
        operador, valor = operacao_item
        if operador == "+":
            return acumulador + valor
        elif operador == "-":
            return acumulador - valor
        elif operador == "*":
            return acumulador * valor
        elif operador == "/":
            if valor == 0:
                raise ValueError("Divisão por zero!")
            return acumulador / valor
        else:
            raise ValueError(f"Operador desconhecido: '{operador}'")

    if not operacoes:
        return 0

    # Se o primeiro operador for "=", define o valor inicial
    if operacoes[0][0] == "=":
        valor_inicial = operacoes[0][1]
        return reduce(aplicar_operacao, operacoes[1:], valor_inicial)
    else:
        # Sem "=", começa do zero e aplica tudo
        return reduce(aplicar_operacao, operacoes, 0)


print("\n--- Calculadora de Expressões ---")

exp1 = [("=", 10), ("+", 5), ("*", 2), ("-", 3)]
print(f"(10 + 5) * 2 - 3 = {calcular_expressao(exp1)}")   # 27

exp2 = [("=", 20), ("/", 4), ("+", 10)]
print(f"20 / 4 + 10    = {calcular_expressao(exp2)}")      # 15.0

exp3 = [("+", 5), ("-", 2)]
print(f"0 + 5 - 2      = {calcular_expressao(exp3)}")      # 3

try:
    exp_div = [("=", 10), ("/", 0)]
    calcular_expressao(exp_div)
except ValueError as e:
    print(f"Erro esperado: {e}")