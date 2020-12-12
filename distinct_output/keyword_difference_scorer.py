def main():
    f1 = open("bagofwords_output/bagofwords_dem_lemma.txt")
    f2 = open("bagofwords_output/bagofwords_rep_lemma.txt")

    output1 = open("distinctly_dem.txt", 'w')
    output2 = open("distinctly_rep.txt", 'w')

    output1.write("DISTINCT DEMOCRATIC KEYWORDS\n")
    f1_line = f1.readlines()
    f2_line = f2.readlines()
    for line in f1_line:
        line = line.strip('\n').split('\t')
        word = line[0]
        frequency = int(line[1])
        difference = 0
        found = 0
        for f2line in f2_line:
            f2line = f2line.strip('\n').split('\t')
            f2word = f2line[0]
            f2frequency = int(f2line[1])
            if (word == f2word):
                found = 1
                if (frequency//5 > f2frequency):
                    difference = abs(frequency - f2frequency)
                    output1.write("Keyword: " + word + ", difference: " + str(difference) + "\n")
        if (found == 0 and frequency > 100):
            output1.write("Keyword: " + word + ", frequency: " + str(frequency) + "\n")

    output2.write("DISTINCT REPUBLICAN KEYWORDS\n")
    for line in f2_line:
        line = line.strip('\n').split('\t')
        word = line[0]
        frequency = int(line[1])
        difference = 0
        found = 0
        for f2line in f1_line:
            f2line = f2line.strip('\n').split('\t')
            f2word = f2line[0]
            f2frequency = int(f2line[1])
            if (word == f2word):
                found = 1
                if (frequency//5 > f2frequency):
                    difference = abs(frequency - f2frequency)
                    output2.write("Keyword: "+ word + ", difference: " + str(difference) + "\n")
        if (found == 0 and frequency > 100):
            output2.write("Keyword: " + word + ", frequency: " + str(frequency) + "\n")

    f1.close()
    f2.close()
    output1.close()
    output2.close()
main()
