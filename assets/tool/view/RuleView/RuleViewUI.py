# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-23 11:19:56
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-30 12:28:05

import wx;

from _Global import _GG;
from function.base import *;

class RuleViewUI(wx.Panel):
	"""docstring for RuleViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(RuleViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self.className_ = RuleViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;
		self.__itemInfoList = [];

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"scoreRuleTextList" : [
				"0-10分 -> 1倍始速",
				"10-30分 -> 2倍始速",
				"30-60分 -> 3倍始速",
				"60-100分 -> 4倍始速",
				"100-200分 -> 5倍始速",
				"200-400分 -> 6倍始速",
				"400-600分 -> 7倍始速",
				"600-800分 -> 8倍始速",
				"800-1000分 -> 9倍始速",
				">1000分 -> 10倍始速",
			],
			"foodRuleTextList" : [
				"绿色：+1分【正常食物】",
				"蓝色：+3分【3秒内提升1个等级速度】",
				"红色：+4分【吃完后会生成黑块】",
				"黑色：--分【当蛇头接触后游戏立即结束】",
			],
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self.curPath + "***View"); # , parent = self, params = {}
		self.createScoreRule();
		self.createFoodRule();
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.AddMany(self.__itemInfoList);
		self.SetSizer(box);

	def updateView(self, data):
		pass;

	def createScoreRule(self):
		scoreRuleTitle = wx.StaticText(self, label = "分数加速：");
		scoreRuleTitle.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		self.__itemInfoList.append((scoreRuleTitle, 0, wx.TOP, 10));
		for scoreRuleText in self.__params["scoreRuleTextList"]:
			scoreRuleContent = wx.StaticText(self, label = scoreRuleText, size = (self.GetSize().x, -1));
			self.__itemInfoList.append((scoreRuleContent, 0, wx.LEFT|wx.TOP, 4));

	def createFoodRule(self):
		foodRuleTitle = wx.StaticText(self, label = "食物规则：");
		foodRuleTitle.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		self.__itemInfoList.append((foodRuleTitle, 0, wx.TOP, 20));
		for foodRuleText in self.__params["foodRuleTextList"]:
			foodRuleContent = wx.StaticText(self, label = foodRuleText, size = (self.GetSize().x, -1));
			self.__itemInfoList.append((foodRuleContent, 0, wx.LEFT|wx.TOP, 4));