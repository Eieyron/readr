import cnfg

from cnt import process_single
from mcdnn import *

def process_image_list(paper, section_cols, char_join):
	for i in range(len(paper)):
		section = paper[i]
		
		for j in range(len(section)):
			field = section[j]
			
			for k in range(len(field)):
				character = field[k]
				field[k] = str(read_character(models, character)[2])
			
			section[j] = ''.join(field)
		
		paper[i] = [char_join[i].join(filter(None, section[x:x+section_cols[i]])) for x in range(0, len(section), section_cols[i])]

	return paper

def print_list(paper, show=True):
	for i in range(len(paper)):
		section = paper[i]

		k = cnfg.number_offset[i]
		for j in range(len(section)):
			field = section[j]
			print(cnfg.form_labels[i]+str(k)+'. '+field)
			k = k + 1

if __name__ == '__main__':	
	mean_px, std_px = load_model_vars()
	models = load_models(n=1)

	paper = process_single("./../images/w2.png")
	paper = process_image_list(paper, cnfg.form_shape, cnfg.field_join)
	print_list(paper)