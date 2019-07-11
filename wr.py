from cnt import processSingle
from mcdnn import *

def processList(paper, section_cols, char_join):
	for i in range(len(paper)):
		section = paper[i]
		
		for j in range(len(section)):
			field = section[j]
			
			for k in range(len(field)):
				character = field[k]
				field[k] = str(readCharacter(models, character)[2])
			
			section[j] = ''.join(field)
		
		paper[i] = [char_join[i].join(section[x:x+section_cols[i]]) for x in range(0, len(section), section_cols[i])]
	paper = processList(paper, FORM_SHAPE, FIELD_JOIN)
	writeList(paper)
	return paper

def writeList(paper, show=True):
	for i in range(len(paper)):
		section = paper[i]
		
		if (i > 0) and (FORM_LABEL[i-1] == FORM_LABEL[i]): k = len(section[i-1])
		else: k = 1
		
		for j in range(len(section)):
			field = section[j]
			print(FORM_LABEL[i]+str(k)+'. '+field)
			k = k + 1

if __name__ == '__main__':
	from settings import *
	
	mean_px, std_px = loadModelVars()
	models = loadModels(n=1)

	paper = processSingle("./../images/w2.png")
	paper = processList(paper, FORM_SHAPE, FIELD_JOIN)
	writeList(paper)