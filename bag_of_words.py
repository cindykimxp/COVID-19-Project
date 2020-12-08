def main():
    democrats_file = open('1.source_preprocess/corpora/party_filtered/democrat/dem_full_lemma.txt', 'r')
    read_df = democrats_file.readlines()
    demo_words = {}

    bagofwords_d = open('bagofwords_dem_lemma.txt', 'w')
    bagofwords_r = open('bagofwords_rep_lemma.txt', 'w')
    
    repub_file = open('1.source_preprocess/corpora/party_filtered/republican/rep_full_lemma.txt', 'r')
    read_rf = repub_file.readlines()
    repub_words = {}
    
    for line in read_df:
        line = line.strip('\n').split('\t')
        if (len(line) == 0 or len(line) == 1):
            continue
        word = line[0].lower()

        if (word != ""):
            if word in demo_words:
                demo_words[word] += 1
            else:
                demo_words[word] = 1

    for line in read_rf:
        line = line.strip('\n').split('\t')
        if (len(line) == 0 or len(line) > 2):
            continue
        word = line[0].lower()

        if (word != ""):
            if word in repub_words:
                repub_words[word] += 1
            else:
                repub_words[word] = 1

    demo_sorted = sorted(demo_words.items(), key=lambda x: x[1], reverse=True)
    repub_sorted = sorted(repub_words.items(), key=lambda x: x[1], reverse=True)

    for words in demo_sorted:
        bagofwords_d.write(words[0] + '\t' + str(words[1]) + '\n')
    for words in repub_sorted:
        bagofwords_r.write(words[0] + '\t' + str(words[1]) + '\n')

    democrats_file.close()
    repub_file.close()
    bagofwords_d.close()
    bagofwords_r.close()
    
    
main()
