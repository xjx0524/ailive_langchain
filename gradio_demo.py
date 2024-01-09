import gradio as gr
import rag

def chat(msg, history):
    return '哈哈'

gr.ChatInterface(
    rag.chat,
    chatbot=gr.Chatbot(),
    textbox=gr.Textbox(placeholder="Chat Here.", container=False, scale=7),
    title="相声大师",
    theme="soft",
    examples=["你是谁", "来段科目三", "你知道南方小土豆吗？"],
    cache_examples=False,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
).launch()