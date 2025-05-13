# Cartoonizer - Chuyển Ảnh Thật Thành Tranh Hoạt Hình

Ứng dụng này giúp bạn chuyển ảnh thật thành tranh hoạt hình (cartoonize image) bằng cách sử dụng các kỹ thuật xử lý ảnh như **Bilateral Filter**, **Canny Edge Detection**, **Histogram-based Clustering**, và **Contours** để tạo ra hiệu ứng hoạt hình với các đường biên sắc nét và màu sắc đơn giản hơn.

## Mục Tiêu

- **Giảm số lượng màu** (Color Quantization) bằng cách phân cụm màu.
- **Tạo ảnh hoạt hình** bằng cách giữ lại các đường biên sắc nét.
- **Cải thiện màu sắc** và làm mịn ảnh bằng **Bilateral Filter**.
- **Vẽ đường biên** trên ảnh hoạt hình để tạo hiệu ứng tay vẽ.

## Các Thư Viện Cần Cài Đặt

Để chạy ứng dụng, bạn cần cài đặt các thư viện sau:

- **OpenCV**: Dùng để xử lý ảnh và phát hiện biên.
- **NumPy**: Dùng cho các phép toán số học.
- **SciPy**: Dùng để kiểm định phân phối chuẩn (normal test).
- **Gradio**: Dùng để xây dựng giao diện người dùng.

Bạn có thể cài đặt các thư viện này bằng cách sử dụng pip:

```bash
!pip install gradio opencv-python numpy scipy
