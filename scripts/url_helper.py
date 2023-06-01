import modules.scripts as scripts
import gradio as gr
import os
import webbrowser
import requests
import random
import io
import hashlib
import json
import shutil
import re
import modules
from modules import script_callbacks
from pprint import pprint
        
def on_before_component(component, **kwargs):
    if ('elem_id' in kwargs) and (kwargs["elem_id"] == "txt2img_prompt"):
        print("## ## ## TEST COMP ## ## ##")
        js_lora_filename_txt = gr.Textbox(label="Request Msg From Js", elem_id="uh_js_lora_filename_txt", visible=False)

        js_open_lora_btn = gr.Button(value="Open Lora Url", visible=False, elem_id="uh_js_open_lora_btn")
        js_open_lora_btn.click(fn=open_model_url_by_file, inputs=[js_lora_filename_txt])
    
def read_chunks(file, size=io.DEFAULT_BUFFER_SIZE):
    while True:
        chunk = file.read(size)
        if not chunk:
            break
        yield chunk

def gen_file_sha256(filname):
    print("Use Memory Optimized SHA256")
    blocksize=1 << 20
    h = hashlib.sha256()
    length = 0
    with open(os.path.realpath(filname), 'rb') as f:
        for block in read_chunks(f, size=blocksize):
            length += len(block)
            h.update(block)

    hash_value =  h.hexdigest()
    print("sha256: " + hash_value)
    return hash_value

def open_model_url_by_file(filename):

    if filename[:1] == "/":
        filename = filename[1:]

    root_path = os.getcwd()
    path = os.path.join(root_path, "models", "Lora", filename)
    print("Calculating SHA256 for" + path)
    
    model_hash = gen_file_sha256(path)
    modelId = get_model_id_from_hash(model_hash)
    
    if(modelId):
        url = "https://civitai.com/models/" + modelId
        webbrowser.open_new_tab(url)
    

def get_model_id_from_hash(model_hash):
    response = requests.get("https://civitai.com/api/v1/model-versions/by-hash/" + model_hash).json()
    if('modelId' in response):
        modelId = str(response['modelId'])
    
        print("Found Model ID: " + modelId)
        return modelId
    else:
        print("Model not found in CivitAi DB")
        return None

# Add the callback!!
script_callbacks.on_before_component(on_before_component)