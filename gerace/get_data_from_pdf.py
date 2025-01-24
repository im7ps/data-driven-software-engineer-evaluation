import fitz
from models import CV
from get_data_from_pdf_helper import *

# returns a class CV_Data with all the information stored inside
def analyze_line(span, cv:CV) -> CV_Data:
	cv_data = cv.cv_data

	try:
		if (span['text'] and span['size'] and span['color'] and span['bbox']):
			if (cv_data.prev_font_size != span['size'] and cv_data.prev_font_size != None):
				# clean text from the last '\n'
				cv_data.text = cv_data.text[:-1]
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
	except Exception as e:
		print(f"text block is corrupted or invalid: {e}")
		return CV_Data()
	finally:
		return cv_data

# first it tries to open the pdf with an external library then if everything is good calls analyze_line that extracts the data
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
						if line:
							for span in line["spans"]:
								if span:
									cv_data = analyze_line(span, cv)

		add_node(cv, cv_data)
		update_cv(cv, cv_data)

	except Exception as e:
		print(f"Error during page elaboration: {e}")
		return
	finally:
		doc.close()
		return cv


