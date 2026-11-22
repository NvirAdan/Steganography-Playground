# Steganography Playground

Hide a text message inside an ordinary image, recover it later, and *see* exactly where it was hidden.

The modified image looks identical to the original. The difference lives in the least significant bit of each color value, which the human eye cannot detect.

Built in under 48 hours as part of a weekend-MVP series.

<!--
**Watch the video:** 
-->

## What it does

| Function | What it does |
|---|---|
| `hide(input_path, output_path, message)` | Hides a text message inside an image and saves the result as a PNG. |
| `recover(image_path)` | Reads the hidden message back out of an image. |
| `diff_image(original_path, modified_path, output_path, factor=255)` | Subtracts two images and amplifies the difference so you can see which pixels changed. |

## How it works

An image is a grid of pixels, and every pixel is three numbers (red, green, blue) between 0 and 255. Each number is stored as 8 bits:

```
150 = 1 0 0 1 0 1 1 0
                    ^ least significant bit (LSB)
```

The leftmost bits change the color a lot. The rightmost bit changes it almost nothing: 150 and 151 are indistinguishable to the eye. This project replaces that last bit with one bit of your message:

```
Original value:    150  200  33   90
Last bit:           0    0    1    0
Bit to hide:        0    1    0    1
New value:         150  201  32   91
```

To recover the message, it reads the last bit of each value in the same order and groups them back into bytes.

**Message format.** The first 32 bits store the message length, followed by the message itself in UTF-8. The length is how the decoder knows where the message ends.

**Capacity.** Roughly `width × height × 3 / 8 − 4` bytes. A 540×720 image can hold about 145 KB of text, which is far more than a link or a short note needs.

## Installation

1. **Install Python 3.9 or newer** from [python.org](https://www.python.org/downloads/). On Windows, tick **"Add Python to PATH"** during setup.
2. **Download this project.** Click the green **Code** button at the top of this page, choose **Download ZIP**, and extract it. (If you use Git: `git clone https://github.com/NvirAdan/Steganography-Playground.git`)
3. **Open a terminal inside the project folder**, the one that contains `steganography.py`.
4. **Create and activate a virtual environment.** It is optional but recommended, because it keeps this project's packages separate from the rest of your system.

   ```bash
   python -m venv venv
   ```

   Then activate it:

   ```bash
   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

   You'll see `(venv)` at the start of the terminal line when it's active. If PowerShell says that running scripts is disabled, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first. It only affects that terminal window.

5. **Install the dependency:**

   ```bash
   pip install pillow
   ```

## Usage

`steganography.py` is a file of functions, not a program with a window. The line `from steganography import ...` means "load these functions from the file `steganography.py` in this same folder", so run your commands from inside the project folder and keep your images there too.

### Recover a hidden message

Put the image in the project folder and run this one-liner, replacing `secret.png` with your file's name:

```bash
python -c "from steganography import recover; print(recover('secret.png'))"
```

The hidden text is printed in the terminal.

### Hide your own message and see the difference

Create a file called `example.py` in the project folder:

```python
from steganography import hide, recover, diff_image

# Hide a message (the output is always saved as PNG)
hide("photo.jpg", "secret.png", "This text is hidden inside the image")

# Recover it
print(recover("secret.png"))

# See where the message lives (changed pixels light up)
diff_image("photo.jpg", "secret.png", "diff.png")
```

Put a `photo.jpg` (or any image) next to it and run:

```bash
python example.py
```

You'll get `secret.png`, which looks identical to the original, and `diff.png`, which shows where the message is hidden.

Tip: with a short message, only the first few rows of pixels change, so the diff image looks almost empty. Hide a long text to see the noise spread across the picture.

## Important limitations

- **Keep the image lossless.** The output must stay a PNG. JPEG compression rewrites pixel values and destroys the hidden bits.
- **Don't send it through apps that recompress images.** WhatsApp, Instagram, X/Twitter and similar platforms often recompress images and will break the message. Share the file as a file, or inside a `.zip`.
- **Don't resize, crop or edit the image** after hiding the message.
- **This hides a message, it does not protect it.** Anyone who suspects an image carries data and uses a tool like this one can extract it. For anything sensitive, encrypt the text first, or use an end-to-end encrypted messenger instead.
- Transparency is dropped: images are converted to RGB.

<!-- 
## Download (no Python needed)

Download the latest `.zip` from DRIVE_LINK_HERE, extract it, and run the app.
-->