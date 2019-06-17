from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import requests
from bs4 import BeautifulSoup

from app.model.url import *

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/productsearch')
def search():
    return render_template('productsearch.html')

@app.route('/result')
def result():
    productName = request.args.get('productName')
    pageNm = request.args.get('pageNm')

    url = Domain()
    url.set_url('http://apis.data.go.kr/B553748/CertImgListService/getCertImgListService')
    url.set_url("?" + "serviceKey=" + "ifUIh0awMCGRjaEZCc7esYmH4zXa1C3F3M8QkUGHr%2Fcf62HQZoIP79sdSsiibcBEx4VCZPIUEt1UHQbRm%2BsPKg%3D%3D")
    url.set_url("&prdlstNm=" + productName)
    url.set_url("&pageNo=" + pageNm)
    url.set_url("&numOfRows=20")


    result = requests.get(url.join_url())
    if result.status_code == 200:
        res_xml = result.text
        soup = BeautifulSoup(res_xml, features="xml")

    temp = []
    allergy = []

    totalCount = int(soup.totalCount.contents[0])
    if totalCount == 0:
        rows = 0
    elif int(soup('rnum')[-1].contents[0]) > 20:
        rows = int(soup('rnum')[-1].contents[0]) % 20
        if rows == 0:
            rows = 20
    else:
        rows = int(soup('rnum')[-1].contents[0])
    for i in range(rows):
        temp.append([soup.find_all('rnum')[i].contents[0],
                     soup.find_all('imgurl1')[i].contents[0],
                     soup.find_all('prdlstNm')[i].contents[0],
                     soup.find_all('allergy')[i].contents[0],
                     soup.find_all('rawmtrl')[i].contents[0]])
        allergy.append(temp[i][3].rsplit('함유', 1)[0].split(","))

    return render_template('result.html', temp=temp, rows=rows, pageCount=int(totalCount/20)+1, urlp=url, productName=productName, pageNm=int(pageNm), allergy=allergy)


if __name__ == '__main__':
    app.run()