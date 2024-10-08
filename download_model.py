from huggingface_hub import snapshot_download

model_path = snapshot_download(
    repo_id="TheBloke/phi-2-GGUF",
    repo_type="model",
    local_dir="./models",
)

print(f"Model downloaded to: {model_path}")