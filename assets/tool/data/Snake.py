# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-12-25 10:31:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-30 17:44:05
import wx;
from enum import Enum, unique;

@unique
class Direction(Enum):
	LEFT = 0;
	TOP = 1;
	RIGHT = 2;
	BOTTOM = 3;

class Snake(object):
	"""docstring for Snake"""
	def __init__(self, params = {}):
		self.initParams(params);
		super(Snake, self).__init__();
		self.__bodyList = []; # 蛇体【0:head; -1:tail】
		self.__direction = Direction.LEFT; # 蛇移动方向
		self.init();

	def initParams(self, params):
		self.params_ = {
			"size" : (10,10),
			"bgColour" : wx.Colour(0,0,0),
			"matrix" : (36,36),
		};
		for k,v in params.items():
			self.params_[k] = v;

	def init(self):
		self.__blankIdxs = list(range(0, self.params_["matrix"][0]*self.params_["matrix"][1])); # 空白位置列表
		self.__dirtyIdxs = []; # 污染【非空白】位置列表

	def eat(self, item):
		item.SetBackgroundColour(self.params_["bgColour"]);
		item.Refresh();
		self.__bodyList.insert(0, item);
		idx = self.getIdx(item.GetPosition());
		self.removeBlankIdx(idx);

	def move(self, idx):
		self.removeBlankIdx(idx);
		pos = self.getPos(idx = idx);
		lastPos = self.moveTo(pos);
		blankIdx = self.getIdx(lastPos);
		self.addBlankIdx(blankIdx);
	
	def check(self):
		if len(self.__bodyList) > 0 and self.checkDirection(self.__direction):
			itemPos = self.__bodyList[0].GetPosition();
			itemRow, itemCol = self.getRow(itemPos), self.getCol(itemPos);
			if self.__direction == Direction.LEFT:
				itemCol-=1;
			elif self.__direction == Direction.TOP:
				itemRow-=1;
			elif self.__direction == Direction.RIGHT:
				itemCol+=1;
			elif self.__direction == Direction.BOTTOM:
				itemRow+=1;
			rows, cols = self.params_["matrix"][0], self.params_["matrix"][1];
			if itemRow >= 0 and itemRow < rows and itemCol >= 0 and itemCol < cols:
				targetIdx = itemRow*cols+itemCol;
				if targetIdx in self.__blankIdxs:
					return True, targetIdx;
		return False, -1;

	def checkDirection(self, direction):
		if direction in [Direction.LEFT, Direction.TOP, Direction.RIGHT, Direction.BOTTOM]:
			return True;
		return False;

	def getDirection(self):
		return self.__direction;

	def setDirection(self, direction):
		if self.checkDirection(direction):
			self.__direction = direction;

	def getPos(self, row = 0, col = 0, idx = -1):
		if idx >= 0:
			cols = self.params_["matrix"][1];
			row = int(idx/cols);
			col = idx % cols;
		return wx.Point(col*self.params_["size"][0], row*self.params_["size"][1]);

	def getIdx(self, pos):
		return self.getRow(pos) * self.params_["matrix"][1] + self.getCol(pos);

	def getRow(self, pos):
		return int(pos.y/self.params_["size"][1]);

	def getCol(self, pos):
		return int(pos.x/self.params_["size"][0]);

	def getBlankIdxs(self):
		return self.__blankIdxs;

	def moveTo(self, pos = None, posList = []):
		lastPos = self.__bodyList[0].GetPosition();
		if pos:
			self.__bodyList[0].Move(pos.x, pos.y);
			for i in range(1, len(self.__bodyList)):
				prePos, lastPos = lastPos, self.__bodyList[i].GetPosition();
				self.__bodyList[i].Move(prePos.x, prePos.y);
		elif len(posList) == self.getBodyLength():
			for i in range(self.getBodyLength()):
				lastPos = self.__bodyList[i].GetPosition();
				self.__bodyList[i].Move(posList[i].x, posList[i].y);
		return lastPos;

	def getBodyLength(self):
		return len(self.__bodyList);

	def getItemIdx(self, index):
		if index >= len(self.__bodyList) or index < -len(self.__bodyList):
			return -1;
		pos = self.__bodyList[index].GetPosition();
		return self.getIdx(pos);

	def getItemPos(self, index):
		if index >= len(self.__bodyList) or index < -len(self.__bodyList):
			return None;
		return self.__bodyList[index].GetPosition();

	def getPosList(self):
		posList = [];
		for item in self.__bodyList:
			posList.append(item.GetPosition());
		return posList;

	def getNextPosList(self, idx):
		posList = [];
		posList.append(self.getPos(idx = idx));
		for item in self.__bodyList:
			posList.append(item.GetPosition());
		posList.pop(); # 移除最后一个pos
		return posList;

	def addBlankIdx(self, idx):
		if not self.checkDirtyIdx(idx):
			if idx not in self.__blankIdxs:
				self.__blankIdxs.append(idx);
			else:
				raise Exception("The idx[{}] is in self.__blankIdxs".format(idx));

	def removeBlankIdx(self, idx):
		if idx in self.__blankIdxs:
			self.__blankIdxs.remove(idx);
		else:
			raise Exception("The idx[{}] is not in self.__blankIdxs".format(idx));

	def setDirtyIdx(self, idx):
		if idx not in self.__dirtyIdxs:
			self.__dirtyIdxs.append(idx);
		if idx in self.__blankIdxs:
			self.__blankIdxs.remove(idx);

	def checkDirtyIdx(self, idx):
		if idx in self.__dirtyIdxs:
			return True;
		return False;