import cv2 as cv
import numpy as np

import mediapipe as mp

class Detector:
    def __init__(self,
                 static_mode=False,
                 number_of_hands=1,
                 complexity=1,
                 detection_confidence=0.5,
                 tracking_confidence=0.5,
                 ):

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.model = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=number_of_hands,
            model_complexity=complexity,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

    def detect(self,
               image: np.ndarray,
               draw: dict,
               padding: int,
               output_size: int,
               output_shape: str,
               flip: bool,
               landmarks_on_blank: bool,
               ) -> tuple[np.ndarray, list[np.ndarray]]:

        mp_results = self.model.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
        h, w, _ = image.shape
        hands = []
        blank_image = np.zeros_like(image)

        if mp_results.multi_hand_landmarks:
            for hand_type, hand_landmarks in zip(mp_results.multi_handedness, mp_results.multi_hand_landmarks):
                hand = {}
                landmarks = []
                x_list, y_list = [], []

                for lm in hand_landmarks.landmark:
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    landmarks.append([px, py, pz])
                    x_list.append(px)
                    y_list.append(py)

                xmin, xmax = min(x_list), max(x_list)
                ymin, ymax = min(y_list), max(y_list)
                bounding_box = (xmin, ymin, xmax - xmin, ymax - ymin)

                hand['landmarks'] = landmarks
                hand['bounding_box'] = bounding_box
                hand['center'] = (bounding_box[0] + bounding_box[2] // 2, bounding_box[1] + bounding_box[3] // 2)
                hand['type'] = Detector._determine_type(hand_type, flip)

                hands.append(hand)

                if draw['draw_landmarks']:
                    self.mp_draw.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=self.mp_draw.DrawingSpec(color=draw['landmarks_color'], thickness=draw['landmarks_thickness']),
                        connection_drawing_spec=self.mp_draw.DrawingSpec(color=draw['connections_color'], thickness=draw['connections_thickness'])
                    )

                if draw['draw_bounding_box']:
                    cv.rectangle(
                        image,
                        (bounding_box[0] - draw['padding'], 
                        bounding_box[1] - draw['padding']),
                        (bounding_box[0] + bounding_box[2] + draw['padding'], 
                        bounding_box[1] + bounding_box[3] + draw['padding']),
                        draw['bounding_box_color'],
                        draw['bounding_box_thickness']
                    )

                if landmarks_on_blank:
                    self.mp_draw.draw_landmarks(
                        blank_image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=self.mp_draw.DrawingSpec(color=draw['landmarks_color'], thickness=draw['landmarks_thickness']),
                        connection_drawing_spec=self.mp_draw.DrawingSpec(color=draw['connections_color'], thickness=draw['connections_thickness'])
                    )

        reshape = {'Square': Detector._square, 'Border': Detector._border, 'None': Detector._resize}.get(output_shape)
        source = image if not landmarks_on_blank else blank_image
        hands = [reshape(source, hand, output_size, padding) for hand in hands]

        return cv.cvtColor(image, cv.COLOR_BGR2RGB), [cv.cvtColor(hand, cv.COLOR_BGR2RGB) for hand in hands]

    @staticmethod
    def _determine_type(hand_type, flip=True):
        return {
            True: {
                'Right': 'Left',
                'Left' : 'Right'
            },
            False: {
                'Right': 'Right',
                'Left' : 'Left'
            }
        }[flip].get(hand_type.classification[0].label, 'Unknown')

    @staticmethod
    def _square(image, hand, size, pad):
        x, y, w, h = hand['bounding_box']

        x_start, x_end, y_start, y_end = x, x + w, y, y + h
        if h > w:
            pad_l = (h - w) // 2
            pad_r = (h - w) - pad_l
            x_start = max(0, x - pad_l - pad)
            x_end = min(image.shape[1], x + w + pad_r + pad)
            y_start = max(0, y - pad)
            y_end = min(image.shape[0], y + h + pad)
        elif w > h:
            pad_u = (w - h) // 2
            pad_d = (w - h) - pad_u
            x_start = max(0, x - pad)
            x_end = min(image.shape[1], x + w + pad)
            y_start = max(0, y - pad_u - pad)
            y_end = min(image.shape[0], y + h + pad_d + pad)
        else:
            x_start = max(0, x - pad)
            x_end = min(image.shape[1], x + w + pad)
            y_start = max(0, y - pad)
            y_end = min(image.shape[0], y + h + pad)

        return cv.resize(image[y_start:y_end, x_start:x_end], (size, size))

    @staticmethod
    def _border(image, hand, size, pad):
        x, y, w, h = hand['bounding_box']
        
        y_start = max(0, y - pad)
        y_end = min(image.shape[0], y + h + pad)
        x_start = max(0, x - pad)
        x_end = min(image.shape[1], x + w + pad)
        
        if h > w:
            pad_l = (h - w) // 2
            pad_r = (h - w) - pad_l
            top, bottom = pad, pad
            left, right = pad_l + pad, pad_r + pad
        elif w > h:
            pad_u = (w - h) // 2
            pad_d = (w - h) - pad_u
            top, bottom = pad_u + pad, pad_d + pad
            left, right = pad, pad
        else:
            top, bottom = pad, pad
            left, right = pad, pad
        
        image = cv.copyMakeBorder(image[y_start:y_end, x_start:x_end],
                                  top=top, bottom=bottom, left=left, right=right,
                                  borderType=cv.BORDER_CONSTANT, value=[0, 0, 0]
                                  )
        return cv.resize(image, (size, size))
 
    @staticmethod
    def _resize(image, hand, size, pad):
        x, y, w, h = hand['bounding_box']
        x_start, y_start = max(0, x - pad), max(0, y - pad)
        x_end, y_end = min(image.shape[1], x + w + pad), min(image.shape[0], y + h + pad)
        scale = (x_end - x_start) / (y_end - y_start)
        if (x_end - x_start) > (y_end - y_start):
            image_w = size
            image_h = int(size / scale)
        else:
            image_h = size
            image_w = int(size * scale)
        return cv.resize(image[y_start:y_end, x_start:x_end], (image_w, image_h))

    #! ----- PreProcessing ----- ----- ----- -----

    @staticmethod
    def preprocess_image(image: np.ndarray, index: int=0, is_blank: bool=False) -> np.ndarray:
        return Detector._0_preprocess(image) if is_blank else [Detector._0_preprocess,
                                                               Detector._1_preprocess,
                                                               Detector._2_preprocess,
                                                               Detector._3_preprocess] [index] (image)

    @staticmethod #ToDo: No PreProcessing
    def _0_preprocess(image: np.ndarray) -> np.ndarray:
        return cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    @staticmethod #ToDo: FG Focus
    def _1_preprocess(image: np.ndarray) -> np.ndarray:
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (5, 5), 0)
        mask = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
        enhanced = cv.addWeighted(gray, 1.5, blur, -0.5, 0)
        return cv.add(cv.bitwise_and(enhanced, enhanced, mask=mask),
                    cv.bitwise_and(blur, blur, mask=cv.bitwise_not(mask))
                )

    @staticmethod #ToDo: UnImplemented Function
    def _2_preprocess(image: np.ndarray) -> np.ndarray:
        ...
        return cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    @staticmethod #ToDo: Sobel Edge Detection
    def _3_preprocess(image: np.ndarray) -> np.ndarray:
        image = cv.medianBlur(cv.cvtColor(image, cv.COLOR_RGB2GRAY), ksize=3)
        return cv.GaussianBlur(
                    cv.filter2D(
                        cv.magnitude(
                            cv.Sobel(image, cv.CV_64F, 1, 0, ksize=3),
                            cv.Sobel(image, cv.CV_64F, 0, 1, ksize=3)
                        ).astype(np.uint8),
                        -1, np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]])
                    ),
                (5, 5), 0)