# Interior Planner Bot

Interior Planner Bot is a smart Streamlit application that identifies the style of your furniture and room aesthetic from an image, then generates a personalized interior styling guide. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot offers color palettes, layout tips, recommended decor, and shopping suggestions — all tailored to your unique space.

## Folder Structure

```
Interior-Planner-Bot/
├── interior-planner-bot.py
├── README.md
└── requirements.txt
```

* **interior-planner-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

### 🛋️ Room Image Input

Upload a photo of your room with visible furniture and surroundings. The bot uses this image to determine the furniture style and room aesthetic.

### 🧠 AI-Powered Style Recognition

The **Furniture Style Identifier** agent analyzes the image and outputs the dominant furniture style (e.g., Mid-Century, Modern) and room vibe (e.g., Scandinavian, Boho).

### 🌐 Decor Research via Web

The **Interior Decor Researcher** agent creates a targeted search using SerpAPI to gather real decor ideas, layout inspirations, and color recommendations from across the web.

### 🧾 Personalized Styling Report

The **Room Design Advisor** agent combines the style insights and research links to generate a highly detailed, actionable Markdown report. It includes:

* 🎨 **Color Palette Suggestions**
* 📐 **Layout Tips**
* 🛋️ **Recommended Decor Pieces**
* 🛒 **Shopping Suggestions**

### 📥 Downloadable Report

Save your room styling guide as a Markdown file with the click of a button.

### 🖥️ Clean Streamlit Interface

A modern, intuitive layout with a sidebar for API configuration and a wide canvas for reports and previews.

## Prerequisites

* Python 3.11 or higher
* An [OpenAI API key](https://platform.openai.com/account/api-keys)
* A [SerpAPI key](https://serpapi.com/manage-api-key)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Interior-Planner-Bot.git
   cd Interior-Planner-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run interior-planner-bot.py
   ```

2. **In your browser**:

   * Enter your **OpenAI API key** and **SerpAPI key** in the sidebar.
   * Upload a photo that shows the furniture and room decor.
   * Click **🪑 Generate Styling Report**.
   * View your personalized room styling report and download it as a `.md` file.

## Code Overview

* **`render_sidebar()`**: Collects API keys via the sidebar and stores them in Streamlit session state.
* **`render_room_profile()`**: Allows users to upload a room image with furniture.
* **`generate_room_report()`**:

  * Uses the `Furniture Style Identifier` to analyze the image.
  * Runs the `Interior Decor Researcher` to find decor links via SerpAPI.
  * Passes both to the `Room Design Advisor` to generate a complete interior styling report.
* **`main()`**: Orchestrates layout, input flow, and report generation logic.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest improvements, report bugs, or open a pull request. Please keep changes clean, well-documented, and aligned with the app’s mission.