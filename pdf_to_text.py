import fitz


def pdf_to_text(pdf_name):
    pdf = fitz.open(f'{pdf_name}.pdf')
    datas = []
    for current_page in range(0,len(pdf)):
        page = pdf.load_page(current_page)
        data = page.get_text()
        data = data.replace('\n','|')
        datas.append(data) 
    return datas