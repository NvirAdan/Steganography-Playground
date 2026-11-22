from PIL import Image

# converts the bytes into a list of integers..
def bytes_to_bits(data: bytes) -> list[int]:
    return [(byte >> i) & 1 for byte in data for i in range(7, -1, -1)]


# collect the bits 8 by 8 and create new bytes.
def bits_to_bytes(bits: list[int]) -> bytes:

    out = bytearray()#selfexplanatory


    for i in range(0,len(bits), 8):
        
        byte = 0

        for bit in bits[i:i + 8]:
            byte = (byte << 1) | bit
        
        out.append(byte)

    
    return bytes(out)



#Now we gonna hide them inside the last bits of the pixel of each channel
def hide(inputs_path: str, output_path: str, message: str) -> None:

    # we convert the image into the 3 different channels
    img = Image.open(inputs_path).convert("RGB")

    flat = bytearray(img.tobytes())

    # encode the message
    data = message.encode("utf-8")

    # 32 bits long + message
    pay_load = len(data).to_bytes(4, "big") + data 

    bits = bytes_to_bits(pay_load)

    # Just in case
    if len(bits) > len(flat):
        raise ValueError(f"[Error] Message is too long..")


    for i, bit in enumerate(bits):
        flat[i] = (flat[i] & 0b11111110) | bit # deletes the last bit and insert the message


    Image.frombytes("RGB", img.size, bytes(flat)).save(output_path, "PNG")




# With this we take the image and recover the message inside it
def recover(image_path: str) -> str:

    # opening the image again with the separated channels like before in "hide" function
    flat = Image.open(image_path).convert("RGB").tobytes()

    length = int.from_bytes(bits_to_bytes([flat[i] & 1 for i in range(32)]), "big")

    # just in case to check that we didn't fuck up the length of the image between the manipulation
    if length * 8 + 32 > len(flat):
        raise ValueError(f"[Error] This image doesn't appear to have a hidden message..")

    # just extract the bits of the message
    bits = [flat[i] & 1 for i in range(32, 32 + length * 8)]

    # return the message decoded
    return bits_to_bytes(bits).decode("utf-8", errors="replace")


# it substract both of the images and amplify the difference so it can be seen.
def diff_image(original_path: str, modified_path: str, output_path: str, factor: int = 255) -> None:

    # Opening the images in the channels formats, as always
    a = Image.open(original_path).convert("RGB")

    b = Image.open(modified_path).convert("RGB")

    # Checking the sizes 
    if a.size != b.size:
        raise ValueError(f"[Error] Sizes doesn't match")


    diff = bytes(min(255, abs(x - y) * factor) for x, y in zip(a.tobytes(), b.tobytes()))

    Image.frombytes("RGB", a.size, diff).save(output_path, "PNG")


if __name__ == "__main__":

    # Hiding and naming the new image with our message ("Hello World") inside it.
    hide("monalisa.png", "showcase.png", "")

    # ---- HERE below write the "print(recover())" from the video ---#

    print(recover("hiddenmessage.png"))

    #----------------------------------------------------------------#













