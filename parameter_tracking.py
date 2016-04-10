print("RUN")
import requests
import csv
import time

write = csv.writer(open('./parm_track.csv', 'w', newline=''))  # 요청결과 csv 파일 작성

url_list = 'http://www.hira.or.kr/rd/hosp/hospSrchListAjax.do'  # 요양기관 목록정보 Request URL
#url_info = 'http://www.hira.or.kr/rd/hosp/hospInfoAjax.do'      # 요양기관 추가정보 Request URL
url_grd = 'http://www.hira.or.kr/re/diag/diagEvlInfoAjax.do'    # 요양기관 평가정보 Request URL

payload = {'pageIndex': 1, 'sidCdNm': '서울', 'sidoCd': '110000'}

# 병원 규모별 검색 파라미터 값 리스트(0: clCdNm, 1:sno, 2: clCd, 고유값은 sno) 한편, 전문병원은 skip
sno_li = [['종합병원', 1061, 11], ['병원', 1121, 21],
        ['의원', 1148, 31] ]

for sno in sno_li:
    payload['sno'] = sno[1]
    payload['clCd'] = sno[2]
    result = requests.post(url=url_list, data=payload)  # 요청 실행
    x = result.json()['data']  # 요청결과(data) json 방식으로 type 변환
    print("*** 강서구 내 <", sno[0], "> 수 :", x['count'], ", pages : ", x['pages'])  # 검색결과 수
    for p in range(x['pages']):
        if p is 0 :
            for j in x['hospSrchList']:
                result_grd = requests.post(url=url_grd, data={'ykiho':j['ykiho']})
                #print(j['yadmNm'], ":", result_grd.headers.keys() )
                if 'content-length' in result_grd.headers.keys():
                    write.writerow([j['yadmNm'], j['clCdNm'], "NaN"])
                    print("not valid data-set :", j['yadmNm'])
                else :
                    y = result_grd.json()['data']['diagEvlVO']
                    write.writerow([j['yadmNm'], j['clCdNm'],
                                    y['BAgcGrd'], y['BEsophCaGrd'], y['BHccGrd'], y['BIntstGrd'], y['BLiverGrd'], y['BPancCaGrd'],
                                    y['BPciGrd'], y['BStemTransp'], y['BStomGrd'], y['BThrGrd'], y['agcGrd'], y['amiGrd'],
                                    y['anbioPrscGrd'], y['astGrd'], y['blddGrd'], y['breastGrd'], y['cabgGrd'], y['caesrGrd'],
                                    y['capGrd'], y['copGrd'], y['diagRstGrd'], y['dmGrd'], y['hytenGrd'], y['ijctPrscGrd'],
                                    y['intstGrd'], y['lcaGrd'], y['mdsAmtGrd'], y['mdsItemGrd'], y['omGrd'], y['prvtAnboGrd'],
                                    y['psydeptGrd'], y['recuhospGrd'], y['soprDiagGrd'], y['strokeGrd'],
                                    j['ykiho']
                                    ])

                    print(j['yadmNm'], "\카테고리 :", j['clCdNm'])
        else :
            payload['pageIndex'] += 1
            result0 = requests.post(url=url_list, data=payload)
            x0 = result0.json()['data']

            for j in x0['hospSrchList']:
                result_grd = requests.post(url=url_grd, data={'ykiho':j['ykiho']})
                header_info = result_grd.headers
                if 'content-length' in result_grd.headers.keys():
                    write.writerow([j['yadmNm'], j['clCdNm'], "NaN"])
                    print("not valid data-set :", j['yadmNm'])
                else :
                    y = result_grd.json()['data']['diagEvlVO']
                    write.writerow([j['yadmNm'], j['clCdNm'],
                                    y['BAgcGrd'], y['BEsophCaGrd'], y['BHccGrd'], y['BIntstGrd'], y['BLiverGrd'], y['BPancCaGrd'],
                                    y['BPciGrd'], y['BStemTransp'], y['BStomGrd'], y['BThrGrd'], y['agcGrd'], y['amiGrd'],
                                    y['anbioPrscGrd'], y['astGrd'], y['blddGrd'], y['breastGrd'], y['cabgGrd'], y['caesrGrd'],
                                    y['capGrd'], y['copGrd'], y['diagRstGrd'], y['dmGrd'], y['hytenGrd'], y['ijctPrscGrd'],
                                    y['intstGrd'], y['lcaGrd'], y['mdsAmtGrd'], y['mdsItemGrd'], y['omGrd'], y['prvtAnboGrd'],
                                    y['psydeptGrd'], y['recuhospGrd'], y['soprDiagGrd'], y['strokeGrd'],
                                    j['ykiho']
                                    ])

                    print(j['yadmNm'], "\카테고리 :", j['clCdNm'])
        time.sleep(1)
        print("========== 현재 ", p+1, "/", x['pages'], "수집 완료 ==========")
    payload['pageIndex'] = 1


'''
for i in sno_li:
    payload['sno'] = i[1]
    payload['clCd'] = i[2]
    result = requests.post(url=url, data=payload)  # 요청 실행
    x = result.json()['data']  # 요청결과(data) json 방식으로 type 변환

    for p in range(x['pages']):
        print("*** 강남구 내 <", i[0], "> 수 :", x['count'])  # 검색결과 수
        print("* 현재 수집중인 pageIndex :", payload['pageIndex'], "/", x['pages'])
        for j in x['hospSrchList']:
            result_grd = requests.post(url=url_grd, data={'ykiho':j['ykiho']})
            header_info = result_grd.headers
            print(j['yadmNm'], "(", k, (payload['pageIndex'])*20, ")")
            """
            if 'content-length' in header_info.keys() and header_info['content-length'] is '0':
                print("not valid data-set :", j['yadmNm'], "(", k, (payload['pageIndex'])*20, ")")
            else :
                y = result_grd.json()['data']['diagEvlVO']

                write.writerow([j['yadmNm'], j['clCdNm'],
                                y['BAgcGrd'], y['BEsophCaGrd'], y['BHccGrd'], y['BIntstGrd'], y['BLiverGrd'], y['BPancCaGrd'],
                                y['BPciGrd'], y['BStemTransp'], y['BStomGrd'], y['BThrGrd'], y['agcGrd'], y['amiGrd'],
                                y['anbioPrscGrd'], y['astGrd'], y['blddGrd'], y['breastGrd'], y['cabgGrd'], y['caesrGrd'],
                                y['capGrd'], y['copGrd'], y['diagRstGrd'], y['dmGrd'], y['hytenGrd'], y['ijctPrscGrd'],
                                y['intstGrd'], y['lcaGrd'], y['mdsAmtGrd'], y['mdsItemGrd'], y['omGrd'], y['prvtAnboGrd'],
                                y['psydeptGrd'], y['recuhospGrd'], y['soprDiagGrd'], y['strokeGrd'],
                                j['ykiho']
                                ])
            """
            time.sleep(1)
    print("==================== 강남구 내 <", i[0], "> 데이터 수집 완료 ==================== ")
    payload['pageIndex'] += 1



"""
yk = 'JDQ4MTg4MSM1MSMkMSMkMCMkOTkkMzgxMzUxIzIxIyQxIyQ5IyQ4MiQzNjEwMDIjNjEjJDEjJDgjJDgz'
yk0 = 'JDQ4MTg4MSM1MSMkMSMkMCMkOTkkMzgxMzUxIzMxIyQxIyQ3IyQwMyQyNjEyMjIjODEjJDEjJDYjJDgz'
result0 = requests.post(url=url_grd, data={'ykiho': yk})
print("type :", type(result0))
print("header :", result0.headers)
# <병원정보> 존재하지 않는 요양기관 예외처리
if 'content-length' in result0.headers.keys() and result0.headers['content-length'] is '0':
    print("null value")
else:
    r1 = result0.json()['data']['diagEvlVO']
    print(r1['yadmNm'])
"""'''

