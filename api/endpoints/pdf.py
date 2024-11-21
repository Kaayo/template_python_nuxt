from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from dto.author_dto import AuthorDTO
from security.auth import create_access_token, decode_access_token
from models_db.author import Author
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image

pdf_router = APIRouter()

@pdf_router.get("/generate-pdf")
async def generate_pdf():
    # Criar um buffer em memória para o PDF
    buffer = BytesIO()

    # Criar o PDF com ReportLab
    c = canvas.Canvas(buffer, pagesize=letter)  # 'letter' tem tamanho A4 em ReportLab (8.5 x 11 polegadas)
    
    # Adicionar conteúdo ao PDF
    c.drawString(100, 750, "Este é um exemplo de PDF gerado com FastAPI!")
    c.drawString(100, 735, "Ele está no formato A4 (tamanho carta no ReportLab).")
    
    # Salvar o PDF no buffer
    c.save()
    
    # Posicionar o buffer no início para leitura
    buffer.seek(0)

    # Retornar o PDF como resposta para o usuário
    return StreamingResponse(buffer, media_type="pdf_routerlication/pdf", headers={"Content-Disposition": "inline; filename=exemplo.pdf"})

@pdf_router.get("/generate-pdf2/")
def gerar_pdf():
    # Buffer para gerar o PDF em memória
    buffer = BytesIO()

    # Criar o documento PDF com margens pequenas para começar no topo
    documento = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0, bottomMargin=0, leftMargin=0, rightMargin=0)

    # Estilização das tabelas
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2aaddf")),  # Fundo do cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Cor do texto do cabeçalho
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Cabeçalho em negrito
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Borda da tabela
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),  # Linhas internas
    ])

    # Título do relatório
    titulo = [["RELATÓRIO ATENDIMENTO"]]

    # Adicionar imagem ao lado do título
    imagem = Image('logo.jpg', width=40, height=40)  # Usando "logo.jpg" como o caminho da imagem
    tabela_titulo = Table([[imagem, "RELATÓRIO ATENDIMENTO"]], colWidths=[50, 450])  # Definir largura para imagem e título
    tabela_titulo.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Alinhar imagem à esquerda
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # Centralizar apenas o título
    ]))

    # Dados principais
    dados_principais = [
        ["Código da Contratação:", "xx", "Contrato", "xx", "Quantidade contratada", "xx"],
        ["Data início relatório", "05/11/2024", "Data fim do relatório", "20/11/2024", "", ""],
    ]

    # Dados da empresa prestadora de serviço
    dados_empresa = [
        ["Razão Social / CNPJ", "Fulano silva ltda", "15.154.155/0001-89"],
        ["Responsável técnico / CPF", "zeca da silva", "139.555.489-40"],
        ["Celular", "(47) 98868-4139", "E-mail", "email@gmail.com"],
    ]

    # Clientes atendidos
    clientes_atendidos = [
        ["Nº", "CNPJ", "Razão Social", "Porte", "Data", "Brasil +", "APP cliente"],
        ["1", "20.432.455/0001-03", "RAFAEL EMPRESA LTDA", "ME", "05/11/2024", "NÃO", "SIM"],
        ["2", "48.563.115/0001-09", "JOSEFINA JOBS LTDA", "ME", "05/11/2024", "NÃO", "SIM"],
    ]

    # Execução do trabalho
    execucao_trabalho = [
        ["Diagnósticos aplicados", "2", "Diagnósticos a realizar", "0", "Assinatura", "\\"]
    ]

    # Criar tabelas
    tabela_dados_principais = Table(dados_principais, colWidths=[100, 80, 100, 80, 100, 80])
    tabela_dados_empresa = Table(dados_empresa, colWidths=[150, 200, 150])
    tabela_clientes = Table(clientes_atendidos, colWidths=[30, 120, 150, 50, 50, 50, 50])
    tabela_execucao = Table(execucao_trabalho, colWidths=[150, 50, 150, 50, 100, 100])

    # Aplicar estilos às tabelas
    tabela_dados_principais.setStyle(style)
    tabela_dados_empresa.setStyle(style)
    tabela_clientes.setStyle(style)
    tabela_execucao.setStyle(style)

    # Montar o layout final
    elementos = []
    elementos.append(tabela_titulo)  # Adiciona a tabela com imagem e título
    elementos.append(tabela_dados_principais)
    elementos.append(tabela_dados_empresa)
    elementos.append(tabela_clientes)
    elementos.append(tabela_execucao)

    # Construir o PDF no buffer
    documento.build(elementos)

    # Resetar o buffer para o início
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="pdf_routerlication/pdf", headers={"Content-Disposition": "inline; filename=exemplo.pdf"})

@pdf_router.get("/generate-pdf3/")
async def gerar_pdf():
    # Buffer para gerar o PDF em memória
    buffer = BytesIO()

    # Criar o documento PDF com margens pequenas para começar no topo
    documento = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0, bottomMargin=0, leftMargin=0, rightMargin=0)

    # Estilização das tabelas
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2aaddf")),  # Fundo do cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Cor do texto do cabeçalho
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Cabeçalho em negrito
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Borda da tabela
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),  # Linhas internas
    ])

    # Título do relatório
    titulo = [["RELATÓRIO ATENDIMENTO"]]

    # Adicionar imagem ao lado do título
    imagem = Image('logo.jpg', width=40, height=40)  # Usando "logo.jpg" como o caminho da imagem
    tabela_titulo = Table([[imagem, "RELATÓRIO ATENDIMENTO"]], colWidths=[50, 450])  # Definir largura para imagem e título
    tabela_titulo.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Alinhar imagem à esquerda
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # Centralizar apenas o título
    ]))

    # Dados principais
    dados_principais = [
        ["Código da Contratação:", "xx", "Contrato", "xx", "Quantidade contratada", "xx"],
        ["Data início relatório", "05/11/2024", "Data fim do relatório", "20/11/2024", "", ""],
    ]

    # Dados da empresa prestadora de serviço
    dados_empresa = [
        ["Razão Social / CNPJ", "Fulano silva ltda", "15.154.155/0001-89"],
        ["Responsável técnico / CPF", "zeca da silva", "139.555.489-40"],
        ["Celular", "(47) 98868-4139", "E-mail", "email@gmail.com"],
    ]

    # Clientes atendidos
    clientes_atendidos = [
        ["Nº", "CNPJ", "Razão Social", "Porte", "Data", "Brasil +", "APP cliente"],
        ["1", "20.432.455/0001-03", "RAFAEL EMPRESA LTDA", "ME", "05/11/2024", "NÃO", "SIM"],
        ["2", "48.563.115/0001-09", "JOSEFINA JOBS LTDA", "ME", "05/11/2024", "NÃO", "SIM"],
    ]

    # Execução do trabalho
    execucao_trabalho = [
        ["Diagnósticos aplicados", "2", "Diagnósticos a realizar", "0", "Assinatura", "\\"]
    ]

    # Criar tabelas
    tabela_dados_principais = Table(dados_principais, colWidths=[100, 80, 100, 80, 100, 80])
    tabela_dados_empresa = Table(dados_empresa, colWidths=[150, 200, 150])
    tabela_clientes = Table(clientes_atendidos, colWidths=[30, 120, 150, 50, 50, 50, 50])
    tabela_execucao = Table(execucao_trabalho, colWidths=[150, 50, 150, 50, 100, 100])

    # Aplicar estilos às tabelas
    tabela_dados_principais.setStyle(style)
    tabela_dados_empresa.setStyle(style)
    tabela_clientes.setStyle(style)
    tabela_execucao.setStyle(style)

    # Montar o layout final
    elementos = []
    elementos.append(tabela_titulo)  # Adiciona a tabela com imagem e título
    elementos.append(tabela_dados_principais)
    elementos.append(tabela_dados_empresa)
    elementos.append(tabela_clientes)
    elementos.append(tabela_execucao)

    # Construir o PDF no buffer
    documento.build(elementos)

    # Resetar o buffer para o início
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="pdf_routerlication/pdf", headers={"Content-Disposition": "inline; filename=exemplo.pdf"})

@pdf_router.get("/pdf")
async def pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4  # A4 size in points (595.27 x 841.89 points)

    # Inserindo a imagem
    image_path = "logo.jpg"
    c.drawImage(image_path, 30, height - 100, width=100, height=50)

    # Título centralizado
    c.setFont("Helvetica-Bold", 16)
    title = "Relatório de Atendimentos"
    title_width = c.stringWidth(title, "Helvetica-Bold", 16)
    c.drawString((width - title_width) / 2, height - 60, title)

    # Criando a tabela com 3 colunas e 10 linhas
    data = [['Coluna 1', 'Coluna 2', 'Coluna 3']]  # Cabeçalho da tabela
    for i in range(1, 11):  # 10 linhas de conteúdo
        data.append([f'Data {i}A', f'Data {i}B', f'Data {i}C'])

    # Definindo as dimensões da tabela
    table_width = width - 60
    col_width = table_width / 3  # Dividindo a largura para 3 colunas
    row_height = 20  # Altura de cada linha

    # Desenhando a tabela
    y_position = height - 150  # Posição inicial para a tabela
    c.setFont("Helvetica", 10)

    for row in data:
        x_position = 30
        for col in row:
            c.drawString(x_position + 5, y_position, col)
            x_position += col_width
        y_position -= row_height

    c.save()

    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=relatorio_atendimentos.pdf"})
