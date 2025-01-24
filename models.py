from collections import defaultdict
from typing import Dict

class AverageValues:
	def __init__(self):
		self.words_num = 0
		# negli average utilizzerò solo l'esistenza dei font, non mi serve sapere quanti sono di un determinato font, posso usare il numero delle parole per filtrare
		self.font_size = defaultdict(int)
		self.font_color = defaultdict(int)
		

class CV_Paragraphs:
	def __init__(self, text, char_num, words_num, font_size, font_color, position_x_start, position_x_finish, position_y_start, position_y_finish):
		self.text = text
		self.char_num = char_num
		self.words_num = words_num
		self.font_size = font_size
		self.font_color = font_color
		self.position_x_start = position_x_start
		self.position_x_finish = position_x_finish
		self.position_y_start = position_y_start
		self.position_y_finish = position_y_finish
		self.category = None

class CV:
	def __init__(self):
		self.cv_instance = []
		self.words_num = 0
		self.font_size_used: Dict[str, int] = defaultdict(int)
		self.font_color_used: Dict[str, int] = defaultdict(int)
		self.average_values = AverageValues()
		self.cv_data = CV_Data()

	def append(self, node: CV_Paragraphs):
		self.cv_instance.append(node)

class CV_Data:
	def __init__(self):
		self.text = ""
		self.char_num = 0
		self.words_num = 0
		self.font_size = None
		self.font_color = None
		self.position_x_start = None
		self.position_x_finish = None
		self.position_y_start = None
		self.position_y_finish = None
		self.prev_font_size = None
