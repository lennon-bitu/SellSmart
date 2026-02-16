import csv
from django.http import HttpResponse
from django.shortcuts import render
import openpyxl
from reportlab.lib.pagesizes import letter
from django.db.models import Sum
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from .models import Product


def export_products_pdf(request):
    from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from django.http import HttpResponse
from .models import Product

def export_products_pdf(request):
    # Define the response as a PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="products_report.pdf"'

    # Create the PDF document with margins
    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=36, leftMargin=72, topMargin=36, bottomMargin=36)
    
    # Define styles for the PDF
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    
    # Title and Header
    title = Paragraph("Relatório de Produto", title_style)
    headers = ["ID", "Nome", "Código", "Preço", "Custo", "Categoria", " "]
    
    # Define column widths: ID and Code are narrower, Name is wider
    col_widths = [40, 300, 40, 60, 60, 80,20]  # Adjusted widths for each column
    
    # Create a table with the header
    data = [headers]
    
    # Fetch all products from the database
    products = Product.objects.all()
    for product in products:
        data.append([product.id, product.name, product.code, f"R${product.price}", f"R${product.cost_price}",product.category ])
    
    # Create and style the table
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#bfbfbf'),  # Light gray header background
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),   # Black text color for the header
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),       # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),     # Padding for header
        ('BACKGROUND', (0, 1), (-1, -1), '#f2f2f2'),  # Light gray background for data rows
        ('GRID', (0, 0), (-1, -1), 1, '#d3d3d3'),   # Light gray grid lines
        ('BOX', (0, 0), (-1, -1), 1, '#d3d3d3')    # Border around the entire table
    ]))

    # Build the PDF
    content = [title, table]
    doc.build(content)

    return response


def export_products_csv(request):
    # Define a resposta como um arquivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produtos.csv"'

    # Cria um escritor CSV
    writer = csv.writer(response)
    
    # Escreve o cabeçalho (nomes das colunas)
    writer.writerow(['ID', 'Nome', 'Codigo', 'Preco','Preco de Custo'])

    # Busca todos os produtos no banco de dados
    products = Product.objects.all()

    # Escreve os dados de cada produto
    for product in products:
        writer.writerow([product.id, product.name, product.code, product.price, product.cost_price])

    # Retorna a resposta contendo o CSV
    return response


def export_product_excel(request):
    # Cria o arquivo Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Produtos"

    # Escreve o cabeçalho
    ws.append(['ID', 'Nome', 'Código', 'Preço', 'Custo'])

    # Busca os produtos e insere no Excel
    products = Product.objects.all()
    for product in products:
        ws.append([product.id, product.name, product.code, product.price, product.cost_price])
    
    #o comando a baixo calcula o total dos valores de preço do produto e custo de produto
    #total_price = products.aggregate(total=Sum('price'))['total']
    #total_cost = products.aggregate(total=Sum('cost_price'))['total']

    # Define a resposta HTTP com o arquivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=produtos.xlsx'

    # Salva o arquivo Excel na resposta
    wb.save(response)

    return response


def product_print(request):
    # Busca os produtos
    products = Product.objects.all()

    # Renderiza o template com estilo para impressão
    return render(request, 'product/product_print.html', {'products': products})
