import sys  
import csv 
import matplotlib.pyplot as plt
import numpy 

def create_bigram(data):
   listOfBigrams = []
   bigramCounts = {}
   unigramCounts = {}
   for i in range(len(data)-1):
      if i < len(data) - 1 and data[i+1].islower():

         listOfBigrams.append((data[i], data[i + 1]))

         if (data[i], data[i+1]) in bigramCounts:
            bigramCounts[(data[i], data[i + 1])] += 1
         else:
            bigramCounts[(data[i], data[i + 1])] = 1

      if data[i] in unigramCounts:
         unigramCounts[data[i]] += 1
      else:
         unigramCounts[data[i]] = 1
   return listOfBigrams, unigramCounts, bigramCounts

def print_most_frequent(listOfBigrams, num=50):
	with open("bigramFrequency.txt",'w') as f:
		for n in sorted(listOfBigrams):
			print('----- {} most common {}-grams -----'.format(num, n))
			for bigram, count in listOfBigrams[n].most_common(num):
				print("{0}: {1}".format(' '.join(bigram), count)+"\n")
				f.write("{0}: {1}".format(' '.join(bigram), count) + "\n")
	f.close()


if __name__ == '__main__':
	file = sys.argv[1]
	data_list =[]
	with open(file, newline = '') as f:
		data = csv.reader(f,delimiter='\t')
		for word in data:
			if (len(word)>1):
				data_list.append(word[0])

	listOfBigrams, unigramCounts, bigramCounts = create_bigram(data_list)
	
	
	with open("dem_full_tweets_listOfBigrams.txt",'w') as f:

		for i in listOfBigrams:
			f.write(str(i)+'\n')

	
	with open("dem_full_tweet_bigramCounts.txt",'w') as f:
	
		for k,v in sorted(bigramCounts.items(), key=lambda x: x[1], reverse=True):
			f.write("{}:{}".format(k,v)+"\n")
	f.close()
	
	
	

	print("done")
