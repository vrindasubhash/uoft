# CSC320 Spring 2024
# Assignment 3
# (c) Kyros Kutulakos
#
#
# UPLOADING THIS CODE TO GITHUB OR OTHER CODE-SHARING SITES IS
# STRICTLY FORBIDDEN.
#
# DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
# AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION
# BY KYROS KUTULAKOS IS STRICTLY FORBIDDEN. VIOLATION OF THIS
# POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY.
#
# THE ABOVE STATEMENTS MUST ACCOMPANY ALL VERSIONS OF THIS CODE,
# WHETHER ORIGINAL OR MODIFIED.

#
# DO NOT MODIFY THIS FILE
#



#
# This file defines a single class called InpaintingControl that
# is derived from the Inpainting class in file inpainting/algorithm.py
# Its purpose is three-fold:
#    (a) It isolates all inpainting-related functions and internal variables
#        from the GUI code
#    (b) It maintains two state variables that can be changed
#        through the GUI: the 'current mode' and the 'current image'
#        The 'current mode' controls which algorithm is run when we
#        press the Run button on the GUI. The 'current image' controls
#        (1) which image variable in the Inpainting class is changed when
#        we press the 'Image Open' button or (2) which image of the
#        inpainting class is saved to a file when we press the 'Image Save'
#        button
#    (c) It stores the various strings to be displayed by the GUI
#        for various modes, input/output images, etc.
#


import kivy
kivy.require('1.9.1')

from itertools import cycle
import sys

## import the Inpainting class and its methods

import sys
import argparse

parser = argparse.ArgumentParser(description="ArgumentParser for CSC320 Inpainting Assignment")    
parser.add_argument('--reference-solution', action='store_true', help='Set this to use the precompiled binary for the reference solution')
parser.add_argument('--usegui', action='store_true')
args = parser.parse_args()

if args.reference_solution:
    import sourcedefender
    print('*** Using Reference Solution ***')
    from binaries.algorithm import Inpainting
else:
    from inpainting.algorithm import Inpainting

class InpaintingControl(Inpainting):
    
    def __init__(self):
        Inpainting.__init__(self)
        # Specify the set of images relevant to each algorithm
        self._modes = {
            'Inpainting':dict(list(self.inpaintingInput().items()) + list(self.inpaintingOutput().items())), 
        }
        # Specify the set of input images expected by all algorithms
        self._inout = {
            'Input':dict(list(self.inpaintingInput().items())), 
            'Output':dict(list(self.inpaintingOutput().items()))
        }
        # Specify which method of Inpainting should be run in each mode
        # (this is a remnant from A1 Part B. there is only one method
        # implemented for inpainting)
        self._algorithm = {
            'Inpainting': self.exampleBasedInpainting,
        }
        
        # Define an iterator that allows us to switch between
        # the two modes of the GUI
        self._modeOrder = ['Inpainting']
        self._modeIter = cycle(self._modeOrder)
        self.nextMode()

    #
    # Top-level methods called when interacting with the GUI. These methods
    # are NOT called directly by the GUI, they are called by methods of 
    # the class RootWidget. 
    #
    
    # Run the algorithm associated with the current mode of the GUI
    def runAlgorithm(self, imviewer, maxIterations=None):
        return (self._algorithm[self._currentMode])(imviewer, maxIterations=maxIterations)

    # Cycle through the modes
    def nextMode(self):
        self._currentMode = next(self._modeIter)
        self._imageIter = cycle(self._sortByMsg(self._modes[self._currentMode]))
        self.nextImage()

    # Cycle through the images relevant to each mode
    def nextImage(self):
        self._currentImage = next(self._imageIter)

    # Load into the current image the file given by filename
    def load(self,filename):
        if self.isInputImage():
            self.setChangedInput()
            return self.readImage(filename, self._currentImage)
        else:
            return False, 'InpaintingInterface: %s is not an input image'%self._currentImage

    # Save the current image to the file given by filename
    def save(self,filename):
        if self.isOutputImage():
            return self.writeImage(filename, self._currentImage)
        else:
            return False, 'InpaintingInterface: %s is not an input image'%self._currentImage

    # Return the OpenCV image data structure for the current image
    def imageData(self):
        if self._currentImage in self._images:
            return self._images[self._currentImage]
        else:
            return None
            
    # Return the descriptor string for the current image
    def imageName(self):
        return self._currentImage
        

    #
    # Utility methods called by methods of the RootWidget class
    #

    # Return a string that describes the current mode
    def currentModeMsg(self):
        return self._currentMode
    # Return a string that describes the current image
    def currentImageMsg(self):
        return self._modes[self._currentMode][self._currentImage]['msg']
    # Return 'Open' if the current image is an input image and 'Save' otherwise
    def currentFileActionMsg(self):
        if self.isInputImage():
            return 'Open'
        else:
            return 'Save'
    # Return True if the current image is an input image
    def isInputImage(self):
        return self._currentImage in list(self._inout['Input'].keys())
    # Return True if the current image is an output image
    def isOutputImage(self):
        return self._currentImage in list(self._inout['Output'].keys())
    
    
    def _sortByMsg(self,modeDict):
        return [x[0] for x in sorted(list(modeDict.items()),key=lambda x:x[1]['msg'])]
    
    #
    # Define the descriptive text to be displayed for the various
    # input and output images 
    #
        
    def inpaintingInput(self): 
        return {
            'source':{'msg':'Source image','default':None},
            'alpha':{'msg':'Alpha matte','default':None},
        }
    # Same as above, but for the output arguments
    def inpaintingOutput(self): 
        return {
            'inpainted':{'msg':'Inpainted image','default':['inpainted.tif']},
            'fillFront':{'msg':'Fill front','default':['fillFront.tif']},
            'confidence':{'msg':'Confidence map','default':['confidence.tif']},
            'filled':{'msg':'Filled pixels','default':['confidence.tif']},
        }

