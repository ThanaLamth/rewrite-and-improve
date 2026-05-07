# Coincu Sitemap: Cách Fix Thực Tế

## Kết luận nhanh

Sitemap của Coincu hiện **ổn về cấu trúc** nhưng có dấu hiệu **cập nhật chậm hoặc lệch cache**:

- Bài mới có trong `google-news-sitemap.xml`
- Nhưng chưa thấy trong `post-sitemap.xml` hoặc `post-sitemap1.xml`
- `sitemap_index.xml` đang báo `lastmod` cũ hơn dữ liệu thật nằm trong child sitemap

Vì vậy, vấn đề chính không phải là thiếu `image-sitemap.xml` riêng, mà là **sitemap freshness** và **độ tin cậy của tín hiệu lastmod**

## Cách fix nên làm theo thứ tự

### 1. Flush lại sitemap của Rank Math

Vào:

- `WordPress Admin -> Rank Math SEO -> Sitemap Settings`

Sau đó:

- đổi tạm `Links Per Sitemap` tăng hoặc giảm `1`
- bấm `Save Changes`

Mục tiêu:

- ép Rank Math regenerate lại sitemap
- kiểm tra xem bài mới đã xuất hiện trong post sitemap thường chưa

Kiểm tra lại các URL sau:

- `https://coincu.com/sitemap_index.xml`
- `https://coincu.com/post-sitemap.xml`
- `https://coincu.com/post-sitemap1.xml`

### 2. Purge cache ở tầng ngoài

Coincu đang đi qua `Cloudflare` và có dấu `WP Rocket`, nên cần xóa cache ở cả hai tầng:

- purge cache toàn site trên `Cloudflare`
- purge cache trên `WP Rocket`

Ngoài ra nên exclude sitemap khỏi cache:

- `/sitemap_index.xml`
- `/*-sitemap.xml`
- `/*-sitemap*.xml`
- `/google-news-sitemap.xml`

Nếu không loại trừ phần này, XML có thể tiếp tục phục vụ bản cache cũ dù WordPress đã có dữ liệu mới.

### 3. Kiểm tra post có bị exclude khỏi sitemap không

Mở đúng bài viết trong WordPress và check:

- bài đang là `index`, không phải `noindex`
- canonical là self-canonical hoặc để mặc định
- không có tùy chọn exclude khỏi sitemap
- post type `Posts` vẫn đang được include trong Rank Math sitemap settings

Vì bài này đang có trong news sitemap nhưng chưa có trong post sitemap thường, cần loại trừ khả năng có rule riêng áp vào bài hoặc vào category.

### 4. Resave permalink

Vào:

- `WordPress Admin -> Settings -> Permalinks`

Sau đó:

- không cần đổi gì
- bấm `Save Changes`

Thao tác này giúp refresh rewrite rules nếu route sitemap bị lệch.

### 5. Nếu vẫn lỗi, tắt sitemap caching của Rank Math

Có thể thêm snippet sau vào chỗ load custom code:

```php
add_filter( 'rank_math/sitemap/enable_caching', '__return_false' );
```

Chỉ nên dùng khi sitemap bị stale lặp lại nhiều lần hoặc XML không refresh đúng dù đã purge cache.

### 6. Kiểm tra plugin custom của Coincu

Site có dấu vết plugin custom:

- `coincu-seo-fixes`

Cần rà plugin này xem có:

- hook vào `rank_math/sitemap/*`
- can thiệp canonical hoặc robots meta
- loại một số post khỏi sitemap
- sửa logic sitemap theo category, tag, template, hoặc post age

Nếu có custom filter ở đây thì khả năng cao đây mới là nguyên nhân gốc.

## Sau khi fix cần kiểm tra lại

### A. Kiểm tra XML

Mở lại:

- `https://coincu.com/sitemap_index.xml`
- `https://coincu.com/post-sitemap.xml`
- `https://coincu.com/post-sitemap1.xml`

Cần xác nhận:

- bài mới đã vào post sitemap thường
- `lastmod` ở `sitemap_index.xml` phản ánh đúng child sitemap mới nhất

### B. Kiểm tra Search Console

Sau khi XML đã đúng:

- submit lại `sitemap_index.xml`
- request indexing cho bài mới nếu cần
- theo dõi vài ngày xem Google có lấy lại sitemap chuẩn không

## Nhận định nguyên nhân khả dĩ nhất

Thứ tự ưu tiên điều tra:

1. `Rank Math sitemap cache`
2. `Cloudflare` hoặc `WP Rocket` đang cache XML
3. plugin custom `coincu-seo-fixes` đang can thiệp
4. post bị exclude riêng khỏi sitemap thường

## Điều này liên quan gì đến image indexing

Nó không phải bằng chứng cho thấy Coincu đang bị chặn index ảnh. Tuy nhiên, nếu sitemap thường cập nhật lệch, còn ảnh trong body lại phụ thuộc nhiều vào lazy-load placeholder, thì khả năng Google discover ảnh đầy đủ sẽ yếu hơn.

Nói ngắn gọn:

- vấn đề sitemap ở đây là **freshness**
- vấn đề image index ở Coincu là **discoverability**
- hai vấn đề khác nhau, nhưng cộng dồn lại sẽ làm tín hiệu thu thập không đẹp

## Nguồn đối chiếu

- Google Search Central: `https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap`
- Google Search Central: `https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps`
- Google Search Central: `https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps`
- Rank Math KB: `https://rankmath.com/kb/configure-sitemaps/`
- Rank Math KB: `https://rankmath.com/kb/url-not-in-sitemap/`
- Rank Math KB: `https://rankmath.com/kb/fix-sitemap-issues/`
