import cv2
import mediapipe as mp
import math

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

def distance(p1, p2, image):
    h, w, _ = image.shape
    x1, y1, z1 = p1.x * w, p1.y * h, p1.z
    x2, y2, z2 = p2.x * w, p2.y * h, p2.z
    return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

def finger_states(hand_landmarks, image):
    lm = hand_landmarks.landmark
    wrist = lm[0]
    fingers = []

    # Thumb
    thumb_tip, thumb_mcp = lm[4], lm[2]
    fingers.append(1 if distance(wrist, thumb_tip, image) > distance(wrist, thumb_mcp, image) else 0)

    # Other 4 fingers
    for tip, mcp in zip([8,12,16,20], [5,9,13,17]):
        fingers.append(1 if distance(wrist, lm[tip], image) > distance(wrist, lm[mcp], image) else 0)

    return fingers

def classify_gesture(fingers, hand_landmarks, image):
    lm = hand_landmarks.landmark
    h, w, _ = image.shape
    def get_xy(id): return int(lm[id].x * w), int(lm[id].y * h)

    # --- Thumbs Up (PRIORITY) ---
    if fingers[0] == 1:  # thumb up
        wrist_y = lm[0].y * h
        thumb_tip_y = lm[4].y * h
        if thumb_tip_y < wrist_y - 40:
            palm_center = ((lm[0].x+lm[5].x+lm[17].x)/3, (lm[0].y+lm[5].y+lm[17].y)/3)
            palm_px = (int(palm_center[0]*w), int(palm_center[1]*h))
            close = True
            for t in [8,12,16,20]:
                if math.dist(get_xy(t), palm_px) > 100:
                    close = False
            if close:
                return "Thumbs Up"

    # --- OK Sign (PRIORITY) ---
    thumb_tip, index_tip = get_xy(4), get_xy(8)
    if math.dist(thumb_tip, index_tip) < 70:  # more lenient
        # At least 2 of [middle, ring, pinky] extended
        if sum(fingers[2:]) >= 2:
            return "OK Sign"

      # --- Fist ---
    # Check 4 fingers (ignore thumb)
    if not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
        palm_center = ((lm[0].x+lm[5].x+lm[17].x)/3,
                        (lm[0].y+lm[5].y+lm[17].y)/3)
        palm_px = (int(palm_center[0]*w), int(palm_center[1]*h))
        tips = [8,12,16,20]  # index, middle, ring, pinky
        close = True
        for t in tips:
            if math.dist(get_xy(t), palm_px) > 100:
                close = False
        if close:
            return "Fist"


    # --- Peace ---
    if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
        if math.dist(get_xy(8), get_xy(12)) > 40:
            return "Peace"

    # --- Rock ---
    if fingers[1] and fingers[4] and not fingers[2] and not fingers[3]:
        return "Rock Sign"

    # --- Open Palm (last, stricter) ---
    if fingers == [1,1,1,1,1]:
        # Require palm flat (z-coords close together)
        depths = [lm[i].z for i in [0,5,9,13,17]]
        if max(depths) - min(depths) < 0.15:
            return "Open Palm"

    return "Unknown"

# Main loop
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                              results.multi_handedness):
            fingers = finger_states(hand_landmarks, frame)
            gesture = classify_gesture(fingers, hand_landmarks, frame)

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
