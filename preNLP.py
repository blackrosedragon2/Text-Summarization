from os import listdir
import string
from pickle import dump	


def loadDoc(filename):
	file = open(filename,encoding='utf-8')
	text = file.read()
	file.close()
	return text 

def loadStories(directory):
	allStories = []
	for name in listdir(directory):
		filename = directory + '/' + name
		doc = loadDoc(filename)
		story , highlights = splitStory(doc)
		allStories.append({'story':story , 'highlights':highlights})
	return allStories

def splitStory(doc):
	index = doc.find('@highlight')
	story, highlights  = doc[:index],doc[index:].split('@highlight')
	highlights = [h.strip() for h in highlights if len(h)>0]
	return story,highlights

def cleanLines(lines):
	cleanLines = []
	translator = str.maketrans('','',string.punctuation)  #https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate

	for line in lines:
		index = line.find('(CNN) -- ') 
		if index > -1:
			line = line[index+len('(CNN)'):] #i not get whats wrong with this line , its not working
		line = line.split() #list of words
		line = [word.lower() for word in line]
		line = [w.translate(translator) for w in line]
		line = [word for word in line if word.isalpha()]
		cleanLines.append(' '.join(line))
	cleanLines = [c for c in cleanLines if len(c)>0]
	return cleanLines


directory = 'cnn/stories/' #for colab add root_path at the beginning
stories = loadStories(directory)

print('Total number of loaded Stories ' , len(stories) )

for tale in stories:
	tale['story'] = cleanLines(tale['story'].split('\n'))
	tale['highlights'] = cleanLines(tale['highlights'])


dump(stories,open('cleanCNN.pkl', 'wb'))





