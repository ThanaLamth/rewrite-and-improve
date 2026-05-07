# Coincu vs Coindesk: So Sánh Cách Xử Lý Ảnh Và Việc Cần Làm

## Kết luận nhanh

Khác biệt chính giữa Coincu và Coindesk không nằm ở việc có sitemap ảnh hay không, mà nằm ở cách HTML trả ảnh ra cho Google.

- **Coindesk**: Google nhìn thấy ảnh thật ngay trong `src` và `srcset`
- **Coincu**: nhiều ảnh trong body đang để placeholder trong `src`, còn ảnh thật nằm ở `data-lazy-src`

Điều đó khiến ảnh của Coincu yếu hơn về mặt discoverability và image indexing.

## Coindesk đang làm như nào

Đối chiếu trực tiếp từ bài:

- `https://www.coindesk.com/markets/2026/05/07/dogecoin-slides-4-bitcoin-rally-pauses-as-iran-ceasefire-optimism-lifts-equities`

### Điểm chính

1. `src` là ảnh thật
2. `srcset` là ảnh thật
3. ảnh hero được `preload`
4. có `width`, `height`, `sizes`, `alt`
5. ảnh phụ có thể `loading="lazy"` nhưng vẫn giữ `src` thật
6. không dùng `data-lazy-src`

### Ảnh hero của Coindesk

Hero image được preload ngay trong `<head>`:

```html
<link rel="preload" as="image" imageSrcSet="...ảnh thật..." imageSizes="(max-width: 768px) 100vw, (max-width: 1200px) 800px, 1200px"/>
```

Ảnh hero trong body:

```html
<img
  alt="..."
  width="1920"
  height="1080"
  decoding="async"
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 800px, 1200px"
  srcSet="...ảnh thật..."
  src="/_next/image?url=...ảnh thật..."
/>
```

### Placeholder của Coindesk

Coindesk có dùng blur placeholder, nhưng placeholder chỉ nằm trong:

```html
style="background-image:url(data:image/jpeg;base64,...)"
```

Tức là:

- placeholder chỉ là lớp nền phụ trợ
- `src` vẫn là ảnh thật

Đây là điểm khác biệt rất quan trọng.

## Coincu đang làm như nào

Đối chiếu từ các bài Coincu đã kiểm tra trước đó:

- `https://coincu.com/what-1-bitcoin-can-buy-in-2026-10-luxury-cars-compared/`
- `https://coincu.com/what-is-kaito-ai-ai-powered-research-web3/`
- `https://coincu.com/what-is-humanity-protocol/`

### Pattern Coincu đang có

Nhiều ảnh body đang theo kiểu:

```html
<img
  src="data:image/svg+xml,..."
  data-lazy-src="https://coincu.com/wp-content/uploads/2026/05/image-36-1024x782.png"
  data-lazy-srcset="..."
>
```

Vấn đề của pattern này:

1. `src` không phải ảnh thật
2. ảnh thật nằm trong thuộc tính phụ thuộc JS
3. Google có thể vẫn render được, nhưng tín hiệu HTML gốc yếu hơn nhiều
4. image discovery bị phụ thuộc vào render/lazy-load

## So sánh ngắn gọn

### Coindesk

- `src` thật
- `srcset` thật
- hero image preload
- lazy-load theo kiểu an toàn hơn
- placeholder không thay thế ảnh thật trong `src`

### Coincu

- nhiều body image có `src` placeholder
- ảnh thật nằm trong `data-lazy-src`
- phụ thuộc JS để thay ảnh vào
- featured image tốt hơn body image
- image sitemap không phải vấn đề chính, HTML mới là vấn đề chính

## Coincu cần làm gì để cải thiện

### 1. Chuyển body images sang native lazy-load

Ảnh nội dung bài nên dùng:

```html
<img
  src="https://coincu.com/wp-content/uploads/2026/05/image-36-1024x782.png"
  srcset="https://coincu.com/wp-content/uploads/2026/05/image-36-300x229.png 300w,
          https://coincu.com/wp-content/uploads/2026/05/image-36-768x586.png 768w,
          https://coincu.com/wp-content/uploads/2026/05/image-36-1024x782.png 1024w"
  sizes="(max-width: 1024px) 100vw, 1024px"
  width="1024"
  height="782"
  alt="..."
  loading="lazy"
  decoding="async"
/>
```

Điểm quan trọng:

- `src` phải là ảnh thật
- `srcset` phải là ảnh thật
- có thể giữ `loading="lazy"`

### 2. Không dùng `src="data:image..."` cho ảnh trong article body

Đây là chỗ cần bỏ trước tiên.

Nếu plugin lazy-load hiện tại đang tự động nhét placeholder vào `src`, cần:

- tắt chế độ lazy-load kiểu JS placeholder
- hoặc exclude ảnh trong nội dung bài

### 3. Featured image không nên lazy-load

Ảnh hero / featured image nên dùng kiểu:

```html
<img
  src="https://coincu.com/wp-content/uploads/2026/05/top-luxury-car-buy-bitcoin-1024x575.png"
  srcset="https://coincu.com/wp-content/uploads/2026/05/top-luxury-car-buy-bitcoin-300x169.png 300w,
          https://coincu.com/wp-content/uploads/2026/05/top-luxury-car-buy-bitcoin-768x431.png 768w,
          https://coincu.com/wp-content/uploads/2026/05/top-luxury-car-buy-bitcoin-1024x575.png 1024w"
  sizes="(max-width: 1024px) 100vw, 1024px"
  width="1024"
  height="575"
  alt="What 1 Bitcoin can buy in 2026 luxury cars comparison"
  fetchpriority="high"
  decoding="async"
/>
```

Nếu có thể thì preload ảnh hero trong `<head>`.

### 4. Nếu chưa bỏ được lazy-load plugin, thêm `noscript` fallback

Phương án tạm:

```html
<img src="data:image/svg+xml,..." data-lazy-src="real-image.jpg" alt="...">
<noscript>
  <img src="real-image.jpg" alt="...">
</noscript>
```

Giải pháp này tốt hơn hiện tại, nhưng vẫn không đẹp bằng việc để `src` là ảnh thật từ đầu.

### 5. Giữ `width` và `height`

Mọi ảnh quan trọng nên có:

- `width`
- `height`

Điều này giúp:

- giảm layout shift
- làm HTML rõ ràng hơn cho Google

### 6. Giữ `alt` thật, không spam

Alt nên mô tả đúng ảnh, không nhồi keyword vô nghĩa.

### 7. Giữ ảnh trong sitemap như hiện tại

Coincu hiện đã có `<image:image>` trong sitemap bài viết. Phần này không phải ưu tiên sửa đầu tiên.

Ưu tiên cao nhất là:

- HTML image delivery
- featured image handling
- body-image lazy-load behavior

## Thứ tự ưu tiên sửa

### Mức 1

- featured image
- hero image
- ảnh đầu bài

### Mức 2

- ảnh trong `.entry-content` hoặc `.post-content`

### Mức 3

- ảnh card bài liên quan
- ảnh list/archive

## Checklist dev ngắn

1. Kiểm tra plugin lazy-load nào đang thay `src` thành placeholder
2. Exclude featured image khỏi lazy-load
3. Exclude ảnh trong article body khỏi kiểu lazy-load dùng `data-lazy-src`
4. Chuyển về native `loading="lazy"`
5. Giữ `src` và `srcset` là ảnh thật
6. Thêm `fetchpriority="high"` hoặc preload cho hero image
7. Re-test lại HTML source sau khi sửa

## Cách verify sau khi fix

Mở source HTML của bài và kiểm tra:

### Pass

- `src="https://coincu.com/wp-content/uploads/..."`
- `srcset="https://coincu.com/wp-content/uploads/..."`
- hero image không dùng placeholder trong `src`

### Fail

- `src="data:image/svg+xml,..."`
- ảnh thật chỉ nằm trong `data-lazy-src`

## Kết luận cuối

Nếu Coincu muốn cải thiện image indexing, cần học từ Coindesk ở điểm này:

- vẫn có thể lazy-load
- vẫn có thể dùng placeholder
- nhưng **ảnh thật phải nằm trong `src` / `srcset` ngay từ HTML gốc**

Đó là điểm Coincu đang yếu nhất hiện tại.
