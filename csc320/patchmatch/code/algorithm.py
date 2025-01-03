# CSC320 Fall 2024
# Assignment 4
# (c) Olga (Ge Ya) Xu, Robin Swanson, Kyros Kutulakos
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

# Import basic packages.
from typing import List, Union, Tuple, Dict
import numpy as np

#
# Basic numpy configuration
#

# Set random seed.
np.random.seed(seed=131)
# Ignore division-by-zero warning.
np.seterr(divide="ignore", invalid="ignore")


# helpers for propogation_and_random_search

def is_valid_offset(offset, source_shape):
    # use source dimensions (height, width)
    height, width = source_shape.shape[:2]
    # check if the offset is within bounds of the source image
    return (0 <= offset[0] < width) and (0 <= offset[1] < height)

def clamp_offset(offset, source_shape):
    # clamp offset values to the source image dimensions
    # use clip function to make sure dimesions are in a valid range
    return np.clip(offset, [0, 0], [source_shape[1] - 1, source_shape[0] - 1])

def compute_similarity(patch1, patch2):
    # compute similarity (SSD) between two patches
    diff = patch1 - patch2
    return np.nansum(diff**2)  # use nan-aware sum to handle the borders


def propagation_and_random_search(
    source_patches: np.ndarray,
    target_patches: np.ndarray,
    f: np.ndarray,
    alpha: float,
    w: int,
    propagation_enabled: bool,
    random_enabled: bool,
    odd_iteration: bool,
    best_D: Union[np.ndarray, None] = None,
    global_vars: Union[Dict, None] = None,
) -> Tuple[np.ndarray, np.ndarray, Dict]:
    """
    Basic PatchMatch loop.

    This function implements the basic loop of the PatchMatch algorithm, as
    explained in Section 3.2 of the paper. The function takes an NNF f as
    input, performs propagation and random search, and returns an updated NNF.

    Args:
        source_patches:
            A numpy matrix holding the patches of the color source image,
              as computed by the make_patch_matrix() function in this module.
              For an NxM source image and patches of width P, the matrix has
              dimensions NxMxCx(P^2) where C is the number of color channels
              and P^2 is the total number of pixels in the patch.  For
              your purposes, you may assume that source_patches[i,j,c,:]
              gives you the list of intensities for color channel c of
              all pixels in the patch centered at pixel [i,j]. Note that patches
              that go beyond the image border will contain NaN values for
              all patch pixels that fall outside the source image.
        target_patches:
            The matrix holding the patches of the target image, represented
              exactly like the source_patches argument.
        f:
            The current nearest-neighbour field.
        alpha:
            Algorithm parameter, as explained in Section 3 and Eq.(1).
        w:
            Algorithm parameter, as explained in Section 3 and Eq.(1).
        propagation_enabled:
            If True, propagation should be performed. Use this flag for
              debugging purposes, to see how your
              algorithm performs with (or without) this step.
        random_enabled:
            If True, random search should be performed. Use this flag for
              debugging purposes, to see how your
              algorithm performs with (or without) this step.
        odd_iteration:
            True if and only if this is an odd-numbered iteration.
              As explained in Section 3.2 of the paper, the algorithm
              behaves differently in odd and even iterations and this
              parameter controls this behavior.
        best_D:
            And NxM matrix whose element [i,j] is the similarity score between
              patch [i,j] in the source and its best-matching patch in the
              target. Use this matrix to check if you have found a better
              match to [i,j] in the current PatchMatch iteration.
        global_vars:
            (optional) if you want your function to use any global variables,
              return them in this argument and they will be stored in the
              PatchMatch data structure.

    Returns:
        A tuple containing (1) the updated NNF, (2) the updated similarity
          scores for the best-matching patches in the target, and (3)
          optionally, if you want your function to use any global variables,
          return them in this argument and they will be stored in the
          PatchMatch data structure.
    """
    new_f = f.copy()

    #############################################
    if best_D is not None:
       new_best_D = best_D.copy()
    else:
       # best_D is None so initialize it with infinite values to show no valid distances have been computed yet
       new_best_D = np.full(f.shape[:2], np.inf)

    height, width, _ = f.shape

    # propgation behavior depends on if youre in a odd or even iteration
       # if you are on an odd iteration you scan top left to bottom right
          # use offsets from the left neighbor and top neighbor
          # use these offsets to compute candidate matches in the source image
          # if a neighbors source patch matches better than the current offset, update the NNF for the current patch
       # if you are on an even iteration you scan bottom right to top left
          # use offsets from right neighbor and bottom neighbor to compute candidate matches

    if odd_iteration:
       # odd iteration (use left and top neighbors)
       directions = ((0,-1), (-1,0))
       x_range = range(width)
       y_range = range(height)
    else: 
       # even iteration (use right and bottom neighbors)
       directions = ((0,1), (1,0))
       x_range = range(width - 1, -1, -1)
       y_range = range(height - 1, -1, -1)


    # loop through all of the patches in the target image
    for y in y_range:
       for x in x_range:
          # propapgation step is enabled, process patches in a scan order
          if propagation_enabled:
             for dx, dy in directions:
                # add the direction offsets to the x and y to get the neighbors coordinates
                nx, ny = x + dx, y + dy
                # check if the neighbor is within the valid image dimensions
                if 0 <= nx < width and 0 <= ny < height:
                   # compute the offset of the near by pixel as it could be helpful for the pixel in source[x.y]
                   candidate_offset = f[ny, nx] + np.array([-dy, -dx])
                   # verify if the candidate offset is valid (within source patches)
                   if is_valid_offset(candidate_offset, source_patches):
                      # compute the similarity between the target patch and the source patch at the candidate offset
                      candidate_D = compute_similarity(target_patches[y,x], source_patches[candidate_offset[1], candidate_offset[0]])
                      # update best offset and similarity if the candidate is better
                      if new_best_D[y,x] > candidate_D:
                         new_f[y,x] = candidate_offset
                         new_best_D[y,x] = candidate_D

          # random search step is enabled
          if random_enabled:
             radius = w # radius starts as max search radius w
             best_offset = new_f[y, x] # best offset is initialized as current best offset/current offset
             # keep examining patches until the radius is below 1 pixel
             while radius >= 1:
                # generate candidate offset using a random vector (between [-1,1]) scaled by the current radius
                random_offset = best_offset + (radius * np.random.uniform(-1, 1, size=2)).astype(int)
                # clamp candidate offset to make sure its within the bounds of the source image
                random_offset = clamp_offset(random_offset, source_patches.shape[:2])
                # check if the candidate offset is valid (corresponds to a valid source patch)
                if is_valid_offset(random_offset, source_patches):
                   # compute the similarity (patch distance) between the target and source patches
                   random_D = compute_similarity(target_patches[y, x], source_patches[random_offset[1], random_offset[0]])
                   # if any random offset improves the match, update the NNF and similarity score
                   if new_best_D[y, x] > random_D:
                      new_f[y, x] = random_offset
                      new_best_D[y, x] = random_D
                # reduce the radius exponentially (by alpha after each test)
                radius *= alpha

    #############################################
    return new_f, best_D, global_vars


def reconstruct_source_from_target(target: np.ndarray, f: np.ndarray) -> np.ndarray:
    """
    Reconstruct a source image using pixels from a target image.

    This function uses a computed NNF f(x,y) to reconstruct the source image
    using pixels from the target image.  To reconstruct the source, the
    function copies to pixel (x,y) of the source the color of
    pixel (x,y)+f(x,y) of the target.

    The goal of this routine is to demonstrate the quality of the
    computed NNF f. Specifically, if patch (x,y)+f(x,y) in the target image
    is indeed very similar to patch (x,y) in the source, then copying the
    color of target pixel (x,y)+f(x,y) to the source pixel (x,y) should not
    change the source image appreciably. If the NNF is not very high
    quality, however, the reconstruction of source image
    will not be very good.

    You should use matrix/vector operations to avoid looping over pixels,
    as this would be very inefficient.

    Args:
        target:
            The target image that was used as input to PatchMatch.
        f:
            A nearest-neighbor field the algorithm computed.
    Returns:
        An openCV image that has the same shape as the source image.
    """
    rec_source = None

    #############################################
    # get dimensions of target image
    h, w, _ = target.shape

    # make a coordinate matrix for the pixel positions of same shape as target image
    coords = make_coordinates_matrix((h, w))  # shape (h, w)

    # add NNF offsets to coordinates
    target_coords = coords + f

    # clip target coordinates to make sure they are in the image bounds
    # make sure the coordinates are between 0 and h - 1 and w - 1 
    target_y = np.clip(target_coords[..., 0], 0, h - 1).astype(int)
    target_x = np.clip(target_coords[..., 1], 0, w - 1).astype(int)

    # use indexing to map the target pixels to the source image
    rec_source = target[target_y, target_x]  
    #############################################

    #############################################

    return rec_source


def make_patch_matrix(im: np.ndarray, patch_size: int) -> np.ndarray:
    """
    PatchMatch helper function.

    This function is called by the initialized_algorithm() method of the
    PatchMatch class. It takes an NxM image with C color channels and a patch
    size P and returns a matrix of size NxMxCxP^2 that contains, for each
    pixel [i,j] in the image, the pixels in the patch centered at [i,j].

    You should study this function very carefully to understand precisely
    how pixel data are organized, and how patches that extend beyond
    the image border are handled.

    Args:
        im:
            A image of size NxM.
        patch_size:
            The patch size.

    Returns:
        A numpy matrix that holds all patches in the image in vectorized form.
    """
    phalf = patch_size // 2
    # create an image that is padded with patch_size/2 pixels on all sides
    # whose values are NaN outside the original image
    padded_shape = (
        im.shape[0] + patch_size - 1,
        im.shape[1] + patch_size - 1,
        im.shape[2],
    )
    padded_im = np.zeros(padded_shape) * np.nan
    padded_im[phalf : (im.shape[0] + phalf), phalf : (im.shape[1] + phalf), :] = im

    # Now create the matrix that will hold the vectorized patch of each pixel.
    # If the original image had NxM pixels, this matrix will have
    # NxMx(patch_size*patch_size) pixels
    patch_matrix_shape = im.shape[0], im.shape[1], im.shape[2], patch_size**2
    patch_matrix = np.zeros(patch_matrix_shape) * np.nan
    for i in range(patch_size):
        for j in range(patch_size):
            patch_matrix[:, :, :, i * patch_size + j] = padded_im[
                i : (i + im.shape[0]), j : (j + im.shape[1]), :
            ]

    return patch_matrix


def make_coordinates_matrix(im_shape: Tuple, step: int = 1) -> np.ndarray:
    """
    PatchMatch helper function.

    This function returns a matrix g of size (im_shape[0] x im_shape[1] x 2)
    such that g(y,x) = [y,x].

    Pay attention to this function as it shows how to perform these types
    of operations in a vectorized manner, without resorting to loops.

    Args:
        im_shape:
            A tuple that specifies the size of the input images.
        step:
            (optional) If specified, the function returns a matrix that is
              step times smaller than the full image in each dimension.
    Returns:
        A numpy matrix holding the function g.
    """
    range_x = np.arange(0, im_shape[1], step)
    range_y = np.arange(0, im_shape[0], step)
    axis_x = np.repeat(range_x[np.newaxis, ...], len(range_y), axis=0)
    axis_y = np.repeat(range_y[..., np.newaxis], len(range_x), axis=1)

    return np.dstack((axis_y, axis_x))
