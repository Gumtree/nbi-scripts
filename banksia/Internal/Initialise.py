import time
from org.gumtree.gumnix.sics.control.events import DynamicControllerListenerAdapter
from org.gumtree.gumnix.sics.control import IStateMonitorListener
from org.gumtree.gumnix.sics.io import SicsProxyListenerAdapter
from org.eclipse.swt.events import DisposeListener
from org.eclipse.swt.widgets import TypedListener
#from org.gumtree.util.messaging import EventHandler
import sys, os
sys.path.append(str(os.path.dirname(get_project_path('Internal'))))
from Internal import sicsext, HISTORY_KEY_WORDS
from Internal.sicsext import *
from au.gov.ansto.bragg.nbi.ui.scripting import ConsoleEventHandler
from org.eclipse.swt.widgets import Display
from java.lang import Runnable
from java.lang import System
from java.io import File
from time import strftime, localtime
import traceback
import socket

sics.ready = False
__script__.title = 'Initialised'
__script__.version = ''
__data_folder__ = 'Z:/sicsdata'
#__data_folder__ = 'Z:/testing/pelican'
__export_folder__ = 'W:/data/current/reports'
__buffer_log_file__ = __export_folder__
Dataset.__dicpath__ = get_absolute_path('/Internal/path_table')
System.setProperty('sics.data.path', __data_folder__)

try:
    __dispose_all__(None)
except:
    pass

fi = File(__buffer_log_file__)
if not fi.exists():
    if not fi.mkdirs():
        print 'Error: failed to make directory: ' + __buffer_log_file__
__history_log_file__ = __buffer_log_file__ + '/History.txt'
__buffer_log_file__ += '/LogFile.txt'
__buffer_logger__ = open(__buffer_log_file__, 'a')
__history_logger__ = open(__history_log_file__, 'a')

print 'Waiting for SICS connection'
while sics.getSicsController() == None:
    time.sleep(1)

time.sleep(3)

__scan_status_node__ = sics.getSicsController().findComponentController('/commands/scan/runscan/feedback/status')
__scan_variable_node__ = sics.getSicsController().findComponentController('/commands/scan/runscan/scan_variable')
__save_count_node__ = sics.getSicsController().findComponentController('/experiment/save_count')
__file_name_node__ = sics.getSicsController().findComponentController('/experiment/file_name')
__file_status_node__ = sics.getSicsController().findComponentController('/experiment/file_status')
#saveCount = int(saveCountNode.getValue().getIntData())
__cur_status__ = str(__scan_status_node__.getValue().getStringData())
__file_name__ = str(__file_name_node__.getValue().getStringData())

class __Display_Runnable__(Runnable):
    
    def __init__(self):
        pass
    
    def run(self):
        global __UI__
        global __dispose_listener__
        __UI__.addDisposeListener(__dispose_listener__)

__file_to_add__ = None
__newfile_enabled__ = True
def add_dataset():
    global __newfile_enabled__
    if not __newfile_enabled__ :
        return
    if __file_to_add__ is None:
        return
    global __DATASOURCE__
    try:
        __DATASOURCE__.addDataset(__file_to_add__, True)
    except:
        slog( 'error in adding dataset: ' + __file_to_add__ )
        

class __SaveCountListener__(DynamicControllerListenerAdapter):
    
    def __init__(self):
        self.saveCount = __save_count_node__.getValue().getIntData()
        pass
    
    def valueChanged(self, controller, newValue):
        global __file_to_add__
        newCount = int(newValue.getStringData());
        if newCount != self.saveCount:
            self.saveCount = newCount;
            if newCount != 1:
                return
            try:
                checkFile = File(__file_name_node__.getValue().getStringData());
                checkFile = File(__data_folder__ + "/" + checkFile.getName());
                __file_to_add__ = checkFile.getAbsolutePath();
                if not checkFile.exists():
                    slog( "The target file :" + __file_to_add__ + " can not be found" )
                    return
                runnable = __Display_Runnable__()
                runnable.run = add_dataset
                Display.getDefault().asyncExec(runnable)
            except: 
                slog( 'failed to add dataset ' + __file_to_add__ )
                    
__saveCountListener__ = __SaveCountListener__()
__save_count_node__.addComponentListener(__saveCountListener__)

def update_buffer_log_folder():
    global __buffer_log_file__, __export_folder__, __buffer_logger__, __history_log_file__, __history_logger__
    __buffer_log_file__ = __export_folder__
    fi = File(__buffer_log_file__)
    if not fi.exists():
        if not fi.mkdirs():
            print 'Error: failed to make directory: ' + __buffer_log_file__
    __history_log_file__ = __buffer_log_file__ + '/History.txt'
    __buffer_log_file__ += '/LogFile.txt'
    if __buffer_logger__:
        __buffer_logger__.close()
    __buffer_logger__ = open(__buffer_log_file__, 'a')
    if __history_logger__:
         __history_logger__.close()
    __history_logger__ = open(__history_log_file__, 'a')


def __run_script__(dss):
    pass


class __State_Monitor__(IStateMonitorListener):
    def __init__(self):
        pass

    def stateChanged(state, infoMessage):
        print state
        print infoMessage
        pass


def __dispose__():
    pass
#    __scan_status_node__.removeComponentListener(__statusListener__)
#    __m2_node__.removeComponentListener(__m2_listener__)
#    __s1_node__.removeComponentListener(__s1_listener__)
#    __s2_node__.removeComponentListener(__s2_listener__)
#    __a2_node__.removeComponentListener(__a2_listener__)

def __load_experiment_data__():
    basename = sicsext.getBaseFilename()
    fullname = str(System.getProperty('sics.data.path') + '/' + basename)
    df.datasets.clear()
    ds = df[fullname]
    data = ds[str(data_name.value)]
    axis = ds[str(axis_name.value)]
    if data.size > axis.size:
        data = data[:axis.size]
    ds2 = Dataset(data, axes=[axis])
    ds2.title = ds.id
    ds2.location = fullname
    Plot1.set_dataset(ds2)
    Plot1.x_label = axis_name.value
    Plot1.y_label = str(data_name.value)
    Plot1.title = str(data_name.value) + ' vs ' + axis_name.value
    Plot1.pv.getPlot().setMarkerEnabled(True)

# This function is called when pushing the Run button in the control UI.
def __std_run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    
    # check if a list of file names has been given
    if (fns is None or len(fns) == 0) :
        slog( 'no input datasets' )
    else :
        for fn in fns:
            # load dataset with each file name
            ds = Plot1.ds
            if ds != None and len(ds) > 0:
                if ds[0].location == fn:
                    return
            df.datasets.clear()
            ds = df[fn]
            dname = str(data_name.value)
            bm2 = ds[dname]
            qm = ds[str(axis_name.value)]
            ds2 = Dataset(bm2, axes=[qm])
            ds2.title = ds.id
            ds2.location = fn
            Plot1.set_dataset(ds2)
            Plot1.x_label = axis_name.value
            Plot1.y_label = dname
            Plot1.title = dname + ' vs ' + axis_name.value
            Plot1.pv.getPlot().setMarkerEnabled(True)
            peak_pos.value = float('NaN')
            fit_curve()
            
def __dataset_added__(fns = None):
    pass
    
def __std_fit_curve__():
    global Plot1
    ds = Plot1.ds
    if ds is None or len(ds) == 0:
        slog('Error: no curve to fit in Plot1.')
        return
    for d in ds:
        if d.title == 'fitting':
            Plot1.remove_dataset(d)
    d0 = ds[0]
    try:
        fitting = Fitting(GAUSSIAN_FITTING)
        fitting.set_histogram(d0)
        res = fitting.fit()
        res.var[:] = 0
        res.title = 'fitting'
        Plot1.add_dataset(res)
        slog(str(fitting.params))
        mean = fitting.mean
        slog('POS_OF_PEAK=' + str(mean))
        slog('FWHM=' + str(2.35482 * math.fabs(fitting.params['sigma'])))
        peak_pos.value = mean
    except:
        slog('failed to fit with Gaussian curve.')
        return

def previous_step():
    load_script(previous_file)

def next_step():
    load_script(next_file)

def logBook(text):
    global __buffer_logger__
    global __history_logger__
    try:
        tsmp = strftime("[%Y-%m-%d %H:%M:%S]", localtime())
        __buffer_logger__.write(tsmp + ' ' + text + '\n')
        __buffer_logger__.flush()
        for item in HISTORY_KEY_WORDS:
            if text.startswith(item):
                __history_logger__.write(tsmp + ' ' + text + '\n')
                __history_logger__.flush()
    except:
        traceback.print_exc(file=sys.stdout)
        print 'failed to log'
    
def slog(text):
    logln(text + '\n')
    logBook(text)


class __Dispose_Listener__(DisposeListener):
    
    def __init__(self):
        pass
    
    def widgetDisposed(self, event):
        pass
    
def __dispose_all__(event):
    global __save_count_node__
    global __saveCountListener__
    __save_count_node__.removeComponentListener(__saveCountListener__)
    if __buffer_logger__:
        __buffer_logger__.close()
    if __history_logger__:
         __history_logger__.close()
    

__dispose_listener__ = __Dispose_Listener__()
__dispose_listener__.widgetDisposed = __dispose_all__


__display_run__ = __Display_Runnable__()
Display.getDefault().asyncExec(__display_run__)

sics.ready = True

