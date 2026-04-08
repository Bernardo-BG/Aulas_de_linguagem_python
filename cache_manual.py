import csv
import os


def ler_dados_csv_gerador(caminho_arquivo, coluna_numerica_idx):
    """Gerador que lê um CSV linha a linha e extrai um valor numérico."""
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Pular o cabeçalho
        for linha in reader:
            try:
                yield float(linha[coluna_numerica_idx])
            except (ValueError, IndexError):
                # Ignora linhas com dados inválidos ou colunas ausentes
                continue


def calcular_media_gerador(caminho_arquivo, coluna_idx):
    total = 0
    contagem = 0
    for valor in ler_dados_csv_gerador(caminho_arquivo, coluna_idx):
        total += valor
        contagem += 1
    return total / contagem if contagem > 0 else 0


# Criar um ficheiro CSV de exemplo grande (100.000 linhas)
with open('dados_grandes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Valor', 'Descrição'])
    for i in range(100_000):
        writer.writerow([i, i * 1.5 + 0.5, f'Item {i}'])

# Calcular a média da coluna 'Valor'
caminho = 'dados_grandes.csv'
coluna  = 1

print(f"Calculando média da coluna {coluna}...")
media = calcular_media_gerador(caminho, coluna)
print(f"Média calculada: {media:.2f}")

# Limpar o ficheiro temporário
os.remove('dados_grandes.csv')
print("Ficheiro removido com sucesso.")