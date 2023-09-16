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
from modules import hashes
from pprint import pprint
from pathlib import Path
        
def on_before_component(component, **kwargs):
    if ('elem_id' in kwargs) and (kwargs["elem_id"] == "txt2img_prompt"):
        js_lora_search_name_txt = gr.Textbox(label="Request Msg From Js", elem_id="uh_js_lora_search_name_txt", visible=False)

        js_open_lora_btn = gr.Button(value="Open Lora Url", visible=False, elem_id="uh_js_open_lora_btn")
        js_open_lora_btn.click(fn=open_model_url_by_file, inputs=[js_lora_search_name_txt])

def open_model_url_by_file(search_name):

    print("Opening the model: " + search_name)

    # Normalize the slashes to the correct kind for the current OS
    search_name = Path(search_name).as_posix()

    if search_name.startswith("/"):
        search_name = search_name[1:]

    root_path = Path.cwd()
    filename = root_path / "models" / "Lora" / search_name

    if not filename.is_file():
        print(f"Model at {filename} no longer exists!")
        return

    name = filename.stem  # name is just base filename without extension
    
    # use webui hash function to get cacheing
    model_hash = str(hashes.sha256(filename, "lora/" + name, use_addnet_hash=False)) # civitai wants regular hash
    
    modelId, versionId = get_model_id_from_hash(model_hash)
    
    if(modelId):
        url = "https://civitai.com/models/" + modelId + "?modelVersionId=" + versionId
        webbrowser.open_new_tab(url)
    

def get_model_id_from_hash(model_hash):
    response = requests.get("https://civitai.com/api/v1/model-versions/by-hash/" + model_hash).json()
    if('modelId' in response):
        modelId = str(response['modelId'])
        versionId = str(response['id'])
        
        title = str(response['model']['name'])
    
        print("Found " + title[:20] + " ID: " + modelId + " : " + versionId )
        return (modelId, versionId)
    else:
        print("Model not found in CivitAi DB")
        return (None, None)

# Add the callback!!
script_callbacks.on_before_component(on_before_component)