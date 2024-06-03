import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

def run_demo():
    demo = gr.Interface(
        fn=greet,
        inputs=["text", "slider"],
        outputs=["text"],
    )
    demo.launch()


if __name__ == '__main__':
    run_demo()