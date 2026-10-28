import torch
import requests
from torchvision import transforms
import gradio as gr

TEST_DATA_FOLDER=os.path.join(os.path.dirname(__file__), "../../test/test-data")
# Download human-readable labels for ImageNet
response = requests.get("https://git.io/JJkYN")
labels = [l.strip() for l in response.text.split("\n") if l.strip()]

# Define image preprocessing (IMPORTANT for ResNet)
transform = transforms.Compose([ transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

def predict(inp):
    # preprocess image
    inp = transform(inp).unsqueeze(0)

    # ensure model runs in inference mode
    with torch.no_grad():
        prediction = torch.nn.functional.softmax(model(inp)[0], dim=0)

    # map predictions to labels
    confidences = {
        labels[i]: float(prediction[i])
        for i in range(len(labels))
    }

    return confidences

demo2 = gr.Interface(fn=predict,
        inputs=gr.Image(type="pil"),
        outputs=gr.Label(num_top_classes=3),
        examples=[os.path.join(TEST_DATA_FOLDER, "landscape.png"), os.path.join(TEST_DATA_FOLDER, "painting.png")])
demo2.launch(server_name="0.0.0.0", server_port= 7860)
