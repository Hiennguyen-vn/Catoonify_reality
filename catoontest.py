import gradio as gr
import cv2
import numpy as np
from collections import defaultdict
from scipy import stats

def update_c(C, hist):
    while True:
        groups = defaultdict(list)
        for i in range(len(hist)):
            if hist[i] == 0:
                continue
            d = np.abs(C - i)
            index = np.argmin(d)
            groups[index].append(i)
        new_C = np.array(C)
        for i, indice in groups.items():
            if np.sum(hist[indice]) == 0:
                continue
            new_C[i] = int(np.sum(indice * hist[indice]) / np.sum(hist[indice]))
        if np.sum(new_C - C) == 0:
            break
        C = new_C
    return C, groups

def K_histogram(hist):
    alpha = 0.001
    N = 80
    C = np.array([128])
    while True:
        C, groups = update_c(C, hist)
        new_C = set()
        for i, indice in groups.items():
            if len(indice) < N:
                new_C.add(C[i])
                continue
            z, pval = stats.normaltest(hist[indice])
            if pval < alpha:
                left = 0 if i == 0 else C[i - 1]
                right = len(hist) - 1 if i == len(C) - 1 else C[i + 1]
                if right - left >= 3:
                    new_C.add((C[i] + left) / 2)
                    new_C.add((C[i] + right) / 2)
                else:
                    new_C.add(C[i])
            else:
                new_C.add(C[i])
        if len(new_C) == len(C):
            break
        C = np.array(sorted(new_C))
    return C

def apply_style(image, style):
    if style == "vintage":
        # Áp bộ lọc màu vintage nhẹ
        vintage = np.array([[0.9, 0.6, 0.3]])
        image = cv2.multiply(image.astype(np.float32), vintage).clip(0, 255).astype(np.uint8)
        image = cv2.GaussianBlur(image, (3, 3), 0)
    elif style == "watercolor":
        image = cv2.edgePreservingFilter(image, flags=1, sigma_s=60, sigma_r=0.5)
    elif style == "pencil":
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256.0)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
    return image

def cartoonizer(img, contour_thickness=2, style="classic"):
    img = cv2.resize(img, (512, 512)) if max(img.shape[:2]) > 512 else img
    kernel = np.ones((2, 2), np.uint8)
    smooth_img = np.zeros_like(img)
    for i in range(3):
        smooth_img[:, :, i] = cv2.bilateralFilter(img[:, :, i], 5, 150, 150)

    edge = cv2.Canny(smooth_img, 100, 200)
    hsv = cv2.cvtColor(smooth_img, cv2.COLOR_RGB2HSV)

    hists = [
        np.histogram(hsv[:, :, 0], bins=np.arange(181))[0],
        np.histogram(hsv[:, :, 1], bins=np.arange(257))[0],
        np.histogram(hsv[:, :, 2], bins=np.arange(257))[0]
    ]
    C = [K_histogram(h) for h in hists]

    x, y, c = hsv.shape
    flat = hsv.reshape((-1, c))
    for i in range(3):
        ch = flat[:, i]
        idx = np.argmin(np.abs(ch[:, np.newaxis] - C[i]), axis=1)
        flat[:, i] = C[i][idx]
    quantized = flat.reshape((x, y, c))
    output = cv2.cvtColor(quantized, cv2.COLOR_HSV2RGB)

    contours, _ = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(output, contours, -1, color=(0, 0, 0), thickness=contour_thickness)

    for i in range(3):
        output[:, :, i] = cv2.erode(output[:, :, i], kernel, iterations=1)

    # Áp dụng phong cách
    output = apply_style(output, style)
    return output

# Giao diện Gradio
gr.Interface(
    fn=cartoonizer,
    inputs=[
        gr.Image(type="numpy", label="📷 Ảnh đầu vào"),
        gr.Slider(1, 5, value=2, step=1, label="✏️ Độ dày nét viền"),
        gr.Radio(["classic", "vintage", "watercolor", "pencil"], label="🎨 Phong cách", value="classic")
    ],
    outputs=gr.Image(type="numpy", label="🖼️ Ảnh hoạt hình đầu ra"),
    title="✨ Cartoon Style Generator",
    description="Chuyển ảnh thành tranh hoạt hình với nhiều phong cách: cổ điển, màu nước, bút chì..."
).launch()
