import streamlit as st
from rebranding_app import branding, image_generator

def main():
    st.set_page_config(page_title="Rebranding", layout="wide")
    st.title("Rebranding Produk UMKM")
    
    st.sidebar.header("Input Produk")
    product_name = st.sidebar.text_input("Nama Produk", value="Sarimi", key="prod_name")
    product_type = st.sidebar.text_input("Jenis Produk", value="Mie Instant", key="prod_type")
    
    if st.sidebar.button("Buat Branding"):
        if product_name and product_type:
            with st.spinner("Memproses branding..."):
                result = branding.generate_branding(product_name, product_type)
                st.session_state["branding_result"] = result
        else:
            st.sidebar.error("Mohon isi Nama Produk dan Jenis Produk terlebih dahulu.")
    
    with st.container():
        if "branding_result" in st.session_state:
            result = st.session_state["branding_result"]
            branding_data = result.get("branding", {})
            image_prompt = result.get("image_prompt", "")
            
            if branding_data:
                nama_brand = branding_data.get("nama_brand", "N/A")
                slogan = branding_data.get("slogan", "N/A")
                deskripsi = branding_data.get("deskripsi_singkat", "N/A")
                
                st.markdown(f"<h1 style='text-align: center;'>{nama_brand}</h1>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center;'>{slogan}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-style: italic;'>\"{deskripsi}\"</p>", unsafe_allow_html=True)
            else:
                st.write("Tidak ada data branding.")
            
            if image_prompt:
                try:
                    image = image_generator.generate_image(image_prompt)
                    st.subheader("Produk")
                    st.image(image, caption="desain produk", use_container_width=True)
                except Exception as e:
                    st.error(f"Error saat menghasilkan gambar: {str(e)}")
            else:
                st.warning("Prompt untuk text-to-image tidak tersedia.")
        else:
            st.info("Silahkan masukkan data produk di sidebar dan klik 'Buat Branding'.")
    
if __name__ == "__main__":
    main()
