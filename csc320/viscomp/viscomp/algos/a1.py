# CSC320 Fall 2022
# Assignment 1
# (c) Kyros Kutulakos, Towaki Takikawa, Esther Lin
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

import numpy as np
import cv2
import viscomp.ops.image as img_ops
from typing import Any, Optional
import numpy.typing as npt
import pdb
import sys

def run_a1_algo(
    source_image: npt.NDArray[np.float32],
    destination_image: npt.NDArray[np.float32],
    source_coords: npt.NDArray[np.float32],
    destination_coords: npt.NDArray[np.float32],
    homography: Optional[npt.NDArray[np.float32]] = None,
) -> npt.NDArray[np.float32]:
    """Run the entire A1 algorithm.

    Args:
        source_image (np.ndarray): The source image of shape [Hs, Ws, 4]
        destination_image (np.ndarray): The destination image of shape [Hd, Wd, 4]
        source_coords (np.ndarray): [4, 2] matrix of 2D coordinates in the source image.
        destination_coords (np.ndarray): [4, 2] matrix of 2D coordinates in the destination image.
        homography (np.ndarray): (Optional) [3, 3] homography matrix. If passed in, will use this
            instead of calculating it.

    Returns:
        (np.ndarray): Written out image of shape [Hd, Wd, 4]
    """

    if homography is None:
        print("Calculating homography...")
        np.set_printoptions(formatter={"float": "{:.4f}".format})
        homography = calculate_homography(source_coords, destination_coords)
    else:
        print("Using preset homography matrix...")

    print(f"Homography matrix:\n{homography}\nPerforming backward mapping...")
    output_buffer = backward_mapping(
        homography, source_image, destination_image, destination_coords
    )

    print("Algorithm has succesfully finished running!")
    return output_buffer


def convex_polygon(
    poly_coords: npt.NDArray[np.float32], image_coords: npt.NDArray[np.float32]
) -> npt.NDArray[np.float32]:
    """From coords that define a convex hull, find which image coordinates are inside the hull.

    Args:
        poly_coords (np.ndarray): [N, 2] list of 2D coordinates that define a convex polygon.
                             Each nth index point is connected to the (n-1)th and (n+1)th
                             point, and the connectivity wraps around (i.e. the first and last
                             points are connected to each other)
        image_coords (np.ndarray): [H, W, 2] array of coordinates on the image. Using this,
                                the goal is to find which of these coordinates are inside
                                the convex hull of the polygon.
        Returns:
            (np.ndarray): [H, W] boolean mask where True means the coords is inside the hull.
    """
    mask = np.ones_like(image_coords[..., 0]).astype(bool)
    N = poly_coords.shape[0]
    for i in range(N):
        dv = poly_coords[(i + 1) % N] - poly_coords[i]
        winding = (image_coords - poly_coords[i][None]) * (np.flip(dv[None], axis=-1))
        winding = winding[..., 0] - winding[..., 1]
        mask = np.logical_and(mask, (winding > 0))

    return mask


""" Student implementation starts here:
"""


def calculate_homography(
    source: npt.NDArray[np.float32], destination: npt.NDArray[np.float32]
) -> npt.NDArray[Any]:
    """Calculate the homography matrix based on source and desination coordinates.
    Args:
        source (np.ndarray): [4, 2] matrix of 2D coordinates in the source image.
        destination (np.ndarray): [4, 2] matrix of 2D coordinates in the destination image.
    Returns:
        (np.ndarray): [3, 3] homography matrix.
    """

    ################################
    ####### PUT YOUR CODE HERE #####
    ################################

    # The idea is to loop through the 4 pairs of corresponding points between the source and destination images. 
    # For each pair of points, we will derive 2 equations: 
    #   - One equation for the x-coordinate in the destination image.
    #   - One equation for the y-coordinate in the destination image.
    #
    # Each pair of points generates these two equations, leading to a total of 8 equations. 
    # These 8 equations correspond to the 8 unknowns in the homography matrix (a, b, c, d, e, f, h, k), 
    # which map the source image coordinates to the destination image coordinates.
    #
    # Each equation is based on the coordinates of the source image (x_i, y_i) and involves the unknown homography matrix coefficients.
    # These equations are then set equal to their corresponding coordinates in the destination image (x'_i, y'_i).
    #
    # Once we have the system of 8 equations, we use NumPy’s linear algebra solver to solve for the 8 unknown homography matrix values.
    # Then we will add 1 to the end of matrix and reshape to 3x3.
    # 
    # Once we have the matrix, we use NumPy's linear algebra solver to create the inverse of the matrix.   
    # Then we normalize it by the last value (2,2) and we have the inverse homography matrix. 
    
  
    
    coefficients = []
    results = []

    # loop through the 4 pairs of points
    for i in range(4):
        # save the coordinates for the source points (x_i, y_i)
        x, y = source[i]
        # save the coordinates for the destination points (x'_i, y'_i)
        x_dest, y_dest = destination[i]
  
        # add the coefficients for the equation for x_'i (first equation)
        coefficients.append([x, y, 1, 0, 0, 0, -x * x_dest, -y * x_dest])
        # add the coefficients for the equation for y_'i (second equation)
        coefficients.append([0, 0, 0, x, y, 1, -x * y_dest, -y * y_dest])
      

        # add the destination x'_i for the result vector (for the first equation)
        results.append(x_dest)
        # add the destination y'_i for the result vector (for the second equation)
        results.append(y_dest)

    # convert the coefficient and result lists to NumPy arrays for easier matrix operations
    coefficients = np.array(coefficients, dtype=np.float32)
    results = np.array(results, dtype=np.float32)
  
    # solve the system of equations (Ax = B) to find the 8 unknown homography coefficients
    # A has the coefficients (a 2D array of shape 8x8 for the 8 equations with the 8 coefficients for the unknowns: a, b, c, d, e, f, h, k)
    # x is the vector of the unknown homography coefficients [a, b, c, d, e, f, h, k]
    # B has the results (a 1D array of shape (8,) for the 8 destination coordinates - x_i' and y_i')
    homography = np.linalg.lstsq(coefficients, results, rcond=None)[0]

    # append the [1] to make the matrix a 3x3 homography matrix and reshape it
    homography = np.append(homography, 1)
    homography = homography.reshape(3,3)

    # find the inverse matrix and normalize it by the last value (to use for backward mapping)
    homography = np.linalg.inv(homography)
    homography /= homography[2][2]
    

    # homography = np.eye(3)
    #################################
    ######### DO NOT MODIFY #########
    #################################
    return homography




def backward_mapping(
    transform: npt.NDArray[np.float32],
    source_image: npt.NDArray[np.float32],
    destination_image: npt.NDArray[np.float32],
    destination_coords: npt.NDArray[np.float32],
) -> npt.NDArray[np.float32]:
    """Perform backward mapping onto the destination image.

    The goal of this function is to map each destination image pixel which is within the polygon
    defined by destination_coords to a corresponding image pixel in source_image.
    Hints: Start by iterating through the destination image pixels using a nested for loop. For each
    pixel, use the convex_polygon function to find whether they are inside the polygon. If they are,
    figure out how to use the homography matrix to find the corresponding pixel in source_image.

    Args:
        transform (np.ndarray): [3, 3] homogeneous transformation matrix.
        source_image (np.ndarray): The source image of shape [H, W, 4]
        destination_image (np.ndarray): The destination image of shape [H, W, 4]
        source_coords (np.ndarray): [4, 2] matrix of 2D coordinates in the source image.
        destination_coords (np.ndarray): [4, 2] matrix of 2D coordinates in the destination image.

    Returns:
        (np.ndarray): [N, 2] matrix of transformed coordinates.
    """
    h, w, _ = destination_image.shape
    output_buffer = np.zeros_like(destination_image)

    # The integer coordinates which you can access via xs_int[r, c]
    xs_int = img_ops.create_coordinates(h, w)

    ################################
    ####### PUT YOUR CODE HERE #####
    ################################
   
    # Idea is to go through pixels in the mask (in the destination image)
    # Get the destination pixel, transform to homogeneous to apply the inverse matrix
    # Normalize to get back to cartesian to get source coordinates
    # If coordinates are in range, add to output buffer (map back to destination) 

    # transform is the inverse homography matrix (renamed for clarity)
    h_inverse = transform

    # use the convex_polygon function to make a mask for the pixels in the polygon
    mask = convex_polygon(destination_coords, xs_int) 

    # One way you can implement this is with a double for loop, like the following.
    # You DO NOT necessarily need to implement it in this way... you can implement
    # this entire assignment pretty easily by utilizing vectorization.
    # As of matter fact, I (the TA) personally think that the vectorized version of the
    # code is simpler and less lines of code than the double for loop version.
    # That being said if you still don't find vectorization natural, go ahead and attempt
    # the double for loop solution!
    for r in range(h):
        # The double for loop is slow, so we implement a progress bar.a
        # tqdm (a progress bar library) doesn't work great with certain GUI libraries,
        # so we implment our own progress bar here.
        # you should ignore this code for the most part.
        sys.stdout.write("\x1b[1A")
        sys.stdout.write("\x1b[2K")
        percent_done = float(r) / float(h - 1)
        print(
            f"[{'#' * int(percent_done*30)}{'-' * (30-int(percent_done*30))}] {int(100*percent_done)}% done"
        )
        # loop through each pixel inside the polygon where the mask is true
        for c in range(w):
            if mask[r,c]:
               # get the pixel in the destination image at coordinates (x,y)
               pixel_coord = xs_int[r, c]
            # Do stuff here!
 
               # convert the destination pixel (x,y) to homogeneous coordinates [x,y,1]
               dest_coord_homog = np.array([pixel_coord[0], pixel_coord[1], 1]) 
               
               # apply the inverse homography matrix to the destination coordinates to get the corresponding source pixel
               source_coord = h_inverse @ dest_coord_homog
               # normalize to get back to cartesian coordinates
               source_coord = source_coord/source_coord[2]
  
               # get the source pixel coordinates (rounded to the nearest integer to properly map)
               source_coord_x = int(round(source_coord[0]))
               source_coord_y = int(round(source_coord[1]))
 
               # make sure that the coordinates are in the bounds of the source images 
               if 0 <= source_coord_x < source_image.shape[1] and 0 < source_coord_y < source_image.shape[0]:
                  # map the source pixel to the destination image
                  output_buffer[r,c] = source_image[source_coord_y, source_coord_x]
               
           
    #################################
    ######### DO NOT MODIFY #########
    #################################
    return output_buffer


