from infer import infer_categories, infer_attributes


def cv_router(cv):
	# condition:bool = False

	# font_len = len(cv.font_size_used)
	# color_len = len(cv.font_color_used)
	# size = font_len + color_len

	# match size:
	# 	case 2:
	# 		condition = font_len > color_len
	# 		sum_to_two(condition)
	# 		return
	# 	case 3:
	# 		condition = font_len > color_len
	# 		sum_to_three(condition)
	# 		return
	# 	case 4:
	# 		condition = font_len > color_len
	# 		sum_to_four(condition)
	# 		return

	# if size < 7:
	# 	infer_attributes()
	# else:
		infer_categories(cv)
	  