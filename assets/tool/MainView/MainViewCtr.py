# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-08 21:02:23
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-11 10:41:53
import os;
import wx;

from _Global import _GG;

from MainViewUI import *;

CurPath = os.path.dirname(os.path.realpath(__file__)); # 当前文件目录

require(GetPathByRelativePath("../", CurPath), "_loadtool"); # 加载逻辑

GameConfig = require(GetPathByRelativePath("../config", CurPath), "gameConfig", "GameConfig");

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateView",
	};

class MainViewCtr(object):
	"""docstring for MainViewCtr"""
	def __init__(self, parent, params = {}):
		super(MainViewCtr, self).__init__();
		self.className_ = MainViewCtr.__name__;
		self.curPath = CurPath;
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent, params); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
		self.__speedGrade = 0; # 速度等级

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unregisterEventMap(); # 注销事件
		self.unbindBehaviors(); # 解绑组件
		self.delCtrMap(); # 銷毀控制器列表

	def delCtrMap(self):
		for key in self.__CtrMap:
			DelCtr(self.__CtrMap[key]);
		self.__CtrMap.clear();

	def initUI(self, parent, params):
		# 创建视图UI类
		self.UI = MainViewUI(parent, curPath = self.curPath, viewCtr = self, params = params);
		self.UI.initView();

	def getUI(self):
		return self.UI;

	"""
		key : 索引所创建控制类的key值
		path : 所创建控制类的路径
		parent : 所创建控制类的UI的父节点，默认为本UI
		params : 扩展参数
	"""
	def createCtrByKey(self, key, path, parent = None, params = {}):
		if not parent:
			parent = self.getUI();
		self.__CtrMap[key] = CreateCtr(path, parent, params = params);

	def getCtrByKey(self, key):
		return self.__CtrMap.get(key, None);

	def getUIByKey(self, key):
		ctr = self.getCtrByKey(key);
		if ctr:
			return ctr.getUI();
		return None;
		
	def registerEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").register(eventId, self, callbackName);

	def unregisterEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").unregister(eventId, self, callbackName);

	def bindBehaviors(self):
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		self.UI.updateView(data);

	def checkUpgradeRate(self, score):
		speedConfig = GameConfig.get("speedConfig", []);
		if self.__speedGrade < len(speedConfig) and score >= speedConfig[self.__speedGrade]:
			self.__speedGrade += 1;
			return True;
		return False;

	def getScoreRuleTextList(self):
		speedConfig = GameConfig.get("speedConfig", []);
		scoreRuleTextList = [];
		index, mul = 0, 1;
		for score in speedConfig:
			if index + 1 < len(speedConfig):
				scoreRuleTextList.append("{0}-{1}分 -> {2}倍始速".format(score, speedConfig[index+1], mul));
			else:
				scoreRuleTextList.append(">{0}分 -> {1}倍始速".format(score, mul));
			index, mul = index + 1, mul + 1;
		return scoreRuleTextList;

	def getFoodRuleTextList(self):
		foodConfig = GameConfig.get("foodConfig", []);
		foodRuleTextList = [
			# "绿色：+1分【正常食物】",
			# "蓝色：+3分【3秒内提升1个等级速度】",
			# "红色：+4分【吃完后会生成黑块】",
			# "黑色：--分【当蛇头接触后游戏立即结束】",
		];
		if "normal" in foodConfig:
			foodRuleTextList.append("{0}：+{1}分【{2}】".format(foodConfig["normal"].get("color_tips", "颜色"), foodConfig["normal"].get("score", 0), foodConfig["normal"].get("exTips", "提示")));
		if "speedUp" in foodConfig:
			foodRuleTextList.append("{0}：+{1}分【{2}】".format(foodConfig["speedUp"].get("color_tips", "颜色"), foodConfig["speedUp"].get("score", 0), foodConfig["speedUp"].get("exTips", "提示")));
		if "excretion" in foodConfig:
			foodRuleTextList.append("{0}：+{1}分【{2}】".format(foodConfig["excretion"].get("color_tips", "颜色"), foodConfig["excretion"].get("score", 0), foodConfig["excretion"].get("exTips", "提示")));
		if "waste" in foodConfig:
			foodRuleTextList.append("{0}：--分【{1}】".format(foodConfig["waste"].get("color_tips", "颜色"), foodConfig["waste"].get("exTips", "提示")));
		return foodRuleTextList;

	def getFoodInfo(self):
		foodConfig = GameConfig.get("foodConfig", []);
		normalConfig, speedUpConfig, excretionConfig = foodConfig["normal"], foodConfig["speedUp"], foodConfig["excretion"];
		return {
			"probabilityMap" : {
				"normal" : {"min" : 0, "max" : normalConfig.get("rate", 0)},
				"speedUp" : {"min" : normalConfig.get("rate", 0), "max" : normalConfig.get("rate", 0) + speedUpConfig.get("rate", 0)},
				"excretion" : {"min" : normalConfig.get("rate", 0) + speedUpConfig.get("rate", 0), "max" : normalConfig.get("rate", 0) + speedUpConfig.get("rate", 0) + excretionConfig.get("rate", 0)},
			},
			"normal" : {"color" : normalConfig.get("color", "green"), "score" : normalConfig.get("score", 1)},
			"speedUp" : {"color" : speedUpConfig.get("color", "blue"), "score" : speedUpConfig.get("score", 3)},
			"excretion" : {"color" : excretionConfig.get("color", "red"), "score" : excretionConfig.get("score", 4)},
			"waste" : {"color" : foodConfig["waste"].get("color", "black")},
		};