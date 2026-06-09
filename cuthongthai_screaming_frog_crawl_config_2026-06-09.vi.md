# Cấu Hình Screaming Frog Cho Case Cuthongthai.vn

Ngày soạn: 2026-06-09  
Đối tượng crawl: `https://cuthongthai.vn/` cùng các subdomain chính  
Mục tiêu: kiểm tra kiến trúc SEO, phân phối internal link, mức độ tách silo giữa các subdomain, và chất lượng triển khai kỹ thuật

## Mục Tiêu Của Lượt Crawl

Với case `cuthongthai.vn`, Screaming Frog không chỉ dùng để đếm URL. Mục tiêu chính là trả lời các câu hỏi đang còn treo:

1. mỗi subdomain có bao nhiêu URL indexable thực sự
2. domain gốc đang phân phối internal link sang các subdomain như thế nào
3. có trùng lặp title, H1, template hoặc intent giữa các vertical hay không
4. canonical, redirect và sitemap của từng subdomain có sạch không
5. subdomain nào là hub thực sự, subdomain nào chỉ là entry point

## Cách Tiếp Cận Khuyến Nghị

Không nên bật JavaScript render cho toàn hệ ngay từ đầu. Cách hợp lý hơn là chia làm `2 vòng crawl`.

### Vòng 1: Crawl kiến trúc tổng thể

Mục tiêu:

- nhìn toàn hệ ở mức URL, internal links, redirects, canonical, directives, title, H1
- lấy được bức tranh toàn bộ mối quan hệ giữa domain gốc và các subdomain

Cấu hình:

- `Mode`: `Spider`
- `Start URL`: `https://cuthongthai.vn/`
- `Rendering`: `Text Only`
- `Scope`: crawl từ domain gốc và đi theo liên kết nội bộ
- `Subdomains`: giữ chế độ crawl tất cả subdomain liên quan

Vì sao dùng `Text Only` trước:

- nhanh hơn
- nhẹ hơn
- đủ để kiểm tra kiến trúc SEO cốt lõi
- tránh tốn tài nguyên vào các thành phần render không cần thiết ở vòng đầu

### Vòng 2: Crawl render JavaScript có chọn lọc

Mục tiêu:

- kiểm tra các phần navigation, card module, hub page, hoặc internal links chỉ xuất hiện sau render
- xác minh các vertical dạng app-like như `Vimo` có lộ đủ link cho bot hay không

Cấu hình:

- `Mode`: `Spider`
- `Rendering`: `JavaScript`
- crawl riêng từng subdomain chính thay vì full hệ cùng lúc

Nên ưu tiên:

- `https://vimo.cuthongthai.vn/`
- `https://thue.cuthongthai.vn/`
- `https://tamlinh.cuthongthai.vn/`
- `https://muanha.cuthongthai.vn/`

## Cấu Hình Chi Tiết Nên Dùng

### 1. Chế độ crawl

- `Mode`: `Spider`
- `Start URL`: `https://cuthongthai.vn/`

Đây là điểm bắt đầu đúng nếu bạn muốn xem toàn bộ hệ sinh thái, không chỉ một subdomain riêng lẻ.

### 2. Phạm vi subdomain

Giữ cấu hình crawl tất cả subdomain liên quan.

Ý nghĩa:

- nếu bắt đầu từ domain gốc, bạn sẽ thấy được root đang link sang đâu
- bạn sẽ không bỏ sót các vertical quan trọng như `vimo`, `thue`, `tamlinh`, `muanha`, `suckhoe`

### 3. Rendering

Cho vòng 1:

- `Text Only`

Cho vòng 2:

- `JavaScript`

Không nên:

- bật `JavaScript` cho toàn hệ ngay từ đầu
- crawl toàn bộ mọi thứ ở chế độ render nếu mục tiêu chính là SEO architecture

### 4. User-Agent

Khuyến nghị:

- để mặc định của Screaming Frog

Nếu muốn gần hơn với góc nhìn của Google:

- có thể chuyển sang `Googlebot Desktop`

Nhưng với case này, khác biệt lớn nhất không nằm ở user-agent mà nằm ở cách bạn chia vòng crawl hợp lý hay không.

### 5. Tốc độ crawl

Khuyến nghị:

- bắt đầu với mức mặc định
- nếu thấy server phản hồi chậm hoặc có dấu hiệu chặn, giảm thread xuống

Mục tiêu:

- không làm lỗi crawl do quá tải
- giữ dữ liệu ổn định hơn cho các vertical đang chạy trên nhiều hạ tầng khác nhau

### 6. Các mục nên bật

Khuyến nghị bật:

- `Store HTML` nếu máy đủ RAM
- `Always Follow Redirects`
- `Crawl Analysis` sau khi crawl xong
- `Structured Data` extraction

Những cái này hữu ích vì:

- bạn sẽ cần đối chiếu canonical và schema giữa các subdomain
- bạn sẽ cần biết có link nội bộ đang đi qua 301 hay không

## Những Thiết Lập Không Nên Bật Ngay

Ở vòng đầu, nên tránh:

- crawl ảnh quá sâu nếu mục tiêu là SEO architecture
- crawl CSS và JS asset quá rộng
- bật render JavaScript toàn hệ
- bắt đầu từng subdomain riêng lẻ nếu bạn chưa có bức tranh tổng

Lý do:

- dữ liệu bị loãng
- crawl chậm
- khó đọc insight kiến trúc
- dễ tốn thời gian vào noise thay vì tín hiệu quan trọng

## Các Tab Cần Xem Trong Screaming Frog

Sau khi crawl xong, tập trung vào các tab sau:

- `Internal`
- `Inlinks`
- `Response Codes`
- `Directives`
- `Canonicals`
- `Page Titles`
- `H1`
- `Structured Data`
- `Sitemaps`

Với case này, đây là các tab đủ để trả lời phần lớn câu hỏi chiến lược.

## Các File Nên Export

Khuyến nghị export tối thiểu:

- `Internal`
- `Inlinks`
- `Response Codes`
- `Directives`
- `Canonicals`
- `Page Titles`
- `H1`
- `Structured Data`
- `Sitemaps`

Khuyến nghị export thêm:

- `Bulk Export > All Inlinks`
- `Bulk Export > Redirect Chains`
- `Bulk Export > Canonical Errors`

Nếu muốn đọc kỹ root domain và vai trò hub page:

- export thêm dữ liệu internal links theo source page

## Cách Đọc Dữ Liệu Cho Đúng Với Case Này

### 1. Kiểm tra root domain đang làm gì

Bạn cần trả lời:

- `cuthongthai.vn` đang là hub thật hay chỉ là cổng điều hướng
- nó link mạnh nhất sang subdomain nào
- nó có đang tạo authority flow cân bằng hay lệch hẳn sang một mảng

Tab nên xem:

- `Internal`
- `All Inlinks`

### 2. Kiểm tra từng subdomain có đủ “site-level identity” không

Bạn cần nhìn:

- title
- H1
- canonical
- schema
- navigation nội bộ

Mục đích:

- xem mỗi subdomain có đang hành xử như một site riêng hay chỉ là một route được gắn hostname

### 3. Kiểm tra duplicate và overlap

Bạn cần tìm:

- title trùng
- H1 trùng
- nhiều URL cùng intent
- page template lặp lại quá mức

Mục đích:

- xem việc tách subdomain có thực sự tạo clarity hay chỉ tạo thêm nhiều lớp URL

### 4. Kiểm tra redirect và canonical

Đặc biệt với case này, rất nên xem:

- root article có redirect sang subdomain không
- canonical có tự trỏ đúng subdomain không
- có URL nào tự mâu thuẫn giữa canonical, redirect và sitemap không

### 5. Kiểm tra sitemap

Bạn cần so:

- sitemap domain gốc
- sitemap từng subdomain
- URL có thật sự indexable không

Mục tiêu:

- phát hiện tình trạng sitemap trộn sai vertical
- phát hiện sitemap chỉ liệt kê một phần hệ sinh thái

## Nên Chạy Thêm Một Vòng Audit Sitemap Riêng

Ngoài spider crawl, rất nên dùng `List Mode` để crawl sitemap riêng.

Danh sách cần kiểm tra:

- `https://cuthongthai.vn/sitemap.xml`
- sitemap của `vimo`
- sitemap của `thue`
- sitemap của `tamlinh`
- sitemap của `muanha`
- sitemap của `suckhoe`

Lý do:

- kiểm tra sitemap độc lập thường lộ ra lỗi mà spider crawl bình thường không nhấn mạnh đủ
- đặc biệt hữu ích khi nghi ngờ root sitemap không phản ánh đúng toàn hệ

## Quy Trình Chạy Khuyến Nghị

### Bước 1

Chạy `Spider` từ:

- `https://cuthongthai.vn/`

Thiết lập:

- `Text Only`
- crawl toàn bộ subdomain liên quan

### Bước 2

Export các file chính:

- `Internal`
- `Inlinks`
- `Response Codes`
- `Directives`
- `Canonicals`
- `Page Titles`
- `H1`
- `Structured Data`
- `Sitemaps`

### Bước 3

Chạy `JavaScript render` riêng cho:

- `vimo`
- `thue`
- `tamlinh`
- `muanha`

Mục tiêu:

- kiểm tra menu render
- card hub
- module links
- điều hướng nội bộ sau render

### Bước 4

Chạy `List Mode` với các sitemap chính

Mục tiêu:

- audit sitemap độc lập
- đối chiếu với dữ liệu indexable và canonical

## Những Câu Hỏi Crawl Này Sẽ Giúp Chốt

Sau khi có dữ liệu, bạn sẽ chốt được:

1. subdomain nào thực sự là một vertical mạnh
2. subdomain nào chỉ đang dùng hostname riêng nhưng chưa có site-level strength đủ mạnh
3. root domain có đang làm đúng vai trò hub hay không
4. authority nội bộ đang được gom hay đang bị chia quá mức
5. mô hình nhiều subdomain này đang hỗ trợ SEO hay đang làm kiến trúc phức tạp hơn mức cần thiết

## Kết Luận Thực Dụng

Nếu chỉ muốn hiểu logic chiến lược của `cuthongthai.vn`, không nhất thiết phải crawl.

Nhưng nếu muốn trả lời câu hỏi khó hơn:

- mô hình này đang tốt thật hay chỉ nhìn có vẻ hợp lý
- subdomain nào nên giữ
- subdomain nào nên gộp
- internal linking hiện tại đang truyền lực ra sao

thì Screaming Frog gần như là bước bắt buộc.

## Link Tài Liệu Chính Thức

- Screaming Frog general guide: `https://www.screamingfrog.co.uk/seo-spider/user-guide/general/`
- Screaming Frog configuration guide: `https://www.screamingfrog.co.uk/seo-spider/user-guide/configuration/`
- JavaScript crawling tutorial: `https://www.screamingfrog.co.uk/seo-spider/tutorials/how-to-crawl-javascript-websites/`
- XML sitemap auditing: `https://www.screamingfrog.co.uk/how-to-audit-xml-sitemaps/`
