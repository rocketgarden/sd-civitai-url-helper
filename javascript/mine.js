"use strict";

let mine_updating = false;

async function open_model(event, search_term){
	
	
	let lora_btn = gradioApp().getElementById("ch_js_open_lora_btn")
	if (!lora_btn) {
        return
    }
	
	let js_msg_txtbox = gradioApp().querySelector("#ch_js_lora_filename_txt  > label > textarea");
    if (js_msg_txtbox && search_term) {
		
		console.log("found text box " + search_term);
        // fill to msg box
        js_msg_txtbox.value = search_term;
        updateInput(js_msg_txtbox);
    }
	
    //click hidden button
    lora_btn.click();
	console.log("Opening " + search_term);

    // stop parent event
    event.stopPropagation()
    event.preventDefault()
	
}

onUiUpdate(() => {		
	if(mine_updating) {
		return;
	}

	
	let cardid_suffix = "cards";
	let tab_prefix_list = ["txt2img", "img2img"];
    let model_type_list = ["textual_inversion", "hypernetworks", "checkpoints", "lora"];
	
	let search_term_node = null
	let search_term = null
	
	let extra_network_id = "";
	let extra_network_node = null;
	let cards = null;
	
	extra_network_id = "txt2img"+"_"+"lora"+"_"+cardid_suffix;
	
	extra_network_node = gradioApp().getElementById(extra_network_id);
	
	if(!extra_network_node) {
		return;
	}
	
	cards = extra_network_node.querySelectorAll(".card");
	
	
	for (let card of cards) {		
	
		let btn = card.querySelector(".open-button")
		if(btn) {
			console.log("Arrows already added");
			return; // already added them
		}
		
		search_term_node = card.querySelector(".actions .additional .search_term"); //TODO use replace preview filename instead
		if (!search_term_node){
			console.log("can not find search_term node for cards in " + extra_network_id);
			continue;
		}

		// get search_term
		search_term = search_term_node.innerHTML;
		if (!search_term) {
			console.log("search_term is empty for cards in " + extra_network_id);
			continue;
		}
		
		mine_updating = true;

		btn = document.createElement("div");
		btn.classList.add('open-button');
		
		btn.setAttribute("onclick","open_model(event, '"+search_term+"')");
		
		card.appendChild(btn);
	}
});



function updateInput(target) {
    let e = new Event("input", {bubbles: true});
    Object.defineProperty(e, "target", {value: target});
    target.dispatchEvent(e);
}