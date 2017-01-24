import requests

url = "https://patents.google.com/xhr/query?url=q%3Dostem%26q%3Dchassis&exp="
r = requests.get(url)
print(r)
#print(r.json())


res = r.json()['results']
print("total_num_results:\t", res['total_num_results'])
print("total_num_pages:\t", res['total_num_pages'])

res_cl = res['cluster']
print(len(res_cl))


for idx_cl in range(len(res_cl)) :
	print("\n\nCluster num ", idx_cl+1)
	if len(res_cl[idx_cl]['result']) < 1 :
		continue
	for idx_sub in range(len(res_cl[idx_cl]['result'])) :
		tg = res_cl[idx_cl]['result'][idx_sub]['patent']
		print(">>",tg['title'], "\n>>", tg['publication_number'],"\n")
