import os
import xml.etree.ElementTree as ET
import hashlib
import json
from models.produto import Produto
from controllers.estoque_controller import atualizar_estoque

HISTORICO_PATH = "storage/historico_importacoes.json"

def carregar_historico():
    if not os.path.exists(HISTORICO_PATH):
        return []
    with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_historico(lista_hashes):
    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        json.dump(lista_hashes, f, indent=4)

def gerar_hash_arquivo(caminho):
    with open(caminho, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def importar_xml(caminho):
    if not os.path.exists(caminho):
        print("Arquivo não encontrado.")
        return

    hash_arquivo = gerar_hash_arquivo(caminho)
    historico = carregar_historico()

    if hash_arquivo in historico:
        print("Este XML já foi importado anteriormente. Ignorado.")
        return

    tree = ET.parse(caminho)
    root = tree.getroot()
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    fornecedor = root.find(".//nfe:emit/nfe:xNome", ns)
    fornecedor_nome = fornecedor.text if fornecedor is not None else "Desconhecido"

    for det in root.findall(".//nfe:det", ns):
        prod = det.find("nfe:prod", ns)
        if prod is None:
            continue

        codigo = prod.find("nfe:cProd", ns).text
        nome = prod.find("nfe:xProd", ns).text
        quantidade = float(prod.find("nfe:qCom", ns).text)
        preco = float(prod.find("nfe:vUnCom", ns).text)

        produto = Produto(
            codigo=codigo,
            nome=nome,
            quantidade=int(quantidade),
            preco=preco,
            fornecedor=fornecedor_nome,
            estoque_minimo=0
        )

        atualizar_estoque(produto, tipo="entrada")

    historico.append(hash_arquivo)
    salvar_historico(historico)
    print("Importação concluída com sucesso.")


def importar_saida_xml(caminho):
    """Importa um XML de saída e subtrai as quantidades do estoque."""
    if not os.path.exists(caminho):
        print("Arquivo não encontrado.")
        return

    hash_arquivo = gerar_hash_arquivo(caminho)
    historico = carregar_historico()

    if hash_arquivo in historico:
        print("Este XML já foi importado anteriormente. Ignorado.")
        return

    tree = ET.parse(caminho)
    root = tree.getroot()
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    cliente = root.find(".//nfe:dest/nfe:xNome", ns)
    cliente_nome = cliente.text if cliente is not None else "Desconhecido"

    for det in root.findall(".//nfe:det", ns):
        prod = det.find("nfe:prod", ns)
        if prod is None:
            continue

        codigo = prod.find("nfe:cProd", ns).text
        nome = prod.find("nfe:xProd", ns).text
        quantidade = float(prod.find("nfe:qCom", ns).text)
        preco = float(prod.find("nfe:vUnCom", ns).text)

        produto = Produto(
            codigo=codigo,
            nome=nome,
            quantidade=int(quantidade),
            preco=preco,
            fornecedor=cliente_nome,
            estoque_minimo=0,
        )

        atualizar_estoque(produto, tipo="saida")

    historico.append(hash_arquivo)
    salvar_historico(historico)
    print("Importação concluída com sucesso.")
