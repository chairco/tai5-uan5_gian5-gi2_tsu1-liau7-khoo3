# -*- coding: utf-8 -*-
"""
著作權所有 (C) 民國102年 意傳文化科技
開發者：薛丞宏
網址：http://意傳.台灣
語料來源：請看各資料庫內說明

本程式乃自由軟體，您必須遵照SocialCalc設計的通用公共授權（Common Public Attribution License, CPAL)來修改和重新發佈這一程式，詳情請參閱條文。授權大略如下，若有歧異，以授權原文為主：
	１．得使用、修改、複製並發佈此程式碼，且必須以通用公共授權發行；
	２．任何以程式碼衍生的執行檔或網路服務，必須公開該程式碼；
	３．將此程式的原始碼當函式庫引用入商業軟體，且不需公開非關此函式庫的任何程式碼

此開放原始碼、共享軟體或說明文件之使用或散佈不負擔保責任，並拒絕負擔因使用上述軟體或說明文件所致任何及一切賠償責任或損害。

臺灣言語工具緣起於本土文化推廣與傳承，非常歡迎各界用於商業軟體，但希望在使用之餘，能夠提供建議、錯誤回報或修補，回饋給這塊土地。

感謝您的使用與推廣～～勞力！承蒙！
"""
from 舊臺灣言語工具.資料庫.資料庫連線 import 資料庫連線

class 教育部閩南語辭典工具:
	揣造字 = 資料庫連線.prepare('SELECT "統一碼","組字式" ' +
		'FROM "教育部臺灣閩南語常用詞辭典"."造字集" ORDER BY "統一碼" ASC')
	造字集 = {統一碼:組字式 for 統一碼, 組字式 in 揣造字()}
	def 共造字換做統一碼表示法(self,文字):
		統一碼表示法 = ''
		for 字元 in 文字:
			if hex(ord(字元))[2:] in self.造字集:
				統一碼表示法 += self.造字集[ hex(ord(字元))[2:] ]
			else:
				統一碼表示法 += 字元
		return 統一碼表示法
	def 釋義挑出翻譯(self,釋義):
		釋義=釋義.split('，',1)[0].split('。',1)[0].split('；',1)[0].split('、')
		翻譯=self.挑出有效的翻譯(釋義)
		return 翻譯
	def 挑出有效的翻譯(self,釋義):
		# 「形容」
		# 	形容多數。
		# 【
		# 	見【骰仔】tâu-á 條。
		# 	釋義參見【九】káu 條。
		# 指
		# 	指刀子的主體部位。
		# 的
		# 	擔任某種職務的人。
		# 	無佇上尾就會使
		# 		年紀、輩份比較低的。
		# 
		# 雄性和雌性或陽性和陰性之合稱
		# 
		# 附錄
		# 	附錄－地名－火車線站名
		# 
		# 詞
		# 	反問語助詞，帶有調侃的意味。
		# 	感嘆詞。表示領悟的語氣詞
		翻譯=[]
		for 釋 in 釋義:
			if 釋=='數字':
				continue
			if 釋.startswith('比喻'):
				continue
			if 釋.startswith('形容'):
				continue
			if 釋.startswith('附錄'):
				continue
			if 釋.startswith('指'):
				continue
			if '【' in 釋:
				continue
			if '的' in 釋 and not 釋.endswith('的'):
				continue
			if '詞' in 釋:
				continue
# 			if '或' in 釋:
# 				print(釋,釋義)
			翻譯.append(釋)
		return 翻譯