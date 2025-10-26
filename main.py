import cv2 as cv
import numpy as np
import os

def apply_grayscale(image):
    """
    Applies a grayscale filter and converts it back to 3 channels.
    """
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Convert back to 3 channels so it can be displayed
    # and processed by other filters if needed
    gray_3_channel = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
    return gray_3_channel

def apply_blur(image):
    """
    Applies a strong Gaussian blur.
    """
    # Using a 21x21 kernel for a noticeable blur
    blurred = cv.GaussianBlur(image, (21, 21), 0)
    return blurred

def apply_sepia(image):
    """
    Applies a sepia filter using a kernel transformation.
    """
    # Define the sepia filter kernel (for BGR order)
    sepia_kernel = np.array([
        [0.131, 0.534, 0.272],  # -> newBlue
        [0.168, 0.686, 0.349],  # -> newGreen
        [0.189, 0.769, 0.393]   # -> newRed
    ])
    
    # Apply the transformation
    sepia_image = cv.transform(image, sepia_kernel)
    
    # Clip values to the 0-255 range
    sepia_image = np.clip(sepia_image, 0, 255)
    
    # Convert back to 8-bit unsigned integers
    sepia_image = np.uint8(sepia_image)
    return sepia_image

def apply_pencil_sketch(image):
    """
    Applies a pencil sketch effect using the "Dodge and Burn" technique.
    """
    # Step 1: Convert to grayscale
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # Step 2: Invert the grayscale image
    inverted_gray = 255 - gray_image
    
    # Step 3: Apply a blur to the inverted image
    blurred = cv.GaussianBlur(inverted_gray, (21, 21), 0)
    
    # Step 4: Invert the blurred image
    inverted_blurred = 255 - blurred
    
    # Step 5: Divide the grayscale image by the inverted-blurred image
    # This is the "Color Dodge" step
    pencil_sketch = cv.divide(gray_image, inverted_blurred, scale=256.0)
    
    # Convert the 1-channel sketch back to 3-channels
    pencil_sketch_3_channel = cv.cvtColor(pencil_sketch, cv.COLOR_GRAY2BGR)
    return pencil_sketch_3_channel

def print_menu():
    """Prints the main menu options."""
    print("\n--- Image Filter Menu ---")
    print("1. Apply Grayscale Filter")
    print("2. Apply Blur Filter")
    print("3. Apply Sepia Filter")
    print("4. Apply Pencil Sketch Filter")
    print("q. Quit")
    print("-------------------------")

def main():
    """Main function to run the image filter tool."""
    
    # --- 1. Load Image ---
    original_image = None
    image_path = ""
    file_extension = ""

    while True:
        image_path = input("Please enter the full path to your image: ")
        original_image = cv.imread(image_path)
        
        if original_image is not None:
            # Get the file extension
            _, file_extension = os.path.splitext(image_path)
            print(f"Image '{os.path.basename(image_path)}' loaded successfully.")
            break
        else:
            print(f"Error: Could not load image from '{image_path}'. Please check the path and try again.")

    # --- 2. Main Filter Loop ---
    while True:
        print_menu()
        choice = input("Enter your choice (1, 2, 3, 4, or q): ").strip().lower()
        
        result_image = None
        
        if choice == '1':
            print("Applying Grayscale filter...")
            result_image = apply_grayscale(original_image.copy())
            
        elif choice == '2':
            print("Applying Blur filter...")
            result_image = apply_blur(original_image.copy())
            
        elif choice == '3':
            print("Applying Sepia filter...")
            result_image = apply_sepia(original_image.copy())
            
        elif choice == '4':
            print("Applying Pencil Sketch filter...")
            result_image = apply_pencil_sketch(original_image.copy())
            
        elif choice == 'q':
            print("Exiting the program. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please select from the menu options.")
            continue # Skip the rest of the loop and show the menu again

        # --- 3. Display and Save Logic ---
        if result_image is not None:
            # Display the result
            print("Displaying original vs. filtered image.")
            print("Press any key in an image window to close and continue...")
            cv.imshow('Original Image', original_image)
            cv.imshow('Filtered Result', result_image)
            cv.waitKey(0)
            cv.destroyAllWindows()
            
            # Ask to save
            while True:
                save_choice = input("Do you want to save this new image? (y/n): ").strip().lower()
                
                if save_choice == 'y':
                    new_name = input(f"Enter the new file name (it will be saved as {file_extension}): ")
                    final_name = f"{new_name}{file_extension}"
                    
                    try:
                        cv.imwrite(final_name, result_image)
                        print(f"Image successfully saved as '{final_name}'")
                        break
                    except Exception as e:
                        print(f"Error saving image: {e}")
                        break
                        
                elif save_choice == 'n':
                    print("Image not saved.")
                    break
                    
                else:
                    print("Invalid choice. Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()
