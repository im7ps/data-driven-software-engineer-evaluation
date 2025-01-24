from models import CV
from process_pdfs import process_pdfs

"""
	i did not divide the list for every single cv, my bad. (this is a mega list with all the sections from all the pdfs)

	returns a CV object.
	inside the CV object there is the cv_list, a list of sections from all the pdfs.
	each section has it's own data like text, number of words etc
	you can access to that data with dot notation.	
""" 


def main():
	data = CV()
	data = process_pdfs("../data-processing/pdfs", data)

	# for cv in data.cv_list:
	# 	print(cv.text)


if __name__ == "__main__":
    main()
