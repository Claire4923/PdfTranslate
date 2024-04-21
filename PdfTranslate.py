import base64
import fitz
import os
import requests
import json
from utils.AuthV3Util import addAuthParams
from PIL import Image
from io import BytesIO


# 应用ID
APP_KEY = 'TODO'
# 应用密钥
APP_SECRET = 'TODO'

# pdf file path
pdf_name = "1"
PATH = './'+pdf_name+'.pdf'

# 待翻译pdf页码，从1开始
translate_all = True
pages_to_translate = []


def createRequest(path):
    '''
    note: 将下列变量替换为需要请求的参数
    取值参考文档: https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E5%9B%BE%E7%89%87%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E5%9B%BE%E7%89%87%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html
    '''
    lang_from = 'ko'
    lang_to = 'zh-CHS'
    render = '1'
    type = '1'

    q = readFileAsBase64(path)
    data = {'q': q, 'from': lang_from, 'to': lang_to, 'render': render, 'type': type}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/ocrtransapi', header, data, 'post')
    print(str(res.content, 'utf-8'))
    file = open(path,'wb')
    file.write(base64.b64decode(json.loads(res.content)["render_image"]))
    file.close()
    # image = Image.open(BytesIO(base64.b64decode(json.loads(res.content)["render_image"])))
    # image.show()

def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)


def readFileAsBase64(path):
    f = open(path, 'rb')
    data = f.read()
    return str(base64.b64encode(data), 'utf-8')

def pdf2png2trans():
    pdf = fitz.open(PATH)
    for pg in range(pdf.page_count):
        page = pdf[pg]
        trans = fitz.Matrix(1,1)
        pm = page.get_pixmap(matrix=trans,alpha=False)
        image_path = "./images/"+pdf_name+"__"+str(pg)+".png"
        pm.save(image_path)
        if translate_all or (pg+1) in pages_to_translate:
            createRequest(image_path)
    pdf.close()

def save2pdf():
    image_folder_path = "./images/"
    pdf_file_path = "./"+pdf_name+"_translated.pdf"
    files = os.listdir(image_folder_path)
    pngs = []
    sources = []
    for file in files:
        if 'png' in file and pdf_name in file:
            pngs.append(image_folder_path + file)
    pngs.sort()
    output = Image.open(pngs[0])
    pngs.pop(0)
    for file in pngs:
        png = Image.open(file)
        if png.mode == "RGB":
            png = png.convert("RGB")
        sources.append(png)
    output.save(pdf_file_path,"pdf",save_all=True,append_images=sources)

if __name__ == '__main__':
    pdf2png2trans()
    save2pdf()