from nustar_gen import wrappers, info, utils
import os

#### This file primarily uses code written by MCB, with some modifications by CJB

obsidnum = str(input('Please provide OBSID number: '))

here = os.getcwd()+'/'
obs = info.Observation(seqid=obsidnum, path=here, evdir=f'./{obsidnum}/event_cl', out_path=f'./{obsidnum}/event_cl/')
# Below spawns an Xselect instance behind the scenes.
# This produces an image in DET1 coordinates, which looks like the image below when you open it in ds9

evfA = obs.evtfiles['A'][0]
det1A_file = wrappers.make_det1_image(evfA, elow=3, ehigh=20)

evfB = obs.evtfiles['B'][0]
det1B_file = wrappers.make_det1_image(evfB, elow=3, ehigh=20)
