import fitz
from models import CV, CV_Data
from get_data_from_pdf_helper import *


def analyze_line(span, cv:CV):
	cv_data = cv.cv_data

	if (span['text'] and span['size'] and span['color'] and span['bbox']):
		# print(span["text"][len(span["text"]) - 2]) idea, usare i punti + spazio bianco come delimitatori di paragrafo per documenti tutti con lo stesso font				
		if (cv_data.prev_font_size != span['size'] and cv_data.prev_font_size != None):
			# clean text
			cv_data.text = cv_data.text[:-1] #per eliminare l'ultimo '\n'
			# create and append node
			add_node(cv, cv_data)
			# update general cv
			cv = update_cv(cv, cv_data)
			# update average values
			cv = update_avg(cv, cv_data)
			# prepare for new iteration
			cv_data = reinitialize_cv_data(cv_data)

		# add information
		cv_data = update_cv_data(cv_data, span)
		# update escape var
		cv_data.prev_font_size = span['size']
	return cv_data



def get_cv_data(cv:CV, path:str) -> list:
	cv_data = cv.cv_data
	cv_data.prev_font_size = None
	try:
		doc = fitz.open(path)
	except Exception as e:
		print(f"Error opening the file with PyMuPDF library: {e}")
		return

	try:
		for page in doc:
			try: 
				blocks = page.get_text("dict")["blocks"]
			except Exception as e:
				print(f"Error during the information extraction: {e}")
				continue
			for block in blocks:
				if 'lines' in block:
					for line in block["lines"]:
						for span in line["spans"]:
							cv_data = analyze_line(span, cv)

		add_node(cv, cv_data)
		update_cv(cv, cv_data)
	except Exception as e:
		print(f"Error during page elaboration: {e}")
		return
	finally:
		doc.close()
		return cv


