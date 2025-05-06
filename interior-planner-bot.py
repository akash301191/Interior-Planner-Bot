import tempfile
import streamlit as st

from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_room_profile():
    st.markdown("---")
    col1, col2 = st.columns(2)

    # Column 1: Upload Furniture + Room Image
    with col1:
        st.subheader("📸 Upload Room Image with Furniture")
        uploaded_image = st.file_uploader(
            "Upload an image that includes the furniture and surrounding room aesthetic",
            type=["jpg", "jpeg", "png"]
        )

    return {
        "uploaded_image": uploaded_image,
    }

def generate_room_report(room_profile):
    uploaded_image = room_profile["uploaded_image"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_image.getvalue())
        image_path = tmp.name

    # Step 1: Style Identifier
    style_identifier = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Furniture Style Identifier",
        role="Identifies the furniture style and dominant room aesthetic from a room photo.",
        description=(
            "You are a furniture and interior design expert. When given a photo of a furnished room, "
            "you identify the style of the visible furniture (e.g., mid-century, modern, boho), the dominant room aesthetic, "
            "and describe the visual elements in a concise format."
        ),
        instructions=[
            "Analyze the furniture in the image and identify its style (e.g., mid-century, traditional, industrial).",
            "Determine the overall room aesthetic (e.g., modern minimalist, Scandinavian, eclectic).",
            "Describe the key visual cues (furniture material, shapes, colors, layout).",
            "Return a structured markdown like:\n\n"
            "**Furniture Style**: <Style>\n"
            "**Room Aesthetic**: <Aesthetic>\n"
            "**Visual Cues**: <Bullet list describing textures, colors, design features>",
            "Be concise and visually grounded. If unsure, offer the closest match."
        ],
        markdown=True
    )

    style_response = style_identifier.run(
        "Identify the furniture style and room aesthetic in this image.",
        images=[Image(filepath=image_path)]
    )
    design_identification = style_response.content

    # Step 2: Styling Researcher
    decor_researcher = Agent(
        name="Interior Decor Researcher",
        role="Finds layout and decor suggestions based on the identified furniture style and room aesthetic.",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a decor researcher. Based on the identified furniture style and room aesthetic, 
            generate a focused Google search to discover layout ideas, color palettes, and decor suggestions.
            Your task is to return 10 high-quality links related to furniture arrangement, wall colors, accessories, 
            and room styling for the given interior style.
        """),
        instructions=[
            "Create one focused Google search query using the style and aesthetic provided.",
            "Use `search_google` with that query.",
            "Review the top results and return a list of the 10 most relevant URLs.",
            "Exclude duplicates, irrelevant content, and ads.",
            "Format the output as a clean markdown list of links (no summaries or raw URLs)."
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
        markdown=True
    )

    research_response = decor_researcher.run(design_identification)
    decor_links = research_response.content

    # Step 3: Room Design Advisor
    interior_advisor = Agent(
        name="Room Design Advisor",
        role="Generates a comprehensive interior styling guide using design knowledge and referenced decor research.",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are an expert interior design consultant. Given:
            1. A furniture and aesthetic summary
            2. A list of researched decor links

            Your goal is to generate a highly detailed, professional-quality styling guide that someone can use to transform their room.
        """),
        instructions=[
            "Start with a section titled ## 🪑 Style Summary.",
            "In this section, clearly list the following in bold or markdown:\n"
            "- **Furniture Style**\n"
            "- **Room Aesthetic**\n"
            "- **Visual Cues** (as a markdown bullet list)\n"
            "- A short paragraph explaining what defines this style, with examples of typical materials, forms, and influences.",

            "",
            "Then continue with a section titled ## 🖼️ Room Styling Guide, divided into the following subsections:",
            
            "### 🎨 Color Palette Suggestions",
            "- Recommend 2–3 harmonious color palette options.\n"
            "- Include suggested wall colors, furniture tones, and fabric choices.\n"
            "- Mention which colors are dominant and which are accents.\n"
            "- Provide reasoning for how the palette supports the aesthetic.\n"
            "- Include links from references if applicable.",

            "### 📐 Layout Tips",
            "- Describe how to arrange furniture for this style.\n"
            "- Include advice on balance, symmetry, traffic flow, and space-saving if needed.\n"
            "- Mention lighting placement or focal points if relevant.\n"
            "- Offer tips for small or large spaces as needed.\n"
            "- Use short paragraphs or bullet lists.",

            "### 🛋️ Recommended Decor Pieces",
            "- Suggest 5–7 types of decor items that suit the style (e.g., brass lamp, tufted ottoman, arched mirror).\n"
            "- Describe what makes each item a match (material, form, color, placement).\n"
            "- Mention ideal fabric types, finishes, and detailing to look for.\n"
            "- Provide inspiration from research links.",

            "### 🛒 Shopping Suggestions",
            "- Based on the research links, recommend specific categories of products or common items to search for online.\n"
            "- Instead of listing raw URLs, write anchor-style markdown links (e.g., [Mid-Century Sofas](https://example.com)).\n"
            "- Suggest 5–8 helpful sources: decor marketplaces, style-specific blogs, etc.\n"
            "- Group by purpose: furniture, lighting, wall decor, textiles, etc.",

            "",
            "Ensure the tone is informative yet warm, like a professional designer explaining to a client.",
            "DO NOT simply redirect to the links—your response must stand on its own as a complete, actionable styling plan.",
            "Use headings, bullet points, and short paragraphs for clarity.",
            "All sections must be well-explained, grounded in visual reasoning, and offer practical next steps."
        ],
        markdown=True,
        add_datetime_to_instructions=True
    )

    advisor_prompt = f"""
    Room Style Identification:
    {design_identification}

    Research Results:
    {decor_links}

    Use these to generate a detailed room styling report.
    """

    report_response = interior_advisor.run(advisor_prompt)
    room_styling_report = report_response.content

    return room_styling_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Interior Planner Bot", page_icon="🛋️", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🛋️ Interior Planner Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Interior Planner Bot — a creative Streamlit tool that detects furniture style from your image and blends it with your room’s vibe, offering decor ideas, layout tips, and shopping insights.",
        unsafe_allow_html=True
    )

    render_sidebar()
    room_profile = render_room_profile()

    st.markdown("---")  

    # Trigger Report Generation
    if st.button("🪑 Generate Styling Report"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        elif "uploaded_image" not in room_profile or not room_profile["uploaded_image"]:
            st.error("Please upload a room image before generating the report.")
        else:
            with st.spinner("Analyzing your room and generating a personalized styling guide..."):
                report = generate_room_report(room_profile)
                st.session_state.room_report = report
                st.session_state.image = room_profile["uploaded_image"]

    # Display and Download Report
    if "room_report" in st.session_state:
        st.markdown("## 🖼️ Uploaded Room Image")
        st.image(st.session_state.image, use_container_width=False)

        st.markdown(st.session_state.room_report, unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Styling Report",
            data=st.session_state.room_report,
            file_name="interior_styling_report.md",
            mime="text/markdown"
        )


if __name__ == "__main__":
    main()
