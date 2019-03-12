# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-30 12:15:13
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-30 14:54:42
import wx;

GameConfig = {
	"foodConfig" : {
		"normal" : {"color" : "green", "score" : 1, "rate" : 0.6, "color_tips" : "绿色", "exTips" : "正常食物"},
		"speedUp" : {"color" : "blue", "score" : 3, "rate" : 0.2, "color_tips" : "蓝色", "exTips" : "3秒内提升1个等级速度"},
		"excretion" : {"color" : "red", "score" : 4, "rate" : 0.2, "color_tips" : "红色", "exTips" : "吃后会排出黑块"},
		"waste" : {"color" : "black", "score" : -999, "color_tips" : "黑色", "exTips" : "吃后当场Game Over"},
	},
	"speedConfig" : [
		0, # 1倍
		10, # 2倍
		30, # 3倍
		60, # 4倍
		100, # 5倍
		200, # 6倍
		400, # 7倍
		600, # 8倍
		800, # 9倍
		1000, # 10倍
	],
}