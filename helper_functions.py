import pandas as pd
import os
from models import CV


def is_date(text):
	months = [
		"January", "February", "March", "April", "May", "June",
		"July", "August", "September", "October", "November", "December"
	]
 
	for month in months:
		if month in text:
			return True

	datetime = pd.to_datetime(text.replace(',', ' '), errors='coerce')
	if datetime == datetime:
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


def is_number(string:str):
	try:
		int(string)
		return True
	except ValueError:
		return False


def process_pdfs(folder_path, cv:CV):
	from get_data_from_pdf import get_cv_data
	from router import cv_router
	try:
		files = os.listdir(folder_path)
	except Exception as e:
		print(f"Error accessing the folder {folder_path}: {e}")
		return

	if not files:
		print("Folder is empty.")
		return

	for filename in files:
		if filename.endswith(".pdf"):
			file_path = os.path.join(folder_path, filename)
			try:
				cv = get_cv_data(cv, file_path)
				cv_router(cv)
			except Exception as e:
				print(f"Error handling CV: {e}")
		else:
			print("CV must be in pdf format.")
			continue
	return cv
