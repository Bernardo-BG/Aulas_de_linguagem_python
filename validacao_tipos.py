def criar_gerador_id(start_id=1):
    current_id = start_id

    def proximo_id():
        nonlocal current_id  # Permite modificar a variável do escopo externo
        id_gerado = current_id
        current_id += 1
        return id_gerado

    return proximo_id


# Criar dois geradores de IDs completamente independentes
gerador_usuarios = criar_gerador_id(100)
gerador_produtos = criar_gerador_id(1)

print("\n--- Gerador de IDs de Usuários ---")
print(f"ID Usuário: {gerador_usuarios()}")   # 100
print(f"ID Usuário: {gerador_usuarios()}")   # 101

print("\n--- Gerador de IDs de Produtos ---")
print(f"ID Produto: {gerador_produtos()}")   # 1
print(f"ID Produto: {gerador_produtos()}")   # 2

print("\n--- Continuação Independente ---")
print(f"ID Usuário: {gerador_usuarios()}")   # 102 (não foi afetado pelos produtos)
print(f"ID Produto: {gerador_produtos()}")   # 3