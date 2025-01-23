import fitz
from typing import Dict
from collections import defaultdict
import numpy as np
import pandas as pd
import datetime

class AverageValues:
	def __init__(self):
		self.words_num = 0
		# negli average utilizzerò solo l'esistenza dei font, non mi serve sapere quanti sono di un determinato font, posso usare il numero delle parole per filtrare
		self.font_size = defaultdict(int)
		self.font_color = {}
		

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
		self.average_values = AverageValues()

	def append(self, node: CV_Paragraphs):
		self.cv_instance.append(node)

def estrai_info_pdf(path) -> list:
	cv = CV()
	avg = cv.average_values
	prev_font_size = None
	text = ""
	char_num = 0
	words_num = 0
	font_size = None
	font_color = None
	position_x_start = None
	position_x_finish = None
	position_y_start = None
	position_y_finish = None

	doc = fitz.open(path)
	for page in doc:
		blocks = page.get_text("dict")["blocks"]
		for block in blocks:
			if 'lines' in block:
				for line in block["lines"]:
					for span in line["spans"]:
						# print(span["text"][len(span["text"]) - 2]) idea, usare i punti + spazio bianco come delimitatori di paragrafo per documenti tutti con lo stesso font				
						if (prev_font_size != span['size'] and prev_font_size != None):
							# clean text
							text = text[:-1] #per eliminare l'ultimo '\n'
							# create and append node
							nodo = CV_Paragraphs(text, char_num, words_num, font_size, font_color, position_x_start, position_x_finish, position_y_start, position_y_finish)
							cv.append(nodo)
							# update general cv
							cv.words_num += words_num
							cv.font_size_used[font_size] += 1
							# update average values
							if (avg.words_num == 0):
								avg.words_num = words_num
							avg.words_num = (avg.words_num + words_num) / 2
							avg.font_size[font_size] += words_num
							# prepare for new iteration
							text = ""
							char_num = 0
							words_num = 0

						# add information
						text += span['text'] + '\n'
						char_num += len(span['text'].replace(" ", ""))
						words_num += span['text'].count(" ") + 1
						font_size = span['size']
						font_color = span['color']
						position_x_start = span['bbox'][0]
						position_x_finish = span['bbox'][2]
						position_y_start = span['bbox'][1]
						position_y_finish = span['bbox'][3]
						# update escape var
						prev_font_size = span['size']
	  

	nodo = CV_Paragraphs(text, char_num, words_num, font_size, font_color, position_x_start, position_x_finish, position_y_start, position_y_finish)
	cv.append(nodo)

	cv.words_num += words_num
	cv.font_size_used[font_size] += 1

	doc.close()
	return cv


def is_number(string:str):
	try:
		int(string)
		return True
	except ValueError:
		return False

def infer_categories(cv):
	prev_node = None
	total_fonts_num = 0
	total_fonts_value = 0

	data = cv.average_values.font_size
	common_font_size = max(data, key=data.get)

	for key, value in data.items():
		total_fonts_value += (key * value)
		total_fonts_num += value

	mean = total_fonts_value / total_fonts_num


	expanded_data = []
	for value, count in data.items():
		expanded_data.extend([value] * count)
	std_dev = np.std(expanded_data)
	lower_bound = mean - std_dev
	higher_bound = mean + std_dev

	font_sizes = np.array(list(data.keys()))
	possible_paragraph_title_font_size = [size for size in font_sizes if lower_bound < size < higher_bound]

	for text_block in cv.cv_instance:
		# conta numero caratteri -> trova la percentuale rispetto al totale -> confronta questa percentuale con la media -> attribuisci categoria
		if (text_block.words_num > cv.average_values.words_num):
			text_block.category = "paragraph"
		else:
			text_block.category = "title"

		if text_block.category == "paragraph":
			if (expanded_data.count(text_block.font_size) == 1): #posizione alta della pagina
				text_block.category = "contacts"
				continue

			if prev_node.category == "title" and text_block.font_size in possible_paragraph_title_font_size:
				prev_node.category = "paragraph title"
				continue

		if text_block.category == "title":
			if is_number(text_block.text) and text_block.words_num == 1:
				text_block.category = "page number"
				continue

			if is_date(text_block.text):
				text_block.category = "birthday"
				continue
			

		prev_node = text_block

	for text_block in cv.cv_instance:
		print(text_block.text)
		print(text_block.category)
		print("-"*20)


	return None


def classic_checker(s):
    dt = pd.to_datetime(s.replace(',', ' '), errors='coerce')
    if dt == dt:
        return True
    return False

def is_date(text):
	months = [
		"January", "February", "March", "April", "May", "June",
		"July", "August", "September", "October", "November", "December"
	]
 
	for month in months:
		if month in text:
			return True

	if classic_checker(text):
		return True
		
	checks = {"day":False, "month":False, "year":False}
	days = [f"{i:02d}" for i in range(1, 32)]
	days.extend(f"{i:01d}" for i in range(1, 10))
	words = text.split()
	
	if all(word.isdigit() for word in words) and max(int(word) for word in words) > 31:
		checks["year"] = True

	day_count = 0
	for word in words:
		if word in days:
			day_count += 1
	if day_count > 2:
		checks["day"] = True

	if words[0].isdigit() and words[1].isdigit() and (0 < words[0] < 13 or 0 < words[1] < 13):
		checks["month"] = True

	if (checks["year"] == True and checks["month"] == True and checks["day"] == True):
		return True

	return False


cv = estrai_info_pdf("./data-processing/pdfs/sample-3.pdf")
infer_categories(cv)
