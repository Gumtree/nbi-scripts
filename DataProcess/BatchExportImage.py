from au.gov.ansto.bragg.nbi.ui.image import ChartImage
from org.gumtree.vis.nexus.utils import NXFactory
from org.gumtree.vis.hist2d.color import ColorScale as color_scale
import math
from Internal import lib


# Script control setup area
# script info
__script__.title = '<Script Template>'
__script__.version = '1.0'
__script__.numColumns = 2
SAVED_EFFICIENCY_FILENAME_PRFN = 'kowari.savedEfficiency'

# Use below example to create parameters.
# The type can be string, int, float, bool, file.

__image_width__ = 600
__image_height__ = 520

HPLOT = ChartImage(__image_width__, __image_height__)

# Use below example to create a button
prog_bar = Par('progress', 0)
prog_bar.colspan = 2
eff_map = Par('file', '')
d_map = get_prof_value(SAVED_EFFICIENCY_FILENAME_PRFN)
if not d_map is None and d_map.strip() != '':
    eff_map.value = d_map
eff_map.title = 'efficiency map file'
par_eff = Par('bool', True)
par_eff.title = "enable efficiency correction"
sp = Par('space', '')
par_geo = Par('bool', True)
par_geo.title = "enable geometry correction"
par_type = Par('string', 'PNG', options = ['JPG', 'PNG'])
par_type.title = 'image format'
act1 = Act('export_images()', 'Batch Export Images')
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
            if ds.ndim <= 3:
                log('dimension of ' + str(ds.id) + ' is not supported')
            dname = ds.name
            if ds.ndim == 4:
                ds = ds.get_reduced(1)
            if par_eff.value and eff_map.value != None \
                and len(eff_map.value.strip()) > 0:
                log('running efficiency correction')
                map = lib.make_eff_map(df, str(eff_map.value))
                ds = lib.eff_corr(ds, map)
            if par_geo.value :
                log('running geometry correction')
                ds = lib.geo_corr(ds, par_geo.value)
            log('process ' + dname)
            idx = dname.find('.')
            if idx > 0:
                fn = dname[0:idx]
            fn = path + '/' + fn
            wt = int(math.log10(len(ds))) + 1
            for i in xrange(len(ds)):
                log('\t frame ' + str(i))
                if ds.ndim == 4:
                    sl = ds[i, 0]
                elif ds.ndim == 3:
                    sl = ds[i]
                elif ds.ndim == 2:
                    sl = ds
                else:
                    log('dimensions are not allowed for ' + dname)
                    break
                pds = NXFactory.createHist2DDataset(sl.__iNXDataset__)
                HPLOT.setDataset(pds)
                HPLOT.getChart().setTitle(str(dname) + '_' + str(i))
                ext = (('%0' + str(wt) + 'd.' + str(par_type.value)) % i)
                try:
                    HPLOT.getXYPlot().getRenderer().getPaintScale().setColorScale(color_scale.Rainbow)
                except:
                    pass
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
