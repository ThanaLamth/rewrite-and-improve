# Checklist Kiểm Tra Featured Image Không Index

## Khi nào dùng checklist này

Dùng khi:

- page đã được crawl hoặc đã index
- nhưng featured image vẫn không xuất hiện tốt trong Google Images
- hoặc nghi ngờ Google không discover được ảnh chính của bài

## 1. Kiểm tra Google có thấy ảnh thật trong HTML không

Ưu tiên kiểm tra:

- featured image có `src` thật không
- hay `src` chỉ là placeholder
- ảnh thật có đang bị đẩy sang `data-lazy-src` hoặc `data-lazy-srcset` không

### Dạng nên có

```html
<img src="https://example.com/real-image.jpg" loading="lazy">
```

### Dạng nên tránh cho featured image

```html
<img src="data:image/svg+xml,..." data-lazy-src="https://example.com/real-image.jpg">
```

Nếu featured image còn đang ở dạng placeholder thì đây là lỗi ưu tiên số 1.

## 2. Kiểm tra ảnh featured có xuất hiện nhất quán ở các vị trí quan trọng không

Nên có cùng một ảnh ở:

- `og:image`
- `twitter:image`
- schema `ImageObject`
- `primaryImageOfPage`
- ảnh hiển thị gần đầu bài trong phần body

Nếu chỉ có ở meta mà không có ảnh thật hiển thị rõ trong nội dung thì tín hiệu sẽ yếu hơn.

## 3. Kiểm tra file ảnh có crawl được không

Xác minh:

- mở trực tiếp URL ảnh có được không
- response của ảnh có phải `200 OK` không
- ảnh không bị `403`, `404`, `5xx`
- không bị robots chặn
- không có hotlink protection hoặc cấu hình CDN kỳ quặc

## 4. Kiểm tra canonical ảnh và sự nhất quán URL

Nhiều site dùng:

- ảnh gốc
- ảnh resize
- nhiều version thumbnail
- nhiều URL khác nhau cho cùng một ảnh

Cần kiểm tra:

- featured image gốc là URL nào
- meta/schema/body có đang trỏ cùng một ảnh hay không
- page có đang dùng resize image ở chỗ này nhưng schema lại trỏ ảnh khác không

Nếu không nhất quán, Google có thể chọn bản khác hoặc bỏ qua.

## 5. Kiểm tra tín hiệu quanh ảnh

Featured image nên có:

- `alt` rõ
- caption nếu phù hợp
- đoạn text gần ảnh mô tả đúng nội dung
- tiêu đề bài và ảnh liên quan chặt với nhau

Nếu ảnh quá generic hoặc ngữ cảnh quanh ảnh quá yếu thì cơ hội index cũng thấp hơn.

## 6. Kiểm tra độ độc đáo và giá trị của ảnh

Dù kỹ thuật đúng, Google vẫn không bắt buộc index mọi ảnh.

Featured image dễ yếu nếu:

- quá giống stock image
- chỉ là screenshot đơn giản
- không có giá trị riêng cho người tìm ảnh
- bị lặp lại quá nhiều nơi trên site

Ảnh gốc, infographic, chart, comparison visual thường mạnh hơn screenshot thuần.

## 7. Kiểm tra ảnh hưởng sitewide

Nếu toàn site đang có các vấn đề như:

- lazy load placeholder quá mạnh
- nhiều ảnh thumbnail không cần thiết
- cấu trúc ảnh trong bài yếu
- image discovery toàn site kém

thì featured image của từng bài cũng có thể bị ảnh hưởng.

## Thứ tự ưu tiên sửa

1. Đảm bảo featured image có `src` thật trong HTML.
2. Dùng cùng một URL ảnh nhất quán ở:
   - `og:image`
   - `twitter:image`
   - schema
   - ảnh đầu bài
3. Đảm bảo URL ảnh trả `200 OK`.
4. Đảm bảo ảnh không bị robots chặn.
5. Giữ `alt` và ngữ cảnh quanh ảnh rõ ràng.
6. Ưu tiên ảnh gốc / visual tự thiết kế nếu có thể.

## Rule cực ngắn

Nếu featured image không index, cần check theo 4 nhóm:

- `render`: Google có thấy ảnh thật trong `src` không
- `crawlability`: ảnh có mở được và crawl được không
- `consistency`: meta / schema / body có dùng cùng một URL ảnh không
- `uniqueness`: ảnh có đủ giá trị và đủ khác biệt không

## Cách dùng thực tế

Cho mỗi bài cần debug, chỉ cần đánh dấu:

- Pass / Fail cho từng mục
- nếu fail ở `render` thì sửa trước
- nếu render ổn rồi mới soi tiếp crawlability và consistency
