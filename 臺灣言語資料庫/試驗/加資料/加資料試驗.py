# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
import json
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.資料模型 import 著作所在地表
from django.core.exceptions import ObjectDoesNotExist

class 加資料試驗(資料庫試驗):
	def setUp(self):
		super(加資料試驗, self).setUp()
		self.詞屬性 = {'詞性':'形容詞'}
		self.詞內容 = {
			'收錄者':{'名':'鄉民', '出世年':'1950', '出世地':'臺灣'},
			'來源':{'名':'Dr. Pigu', '出世年':'1990', '出世地':'花蓮人'},
			'版權':'會使公開',
			'種類':'字詞',
			'語言腔口':'閩南語',
			'著作所在地':'花蓮',
			'著作年':'2014',
			'屬性':self.詞屬性,
			}
		self.句屬性 = {'性質':'例句'}
		self.句內容 = {
			'收錄者':{'名':'Dr. Pigu', '出世年':'1990', '出世地':'花蓮人'},
			'來源':{'名':'鄉民', '出世年':'1950', '出世地':'臺灣'},
			'版權':'袂使公開',
			'種類':'語句',
			'語言腔口':'四縣話',
			'著作所在地':'臺灣',
			'著作年':'195x',
			'屬性':self.句屬性,
			}
	def test_加詞(self):
		原來資料數 = self.資料表.objects.all().count()
		self.資料 = self.資料表.加資料(self.詞內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(self.資料.收錄者, self.臺灣人)
		self.assertEqual(self.資料.來源, self.花蓮人)
		self.assertEqual(self.資料.版權, self.會使公開)
		self.assertEqual(self.資料.種類, self.字詞)
		self.assertEqual(self.資料.語言腔口, self.閩南語)
		self.assertEqual(self.資料.著作所在地, self.花蓮)
		self.assertEqual(self.資料.著作年, self.二空一四)
		self.比較屬性(self.資料, self.詞屬性)
	def test_加句(self):
		原來資料數 = self.資料表.objects.all().count()
		self.資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(self.資料.收錄者, self.花蓮人)
		self.assertEqual(self.資料.來源, self.臺灣人)
		self.assertEqual(self.資料.版權, self.袂使公開)
		self.assertEqual(self.資料.種類, self.語句)
		self.assertEqual(self.資料.語言腔口, self.四縣話)
		self.assertEqual(self.資料.著作所在地, self.臺灣)
		self.assertEqual(self.資料.著作年, self.一九五空年代)
		self.比較屬性(self.資料, self.句屬性)
	def test_濟个正常語料(self):
		self.test_加詞()
		self.test_加句()
		self.test_加句()
		self.test_加詞()
		self.test_加詞()
		self.test_加句()
		self.test_加句()
	def test_收錄者舊字串(self):
		self.句內容['收錄者'] = json.dumps(self.句內容['收錄者'])
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_收錄者舊編號(self):
		self.句內容['收錄者'] = self.花蓮人.pk
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_收錄者新物件(self):
		self.句內容['收錄者'] = json.dumps({'名':'阿媠', '職業':'學生'})
		self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
	def test_收錄者新字串(self):
		self.句內容['收錄者'] = json.dumps({'名':'阿媠', '職業':'學生'})
		self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
	def test_收錄者新編號(self):
		self.句內容['收錄者'] = 1990
		self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
	def test_收錄者無(self):
		self.句內容.pop('收錄者')
		self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
	# 會當傳物件的攏用AttributeError
	def test_收錄者毋是字典字串佮編號(self):
		self.句內容['收錄者'] = 1990.0830
		self.assertRaises(AttributeError, self.資料表.加資料, self.句內容)
		self.句內容['收錄者'] = None
		self.assertRaises(AttributeError, self.資料表.加資料, self.句內容)
		self.句內容['收錄者'] = ['阿媠']
		self.assertRaises(AttributeError, self.資料表.加資料, self.句內容)
	def test_來源舊字串(self):
		self.句內容['來源'] = json.dumps(self.句內容['來源'])
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_來源舊編號(self):
		self.句內容['來源'] = self.臺灣人.pk
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_來源新物件(self):
		self.句內容['來源'] = {'名':'阿媠', '職業':'學生'}
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源.名, '阿媠')
		self.assertEqual(資料.來源.屬性.count(), 1)
		self.assertEqual(資料.來源.屬性.first().分類, '職業')
		self.assertEqual(資料.來源.屬性.first().性質, '學生')
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_來源新字串(self):
		self.句內容['來源'] = json.dumps({'名':'阿媠', '職業':'學生'})
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源.名, '阿媠')
		self.assertEqual(資料.來源.屬性.count(), 1)
		self.assertEqual(資料.來源.屬性.first().分類, '職業')
		self.assertEqual(資料.來源.屬性.first().性質, '學生')
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_來源新物件無名(self):
		self.句內容['來源'] = {'姓名':'阿媠', '職業':'學生'}
		self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
	def test_來源新字串無名(self):
		self.句內容['來源'] = json.dumps({'姓名':'阿媠', '職業':'學生'})
		self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
	def test_來源新編號(self):
		self.句內容['來源'] = 200
		self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
	def test_來源無(self):
		self.句內容.pop('來源')
		self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
	# 會當傳物件的攏用AttributeError
	def test_來源毋是字典字串佮編號(self):
		self.句內容['來源'] = 1990.0328
		self.assertRaises(AttributeError, self.資料表.加資料, self.句內容)
		self.句內容['來源'] = None
		self.assertRaises(AttributeError, self.資料表.加資料, self.句內容)
		self.句內容['來源'] = ['阿緣']
		self.assertRaises(AttributeError, self.資料表.加資料, self.句內容)
	def test_版權舊編號(self):
		self.句內容['版權'] = self.袂使公開.pk
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_版權新字串(self):
		self.句內容['版權'] = '攏會使'
		self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
	def test_版權新編號(self):
		self.句內容['版權'] = 2815
		self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
	def test_版權無(self):
		self.句內容.pop('版權')
		self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
	def test_版權毋是字串佮編號(self):
		self.句內容['版權'] = 1990.0328
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.句內容['版權'] = None
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.句內容['版權'] = ['阿投']
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
	def test_種類舊編號(self):
		self.句內容['種類'] = self.語句.pk
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_種類新字串(self):
		self.句內容['種類'] = '課本'
		self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
	def test_種類新編號(self):
		self.句內容['種類'] = -5
		self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
	def test_種類無(self):
		self.句內容.pop('種類')
		self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
	def test_種類毋是字串佮編號(self):
		self.句內容['種類'] = 1115.12
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.句內容['種類'] = None
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.句內容['種類'] = ['過年']
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
	def test_語言腔口舊編號(self):
		self.句內容['語言腔口'] = self.四縣話.pk
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_語言腔口新字串(self):
		self.句內容['語言腔口'] = '豬豬語'
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口.語言腔口, '豬豬語')
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_語言腔口新編號(self):
		self.句內容['語言腔口'] = 語言腔口表.objects.count() * 5
		self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
	def test_語言腔口無(self):
		self.句內容.pop('語言腔口')
		self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
	def test_語言腔口毋是字串佮編號(self):
		self.句內容['語言腔口'] = 1115.12
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.句內容['語言腔口'] = None
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.句內容['語言腔口'] = ['噶哈巫', '四庄番']
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
	def test_著作所在地舊編號(self):
		self.句內容['著作所在地'] = self.臺灣.pk
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_著作所在地新字串(self):
		self.句內容['著作所在地'] = '埔里'
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地.著作所在地, '埔里')
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_著作所在地新編號(self):
		self.句內容['著作所在地'] = 著作所在地表.objects.order_by('-pk').first().pk + 1
		self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
	def test_著作所在地無(self):
		self.句內容.pop('著作所在地')
		self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
	def test_著作所在地毋是字串佮編號(self):
		self.句內容['著作所在地'] = 1115.12
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.句內容['著作所在地'] = None
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.句內容['著作所在地'] = {'守城份', '牛眠山', '大湳', '蜈蚣崙'}
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
	def test_著作年舊編號(self):
		self.句內容['著作年'] = self.一九五空年代.pk
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_著作年新字串(self):
		self.句內容['著作年'] = '19xx'
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年.著作年, '19xx')
		self.比較屬性(資料, self.句屬性)
	def test_著作年新編號(self):
		self.句內容['著作年'] = 333
		self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
	def test_著作年無(self):
		self.句內容.pop('著作年')
		self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
	def test_著作年毋是字串佮編號(self):
		self.句內容['著作年'] = 180.55
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.句內容['著作年'] = None
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.句內容['著作年'] = {'苗栗縣', '台中縣', '彰化縣'}
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
	def test_屬性是字串(self):
		self.句內容['屬性'] = json.dumps(self.句內容['屬性'])
		原來資料數 = self.資料表.objects.all().count()
		self.資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(self.資料.收錄者, self.花蓮人)
		self.assertEqual(self.資料.來源, self.臺灣人)
		self.assertEqual(self.資料.版權, self.袂使公開)
		self.assertEqual(self.資料.種類, self.語句)
		self.assertEqual(self.資料.語言腔口, self.四縣話)
		self.assertEqual(self.資料.著作所在地, self.臺灣)
		self.assertEqual(self.資料.著作年, self.一九五空年代)
		self.比較屬性(self.資料, self.句屬性)
	def test_屬性無合法的json字串(self):
		self.句內容['屬性'] = '{[}'
		self.assertRaises(ValueError, self.資料表.加資料, self.句內容)
	# 會當傳物件的攏用AttributeError
	def test_屬性是數字(self):
		self.句內容['屬性'] = 33
		self.assertRaises(AttributeError, self.資料表.加資料, self.句內容)
	def test_屬性是字典(self):
		self.句內容['屬性'] = {'詞性'}
		self.assertRaises(AttributeError, self.資料表.加資料, self.句內容)
	def test_屬性是陣列(self):
		self.句內容['屬性'] = ['詞性']
		self.assertRaises(AttributeError, self.資料表.加資料, self.句內容)
	def test_無屬性(self):
		self.句內容.pop('屬性')
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源, self.臺灣人)
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口, self.四縣話)
		self.assertEqual(資料.著作所在地, self.臺灣)
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, {})
	def test_濟个綜合語料(self):
		self.句內容['來源'] = json.dumps({'名':'阿媠', '職業':'學生'})
		self.句內容['版權'] = self.袂使公開.pk
		self.句內容['語言腔口'] = '豬豬語'
		self.句內容['著作所在地'] = '員林'
		原來資料數 = self.資料表.objects.all().count()
		資料 = self.資料表.加資料(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
		self.assertEqual(資料.收錄者, self.花蓮人)
		self.assertEqual(資料.來源.名, '阿媠')
		self.assertEqual(資料.來源.屬性.count(), 1)
		self.assertEqual(資料.來源.屬性.first().分類, '職業')
		self.assertEqual(資料.來源.屬性.first().性質, '學生')
		self.assertEqual(資料.版權, self.袂使公開)
		self.assertEqual(資料.種類, self.語句)
		self.assertEqual(資料.語言腔口.語言腔口, '豬豬語')
		self.assertEqual(資料.著作所在地.著作所在地, '員林')
		self.assertEqual(資料.著作年, self.一九五空年代)
		self.比較屬性(資料, self.句屬性)
	def test_規個內容用字串(self):
		self.詞內容 = json.dumps(self.詞內容)
		self.test_加詞()
		self.句內容 = json.dumps(self.句內容)
		self.test_加句()
	def 比較屬性(self, 資料, 屬性欄位內容):
		try:
			內容 = json.loads(屬性欄位內容)
		except:
			內容 = 屬性欄位內容
		self.assertEqual(資料.屬性內容(), 內容)
