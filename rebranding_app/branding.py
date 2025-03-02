import json
import re
from huggingface_hub import InferenceClient
from rebranding_app import config

def generate_branding(product_name: str, product_type: str):
    system_prompt = (
        "Anda adalah konsultan branding yang ahli. Berdasarkan nama produk dan jenis produk, "
        "buatlah identitas merek yang kuat dan menarik. Sertakan nama merek, slogan yang mudah diingat, "
        "dan deskripsi singkat yang menggambarkan identitas merek. Selain itu, buatlah prompt text-to-image "
        "untuk menghasilkan logo. Pastikan prompt tersebut mencantumkan nama merek dalam tanda kutip. "
        "Outputkan hasil dalam format JSON persis seperti berikut:\n\n"
        '=== BRANDING ===\n'
        '**Nama Merek:** Nama Merk\n'
        '**Slogan:** [Slogan yang menarik dan Profesional]\n'
        '**Deskripsi Singkat:** [Deskripsi singkat tentang identitas merek]\n'
        '**Prompt Gambar:** [Prompt untuk menghasilkan visualisasi produk]\n\n'
        "Keluaran harus berupa JSON dengan struktur:\n"
        '{"branding": {"nama_brand": "ContohMerek", "slogan": "Slogan Menarik dalam bahasa indonesia", "deskripsi_singkat dalam bahasa indonesia": "Deskripsi singkat"}, "image_prompt": "prompt untuk membuat visualisasi iklan produk dari brand tersebut, pastikan nama brand ada di dalam tanda kutip ( contoh "Sarimi") pastikan tercipta visualisasi iklan yang menarik dan modern dan dalam bahasa inggris, maksimal 50 kata, gunakan tanda koma untuk efisiensi elemen prompt."}'
    )
    
    user_prompt = (
        f"Nama Produk: {product_name}\n"
        f"Jenis Produk: {product_type}\n\n"
        "Buat identitas merek sesuai dengan format yang telah diberikan di atas."
    )
    
    client = InferenceClient(provider="hf-inference", api_key=config.LLM_HF_TOKEN)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=messages,
            max_tokens=2000,
        )
    except Exception as e:
        return {
            "branding": {
                "nama_brand": "",
                "slogan": "",
                "deskripsi_singkat": f"Error memanggil LLM: {str(e)}"
            },
            "image_prompt": ""
        }
    
    output_text = response.choices[0].message.get("content", "").strip()
    

    try:
        data = json.loads(output_text)
    except Exception:
        try:
            json_start = output_text.find('{')
            json_end = output_text.rfind('}') + 1
            json_str = output_text[json_start:json_end]
            data = json.loads(json_str)
        except Exception:
            return {
                "branding": {
                    "nama_brand": "",
                    "slogan": "",
                    "deskripsi_singkat": output_text
                },
                "image_prompt": ""
            }
    
    branding_data = data.get("branding", {})
    image_prompt = data.get("image_prompt", "").strip()
    nama_brand = branding_data.get("nama_brand", product_name)
    
    
    if f'"{nama_brand}"' not in image_prompt:
        if "logo" in image_prompt.lower():
            image_prompt = re.sub(r'(logo)', r'\1 "' + nama_brand + r'"', image_prompt, flags=re.IGNORECASE)
        else:
            image_prompt = f'"{nama_brand}" ' + image_prompt
    
    
    image_prompt = image_prompt.replace("縫の", "kuning")
    
    return {"branding": branding_data, "image_prompt": image_prompt}
