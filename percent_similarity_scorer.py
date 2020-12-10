def main():
    #Type the whole path to the file!
    fname1 = input("Enter the first filename: ")
    fname2 = input("Enter the second filename: ")

    f1 = open(f1name)
    f2 = open(f2name)
    f1_line = f1.readline()
    f2_line = f2.readline()
    count = 1
    matched = 0
    
    while (f1_line != "" or f2_line != ""):
        f1_line = f1_line.strip('\n').split('\t')
        f2_line = f2_line.strip('\n').split('\t')

        if (f1_line[0] == f2_line[0]):
            matched += 1
            print("Matched: ", f1_line[0])
        count += 1
        f1_line = f1.readline()
        f2_line = f2.readline()

    score = float(matched/count) * 100
    print("Score: ", score, "%")
    
        
    f1.close()
    f2.close()
main()
