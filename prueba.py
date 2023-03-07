import optparse

opts = optparse.OptionParser()

opts.add_option("-f", "--file", dest='fname', help="This is the file name that you would like to read")
opts.add_option("-w", "--word", dest='word', help="This is the word that you would like to search")

(options, arguments) = opts.parse_args()
print(bool(options.fname) == True)
print(options.word)