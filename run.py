# run.py
import gradio as gr
from agent import ask_weather_agent

def main():
    demo = gr.Interface(
        fn=ask_weather_agent,
        inputs=gr.Textbox(label="Ask about the weather"),
        outputs=gr.Textbox(label="Response"),
        title="🌤️ SkyCast - AI Weather Assistant",
        description="Ask in natural language like 'What's the weather in London?'"
    )
    demo.launch()

if __name__ == "__main__":
    main()
