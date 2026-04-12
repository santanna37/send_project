





caminho = "/home/santanna/develope/projetos/send_project/ADP SIMPLES.pdf"
# def ler_pdf_pypdf2(caminho):
#     texto_total = ""
    
#     with open(caminho, 'rb') as arquivo:
#         print("inicio projeto")
#         leitor = PyPDF2.PdfReader(arquivo)
        
#         print(f"Número de páginas: {len(leitor.pages)}")
        
#         print("começo do loop")
#         for num_pagina, pagina in enumerate(leitor.pages):
#             print("detro do loop")
#             texto_pagina = pagina.extract_text()
#             print("texto pagina")
#             if texto_pagina:  # Verifica se há texto
#                 texto_total += f"--- Página {num_pagina + 1} ---\n{texto_pagina}\n\n"
    
#     return texto_total

# import pdfplumber

# def ler_pdf_com_tabelas(caminho_arquivo):
#     with pdfplumber.open(caminho_arquivo) as pdf:
#         for i, pagina in enumerate(pdf.pages):
#             # Extrai texto simples
#             texto = pagina.extract_text()
            
#             # Extrai tabelas (se houver)
#             tabelas = pagina.extract_tables()
            
#             print(f"Página {i + 1}:")
#             print(f"Texto: {texto[:200]}...")
            
#             if tabelas:
#                 print(f"Tabelas encontradas: {len(tabelas)}")
            
#             print("-" * 50)

# from pypdf import PdfReader  # pip install pypdf

# def ler_pdf(caminho):
#     texto_total = ""
    
#     with open(caminho, 'rb') as arquivo:
#         leitor = PdfReader(arquivo)
        
#         print(f"Número de páginas: {len(leitor.pages)}")
        
#         for num_pagina, pagina in enumerate(leitor.pages):
#             texto_pagina = pagina.extract_text()
#             if texto_pagina:
#                 texto_total += f"--- Página {num_pagina + 1} ---\n{texto_pagina}\n\n"
#         print(texto_total)
    
#     return texto_total
#ler_pdf(caminho=caminho)

import fitz  # pip install pymupdf
import re

def extrair_campos_darf(caminho_pdf):
    """
    Extrai apenas os campos essenciais do DARF
    """
    with fitz.open(caminho_pdf) as pdf:
        texto = pdf[0].get_text()
        print(texto)
    
    # Regex para capturar os dados específicos do DARF
    campos = {
        'cnpj': re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', texto),
        'razao_social': re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\s+([A-Z\s\.]+?)(?:Período|CNPJ|$)', texto, re.IGNORECASE),
        'periodo': re.search(r'Período.*?Apuração\s*([A-Za-z0-9/]+)', texto, re.IGNORECASE),
        'vencimento': re.search(r'Vencimento\s*([0-9]{2}/[0-9]{2}/[0-9]{4})', texto),
        'numero_documento': re.search(r'Número do Documento\s*([0-9\.\-]+)', texto),
        'valor_total': re.search(r'Valor Total do Documento\s*([0-9,\.]+)', texto),
        'codigo_receita': re.search(r'(\d{4})\s+CP\s+DESCONTADA', texto),
    }
    
    # Processar resultados
    resultado = {}
    for chave, match in campos.items():
        resultado[chave] = match.group(1).strip() if match else None
    
    # Limpar razão social (remove múltiplos espaços)
    if resultado.get('razao_social'):
        resultado['razao_social'] = re.sub(r'\s+', ' ', resultado['razao_social'])
    
    return resultado

# # Uso


# Uso
texto = extrair_campos_darf(caminho)
print(texto)


