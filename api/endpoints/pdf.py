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

pdf_router = APIRouter(
    prefix="/pdf",     # Prefixo para todas as rotas aqui
    tags=["PDF"],     
)

@pdf_router.get("/generate-pdf")
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

    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=exemplo.pdf"})


