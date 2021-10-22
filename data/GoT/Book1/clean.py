ALINEA_TAG = "ALINEA"

for chapter in range(1, 73):
    with open("./Chapters/chapter_" + str(chapter) + ".txt") as file:
        with open("./Chapter_copies/chapter_" + str(chapter) + "_copy.txt", 'w') as file2:
            for line in file.read().split('\n'):
                if line != "":
                    file2.write(line + ' ')
                    file2.write(ALINEA_TAG + '\n')
