from models import CV
from infer_helper import calc_possible_values_for_attribute, infer_categories_router
import numpy as np
from get_data_from_pdf_helper import reinitialize_cv


# calculate the average values based on all the pdfs (right now it takes data only from one pdf but i want to let him take average values from all the pdf in the folder progressively)
def infer_categories(cv:CV):
    # calculate all the font used and their occurrency
	font_sizes = cv.font_size_used
	# calculate the mean value (the paragraphs are the longest so above the mean there is a paragraph)
	mean = np.mean(font_sizes)
	# calculate std_dev for things longer than a title but not long enough to be a paragraph
	std_dev = np.std(font_sizes)
	# calculate candidates values
	font_possible_values = calc_possible_values_for_attribute(font_sizes, mean, std_dev)
	# after calculating the data try to guess the categories of the paragraphs
	cv = infer_categories_router(cv, font_possible_values, font_sizes)
	# reinitialize part of the cv
	cv = reinitialize_cv(cv)


def infer_attributes(cv: CV):
	return