import cv2
import numpy as np
from collections import defaultdict
from scipy import stats
import gradio as gr


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
    alpha = 0.001  # Đặt rất nhỏ, để chỉ khi nào rất rõ ràng là "không chuẩn" mới chia cụm
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
                delta = right - left
                if delta >= 3:
                    c1 = (C[i] + left) / 2
                    c2 = (C[i] + right) / 2
                    new_C.add(c1)
                    new_C.add(c2)
                else:
                    new_C.add(C[i])
            else:
                new_C.add(C[i])

        if len(new_C) == len(C):
            break
        else:
            C = np.array(sorted(new_C))
    return C


def caart(img, bilateral_d=5, bilateral_sigmaColor=150, bilateral_sigmaSpace=150,
          canny_thresh1=100, canny_thresh2=200, erosion_iter=1):
    kernel = np.ones((2, 2), np.uint8)
    output = np.array(img)
    x, y, c = output.shape

    for i in range(c):
        output[:, :, i] = cv2.bilateralFilter(output[:, :, i], bilateral_d, bilateral_sigmaColor, bilateral_sigmaSpace)

    edge = cv2.Canny(output, canny_thresh1, canny_thresh2)
    output = cv2.cvtColor(output, cv2.COLOR_RGB2HSV)

    hists = []
    for i in range(c):
        bins = np.arange(180 + 1) if i == 0 else np.arange(256 + 1)
        hist, _ = np.histogram(output[:, :, i], bins=bins)
        hists.append(hist)

    C = [K_histogram(h) for h in hists]

    output = output.reshape((-1, c))
    for i in range(c):
        channel = output[:, i]
        index = np.argmin(np.abs(channel[:, np.newaxis] - C[i]), axis=1)
        output[:, i] = C[i][index]
    output = output.reshape((x, y, c))
    output = cv2.cvtColor(output, cv2.COLOR_HSV2RGB)

    contours, _ = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(output, contours, -1, 0, thickness=1)

    for i in range(3):
        output[:, :, i] = cv2.erode(output[:, :, i], kernel, iterations=erosion_iter)

    return output


def process(img, bilateral_d, bilateral_sigmaColor, bilateral_sigmaSpace, canny_thresh1, canny_thresh2, erosion_iter):
    cartoon = caart(img, bilateral_d, bilateral_sigmaColor, bilateral_sigmaSpace,
                    canny_thresh1, canny_thresh2, erosion_iter)
    return cartoon


iface = gr.Interface(
    fn=process,
    inputs=[
        gr.Image(type="numpy", label="Ảnh gốc"),
        gr.Slider(1, 15, step=1, value=5, label="Bilateral Diameter"),
        gr.Slider(50, 250, step=10, value=150, label="Sigma Color"),
        gr.Slider(50, 250, step=10, value=150, label="Sigma Space"),
        gr.Slider(50, 200, step=10, value=100, label="Ngưỡng Canny thấp"),
        gr.Slider(100, 300, step=10, value=200, label="Ngưỡng Canny cao"),
        gr.Slider(0, 5, step=1, value=1, label="Số lần Erode"),
    ],
    outputs=gr.Image(type="numpy", label="Ảnh hoạt hình"),
    title="🎨 Cartoonizer App",
    description="Chuyển ảnh thật thành tranh hoạt hình bằng phân cụm màu và viền nét tay.",
)

iface.launch()
