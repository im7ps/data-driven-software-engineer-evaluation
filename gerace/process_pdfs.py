from get_data_from_pdf import get_cv_data
from router import cv_router
import os
from models import CV

# first we get the data with get_cv_data and then we try to guess the category of every paragraph or section of that cv
def process_single_pdf(pdf_path, cv:CV) -> CV:

	try:
		cv = get_cv_data(cv, pdf_path)
		if not cv:
			raise Exception(f"CV {pdf_path} not valid.")
		cv_router(cv)
  
	except Exception as e:
		print(f"Error handling CV: {e}")

	return cv


# open the folder if possible and if it finds .pdfs file starts the cicle for every pdf (here i had to create a new node for every pdf)
def process_pdfs(folder_path, cv:CV) -> CV:
	try:
		files = os.listdir(folder_path)
	except Exception as e:
		print(f"Error accessing the folder {folder_path}: {e}")
		return

	if not files:
		print("Folder is empty.")
		return

	try:
		pdf_files = [os.path.join(folder_path, filename) for filename in files if filename.endswith(".pdf")]		
		if not pdf_files:
			raise Exception("Upload a valid .pdf file")
	except Exception as e:
		print(f"Error creating pdf's files folder: {e}")


	for pdf_path in pdf_files:
		cv = process_single_pdf(pdf_path, cv)

	return cv
