import sys
import math


def scanFiles(file):
	P_WordCount = [0]*1449
	N_WordCount = [0]*1449
	P_Prior = 0;
	N_Prior = 0;
	for line in file:
		words = line.split()		
		if (words[0] == '1'):
			P_Prior += 1
			for i in range(1, len(words)):
				word, value = words[i].split(":")
				P_WordCount[int(word)] += int(value)
		else:
			N_Prior += 1
			for i in range(1, len(words)):
				word, value = words[i].split(":")
				N_WordCount[int(word)] += int(value)
	return P_Prior, N_Prior, P_WordCount, N_WordCount


def main(argv):

	P_WordCount = [0]*1449
	N_WordCount = [0]*1449
	P_Prior = 0;
	N_Prior = 0;

	trainFile = open("/home/dongchen/Documents/545/SPARSE.TRAIN").readlines()
	trainFileInput = [x.strip() for x in trainFile]

	tokenFile = open("/home/dongchen/Documents/545/TOKENS_LIST").readlines()
	tokenFileInput = [x.strip() for x in tokenFile]

	testFile = open("/home/dongchen/Documents/545/SPARSE.TEST").readlines()
	testFileInput = [x.strip() for x in testFile]

	P_Prior, N_Prior, P_WordCount, N_WordCount = scanFiles(trainFile)

	P_PriorProb = P_Prior / float(P_Prior+N_Prior)
	N_PriorProb = N_Prior / float(P_Prior+N_Prior)

	P_WordProb = [0]*1449
	N_WordProb = [0]*1449
	PN_Ratio = [0]*1449

	for i in range(1, len(tokenFileInput)+1):
		#print(i)
		P_WordProb[i] = (float)( 1 + P_WordCount[i])/(float)(sum(P_WordCount) + len(tokenFileInput))
		N_WordProb[i] = (float)( 1 + N_WordCount[i])/(float)(sum(N_WordCount) + len(tokenFileInput))
		PN_Ratio[i] = P_WordProb[i]/N_WordProb[i]
	#test

	errorCount = 0;

	for line in testFileInput:
		P_Product = math.log10(P_PriorProb)
		N_Product = math.log10(N_PriorProb)
		words = line.split()
		for i in range(1, len(words)):
			word, value = words[i].split(":")
			#print(int(word))
			#print(P_WordProb[int(word)])
			P_Product += int(value) * math.log10(P_WordProb[int(word)])
			N_Product += int(value) * math.log10(N_WordProb[int(word)])

		if (P_Product > N_Product) and (words[0]=='-1'):
			errorCount += 1

		if (P_Product < N_Product) and (words[0]=='1'):
			errorCount += 1

	print("errorRate: ")
	print(errorCount/(float)(len(testFileInput)))

#############################################################
	# part 2
	print("")
	print("5 tokens that are most indicative of the SPAM class: ")
	res = sorted(range(len(PN_Ratio)), key=lambda x: PN_Ratio[x])[-5:]
	res.reverse()
	for i in res:
		print(tokenFileInput[i-1])

if __name__ == "__main__":
	main(sys.argv)
