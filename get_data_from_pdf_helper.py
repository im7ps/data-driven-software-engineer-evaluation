from models import CV, CV_Paragraphs, CV_Data

def update_avg(cv, cv_data):
	avg = cv.average_values
	if (avg.words_num == 0):
		avg.words_num = cv_data.words_num
	avg.words_num = (avg.words_num + cv_data.words_num) / 2
	avg.font_size[cv_data.font_size] += cv_data.words_num
	avg.font_color[cv_data.font_color] += cv_data.words_num
	return cv


def reinitialize_cv_data(cv_data):
	cv_data.text = ""
	cv_data.char_num = 0
	cv_data.words_num = 0
	return cv_data
	

def update_cv_data(cv_data, span):
	cv_data.text += span['text'] + '\n'
	cv_data.char_num += len(span['text'].replace(" ", ""))
	cv_data.words_num += span['text'].count(" ") + 1
	cv_data.font_size = span['size']
	cv_data.font_color = span['color']
	cv_data.position_x_start = span['bbox'][0]
	cv_data.position_x_finish = span['bbox'][2]
	cv_data.position_y_start = span['bbox'][1]
	cv_data.position_y_finish = span['bbox'][3]
	return cv_data
 

def add_node(cv:CV, cv_data:CV_Data):
	nodo = CV_Paragraphs(cv_data.text, cv_data.char_num, cv_data.words_num, cv_data.font_size, cv_data.font_color, cv_data.position_x_start, cv_data.position_x_finish, cv_data.position_y_start, cv_data.position_y_finish)
	cv.append(nodo)
    

def update_cv(cv:CV, cv_data:CV_Data):
	cv.words_num += cv_data.words_num
	cv.font_size_used[cv_data.font_size] += 1
	cv.font_color_used[cv_data.font_color] += 1
	return cv