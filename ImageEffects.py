from tkinter import filedialog
import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import os

import numpy as np

# global variables
MARGIN = 10  # px
MAXDIM = 530


class App():
    def __init__(self, window, window_title):
        self.image_path="Obama (Img 3).jpg"
        self.window = window
        self.window.title(window_title)
        
        # Load image using OpenCV
        self.cv_img = cv2.cvtColor(cv2.imread(self.image_path), cv2.COLOR_BGR2RGB)
        self.NEWcv_img = self.cv_img.copy()  # for recursive processing
        self.height, self.width, num_channel = self.cv_img.shape
        
        # Create a Frame that can fit the images
        self.frame1 = tk.Frame(self.window , width=100, height=100, bg='#f7fffc')  # size not important
        self.frame1.pack(fill=tk.BOTH)
        
        self.frame2 = tk.Frame(self.window , width=100, height=100, bg='#f7fffc')  # size not important
        self.frame2.pack(fill=tk.BOTH)
        
        # Create two Canvases for image display
        self.canvas0 = tk.Canvas(self.frame1, width=MAXDIM, height=MAXDIM, bg='#f7fffc', highlightthickness=0)  # original
        self.canvas0.pack(side=tk.LEFT)
        self.canvas1 = tk.Canvas(self.frame1, width=MAXDIM, height=MAXDIM, bg='#f7fffc', highlightthickness=0)  # original
        self.canvas1.pack()
        
        self.canvas3 = tk.Canvas(self.frame2, width=MAXDIM, height=4*MARGIN, bg='#f7fffc', highlightthickness=0)  # original
        self.canvas3.pack(side=tk.LEFT)
        self.canvas4 = tk.Canvas(self.frame2, width=MAXDIM, height=4*MARGIN, bg='#f7fffc', highlightthickness=0)  # original
        self.canvas4.pack()
        
        # PhotoImage
        self.photoOG = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))  # original
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))  # modified
        
        # Add PhotoImage to Canvas
        self.canvas0.create_image(MAXDIM//2, MAXDIM//2, image=self.photoOG)
        self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo)
        
        # Write caption for both images
        self.canvas3.create_text(MAXDIM//2, (2*MARGIN), text="Original Photo", font="Tahoma 20")
        self.canvas4.create_text(MAXDIM//2, (2*MARGIN), text="Modified Photo", font="Tahoma 20")
        
# ##############################################################################################
# ################################   PARAMETER TOOLBAR   #######################################
# ##############################################################################################

        # Create a Frame that can fit the images
        self.frame3 = tk.Frame(self.window , width=100, height=100, bg='#9dc2b2')
        self.frame3.pack(side=tk.BOTTOM, fill=tk.BOTH)
        
        # Create a Button for loading an image
        self.button_exit = tk.Button(self.frame3, text="Load Image", command=self.load_image, height= 2, width = 14, font="Tahoma 10")
        self.button_exit.pack(side=tk.LEFT, padx = 20)
                
        # Create a Button for exiting the program
        self.button_exit = tk.Button(self.frame3, text="Exit", command=lambda: exit(), height= 2, width = 14, font="Tahoma 10")
        self.button_exit.pack(side=tk.RIGHT, padx = 20)
        
        # Create a Button for negating the image
        self.button_reset = tk.Button(self.frame3, text="Reset", command=self.reset, height= 2, width = 14, font="Tahoma 10")
        self.button_reset.pack(side=tk.LEFT, padx = (10, 100))

        # Create a Scale that lets users blur the image
        self.scale_blur = tk.Scale(self.frame3, label="Blur", orient=tk.HORIZONTAL, command=self.blur)
        self.scale_blur.pack(side=tk.LEFT, padx = 25)
        
        # Create a Scale that lets users cartoonify the image
        self.scale_cartoon = tk.Scale(self.frame3, label="Cartoon Effect", orient=tk.HORIZONTAL, command=self.cartoon)
        self.scale_cartoon.pack(side=tk.LEFT, padx = 25)
                
        # Create a Scale that lets the users make a pencil sketch
        self.scale_pencil = tk.Scale(self.frame3, label="Pencil Effect", orient=tk.HORIZONTAL, command=self.pencil)
        self.scale_pencil.pack(side=tk.LEFT, padx = 25)
        
        self.window.mainloop()
        
##############################################################################################
#################################  CALLBACK FUNCTIONS  #######################################
##############################################################################################
    def load_image(self):
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes = (("JGP file", "*.jpg"), ("PNG file", "*.png"), ("All Files", "*.")))
        self.image_path = fln
        self.cv_img = cv2.cvtColor(cv2.imread(self.image_path), cv2.COLOR_BGR2RGB)
        self.NEWcv_img = self.cv_img.copy()
        
        self.photoOG = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))  # original
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))  # modified
        
        self.canvas0.create_image(MAXDIM//2, MAXDIM//2, image=self.photoOG)
        self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo)
        
    # Callback for negative button
    def reset(self):
#         self.NEWcv_img = 255 - self.NEWcv_img
        self.scale_blur.set(0)
        self.scale_cartoon.set(0)
        self.scale_pencil.set(0)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.NEWcv_img))
        self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo)
    
    # Callback for blur scale
    def blur(self, k):
        self.NEWcv_img = self.cv_img.copy()
        scale = int(int(k)/2.5)
        size = 0
        for i in range (scale):
            size = i
            if size % 2 == 0: #ensure that size is odd.
                size += 1
            self.NEWcv_img = cv2.GaussianBlur(self.NEWcv_img,(size,size),cv2.BORDER_DEFAULT)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.NEWcv_img))
        self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo)
    
    # Callback for cartoon scale
    def cartoon(self, k):
        self.NEWcv_img = self.cv_img.copy()
        if int(k) == 0:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))
            self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo)
        else:
            img_color = self.NEWcv_img
            
            num1 = int(int(k)/12)           # number for median filter kernal size
            num2 = int(int(k)/9)            # block size for adaptive threshold
      

            while num1 % 2 == 0 or num1 == 1:  # make sure numbers are greater than 1 AND odd.
                num1+=1

            while num2 % 2 == 0 or num2 == 1:
                num2+=1


            # convert to grayscale and apply median blur
            NEWcv_image_gray = cv2.cvtColor(self.NEWcv_img, cv2.COLOR_RGB2GRAY)
            NEWcv_image_blur = cv2.medianBlur(NEWcv_image_gray, num1)

            # detect and enhance edges
            NEWcv_image_edge = cv2.adaptiveThreshold(NEWcv_image_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=num2, C=2)

            # convert back to color, bit-AND with color image
            NEWcv_image_edge = cv2.cvtColor(NEWcv_image_edge, cv2.COLOR_GRAY2RGB)
            self.NEWcv_img = cv2.bitwise_and(self.NEWcv_img, NEWcv_image_edge)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.NEWcv_img))
            self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo)
    
    # Callback for Pencil Sketch
    def pencil(self, k):
                   
        self.NEWcv_img = self.cv_img.copy()
        if int(k) == 0:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))
            self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo)
        else:
            
            num1 = int(int(k)/3)   # number for Gaussian kernal size
            num2 = int(int(k)/0.4) # number for blending scale

            while num1 % 2 == 0 or num1 < 7:
                num1+=1

            while num2 % 2 == 0 or num2 < 240:
                num2+=1
            NEWcv_image_gray = cv2.cvtColor(self.NEWcv_img, cv2.COLOR_RGB2GRAY)
            NEWcv_image_blur = cv2.GaussianBlur(NEWcv_image_gray, (num1, num1), 0, 0)
            NEWcv_image_blend = cv2.divide(NEWcv_image_gray, NEWcv_image_blur, scale=num2)

            # if available, blend with background canvas
            background = cv2.imread("canvas.jpg")
            background = background[0:NEWcv_image_blend.shape[0], 0:NEWcv_image_blend.shape[1]]
            background = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
            NEWcv_image_blend = cv2.multiply(NEWcv_image_blend, background, scale=1. / 256)

            pencil = cv2.cvtColor(NEWcv_image_blend, cv2.COLOR_GRAY2RGB)

            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(NEWcv_image_blend))
            self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo)
        
# Create a window and pass it to the Application object
App(tk.Tk(), "EE 440 Final Project - Youssef Lahrichi")
