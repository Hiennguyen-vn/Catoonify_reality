import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def cartoon_handdrawn_effect(img, num_colors=8, use_contour=True):
    """
    Áp dụng hiệu ứng vẽ tay hoạt hình lên ảnh.
    """

    # Làm mịn ảnh nhưng vẫn giữ nét biên
    smooth = cv2.bilateralFilter(img, d=9, sigmaColor=200, sigmaSpace=200)

    # Giảm số lượng màu bằng KMeans
    z = smooth.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(z, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    simplified_img = centers[labels.flatten()].reshape(img.shape)

    # Tạo viền
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 7)

    if use_contour:
        # Viền đậm bằng contour
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        edge_mask = np.ones_like(gray) * 255
        cv2.drawContours(edge_mask, contours, -1, color=0, thickness=2)
        edges = edge_mask
    else:
        # Viền truyền thống
        edges = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=9,
            C=2
        )

    cartoon = cv2.bitwise_and(simplified_img, simplified_img, mask=edges)
    return cartoon


def resize_image(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)


def display_images(original, cartooned):
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    cartoon_rgb = cv2.cvtColor(cartooned, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(original_rgb)
    plt.title("Ảnh gốc")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(cartoon_rgb)
    plt.title("Ảnh hiệu ứng vẽ tay")
    plt.axis("off")

    plt.tight_layout()
    plt.show()


def main():
    image_path = input("Nhập đường dẫn đến ảnh: ").strip().strip('"')
    if not os.path.exists(image_path):
        print("❌ Lỗi: Không tìm thấy ảnh.")
        return

    use_contour_input = input("Dùng contour để tạo nét viền đậm? (y/n): ").strip().lower()
    use_contour = use_contour_input == 'y'

    try:
        scale_percent = int(input("Nhập phần trăm thu nhỏ ảnh (ví dụ 50): ").strip())
    except:
        scale_percent = 50

    try:
        num_colors = int(input("Nhập số lượng màu (ví dụ 8): ").strip())
    except:
        num_colors = 8

    output_path = "output_handdrawn.jpg"

    # Đọc ảnh
    img = cv2.imread(image_path)
    resized_img = resize_image(img, scale_percent)

    # Áp dụng hiệu ứng
    cartoon_img = cartoon_handdrawn_effect(resized_img, num_colors=num_colors, use_contour=use_contour)

    # Hiển thị và lưu ảnh
    display_images(resized_img, cartoon_img)
    cv2.imwrite(output_path, cartoon_img)
    print(f"✅ Ảnh đã được lưu tại: {output_path}")


if __name__ == "__main__":
    main()
