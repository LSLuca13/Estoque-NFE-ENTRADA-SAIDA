import os
from controllers.estoque_controller import (
    listar_estoque,
    buscar_por_filtros,
    excluir_produto_por_codigo
)
from services.xml_service import importar_xml, importar_saida_xml
from services.export_service import exportar_estoque_excel

def menu():
    while True:
        print("\n== Sistema de Estoque ==")
        print("1. Ver estoque")
        print("2. Importar XML de Entrada")
        print("3. Importar XML de Saída")
        print("4. Buscar produtos com filtros")
        print("5. Excluir produto por código")
        print("6. Exportar estoque para Excel")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            produtos = listar_estoque()
            exibir_estoque(produtos)

        elif opcao == "2":
            nome_arquivo = input("Digite o nome do arquivo XML de entrada (dentro da pasta 'xmls/'): ")
            caminho = os.path.join("xmls", nome_arquivo)
            importar_xml(caminho)

        elif opcao == "3":
            nome_arquivo = input("Digite o nome do arquivo XML de saída (dentro da pasta 'xmls/'): ")
            caminho = os.path.join("xmls", nome_arquivo)
            importar_saida_xml(caminho)

        elif opcao == "4":
            aplicar_filtros()

        elif opcao == "5":
            codigo = input("Digite o código do produto que deseja excluir: ").strip()
            excluir_produto_por_codigo(codigo)
            print(f"Produto com código {codigo} excluído (se existia).")

        elif opcao == "6":
            produtos = listar_estoque()
            exportar_estoque_excel(produtos)

        elif opcao == "7":
            print("Encerrando o sistema.")
            break

        else:
            print("Opção inválida!")

def exibir_estoque(produtos):
    print("\nEstoque Atual:")
    if not produtos:
        print("Nenhum produto encontrado.")
        return
    for p in produtos:
        print(f"{p.nome} (Código {p.codigo}): {p.quantidade} unidades - "
              f"R$ {p.preco:.2f} | Fornecedor: {p.fornecedor} | Mínimo: {p.estoque_minimo}")

def aplicar_filtros():
    nome = input("Filtrar por nome (pressione Enter para ignorar): ").strip()
    fornecedor = input("Filtrar por fornecedor (pressione Enter para ignorar): ").strip()
    try:
        quantidade_max = input("Filtrar por quantidade até (pressione Enter para ignorar): ").strip()
        quantidade_max = int(quantidade_max) if quantidade_max else None
    except ValueError:
        print("Valor inválido para quantidade.")
        return

    filtrados = buscar_por_filtros(
        nome=nome if nome else None,
        quantidade_minima=quantidade_max,
        fornecedor=fornecedor if fornecedor else None
    )
    exibir_estoque(filtrados)

if __name__ == "__main__":
    menu()
