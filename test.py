from ultralytics import YOLO

test_dir = r"datasets\scorebug-detection_dataset\test\images"

# Provide the path to the pre-trained model
model_path = r"runs\detect\train5\weights\best.pt"

# Load the YOLO model
model = YOLO(model_path)

# Test the model
result = model.predict(test_dir, conf = 0.7, save = True)