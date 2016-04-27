# Script control setup area
# script info
__script__.title = 'Collect Data'
__script__.version = '1.0'

# Use below example to create parameters.
# The type can be string, int, float, bool, file.
mode = Par('str', 'unlimited', options = ['unlimited', 'time', 'count'])
preset = Par('float', 0)

# Use below example to create a button
act1 = Act('act1_changed()', 'Start') 
def act1_changed():
    sics.execute('histmem mode ' + str(mode.value))
    sics.execute('histmem preset ' + str(preset.value))
    sics.execute('histmem start')
    
act2 = Act('act2_changed()', 'Stop and Save') 
def act2_changed():
    sics.execute('newfile histogram_xyt')
    sics.execute('save')
    sics.execute('histmem stop')
    
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
