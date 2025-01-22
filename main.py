import fitz

class AverageValues:
	def __init__(self):
		self.char_num = 0
		self.words_num = 0
		self.font_size = {}
		self.font_color = {}
		
	def update(self, char_num, words_num):
		self.char_num += (self.char_num + char_num) / 2
		self.words_num += (self.words_num + words_num) / 2
		
	def get_char_num(self):
		return self.char_num
		

class Nodo:
	def __init__(self, text, char_num, words_num, font_size, font_color, position_x_start, position_x_finish, position_y_start, position_y_finish, avg_values):
		self.text = text
		self.char_num = char_num
		self.words_num = words_num
		self.font_size = font_size
		self.font_color = font_color
		self.position_x_start = position_x_start
		self.position_x_finish = position_x_finish
		self.position_y_start = position_y_start
		self.position_y_finish = position_y_finish
		
		avg_values.update(char_num, words_num)


def estrai_info_pdf(nome_file) -> list:
	data = []
	current_font_size = ""
	text = ""
	char_num = 0
	words_num = 0
	font_size = None
	font_color = None
	position_x_start = None
	position_x_finish = None
	position_y_start = None
	position_y_finish = None

	doc = fitz.open(nome_file)
	for page in doc:
		blocks = page.get_text("dict")["blocks"]
		for block in blocks:
			if 'lines' in block:
				for line in block["lines"]:
					for span in line["spans"]:
						if (current_font_size != span['size'] and current_font_size != ""):
							text = text[:-1]
							nodo = Nodo(text, char_num, words_num, font_size, font_color, position_x_start, position_x_finish, position_y_start, position_y_finish, average_values)
							data.append(nodo)
							text = ""
							char_num = 0
							words_num = 0

						if (span['text'] and span['size'] and span['bbox']):
							text += span['text'] + '\n'
							char_num += len(span['text'].replace(" ", ""))
							words_num += span['text'].count(" ") + 1
							font_size = span['size']
							font_color = span['color']
							position_x_start = span['bbox'][0]
							position_x_finish = span['bbox'][2]
							position_y_start = span['bbox'][1]
							position_y_finish = span['bbox'][3]
							current_font_size = span['size']

	doc.close()
	return data

average_values = AverageValues()
data = estrai_info_pdf("./data-processing/pdfs/sample-1.pdf")
print(data[1].text)



