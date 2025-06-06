import requests
from bs4 import BeautifulSoup
import os
import base64
import urllib.parse

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions
from docling.document_converter import PdfFormatOption, DocumentConverter
import os
from tqdm import tqdm

# 目標網頁 URL
url = 'https://health.gov.taipei/News.aspx?n=13A23138C06A3532&sms=8E7386D329C4B210&page=1&PageSize=50'

# 建立下載資料夾
download_dir = 'pdf_downloads'
os.makedirs(download_dir, exist_ok=True)

# 發送 GET 請求
headers = {
    'User-Agent': 'Mozilla/5.0'
}
response = requests.get(url, headers=headers)
response.raise_for_status()

# 解析 HTML 內容
soup = BeautifulSoup(response.text, 'html.parser')

# 找出所有包含 'Download.ashx' 的連結
pdf_links = soup.find_all('a', href=lambda href: href and 'Download.ashx' in href)

print(f'找到 {len(pdf_links)} 個 PDF 連結，開始下載...')

for idx, link in enumerate(pdf_links, start=1):
    href = link['href']
    full_url = urllib.parse.urljoin(url, href)
    parsed_url = urllib.parse.urlparse(full_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    n_param = query_params.get('n', [None])[0]

    if n_param:
        try:
            # 解碼檔名
            decoded_name = base64.b64decode(n_param).decode('utf-8')
            filename = urllib.parse.unquote(decoded_name)
        except Exception as e:
            print(f'檔名解碼失敗，使用預設檔名。錯誤：{e}')
            filename = f'file_{idx}.pdf'
    else:
        filename = f'file_{idx}.pdf'

    # 下載 PDF
    try:
        pdf_response = requests.get(full_url, headers=headers)
        pdf_response.raise_for_status()
        file_path = os.path.join(download_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(pdf_response.content)
        print(f'已下載：{filename}')
    except Exception as e:
        print(f'下載失敗：{filename}，錯誤：{e}')

print('所有 PDF 檔案下載完成。')



pipeline_options = PdfPipelineOptions(do_ocr = True, ocr_options = EasyOcrOptions(lang=["ch_tra","en"]), gpu=True)

pdfFormatOption = PdfFormatOption(pipeline_options=pipeline_options)
doc_converter = DocumentConverter(
    format_options={InputFormat.PDF: pdfFormatOption}
)

def docling_pdf_extraction(file_name: str):
    return doc_converter.convert(file_name).document.export_to_markdown()

raw_pdf_dir = "./pdf_downloads"
result_dir = "./md_result"
os.makedirs(result_dir, exist_ok=True)

pdf_files = [f for f in os.listdir(raw_pdf_dir) if f.lower().endswith(".pdf")]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    pdf_path = os.path.join(raw_pdf_dir, file_name)
    markdown_output = docling_pdf_extraction(pdf_path)
    md_file_name = os.path.splitext(file_name)[0] + ".md"
    md_path = os.path.join(result_dir, md_file_name)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_output)