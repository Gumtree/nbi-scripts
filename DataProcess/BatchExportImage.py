from au.gov.ansto.bragg.nbi.ui.image import ChartImage
from org.gumtree.vis.nexus.utils import NXFactory
import math

# Script control setup area
# script info
__script__.title = '<Script Template>'
__script__.version = '1.0'

# Use below example to create parameters.
# The type can be string, int, float, bool, file.

__image_width__ = 600
__image_height__ = 520

HPLOT = ChartImage(__image_width__, __image_height__)

# Use below example to create a button
prog_bar = Par('progress', 0)
par_type = Par('string', 'JPG', options = ['JPG', 'PNG'])
par_type.title= 'Image Format'
act1 = Act('export_images()', 'Batch Export Images from Selected HDF Files') 
def export_images():
    path = selectSaveFolder()
    if path == None:
        return
    dss = __DATASOURCE__.getSelectedDatasets()
    if len(dss) == 0:
        print 'Error: please select at least one data file.'
    fi = File(path)
    if not fi.exists():
        if not fi.mkdir():
            print 'Error: failed to make directory: ' + path
            return
    dss_idx = 0
    prog_bar.max = len(dss) + 1
    try:
        for dinfo in dss:
            dss_idx += 1
            prog_bar.selection = dss_idx
            ds = df[str(dinfo.location)]
            if ds.ndim != 4:
                slog('dimension of ' + str(ds.id) + ' is not supported')
            fn = ds.name
            log('process ' + ds.name)
            idx = fn.find('.')
            if idx > 0:
                fn = fn[0:idx]
            fn = path + '/' + fn
            wt = int(math.log10(len(ds))) + 1
            for i in xrange(len(ds)):
                log('\t frame ' + str(i))
                sl = ds[i, 0]
                pds = NXFactory.createHist2DDataset(sl.__iNXDataset__)
                HPLOT.setDataset(pds)
                HPLOT.getChart().setTitle(str(ds.name) + '_' + str(i))
                ext = (('%0' + str(wt) + 'd.' + str(par_type.value)) % i)
                HPLOT.saveImage(fn + '_' + ext, str(par_type.value))
    finally:
        prog_bar.selection = 0
        prog_bar.max = 0
    log('Done')
        
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
