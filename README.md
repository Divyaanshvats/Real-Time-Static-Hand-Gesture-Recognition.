# **Real-Time-Static-Hand-Gesture-Recognition**.
##**Author: DIVYAANSH VATS**


**##📖 Overview**

This project is a real-time static hand gesture recognition system built using Python, OpenCV, and Mediapipe.
The webcam captures live video, and Mediapipe detects 21 landmarks (key points) on the hand.
By analyzing the positions and distances of these landmarks, the system classifies the hand into one of six static gestures:

🖐️ Open Palm

👊 Fist

✌️ Peace Sign (V-sign)

👍 Thumbs Up

👌 OK Sign

🤘 Rock Sign

⚙️ Technology Justification

OpenCV

Enables real-time webcam access and image processing.

Simple, lightweight, and widely used for computer vision tasks.

Mediapipe (by Google)

Provides a pre-trained model that tracks 21 landmarks per hand in real time.

Very accurate, works across lighting/background variations.

Eliminates the need for training a custom hand detector, making the project efficient and reliable.

NumPy

Used for numerical calculations (like distances between points).

Makes geometry-based classification fast and efficient.

These frameworks are the best choice for this project as they provide real-time speed, accuracy, and ease of use without requiring complex deep learning training pipelines.

✋ Gesture Logic Explanation

The gestures are recognized by applying rule-based checks on landmark positions:

Open Palm 🖐️

All five fingers are extended (all landmarks farther from the wrist than their base joints).

Palm surface is flat (z-coordinates of palm points are close together).

Fist 👊

All four non-thumb fingers are curled close to the palm center.

Thumb may be tucked inside or folded across fingers.

Fingertips are within a short distance of the palm center.

Peace Sign ✌️

Index and Middle fingers extended.

Ring and Pinky folded.

Index and Middle are separated by a visible gap, forming a “V” shape.

Thumbs Up 👍

Thumb extended upward, above wrist level.

All other four fingers folded near the palm center.

Works even when the hand is rotated.

OK Sign 👌

Thumb tip and Index tip touch (circle formation).

At least two of the other fingers (Middle, Ring, Pinky) are extended.

Rock Sign 🤘

Index and Pinky fingers extended.

Middle and Ring fingers folded.

Thumb position can vary.

If none of these conditions are met, the gesture is labeled Unknown.

🛠️ Setup and Execution Instructions
1. Clone or Download the Project
git clone <your-repo-link>
cd <your-project-folder>

2. Create a Virtual Environment

On Windows:

python -m venv venv
venv\Scripts\activate


On Mac/Linux:

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

Install all required libraries from requirements.txt:

pip install -r requirements.txt

4. Run the Application

Start the gesture recognition system:

python gesture_recog.py


A webcam window will open. Show one of the six gestures in front of your camera.
The system will classify and display the gesture name in real time.

5. Exit

To exit the program, press q in the webcam window.

🎥 Demo

A demo video of the system in action has been provided in the repository as a demo file.

To download and view it:

Go to the demo file in the repository.

Click on it, then click Raw.

The file (zipped video) will automatically download to your system.

Extract and play the video to see live examples of each gesture.

✅ This system successfully recognizes all six gestures in real time using a simple, explainable, and efficient rule-based approach.
