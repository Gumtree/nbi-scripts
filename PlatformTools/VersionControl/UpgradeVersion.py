# Script control setup area
# script info
__script__.title = '<Script Template>'
__script__.version = '1.0'

# Use below example to create parameters.
# The type can be string, int, float, bool, file.
root_path = Par('file', '')
root_path.dtype = 'folder'
filenames = Par('str', 'MANIFEST.MF,feature.xml,pom.xml')
old_string = Par('str', '1.8.0.qualifier,1.8.0.qualifier,1.8.0-SNAPSHOT')
new_string = Par('str', '1.9.0.qualifier,1.9.0.qualifier,1.9.0-SNAPSHOT')

# Use below example to create a button
act1 = Act('act1_changed()', 'Change All') 
def act1_changed():
    if root_path.value == None or root_path.value.strip() == '':
        print 'please browse to a folder first'
        return
    print 'looking for files'
    root = str(root_path.value)
    arg = [filenames.value.split(','), old_string.value.split(','), new_string.value.split(',')]
    os.path.walk(root, myvisit, arg)
#    fns = str(filenames.value).split(',')
#    for fn in fns:
        

def myvisit(arg, dir, files):
    for file in files:
        fns = arg[0]
        for i in xrange(len(fns)):
            if file == fns[i]:
                fname = str(dir + '/' + fns[i])
                change_file(fname, arg[1][i], arg[2][i])
                
def change_file(filename, old_str, new_str):
    print 'change file ', filename
    fin = open(filename, 'r')
    text = fin.read()
    fin.close()
    text = text.replace(str(old_str), str(new_str), 1)
    fout = open(filename, 'w')
    fout.write(text)
    fout.close()

# Use below example to create a new Plot
# Plot4 = Plot(title = 'new plot')

# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    
    # check if a list of file names has been given
    if (fns is None or len(fns) == 0) :
        print 'no input datasets'
    else :
        for fn in fns:
            # load dataset with each file name
            ds = df[fn]
            print ds.shape
    print arg1_name.value
    
def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
