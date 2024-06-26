# Run the following in the cmd prompt
# python D:\Github_Desktop\Computer-Vision-Practice\Keras-networks\keras-networks\classify_image.py --image "D:\Github_Desktop\Computer-Vision-Practice\Keras-networks\keras-networks\images\soccer_ball.jpg" --model inception


import sys
from tensorflow.keras.applications import ResNet50, InceptionV3, Xception, VGG16, VGG19, imagenet_utils
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import argparse
import cv2

def main(args):
    # define a dictionary that maps model names to their classes inside Keras
    MODELS = {
        "vgg16": VGG16,
        "vgg19": VGG19,
        "inception": InceptionV3,
        "xception": Xception,  # TensorFlow ONLY
        "resnet": ResNet50
    }

    # esnure a valid model name was supplied via command line argument
    if args["model"] not in MODELS.keys():
        raise AssertionError("The --model command line argument should "
                             "be a key in the `MODELS` dictionary")

    # initialize the input image shape (224x224 pixels) along with
    # the pre-processing function (this might need to be changed
    # based on which model we use to classify our image)
    inputShape = (224, 224)
    preprocess = imagenet_utils.preprocess_input

    # if we are using the InceptionV3 or Xception networks, then we
    # need to set the input shape to (299x299) [rather than (224x224)]
    # and use a different image pre-processing function
    if args["model"] in ("inception", "xception"):
        inputShape = (299, 299)
        preprocess = preprocess_input

    print("[INFO] loading {}...".format(args["model"]))
    Network = MODELS[args["model"]]
    model = Network(weights="imagenet")

    print("[INFO] loading and pre-processing image...")
    image = load_img(args["image"], target_size=inputShape)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess(image)

    print("[INFO] classifying image with '{}'...".format(args["model"]))
    preds = model.predict(image)
    P = imagenet_utils.decode_predictions(preds)

    for (i, (imagenetID, label, prob)) in enumerate(P[0]):
        print("{}. {}: {:.2f}%".format(i + 1, label, prob * 100))

    orig = cv2.imread(args["image"])
    (imagenetID, label, prob) = P[0][0]
    cv2.putText(orig, "Label: {}, {:.2f}%".format(label, prob * 100),
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.imshow("Classification", orig)
    cv2.waitKey(0)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    ap.add_argument("-model", "--model", type=str, default="vgg16", help="name of pre-trained network to use")
    
    # Check if any arguments were passed; if not, print usage and exit with an error
    if len(sys.argv) <= 1:
        ap.print_help()
        sys.exit(1)
    
    args = vars(ap.parse_args())
    main(args)
