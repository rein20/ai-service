import gradio as gr

from eval import get_eval_data
from utils import summarize, get_prompt


def fn(conversation, history):
    prompt = get_prompt()
    summary = summarize(
        conversation,
        prompt,
        temperature=0.0,
        model='claude-3-haiku-20240307'
    )
    return summary


demo = gr.ChatInterface(
    fn=fn,
    examples=[
        get_eval_data()[0],
        get_eval_data()[1]
    ],
    title="톡 대화 요약 데모"
)
demo.launch()