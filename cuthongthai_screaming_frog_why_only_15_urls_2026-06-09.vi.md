# Vì Sao Screaming Frog Chỉ Crawl Được 15 URL Ở Cuthongthai.vn

Ngày soạn: 2026-06-09  
Case: crawl `https://cuthongthai.vn/` nhưng kết quả chỉ ra khoảng `15 URL`

## Kết Luận Nhanh

Con số `15 URL` trong case này gần như chắc chắn **không phải 15 trang nội dung thật**.

Nó nhiều khả năng chỉ là:

- `1` URL HTML của homepage
- phần còn lại là file `JavaScript` và `CSS` của Next.js

Nói cách khác, Screaming Frog đang đếm cả asset tĩnh, trong khi chưa crawl đủ các trang HTML và chưa đi sang các subdomain chính.

## Dấu Hiệu Nhìn Thấy Ngay Từ Dữ Liệu

Trong danh sách URL bạn gửi:

- URL đầu tiên là homepage: `https://cuthongthai.vn/`
- các URL còn lại chủ yếu là:
  - `/_next/static/chunks/...js`
  - `/_next/static/css/...css`

Đây là asset render của website Next.js, không phải landing page SEO.

Vì vậy, nếu Screaming Frog báo tổng cộng rất ít URL trong tình huống này, thì nguyên nhân gần như không phải là site nhỏ, mà là **cấu hình crawl chưa đúng cho mục tiêu SEO architecture**.

## Nguyên Nhân Nhiều Khả Năng Nhất

### 1. Chưa crawl sang các subdomain

Nếu chưa bật `Crawl All Subdomains`, Screaming Frog sẽ không đi sang:

- `vimo.cuthongthai.vn`
- `thue.cuthongthai.vn`
- `tamlinh.cuthongthai.vn`
- `muanha.cuthongthai.vn`
- `suckhoe.cuthongthai.vn`

Trong khi đây mới là phần lớn hệ site mà bạn đang cần phân tích.

### 2. Crawl asset thay vì tập trung vào HTML

Nếu để cấu hình crawl cả:

- JavaScript
- CSS
- images

thì với site dùng Next.js, danh sách sẽ rất nhanh bị lấp bởi asset như `/_next/static/...`

Kết quả là:

- số URL nhìn thì có vẻ tăng
- nhưng insight SEO thật thì rất ít

### 3. Có thể đang bật giới hạn crawl

Nếu bạn lỡ bật:

- `Max URI`
- `Max Crawl Depth`

thì Screaming Frog có thể dừng rất sớm, trước khi chạm tới các hub page hoặc subdomain khác.

### 4. Có thể đang dùng `Text Only` trong khi site cần render để lộ thêm link

Với `cuthongthai.vn`, điều này không phải nguyên nhân duy nhất, nhưng vẫn có thể góp phần làm thiếu URL nếu menu hoặc card links được render bằng JavaScript.

## Cách Đọc Đúng Dữ Liệu Hiện Tại

Đừng nhìn tổng toàn bộ URL lẫn asset.

Hãy vào:

- `Internal`

rồi lọc:

- `HTML`

Nếu sau khi lọc `HTML` mà vẫn chỉ có `1` hoặc rất ít URL, thì đó là lúc kết luận crawl đang thiếu dữ liệu thật.

## Cấu Hình Nên Chạy Lại

### Vòng 1: Crawl kiến trúc tổng thể

Thiết lập nên dùng:

- `Mode`: `Spider`
- `Start URL`: `https://cuthongthai.vn/`
- `Rendering`: `Text Only`
- bật `Crawl All Subdomains`
- tắt tạm crawl asset không cần thiết

Tạm thời nên tắt:

- `Check Images`
- `Check CSS`
- `Check JavaScript`

Mục tiêu:

- lấy page HTML trước
- xem cấu trúc site
- xem internal links
- xem canonical, directives, redirect

### Vòng 2: Crawl JavaScript có chọn lọc

Sau khi có bức tranh tổng, mới chạy lại từng subdomain chính ở chế độ:

- `Rendering`: `JavaScript`

Ưu tiên:

- `vimo.cuthongthai.vn`
- `thue.cuthongthai.vn`
- `tamlinh.cuthongthai.vn`
- `muanha.cuthongthai.vn`

## 4 Chỗ Cần Kiểm Tra Ngay Trong Screaming Frog

### 1. `Config > Spider > Crawl`

Nên:

- bật crawl HTML
- tắt tạm asset crawl không cần thiết ở vòng đầu

### 2. `Config > Spider` phần subdomain

Nên:

- bật `Crawl All Subdomains`

### 3. `Config > Limits`

Kiểm tra xem có đang giới hạn:

- `Max URI`
- `Max Crawl Depth`

Nếu có, nên bỏ giới hạn hoặc đặt về mức đủ lớn.

### 4. `Rendering`

Nên:

- dùng `Text Only` trước
- nếu HTML vẫn quá ít, chạy thêm `JavaScript`

## Kỳ Vọng Sau Khi Sửa Cấu Hình

Nếu cấu hình đúng, bạn sẽ không còn chỉ thấy khoảng `15 URL`.

Bạn sẽ thấy:

- domain gốc
- các subdomain chính
- blog pages
- tool pages
- hub pages
- thư viện nội dung như `văn khấn`, `thuế`, `mua nhà`, `vĩ mô`

## Kết Luận Thực Dụng

Với output bạn gửi, vấn đề không nằm ở chỗ site chỉ có ít trang.

Vấn đề nằm ở chỗ:

- Screaming Frog đang crawl asset
- chưa lấy đủ HTML pages
- và nhiều khả năng chưa đi qua các subdomain cần thiết

Cho nên con số `15` hiện tại chưa có giá trị để đánh giá kiến trúc SEO của `cuthongthai.vn`.

Nó chỉ cho thấy bạn cần chỉnh lại cấu hình crawl.
