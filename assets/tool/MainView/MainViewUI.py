# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-08 21:02:23
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-30 17:54:14

import wx;

from _Global import _GG;
from function.base import *;

class MainViewUI(wx.ScrolledWindow):
	"""docstring for MainViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(MainViewUI, self).__init__(parent, id, size = self.__params["size"]);
		self.className_ = MainViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;
		self.bindEvents(); # 绑定事件
		self.SetBackgroundColour(self.__params["bgColour"]);
		# 初始化滚动条参数
		self.SetScrollbars(1, 1, *self.__params["size"]);

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unbindEvents();

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : _GG("WindowObject").GetToolWinSize(),
			"style" : wx.BORDER_THEME,
			"bgColour" : wx.Colour(255,255,255),
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.viewCtr;

	def bindEvents(self):
		_GG("WindowObject").BindEventToToolWinSize(self, self.onToolWinSize);

	def unbindEvents(self):
		_GG("WindowObject").UnbindEventToToolWinSize(self);

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局
		self.resetScrollbars(); # 重置滚动条
		self.initViewEvents(); # 初始化视图事件

	def createControls(self):
		self.createControlPanel();
		self.createContentPanel();
		self.createOtherPanel();
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.controlPanel);
		box.Add(self.contentPanel);
		box.Add(self.otherPanel);
		self.SetSizer(box);

	def resetScrollbars(self):
		self.SetScrollbars(1, 1, self.GetSizer().GetSize().x, self.GetSizer().GetSize().y);

	def onToolWinSize(self, sizeInfo, event = None):
		self.SetSize(self.GetSize() + sizeInfo["preDiff"]);
		self.Refresh();
		self.Layout();

	def updateView(self, data):
		pass;

	def createControlPanel(self):
		self.controlPanel = wx.Panel(self, size = (100, self.GetSize().y), style = wx.BORDER_THEME);
		self.createStartGameBtn(self.controlPanel);
		self.createRestartGameBtn(self.controlPanel);
		self.initControlPanelLayout();

	def createStartGameBtn(self, parent):
		self.startGameBtn = wx.Button(parent, label = "开始游戏");
		self.startGameBtn.Bind(wx.EVT_BUTTON, self.onStartGame);

	def createRestartGameBtn(self, parent):
		self.restartGameBtn = wx.Button(parent, label = "重新开始");
		self.restartGameBtn.Bind(wx.EVT_BUTTON, self.onRestartGame);

	def onStartGame(self, event = None):
		if self.getCtr().getCtrByKey("SnakeViewCtr").isRunning():
			self.getCtr().getCtrByKey("SnakeViewCtr").pauseGame();
			self.startGameBtn.SetLabel("开始游戏");
		else:
			self.getCtr().getCtrByKey("SnakeViewCtr").startGame();
			self.startGameBtn.SetLabel("暂停游戏");

	def onRestartGame(self, ecent = None):
		self.onStartGame();

	def initControlPanelLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.startGameBtn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		box.Add(self.restartGameBtn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		self.controlPanel.SetSizerAndFit(box);

	def createContentPanel(self):
		self.contentPanel = wx.Panel(self, size = (600, max(600, self.GetSize().y)), style = wx.BORDER_THEME);
		self.contentPanel.SetBackgroundColour(wx.Colour(0,0,0));
		self.getCtr().createCtrByKey("SnakeViewCtr", GetPathByRelativePath("../view/SnakeView", self.curPath), parent = self.contentPanel, params = {
			"size" : (580,580),
			"matrix" : (58,58),
			"foodInfo" : self.getCtr().getFoodInfo(),
		});
		self.updateContentPanelSize();
		self.initContentPanelLayout();

	def updateContentPanelSize(self):
		contentPanelSize = self.contentPanel.GetSize();
		snakeViewSize = self.getCtr().getUIByKey("SnakeViewCtr").GetSize();
		newSizeX = max(contentPanelSize.x, snakeViewSize.x);
		newSizeY = max(self.controlPanel.GetSize().y, contentPanelSize.y, snakeViewSize.y);
		self.contentPanel.SetSize(newSizeX, newSizeY);

	def initContentPanelLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		topOffset = (self.contentPanel.GetSize().y - self.getCtr().getUIByKey("SnakeViewCtr").GetSize().y - 6) / 2;
		box.Add(self.getCtr().getUIByKey("SnakeViewCtr"), flag = wx.ALIGN_CENTER|wx.TOP, border = topOffset);
		self.contentPanel.SetSizer(box);

	def createOtherPanel(self):
		self.otherPanel = wx.Panel(self, size = (max(200, self.GetSize().x - 700), max(600, self.GetSize().y)), style = wx.BORDER_THEME);
		self.createOtherViews(self.otherPanel);
		self.updateOtherPanelSize();
		self.initOtherPanelLayout();

	def createOtherViews(self, parent):
		self.getCtr().createCtrByKey("ScoreViewCtr", GetPathByRelativePath("../view/ScoreView", self.curPath), parent = parent, params = {"size" : (parent.GetSize().x, -1)}); # , parent = self, params = {}
		scoreViewSize = self.getCtr().getUIByKey("ScoreViewCtr").GetSize();
		self.getCtr().createCtrByKey("RuleViewCtr", GetPathByRelativePath("../view/RuleView", self.curPath), parent = parent, params = {
			"size" : (scoreViewSize.x, parent.GetSize().y - scoreViewSize.y),
			"scoreRuleTextList" : self.getCtr().getScoreRuleTextList(),
			"foodRuleTextList" : self.getCtr().getFoodRuleTextList(),
		}); # , parent = self, params = {}

	def updateOtherPanelSize(self):
		otherPanelSize = self.otherPanel.GetSize();
		scoreViewSize = self.getCtr().getUIByKey("ScoreViewCtr").GetSize();
		ruleViewSize = self.getCtr().getUIByKey("RuleViewCtr").GetSize();
		newSizeX = max(otherPanelSize.x, scoreViewSize.x, ruleViewSize.x);
		newSizeY = max(self.controlPanel.GetSize().y, self.contentPanel.GetSize().y, otherPanelSize.y, scoreViewSize.y + ruleViewSize.y);
		self.otherPanel.SetSize(newSizeX, newSizeY);

	def initOtherPanelLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		topOffset = (self.otherPanel.GetSize().y - self.getCtr().getUIByKey("ScoreViewCtr").GetSize().y - self.getCtr().getUIByKey("RuleViewCtr").GetSize().y) / 2;
		box.Add(self.getCtr().getUIByKey("ScoreViewCtr"), flag = wx.ALIGN_CENTER|wx.TOP, border = topOffset);
		box.Add(self.getCtr().getUIByKey("RuleViewCtr"), flag = wx.ALIGN_CENTER);
		self.otherPanel.SetSizer(box);

	def initViewEvents(self):
		self.getCtr().getUIByKey("SnakeViewCtr").onAddScore = self.onAddScore;

	def onAddScore(self, score):
		self.getCtr().getUIByKey("ScoreViewCtr").addScore(score);
		if self.getCtr().checkUpgradeRate(self.getCtr().getUIByKey("ScoreViewCtr").getScore()):
			self.getCtr().getUIByKey("SnakeViewCtr").upgradeRate();