import io
import base64
import requests
from PIL import Image, ImageTk
import tkinter as tk


def generate_image():
    info_label.config(text="Generating...")
    window.update()

    # Construct the payload with the parameters you want.
    payload = {
        "prompt": "p1xindianajones",
	"sampling_method": "DPM++ 2M Karras",
    	"model": "p1x-indianajonesdos/p1x-indianajonesdos_3500.safetensors", 
       	"steps": 20,
	"cfg_scale": 7,
	"width": 800,
	"height": 386
    }

    # Send the payload to the API
    response = requests.post(url='http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload)

    # Parse the response
    r = response.json()

    # Retrieve and decode the generated image
    for i in r['images']:
        image_data = i
        if "," in i:  # if the image data includes the data type, split it off
            image_data = i.split(",",1)[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

    # Convert the image to a format tkinter can use
    photo = ImageTk.PhotoImage(image)

    # Update the image_label with the new image
    image_label.config(image=photo)
    image_label.image = photo
    info_label.pack_forget()

url = 'http://127.0.0.1:7860'
option_payload = {
    "sd_model_checkpoint": "p1x-indianajonesdos/p1x-indianajonesdos_3500.safetensors"
}
response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)

window = tk.Tk()
window.title("P1X DOS Dreamer")
window.geometry('800x440')
window.configure(bg='black')


info_label = tk.Label(window, text="Generate a DOS game background",fg='white', bg='black')
info_label.pack(expand=True)

image_label = tk.Label(window,bg='black')
image_label.pack()

button = tk.Button(window, text="Dream...", command=generate_image,fg='white', bg='blue')
button.pack(pady=10)

window.mainloop()
