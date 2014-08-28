# Script control setup area
# script info
__script__.title = 'Repair Broken File'
__script__.version = ''

# Use below example to create parameters.
# The type can be string, int, float, bool, file.


# Use below example to create a button
act1 = Act('repair()', 'Click to Repair Selected Files') 
def repair():
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
    
    for dinfo in dss:
        loc = dinfo.getLocation()
        ds = df[str(loc)]
        sx = ds.sx
        cmp = sx > 1e6
        gid = 0
        for i in xrange(len(cmp)):
            if not cmp[i]:
                gid = i
                break
        meta = harvest_metadata(ds)
        for i in xrange(len(cmp)):
            if cmp[i]:
                ds[i] = 0
                for key in meta.keys():
                    item = meta[key]
#                    if item.dtype is float:
                    try:
                        item[i] = item[gid]
                    except:
                        pass
        savepath = path + '/' + ('KWR%07d' % ds.id) + '_fix.hdf'
        ds.save_copy(str(savepath))
        print 'Fixed file saved to ' + savepath
            
                
            

def harvest_metadata(ds):
    meta = dict()
    if hasattr(ds, '__iDictionary__') :
        keys = ds.__iDictionary__.getAllKeys().toArray()
        for key in keys :
            item = ds.__iNXroot__.findDataItem(key.getName())
            if item:
                meta[key.getName()] = SimpleData(item)
        items = ds.__iNXroot__.getDataItemList()
        for item in items :
            name = str(item.getShortName())
            meta[name] = SimpleData(item)
    return meta
# Use below example to create a new Plot
# Plot4 = Plot(title = 'new plot')

# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    pass
    
def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
