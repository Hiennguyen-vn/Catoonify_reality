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

Cơ Sở Lý Thuyết
1. Làm Mịn Ảnh (Image Smoothing)
1.1 Bộ lọc tích chập 2D (2D Convolution)

Bộ lọc truyền dẫn thấp (Low-Pass Filter - LPF) giúp làm mịn ảnh và loại bỏ nhiễu.

Bộ lọc truyền dẫn cao (High-Pass Filter - HPF) dùng để phát hiện các cạnh trong ảnh.

OpenCV cung cấp hàm cv2.filter2D() để thực hiện tích chập 2D với các bộ lọc khác nhau trên ảnh.

1.2 Làm Mờ Ảnh (Image Blurring)

Làm mờ ảnh giúp loại bỏ nhiễu và làm sắc nét các vùng có độ tương phản cao.

OpenCV hỗ trợ nhiều phương pháp làm mờ như Trung Bình (Average Blur), Bộ lọc Gaussian (Gaussian Blur), và Bộ lọc Bilateral (Bilateral Filter).

Bilateral Filter là bộ lọc được sử dụng trong dự án này vì nó làm mờ vùng màu mà không làm mất đi các chi tiết biên sắc nét.

2. Phát Hiện Cạnh (Edge Detection)
Canny Edge Detection là một phương pháp phát hiện cạnh phổ biến, giúp xác định các biên trong ảnh.

Các bước chính của phương pháp này gồm:

Giảm nhiễu ảnh bằng bộ lọc Gaussian.

Tính gradient của ảnh để xác định các cạnh.

Triệt tiêu phi tối đa (Non-Maximum Suppression) để loại bỏ các pixel không phải là cực đại cục bộ.

Ngưỡng độ trễ (Hysteresis Thresholding) để quyết định các biên thực sự và bỏ qua nhiễu.

3. Contours
Contours là những đường bao quanh các vùng có biên trong ảnh. Chúng được sử dụng để phân tích hình dạng và phát hiện đối tượng trong ảnh.

Tính toán Moment: Các moments giúp tính toán các đặc trưng của contour như diện tích và tâm của vật thể.

Bounding Box: Là khung bao quanh vật thể, có thể có nhiều hình dạng khác nhau (chữ nhật, tam giác, tròn).

4. Histogram-based Clustering
Mục tiêu của phân cụm màu là giảm số lượng màu (color quantization) bằng cách sử dụng histogram của từng kênh màu trong ảnh.

Quá trình phân cụm màu sử dụng các K-means clustering để nhóm các màu sắc tương tự lại với nhau.

Histogram là biểu đồ thể hiện số lần xuất hiện của các giá trị màu sắc (độ sáng/màu) trong ảnh.

5. K-means Clustering
K-means là một thuật toán phân cụm phổ biến, giúp nhóm các điểm dữ liệu thành K cụm dựa trên sự tương đồng giữa các điểm. Trong trường hợp phân cụm màu, mỗi màu được phân loại vào một cụm và mỗi cụm có một trung tâm cụm đại diện cho màu sắc chung của các pixel trong cụm đó.

Các bước cơ bản của thuật toán K-means:
Khởi tạo các trung tâm cụm: Chọn K trung tâm cụm ngẫu nhiên.

Gán điểm dữ liệu vào cụm gần nhất: Mỗi pixel trong ảnh được gán vào cụm có trung tâm gần nhất.

Cập nhật các trung tâm cụm: Trung tâm của mỗi cụm được cập nhật bằng trung bình của tất cả các điểm trong cụm.

Lặp lại quá trình cho đến khi trung tâm không thay đổi hoặc thay đổi rất ít.

Thuật toán K-means được sử dụng trong dự án này để giảm số lượng màu trong ảnh, giúp ảnh trông đơn giản và dễ nhìn hơn.
```bash
!pip install gradio opencv-python numpy scipy



