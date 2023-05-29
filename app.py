import io
import base64
import requests
from PIL import Image, ImageTk
import tkinter as tk
url = 'http://127.0.0.1:7860'
payloads = {
    "Indiana Jones® and the Fate of Atlantis": {
        "prompt": "screenshot from DOS game p1xindianajones",
        "sampling_method": "DPM++ 2M Karras",
        "model": "p1x-indianajonesdos/p1x-indianajonesdos_6800.safetensors",
        "sampling_method": "Euler a",
        "steps": 14,
        "cfg_scale": 7,
        "width": 1024,
        "height": 512
    },
    "Riven The Sequel to MYST": {
        "prompt": "p1xriven",
        "sampling_method": "other_method",
        "model": "p1x-rivendos/p1x-rivendos_3100.safetensors",
        "sampling_method": "Euler a",
        "steps": 28,
        "cfg_scale": 8,
        "width": 1024,
        "height": 512
    },
    # Add more payloads here
}


def load_model(model_name):
    # Disable the button and dropdown
    generate_button.config(state="disabled", text="...")
    payload_dropdown.config(state="disabled")

    option_payload = {
        "sd_model_checkpoint": payloads[model_name]["model"]
    }

    response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)
    payload_var = tk.StringVar(value=model_name)

        # Re-enable the button and dropdown
    generate_button.config(state="normal", text="    DREAM    ")
    payload_dropdown.config(state="normal")

def generate_image():
    global counter
    counter += 1
    counter_label.config(text=f"Dreams: {counter}")


    # Disable the button and dropdown
    generate_button.config(state="disabled", text="...")
    payload_dropdown.config(state="disabled")

    info_label.config(text="Dreaming of a DOS game...")
    window.update()

    payload = payloads[payload_var.get()]
    response = requests.post(url='http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload)

    r = response.json()
    for i in r['images']:
        image_data = i
        if "," in i:  # if the image data includes the data type, split it off
            image_data = i.split(",",1)[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo
    info_label.pack_forget()

    # Re-enable the button and dropdown
    generate_button.config(state="normal", text="    DREAM    ")
    payload_dropdown.config(state="normal")
    info_label.config(text="Sleeping...")
    window.update()


window = tk.Tk()
window.title("P1X DOS Dreamer")
window.geometry('1048x608')
window.configure(bg='black')


info_label = tk.Label(window, text="Sleeping...",fg='white', bg='black')
info_label.grid(row=0, column=0, columnspan=3)


image_label = tk.Label(window,bg='black')
image_label.grid(row=1, column=0, columnspan=3,padx=12, pady=12)

model_var = tk.StringVar(window)
payloads_list = list(payloads.keys())
payload_var = tk.StringVar(value=payloads_list[0])
payload_dropdown = tk.OptionMenu(window, payload_var, payloads_list[0], payloads_list[1], command=load_model)
payload_dropdown.grid(row=2, column=0,padx=12, pady=6)

counter = 0
counter_label = tk.Label(window, text="Dreams: none", fg='white', bg='black')
counter_label.grid(row=2, column=1,padx=12, pady=6)

generate_button = tk.Button(window, text="    DREAM    ", command=generate_image,fg='white', bg='blue')
generate_button.grid(row=2, column=2,padx=12, pady=6)


window.mainloop()
