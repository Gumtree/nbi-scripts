from gumpy.commons.logger import log
import pickle
import datetime
from java.text import SimpleDateFormat
import time
from time import strftime, localtime
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
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from gumpy.commons.logger import n_logger
from gumpy.lib import enum

# Script control setup area
# script info
__script__.title = 'Bilby Workflow'
__script__.version = '1.0'

sics.ready = False

#__data_folder__ = 'W:/data/current'
__data_folder__ = 'Z:/sicsdata'
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
        
#    try:
#        def remote_path(local):
#            result = local.replace('\\', '/')
#            if result[0:2] == 'W:':
#                result = "/mnt/nbi_experiment_data/bilby" + result[2:]
#            elif result[0:2] == 'V:':
#                result = "/mnt/nbi_experiment_hsdata/bilby/hsdata" + result[2:]
#                
#            return result
#        
#        hdfFile = remote_path(str(__file_to_add__))
#        
#        if len(hdfFile) < 8 or hdfFile[-7:].lower() != '.nx.hdf':
#            raise RuntimeError("unknown hdf extension")
#            
#        tarFile = hdfFile[:-7] + ".tar"
#        
#        ds = df[str(__file_to_add__)]
#
#        daqDirName = str(ds['/entry1/instrument/detector/daq_dirname'])
#        datasetNumbers = ds['/entry1/instrument/detector/dataset_number']
#        
#        if len(ds) > 1:
#            datasetNumbers = datasetNumbers[0]
#        binFile = "/mnt/nbi_experiment_hsdata/bilby/hsdata/%s/DATASET_%i/EOS.bin" % (daqDirName, int(datasetNumbers))
#
#        msg = "SRC:\"%s\",\"%s\"\r\nDST:\"%s\"\r\n" % (hdfFile, binFile, tarFile)
#        
#        host = 'ics1-bilby'
#        port = 8123
#        
#        # create TCP/IP socket
#        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        sock.connect((host, port))
#        
#        try:
#            # receive welcome message from daemon
#            welcome = sock.recv(1024)
#            if not welcome:
#                raise RuntimeError("connection broken")
#        
#            slog( str(welcome) )
#            slog( str(msg) )
#        
#            sock.send(msg)
#            response = ""
#            while True:
#                recv = sock.recv(1024)
#                if not recv:
#                    break
#                response += recv
#        
#            slog( str(response) )
#        
#        finally:
#            sock.close()
#
#    except:
##        traceback.print_exc(file=sys.stdout)
#        slog( 'failed to create tar file for ' + __file_to_add__ )

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

class BatchStatusListener(SicsProxyListenerAdapter):
    
    def __init__(self):
        pass
    
    def proxyConnected(self):
        pass

    def proxyConnectionReqested(self):
        pass

    def proxyDisconnected(self):
        pass

    def messageReceived(self, message, channelId):
        if str(channelId) == 'rawBatch':
            logBook(message)

    def messageSent(self, message, channelId):
        pass

try:
    sics.SicsCore.getSicsManager().proxy().removeProxyListener(__batch_status_listener__)
except:
    pass
__batch_status_listener__ = BatchStatusListener()
sics.SicsCore.getSicsManager().proxy().addProxyListener(__batch_status_listener__)

def __dataset_added__(fns = None):
    pass

class SICSConsoleEventHandler(ConsoleEventHandler):
    
    def __init__(self, topic):
        ConsoleEventHandler.__init__(self, topic)
    
    def handleEvent(self, event):
        data = str(event.getProperty('sentMessage'))
        logBook(data)

__sics_console_event_handler_sent__ = SICSConsoleEventHandler('org/gumtree/ui/terminal/telnet/sent')
__sics_console_event_handler_received__ = SICSConsoleEventHandler('org/gumtree/ui/terminal/telnet/received')
__sics_console_event_handler_sent__.activate()
__sics_console_event_handler_received__.activate()

class __Dispose_Listener__(DisposeListener):
    
    def __init__(self):
        pass
    
    def widgetDisposed(self, event):
        pass
    
def __dispose_all__(event):
    global __batch_status_listener__
    global __sics_console_event_handler_sent__
    global __sics_console_event_handler_received__
    global __statusListener__
    global __save_count_node__
    global __saveCountListener__
    sics.SicsCore.getSicsManager().proxy().removeProxyListener(__batch_status_listener__)
    __sics_console_event_handler_sent__.deactivate()
    __sics_console_event_handler_received__.deactivate()
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
# Use below example to create parameters.
# The type can be string, int, float, bool, file.

# Use below example to create a button
__number_of_sample__ = 10
__default_transmission_time__ = 60
__default_scattering_time__ = 120

__script__.numColumns = 2

workflow_list = []
__workflow_id__ = 0
__report_folder__ = 'W:/data/current/reports/pWorkflow'
_is_running = False
_start_timestamp = 0
_counting_status = 'in progress'
_block_config_time = 5 * 60
_trans_setup_time = 1 * 60
_scatt_setup_time = 1 * 60
_drive_sample_time = 20

class WorkflowBlock():
    def __init__(self):
        global __workflow_id__
        self.wid = __workflow_id__
        __workflow_id__ += 1
#        self.config = config
#        self.samples = samples
        tt = 'Workflow Block #' + str(self.wid)
        gc = Group(tt)
        gc.colspan = 2
        gc.numColumns = 2
        cenabled = Par('bool', True, command \
                       = 'set_enabled(' + str(self.wid) + ')')
        cenabled.title = 'enable/disable'
        cremove = Act('remove_block(' + str(self.wid) + ')', 'Remove This Block')
#        cremove = Act('run1()', 'Remove This Block')
        cremove.name = 'cremove_' + str(self.wid)
        cremove.independent = True
        globals()[str(cremove.name)] = cremove
        ctitle = Par('string', tt, command \
                     = 'update_title(' + str(self.wid) + ')')
        ctitle.title = 'title'
        ctext = Par('string', '')
        ctext.height = 60
        ctext.rowspan = 3
        ctext.title = 'configuration'
        gc.add(cenabled, ctext, ctitle, cremove)
        #gs = Group('samples')
        gt = SampleTable(self.wid)
        gc.add(gt.group)
        cnew = Act('insert_block(' + str(self.wid) + ')', 'Add New Block Below')
        cnew.name = 'cnew_' + str(self.wid)
        cnew.colspan = 2
        cnew.independent = True
        globals()[str(cnew.name)] = cnew
        gc.add(cnew)
        self.group = gc
        self.enabled = cenabled
        self.remove = cremove
        self.title = ctitle
        self.config = ctext
        self.table = gt
        self.new_block = cnew
        self.is_running = False
        self.config_start_time = 0
        self.config_stop_time = 0
        
    def update_title(self):
        self.group.name = str(self.title.value)
        self.group.title = str(self.title.value)
        
    def set_enabled(self):
        flag = self.enabled.value
#        self.remove.enable = flag
        self.title.enabled = flag
        self.config.enabled = flag
        self.table.set_enabled(flag)
        update_progress()
        
    def is_enabled(self):
        return self.enabled.value
    
    def __copy__(self):
        pass
        
    def dispose(self):
        self.enabled.dispose()
        self.remove.dispose()
        self.title.dispose()
        self.config.dispose()
        self.table.dispose()
        self.group.dispose()
        self.new_block.dispose()
        
    def run(self):
        tt = self.title.value
        if tt is None or len(tt.strip()) == 0:
            tt = self.group.name
        slog('start block: ' + str(tt))
        if self.need_to_run() :
            self.remove.enabled = False
            self.config.enabled = False
            self.group.highlight = True
            self.is_running = True
#            self.new_block.enabled = False
            try:
                slog('running configuration setup')
                self.config_stop_time = 0
                self.config_start_time = time.time()
                try:
                    exec(str(self.config.value))
                finally:
                    self.config_stop_time = time.time()
                self.table.run()
                slog('block finished: ' + str(tt))
            finally:
                self.group.highlight = False
                self.remove.enabled = True
                self.config.enabled = True
                self.is_running = False
                html = self.get_html()
                if not html is None:
                    slog('upload scan result to notebook database')
                    n_logger.log_table(html)
#                self.new_block.enabled = True
        else:
            slog('block: ' + str(self.title.value) + ' skipped')
        
    def to_rep(self):
        rep = dict()
        rep['title'] = self.title.value
        rep['config'] = self.config.value
        rep['trans_setup'] = self.table.trans_setup.value
        rep['scatt_setup'] = self.table.scatt_setup.value
        rep['trans_time'] = self.table.trans_time.value
        rep['scatt_time'] = self.table.scatt_time.value
        rep['trans_enabled'] = self.table.t3.value
        rep['scatt_enabled'] = self.table.t5.value
        for id in self.table.samples:
            sp = self.table.samples[id]
            rep['name_' + str(id)] = sp.name_text.value
            rep['trans_enabled_' + str(id)] = sp.do_trans.value
            rep['trans_time_' + str(id)] = sp.trans_time.value
            rep['scatt_enabled_' + str(id)] = sp.do_scatt.value
            rep['scatt_time_' + str(id)] = sp.scatt_time.value
        return rep
    
    def from_rep(self, rep):
        self.title.value = rep['title']
        self.group.name = self.title.value
        self.config.value = rep['config'] 
        self.table.trans_setup.value = rep['trans_setup'] 
        self.table.scatt_setup.value = rep['scatt_setup'] 
        self.table.trans_time.value = rep['trans_time'] 
        self.table.scatt_time.value = rep['scatt_time'] 
        self.table.t3.value = rep['trans_enabled'] 
        self.table.t5.value = rep['scatt_enabled'] 
        for id in self.table.samples:
            sp = self.table.samples[id]
            sp.name_text.value = rep['name_' + str(id)] 
            sp.do_trans.value = rep['trans_enabled_' + str(id)] 
            sp.trans_time.value = rep['trans_time_' + str(id)] 
            sp.do_scatt.value = rep['scatt_enabled_' + str(id)] 
            sp.scatt_time.value = rep['scatt_time_' + str(id)]
    
    def need_to_run(self):
#        for i in self.table.samples:
#            if self.table.samples[i].need_to_run():
#                return True
        return self.table.need_to_run()
    
    def get_job_count(self):
        if self.is_enabled():
            return self.table.get_job_count()
        else :
            return 0
        
    def get_done_count(self):
        if self.is_enabled():
            return self.table.get_done_count()
        else:
            return 0
        
    def get_time_estimation(self):
        global _block_config_time
        global _is_running
        if self.is_enabled():
            if _is_running:
                t = self.table.get_time_estimation()
                if t > 0 :
                    if len(self.config.value.strip()) > 0:
                        if self.config_stop_time != 0:
                            return t
                        else:
                            if self.config_start_time != 0:
                                past = time.time() - self.config_start_time
                                if past > _block_config_time :
                                    return t
                                else :
                                    return _block_config_time - past + t
                            else:
                                return _block_config_time + t
                    else:
                        return t
                else:
                    return 0
            else:
                t = self.table.get_time_estimation()
                if t > 0 :
                    if len(self.config.value.strip()) > 0:
                        return _block_config_time + t
                    else:
                        return t
                else:
                    return 0
        else:
            return 0
        
    def reset_result(self):
        self.config_start_time = 0
        self.config_stop_time = 0
        self.table.reset_result()
            
    def append_xml(self, parent):
        if self.enabled.value:
            block = SubElement(parent, 'config')
            block.set('name', self.title.value)
            self.table.append_xml(block)

    def get_html(self):
        if self.enabled.value:
            html = self.table.get_html(self.title.value)
            try:
                span = Element('span')
                span.set('class', 'class_span_tablefoot')
                span.text = 'L1=16776.0, L2=16000.3'
                html += tostring(span)
            except:
                pass
            return html
        return None
        
class Sample():
    def __init__(self, idx):
        global __default_scattering_time__
        self.idx = idx
        s1_idx = Par('label', str(idx))
        s1_idx.width = 24
        s1_name = Par('string', '')
        s1_name.title = ''
        s1_trans = Par('bool', True, command = 'update_progress()')
        s1_trans.title = ''
        s1_trans_time = Par('float', __default_transmission_time__, command = 'update_progress()')
        s1_trans_time.title = ''
        s1_trans_time.width = 20
        s1_trans_res = Par('label', ' ' * 17)
        s1_trans_res.width = 100
        s1_scatt = Par('bool', True, command = 'update_progress()')
        s1_scatt.title = ''
        s1_scatt_time = Par('float', __default_scattering_time__, command = 'update_progress()')
        s1_scatt_time.title = ''
        s1_scatt_time.width = 20
        s1_scatt_res = Par('label', ' ' * 17)
        s1_scatt_res.width = 100
        self.id_label = s1_idx
        self.name_text = s1_name
        self.do_trans = s1_trans
        self.trans_time = s1_trans_time
        self.trans_res = s1_trans_res
        self.do_scatt = s1_scatt
        self.scatt_time = s1_scatt_time
        self.scatt_res = s1_scatt_res
        self.trans_start_time = 0
        self.trans_stop_time = 0
        self.scatt_start_time = 0
        self.scatt_stop_time = 0
        
    def dispose(self):
        self.id_label.dispose()
        self.name_text.dispose()
        self.do_trans.dispose()
        self.trans_time.dispose()
        self.trans_res.dispose()
        self.do_scatt.dispose()
        self.scatt_time.dispose()
        self.scatt_res.dispose()
        
    def run_transmission(self):
        global _counting_status
        if self.do_trans.value and len(self.trans_res.value.strip()) == 0:
            slog('start transmission collect for sample number ' + str(self.idx))
            self.trans_res.value = _counting_status
            self.trans_stop_time = 0
            self.trans_start_time = time.time()
            self.trans_res.highlight = True
            try:
                scan10(self.idx, self.trans_time.value, self.name_text.value)
                self.trans_res.value = get_base_filename()
                step_progress()
            finally:
                self.trans_res.highlight = False
                self.trans_stop_time = time.time()
                
    def run_scattering(self):
        global _counting_status
        if self.do_scatt.value and len(self.scatt_res.value.strip()) == 0:
            slog('start scattering collect for sample number ' + str(self.idx))
            self.scatt_res.value = _counting_status
            self.scatt_stop_time = 0
            self.scatt_start_time = time.time()
            self.scatt_res.highlight = True
            try:
                scan10(self.idx, self.scatt_time.value, self.name_text.value)
                self.scatt_res.value = get_base_filename()
                step_progress()
            finally:
                self.scatt_res.highlight = False
                self.scatt_stop_time = time.time()
            
    def set_enabled(self, flag):
        self.id_label.enabled = flag
        self.name_text.enabled = flag
        self.do_trans.enabled = flag
        self.trans_time.enabled = flag
        self.trans_res.enabled = flag
        self.do_scatt.enabled = flag
        self.scatt_time.enabled = flag
        self.scatt_res.enabled = flag
        
    def need_to_run(self):
        return self.need_to_run_trans() or self.need_to_run_scatt()
    
    def reset_trans_result(self):
        self.trans_res.value = ''
        self.trans_start_time = 0
        self.trans_stop_time = 0
        
    def reset_scatt_result(self):
        self.scatt_res.value = ''
        self.scatt_start_time = 0
        self.scatt_stop_time = 0
        
    def get_trans_time_estimation(self):
        global _drive_sample_time
        global _is_running
        if _is_running:
            if self.trans_start_time != 0:
                if self.trans_stop_time == 0 :
                    past = time.time() - self.trans_start_time
                    est = float(self.trans_time.value) + _drive_sample_time
                    if past > est :
                        return 0
                    else:
                        return est - past
                else:
                    return 0
            else:
                if self.do_trans.value:
                    return float(self.trans_time.value) + _drive_sample_time
                else:
                    return 0
        else:
            if self.do_trans.value :
                return float(self.trans_time.value) + _drive_sample_time
            else:
                return 0


    def get_scatt_time_estimation(self):
        global _drive_sample_time
        global _is_running
        if _is_running:
            if self.scatt_start_time != 0:
                if self.scatt_stop_time == 0 :
                    past = time.time() - self.scatt_start_time
                    est = float(self.scatt_time.value) + _drive_sample_time
                    if past > est :
                        return 0
                    else:
                        return est - past
                else:
                    return 0
            else:
                if self.do_scatt.value:
                    return float(self.scatt_time.value) + _drive_sample_time
                else:
                    return 0
        else:
            if self.do_scatt.value :
                return float(self.scatt_time.value) + _drive_sample_time
            else:
                return 0
        
    def need_to_run_trans(self):
        return self.do_trans.value and len(self.trans_res.value.strip()) == 0

    def need_to_run_scatt(self):
        return self.do_scatt.value and len(self.scatt_res.value.strip()) == 0
    
    def append_xml(self, parent):
        if len(self.trans_res.value.strip()) > 0 or len(self.scatt_res.value.strip()) > 0:
            sp = SubElement(parent, 'sample')
            sp.set('index', str(self.idx))
            sp.set('name', self.name_text.value.strip())
            trans = SubElement(sp, 'transmission')
            trans.text = self.trans_res.value.strip()
            scatt = SubElement(sp, 'scattering')
            scatt.text = self.scatt_res.value.strip()
        
    def get_html_elmt(self):
        if len(self.trans_res.value.strip()) > 0 or len(self.scatt_res.value.strip()) > 0:
            tr = Element('tr')
            td = SubElement(tr, 'td')
            td.text = str(self.idx)
            td = SubElement(tr, 'td')
            td.text = str(self.name_text.value.strip())
            td = SubElement(tr, 'td')
            td.text = get_short_pdfname(self.trans_res.value.strip())
            td = SubElement(tr, 'td')
            td.text = get_short_pdfname(self.scatt_res.value.strip())
            td = SubElement(tr, 'td')
            td.text = str(self.scatt_time.value)
            td = SubElement(tr, 'td')
            return tr
        return None
        
def get_short_pdfname(fn):
    idx = fn.find('.')
    if idx > 0:
        return fn[0:idx]
    return fn
    
class SampleTable():
    def __init__(self, wid, name = 'Samples'):
        self.wid = wid
        self.samples = dict()
        self.group = Group(name)
        self.group.hideTitle = True
        self.group.numColumns = 8
        self.group.colspan = 2
        trans_setup = Par('string', '')
        trans_setup.title = 'transmission setup'
        trans_setup.colspan = 4
        trans_setup.height = 40
        scatt_setup = Par('string', '')
        scatt_setup.title = 'scattering setup'
        scatt_setup.colspan = 3
        scatt_setup.height = 40
        space1 = Par('space')
        trans_time = Par('float', '60', command='change_trans_time(' \
                         + str(wid) + ')')
        trans_time.title = 'transmission time'
        trans_time.colspan = 4
        scatt_time = Par('float', '120', command='change_scatt_time(' \
                         + str(wid) + ')')
        scatt_time.title = 'scattering time'
        scatt_time.colspan = 3
        space2 = Par('space')
         
        tit_1 = Par('label', 'idx')
        tit_1.width = 24
        tit_2 = Par('label', 'Sample Name')
        tit_3 = Par('bool', True, command='toggle_trans_enabled(' \
                         + str(wid) + ')')
        tit_3.title = ''
        tit_4 = Par('label', 'Transmission')
        tit_4.colspan = 2
        tit_5 = Par('bool', True, command='toggle_scatt_enabled(' \
                         + str(wid) + ')')
        tit_5.title = ''
        tit_6 = Par('label', 'Scattering')
        tit_6.colspan = 2
        self.trans_time = trans_time
        self.scatt_time = scatt_time
        self.trans_setup = trans_setup
        self.scatt_setup = scatt_setup
        self.space1 = space1
        self.space2 = space2
        self.t1 = tit_1
        self.t2 = tit_2
        self.t3 = tit_3
        self.t4 = tit_4
        self.t5 = tit_5
        self.t6 = tit_6
        self.group.add(trans_setup, scatt_setup, space1, trans_time, \
                       scatt_time, space2, \
                       tit_1, tit_2, tit_3, \
                       tit_4, tit_5, tit_6)
        for i in xrange(__number_of_sample__) :
            self.add_sample(i + 1)
        self.trans_config_start_time = 0
        self.trans_config_stop_time = 0
        self.scatt_config_start_time = 0
        self.scatt_config_stop_time = 0
        self.trans_start_time = 0
        self.trans_stop_time = 0
        self.scatt_start_time = 0
        self.scatt_stop_time = 0
        
    def add_sample(self, id):
        sample = Sample(id)
        self.samples[id] = sample
#        sample.do_trans.command = 'redo_trans(' + str(self.wid) + ', ' + str(id) + ')'
#        sample.do_scatt.command = 'redo_scatt(' + str(self.wid) + ', ' + str(id) + ')'
        self.group.add(sample.id_label, sample.name_text, sample.do_trans, sample.trans_time, \
                 sample.trans_res, sample.do_scatt, sample.scatt_time, sample.scatt_res)
    
    def run(self):
#        self.trans_time.enabled = False
#        self.scatt_time.enabled = False
#        self.t3.enabled = False
#        self.t5.enabled = False
        self.trans_setup.enabled = False
        self.scatt_setup.enabled = False
        try:
            while self.need_to_run():
                if self.need_to_run_trans():
                    self.run_trans_setup()
                    self.run_trans()
                if self.need_to_run_scatt():
                    self.run_scatt_setup()
                    self.run_scatt()
        finally:
#            self.trans_time.enabled = True
#            self.scatt_time.enabled = True
#            self.t3.enabled = True
#            self.t5.enabled = True
            self.trans_setup.enabled = True
            self.scatt_setup.enabled = True
            
    def need_to_run(self):
        return self.need_to_run_trans() or self.need_to_run_scatt()
        
    def need_to_run_trans(self):
        for i in self.samples:
            if self.samples[i].need_to_run_trans():
                return True
        return False

    def need_to_run_scatt(self):
        for i in self.samples:
            if self.samples[i].need_to_run_scatt():
                return True
        return False

    def get_job_count(self):
        ct = 0
        for i in self.samples:
            if self.samples[i].do_trans.value:
                ct += 1
            if self.samples[i].do_scatt.value:
                ct += 1
        return ct
        
    def get_done_count(self):
        ct = 0
        for i in self.samples:
            if self.samples[i].do_trans.value and len(self.samples[i].trans_res.value.strip()) > 0:
                ct += 1
            if self.samples[i].do_scatt.value and len(self.samples[i].scatt_res.value.strip()) > 0:
                ct += 1
        return ct
    
    def get_time_estimation(self):
        global _trans_setup_time
        global _scatt_setup_time
        global _drive_sample_time
        global _is_running
        
        if _is_running :
            t = 0
            if self.trans_config_start_time != 0 and self.trans_config_stop_time == 0:
                past = time.time() - self.trans_config_start_time
                if past < _trans_setup_time :
                    t += _trans_setup_time - past
                else:
                    pass
                for i in self.samples:
                    t += self.samples[i].get_trans_time_estimation()
                if self.need_to_run_scatt():
                    if len(self.scatt_setup.value.strip()) > 0 :
                        t += _scatt_setup_time
                    for i in self.samples:
                        t += self.samples[i].get_scatt_time_estimation()
                else:
                    pass
            elif self.trans_start_time != 0 and self.trans_stop_time == 0:
                for i in self.samples:
                    t += self.samples[i].get_trans_time_estimation()
                if self.need_to_run_scatt():
                    if len(self.scatt_setup.value.strip()) > 0 :
                        t += _scatt_setup_time
                    for i in self.samples:
                        t += self.samples[i].get_scatt_time_estimation()
                else:
                    pass
            elif self.scatt_config_start_time != 0 and self.scatt_config_stop_time == 0:
                past = time.time() - self.scatt_config_start_time
                if past < _scatt_setup_time :
                    t += _scatt_setup_time - past
                else:
                    pass
                for i in self.samples:
                    t += self.samples[i].get_scatt_time_estimation()
                if self.need_to_run_trans():
                    if len(self.trans_setup.value.strip()) > 0 :
                        t += _trans_setup_time
                    for i in self.samples:
                        t += self.samples[i].get_trans_time_estimation()
                else:
                    pass
            elif self.scatt_start_time != 0 and self.scatt_stop_time == 0:
                for i in self.samples:
                    t += self.samples[i].get_scatt_time_estimation()
                if self.need_to_run_trans():
                    if len(self.trans_setup.value.strip()) > 0 :
                        t += _trans_setup_time
                    for i in self.samples:
                        t += self.samples[i].get_trans_time_estimation()
                else:
                    pass
            else:
                if self.need_to_run_scatt() :
                    if len(self.scatt_setup.value.strip()) > 0 :
                        t += _scatt_setup_time
                    for i in self.samples:
                        t += self.samples[i].get_scatt_time_estimation()
                if self.need_to_run_trans():
                    if len(self.trans_setup.value.strip()) > 0 :
                        t += _trans_setup_time
                    for i in self.samples:
                        t += self.samples[i].get_trans_time_estimation()
            return t
        else:
            tt = 0
            st = 0
            for i in self.samples:
                tt += self.samples[i].get_trans_time_estimation()
                st += self.samples[i].get_scatt_time_estimation()
            if tt > 0:
                if len(self.trans_setup.value.strip()) > 0 :
                    tt += _trans_setup_time
            if st > 0:
                if len(self.scatt_setup.value.strip()) > 0 :
                    st += _scatt_setup_time
            return tt + st
        
    def run_trans_setup(self):
        slog('collecting neutrons for transmission')
        ts = self.trans_setup.value
        if ts != None and len(ts.strip()) > 0:
            slog('running transmission setup ' + str(ts).strip().replace('\r\n', ' + '))
            self.trans_config_stop_time = 0
            self.trans_config_start_time = time.time()
            try:
                exec(str(ts))
            finally:
                self.trans_config_stop_time = time.time()
        
    def run_trans(self):
        if self.need_to_run_trans():
            self.trans_stop_time = 0
            self.trans_start_time = time.time()
            try:
                for i in sorted(self.samples):
                    self.samples[i].run_transmission()
            finally:
                self.trans_stop_time = time.time()
            self.run_trans()

    def run_scatt_setup(self):
        slog('collecting neutrons for scattering')
        ss = self.scatt_setup.value
        if ss != None and len(ss.strip()) > 0:
            slog('running scattering setup ' + str(ss).strip().replace('\r\n', ' + '))
            self.scatt_config_stop_time = 0
            self.scatt_config_start_time = time.time()
            try:
                exec(str(ss))
            finally:
                self.scatt_config_stop_time = time.time()
        
    def run_scatt(self):
        if self.need_to_run_scatt():
            self.scatt_stop_time = 0
            self.scatt_start_time = time.time()
            try:
                for i in sorted(self.samples):
                    self.samples[i].run_scattering()
            finally:
                self.scatt_stop_time = time.time()
            self.run_scatt()

    def reset_result(self):
        self.trans_config_start_time = 0
        self.trans_config_stop_time = 0
        self.scatt_config_start_time = 0
        self.scatt_config_stop_time = 0
        self.trans_start_time = 0
        self.trans_stop_time = 0
        self.scatt_start_time = 0
        self.scatt_stop_time = 0
        for i in self.samples:
            self.samples[i].reset_trans_result()
            self.samples[i].reset_scatt_result()
        
    def set_enabled(self, flag):
        self.t1.enabled = flag
        self.t2.enabled = flag
        self.t3.enabled = flag
        self.t4.enabled = flag
        self.t5.enabled = flag
        self.t6.enabled = flag
        self.trans_time.enabled = flag
        self.scatt_time.enabled = flag
        self.trans_setup.enabled = flag
        self.scatt_setup.enabled = flag
        for i in self.samples:
            self.samples[i].set_enabled(flag)
            
    def update_trans_time(self):
        for i in self.samples:
            self.samples[i].trans_time.value = self.trans_time.value

    def update_scatt_time(self):
        for i in self.samples:
            self.samples[i].scatt_time.value = self.scatt_time.value
        
    def toggle_trans_enabled(self):
        for i in self.samples:
            self.samples[i].do_trans.value = self.t3.value

    def toggle_scatt_enabled(self):
        for i in self.samples:
            self.samples[i].do_scatt.value = self.t5.value
        
    def dispose(self):
        for i in self.samples:
            self.samples[i].dispose()
        self.t1.dispose()
        self.t2.dispose()
        self.t3.dispose()
        self.t4.dispose()
        self.t5.dispose()
        self.t6.dispose()
        self.trans_time.dispose()
        self.scatt_time.dispose()
        self.group.dispose()
        self.trans_setup.dispose()
        self.scatt_setup.dispose()
        self.space1.dispose()
        self.space2.dispose()
        
    def append_xml(self, parent):
        for i in sorted(self.samples):
            sp = self.samples[i]
            sp.append_xml(parent)

    def get_html(self, title):
        table = Element('table')
        table.set('align', 'center')
        table.set('border', '1')
        table.set('cellpadding', '2')
        table.set('cellspacing', '0')
        table.set('class', 'xmlTable')
        table.set('style', 'table-layout:fixed; width:100%; word-wrap:break-word')
        tr = SubElement(table, 'tr')
        th = SubElement(tr, 'th')
        th.set('colspan', '2')
        th.text = strftime("%Y-%m-%dT%H:%M:%S", localtime())
        th = SubElement(tr, 'th')
        th.set('colspan', '4')
        th.text = title
        
        tr = SubElement(table, 'tr')
        th = SubElement(tr, 'th')
        th.text = 'Position'
        th = SubElement(tr, 'th')
        th.text = 'Sample Name'
        th = SubElement(tr, 'th')
        th.text = 'Transmission'
        th = SubElement(tr, 'th')
        th.text = 'Scattering'
        th = SubElement(tr, 'th')
        th.text = 'Preset'
        th = SubElement(tr, 'th')
        th.text = 'Comment'
        
        for i in sorted(self.samples):
            sp = self.samples[i]
            elmt = sp.get_html_elmt()
            if not elmt is None:
                table.append(elmt)
            
        return tostring(table, method = 'html')
    
def update_title(wid):
    b = get_workflow_block(wid)
    if not b is None:
        b.update_title()

def set_enabled(wid):
    b = get_workflow_block(wid)
    if not b is None:
        b.set_enabled()
                
def get_workflow_block(wid):
    global workflow_list
    for i in xrange(len(workflow_list)):
        wb = workflow_list[i]
        if wb.wid == wid:
            return wb
    return None
    
def change_trans_time(wid):
    wb = get_workflow_block(wid)
    if not wb is None:
        wb.table.update_trans_time()
    update_time()

def change_scatt_time(wid):
    wb = get_workflow_block(wid)
    if not wb is None:
        wb.table.update_scatt_time()
    update_time()
            
def toggle_trans_enabled(wid):
    wb = get_workflow_block(wid)
    if not wb is None:
        wb.table.toggle_trans_enabled()
    update_progress()

def toggle_scatt_enabled(wid):
    wb = get_workflow_block(wid)
    if not wb is None:
        wb.table.toggle_scatt_enabled()
    update_progress()
        
def remove_block(wid = None):
    if wid is None:
        if len(workflow_list) > 0:
            try:
                rmv = workflow_list.pop()
                rmv.dispose()
            finally:
                __UI__.updateUI()
                update_progress()
    else:
        wb = get_workflow_block(wid)
        if not wb is None:
            tt = 'Block ' + wb.title.value + ' removed'
            try:
                workflow_list.remove(wb)
                wb.dispose()
                slog(tt)
            finally:
                __UI__.updateUI()
                update_progress()

def insert_block(wid):
    global workflow_list
    old = None
    idx = -1
    for i in xrange(len(workflow_list)):
        wb = workflow_list[i]
        if wb.wid == wid:
            idx = i
            old = wb
            break
    if idx < 0:
        add_block()
    else:
        wb = WorkflowBlock()
        workflow_list.insert(idx + 1, wb)
        try:
            wb.group.moveAfterObject(old.group)
            wb.config.value = old.config.value
            wb.table.t3.value = old.table.t3.value
            wb.table.t5.value = old.table.t5.value
            wb.table.trans_time.value = old.table.trans_time.value
            wb.table.scatt_time.value = old.table.scatt_time.value
            wb.table.trans_setup.value = old.table.trans_setup.value
            wb.table.scatt_setup.value = old.table.scatt_setup.value
            for i in wb.table.samples:
                sample = wb.table.samples[i]
                old_sample = old.table.samples[i]
                sample.name_text.value = old_sample.name_text.value
                sample.do_trans.value = old_sample.do_trans.value
                sample.trans_time.value = old_sample.trans_time.value
                sample.do_scatt.value = old_sample.do_scatt.value
                sample.scatt_time.value = old_sample.scatt_time.value
        finally:
            __UI__.updateUI()
    update_progress()
                
def add_block():
    global workflow_list
    old = None
    if len(workflow_list) > 0 :
        old = workflow_list[-1]
    wb = WorkflowBlock()
    workflow_list.append(wb)
    try:
        if not old is None:
            wb.config.value = old.config.value
            wb.table.t3.value = old.table.t3.value
            wb.table.t5.value = old.table.t5.value
            wb.table.trans_time.value = old.table.trans_time.value
            wb.table.scatt_time.value = old.table.scatt_time.value
            wb.table.trans_setup.value = old.table.trans_setup.value
            wb.table.scatt_setup.value = old.table.scatt_setup.value
            for i in wb.table.samples:
                sample = wb.table.samples[i]
                old_sample = old.table.samples[i]
                sample.name_text.value = old_sample.name_text.value
                sample.do_trans.value = old_sample.do_trans.value
                sample.trans_time.value = old_sample.trans_time.value
                sample.do_scatt.value = old_sample.do_scatt.value
                sample.scatt_time.value = old_sample.scatt_time.value
    finally:
        __UI__.updateUI()

def run_scan():
    global _is_running
    global _start_timestamp
    act_load.enabled = False
    act_run.enabled = False
    _is_running = True
    _start_timestamp = time.time()
    try:
        slog('start Bilby workflow')
        for wb in workflow_list:
            wb.reset_result()
        update_progress()
        for wb in workflow_list:
            if wb.is_enabled() :
                wb.run()
        slog('workflow is finished')
    finally:
        act_load.enabled = True
        act_run.enabled = True
        _is_running = False
        _start_timestamp = 0
        pro_bar.selection = 0
        export_report()
        update_time()
        sics.execute('hset /experiment/gumtree_time_estimate 0')
        
def load_workflow():
    global workflow_list
    fn = selectSaveFile(['*.pkl'])
    if fn is None:
        return
    wl = None
    try :
        file = open(fn, 'rb')
        wl = pickle.load(file)
    finally:
        file.close()
    try:
        if not wl is None and len(wl) > 0:
            if len(wl) > len(workflow_list) :
                for i in xrange(len(wl) - len(workflow_list)):
                    workflow_list.append(WorkflowBlock())
            elif len(wl) < len(workflow_list) :
                for i in xrange(len(workflow_list) - len(wl)):
                    rmv = workflow_list.pop()
                    rmv.dispose()
            for i in xrange(len(wl)):
                workflow_list[i].from_rep(wl[i])
    finally:
        __UI__.updateUI()
        update_time()

def export_workflow():
    global workflow_list
    path = selectSaveFile(['*.pkl'])
    if path == None:
        return
    if not path.lower().endswith('.pkl') :
        path += '.pkl'
    fi = File(path)
    fp = fi.getParentFile()
    if not fp.exists():
        if not fp.makedirs():
            print 'Error: failed to make directory: ' + path
            return
    slog('workflow exported to ' + path)
    file = open(path, 'wb')
    wf_rep = []
    for wb in workflow_list:
        wf_rep.append(wb.to_rep())
    try:
        pickle.dump(wf_rep, file)
    except:
        traceback.print_exc(__writer__)
    finally:
        file.close()

def export_report():
    global __export_folder__
    root = Element('workflow')
    tree = ElementTree(root)
    for bl in workflow_list:
        bl.append_xml(root)
    fn = strftime("%Y-%m-%dT%H-%M-%S", localtime())
    fn = __export_folder__ + '/' + 'BBY_' + fn + '.xml'
    tree.write(fn)
    slog('Report XML created at ' + fn)
    
def update_progress():
#    print 'updating progress'
    update_time()
#    global _is_running
#    if not _is_running:
#        return
#    job_ct = 0
#    done_ct = 0
#    for wb in workflow_list:
#        if not wb.is_enabled():
#            continue
#        if wb.is_running:
#            done_ct = job_ct
#        job_ct += wb.get_job_count()
#        done_ct += wb.get_done_count()
#    pro_bar.max = job_ct
#    pro_bar.selection = done_ct
#    print 'job count is ' + str(job_ct)
#    print 'done count is ' + str(done_ct)
    
def step_progress():
#    pro_bar.selection = int(pro_bar.selection) + 1
    update_time()
    
def update_time():
    global _start_timestamp
    if _is_running:
        t = 0
        for wb in workflow_list:
            t += wb.get_time_estimation()
        slog('estimated time left: ' + str(int(t)) + 's')
#        par_time.value = _get_tstring(t)
        ft = int(time.time() + t)
        sics.execute('hset /experiment/gumtree_time_estimate ' + str(ft))
        d = datetime.datetime.fromtimestamp(ft)
        td = datetime.datetime.today()
        fs = 'to finish at '
        if t > 3600 * 24 :
            fs += SimpleDateFormat("H:mm dd/M").format(d)
        else:
            if d.day != td.day :
                fs += SimpleDateFormat("H:mm ").format(d) + 'tomorrow'
            else:
                fs += SimpleDateFormat("H:mm").format(d)
        par_time.value = fs
        past = time.time() - _start_timestamp
        pct = int(round(past / (past + t) * 100))
        pro_bar.max = 100
        pro_bar.selection = pct
    else :
        t = 0
        for wb in workflow_list:
            t += wb.get_time_estimation()
        slog('estimated time to run: ' + str(int(t)) + 's')
        par_time.value = _get_tstring(t)
        
def _get_tstring(t):
        if t == 0:
            return ''
        if t < 360:
            return "%d seconds" % t
        if t < 3600 * 2:
            return "%d minutes" % round(t / 60)
        if t < 3600 * 24:
            rm = t % 3600
            m = round(rm / 60)
            h = t / 3600
            if h >= 2 :
                hs = 'hours'
            else:
                hs = 'hour'
            if m > 0:
                if m >= 2:
                    ms = 'minutes'
                else:
                    ms = 'minute'
                return ("%d " % h) + hs + ("%d " % m) + ms
            else:
                return ("%d " % h) + hs
        return "%d hours" % round(t / 3600)
    
#def upload_html(wid):
#    bl = get_workflow_block(wid)
#    if not bl is None:
#        html = bl.get_html()
#        if not html is None:
#            n_logger.log_table(html)
    
pro_bar = Par('progress', 0)
pro_bar.max = 0
pro_bar.selection = 0
par_time = Par('string', '')
par_time.title = 'Time Estimation'
par_time.enabled = False

act_load = Act('load_workflow()', 'Load Workflow')
act_exp = Act('export_workflow()', 'Export Workflow')
act_exp.independent = True
#act_rmv = Act('remove_block()', 'Remove Workflow Block')
#act_rmv.independent = True
act_add = Act('add_block()', 'Add Workflow Block')
act_add.independent = True 
act_run = Act('run_scan()', 'Run Bilby Workflow')
#act_run.colspan = 2
    
#def add_sample(table, i):
##    group.add(s1_idx, s1_name, s1_trans, s1_trans_time, s1_trans_res, s1_scatt, s1_scatt_time, s1_scatt_res)
#    table.add_sample(sam)
#add_block()
workflow_list.append(WorkflowBlock())

update_time()
# Use below example to create a new Plot
# Plot4 = Plot(title = 'new plot')

def __dataset_selected__(datasets):
    global __selected_dataset__
    __selected_dataset__ = datasets
    dfs = __DATASOURCE__.getSelectedDatasets()
    __INFOTEXT__.clear()
    for df in dfs:
        fid = df.getFileID() + ': '
        __INFOTEXT__.appendText(fid, 'bold')
        des = ''
        if df.getTitle() != None:
            des += df.getTitle() + '\n'
        if df.getDescription() != None:
            des += ' ' * len(fid) + df.getDescription() + '\n'
        des += '\n'
        __INFOTEXT__.appendText(des)
    
# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    from threading import Thread
    global workflow_list
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    
    print str(fns) + ' selected'
    # check if a list of file names has been given
#    run_action(act_run)
#    logErr('start new thread')
#    task = Thread(target=run_action(act_run))
#    task.start()
#    logErr('started')
    
def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
