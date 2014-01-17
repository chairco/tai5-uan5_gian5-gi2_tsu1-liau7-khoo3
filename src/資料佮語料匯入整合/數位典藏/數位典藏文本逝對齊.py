"""
著作權所有 (C) 民國103年 意傳文化科技
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
from 資料庫.資料庫連線 import 資料庫連線
from 字詞組集句章.解析整理工具.文章初胚工具 import 文章初胚工具
from 字詞組集句章.解析整理工具.拆文分析器 import 拆文分析器
from 字詞組集句章.音標系統.閩南語.教會羅馬字音標 import 教會羅馬字音標

class 數位典藏文本逝對齊:
	到逝 = True
	揣數位典藏文本段資料庫 = 資料庫連線.prepare(
		'SELECT "流水號","時代","年","類","類二","漢羅標","全羅標","漢羅名","全羅名","檔案名","漢羅文","全羅文","漢羅逝","全羅逝" ' +
		'FROM "台語文數位典藏"."改過逝資料" ORDER BY "流水號"')
	插入台語數位典藏文本資料庫 = 資料庫連線.prepare('INSERT INTO "台語文數位典藏"."原始字資料" ' +
		'("流水號","時代","年","類","類二","漢羅文","全羅文","無齊記號") ' +
		'VALUES ($1,$2,$3,$4,$5,$6,$7,$8)')
	插入修改數位典藏文本資料庫 = 資料庫連線.prepare('INSERT INTO "台語文數位典藏"."改過字資料" ' +
		'("流水號","時代","年","類","類二","漢羅文","全羅文","無齊記號") ' +
		'VALUES ($1,$2,$3,$4,$5,$6,$7,$8)')
	def __init__(self):
		初胚工具 = 文章初胚工具()
		分析器 = 拆文分析器()
		for 流水號, 時代, 年, 類, 類二, 漢羅標, 全羅標, 漢羅名, 全羅名, 檔案名, 漢羅文, 全羅文, 漢羅逝, 全羅逝 in self.揣數位典藏文本段資料庫():
			漢羅文 = [漢羅標, 漢羅名, ''] + 漢羅文.split('\n')
			全羅文 = [全羅標, 全羅名, ''] + 全羅文.split('\n')
			for 所在 in range(len(漢羅文)):
				漢羅文[所在] = 漢羅文[所在].strip()
			for 所在 in range(len(全羅文)):
				全羅文[所在] = 全羅文[所在].strip()
			print(流水號)
			if 漢羅逝 != 全羅逝 or 漢羅逝 + 3 != len(漢羅文) or 全羅逝 + 3 != len(全羅文):
				raise RuntimeError('句數有錯！！')
			無齊記號 = []
			for 漢羅, 全羅 in zip(漢羅文, 全羅文):
				try:
					新全羅 = 初胚工具.建立物件語句前處理減號(教會羅馬字音標, 全羅)
					分析器.產生對齊句(漢羅, 新全羅)
				except:
					無齊記號.append('*')
				else:
					無齊記號.append('')
			漢羅文 = '\n'.join(漢羅文)
			全羅文 = '\n'.join(全羅文)
			無齊記號 = '\n'.join(無齊記號)
			if self.到逝:
# 				print(流水號, 時代, 年, 類, 類二, 漢羅文, 全羅文, 無齊記號)
				self.插入台語數位典藏文本資料庫(流水號, 時代, 年, 類, 類二, 漢羅文, 全羅文, 無齊記號)
				self.插入修改數位典藏文本資料庫(流水號, 時代, 年, 類, 類二, 漢羅文, 全羅文, 無齊記號)

if __name__ == '__main__':
	數位典藏文本逝對齊()
