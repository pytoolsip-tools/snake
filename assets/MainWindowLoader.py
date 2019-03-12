# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-10-08 20:56:43
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-30 18:00:49

import wx;
from _Global import _GG;
from _Global import isExist_G;
from function.base import *;
from ProjectConfig import ProjectConfig;

class MainApp(wx.App):
	"""docstring for MainApp"""
	def __init__(self):
		super(MainApp, self).__init__(ProjectConfig["isOpenLogWin"]);

	def OnExit(self):
		_GG("TimerManager").clearAllTimer(); # 清除所有定时器
		return 1;

class MainWindow(wx.MDIChildFrame):
	"""docstring for MainWindow"""
	def __init__(self, parent, id = -1, title = "", pos = (0,0), size = (0,0), style = wx.DEFAULT_FRAME_STYLE):
		super(MainWindow, self).__init__(parent, id, title = title, pos = pos, size = size, style = style);
		self.className_ = MainWindow.__name__;
		self.__CtrMap = {}; # 所创建的控制器
		self.Bind(wx.EVT_CLOSE, self.onClose)

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.delCtrMap(); # 銷毀控制器列表

	def onClose(self, event = None):
		_GG("TimerManager").clearAllTimer(); # 清除所有定时器
		# self.Close();

	def delCtrMap(self):
		for key in self.__CtrMap:
			DelCtr(self.__CtrMap[key]);
		self.__CtrMap.clear();

	"""
		key : 索引所创建控制类的key值
		path : 所创建控制类的路径
		parent : 所创建控制类的UI的父节点，默认为本UI
		params : 扩展参数
	"""
	def createCtrByKey(self, key, path, parent = None, params = {}):
		if not parent:
			parent = self;
		self.__CtrMap[key] = CreateCtr(path, parent, params = params);

	def getCtrByKey(self, key):
		return self.__CtrMap.get(key, None);


class MainWindowLoader(object):
	def __init__(self):
		super(MainWindowLoader, self).__init__();
		self.className_ = MainWindowLoader.__name__;
		self.curPath = os.path.dirname(os.path.realpath(__file__));
		self.MainApp = MainApp();
		self.toolWinSizeEventDict = {}; # 窗口大小事件字典
		self.registerEvent(); # 注册事件

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		if isExist_G(): # window加载类中的析构函数，涉及到全局变量时，要判断全局变量是否存在
			self.unregisterEvent(); # 注销事件

	def initWindowEvent(self):
		self.initKeyDownEvent(); # 初始化按下按键事件
		pass;

	def createWindows(self):
		self.createParentWindowCtr();
		self.createMainWindowCtr();
		pass;

	def createParentWindowCtr(self):
		self.parentWindowUI = wx.MDIParentFrame(None, -1, title = ProjectConfig["name"], size = ProjectConfig["winSize"], style = wx.DEFAULT_FRAME_STYLE|wx.FRAME_NO_WINDOW_MENU); # 加载并获取UI
		self.parentWindowUI.Bind(wx.EVT_SIZE, self.onParentWinSize);
		self.parentWindowUI.ClientWindow.Bind(wx.EVT_SIZE, self.onClientWinSize);
		self.PreWinUISize = self.parentWindowUI.Size; # 初始化self.PreWinUISize
		self.parentWindowUI.ClientWindow.Size = self.parentWindowUI.Size; # 重置self.parentWindowUI.ClientWindow.Size
		
	def createMainWindowCtr(self):
		self.MainWindowUI = MainWindow(self.parentWindowUI, -1, title = "", pos = (0,0), size = self.parentWindowUI.ClientWindow.Size, style = wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.CAPTION));
		self.MainWindowUI.Bind(wx.EVT_SIZE, self.onToolWinSize);
	
	# 初始化窗口对象的公有函数
	def initWindowMethods(self):
		_GG("WindowObject").GetToolWinSize = self.getToolWinSize; # 设置获取工具窗口大小的函数
		_GG("WindowObject").BindEventToToolWinSize = self.bindEventToToolWinSize; # 绑定工具窗口大小变化事件
		_GG("WindowObject").UnbindEventToToolWinSize = self.unbindEventToToolWinSize; # 解绑工具窗口大小变化事件
		_GG("WindowObject").GetMainWindowCenterPoint = self.getMainWindowCenterPoint; # 获取主窗口的中心点

	def getToolWinSize(self):
		mainWinSize = self.MainWindowUI.GetClientSize();
		return wx.Size(mainWinSize.x - 18, mainWinSize.y - 44);

	def onParentWinSize(self, event):
		self.parentWindowUI.ClientWindow.Size = self.parentWindowUI.Size;
		
	def onClientWinSize(self, event):
		preWinUISize = self.PreWinUISize;
		curSize = self.parentWindowUI.GetSize();
		# 重置PreWinUISize
		self.PreWinUISize = curSize;
		# 重置MainWindowUI Size
		if hasattr(self, "MainWindowUI"):
			self.MainWindowUI.SetSize(self.MainWindowUI.Size[0] + curSize[0] - preWinUISize[0], self.MainWindowUI.Size[1] + curSize[1] - preWinUISize[1]);	

	def initKeyDownEvent(self):
		self.MainApp.Bind(wx.EVT_CHAR_HOOK, _GG("HotKeyManager").dispatchEvent);

	def registerEvent(self):
		_GG("EventDispatcher").register(_GG("EVENT_ID").RESTART_APP_EVENT, self, "restartApp");

	def unregisterEvent(self):
		_GG("EventDispatcher").unregister(_GG("EVENT_ID").RESTART_APP_EVENT, self, "restartApp");

	def restartApp(self, data):
		self.MainApp.ExitMainLoop(); # 退出App的主循环
		if sys.platform == "win32":
			if ProjectConfig["isOpenLogWin"] :
				os.system('start ..\\run\\run.bat'); # 启动app【有日志窗口】
			else :
				os.system('cd ..\\run\\&&run.vbs'); # 启动app【无日志窗口】

	def runWindows(self):
		self.parentWindowUI.Tile();
		self.parentWindowUI.Centre();
		self.parentWindowUI.Show(True);
		self.MainApp.MainLoop();

	def bindEventToToolWinSize(self, obj, func):
		if callable(func):
			objId = id(obj);
			if objId not in self.toolWinSizeEventDict:
				self.toolWinSizeEventDict[objId] = {"obj" : obj, "funcDict" : {}};
			self.toolWinSizeEventDict[objId]["funcDict"][id(func)] = func;

	def unbindEventToToolWinSize(self, obj, func = None):
		objId = id(obj);
		if objId in self.toolWinSizeEventDict:
			if not func:
				self.toolWinSizeEventDict.pop(objId);
			elif callable(func):
				funcId = id(func);
				if funcId in self.toolWinSizeEventDict[objId]["funcDict"]:
					self.toolWinSizeEventDict[objId]["funcDict"].pop(funcId);

	def onToolWinSize(self, event):
		if not hasattr(self, "OriToolUISize"):
			self.OriToolUISize = self.MainWindowUI.GetSize();
			self.PreToolUISize = self.MainWindowUI.GetSize();
		curToolUISize = self.MainWindowUI.GetSize();
		sizeInfo = {
			"oriDiff" : curToolUISize - self.OriToolUISize,
			"preDiff" : curToolUISize - self.PreToolUISize,
		}
		for objId in self.toolWinSizeEventDict:
			if self.toolWinSizeEventDict[objId]["obj"]:
				for funcId in self.toolWinSizeEventDict[objId]["funcDict"]:
					self.toolWinSizeEventDict[objId]["funcDict"][funcId](sizeInfo, event = event);
		# 重置PreToolUISize
		self.PreToolUISize = curToolUISize;

	def getMainWindowCenterPoint(self, isToScreen = True):
		pos = self.MainWindowUI.GetPosition();
		if isToScreen == True:
			pos = self.MainWindowUI.ClientToScreen(pos);
		return wx.Point(pos[0] + self.MainWindowUI.GetSize().x/2, pos[1] + self.MainWindowUI.GetSize().y/2);

	def createViews(self):
		wx.CallLater(500, self.onCreateViews);

	def onCreateViews(self, event = None):
		self.createMainView();

	def createMainView(self):
		self.MainWindowUI.createCtrByKey("MainViewCtr", self.curPath + "\\tool\\MainView");