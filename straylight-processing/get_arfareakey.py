from nustar_gen import wrappers, info, utils
import os
from astropy import units as u

#### This script is mostly code written by MCB, with some modifications by CJB

obsidnum = input('ObsID: ')
regfilename = input('Region file name: ' )
module = input('FPM: ')
eventfilename = f'nu{obsidnum}{module}01_cl_3to160_{regfilename.replace('.reg', '')}.evt'
det1expofilename = f'nu{obsidnum}{module}_det1_expo.fits'
phafilename = 'nu{obsidnum}{module}01_cl_3to160_{regfilename.replace('.reg', '')}_sr.pha'
arffilename = phafilename.replace('_sr.pha','.arf')

#top = some path to your top level data directory.
here = os.getcwd()+'/'
obs = info.Observation(seqid=obsidnum, path=here, evdir=f'./{obsidnum}/event_cl/', out_path=f'./{obsidnum}/event_cl/')


# You need to specify the location of the exposure map file produce by the script above:
mod = module
det1expo = os.path.join(obs.out_path, det1expofilename)
filt_ev = os.path.join(obs.evdir, eventfilename)
reg_file = os.path.join(obs.evdir, regfilename) ## acquired from user input
utils.make_straylight_arf(det1expo, reg_file, filt_ev, mod, obs=obs)

# This produces an ARF in obs.out_path

# You also need to know what the illuminated area is. Do that here:
area = utils.straylight_area(det1expo, reg_file, filt_ev)
print(f'Straylight area: {area:8.2f}')

# We're now ready for Xspec analysis, but you will need to load the ARF by hand after loading in the data.

# Finally, we want to update a few header keywords to make things work.

from astropy.io.fits import setval, getval

# Set your PHA file here:
pha_file = os.path.join(obs.out_path, phafilename)

# Target the SPECTRUM extension (which is #1)
ext=1
backscal = getval(pha_file, 'BACKSCAL', ext=ext)
print(f'Initial BACKSCAL value is meaninglss: {backscal}')

# Update it to be your straylight area value:
setval(pha_file, 'BACKSCAL', value=area.value, ext=ext)

backscal = getval(pha_file, 'BACKSCAL', ext=ext)
print(f'Confirm updated BACKSCAL value: {backscal}')

# Now also add on the ANCRFILE to point at the ARF:
# **NOTE** Figure out whether or not you want to have this be a realtive path or the *absolute* path to
# the ARF file


######## This should be the name of the arf file
arf_file = arffilename
# Update it to be your straylight area:
setval(pha_file, 'ANCRFILE', value=arf_file, ext=ext)

# You should be able to load things into Xspec now.
