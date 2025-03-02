from huggingface_hub import InferenceClient
import streamlit as st

IMG_HF_TOKEN = st.secrets["IMG_HF_TOKEN"]
def generate_image(prompt: str):
    
    detailed_prompt = f"{prompt}, hyper realistic, product packaging, 3D rendered, dramatical ,showcase,ads,commercial,marketing,branding,design,product design,product showcase,product ads,product commercial."
    
    client = InferenceClient(provider="hf-inference", api_key=config.IMG_HF_TOKEN)
    try:
        
        image = client.text_to_image(detailed_prompt, model="black-forest-labs/FLUX.1-schnell")
    except Exception as e:
        raise RuntimeError(f"Error generating image: {str(e)}")
    return image
