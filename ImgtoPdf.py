import tkinter as tk
from tkinter import filedialog # to open files in computer
from reportlab.pdfgen import canvas # helps with working with images 
from PIL import Image
import os

class ImageToPdf:
    def __init__(self, root):
        self.root = root
        self.image_paths = []  # List to store selected image paths
        self.output_pdf_name = tk.StringVar()  # Variable to store the output PDF name
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)  # Listbox to display selected images &
                                                                                 # we will be selecting multiple images
        
        self.initialize_ui()  # Call method to initialize the UI

    def initialize_ui(self):
        # Create and pack the title label
        title_label = tk.Label(self.root, text="Image To PDF Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)  # Add padding around the label               # font,size,bold or not

        # Create and pack the button to select images
        select_image_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_image_button.pack(pady=(0, 10))  # Add padding below the button

        # Pack the Listbox to display selected images
        self.selected_images_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        # Create and pack the label for PDF name entry
        label = tk.Label(self.root, text="Enter Output PDF Name")
        label.pack()
         #The pack() method will place the entry widget within the window, ensuring it is displayed to the user.
        #The widget will be centered horizontally within the space allocated to it, thanks to the justify="center" option
        #within the Entry widget itself (though justify primarily affects text alignment within the entry).

        # Create and pack the entry widget to input PDF name
        pdf_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify="center")
        pdf_entry.pack()

        # Create and pack the button to convert images to PDF
        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf)
        convert_button.pack(pady=(20, 40))  # Add padding above and below the button

    def select_images(self):
        # Open file dialog to select images
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        print("Selected images:", self.image_paths)  # Debug statement                # "*" matlab file ka kuch bhi naam ho skta hai
        self.update_selected_images_listbox()  # Update the Listbox with selected images

    def update_selected_images_listbox(self):
        # Clear the Listbox
        self.selected_images_listbox.delete(0, tk.END)
        # Insert each selected image's name into the Listbox
        for image_path in self.image_paths:
            _, image_name = os.path.split(image_path)  # Get the image name from the path
            self.selected_images_listbox.insert(tk.END, image_name)  # Insert the image name into the Listbox

    def convert_images_to_pdf(self):
        # Check if any images are selected
        if not self.image_paths:
            print("No images selected.")  # Debug statement
            return

        # Get the output PDF path, default to "output.pdf" if no name is provided
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"
        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))  # Create a new PDF with specified page size

        for image_path in self.image_paths:
            img = Image.open(image_path)  # Open the image using PIL
            available_height = 720
            available_width = 540
            # Calculate the scale factor to fit the image within the available dimensions
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            # Calculate the center position for the image
            x_center = (612 - new_width) / 2
            y_center = (792 - new_height) / 2
            pdf.setFillColorRGB(1, 1, 1)  # Set the fill color to white
            pdf.rect(0, 0, 612, 792, fill=True)  # Draw a white rectangle as the background
            pdf.drawInlineImage(img, x_center, y_center, width=new_width, height=new_height)  # Draw the image
            pdf.showPage()  # Create a new page in the PDF

        pdf.save()  # Save the PDF
        print(f"PDF saved as: {output_pdf_path}")  # Debug statement

if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = ImageToPdf(root)  # Create an instance of the ImageToPdf class
    root.mainloop()  # Start the Tkinter event loop
