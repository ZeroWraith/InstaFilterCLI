# 🖼️ OpenCV Image Filter CLI Tool ✨

## 💡 High-Level Summary

This is a simple, interactive command-line tool (CLI) built with Python, OpenCV, and NumPy. It allows a user to load any image, apply a variety of artistic and corrective filters (Grayscale, Blur, Sepia, Pencil Sketch), and instantly preview the "Before vs. After" result. The user can then choose to save the newly filtered image.

## 🎯 Problem Statement

In many situations, applying a simple filter to an image requires opening a heavy GUI application like Photoshop, GIMP, or a mobile app. This project's goal was to provide a lightweight, fast, and interactive command-line alternative for users who want to quickly process, preview, and save basic image manipulations without the overhead of a large software suite.

##⚙️ Features & Methodology

This tool uses core functionalities from OpenCV and NumPy to perform image manipulations. After loading an image, the user can select from the following filters, which are implemented using specific computer vision techniques.

### 1. 🎨 Grayscale

Method: Converts the 3-channel BGR (Blue, Green, Red) image to a single-channel grayscale image using cv.cvtColor(image, cv.COLOR_BGR2GRAY).

Note: The 1-channel image is then converted back to a 3-channel image (cv.COLOR_GRAY2BGR) to ensure it can be displayed and processed consistently with the other 3-channel filters.

### 2. 🌫️ Gaussian Blur

Method: Applies a strong 21x21 Gaussian blur kernel using cv.GaussianBlur(image, (21, 21), 0).

Purpose: This softens the image, reduces noise, and de-focuses details. The kernel size (21x21) was chosen to make the effect highly noticeable.

### 3. 🎞️ Sepia

Method: Applies a classic sepia tone by transforming the image's BGR values using a custom sepia kernel and cv.transform. This is a matrix multiplication on every pixel.

Kernel: The specific kernel used for BGR images is:

#### BGR values are transformed to create new BGR values
```
sepia_kernel = np.array([
    # [newBlue, newGreen, newRed] from [oldB, oldG, oldR]
    [0.131, 0.534, 0.272],  # -> newBlue
    [0.168, 0.686, 0.349],  # -> newGreen
    [0.189, 0.769, 0.393]   # -> newRed
])
```

The result is then clipped to the valid 0-255 range using np.clip.

### 4. ✏️ Pencil Sketch

Method: Simulates a hand-drawn pencil sketch using the "Dodge and Burn" technique. This is a multi-step algorithm:

- Grayscale: The image is first converted to grayscale.

- Invert: The grayscale image is inverted ( 255 - image ), creating a photo-negative.

- Blur: The inverted image is heavily blurred.

- Invert Again: The blurred image is inverted.

- Color Dodge: The original grayscale image (Step 1) is "dodged" by the inverted-blurred image (Step 4) using cv.divide(gray_image, inverted_blurred, scale=256.0). This divides the bottom layer by the inverted top layer, which brightens the image and leaves only the dark "lines" from the blurred negative, creating a sketch effect.


## Install Dependencies
Ensure you have Python 3 installed. Then, install the required libraries:

```pip install opencv-python numpy```


Run the Script

```python image_filter_tool.py```



## ✅ Results

The primary result is a functional CLI tool. Upon selecting a filter, the script opens two windows showing a real-time, side-by-side comparison.

Here is an example of what the user sees :

### 📸 Filter Comparison

| Original | Grayscale 🎨 | Sepia 🎞️ | Blur 🌫️ | Pencil Sketch ✏️ |
| :---: | :---: | :---: | :---: | :---: |
| ![Original Image]([emma.jpg]) | ![Grayscale Image]([grey.jpg]) | ![Sepia Image]([sepia.jpg]) | ![Blurred Image]([blur.jpg]) | ![Pencil Sketch Image]([pencil.jpg]) |



## 🧠 Challenges & Learnings

### 🧩 Challenge 1: Implementing Non-Native Filters

While Grayscale and Blur are simple, one-line OpenCV functions, the Sepia and Pencil Sketch filters are not. This required researching the underlying algorithms.

#### 💡 Learning: 

I learned how to implement a custom sepia filter by finding the correct transformation matrix and applying it with cv.transform. For the pencil sketch, I learned how to combine simple arithmetic operations (cv.divide, invert) to simulate the "Color Dodge" blend mode found in professional photo editors.

### 🔧 Challenge 2: Data Types and Image Channels

Applying matrix transformations (like for Sepia) can result in pixel values outside the valid 8-bit unsigned integer range (0-255).

#### 💡 Learning: 
This taught me the importance of np.clip(image, 0, 255) to clamp values back into the valid range, preventing visual artifacts. I also learned the importance of managing image channels, as the grayscale and sketch filters produce 1-channel images that must be converted back to 3-channels (cv.COLOR_GRAY2BGR) to be displayed and saved correctly.