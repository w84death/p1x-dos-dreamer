import io
import base64
import requests
import argparse
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

payloads = {
    "Riven The Sequel to MYST": {
        "prompt": "p1xriven",
        "sampling_method": "other_method",
        "model": "p1x-rivendos_3100.safetensors",
        "sampling_method": "Euler a",
        "steps": 28,
        "cfg_scale": 8,
        "width": 1024,
        "height": 512
    },
    "Indiana Jones® and the Fate of Atlantis": {
        "prompt": "screenshot from DOS game p1xindianajones",
        "sampling_method": "DPM++ 2M Karras",
        "model": "p1x-indianajonesdos_6800.safetensors",
        "sampling_method": "Euler a",
        "steps": 14,
        "cfg_scale": 7,
        "width": 1024,
        "height": 512
    }

    # Add more payloads here
}

default_prompt = "<--- CHOOSE MODEL FIRST"
current_image = None

parser = argparse.ArgumentParser(description='P1X DOS Dreamer')
parser.add_argument('--ip', type=str, default='127.0.0.1', help='The IP of the Automatic1111 API endpoint')
args = parser.parse_args()

def load_model(model_name):
    # Disable the button and dropdown
    generate_button.config(state="disabled", text="...")
    payload_dropdown.config(state="disabled")

    if model_name == "--- CHOOSE MODEL ---":
        payload_dropdown.config(state="normal")
        return

    option_payload = {
        "sd_model_checkpoint": payloads[model_name]["model"]
    }

    response = requests.post(url=f'http://{args.ip}:7860/sdapi/v1/options', json=option_payload)
    payload_var = tk.StringVar(value=model_name)

    default_prompt =  payloads[model_name]["prompt"]
    prompt_entry.delete(0, 'end')
    prompt_entry.insert(0, default_prompt)

    # Re-enable the button and dropdown
    generate_button.config(state="normal", text="    DREAM    ")
    payload_dropdown.config(state="normal")

def generate_image():
    global current_image # use the global variable current_image

    # Disable the button and dropdown
    generate_button.config(state="disabled", text="...")
    payload_dropdown.config(state="disabled")

    info_label.config(text="Dreaming of an old game...")
    window.update()

    payload = payloads[payload_var.get()]
    payload['prompt'] = prompt_entry.get()
    response = requests.post(url=f'http://{args.ip}:7860/sdapi/v1/txt2img', json=payload)

    r = response.json()
    for i in r['images']:
        image_data = i
        if "," in i:
            image_data = i.split(",",1)[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

    current_image = image
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo
    info_label.pack_forget()

    # Re-enable the button and dropdown
    generate_button.config(state="normal", text="    DREAM    ")
    payload_dropdown.config(state="normal")
    info_label.config(text="Sleeping...")
    window.update()

def save_image():
    # open save file dialog
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))

    if file_path:
        # save the image
        current_image.save(file_path)


window = tk.Tk()
window.title("P1X DOS Dreamer // alpha-1 / by Krzysztof Krystian Jankowski")
window.geometry('1048x608')
window.configure(bg='black')


info_label = tk.Label(window, text="Sleeping...",fg='white', bg='black')
info_label.grid(row=0, column=0, columnspan=4)


image_label = tk.Label(window,bg='black')
image_label.grid(row=1, column=0, columnspan=4,padx=12, pady=12)

model_var = tk.StringVar(window)
payloads_list = list(payloads.keys())
payload_var = tk.StringVar(value="--- CHOOSE MODEL ---")
payload_dropdown = tk.OptionMenu(window, payload_var, "--- CHOOSE MODEL ---", payloads_list[0], payloads_list[1], command=load_model)
payload_dropdown.grid(row=2, column=0,padx=12, pady=6)

# Create input field
prompt_entry = tk.Entry(window, width=64)
prompt_entry.insert(0, default_prompt)
prompt_entry.grid(row=2, column=1,padx=12, pady=6)

generate_button = tk.Button(window, text="    DREAM    ", command=generate_image,fg='white', bg='blue')
generate_button.grid(row=2, column=2,padx=12, pady=6)

save_button = tk.Button(window, text="Save Image", command=save_image)
save_button.grid(row=2, column=3,padx=12, pady=6)

window.mainloop()

