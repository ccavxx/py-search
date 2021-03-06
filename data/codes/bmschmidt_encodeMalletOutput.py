import gzip
input = gzip.open("topic-state.gz")
thisDoc = -1counts = dict()
#The first three lines aren't useful for us.input.readline()input.readline()input.readline()

"""To save space, we write the long version to stdout, but the compact (just doc-topic assignments) version to disk in the file "topicAssignments.txt""""
topicAssignments = open("topicAssignments.txt","w")
def return_lookup_keys():    docids = dict() for line in open("compostion.txt"): try:            splat = line.split("\t")            docids[splat[0]] = splat[1] except IndexError: pass return docids
def printOutBook(counts,thisDoc):    topics = dict() for token in counts.keys(): for topic in counts[token].keys(): try:                topics[topic] += counts[token][topic] except KeyError:                topics[topic] = counts[token][topic] print "\t".join([thisDoc,token,topic,str(counts[token][topic])]) for topic in topics.keys():        topicAssignments.write("\t".join([thisDoc,topic,str(topics[topic])]) + "\n")

docids = return_lookup_keys()
for line in input:    line = line.rstrip("\n")    lookups = dict()    line = line.split(" ") try:        doc = docids[line[0]] except KeyError: print "docid " + line[0] + " not in lookups: moving on..." continue
    token = line[4]    topic = line[5]
 if doc != thisDoc:        printOutBook(counts,thisDoc)
        thisDoc = doc        counts = dict()  try:        counts[token][topic] += 1 except KeyError: try:            counts[token][topic] = 1 except KeyError:            counts[token] = dict()            counts[token][topic] = 1
#And once for the last documenttry:    printOutBook(counts,thisDoc)except: #It seems to work fine with the blank last line, but just in case. pass 