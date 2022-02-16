import math
from PIL import Image

# CODE FROM LAB 1 (replace with your code)

def inverted(image):
    returnImage = {
        'width': image['width'],
        'height': image['height'],
        'pixels': [255-i for i in image['pixels']]
    }
    return returnImage

def correlate(image, kernel, noClip = False):
    # Assertions to make sure the code will run properly.
    assert 'width' in kernel, "The image kernel is missing 'width'"
    assert 'height' in kernel, "The image kernel is missing 'height'"
    assert 'pixels' in kernel, "The image kernel is missing 'pixels'"
    #assert kernel['width'] <= image['width'], "the kernel must be smaller than the image"
    #assert kernel['height'] <= image['height'], "the kernel must be smaller than the image"
    assert kernel['width']%2 != 0, "the kernel must have an odd size in order to have a center"
    assert kernel['height']%2 != 0, "the kernel must have an odd size in order to have a center"

    ySpace = kernel['height']//2
    xSpace = kernel['width']//2

    newImage = {
        'height': image['height'],
        'width': image['width'],
        'pixels': []
    }

    for ph in range(image['height']):
        for pw in range(image['width']):
            newValue = 0
            for h in range(kernel["height"]):
                for w in range(kernel["width"]):
                    xTestMin = pw%image['width']-xSpace+w
                    yTestMin = ph%image['height']-ySpace+h
                    xTestMax = pw%image['width']-xSpace+w-image['width']+1
                    yTestMax = ph%image['height']-ySpace+h-image['height']+1

                    kValue = kernel['width']*h+w
                    iValue = (image['width']*ph+pw)-(ySpace*image['width']+xSpace)+(image['width']*h+w)

                    if(xTestMin < 0):
                        iValue -= xTestMin
                    if(yTestMin < 0):
                        iValue -= yTestMin*image["width"]
                    if(yTestMax > 0):
                        iValue -= yTestMax*image["width"]
                    if(xTestMax > 0):
                        iValue -= xTestMax
                    newValue += kernel['pixels'][kValue]*image['pixels'][iValue]
            if (newValue > 255 and noClip == False):
                newValue = 255
            elif (newValue < 0 and noClip == False):
                newValue = 0
            if(noClip == False):
                newImage['pixels'].append(round(newValue))
            else:
                newImage['pixels'].append(newValue)

    return newImage

def round_and_clip_image(image):
    pic = image.copy()
    returnList = []
    for i in pic['pixels']:
        if(i < 0):
            i = 0
        elif(i > 255):
            i = 255
        i = round(i)
        returnList.append(i)

    returnImage = {
        'width': image['width'],
        'height': image['height'],
        'pixels': returnList
    }
    return returnImage

def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    pic = image #load_image('test_images/pigbird.png')
    value = 1/(n*n)
    kernel = {
    'width': n,
    'height': n,
    'pixels': [value for i in range(n*n)]
    }
    mutatedPic = correlate(pic, kernel)
    #save_image(mutatedPic, 'mutatedpigbird.png')
    return mutatedPic

def sharpened(image, n):
    pic = image #load_image('test_images/pigbird.png')
    value = 1/(n*n)
    pList = [-value for i in range(n*n)]
    if(len(pList) > 1):
        pList[len(pList)//2] += 2
    else:
        pList[0] += 2
    kernel = {
    'width': n,
    'height': n,
    'pixels': pList
    }
    mutatedPic = correlate(pic, kernel)
    #save_image(mutatedPic, 'mutatedpigbird.png')
    return mutatedPic

def edges(image, saveImages = False):
    pic = image
    k1 = {
    'width': 3,
    'height': 3,
    'pixels': [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    }
    k2 = {
    'width': 3,
    'height': 3,
    'pixels': [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    }

    k1Pic = correlate(pic, k1, True)
    k2Pic = correlate(pic, k2, True)

    rPixels = [math.sqrt(((k1Pic['pixels'][i])**2)+((k2Pic['pixels'][i])**2)) for i in range(len(k1Pic['pixels']))]
    for i in range(len(rPixels)):
        if (rPixels[i] > 255):
            rPixels[i] = 255
        elif(rPixels[i] < 0):
            rPixels[i] = 0

    returnPic = {
    'width': pic['width'],
    'height': pic['height'],
    'pixels': [round(i) for i in rPixels]
    }

    if(saveImages == True):
        image1 = {
        'width': pic['width'],
        'height': pic['height'],
        'pixels': [round(k1Pic['pixels'][i]) for i in range(len(k1Pic['pixels']))]
        }
        save_image(image1, "edgeDetectorFunc1.png")

        image2 = {
        'width': pic['width'],
        'height': pic['height'],
        'pixels': [round(k2Pic['pixels'][i]) for i in range(len(k2Pic['pixels']))]
        }
        save_image(image2, "edgeDetectorFunc2.png")

    return returnPic


# LAB 2 FILTERS
def color_filter_from_greyscale_filter(filt, secondArgument = False):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def func (image):
        rImage = {
            'width': image['width'],
            'height': image['height'],
            'pixels': [i[0] for i in image['pixels']]
        }
        bImage = {
            'width': image['width'],
            'height': image['height'],
            'pixels': [i[1] for i in image['pixels']]
        }
        gImage = {
            'width': image['width'],
            'height': image['height'],
            'pixels': [i[2] for i in image['pixels']]
        }
        if(secondArgument == False):
            r = filt(rImage)
            b = filt(bImage)
            g = filt(gImage)
        else:
            r = filt(rImage, secondArgument)
            b = filt(bImage, secondArgument)
            g = filt(gImage, secondArgument)

        colorImg = {
            'width': image['width'],
            'height': image['height'],
            'pixels': [(r['pixels'][i], b['pixels'][i], g['pixels'][i]) for i in range(len(rImage['pixels']))]
        }
        return colorImg
    return func

def make_blur_filter(n):
    number = n
    def blur_filter(image):
        return blurred(image, number)
    return blur_filter

def make_sharpen_filter(n):
    number = n
    def sharpen_filter(image):
        return sharpened(image, number)
    return sharpen_filter

def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    filterSet = filters.copy()
    def returnFilter(image):
        newImage = image.copy()
        for filt in filterSet:
            newImage = filt(newImage)
        return newImage
    return returnFilter


# SEAM CARVING

# Main Seam Carving Implementation

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image.
    """
    imageCopy = image.copy()
    greyScale = greyscale_image_from_color_image(image)
    for i in range(ncols):
        energy = compute_energy(greyScale)
        energyMap = cumulative_energy_map(energy)
        #print(energyMap)
        #save_image(energyMap, 'debugging.png')
        seam = minimum_energy_seam(energyMap)
        imageCopy = image_without_seam(imageCopy, seam)
        greyScale = image_without_seam(greyScale, seam)
        #save_color_image(imageCopy, 'twoCats.png')
        #print(seam)
    return imageCopy



# Optional Helper Functions for Seam Carving
def compareImages(pic1, pic2):
    if (len(pic1['pixels']) != len(pic2['pixels'])):
        return("Pictures are not the same pixel length")
    return [pic1['pixels'][i]-pic2['pixels'][i] for i in range(len(pic2['pixels']))]

def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    greyPixels = [round(.299*image['pixels'][i][0]+.587*image['pixels'][i][1]+.114*image['pixels'][i][2]) for i in range(len(image['pixels']))]
    returnPic = {
        'width': image['width'],
        'height': image['height'],
        'pixels': greyPixels
    }
    return returnPic


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    mutatedEnergy = energy.copy()
    energyPixels = energy['pixels']
    cumulative = [energy['pixels'][i] for i in range(energy['width'])]
    for i in range(len(cumulative)):
        mutatedEnergy['pixels'][i] = cumulative[i]
    for ph in range(1, energy['height']):
        for pw in range(energy['width']):
            cumulative.append(min_three_pixels(mutatedEnergy, (pw, ph)))
            mutatedEnergy['pixels'][pw+ph*energy['width']] = cumulative[-1]
    newImage = {
        'width': energy['width'],
        'height': energy['height'],
        'pixels': cumulative
    }
    return newImage

def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    minPixels = []
    minPixels.append(0)
    minValue = 255*cem['height']
    for i in range(len(cem['pixels'])-cem['width'], len(cem['pixels'])):
        if cem['pixels'][i] < minValue:
            minValue = cem['pixels'][i]
            minPixels[0] = i

    for i in range(cem['height']-1): #i is the row that we are checking
        minPixels.append(min_three_pixels(cem, minPixels[-1], returnPosition = True))
    return minPixels



def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    smallerImage = {
        'width': image['width']-1,
        'height': image['height'],
        'pixels': [image['pixels'][i] for i in range(len(image['pixels'])) if i not in seam]
    }
    return smallerImage


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}

def save_color_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}

def min_three_pixels(image, pos, returnPosition = False):
    """
    returns the minimum pixel value of the three pixels above the specified pixel
    pos is either a tuple of x, y or the position of the pixel in the list
    """
    if (type(pos) == type(2)):
        num = pos
    else:
        num = pos[0]+pos[1]*image['width']

    n = 3

    xTest = num%image['width']
    topPos = num - image['width']-1
    if(xTest <= 0):
        topPos += 1
        n -= 1
    if(xTest+1 >= image['width']):
        n -= 1
    values = []
    for i in range(n):
        values.append(image['pixels'][topPos+i])
    if(returnPosition == False):
        return min(values)+image['pixels'][num]
    else:
        #return topPos + values.index(min(values))
        for i in range(len(values)): #-1, -1, -1):
            if values[i] == min(values):
                #print(topPos)
                return topPos + i

def vignette(image, s = 0.8):
    centerX = image['width']//2
    centerY = image['height']//2

    newPixels = []
    for ph in range(image['height']):
        for pw in range(image['width']):
            distance = math.sqrt(((pw-centerX)/centerX)**2+((ph-centerY)/centerY)**2)/math.sqrt(2)
            newValue = image['pixels'][image['width']*ph+pw]*getVingetteValue(distance, s)
            newPixels.append(newValue)
    newImage = {
        'height': image['height'],
        'width': image['width'],
        'pixels': newPixels
    }
    return newImage


def getVingetteValue(distance, strength, angle = 10):
    """
    getVingette returns a value between 0 and 1 for creating a VingetteValue
    distance is a value typically between 0 and 1
        distances before 0 will likely output 1 and value after 1 will likely output 0
    Angle is a number that varies 10-60
    """
    value = 1 - (1/(1+math.e**(-angle*(distance+strength-1.1))))
    return value

def load_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}
def save_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()

def save_greyscale_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()



# Code Blocks for Completing Specific Tasks From Lab
def mutateCat():
    pic = load_color_image('test_images/cat.png')
    mutatedPic = color_filter_from_greyscale_filter(inverted)(pic)
    save_color_image(mutatedPic, 'mutatedCat.png')
    # print(compareImages(pic, mutatedPic))
    pass
def mutatePython():
    pic = load_color_image('test_images/python.png')
    blurring = make_blur_filter(9)
    mutatedPic = color_filter_from_greyscale_filter(blurring)(pic)
    save_color_image(mutatedPic, 'mutatedPython.png')
    # print(compareImages(pic, mutatedPic))
    pass
def mutateSparrowChick():
    pic = load_color_image('test_images/sparrowchick.png')
    sharpening = make_sharpen_filter(7)
    mutatedPic = color_filter_from_greyscale_filter(sharpening)(pic)
    save_color_image(mutatedPic, 'mutatedSparrowChick.png')
    # print(compareImages(pic, mutatedPic))
    pass
def mutateFrog():
    filter1 = color_filter_from_greyscale_filter(edges)
    filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))
    filt = filter_cascade([filter1, filter1, filter2, filter1])
    pic = load_color_image('test_images/frog.png')
    mutatedPic = filt(pic)
    save_color_image(mutatedPic, 'mutatedFrog.png')
    # print(compareImages(pic, mutatedPic))
    pass
def vingetteRun():
    pic = load_color_image('test_images/cat.png')
    mutatedPic = color_filter_from_greyscale_filter(vignette, 0.1)(pic)
    finalPic = color_filter_from_greyscale_filter(round_and_clip_image)(mutatedPic)
    #print(finalPic)
    save_color_image(finalPic, 'vingetteCat.png')

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    vingetteRun()
    pass
