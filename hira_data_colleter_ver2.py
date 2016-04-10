# HIRA(심평원) 데이터 크롤링

print("RUN")
import requests
import csv
import time

#write = csv.writer(open('./hira_hosp_list.csv','w',newline=''))     # 요양기관 기본정보 csv파일
#write0 = csv.writer(open('./hira_hosp_grd.csv', 'w', newline='')) # 요양기관 등급정보 csv파일

# 병원 규모별 검색 파라미터 값 리스트(0: clCdNm, 1:sno, 2: clCd, 고유값은 sno) 한편, 전문병원은 skip
#sno_li = [['종합병원', 1061,11], ['병원', 1121,21]]
sno_li = [['의원', 1148,31]]

'''
write.writerow(["병원 이름", "병원구분", "설립구분", "주소(광역단위)", "주소(행정단위)", "주소(세부주소)", "전화번호", "URL",
                "의사수(총인원)", "의사수(전문의)",
                "일반입원실(상급)", "일반입원실(일반)", "중환자실(성인소아)", "중환자실(신생아)", "분만실", "수술실", "응급실", "물리치료실"
                ])
write0.writerow(['hosp_name', 'hosp_type',
                'BAgcGrd','BEsophCaGrd','BHccGrd','BIntstGrd','BLiverGrd','BPancCaGrd','BPciGrd','BStemTransp',
                 'BStomGrd','BThrGrd','agcGrd','amiGrd','anbioPrscGrd','astGrd','blddGrd','breastGrd','cabgGrd',
                 'caesrGrd','capGrd','copGrd','diagRstGrd','dmGrd','hytenGrd','ijctPrscGrd','intstGrd','lcaGrd',
                 'mdsAmtGrd','mdsItemGrd','omGrd','prvtAnboGrd','psydeptGrd','recuhospGrd','soprDiagGrd','strokeGrd'
                 'ykiho'])
write0.writerow(['병원이름', '병원구분','위암','식도암수술','간암','Unknown','간암수술','췌장암수술','Unknown','조혈모세포이식술','위암수술','고관절치환술',
                 '위암(결과)','급성심근경색증','항생제처방률','천식','혈액투석','유방암','관상동맥우회술','제왕절개분만','폐렴','만성폐쇄성폐질환',
                 'Unknown','당뇨병','고혈압','주사제처방률','대장암','폐암','처방약품비','약품목수','유소아중이염항생제','수술의예방적항생제',
                 '의료급여정신과','Unknown','Unknown','급성기뇌졸중','검색KEY값'])
'''
url_list = 'http://www.hira.or.kr/rd/hosp/hospSrchListAjax.do'  # 요양기관 목록정보 Request URL
url_info = 'http://www.hira.or.kr/rd/hosp/hospInfoAjax.do'      # 요양기관 추가정보 Request URL
url_grd = 'http://www.hira.or.kr/re/diag/diagEvlInfoAjax.do'    # 요양기관 평가정보 Request URL

payload = {'pageIndex': 1, 'sidCdNm': '서울', 'sidoCd': '110000'}


for sno in sno_li:
    payload['sno'] = sno[1]
    payload['clCd'] = sno[2]
    result = requests.post(url=url_list, data=payload)  # 요청 실행
    x = result.json()['data']  # 요청결과(data) json 방식으로 type 변환
    print("*** 서울시 내 <", sno[0], "> 수 :", x['count'], ", pages : ", x['pages'])  # 검색결과 수
    for p in range(x['pages']):
        if p is 0 :
            for j in x['hospSrchList']:
                result_info = requests.post(url=url_info, data={'ykiho':j['ykiho']})
                y = result_info.json()['data']
                y0 = y['hospInfo']
                addr = (j['addr'].split(' ',2))
                '''
                write.writerow([j['yadmNm'], j['clCdNm'], y0['orgTyCdNm'], addr[0], addr[1], addr[2], j['telNo'], j['hospUrl'],
                                y['gnlNopCnt']['gnlNopCnt0'], y['gnlNopCnt']['gnlNopCnt4'],
                                y0['hghrSickbdCnt'], y0['stdSickbdCnt'], y0['aduChldSprmCnt'], y0['nbySprmCnt'],
                                y0['partumCnt'], y0['soprmCnt'], y0['emymCnt'], y0['ptrmCnt']
                                ])
                '''
                print(j['yadmNm'], "    기본정보 수집중...")

                result_grd = requests.post(url=url_grd, data={'ykiho':j['ykiho']})
                if 'content-length' in result_grd.headers.keys():
                    write0.writerow([j['yadmNm'], j['clCdNm'], "null"])
                    print("not valid grade data")
                else :
                    z = result_grd.json()['data']['diagEvlVO']
                    '''
                    write0.writerow([j['yadmNm'], j['clCdNm'],
                                    z['BAgcGrd'], z['BEsophCaGrd'], z['BHccGrd'], z['BIntstGrd'], z['BLiverGrd'], z['BPancCaGrd'],
                                    z['BPciGrd'], z['BStemTransp'], z['BStomGrd'], z['BThrGrd'], z['agcGrd'], z['amiGrd'],
                                    z['anbioPrscGrd'], z['astGrd'], z['blddGrd'], z['breastGrd'], z['cabgGrd'], z['caesrGrd'],
                                    z['capGrd'], z['copGrd'], z['diagRstGrd'], z['dmGrd'], z['hytenGrd'], z['ijctPrscGrd'],
                                    z['intstGrd'], z['lcaGrd'], z['mdsAmtGrd'], z['mdsItemGrd'], z['omGrd'], z['prvtAnboGrd'],
                                    z['psydeptGrd'], z['recuhospGrd'], z['soprDiagGrd'], z['strokeGrd'],
                                    j['ykiho']
                                    ])
                    '''
                time.sleep(1)
        else :
            payload['pageIndex'] += 1
            result0 = requests.post(url=url_list, data=payload)
            x0 = result0.json()['data']
            for j in x0['hospSrchList']:
                result_info = requests.post(url=url_info, data={'ykiho':j['ykiho']})
                y = result_info.json()['data']
                y0 = y['hospInfo']
                addr = (j['addr'].split(' ',2))
                '''
                write.writerow([j['yadmNm'], j['clCdNm'], y0['orgTyCdNm'], addr[0], addr[1], addr[2], j['telNo'], j['hospUrl'],
                                y['gnlNopCnt']['gnlNopCnt0'], y['gnlNopCnt']['gnlNopCnt4'],
                                y0['hghrSickbdCnt'], y0['stdSickbdCnt'], y0['aduChldSprmCnt'], y0['nbySprmCnt'],
                                y0['partumCnt'], y0['soprmCnt'], y0['emymCnt'], y0['ptrmCnt']
                                ])
                '''
                print(j['yadmNm'], "    기본정보 수집중...")

                result_grd = requests.post(url=url_grd, data={'ykiho':j['ykiho']})
                if 'content-length' in result_grd.headers.keys():
                    #write0.writerow([j['yadmNm'], j['clCdNm'], "null"])
                    print("not valid grade data")
                else :
                    z = result_grd.json()['data']['diagEvlVO']
                    '''
                    write0.writerow([j['yadmNm'], j['clCdNm'],
                                    z['BAgcGrd'], z['BEsophCaGrd'], z['BHccGrd'], z['BIntstGrd'], z['BLiverGrd'], z['BPancCaGrd'],
                                    z['BPciGrd'], z['BStemTransp'], z['BStomGrd'], z['BThrGrd'], z['agcGrd'], z['amiGrd'],
                                    z['anbioPrscGrd'], z['astGrd'], z['blddGrd'], z['breastGrd'], z['cabgGrd'], z['caesrGrd'],
                                    z['capGrd'], z['copGrd'], z['diagRstGrd'], z['dmGrd'], z['hytenGrd'], z['ijctPrscGrd'],
                                    z['intstGrd'], z['lcaGrd'], z['mdsAmtGrd'], z['mdsItemGrd'], z['omGrd'], z['prvtAnboGrd'],
                                    z['psydeptGrd'], z['recuhospGrd'], z['soprDiagGrd'], z['strokeGrd'],
                                    j['ykiho']
                                    ])
                    '''
                time.sleep(1)
        print("========== 현재 <",sno[0], "> 데이터 수집 중", p+1, "/", x['pages'], "수집 완료 ==========")
        time.sleep(3)
    payload['pageIndex'] = 1

