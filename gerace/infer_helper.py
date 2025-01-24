from categories import is_date, is_paragraph, is_contacts


def calc_possible_values_for_attribute(data, mean, std_dev):
	lower_bound = mean - std_dev
	higher_bound = mean + std_dev
	possibilities = [size for size in data if lower_bound < size < higher_bound]
	return possibilities


# adding the consideration of the spacial position of the objects we can infer more precisely:
# contacts: it's most likely in the upper part of the document
# signature: lower part of the pdf
# personal photo: upper part of the pdf

# and so on, even with the color:
# a paragraph is not red, imagine a pdf all red
# brighter colours are for paragraphs title

def infer_categories_router(cv, font_possible_values, font_sizes):
	prev_node = None
	for node in cv.cv_list:
		if is_paragraph(node.words_num, cv.average_values.words_num):
			node.category = "paragraph"
		else:
			node.category = "title"

		if node.category == "paragraph":
			if is_contacts(font_sizes, node.font_size):
				node.category = "contacts"
				continue

			if prev_node.category == "title" and node.font_size in font_possible_values:
				prev_node.category = "paragraph title"
				continue

		if node.category == "title":
			if node.text.isdigit() and node.words_num == 1:
				node.category = "page number"
				continue

			if is_date(node.text):
				node.category = "birthday"
				continue
		prev_node = node
	return cv
