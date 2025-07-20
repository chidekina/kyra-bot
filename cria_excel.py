from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Planilha1"
ws.append(["Coluna1", "Coluna2", "Coluna3"])
ws.append(["A", 1, True])
ws.append(["B", 2, False])
ws.append(["C", 3, True])
wb.save("teste.xlsx")
