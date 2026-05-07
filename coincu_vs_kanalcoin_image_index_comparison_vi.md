# So Sánh Coincu vs Kanalcoin Về Image Index

## Mục tiêu

Tài liệu này dùng để so sánh hai site ở đúng phần liên quan đến image indexing:

- robots / meta robots
- sitemap ảnh
- cách render ảnh trên homepage
- cách render ảnh trên article page

Mục tiêu là xác định Coincu đang gặp vấn đề kiểu:

- bị chặn index ảnh
- hay không bị chặn nhưng render ảnh kém tối ưu hơn

## Kết luận nhanh

Coincu không có dấu hiệu chặn image index một cách rõ ràng. Vấn đề chính nằm ở cách render ảnh.

So với Kanalcoin:

- `Kanalcoin` sạch hơn về mặt HTML render ảnh
- `Coincu` dùng lazy-load placeholder nặng hơn rất nhiều
- vì vậy Coincu dễ rơi vào tình trạng:
  - page vẫn index
  - nhưng ảnh không được Google discover/index mạnh

## 1. Robots / Meta Robots

### Coincu

Meta robots quan sát được:

```html
<meta name="robots" content="follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large"/>
```

### Kanalcoin

Meta robots quan sát được:

```html
<meta name="robots" content="follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large"/>
```

### Nhận xét

Hai site đều đang:

- cho phép index
- không có `noimageindex`
- không có `noindex`
- cho phép `max-image-preview:large`

=> Không phải khác biệt nằm ở meta robots.

## 2. robots.txt

### Coincu

Không chặn thư mục ảnh uploads.

### Kanalcoin

Không chặn thư mục ảnh uploads.

### Nhận xét

Không thấy site nào chặn `/wp-content/uploads/`.

=> Không phải khác biệt nằm ở robots.txt.

## 3. Sitemap ảnh

### Coincu

Coincu không có `image-sitemap.xml` riêng, nhưng ảnh được nhúng trong:

- `post-sitemap.xml`
- `page-sitemap.xml`

với namespace:

- `xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"`

### Kanalcoin

`sitemap_index.xml` hoạt động bình thường. Một số endpoint sitemap cụ thể khi check trực tiếp trả nội dung maintenance, nên chưa dùng được để so sâu phần image entry.

### Nhận xét

Coincu không thiếu image sitemap.

=> Không phải khác biệt chính nằm ở sitemap.

## 4. Homepage Image Render

### Coincu homepage

Kết quả quan sát:

- `img count`: `185`
- `data-lazy-src`: `269`
- `loading="lazy"`: `3`

### Kanalcoin homepage

Kết quả quan sát:

- `img count`: `45`
- `data-lazy-src`: `0`
- `data-src`: `2`
- `loading="lazy"`: `3`

### Nhận xét

Homepage Coincu dùng lazy-load placeholder rất nặng.

Homepage Kanalcoin nhẹ hơn rõ rệt và ít phụ thuộc vào kiểu:

- `src` placeholder
- ảnh thật nằm trong `data-lazy-src`

=> Ở homepage, Kanalcoin thân thiện với image discovery hơn Coincu.

## 5. Article Page Comparison

### Coincu article checked

- `https://coincu.com/what-1-bitcoin-can-buy-in-2026-10-luxury-cars-compared/`

Kết quả:

- tổng số upload images quan sát được: `104`
- `real-src`: `23`
- `lazy-placeholder`: `81`

Nghĩa là phần lớn ảnh đang có pattern:

```html
<img src="data:image/svg+xml,..." data-lazy-src="real-image-url">
```

### Kanalcoin article checked

- `https://www.kanalcoin.com/cryptocurrency-exchange-indonesia/`

Kết quả:

- tổng số upload images quan sát được: `11`
- `real-src`: `11`
- `lazy-placeholder`: `0`

Ảnh của Kanalcoin đang dùng pattern tốt hơn:

```html
<img src="real-image-url" loading="lazy">
```

### Nhận xét

Đây là khác biệt lớn nhất giữa hai site.

Coincu:

- quá nhiều ảnh bị ẩn sau placeholder
- ảnh thật không lộ ngay trong `src`

Kanalcoin:

- ảnh thật có ngay trong `src`
- vẫn lazy load được bằng `loading="lazy"`

=> Ở article page, Kanalcoin thân thiện với image indexing hơn Coincu rõ rệt.

## 6. Featured Image

### Coincu

Featured image của bài test:

- có `og:image`
- có `twitter:image`
- có schema `ImageObject`
- có `primaryImageOfPage`
- có một ảnh dùng `src` thật trong HTML

=> Featured image riêng lẻ không có dấu hiệu bị chặn.

### Kanalcoin

og:image và ảnh trong page cũng hiển thị theo kiểu trực tiếp hơn.

### Nhận xét

Coincu có thể vẫn để featured image hoạt động tương đối ổn, nhưng body images yếu hơn nhiều.

## Kết luận phân loại vấn đề của Coincu

Coincu hiện nghiêng mạnh về case:

- `không bị chặn image index`
- `nhưng render ảnh chưa tối ưu cho discovery/index`

Nói cách khác:

- page có thể index bình thường
- featured image có thể có cơ hội index
- nhưng nhiều body images dễ không được Google ưu tiên index

## Fix ưu tiên rút ra từ so sánh này

Nếu muốn Coincu tiến gần hơn mức “sạch” của Kanalcoin, ưu tiên lớn nhất là:

1. Giữ URL ảnh thật ngay trong `src`
2. Nếu cần lazy load, dùng:

```html
<img src="real-image.jpg" loading="lazy">
```

3. Hạn chế kiểu:

```html
<img src="placeholder" data-lazy-src="real-image.jpg">
```

đặc biệt với:

- featured image
- hero image
- các ảnh body quan trọng

## Kết luận cuối cùng

Nếu chỉ nhìn theo góc image index technical:

- `Kanalcoin` đang thân thiện hơn với Google Image discovery
- `Coincu` không bị chặn, nhưng render ảnh kém tối ưu hơn

Vì vậy Coincu hiện nhiều khả năng nằm ở nhóm:

- `page index được`
- `image không được Google chọn index mạnh`

chứ không phải nhóm:

- `bị robots/meta/header chặn image index`
