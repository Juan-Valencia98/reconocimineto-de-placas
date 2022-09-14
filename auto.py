import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
import LPR

def plot_image(img, grayscale=True):
    plt.axis('off')
    if grayscale:
        plt.imshow(img, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()
    
idx = 5
lpr = LPR.LPR()

# Muestra imagen normal 
img = cv2.imread(f"./upeaimagen/imagen13.png")
plot_image(img, False)

# Muestra imagen Blanco y Negro
gray = lpr.grayscale(img)
plot_image(gray)


# Muestra imagen Resaltando mas el negro
thresh = lpr.apply_threshold(gray)
plot_image(thresh)


contours = lpr.find_contours(thresh)
canvas = np.zeros_like(img)
cv2.drawContours(canvas , contours, -1, (0, 255, 0), 2)
plt.axis('off')
plot_image(canvas)
plt.imshow(canvas);

candidates = lpr.filter_candidates(contours)
canvas = np.zeros_like(img)
cv2.drawContours(canvas , candidates, -1, (0, 255, 0), 2)
plt.axis('off')
plot_image(canvas)
plt.imshow(canvas);




license = lpr.get_lowest_candidate(candidates)
canvas = np.zeros_like(img)
cv2.drawContours(canvas , [license], -1, (0, 255, 0), 2)
plt.axis('off')
plot_image(canvas)
plt.imshow(canvas);

# Muestra posible placa
cropped = lpr.crop_license_plate(gray, license)
cropped2 = lpr.crop_license_plate(img, license)
plot_image(cropped2, False)

# Lo combierte en Blanco y Negro
thresh_cropped = lpr.apply_adaptive_threshold(cropped)
plot_image(thresh_cropped)

# Saca el texto blanco y negro
clear_border = lpr.clear_border(thresh_cropped)
final = lpr.invert_image(clear_border)
plot_image(final)

psm = 7
alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
options = "-c tessedit_char_whitelist={}".format(alphanumeric)
options += " --psm {}".format(psm)
txt = pytesseract.image_to_string(final, config=options)
print(txt[:4], txt[4:])