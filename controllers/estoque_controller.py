import json
import os
from models.produto import Produto

ESTOQUE_PATH = "storage/estoque.json"

def carregar_estoque():
    if not os.path.exists(ESTOQUE_PATH):
        return []
    with open(ESTOQUE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Produto.from_dict(p) for p in data]

def salvar_estoque(produtos):
    with open(ESTOQUE_PATH, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in produtos], f, indent=4)

def atualizar_estoque(produto_novo, tipo="entrada"):
    estoque = carregar_estoque()
    atualizado = False
    for produto in estoque:
        if produto.codigo == produto_novo.codigo:
            if tipo == "entrada":
                produto.quantidade += produto_novo.quantidade
                produto.fornecedor = produto_novo.fornecedor
                produto.preco = produto_novo.preco
            elif tipo == "saida":
                produto.quantidade -= produto_novo.quantidade
            atualizado = True
            break
    if not atualizado and tipo == "entrada":
        estoque.append(produto_novo)
    salvar_estoque(estoque)

def listar_estoque():
    return carregar_estoque()

def excluir_produto_por_codigo(codigo):
    estoque = carregar_estoque()
    estoque = [p for p in estoque if p.codigo != codigo]
    salvar_estoque(estoque)

def buscar_por_filtros(nome=None, quantidade_minima=None, fornecedor=None):
    produtos = carregar_estoque()
    filtrados = produtos
    if nome:
        filtrados = [p for p in filtrados if nome.lower() in p.nome.lower()]
    if quantidade_minima is not None:
        filtrados = [p for p in filtrados if p.quantidade <= quantidade_minima]
    if fornecedor:
        filtrados = [p for p in filtrados if fornecedor.lower() in p.fornecedor.lower()]
    return filtrados
