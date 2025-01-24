from helper_functions import process_pdfs
from models import CV

if __name__ == '__main__':
	cv = CV()
	cv = process_pdfs("./data-processing/pdfs", cv)
	for text_block in cv.cv_instance:
		print(text_block.text)
		print(text_block.category)
		print("-"*20)
