class Produto:
    def __init__(self, codigo, nome, quantidade, preco, fornecedor="", estoque_minimo=0):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.fornecedor = fornecedor
        self.estoque_minimo = estoque_minimo

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "quantidade": self.quantidade,
            "preco": self.preco,
            "fornecedor": self.fornecedor,
            "estoque_minimo": self.estoque_minimo
        }

    @staticmethod
    def from_dict(data):
        return Produto(
            codigo=data["codigo"],
            nome=data["nome"],
            quantidade=data["quantidade"],
            preco=data["preco"],
            fornecedor=data.get("fornecedor", ""),
            estoque_minimo=data.get("estoque_minimo", 0)
        )
