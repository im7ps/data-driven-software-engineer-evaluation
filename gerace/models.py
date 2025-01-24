from collections import defaultdict
from typing import Dict

class AverageValues:
	def __init__(self):
		self.words_num = 0
		self.font_size = defaultdict(int)
		self.font_color = defaultdict(int)


class CV_Data:
	def __init__(self, text="", char_num=0, words_num=0, font_size=None, font_color=None, position_x_start=None, position_x_finish=None, position_y_start=None, position_y_finish=None, prev_font_size=None):
		self.text = text
		self.char_num = char_num
		self.words_num = words_num
		self.font_size = font_size
		self.font_color = font_color
		self.position_x_start = position_x_start
		self.position_x_finish = position_x_finish
		self.position_y_start = position_y_start
		self.position_y_finish = position_y_finish
		self.prev_font_size = prev_font_size
		self.category = None


class CV:
	def __init__(self):
		self.cv_list = []
		self.words_num = 0
		self.font_size_used = []
		self.font_color_used: Dict[str, int] = defaultdict(int)
		self.average_values = AverageValues()
		self.cv_data = CV_Data()

	def append(self, node: CV_Data):
		self.cv_list.append(node)


