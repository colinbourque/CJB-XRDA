from importlib import reload
import nustar_gen as nsg
from nustar_gen import info
from nustar_gen import wrappers
reload(wrappers)
import os
here = os.getcwd()+'/'

import subprocess
from subprocess import DEVNULL, STDOUT

#### This script is entirely written by RML: it is included here for completeness in the processing files

# Required to run heasoft stuff in the background

#%env HEADASNOQUERY=
#%env HEADASPROMPT=/dev/null

seqid=input("Enter the ObsID: ")  #sequence ID for observation of interest

obs = info.Observation(path=here, seqid=seqid, evdir=here+'/'+seqid+'/event_cl')
#obs.evtfiles['A'][0]
#obs.exposure_report()
#print(obs.observation_date)

# Make a 3--20 keV image and a 20--40 keV image for both FPMs
print(f'Output images are produced here: {obs.out_path}')

# Set up an outdir
outdir = os.path.join(obs.path+'/'+seqid+'/'+'event_cl')
print(outdir)

# Make the directory if it doesn't already exist
try:
    os.path.isdir(outdir)
except:
    print()



for mod in ['A', 'B']:
    nsg.wrappers.make_image(infile=obs.evtfiles[mod][0], elow=3, ehigh=20)
    nsg.wrappers.make_image(infile=obs.evtfiles[mod][0], elow=20, ehigh=40)
    
    


for mod in ['A', 'B']:
    ev = obs.evtfiles[mod][0]
    reg_file = os.path.join(obs.path+'/'+seqid+'/'+'event_cl/', f'skysrc{mod}.reg')
    print(reg_file)
    outscr = nsg.wrappers.make_spectra(ev, mod, reg_file, bgd_reg='None', runmkarf='no', extended='yes', outpath=outdir)
    print(outscr)
