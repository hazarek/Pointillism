import cv2
import math
import progressbar
from pointillism import *
import sys

img = cv2.imread("test/lake.jpg")
# img = limit_size(img, 900)
gradient_smoothing_radius = int(round(max(img.shape) / 50))
# stroke_scale = int(math.ceil(max(img.shape) / 1000))
palette_size = 20 #default 20

stroke_scale = 12
# convert the image to grayscale to compute the gradient
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print("Computing color palette...")
palette = ColorPalette.from_image(img, palette_size)
print("Extending color palette...")
palette = palette.extend([(0, 50, 0), (15, 30, 0), (-15, 30, 0)])
# display the color palette
# cv2.imshow("palette", palette.to_image())
# cv2.waitKey(200)
print("Computing gradient...")
gradient = VectorField.from_gradient(gray)
print("Smoothing gradient...")
gradient.smooth(gradient_smoothing_radius)
print("Drawing image...")
# create a "cartonized" version of the image to use as a base for the painting
# res = cv2.medianBlur(img, 33)

res = np.zeros(img.shape, dtype=np.uint8)
# res2 = cv2.cvtColor(gradient.get_magnitude_image(), cv2.COLOR_GRAY2BGR)

# define a randomized grid of locations for the brush strokes
grid = normal_grid(img.shape[0], img.shape[1], scale=16)
# print(img.shape[0] * img.shape[1], len(grid))
batch_size = 10000
bar = progressbar.ProgressBar()
for h in bar(range(0, len(grid), batch_size)):
    cv2.imshow("res", res)
    # get the pixel colors at each point of the grid
    pixels = np.array([img[x[0], x[1]] for x in grid[h:min(h + batch_size, len(grid))]])
    # precompute the probabilities for each color in the palette
    # lower values of k means more randomnes
    color_probabilities = compute_color_probabilities(pixels, palette, k=9)
    for i, (y, x) in enumerate(grid[h:min(h + batch_size, len(grid))]):
        color = color_select(color_probabilities[i], palette)
        # color = (255, 0, 255)
        # angle = math.degrees(gradient.direction(y, x)) + 90
        # angle = math.degrees(gradient.direction(y, x))
        # ellipse width and height
        length = int(round(stroke_scale + stroke_scale * math.sqrt(gradient.magnitude(y, x))))
        # length = int(gradient.magnitude(y, x))
        # draw the brush stroke
        angle = gradient.direction(y, x)
        cv2.line(res, 
            pt1=(x, y),
            pt2=(int(x + math.cos(angle) * length), int(y - math.sin(angle) * length)),
          color=color,
          thickness=int(math.sqrt(length)),
          lineType=cv2.LINE_AA)
        
        # cv2.ellipse(res2,
        #     center=(x, y), #brush coordinate
        #       axes=(length, stroke_scale), #width and height / (length, stroke_scale)
        #      angle=angle,
        # startAngle=0,
        #   endAngle=360,
        #      color=color,
        #  thickness=-1, # border thickness. -1 px will fill the shape by the specified color.
        #   lineType=cv2.LINE_AA)
    key = cv2.waitKey(1000)
    if key == ord('q'):
        break
    

# cv2.imshow("res", limit_size(res, 1080))
# cv2.imwrite("test/output.png", res)
cv2.imshow("res", res)
cv2.waitKey(0)
cv2.destroyAllWindows()
