# Training Image Processor

This project speeds up the process of manually preparing images for training Stable Diffusion embeddings.

It provides a UI for selecting a square portion of a picture and then scales that section to 512x512 for training, and then provides a steamlined UI for renaming all your images with a preview so you can see them.

## Installation and Launching
### Windows

* Install python 3.x from python.org.
* Download this repository as a zip file and extract
* Enter the extracted folder with your file browser
* Double click setup (setup.bat) - This only needs done once
* Double click launch (launch.bat)

### Linux - and other Unix-likes/BSDs/MacOS
Ya'll probably know what to do already...
* Git clone the repo or download the zip and extract
* Enter the project folder in a bash terminal
* run `make`
* activate the venv with `source ./venv/bin/activate` or alternative script if not using bash...
* run the script `python src/training_image_processor`

## Usage
* First open a directory with pictures
* Use the buttons at the top to rotate/flip immages as needed
* Resize selection square with mouse wheel
* Click the image to process it and load the next image. The 512x512 image is placed in a new 'outputs' folder and the original goes in a new 'originals' folder, inside the open directory

### Licensing
The contents under the assets folder are from the adwaita-icons project and are released under the license LGPL-v3.0. The rest of the project is GPL-v2 only.
