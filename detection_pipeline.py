from groundingdino.util.inference import load_model, predict
from segment_anything import SamPredictor, sam_model_registry
import cv2
import torch
import numpy as np
from PIL import Image

# Load Grounding DINO
dino_model = load_model("groundingdino_swint_ogc.pth", config_path="GroundingDINO_SwinT_OGC.py")

# Load SAM
sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h_4b8939.pth").cuda()
sam_predictor = SamPredictor(sam)

# Example detection function
def detect_clarifiers(image_path, text_prompt="circular clarifier"):
    image = Image.open(image_path).convert("RGB")
    boxes, logits, phrases = predict(dino_model, image, text_prompt, box_threshold=0.3)

    # Convert to numpy
    image_np = np.array(image)
    sam_predictor.set_image(image_np)

    masks = []
    for box in boxes:
        mask, _, _ = sam_predictor.predict(box=box)
        masks.append(mask)

    # Optional: filter masks by circularity
    valid_clarifiers = []
    for mask in masks:
        contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * (area / (perimeter ** 2))
            if 0.7 < circularity < 1.2:
                valid_clarifiers.append(cnt)

    return len(valid_clarifiers), valid_clarifiers
