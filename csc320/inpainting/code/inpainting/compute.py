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
# DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
#

import numpy as np
import cv2 as cv

# File psi.py define the psi class. You will need to 
# take a close look at the methods provided in this class
# as they will be needed for your implementation
from inpainting import psi        

# File copyutils.py contains a set of utility functions
# for copying into an array the image pixels contained in
# a patch. These utilities may make your code a lot simpler
# to write, without having to loop over individual image pixels, etc.
from inpainting import copyutils

#########################################
from inpainting.copyutils import getWindow
from inpainting.copyutils import outerBorderCoords

#########################################

# If you need to import any additional packages
# place them here. Note that the reference 
# implementation does not use any such packages

#########################################


#########################################
#
# Computing the Patch Confidence C(p)
#
# Input arguments: 
#    psiHatP: 
#         A member of the PSI class that defines the
#         patch. See file inpainting/psi.py for details
#         on the various methods this class contains.
#         In particular, the class provides a method for
#         accessing the coordinates of the patch center, etc
#    filledImage:
#         An OpenCV image of type uint8 that contains a value of 255
#         for every pixel in image I whose color is known (ie. either
#         a pixel that was not masked initially or a pixel that has
#         already been inpainted), and 0 for all other pixels
#    confidenceImage:
#         An OpenCV image of type uint8 that contains a confidence 
#         value for every pixel in image I whose color is already known.
#         Instead of storing confidences as floats in the range [0,1], 
#         you should assume confidences are represented as variables of type 
#         uint8, taking values between 0 and 255.
#
# Return value:
#         A scalar containing the confidence computed for the patch center
#

def computeC(psiHatP=None, filledImage=None, confidenceImage=None):
    assert confidenceImage is not None
    assert filledImage is not None
    assert psiHatP is not None
    
    #########################################
    # get the coordinates and radius of the patch
    center = psiHatP._coords
    w = psiHatP._w

    # use getWindow to get the confidence values inside the patch
    patch_confidence, valid = getWindow(confidenceImage, center, w)

    # use getWindow to figure out which pixels are filled
    filled_patch, _ = getWindow(filledImage, center, w)

    # compute the total confidence of known (filled) pixels
    known_pixels = (filled_patch > 0)
    total_confidence = np.sum(patch_confidence[known_pixels])
    #########################################
    
    # Replace this dummy value with your own code
    # normalize the total confidence by the total number of pixels in the patch
    # C is the average confidence for the patch
    C = total_confidence / (2 * w + 1) ** 2
    #########################################
    
    return C

#########################################
#
# Computing the max Gradient of a patch on the fill front
#
# Input arguments: 
#    psiHatP: 
#         A member of the PSI class that defines the
#         patch. See file inpainting/psi.py for details
#         on the various methods this class contains.
#         In particular, the class provides a method for
#         accessing the coordinates of the patch center, etc
#    filledImage:
#         An OpenCV image of type uint8 that contains a value of 255
#         for every pixel in image I whose color is known (ie. either
#         a pixel that was not masked initially or a pixel that has
#         already been inpainted), and 0 for all other pixels
#    inpaintedImage:
#         A color OpenCV image of type uint8 that contains the 
#         image I, ie. the image being inpainted
#
# Return values:
#         Dy: The component of the gradient that lies along the 
#             y axis (ie. the vertical axis).
#         Dx: The component of the gradient that lies along the 
#             x axis (ie. the horizontal axis).
#
    
def computeGradient(psiHatP=None, inpaintedImage=None, filledImage=None):
    assert inpaintedImage is not None
    assert filledImage is not None
    assert psiHatP is not None
    
    #########################################
    # get the patch using the PSI class method
    patch, _ = psiHatP.pixels(returnValid=True)
 
    # convert the patch to grayscale
    grayscale_patch = cv.cvtColor(patch, cv.COLOR_BGR2GRAY)

    # calculate gradients using the Sobel operator
    # the Sobel operator highlights areas of quick intensity change (often correspond to edges in an image)
    # ksize = 3 means use a 3x3 convolution kernel 
    grad_x = cv.Sobel(grayscale_patch, cv.CV_64F, 1, 0, ksize=3) # first derivative in the x direction (horizontal edges)
    grad_y = cv.Sobel(grayscale_patch, cv.CV_64F, 0, 1, ksize=3) # first derivative in the y direction (vertical edges)

    # calculate the gradient magnitude and mask out unfilled pixels
    grad_magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)

    # get the filled pixels in the patch
    filled_patch = psiHatP.filled()
 
    grad_magnitude[filled_patch == 0] = -1  # mask unfilled pixels

    # find the index of the maximum valid gradient
    max_index = np.argmax(grad_magnitude)
    #########################################
    
    # Replace these dummy values with your own code
    # get the parts of the gradient where the gradient magnitude is the largest
    Dy = grad_y.flat[max_index]
    Dx = grad_x.flat[max_index]
    #########################################
    
    return Dy, Dx

#########################################
#
# Computing the normal to the fill front at the patch center
#
# Input arguments: 
#    psiHatP: 
#         A member of the PSI class that defines the
#         patch. See file inpainting/psi.py for details
#         on the various methods this class contains.
#         In particular, the class provides a method for
#         accessing the coordinates of the patch center, etc
#    filledImage:
#         An OpenCV image of type uint8 that contains a value of 255
#         for every pixel in image I whose color is known (ie. either
#         a pixel that was not masked initially or a pixel that has
#         already been inpainted), and 0 for all other pixels
#    fillFront:
#         An OpenCV image of type uint8 that whose intensity is 255
#         for all pixels that are currently on the fill front and 0 
#         at all other pixels
#
# Return values:
#         Ny: The component of the normal that lies along the 
#             y axis (ie. the vertical axis).
#         Nx: The component of the normal that lies along the 
#             x axis (ie. the horizontal axis).
#
# Note: if the fill front consists of exactly one pixel (ie. the
#       pixel at the patch center), the fill front is degenerate
#       and has no well-defined normal. In that case, you should
#       set Nx=None and Ny=None
#

def computeNormal(psiHatP=None, filledImage=None, fillFront=None):
    assert filledImage is not None
    assert fillFront is not None
    assert psiHatP is not None

    #########################################
    # get the coordinates and radius of the patch
    center = psiHatP._coords
    w = psiHatP._w

    # get the outer border coordinates of the patch
    border_coords = outerBorderCoords(fillFront, center, w)

    # fill front has only one pixel at the patch center
    if len(border_coords) == 0:
        return None, None  # degenerate case

    # compute differences between border pixels and the center
    # (gets the vectors pointing from the patch center to each border pixel)
    differences = np.array(border_coords) - np.array(center)
 
    # taking the mean of differences gives an average direction pointing out from the patch center toward the fill front
    # this is an approximation of the tangent at the patch center
    tangent = np.mean(differences, axis=0)

    # get the magnitude (length) of the tangent vector
    tangent_magnitude = np.linalg.norm(tangent)
    #########################################
    
    # Replace these dummy values with your own code

    # get the nromal vectors to the tangent by rotating them
    # normalize by the tangents magnitude 
    Ny = -tangent[0] / tangent_magnitude
    Nx = tangent[1] / tangent_magnitude 
    #########################################

    return Ny, Nx
