from helper_functions import is_number, is_date
from models import CV
import numpy as np

def infer_categories(cv:CV):
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
	return None

def infer_attributes(cv: CV):
	return