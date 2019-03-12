# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-23 11:19:34
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-30 18:12:23

import wx;
import random,math;

from _Global import _GG;
from function.base import *;

class SnakeViewUI(wx.Panel):
	"""docstring for SnakeViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(SnakeViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self.className_ = SnakeViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;
		self.init();

	def init(self):
		self.SetBackgroundColour(self.__params["bgColour"]);
		self.createTimer();
		self.__snake = self.createSnake(); # 蛇体数据处理对象
		self.__playing = False; # 游戏进行中的标记
		self.__foodInfoMap = {}; # 食物信息表【key = idx, value = item】
		self.__direction = self.__snake.getDirection(); # 初始化方向
		self.__movingData = { # 移动蛇体的信息
			"flag" : False, # 移动标记
			"rate" : self.__params["movingRate"], # 移动率【移动距离/单个Item尺寸】
			"bodyTailIdx" : -1, # 蛇体尾部索引位置
			"targetIdx" : -1, # 目标索引位置
			"targetPosList" : [], # 目标位置列表
			"incrementList" : [], # 移动增量列表
		};

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.stopTimer(isDestroy = True); # 停止定时器

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (360,360),
			"style" : wx.BORDER_NONE,
			"bgColour" : wx.Colour(255,255,255),
			"matrix" : (36,36),
			"snakeColour" : wx.Colour(0,0,0),
			"movingRate" : 0.1,
			"interval" : 30,
			"foodInfo" : {
				"probabilityMap" : {
					"normal" : {"min" : 0, "max" : 0.6},
					"speedUp" : {"min" : 0.6, "max" : 0.8},
					"excretion" : {"min" : 0.8, "max" : 1.0},
				},
				"normal" : {"color" : "green", "score" : 1},
				"speedUp" : {"color" : "blue", "score" : 3},
				"excretion" : {"color" : "red", "score" : 4},
				"waste" : {"color" : "black"},
			},
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
		pass;
		
	def initViewLayout(self):
		pass;

	def updateView(self, data):
		pass;

	# 创建蛇体
	def createSnake(self):
		params = {
			"size" : self.getItemSize(),
			"bgColour" : self.__params["snakeColour"],
			"matrix" : self.__params["matrix"],
		};
		return self.getCtr().createSnake(params = params);

	def createTimer(self):
		self.__timer = _GG("TimerManager").createTimer(self, callback = self.onTimer);

	def startTimer(self):
		self.__timer.Start(self.__params["interval"]);

	def stopTimer(self, isDestroy = False):
		if self.__timer.IsRunning():
			self.__timer.Stop();
			if isDestroy:
				_GG("TimerManager").deleteTimer(self.__timer);

	def onTimer(self, event = None):
		self.moveSnake();

	def getItemSize(self):
		rows, cols = self.__params["matrix"][0], self.__params["matrix"][1];
		return wx.Size(self.__params["size"][0]/cols, self.__params["size"][1]/rows);

	def createItem(self):
		item = wx.Panel(self, size = self.getItemSize(), style = wx.BORDER_NONE);
		self.resetItem(item);
		return item;

	def resetItem(self, item):
		item.m_score = 0;
		item.m_key = "";

	def moveSnake(self):
		if self.__moveSnake__():
			return; # 直接返回，不执行以下逻辑
		ret,idx = self.__snake.check();
		if ret:
			# 更新方向数据
			self.__direction = self.__snake.getDirection();
			if idx in self.__foodInfoMap:
				foodItem = self.__foodInfoMap.pop(idx);
				self.__snake.eat(foodItem);
				self.__onEatFood__(foodItem);
			else:
				self.__moveSnake__(idx);
				# self.__snake.move(idx);
		else:
			self.gameOver();

	def __moveSnake__(self, idx = -1):
		if self.__movingData["flag"]:
			incrementList = self.__movingData["incrementList"];
			targetPosList = self.__movingData["targetPosList"];
			posList = [];
			for i in range(self.__snake.getBodyLength()):
				curPos = self.__snake.getItemPos(i);
				diffPos = targetPosList[i] - curPos;
				if math.fabs(diffPos.x) >= math.fabs(incrementList[i].x) and math.fabs(diffPos.y) >= math.fabs(incrementList[i].y):
					nextPos = curPos + incrementList[i];
					posList.append(nextPos);
				else:
					self.__movingData["flag"] = False;
					self.__snake.moveTo(posList = targetPosList); # 直接移到目标位置处
					self.__snake.removeBlankIdx(self.__movingData["targetIdx"]);
					self.__snake.addBlankIdx(self.__movingData["bodyTailIdx"]);
					return False;
			self.__snake.moveTo(posList = posList);
			return True;
		elif idx >= 0:
			self.__movingData["flag"] = True;
			self.__movingData["targetIdx"] = idx;
			self.__movingData["bodyTailIdx"] = self.__snake.getItemIdx(-1);
			self.__movingData["targetPosList"] = self.__snake.getNextPosList(idx);
			self.__movingData["incrementList"] = [];
			for i in range(self.__snake.getBodyLength()):
				movingDist = self.__movingData["targetPosList"][i] - self.__snake.getItemPos(i);
				self.__movingData["incrementList"].append(wx.Point(movingDist.x * self.__movingData["rate"], movingDist.y * self.__movingData["rate"]));
			self.__moveSnake__();
		return False;

	def gameOver(self):
		self.stopTimer();
		self.__playing = False;
		msgDialog = wx.MessageDialog(self, "游戏结束！", "游戏结束", style = wx.OK|wx.ICON_INFORMATION);
		msgDialog.ShowModal();

	def initGame(self):
		row = int(self.__params["matrix"][0]/2);
		col = int(self.__params["matrix"][1]/2);
		itemPos = self.__snake.getPos(row = row, col = col);
		item = self.createItem();
		item.Move(itemPos.x, itemPos.y);
		direction = self.getCtr().getRandomDirection();
		self.__snake.setDirection(direction);
		self.__snake.eat(item);

	def createFoodItem(self):
		idx = random.randint(0, len(self.__snake.getBlankIdxs())-1);
		itemPos = self.__snake.getPos(idx = idx);
		item = self.createItem();
		item.Move(itemPos.x, itemPos.y);
		item.m_key, foodItemInfo = self.getFoodItemInfo();
		item.m_score = foodItemInfo["score"];
		item.SetBackgroundColour(foodItemInfo["color"]);
		item.Refresh();
		self.__foodInfoMap[idx] = item;

	def getFoodItemInfo(self):
		foodInfo = self.__params["foodInfo"];
		probability = random.random();
		for k,v in foodInfo.get("probabilityMap", {}).items():
			if probability >= v["min"] and probability <= v["max"]:
				return k, foodInfo[k];
		print("Error foodInfo !", foodInfo);
		raise Exception("There is a error in foodInfo!");

	def getDirection(self):
		return self.__direction;

	def updateDirection(self, direction):
		if self.getCtr().checkDirection(direction):
			self.__snake.setDirection(direction);

	def startGame(self, event = None):
		if not self.__playing:
			self.initGame();
			for i in range(3):
				self.createFoodItem();
			self.__playing = True;
		if not self.__timer.IsRunning():
			self.startTimer();

	def pauseGame(self, event = None):
		if self.__playing:
			self.stopTimer();

	def isPlaying(self):
		return self.__playing;

	def isRunningTimer(self):
		return self.__timer.IsRunning();

	def upgradeRate(self):
		if self.__movingData["rate"] < 1:
			self.__movingData["rate"] += 0.1;

	def dropRate(self):
		if self.__movingData["rate"] > 0:
			self.__movingData["rate"] -= 0.1;

	def __onEatFood__(self, foodItem):
		self.createFoodItem();
		if hasattr(self, "onAddScore"):
			self.onAddScore(foodItem.m_score);
		self.__onKeyCallback__(foodItem);
		self.resetItem(foodItem);

	def __onKeyCallback__(self, foodItem):
		if foodItem.m_key == "speedUp":
			self.upgradeRate();
			wx.CallLater(3000, self.dropRate);
		elif foodItem.m_key == "excretion":
			# 设置相应脏索引
			self.__snake.setDirtyIdx(self.__snake.getItemIdx(-1));
			# 创建垃圾item
			itemPos = self.__snake.getItemPos(-1);
			item = self.createItem();
			item.Move(itemPos.x, itemPos.y);
			itemInfo = self.__params["foodInfo"].get("waste", {"color" : "black"});
			item.SetBackgroundColour(itemInfo["color"]);
			item.Refresh();