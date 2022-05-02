ngrams = {}

def readText(filename):
    file = open(filename, encoding="utf8")
    content = file.read()
    file.close()
    return content

def formatText(text):
    remove = [",", "'", '"', ":","，","：",",","•","、"]
    for char in remove:
        text = text.replace(char, "")

    split = [".", "。", " "]
    for char in split:
        text = text.replace(char, "\n")

    while "\n\n" in text:
        text = text.replace("\n\n", "\n")

    text = text.lower()
    text = text.split("\n")
    return text

def getNGrams(strings):
    for string in strings:
        getNGram(string)

def getNGram(string):
    for i in range(len(string)):
        if string[0:i+1] in ngrams.keys():
            ngrams.update({string[0:i+1]: ngrams.get(string[0:i+1])+1})
        else:
            ngrams.update({string[0:i + 1]: 1})
    if len(string) > 0:
        return getNGram(string[1:])
    else:
        return

def filterNGrams(list):
    refined = []
    for item in list:
        if item[1] > 1:
            refined.append(item)

    refined.sort(key=e, reverse=True)

    kill = []
    n = 0
    while n < len(refined):
        point = refined[n][1]
        group = []
        while refined[n][1] == point:
            #print(point)
            group.append([refined[n][0], n])
            n += 1

            if n >= len(refined):
                break

        #print(group)

        while len(group) > 1:
            for item in group:
                #print(item[0]+" "+group[0][0])
                if group[0][0] != item[0]:
                    if item[0] in group[0][0] and group[0][0] != item[0]:
                        #print("kill: "+item[0] + " for " + group[0][0])
                        kill.append(item[1])
                    elif group[0][0] in item[0]:
                        #print("kill: "+group[0][0] + " for " + item[0])
                        kill.append(group[0][1])
            group.pop(0)

    #print(refined)

    for index in kill:
        refined[index] = None

    i = 0
    while i < len(refined):
        if refined[i] == None:
            refined.pop(i)
        else:
            i+=1


    #print(refined)

    return refined

def createCSV(list, filename):
    output = open(filename, "w", encoding="utf8")
    for item in list:
        output.write(item[0]+","+str(item[1])+"\n")
    output.close()

def e(x):
    return x[1]

if __name__ == "__main__":
    text = readText("message.txt")
    text = formatText(text)
    getNGrams(text)
    ngramList = ngrams.items()
    ngramList = filterNGrams(list(ngramList))

    createCSV(ngramList, "output.csv")