from 語音合成.處理中研院標音.第一步共外語處理掉 import 第一步共外語處理掉
import os
from 語音合成.處理中研院標音.第二步拆標題漢羅佮音標 import 第二步拆標題漢羅佮音標
from 語音合成.處理中研院標音.第三步整理文本格式 import 第三步整理文本格式
from 語音合成.處理中研院標音.第四步建立句物件 import 第四步建立句物件

if __name__ == '__main__':
	共外語處理掉=第一步共外語處理掉()
	拆標題漢羅佮音標=第二步拆標題漢羅佮音標()
	整理文本格式=第三步整理文本格式()
	建立物件=第四步建立句物件()
	資料="/home/Ihc/意傳計劃/語音合成/辨識合成實作/九、聽打資料處理/"
	os.chdir(資料)
	for 檔名 in os.listdir("."):
		if 檔名.endswith(".trs"):
			無外語=共外語處理掉.擲掉外語(open(資料+檔名))
			print (無外語[:10])
			分堆句=拆標題漢羅佮音標.拆開(無外語)
			print(分堆句[:10])
			整理堆=整理文本格式.整理(分堆句)
			print(整理堆[:10])
			物件堆=建立物件.建立(整理堆)
			print(物件堆[:10])
			
