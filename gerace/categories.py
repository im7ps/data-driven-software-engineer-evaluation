import pandas as pd

def is_date(text):
	months = [
		"January", "February", "March", "April", "May", "June",
		"July", "August", "September", "October", "November", "December"
	]
 
	for month in months:
		if month in text:
			return True
		
	checks = {"day":False, "month":False, "year":False}
	days = [f"{i:02d}" for i in range(1, 32)]
	days.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
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



def is_paragraph(words_num, average_words_num):
	if (words_num > average_words_num):
		return True
	return False


def is_contacts(data, value):
	if (data.count(value) == 1): # font unico + posizione alta della pagina
		return True
	return False
