import os
import asyncio
import cozmo
from PIL import ImageDraw, ImageOps
import PIL.Image
import PIL.ImageFont
import PIL.ImageTk
import cv2
import numpy as np
import tkinter

# Run Configuration
os.environ['COZMO_PROTOCOL_LOG_LEVEL'] = 'DEBUG'
os.environ['COZMO_LOG_LEVEL'] = 'DEBUG'
USE_LOGGING = False
WRITE_TO_FILE = True

# TO INSTALL OPENCV ON MAC:
# brew install opencv3 --HEAD --with-contrib --with-python3
# to ~/.bash_profile add:
#   PYTHONPATH="/usr/local/Cellar/opencv3/HEAD-dd379ec_4/lib/python3.5/site-packages/:$PYTHONPATH"
#   export PYTHONPATH

'''
Edge Test
-Experimenting with Cozmo's camera and OpenCV
-Displays TKinter window with both pre and post-processed live camera feed
-Current frame can also written to file
@author Team Cozplay
'''
class EdgeTest:
    def __init__(self):
        self._robot = None
        self._tk_root = 0
        self._tk_label_input = 0
        self._tk_label_output = 0
        if USE_LOGGING:
            cozmo.setup_basic_logging()
        cozmo.connect(self.run)

    def on_new_camera_image(self, event, *, image:cozmo.world.CameraImage, **kw):
        raw_image = image.raw_image
        #width, height = raw_image.size
        #print(width)
        #print(height)
        raw_image = raw_image.crop((5, 80, 320, 240))

        # Convert PIL Image to OpenCV Image
        # See: http://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
        cv2_image = cv2.cvtColor(np.array(raw_image), cv2.COLOR_RGB2BGR)

        # Apply edge filter
        cv2_edges = self.auto_canny(cv2_image)
        minLineLength = 20
        maxLineGap = 20
        maxNumLines = 30
        cv2_lines = cv2.HoughLinesP(cv2_edges, 10, np.pi / 180, 100, maxNumLines, minLineLength, maxLineGap)
        # cv2_lines = self.auto_lines(cv2_edges)
        # print(cv2_lines)

        # Save OpenCV image
        if WRITE_TO_FILE:
            cv2.imwrite('cv2_edge_input.png', cv2_image)
            cv2.imwrite('cv2_edge_output.png', cv2_edges)

        # Convert output image back to PIL image
        pil_edges = PIL.Image.fromarray(cv2.cvtColor(cv2_edges, cv2.COLOR_GRAY2RGB))

        # Display input and output feed
        draw = ImageDraw.Draw(image.raw_image)
        # for line in cv2_lines:
        #     for x1, y1, x2, y2 in cv2_lines[0]:  # display hough lines
        a, b, c = cv2_lines.shape
        for i in range(a):
            # rho = cv2_lines[i][0][0]
            # theta = cv2_lines[i][0][1]
            # a = np.cos(theta)
            # b = np.sin(theta)
            # x0 = a * rho
            # y0 = b * rho
            # x1 = int(x0 + 1000 * (-b))
            # y1 = int(y0 + 1000 * (a))
            # x2 = int(x0 - 1000 * (-b))
            # y2 = int(y0 - 1000 * (a))
            x1 = cv2_lines[i][0][0]+5
            y1 = cv2_lines[i][0][1]+80
            x2 = cv2_lines[i][0][2]+5
            y2 = cv2_lines[i][0][3]+80
            if (x1-x2)<10 and (x1-x2)>-10: #vertical
                draw.line([(x1, y1), (x2, y2)], fill=(0, 128, 0), width=2) #green
            elif (y1-y2)<10 and (y1-y2)>-10: #horizontal
                draw.line([(x1, y1), (x2, y2)], fill=(128,0, 128), width=2) #purple
            elif ((y1-y2)/(x1-x2)) > 0: # and ((y1-y2)/(x1-x2)) <-75:
                draw.line([(x1, y1), (x2, y2)], fill=(135, 206, 250), width=2) #light blue
            else:
                draw.line([(x1, y1), (x2, y2)], fill=(255, 0, 0), width=2) #red
        display_image_input = PIL.ImageTk.PhotoImage(image=image.raw_image)
        display_image_output = PIL.ImageTk.PhotoImage(image=pil_edges)
        self._tk_label_input.imgtk = display_image_input
        self._tk_label_input.configure(image=display_image_input)
        self._tk_label_output.imgtk = display_image_output
        self._tk_label_output.configure(image=display_image_output)
        self._tk_root.update()

    # Auto-paramter Canny edge detection adapted from:
    # http://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    def auto_canny(self, img, sigma=0.33):  #was .33
        blurred = cv2.GaussianBlur(img, (3, 3), 0)
        v = np.median(blurred)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(blurred, lower, upper)
        return edged

    #hough line detection
    def auto_lines(self, img):
        minLineLength = 50
        maxLineGap = 5
        maxNumLines = 30
        lines = cv2.HoughLinesP(img, 10, np.pi / 180, 100, maxNumLines, minLineLength, maxLineGap)
        return lines

    async def set_up_cozmo(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self._robot = await coz_conn.wait_for_robot()
        self._robot.camera.image_stream_enabled = True
        self._robot.add_event_handler(cozmo.world.EvtNewCameraImage, self.on_new_camera_image)
        self._robot.set_head_angle(cozmo.util.Angle(degrees=0))
       # self._robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    async def run(self, coz_conn):
        # Set up Cozmo
        await self.set_up_cozmo(coz_conn)

        self._tk_root = tkinter.Tk()
        # TODO: ESC to exit
        self._tk_label_input = tkinter.Label(self._tk_root)
        self._tk_label_output = tkinter.Label(self._tk_root)
        self._tk_label_input.pack()
        self._tk_label_output.pack()

        while True:
            await asyncio.sleep(0)


if __name__ == '__main__':
    EdgeTest()