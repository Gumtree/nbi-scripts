# Script control setup area
# script info
__script__.title = '<Script Template>'
__script__.version = '1.0'

FILE_NAME = 'path_table'
# Use below example to create parameters.
# The type can be string, int, float, bool, file.
arg1_name = Par('string', FILE_NAME)
arg1_name.title = 'filename exported to:'

# Use below example to create a button
act1 = Act('act1_changed()', 'click to export') 
def act1_changed():
    export_dict()

def export_dict():
    global FILE_NAME
    dss = __DATASOURCE__.getSelectedDatasets()
    if dss is None or len(dss) == 0:
        print 'Please select one or more files to export.'
        return
    path = selectSaveFolder()
    if path == None:
        return
    fi = File(path)
    if not fi.exists():
        if not fi.mkdir():
            print 'Error: failed to make directory: ' + path
            return
    path += '/' + FILE_NAME
    
    d0 = dss[0]
    ds=d0.getDataset()
    ds.open()
    root = ds.getRootGroup()
    entry = root.getFirstEntryAccess()
    d = dict()
    iter_group(entry, '$entry/', d)
#    print(d)
    keys = d.keys()
    keys.sort()
    with open(path, 'w') as f:
        for key in keys:
            f.write('{} = {}\n'.format(key, d[key]))
    print ('done')
    
def iter_group(g, path, d):
    gn = g.getShortName()
    dis = g.getDataItemList()
    for di in dis:
        sn = di.getShortName()
        fn = path + sn
        if sn in d.keys():
            sn = gn + '_' + sn
            if sn in d.keys():
                print('{} already exists'.format(sn))
        d[sn] = fn
    grs = g.getGroupList()
    for gr in grs:
        iter_group(gr, path + gr.getShortName() + '/', d)
        

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
            print ds.name
    
def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
