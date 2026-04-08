import re

log_data = """ 
2023-10-26 10:00:01 INFO Usuário 'admin' logado com sucesso. 
2023-10-26 10:00:05 WARNING Tentativa de login falhou para 'guest'. 
2023-10-26 10:00:10 ERROR Erro crítico: Falha na conexão com o banco de dados. 
2023-10-26 10:00:15 INFO Processo de backup iniciado. 
2023-10-26 10:00:20 ERROR Erro de E/S: Disco cheio. 
"""


def analisar_log(log_content):
    # Regex para capturar data, hora, nível e mensagem
    log_pattern = re.compile(
        r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR) (.*)$",
        re.MULTILINE
    )

    registros = []
    erros_count = 0

    for match in log_pattern.finditer(log_content):
        data, hora, nivel, mensagem = match.groups()
        registros.append({
            "data": data,
            "hora": hora,
            "nivel": nivel,
            "mensagem": mensagem
        })
        if nivel == "ERROR":
            erros_count += 1

    return registros, erros_count


print("\n--- Análise de Log com Regex ---")
registros, erros = analisar_log(log_data)
print("Registros de Log:")
for reg in registros:
    print(f"  Data: {reg['data']}, Hora: {reg['hora']}, Nível: {reg['nivel']}, Mensagem: {reg['mensagem']}")
print(f"Total de erros encontrados: {erros}")