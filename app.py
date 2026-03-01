import gradio as gr
from main import natural_to_cli

def generate_command(instruction: str) -> str:
    if not instruction.strip():
        return ""
    try:
        return natural_to_cli(instruction)
    except Exception as e:
        return f"Error: {e}"

with gr.Blocks(title="Windows CLI Generator") as demo:
    gr.Markdown("## 🖥️ Windows CLI Command Generator")
    gr.Markdown("Type a natural language instruction and get the Windows CLI command.")

    with gr.Row():
        with gr.Column():
            instruction = gr.Textbox(
                label="Natural Language Instruction",
                placeholder='e.g. "Show all running processes sorted by memory usage"',
                lines=3,
            )
            submit_btn = gr.Button("Generate Command", variant="primary")

        with gr.Column():
            output = gr.Code(
                label="CLI Command",
                language="shell",
                lines=3,
            )

    gr.Examples(
        examples=[
            ["Show my IP address"],
            ["List all .txt files in the Downloads folder"],
            ["Kill the process named notepad"],
            ["Show disk usage for all drives"],
            ["What version of Windows am I running?"],
            ["Find files larger than 100MB on the C drive"],
        ],
        inputs=instruction,
    )

    submit_btn.click(fn=generate_command, inputs=instruction, outputs=output)
    instruction.submit(fn=generate_command, inputs=instruction, outputs=output)

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
