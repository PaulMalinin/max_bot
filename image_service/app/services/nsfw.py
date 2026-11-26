from opennsfw_onnx import NSFWClassifier
from PIL import Image

classifier = NSFWClassifier()

NSFW_THRESHOLD = 0.8

def is_nsfw(image: Image.Image) -> bool:
    pred = classifier.classify(image)

    return pred.nsfw > NSFW_THRESHOLD