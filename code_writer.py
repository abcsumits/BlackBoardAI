def writer(text,file_name):
    fo=open(file_name,"w")
    for x in text.split('\n'):
        fo.write(x)
        fo.write("\n")
    fo.close()