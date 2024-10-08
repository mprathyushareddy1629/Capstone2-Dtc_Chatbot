# # from llama_cpp import Llama
# # import gradio as gr

# # # Load the Phi-2 model
# # model_path = "./models/phi-2.Q5_K_M.gguf"  # Adjust if needed
# # llm = Llama(model_path=model_path, n_ctx=2048) 

# from llama_cpp import Llama
# import gradio as gr
# from huggingface_hub import hf_hub_download
# from process_pdf import extract_text_from_pdf

# # Load the Phi-2 model directly from Hugging Face
# model_path = hf_hub_download(
#     repo_id="TheBloke/phi-2-GGUF", 
#     filename="phi-2.Q5_K_M.gguf",
#     local_dir="./models"  # Optional: Specify a local directory to save the model
# )

# llm = Llama(model_path=model_path, n_ctx=2048) 


# # Load the processed PDF text (you'll need to integrate this properly later)

# pdf_text = extract_text_from_pdf('data/DTC_Codes-m.pdf')  # Make sure the path is correct

# def diagnose_error(error_code):
#   """Diagnoses the error code using the model and PDF data."""

#   prompt = f"""
#   You are an expert automotive diagnostic assistant. 
#   Utilize the following DTC (Diagnostic Trouble Code) reference information to provide a clear and concise diagnosis for the given error code. Additionally, offer a bulleted list of potential solutions to address the issue.

#   Reference information:
#   {pdf_text}

#   Error code:
#   {error_code}

#   Diagnosis and solutions:
#   """

#   output = llm(prompt, max_tokens=512, temperature=0.7, top_p=1)
#   return output['choices'][0]['text']

# # Create the Gradio interface
# iface = gr.Interface(
#   fn=diagnose_error,
#   inputs=gr.Textbox(label="Enter the DTC error code:"),
#   outputs=gr.Textbox(label="Diagnosis and possible solutions:"),
# )

# iface.launch()




from llama_cpp import Llama
import gradio as gr
from huggingface_hub import hf_hub_download
from process_pdf import extract_text_from_pdf
import re
# from evaluate_section_finder import evaluate_section_finder

# Load the Phi-2 model directly from Hugging Face
model_path = hf_hub_download(
    repo_id="TheBloke/phi-2-GGUF", 
    filename="phi-2.Q5_K_M.gguf",
    local_dir="./models" 
)

llm = Llama(model_path=model_path, n_ctx=2048) 

# Load the processed PDF text
pdf_text = extract_text_from_pdf('data/DTC_Codes-m.pdf')

# def find_relevant_section(pdf_text, error_code):
#   """Finds the section in the PDF text that is exactly relevant to the given error code."""

#   # Assuming error code sections start with "P" followed by digits
#   sections = pdf_text.split("P") 

#   for section in sections:
#     if section.startswith(error_code):  # Case-sensitive check
#       return "P" + section  # Include the "P" we split on

#   return ""  # No relevant section found
def find_relevant_section(pdf_text, error_code):
  """Finds the section in the PDF text that is likely relevant to the given error code.
  This improved version handles potential variations in error code formatting."""

  # Use regex to capture potential error code patterns, including those with decimals or hyphens
  pattern = rf"P\d+[.\-]?\d*\s+{error_code}" 
  match = re.search(pattern, pdf_text)

  if match:
    # Extract the entire section from the start of the matched "P" to the next "P" 
    start = match.start()
    end = pdf_text.find("P", start + 1)  # Find the next "P"
    if end == -1:  # If no next "P" is found, take the rest of the text
        end = len(pdf_text)
    return pdf_text[start:end].strip()

  return ""  # No relevant section found
def respond(chat_history, message):
    """Handles user messages and generates responses."""
    error_code = message  # Assuming the user enters the error code directly

    # Basic input validation
    if not error_code:
        return "", chat_history.append((message, "Please enter a valid DTC error code."))

    # Check if error code is in the PDF data
    if error_code.upper() not in pdf_text:
        return "", chat_history.append((message, "Error code not found in the reference. Please double-check the code or provide additional information."))
    
    relevant_section = find_relevant_section(pdf_text, error_code)

    prompt = f"""
    You are an expert automotive diagnostic assistant. 

      Carefully review the following DTC (Diagnostic Trouble Code) reference information. Then, provide a structured response that includes:

      * A clear explanation of what this error code means, referencing the provided information
      * A concise diagnosis of the potential issue, based on the reference details
      * Potential solutions or next steps to address the issue and complete with conclusion


    Reference information:

    {relevant_section}


    Error code:
    {error_code}

    Diagnosis and solutions:
    """

    # try:
    #     output = llm(prompt, max_tokens=128, temperature=0.5, top_p=0.9)
    #     response = output['choices'][0]['text']
    # except Exception as e:
    #     response = f"An error occurred during diagnosis: {e}" 

    # chat_history.append((message, response)) 
    # return "", chat_history 
    try:
        output = llm(prompt, max_tokens=200, temperature=0.2, top_p=0.9)
        response_text = output['choices'][0]['text']

        # Extract the Meaning and Diagnosis sections from the response
        meaning_start = response_text.find("**Meaning:**") + len("**Meaning:**")
        diagnosis_start = response_text.find("**Diagnosis:**") + len("**Diagnosis:**")

        # Handle cases where the model doesn't follow the exact format
        if meaning_start == -1 or diagnosis_start == -1:
            response = "The model's response is not in the expected format. Please try again or rephrase your query."
        else:
            meaning = response_text[meaning_start:diagnosis_start].strip()
            diagnosis = response_text[diagnosis_start:].strip()

            # Format the output using Markdown for better readability
            formatted_response = f"""
            Diagnosis: {diagnosis}
            """
            response = formatted_response

    except Exception as e:
        response = f"An error occurred during diagnosis: {e}"

    chat_history.append((message, response))
    return "", chat_history    


 

# Create the Gradio Chatbot interface
with gr.Blocks(css="""
    #chatbot { height: 400px; }  /* Adjust height as needed */
    """) as iface:
    gr.Markdown("<center><h1>DTC Diagnostic Chatbot</h1></center>")  # Centered title

    chatbot = gr.Chatbot(elem_id="chatbot") 
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(respond, [chatbot, msg], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

iface.launch()