# Script control setup area
# script info
__script__.title = '<Script Template>'
__script__.version = '1.0'

# Use below example to create parameters.
# The type can be string, int, float, bool, file.
# Use below example to create a button
act1 = Act('split()', 'split')
act2 = Act('print "do nothing"', 'nothing')
def split():
    li = __DATASOURCE__.getSelectedDatasets()
    for item in li:
        df.datasets.clear()
        ds = df[str(item.location)]
        dc = copy(ds)
        iData = ds.__iNXdata__
        iData.removeDataItem('hmm')
        iData.removeDataItem('variance')
        iEntry = ds.__iNXroot__.getFirstEntry()
        iEntry.getGroup('instrument').getGroup('detector').removeDataItem('hmm')
        
        l = dc.shape[1]
        for i in xrange(l):
            di = dc[:, i][0]
            iItem = di.__iDataItem__
            ename = 'QKK' + ('%07d' % int(ds.id)) + '_' + str(i) \
                         + '.nx.hdf'
            iItem.setShortName('hmm_xy')
            iData.addDataItem(iItem)
            iEntry.setShortName(ename)
            rr = iEntry.getGroup('data').removeDataItem('variance')
            log('remove variance')
            log(str(rr))
            log('export to ' + ename)
            ds.save_copy(os.path.dirname(ds.location) + '/' + ename)
            break
        
    
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
