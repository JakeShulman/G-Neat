import  math

def sqrtData(distractors = True):
	inputData = []
	targetData = []
	for x in range(2,100):
		if distractors: inputData.append([x-1,x,x+1])
		else: inputData.append([x])
		targetData.append([x-1,x,x+1])
	return inputData, targetData