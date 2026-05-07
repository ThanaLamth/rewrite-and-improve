# Feedback Index Ảnh Cho Coincu

## URL đã kiểm tra

- `https://coincu.com/what-1-bitcoin-can-buy-in-2026-10-luxury-cars-compared/`

## Tóm tắt nhanh

Trang này không phải bị lỗi index ảnh hoàn toàn. Vấn đề chính là:

- ảnh cover chính của bài đang có tín hiệu khá ổn cho Google Image
- nhưng nhiều ảnh trong thân bài đang dùng lazy load theo kiểu placeholder
- vì vậy Google có thể crawl page nhưng discover/index ảnh trong body kém hơn

## Phát hiện chính

### 1. Ảnh chính của bài tương đối ổn

Ảnh chính đang có đủ nhiều tín hiệu hỗ trợ:

- có `og:image`
- có `twitter:image`
- có `ImageObject` trong schema
- có caption rõ
- có ảnh với `src` thật trong HTML

Ảnh chính quan sát được:

- `https://coincu.com/wp-content/uploads/2026/05/top-luxury-car-buy-bitcoin.png`

Đây là phần đang ổn hơn các ảnh còn lại trong bài.

### 2. Ảnh trong thân bài yếu hơn cho image indexing

Nhiều ảnh trong nội dung đang hiển thị theo kiểu:

```html
<img
  src="data:image/svg+xml,..."
  data-lazy-src="https://coincu.com/wp-content/uploads/2026/05/image-36-1024x782.png"
  data-lazy-srcset="..."
>
```

Tức là:

- `src` ban đầu chỉ là placeholder SVG
- ảnh thật bị đẩy sang `data-lazy-src`
- `srcset` thật cũng bị đẩy sang `data-lazy-srcset`

Điều này làm khả năng Google nhận diện ảnh thật trong HTML ban đầu kém hơn.

## Bằng chứng đã thấy

### Ảnh mạnh hơn

Ảnh hero gần đầu bài đang có `src` thật:

- `top-luxury-car-buy-bitcoin-1024x575.png`

### Ảnh yếu hơn

Các ảnh trong bài đang dùng lazy-load placeholder gồm:

- `bitcoin-luxury-cars-real-grid-capture.png`
- `image-36.png`
- `image-37.png`
- `image-38.png`
- `genesis-g90.png`

## Vì sao các ảnh này dễ khó index hơn

### 1. Lazy load kiểu placeholder

Với ảnh quan trọng trong bài, cách an toàn hơn là:

```html
<img src="real-image.jpg" loading="lazy">
```

Không nên dùng kiểu:

```html
<img src="placeholder" data-lazy-src="real-image.jpg">
```

Vì Google có thể nhìn thấy placeholder trước thay vì ảnh thật.

### 2. Tên file ảnh quá chung chung

Một số file đang tên như:

- `image-36.png`
- `image-37.png`
- `image-38.png`

Tên như vậy yếu về tín hiệu ngữ nghĩa.

Nên đổi thành tên rõ hơn, ví dụ:

- `bitcoin-luxury-cars-bmw-x5.png`
- `bitcoin-luxury-cars-mercedes-e450.png`
- `bitcoin-luxury-cars-volvo-ex90-threshold.png`

### 3. Ảnh dạng screenshot

Một số ảnh là screenshot từ trang hãng xe.

Những ảnh này thường kém mạnh hơn:

- infographic tự làm
- comparison chart tự dựng
- visual gốc của bài

### 4. Page có nhiều ảnh lazy-loaded khác

Ngoài ảnh trong thân bài, page còn có ảnh related posts và thumbnail khác cũng dùng lazy-load.

Điều này có thể làm tín hiệu nổi bật của ảnh chính trong bài bị loãng hơn.

## Việc nên làm

## Mức ưu tiên: Phải sửa trước

1. Với các ảnh quan trọng trong thân bài, đưa URL ảnh thật vào `src`.
2. Nếu vẫn muốn lazy load, dùng dạng an toàn hơn:

```html
<img src="real-image.jpg" loading="lazy">
```

3. Đổi tên file ảnh từ dạng generic sang dạng mô tả rõ nội dung.

## Mức ưu tiên: Nên cải thiện

1. Ưu tiên ảnh gốc hoặc infographic thay cho screenshot khi có thể.
2. Giữ `alt` mô tả rõ cho từng ảnh quan trọng.
3. Giữ `figcaption` rõ và bám sát nội dung ảnh.
4. Đặt ảnh gần đúng đoạn text liên quan nhất.

## Mức ưu tiên: Tối ưu thêm nếu có thời gian

1. Giảm số lượng ảnh không thật sự cần thiết trong bài.
2. Chỉ giữ 1 ảnh cover mạnh và 1-2 ảnh body quan trọng nhất.

## Ưu tiên sửa riêng cho bài này

Nên xử lý trước các ảnh sau:

1. `bitcoin-luxury-cars-real-grid-capture.png`
2. `image-36.png`
3. `image-37.png`
4. `image-38.png`
5. `genesis-g90.png`

Riêng ảnh cover:

- `top-luxury-car-buy-bitcoin.png`

đang ở trạng thái tốt hơn phần còn lại của bài.

## Kết luận

Vấn đề ở đây không phải là bài không có cơ hội index ảnh. Vấn đề chính là:

- ảnh cover chính đang được expose khá rõ
- nhưng nhiều ảnh trong thân bài đang bị ẩn sau lazy-load placeholder

Nếu Coincu muốn cải thiện image indexing, ưu tiên lớn nhất là:

- cho ảnh thật vào `src`
- dùng lazy load theo chuẩn an toàn hơn
- đổi tên file ảnh rõ nghĩa
- tăng tỷ lệ ảnh gốc / visual tự làm thay vì screenshot
