import os
from openpyxl import Workbook

def exportar_estoque_excel(produtos, caminho="relatorios/estoque.xlsx"):
    if not produtos:
        print("Não há produtos no estoque para exportar.")
        return

    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Estoque Atual"

    # Cabeçalhos
    cabecalhos = ["Código", "Nome", "Quantidade", "Preço (R$)", "Fornecedor", "Estoque Mínimo"]
    ws.append(cabecalhos)

    for p in produtos:
        ws.append([
            p.codigo,
            p.nome,
            p.quantidade,
            f"{p.preco:.2f}",
            p.fornecedor,
            p.estoque_minimo
        ])

    # Ajusta largura das colunas automaticamente (simples)
    for coluna in ws.columns:
        max_length = max(len(str(cell.value)) for cell in coluna)
        ws.column_dimensions[coluna[0].column_letter].width = max_length + 2

    wb.save(caminho)
    print(f"Relatório gerado com sucesso em: {caminho}")
