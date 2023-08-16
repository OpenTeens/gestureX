# Multi-functional extensible project based on gesture recognition
This is a sample code program that builds functionalities (virtual keyboard, touchpad, and drawboard) upon hand gesture recognition project ([this one](https://github.com/Kazuhito00/hand-gesture-recognition-using-mediapipe)) which utilizes a simple MLP using key points detected with Mediapipe.

![mqlrf-s6x16](https://user-images.githubusercontent.com/37477845/102222442-c452cd00-3f26-11eb-93ec-c387c98231be.gif)

This repository contains the following contents.
* Sample program
* Hand sign recognition model(TFLite)
* Hand controlled virtual touchpad
* Hand controlled virtual keyboard
* Hand controlled virtual drawboard
# Requirements
    * mediapipe 0.8.1
    * OpenCV 3.4.2 or Later
    * Tensorflow 2.3.0 or Later<br>tf-nightly 2.5.0.dev or later (Only when creating a TFLite for an LSTM model)
* scikit-learn 0.23.2 or Later (Only if you want to display the confusion matrix)
* matplotlib 3.3.2 or Later (Only if you want to display the confusion matrix)
* pyautogui 0.9.54 or Later

# Demo
Here's how to run the demo using your webcam.
```bash
python app.py
```

The following options can be specified when running the demo.
* --device<br>Specifying the camera device number (Default：0)
* --width<br>Width at the time of camera capture (Default：960)
* --height<br>Height at the time of camera capture (Default：540)
* --use_static_image_mode<br>Whether to use static_image_mode option for MediaPipe inference (Default：Unspecified)
* --min_detection_confidence<br>
  Detection confidence threshold (Default：0.5)
* --min_tracking_confidence<br>
  Tracking confidence threshold (Default：0.5)
* --function to be enabled
* --max_num of hands detected

# Directory
<pre>
│  app.py
│  keypoint_classification.ipynb
│  point_history_classification.ipynb
│  
├─model
│  ├─keypoint_classifier
│  │  │  keypoint.csv
│  │  │  keypoint_classifier.hdf5
│  │  │  keypoint_classifier.py
│  │  │  keypoint_classifier.tflite
│  │  └─ keypoint_classifier_label.csv
│  │          
│  └─point_history_classifier
│      │  point_history.csv
│      │  point_history_classifier.hdf5
│      │  point_history_classifier.py
│      │  point_history_classifier.tflite
│      └─ point_history_classifier_label.csv
├─plugin
│  ├─cnn_model
│  │  │  dataCNN
│  │  │  cnn_labels.json
│  │  │  cnn.py
│  │  │  getdata.py
│  │  │  load_model.py
│  │  └─ make_labels.py
│  │ 
│  │ blackboard.py
│  │ keyboard.py
│  │ mouse.py
│  │ stablediffusion.py
│  │ UI.py         
│  └─point_history_classifier
│     
│          
└─utils
    └─cvfpscalc.py
</pre>
### app.py
This is a sample program for inference.<br>
In addition, learning data (key points) for hand sign recognition,<br>
You can also collect training data (index finger coordinate history) for finger gesture recognition.

### keypoint_classification.ipynb
This is a model training script for hand sign recognition.

### point_history_classification.ipynb
This is a model training script for finger gesture recognition.

### model/keypoint_classifier
This directory stores files related to hand sign recognition.<br>
The following files are stored.
* Training data(keypoint.csv)
* Trained model(keypoint_classifier.tflite)
* Label data(keypoint_classifier_label.csv)
* Inference module(keypoint_classifier.py)

### model/point_history_classifier
This directory stores files related to finger gesture recognition.<br>
The following files are stored.
* Training data(point_history.csv)
* Trained model(point_history_classifier.tflite)
* Label data(point_history_classifier_label.csv)
* Inference module(point_history_classifier.py)

### model/point_history_classifier
This is directory stores the different functions as plugins that will be inserted in app.py.<br>
The following folders/files are stored.
* cnn_model
* blackboard.py
* keyboard.py
* mouse.py
* stablediffusion.py
* UI.py
### utils/cvfpscalc.py
This is a module for FPS measurement.
