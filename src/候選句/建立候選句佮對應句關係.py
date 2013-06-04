from 剖析相關工具.剖析結構化工具 import 剖析結構化工具
from 剖析相關工具.剖析結構化工具 import 國閩單位翻譯
from 剖析相關工具.剖析工具 import 剖析工具
from 言語資料庫.公用資料 import 資料庫連線
from 候選句.交叉二維揣候選句 import 詞相關評價
from 閩南資料.國閩字詞翻譯 import 字音結構化
from 候選句.交叉二維揣候選句 import 交叉二維揣候選句
from 閩南資料.國閩字詞翻譯 import 翻譯佮詞性語意字音結構化

class 建立候選句佮對應句關係:
	def __init__(self):
# 		self.揣剖析資料 = 資料庫連線.prepare('SELECT ' +
# 			'"甲"."流水號","丁"."流水號","甲"."型體","甲"."音標","乙"."型體","丁"."型體","丁"."音標"' +
# 			'FROM "言語"."文字" AS "甲","言語"."斷詞暫時表" AS "乙","言語"."關係" AS "丙",' +
# 			'"言語"."文字" AS "丁" ' +
# 			'WHERE "甲"."流水號"="乙"."斷詞目標流水號" AND' +
# 			'"甲"."流水號"="丙"."乙流水號" AND "丙"."關係性質"=\'會當替換\' AND ' +
# 			'"丁"."流水號"="丙"."甲流水號" ' +
# 			'ORDER BY "甲"."流水號" DESC ' +
# 			'LIMIT 10000')()
# 		self.揣剖析資料 = 資料庫連線.prepare('SELECT DISTINCT ' +
# 			'"甲"."流水號","甲"."型體","甲"."音標","乙"."型體","丁"."型體","丁"."音標"' +
# 			'FROM "言語"."文字" AS "甲","言語"."斷詞暫時表" AS "乙","言語"."關係" AS "丙",' +
# 			'"言語"."文字" AS "丁" ' +
# 			'WHERE "甲"."流水號"="乙"."斷詞目標流水號" AND' +
# 			'"甲"."流水號"="丙"."乙流水號" AND "丙"."關係性質"=\'會當替換\' AND ' +
# 			'"丁"."流水號"="丙"."甲流水號" ' +
# 			'ORDER BY "甲"."流水號" DESC ' +
# 			'LIMIT 100000')()
		self.揣剖析資料 = [(1099398, '你這乳臭未乾的小子，自以為長大了就不肯聽話，我看你是皮癢的樣子。', None, '#3:1.[0] S(NP(Head:N:我)|Head:Vt:看|S(NP(Head:N:你)|Head:Vt:是|NP(V‧的(Vi:皮癢|Head:T:的)|Head:N:樣子)))#。(PERIODCATEGORY)', '囡仔疕爾爾就生毛閣發角，我看你是皮咧癢的款。', 'gin2-a2-phi2 nia7-nia7 to7 senn1-mng5 koh4 huat4-kak4, gua2 khuann3 li2 si7 phue5 teh4 tsiunn7 e5 khuan2. '), (988032, '我很討厭別人干預我的事。', None, '#1:1.[0] S(NP(Head:N:我)|ADV:很|Head:Vt:討厭|S(NP(Head:N:別人)|Head:Vt:干預|NP(N‧的(N:我|Head:T:的)|Head:N:事)))#。(PERIODCATEGORY)', '我真討厭別人干涉我的代誌。', 'gua2 tsin1 tho2-ia3 pat8-lang5 kan1-siap8 gua2 e5 tai7-tsi3. ')]
		self.揣對應資料 = lambda 流水號: 資料庫連線.prepare('SELECT DISTINCT ' +
			'"丁"."流水號","丁"."型體","丁"."音標" ' +
			'FROM "言語"."關係" AS "丙",' +
			'"言語"."文字" AS "丁" ' +
			'WHERE ' +
			'"丙"."乙流水號"=$1 AND "丙"."關係性質"=\'會當替換\' AND ' +
			'"丁"."流水號"="丙"."甲流水號" ' +
			'ORDER BY "丁"."流水號" DESC ' +
			'LIMIT 100000')(流水號)
# 		print(self.揣剖析資料)
	def 相似換新(self, 待翻句, 候選句, 對應句, 對應音標, 配對, 細配對):
		替換表 = []
		for 待翻位置 in range(1, len(待翻句)):
			if (待翻位置, 配對[待翻位置]) in 細配對:
				替換表.extend(
						self.相似換新(待翻句[待翻位置], 候選句[配對[待翻位置]], 對應句, 對應音標,
					細配對[(待翻位置, 配對[待翻位置])][0], 細配對[(待翻位置, 配對[待翻位置])][1]))
			elif 配對[待翻位置] == -1:
				待翻對照詞 = 國閩單位翻譯(待翻句[待翻位置])
				print(翻譯佮詞性語意字音結構化(待翻對照詞))
				print(待翻對照詞, end = '')
				print('加入來')
			else:
				待翻對照詞 = 國閩單位翻譯(待翻句[待翻位置])
				print(翻譯佮詞性語意字音結構化(待翻對照詞))
				if 待翻句[待翻位置][0] == 候選句[配對[待翻位置]][0]:
# 					print(待翻對照詞, end = '')
					
					for 對照 in 待翻對照詞[0]:  # 結果=(字,音）
# 						if 對照[0] in 對應句 and 對照[1] in 對應音標:
						if 對照[0] in 對應句 and 對照[1] in 對應音標:
							print(對照, end = ",")
					
					print(" 免變")
				else:
					候選對照詞 = 國閩單位翻譯(候選句[配對[待翻位置]])
					for 對照 in 候選對照詞[0]:  # 結果=(字,音）
# 						if 對照[0] in 對應句 and 對照[1] in 對應音標:
						if 對照[0] in 對應句 and 對照[1] in 對應音標:
							print(對照, end = ",")
# 							else:
# 								賰的.append(結果)
# 						print(對照詞, end = '')
					print(" ----> ", end = '')
# 						賰的=[]
					print(待翻對照詞)
		for 候選位置 in range(1,len(候選句)):
			if 候選位置 not in 配對:
				候選對照詞 = 國閩單位翻譯(候選句[候選位置])
				print(候選對照詞, end = '')
				print('擲掉')
		return 替換表
if __name__ == '__main__':
	結構化工具 = 剖析結構化工具()
	揣候選句工具 = 交叉二維揣候選句()
	翻譯句 = '#2:1.[0] S(NP(Head:N:我)|Head:Vt:想|VP(Head:Vi:回家))#，(COMMACATEGORY)'
	翻譯句 = '#1:1.[0] S(NP(Head:N:我)|Head:Vt:覺得|S(NP(Head:N:我)|Head:Vt:做|ASP:了|NP(DM:一個|V‧的(Vi:假|Head:T:的)|Head:N:作品)))#'

	翻譯句結構化結果 = 結構化工具.結構化剖析結果(翻譯句)
	印出 = lambda 型體佮詞性語意:print(型體佮詞性語意[0], end = ' ')
# 	print(國閩單位翻譯(('吃',)))

	for 剖析結果字串 in 揣候選句工具.揣剖析資料:
# 		print(剖析結果字串)
		結構化結果 = 結構化工具.結構化剖析結果(剖析結果字串[3])
		分數 = 揣候選句工具.相似比較(翻譯句結構化結果[1], 結構化結果[1], 詞相關評價)
# 		print(分數)
		if 分數[0] >= 6400:
			print(剖析結果字串)
			print(翻譯句結構化結果)
			print(結構化結果)
			結構化工具.處理結構化結果(翻譯句結構化結果, 印出)
			print()
			結構化工具.處理結構化結果(結構化結果, 印出)
			print()
			print(分數)
			建立關係=建立候選句佮對應句關係()
			結構化=字音結構化([(剖析結果字串[4], 剖析結果字串[5])])
			print(結構化)
			print(結構化[0].下跤)
# 			建立關係.相似換新(翻譯句結構化結果[1], 結構化結果[1], 剖析結果字串[4], 剖析結果字串[5], 分數[1], 分數[2])
# 			分數=揣候選句工具.相似(翻譯句結構化結果[1], 結構化結果[1], 詞相關評價)
# 			for 對應句 in 揣候選句工具.揣對應資料(剖析結果字串[0]):
# 				print(對應句[1])
# 				print(揣候選句工具.相似換新(翻譯句結構化結果, 結構化結果, 對應句[1], 詞相關評價))
			print()


	工具 = 剖析工具()
# 	剖析結果字串集=工具.剖析('我想吃飯，，，我想吃很多飯。假如我也用這種方式旅行。再想到蝴蝶會生滿屋的毛蟲。')
	剖析結果字串集 = ['#1:1.[0] S(NP(Head:N:我)|Head:Vt:想|VP(Head:Vi:吃飯))#，(COMMACATEGORY)',
			'#2:1.[0] %()#，(COMMACATEGORY)',
			'#3:1.[0] %()#，(COMMACATEGORY)',
			'#4:1.[0] S(NP(Head:N:我)|Head:Vt:想|VP(Head:Vt:吃|NP(DET:很多|Head:N:飯)))#。(PERIODCATEGORY)',
			'#5:1.[0] S(C:假如|NP(Head:N:我)|ADV:也|PP(Head:P:用|NP(DM:這種|Head:N:方式))|Head:Vi:旅行)#。(PERIODCATEGORY)',
			'#6:1.[0] VP(ADV:再|Head:Vt:想到|NP(S‧的(head:S(NP(Head:N:蝴蝶)|ADV:會|Head:Vt:生|NP(Head:N:滿屋))|Head:T:的)|Head:N:毛蟲))#。(PERIODCATEGORY)',
			'#1:1.[0] VP(evaluation:Dbb:再|Head:VE2:想到|goal:NP(predication:S‧的(head:S(agent:NP(Head:Nab:蝴蝶)|epistemics:Dbaa:會|Head:VC31:生|theme:NP(Head:Na:滿屋))|Head:DE:的)|Head:Nab:毛蟲))#。(PERIODCATEGORY)',
			'#1:1.[0] S(NP(Head:N:我們)|ADV:要|Head:Vi:下班)#，(COMMACATEGORY)',
			'#2:1.[0] S(NP(Head:N:我)|PP(Head:P:和|NP(Head:N:他))|Head:Vt:想|VP(Head:Vi:回家))#，(COMMACATEGORY)',
			'#3:1.[0] S(NP(Head:N:你們)|DM:兩個|Head:Vt:想|VP(Head:Vi:睡覺))#。(PERIODCATEGORY)']
# 	for 剖析結果字串 in 剖析結果字串集:
# # 		print(剖析結果字串)
# 		結構化結果 = 結構化工具.結構化剖析結果(剖析結果字串)
# 		print(翻譯句結構化結果)
# 		print(結構化結果)
# 		結構化工具.處理結構化結果(翻譯句結構化結果,印出)
# 		print()
# 		結構化工具.處理結構化結果(結構化結果,印出)
# 		print()
# 		print(揣候選句工具.相似比較(翻譯句結構化結果,結構化結果,None))
# 		print(揣候選句工具.相似換新(翻譯句結構化結果,結構化結果,'',None))
# # 		翻譯結果=結構化工具.處理結構化結果(結構化結果,國閩單位翻譯)
# # 		print(翻譯結果)
# # 		結構化工具.處理結構化結果(翻譯結果,印出)
# # 		print()
#
#
# # 	結構化結果 = 結構化工具.結構化剖析結果(剖析結果字串集[0])
# # 	結構化工具.處理結構化結果(翻譯句結構化結果,印出)
# # 	print()
# # 	結構化工具.處理結構化結果(結構化結果,印出)
# # 	print()
# # 	print(揣候選句工具.相似比較(翻譯句結構化結果,結構化結果,None))
# # 	print(揣候選句工具.相似換新(翻譯句結構化結果,結構化結果,'我想欲食飯',None))
# #
# # 	print(國閩單位翻譯(['回家']))
