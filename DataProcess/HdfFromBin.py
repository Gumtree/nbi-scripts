# Script control setup area
# script info
__script__.title = '<Script Template>'
__script__.version = '1.0'

SOURCE_PATH = 'Z:/kowari/data/current'
START_NUM = 58201
END_NUM = 60186
BIN_PREFIX = 'DATASET_'
BIN_FILENAME = 'HDS_P0.nx.hdf'


# Use below example to create parameters.
# The type can be string, int, float, bool, file.
num_entries = Par('int', 72)
base_file = Par('string', 'Z:/kowari/data/current/KWR0058602.nx.hdf')
bin_folder = Par('string', 'W:/data/kowari/lost/DAQ_2016-01-22T07-00-43')
target_file = Par('string', 'KWR0070043.nx.hdf')

# Use below example to create a button
act1 = Act('find_num_file()', 'Find file with same number of frames') 
def find_num_file():
    for i in xrange(END_NUM - START_NUM + 1):
        num = START_NUM + i
        fn = SOURCE_PATH + '/' + 'KWR00' + str(num) + '.nx.hdf'
        ds = df[str(fn)]
        if len(ds) == num_entries.value:
            base_file.value = fn
            print 'found at ' + fn
            break
        ds.close()
        df.datasets.clear()
        
act2 = Act('create_hdf()', 'Make new HDF file')
def create_hdf():
    ds = df[str(base_file.value)]
    for i in xrange(num_entries.value):
        bin_file = bin_folder.value + '/' + BIN_PREFIX + str(i) + '/' + BIN_FILENAME
        bin = df[str(bin_file)]
        hmm_xy = bin['/entry1/data/hmm_xy_uncal']
        ds[i, 0] = hmm_xy
        bin.close()
    ds.save_copy(str(bin_folder.value + '/' + target_file.value))
    
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
    
def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
