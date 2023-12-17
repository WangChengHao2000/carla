import torch
import torchvision
import cv2

model = torch.hub.load(
    repo_or_dir="./yolov5",
    model="custom",
    path="yolov5/yolov5n.pt",
    source="local",
)

image = cv2.imread("data/rgb/img.png")
image = cv2.resize(image, (640, 640))

model.eval()
result = model(image)
print(result)

