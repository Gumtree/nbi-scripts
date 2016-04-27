# Script control setup area
# script info
__script__.title = '2D Bilby Plot'
__script__.version = '1.15 with panel rotation'


# Use below example to create parameters.
# The type can be string, int, float, bool, file.

directory = 'C:/temp/' 


# INFO ################################################
det_info7 = Par('label', 'Detector Height: 0 - 81')
det_info7.colspan = 1
det_info8 = Par('label', 'Detector Tubes: 0 - 239')
det_info8.colspan = 1
sep_line1 =  Par('label', '                  ---------------')
sep_line1.colspan = 4
det_info1 = Par('label', 'curtain_l:   0-39')
det_info1.colspan = 1
det_info2 = Par('label', 'curtain_r: 40-79')
det_info2.colspan = 1
det_info3 = Par('label', 'curtain_u:   80-119')
det_info3.colspan = 1
det_info4 = Par('label', 'curtain_d: 120-159')
det_info4.colspan = 1
det_info5 = Par('label', 'rear_l: 160-199')
det_info5.colspan = 2
det_info6 = Par('label', 'rear_r: 200-239')
det_info6.colspan = 2

g0 = Group('Info')
g0.numColumns = 2 #9
g0.add(det_info7,det_info8,
       sep_line1,det_info1,det_info3,det_info5,
       det_info2,det_info4,det_info6)

# INPUT ################################################################
# DETECTOR AREA FOR PLOT 1
frame_number = Par('int', 0, command = 'frame_number_changed()')
frame_number.title = 'Frame Number: '
frame_number.colspan = 2
def frame_number_changed():
    print 'Frame Number ' + str(timebin_start.value)


timebin_start = Par('int', 0, command = 'timebin_start_changed()')
timebin_start.title = 'Time bin from '
def timebin_start_changed():
    print 'Time bin from ' + str(timebin_start.value)
timebin_end = Par('int', 299, command = 'timebin_end_changed()')
timebin_end.title = 'to '
def timebin_end_changed():
    print 'Time bin to ' + str(timebin_end.value)
timebins_FromFile = Par('string', 'NaN')
timebins_FromFile.title = 'of'
timebins_FromFile.enabled = False

timebin_info = Par('label', '')
timebin_info.colspan = 2

# -------------------------------------------------------

detheight_start = Par('int', 0, command = 'detheight_start_changed()')
detheight_start.title = 'Detector tube height from '
def detheight_start_changed():
    print 'Detector tube height from ' + str(detheight_start.value)
detheight_end = Par('int', 81, command = 'detheight_end_changed()')
detheight_end.title = 'to '
def detheight_end_changed():
    print 'Detector tube height to ' + str(detheight_end.value)

dettube_start = Par('int', 0, command = 'dettube_start_changed()')
dettube_start.title = 'Detector tube number from '
def dettube_start_changed():
    print 'Detector tube number from ' + str(dettube_start.value)
dettube_end = Par('int', 239, command = 'dettube_end_changed()')
dettube_end.title = 'to '
def dettube_end_changed():
    print 'Detector tube number to ' + str(dettube_end.value)    

# -------------------------------------------------------

Rotate_leftright = Par('bool', False, command = 'Rotate_leftright_changed()')
Rotate_leftright.title = 'Rotate Left and Right Curtains'
Rotate_leftright.colspan = 1
def Rotate_leftright_changed():
    if Rotate_leftright.value:
        print        
        print 'Rotate Left and Right Curtain'
        
Rotate_topbottom = Par('bool', False, command = 'Rotate_topbottom_changed()')
Rotate_topbottom.title = 'Rotate Top and Bottom Curtains'
Rotate_topbottom.colspan = 1
def Rotate_topbottom_changed():
    if Rotate_topbottom.value:
        print        
        print 'Rotate Top and Bottom Curtain'
        
Rotate_rear = Par('bool', False, command = 'Rotate_rear_changed()')
Rotate_rear.title = 'Rotate Rear Detector'
Rotate_rear.colspan = 1
def Rotate_rear_changed():
    if Rotate_topbottom.value:
        print        
        print 'Rotate Rear Detector'
        
        
Gap_leftright = Par('int', 0, command = 'gap_leftright_changed()')
Gap_leftright.title = 'Gap '
Gap_leftright.colspan = 1
def gap_leftright_changed():
    print
    print 'Gap between left and right panel: ' + str(Gap_leftright.value) + ' pixels'
    print 'Gap doesnt work yet'
    
Gap_topbottom = Par('int', 0, command = 'gap_topbottom_changed()')
Gap_topbottom.title = 'Gap '
Gap_topbottom.colspan = 1
def gap_topbottom_changed():
    print
    print 'Gap between top and bottom panel: ' + str(Gap_topbottom.value) + ' pixels'
    print 'Gap doesnt work yet'

g1 = Group('Choose Time Bin and Detector Area                           [Plot 1,2]')
g1.numColumns = 2 #9
g1.add(frame_number,
       timebin_start, timebin_end,
       timebin_info, timebins_FromFile,
       sep_line1,
       detheight_start, detheight_end,
       dettube_start, dettube_end,
       sep_line1,
       Rotate_leftright,Gap_leftright,
       Rotate_topbottom,Gap_topbottom,
       Rotate_rear
       )


# DETECTOR AREA TO INTEGRATE PROFILES
detheight_int_start = Par('int', 0, command = 'detheight_int_start_changed()')
detheight_int_start.title = 'Detector tube height from '
def detheight_int_start_changed():
    print 'Detector tube height from ' + str(detheight_int_start.value)
detheight_int_end = Par('int', 81, command = 'detheight_int_end_changed()')
detheight_int_end.title = 'to '
def detheight_int_end_changed():
    print 'Detector tube height to ' + str(detheight_int_end.value)

dettube_int_start = Par('int', 0, command = 'dettube_int_start_changed()')
dettube_int_start.title = 'Detector tube number from '
def dettube_int_start_changed():
    print 'Detector tube number from ' + str(dettube_int_start.value)
dettube_int_end = Par('int', 239, command = 'dettube_int_end_changed()')
dettube_int_end.title = 'to '
def dettube_int_end_changed():
    print 'Detector tube number to ' + str(dettube_int_end.value)





integration_mode = Par('string', 'Tube Height', options = ['Tube Height', 'Tube Number'])
integration_mode.title = 'Profile along '   

g3 = Group('Choose Detector Area for Profile       [Plot 1(red marker),3 ]')
g3.numColumns = 2
g3.add(detheight_int_start, detheight_int_end,
       dettube_int_start, dettube_int_end,
       integration_mode)

automatic_PROFILEexport = Par('bool', False)
automatic_PROFILEexport.title = 'Time binned profiles'

incr_timebins = Par('int', 10, command = 'incr_timebins_changed()')
incr_timebins.title = ' in increment of  '
def incr_timebins_changed():
    print 'Automatically bin and export TOF spectra every ' + str(incr_timebins.value) + ' frames'
    

g4 = Group('Automatically Export Profiles For All Time Bins?')
g4.numColumns = 2 #9
g4.add(automatic_PROFILEexport,incr_timebins)




#############################################################################
# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
    
    # check if a list of file names has been given
    
    if (fns is None or len(fns) == 0) :
        print 'no input datasets'
    else :
        for fn in fns:
            # load dataset with each file name
            ds = df[fn]

            filename = os.path.basename(fn) # gets rid of the path
            filename = filename[:filename.find('.nx.hdf')] # gets rid of the hdf
            filename = filename.replace('0000','')
            
            if frame_number.value > (ds.shape[0]-1):
                print 'Only ',ds.shape[0], ' frames available, using frame [0]' 
                det = ds[0]
                 #print ds.shape[0]
            #det = ds[frame_number.value]
            else:
                print ' '
                print 'Frame: ',frame_number.value 
                det = ds[frame_number.value]
            
            #det = ds[0] # to get rid of first nonsense number -> takes first element in list(list(list(list))))
            
            
            det.axes[0] = range(det.shape[0]) # so that all axes are integers
            det.axes[1] = range(det.shape[1]) 
            det.axes[2] = range(det.shape[2])           

            
            a = copy(det)
            
            #a [:,0:82,0:40] = det[:,0:82,20:60] # doesn't work neg             
              
                        
            if Rotate_leftright.value:               
                
                b = copy(a)
                
                b[:,:,40:80]= a[:,:,0:40]                
                for i in range(40):
                    b [:,:,i] = a[:,:,79-i]                    
                a = copy (b)    
                for i in range(82):
                    b [:,i,0:80] = a [:,81-i,0:80]
                
                a = copy (b)
                              
            if Rotate_topbottom.value:               
                
                b = copy(a)
                
                b[:,:,120:160]= a[:,:,80:120]                
                for i in range(40):
                    b [:,:,80+i] = a[:,:,159-i]                    
                a = copy (b)    
                for i in range(82):
                    b [:,i,80:120] = a [:,81-i,80:120]
                
                a = copy (b)
                
            if Rotate_rear.value: 
                
                b = copy(a)
                
                b[:,:,200:240]= a[:,:,160:200]                
                for i in range(40):
                    b [:,:,160+i] = a[:,:,239-i]                    
                a = copy (b)    
                for i in range(82):
                    b [:,i,160:200] = a [:,81-i,160:200]
                
                a = copy (b)
             
            det = copy(a)
        
            
            timebins_FromFile.value  = det.shape[0]
                          
            det_roi = det[:,
                       detheight_start.value:detheight_end.value+1,
                       dettube_start.value:dettube_end.value+1]# limit detector to ROI
           
            det_roi_tof_1D = det_roi[:, :, :].sum(0) # sum to one axis (axis [0] = time of flight)
            
            det_roi_totcounts = sum(det_roi_tof_1D)
            print
            print 'Total counts: ',det_roi_totcounts 
            
            det_roi_tof_1D.axes.title = 'time_bin'
            det_roi_tof_1D.title = 'intensity'
           
            Plot2.set_dataset(det_roi_tof_1D)
            Plot2.add_x_marker(timebin_start.value, 50, 'red')
            Plot2.add_x_marker(timebin_end.value, 50, 'red')
            Plot2.title = 'TOF spectrum of detector image above'
            Plot2.x_label = str(det_roi_tof_1D.axes.title) #'time bin'
           
            export_ascii_1D(det_roi_tof_1D, directory + 'TOF_' + filename +
                         '_HOR_'+ str(dettube_start.value) + 'to' + str(dettube_end.value) +
                         '_VER_'+ str(detheight_start.value) + 'to' + str(detheight_end.value)+ '.txt')           
            
            det_roi_time = det_roi[timebin_start.value:timebin_end.value+1]
            det_roi_timebin = det_roi_time.intg(0)
            det_roi_timebin.axes[0].title = 'tube_height'
            det_roi_timebin.axes[1].title = 'tube_number'
            Plot1.set_dataset(det_roi_timebin)
            Plot1.title = filename + ': Detector image from time bin ' + str(timebin_start.value) + ' to ' + str(timebin_end.value)
            
            export_ascii_2D(det_roi_timebin, directory + '2D_' + filename +
                         '_TIME_'+ str(timebin_start.value) + 'to' + str(timebin_end.value) +
                         '_HOR_'+ str(dettube_start.value) + 'to' + str(dettube_end.value) +
                         '_VER_'+ str(detheight_start.value) + 'to' + str(detheight_end.value)+ '.txt')
            
            print ''
            print 'TOF of the detector image is exported'
            
            
            # integrate profile        
            det_roi_profile = det[:,
                       detheight_int_start.value:detheight_int_end.value+1,
                       dettube_int_start.value:dettube_int_end.value+1]
            det_roi_profile_timebin = det_roi_profile[timebin_start.value:timebin_end.value+1,:,:]
            
            Plot1.add_x_marker(dettube_int_start.value, 50, 'red')
            Plot1.add_x_marker(dettube_int_end.value, 50, 'red')
            Plot1.add_y_marker(detheight_int_start.value, 50, 'red')
            Plot1.add_y_marker(detheight_int_end.value, 50, 'red')
            
            print ''    
            print 'Detector image is exported'
                
            if str(integration_mode.value) == 'Tube Height':                                
                det_roi_profile_1D = det_roi_profile_timebin[:, :, :].sum(1)             
                det_roi_profile_1D.axes.title = 'tube_height'
                det_roi_profile_1D.title = 'intensity'
                
                Plot3.set_dataset(det_roi_profile_1D)
                Plot3.title = 'PROFILE. Tube Number: ' + str(dettube_int_start.value) + 'to' + str(dettube_int_end.value) + '. Time Bin:'+ str(timebin_start.value)+ 'to' + str(timebin_end.value)                              
                Plot3.x_label = str(det_roi_profile_1D.axes.title) #'tube height' # WHY IS THAT NECESSARY?                          
                
            if str(integration_mode.value) == 'Tube Number':                
                det_roi_profile_1D = det_roi_profile_timebin[:, :, :].sum(2)
                det_roi_profile_1D.axes.title = 'tube_number'
                det_roi_profile_1D.title = 'intensity'
                
                Plot3.set_dataset(det_roi_profile_1D)
                Plot3.title = 'PROFILE. Tube Height: ' + str(detheight_int_start.value) + 'to' + str(detheight_int_end.value) + '. Time Bin:'+ str(timebin_start.value)+ 'to' + str(timebin_end.value)                  
                Plot3.x_label = str(det_roi_profile_1D.axes.title) # 'tube number'# WHY IS THAT NECESSARY?                
            
            export_ascii_1D(det_roi_profile_1D, directory + 'PRO_' + filename +
                '_TIME_'+ str(timebin_start.value) + 'to' + str(timebin_end.value) +
                '_HOR_'+ str(dettube_int_start.value) + 'to' + str(dettube_int_end.value) +
                '_VER_'+ str(detheight_int_start.value) + 'to' + str(detheight_int_end.value)+ '.txt')
            
            print ''
            print 'Detector profile is exported'    
 
            # automatic export                                 
            if automatic_PROFILEexport.value:                                                         
                    number_of_bins = det_roi_profile.shape[0] // incr_timebins.value              
                    det_roi_profile_onebin = zeros([det_roi_profile.shape[1]])
                   
                    title = range(number_of_bins) # why do we need this? axes title doesn't seem to always work?!?
                    det_roi_profile_allbins = zeros([number_of_bins,det_roi_profile.shape[1]])
                    if str(integration_mode.value) == 'Tube Height':
                        det_roi_profile_allbins = zeros([number_of_bins,det_roi_profile.shape[1]])
                    if str(integration_mode.value) == 'Tube Number':
                        det_roi_profile_allbins = zeros([number_of_bins,det_roi_profile.shape[2]])    
                    
                    
                    
                    for i in range(number_of_bins):                       
                        istart = i*incr_timebins.value
                        iend = istart + incr_timebins.value
                        if str(integration_mode.value) == 'Tube Height':
                           det_roi_profile_onebin = det_roi_profile[istart:iend,:,:].sum(1)                        
                           det_roi_profile_allbins[i] = det_roi_profile_onebin
                           title [i] = 'fr_' + str(istart) + '_' + str(iend-1)
                           det_roi_profile_allbins.axes[1].title = 'detheight'
                        
                        
                        if str(integration_mode.value) == 'Tube Number':
                           det_roi_profile_onebin = det_roi_profile[istart:iend,:,:].sum(2)                        
                           det_roi_profile_allbins[i] = det_roi_profile_onebin
                           title [i] = 'fr_' + str(istart) + '_' + str(iend-1)
                           det_roi_profile_allbins.axes[1].title = 'detnumber'
                    
                    
            
                    
                    export_ascii_1D_all_timebins(det_roi_profile_allbins, directory + 'PRO_' + filename +
                         '_ALLTIMEBINS_'+ str(number_of_bins) +
                         '_HOR_'+ str(dettube_int_start.value) + 'to' + str(dettube_int_end.value) +
                         '_VER_'+ str(detheight_int_start.value) + 'to' + str(detheight_int_end.value)+ '.txt',
                         title)
                    
                    print ''
                    print 'Detector profile is exported in timebin increments of ' + str(incr_timebins.value)
                    print '-------------'
                    
def export_ascii_1D_all_timebins(ds, path, title):
        
    f = open(path, 'w')
    f.write ('%5s' % str(ds.axes[1].title)) 
    
    for i in range(ds.shape[0]):
            f.write('%12s' % str(title[i]))
    f.write('\n')
    for i in range(ds.shape[1]): # 82 detector height -> 82 lines
            f.write('%5g' % ds.axes[1][i])            
            for j in range(ds.shape[0]):
                f.write('%12g ' % ds[j][i])                
            f.write('\n')          
    f.close()

   
def export_ascii_1D(ds, path):
    f = open(path, 'w')    
    x = str(ds.axes[0].title)
    y = str(ds.title)       
    f.write("%s    %s" % (x, y) + '\n')
    for i in xrange(len(ds)):
       f.write("%5g %15g" % (ds.axes[0][i], ds.storage[i]) + '\n')            
    f.close()   
                    
def export_ascii_2D(ds, path, delimiter = ','):
    if ds.ndim != 2:
        raise Exception, 'wrong dimension, should be 2 instead of ' + str(ds.ndim)
    f = open(path, 'w')
    try:
        for i in xrange(len(ds)) : # note that this also gets rid of the brackets
            it = ds[i].item_iter()
            while it.has_next():
                f.write(str(it.next()) + delimiter)
            f.write('\n')
    finally:
        if f != None:
            f.close()                

    
def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
