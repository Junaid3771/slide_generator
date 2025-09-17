import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

def run_slide_generator():
    st.set_page_config(page_title="Text-to-PPT Slide Generator", layout="centered")
    with st.sidebar:
        st.markdown("## 📄 About This App")
        st.markdown(
            """
            Welcome to **Text-to-PPT Slide Generator**! ✨  
            Instantly create slide-ready content from your **text prompt**.
            """
        )

    if "slides" not in st.session_state:
        st.session_state["slides"] = []  # Each slide is {role: ..., content: str}
        
    if "assistant_slides_json" not in st.session_state:
        st.session_state["assistant_slides_json"] = []  # To store structured slide data from assistant

    st.markdown(
        """
        <h1 style='text-align: center;'>📄 Text-to-PPT Slide Generator</h1>
        <p style='text-align: center; font-size: 16px;'>Type your slide content in and preview it below.</p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
    """
    <div style="font-size: 16px;">
        <b>📝 Sample Prompt for Slide Creation:</b><br><br>

        "Create me a 5-slide presentation to show my progress on the drug development pipeline. Use the following data and observations as a reference:

        - Discovery phase completed in Q1 2024 with identification of 3 lead compounds.
        - Preclinical testing conducted by Q4 2024 showed promising efficacy and safety profiles.
        - Phase 1 clinical trial launched in Q1 2025 with 50 healthy volunteers; safety endpoints met.
        - Phase 2 trial underway in Q3 2025 with 120 patients, focusing on dose optimization and preliminary efficacy.
        - Regulatory submission planned for Q2 2026 after Phase 3 completion.

        Organize the slides as a clear, engaging story that highlights key milestones, challenges faced, and next steps in the pipeline. Make it simple enough for a broad audience to understand the progress and importance."
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown("---")
    

    for slide in st.session_state["slides"]:
        with st.chat_message(slide["role"]):
            st.write(slide["content"])

    if prompt := st.chat_input("Type your slide content or topic here...Please give how many slides you want to generate."):
        with st.chat_message("user"):
                st.write(prompt)
        with st.spinner("🎨 Generating slide preview..."):
            
            st.session_state["slides"].append({"role": "user", "content": prompt})

            # history should include both user and assistant messages
            history = [slide for slide in st.session_state["slides"] if slide["role"] in ["user", "assistant"]]
            response = requests.post(
                f"{BACKEND_API_URL}/content_generation_api",
                json={"prompt": prompt, "history": history}
            )
            assistant_content = response.json().get("content", "")
            st.session_state["assistant_slides_json"] = assistant_content
         
            with st.chat_message("assistant"):
                slide_content = ""
                for slide in assistant_content:
                    slide_content += "---\n"
                    slide_content += f"### Slide {slide['slide_no']}"
                    slide_content += f"\n**Category:** {slide['slide_category']}\n"
                    if slide['slide_category'] == 'Title Slide':
                        slide_c = slide['slide_content']
                        slide_content += f"\n\n**Title:** {slide_c.get('title', 'N/A')}\n\n**Subtitle:** {slide_c.get('subtitle', 'N/A')}"
                        slide_content += f"\n\n**content:** {slide_c.get('content', 'N/A')}"
                        slide_content += f"\n\n**Image Description:** {slide_c.get('image_description', 'N/A')}"
                        
                    if slide['slide_category'] == 'Bullet Slide':
                        slide_c = slide['slide_content']
                        slide_content += f"\n\n**Title:** {slide_c.get('title', 'N/A')}"
                        if slide_c.get('bullets'):
                            slide_content += "\n\n**Bullets:**\n" + "\n".join([f"- {point}" for point in slide_c.get('bullets', [])])
                        slide_content += f"\n\n**Image Description:** {slide_c.get('image_description', 'N/A')}"
                    
                    if slide['slide_category'] ==  'Two Column Slide':
                        slide_c = slide['slide_content']
                        slide_content += f"\n\n**Title:** {slide_c.get('title', 'N/A')}"
                        if slide_c.get('left_column'):
                            slide_content += "\n\n**Left Column:**\n" + "\n".join([f"- {item}" for item in slide_c.get('left_column', [])])
                        if slide_c.get('right_column'):
                            slide_content += "\n\n**Right Column:**\n" + "\n".join([f"- {item}" for item in slide_c.get('right_column', [])])
                        slide_content += f"\n\n**Image Description:** {slide_c.get('image_description', 'N/A')}"
                    if slide['slide_category'] == 'Content with Image Slide':
                        slide_c = slide['slide_content']
                        slide_content += f"\n\n**Title:** {slide_c.get('title', 'N/A')}"
                        if slide_c.get('content'):
                            slide_content += f"\n\n**Content:**\n{slide_c.get('content'):}"
                        slide_content += f"\n\n**Image Description:** {slide_c.get('image_description', 'N/A')}"    
                                                
                st.markdown(slide_content)
              #  st.write(st.session_state["assistant_slides_json"])
                
            st.session_state["slides"].append({"role": "assistant", "content": slide_content})

            # Add Create Slide button after showing slide_content
    if st.button("Create Slide"):
             #   st.write(st.session_state["assistant_slides_json"])
                with st.spinner("Generating PowerPoint file..."):
                    ppt_response = requests.post(
                        f"{BACKEND_API_URL}/generate_ppt",
                        json={"slides": st.session_state["assistant_slides_json"]}
                    )
                    if ppt_response.status_code == 200:                        
                        st.download_button(
                            label="Download Presentation",
                            data=ppt_response.content,
                            file_name="generated_presentation.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        )
                    else:
                        st.error("Failed to generate PowerPoint file.")

if __name__ == "__main__":
    run_slide_generator()
