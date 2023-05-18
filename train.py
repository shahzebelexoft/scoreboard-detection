from ultralytics import YOLO

data_path = "/content/datasets/scorebug-detection_dataset/data.yaml"

# Load a model
model = YOLO('yolov8n.yaml')  # build a new model from YAML
model = YOLO('/content/last.pt')  # load a pretrained model (recommended for training)
model = YOLO('yolov8n.yaml').load('/content/last.pt')  # build from YAML and transfer weights

# Train the model
model.train(data = data_path, epochs = 10, imgsz = 640, batch = 32, save = True,
            save_period = 3, optimizer = 'Adam', verbose = True, lr0 = 0.0001, val = True, device = 0)