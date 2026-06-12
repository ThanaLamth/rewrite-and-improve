# Script Chi Tiết Để Tích Hợp Feature `Crypto Tax Top-5` Vào CoinLineup

Ngày soạn: 2026-06-12  
Đối tượng: `https://coinlineup.com/`  
Mục tiêu: mô tả chi tiết cách nhét feature `crypto tax calculator` vào web theo kiểu `integrated product feature`, không phải landing page rời

## 1. Mục Tiêu Của Feature

Feature này không nên được đóng như một trang campaign độc lập.

Nó nên được xây như một `tool module` thật trong hệ `CoinLineup`, với 3 mục tiêu cùng lúc:

- phục vụ user intent cao: `crypto tax calculator`, `bitcoin tax by country`, `crypto gain tax`
- tăng độ dính của hệ `Tools`
- mở một cụm nội dung mới nối giữa `Tools`, `Guides` và `Crypto Regulations`

## 2. Tên Feature

Tên gợi ý:

- `Crypto Tax Calculator`
- hoặc `Crypto Tax Estimator`

Tên hub page:

- `Crypto Tax Calculator by Country`

Tên sub-pages:

- `Japan Crypto Tax Calculator`
- `Denmark Crypto Tax Calculator`
- `South Africa Crypto Tax Calculator`
- `Ireland Crypto Tax Calculator`
- `India Crypto Tax Calculator`

## 3. Kiến Trúc URL Nên Dùng

Nếu `CoinLineup` đã có cụm `Tools`, ưu tiên:

- `/tools/crypto-tax/`
- `/tools/crypto-tax/japan/`
- `/tools/crypto-tax/denmark/`
- `/tools/crypto-tax/south-africa/`
- `/tools/crypto-tax/ireland/`
- `/tools/crypto-tax/india/`

Không nên:

- nhét tất cả vào một trang có dropdown duy nhất
- làm 1 landing page riêng ngoài IA chính của site
- dùng fragment như `#japan`, `#india` để thay URL

Lý do:

- user vẫn thấy đây là 1 feature thống nhất
- Google vẫn có từng URL riêng để hiểu country intent
- dễ internal link từ guides và regulation pages sang đúng page đích

## 4. Kiến Trúc Product Nên Dùng

Feature nên có 2 lớp:

### 4.1 Lớp hub

`/tools/crypto-tax/`

Vai trò:

- giới thiệu feature
- giải thích cách dùng
- liệt kê 5 quốc gia support
- chọn country
- link sang từng calculator cụ thể

### 4.2 Lớp country page

Mỗi quốc gia 1 page riêng.

Mỗi page dùng chung một calculator engine, nhưng:

- title khác
- copy khác
- assumptions khác
- tax logic khác
- sources khác

## 5. Logic Ranking Nội Dung Của Feature

Không nên để page chỉ có form.

Mỗi country page cần đủ 5 lớp:

1. `tool UI`
2. `methodology`
3. `assumptions`
4. `official sources`
5. `supporting explanation`

Đây là phần rất quan trọng.

Nếu page chỉ là một widget:

- user vẫn dùng được
- nhưng Google sẽ khó hiểu page nói gì

Nếu page có cả tool + content:

- vừa dùng được
- vừa crawl/read/index tốt hơn

## 6. Quốc Gia Support Trong V1

Top 5 đề xuất cho v1:

1. `Japan`
2. `Denmark`
3. `South Africa`
4. `Ireland`
5. `India`

Lưu ý:

- đây là `top 5 để làm product v1`
- không phải bảng xếp hạng tuyệt đối cho mọi cấu trúc thuế trên thế giới

## 7. Cấu Trúc Chung Của Hub Page

URL:

- `/tools/crypto-tax/`

### 7.1 Hero

Gồm:

- H1: `Crypto Tax Calculator by Country`
- subheading: nêu rõ đây là estimator theo từng quốc gia
- CTA chọn country

Copy mẫu:

`Estimate your crypto tax in high-tax jurisdictions using country-specific assumptions and official tax references.`

### 7.2 Country selector block

Hiển thị:

- Japan
- Denmark
- South Africa
- Ireland
- India

Mỗi card có:

- tên nước
- tax style
- headline rate
- 1 dòng mô tả
- CTA `Open calculator`

### 7.3 How it works

3 bước:

1. chọn country
2. nhập net gain
3. xem estimated tax và assumptions

### 7.4 Why this calculator is limited

Phải có box note:

- not tax filing software
- not legal advice
- retail individual scenarios only
- DeFi / perps / advanced structures chưa cover đầy đủ

### 7.5 Internal links section

Khối link sang:

- crypto regulation guides
- tax education guides
- price/converter tools liên quan nếu có

## 8. Cấu Trúc Chung Của Country Page

Ví dụ:

- `/tools/crypto-tax/japan/`

### 8.1 Hero

Phải có:

- H1: `Japan Crypto Tax Calculator`
- short explainer
- last updated

### 8.2 Calculator block

UI gồm:

- `Net crypto gain`
- `Other taxable income` nếu cần
- field phụ theo từng nước

Outputs:

- `Estimated tax`
- `After-tax gain`
- `Effective rate`

### 8.3 Assumptions

Ví dụ với Japan:

- gain được model như miscellaneous income
- national progressive tax
- reconstruction surtax
- local resident tax mặc định 10%

### 8.4 Methodology

Phần text giải thích:

- page này đang tính cái gì
- chưa tính cái gì
- trường hợp nào kết quả có thể chênh nhiều

### 8.5 Official sources

Dùng list link ra nguồn chính thức.

### 8.6 Related guides

Ít nhất 2-4 internal links:

- how crypto tax works in Japan
- Japan crypto tax basics for retail traders
- country comparison pages

## 9. Logic Riêng Của Từng Quốc Gia

## 9.1 Japan

URL:

- `/tools/crypto-tax/japan/`

Currency:

- `JPY`

Inputs:

- `Net crypto gain`
- `Other taxable income`
- `Resident tax rate`

Output logic:

- progressive national tax
- cộng `2.1%` reconstruction surtax trên income tax
- cộng resident tax

Page note:

- model resident individual
- gain treated as miscellaneous income

Suggested title:

`Japan Crypto Tax Calculator: Estimate Miscellaneous Income Tax on Crypto Gains`

## 9.2 Denmark

URL:

- `/tools/crypto-tax/denmark/`

Currency:

- `DKK`

Inputs:

- `Net crypto gain`
- `Other taxable income`
- `Municipal tax rate`

Output logic:

- bottom-bracket tax
- middle-bracket tax
- top-bracket tax
- municipal layer

Page note:

- model private speculation / personal income scenario
- church tax chưa tính

Suggested title:

`Denmark Crypto Tax Calculator: Estimate Personal Income Tax on Crypto Gains`

## 9.3 South Africa

URL:

- `/tools/crypto-tax/south-africa/`

Currency:

- `ZAR`

Inputs:

- `Net crypto gain`
- `Other taxable income`

Output logic:

- normal individual progressive tax
- incremental tax from gain

Page note:

- chỉ model `revenue account / trading` scenario
- không model CGT scenario trong v1

Suggested title:

`South Africa Crypto Tax Calculator: Trading Income Estimate`

## 9.4 Ireland

URL:

- `/tools/crypto-tax/ireland/`

Currency:

- `EUR`

Inputs:

- `Net crypto gain`
- `Unused annual exemption`

Output logic:

- gain trừ exemption
- tax `33%`

Page note:

- personal disposal case
- annual exempt amount mặc định `EUR 1,270`

Suggested title:

`Ireland Crypto Tax Calculator: Estimate CGT on Crypto Gains`

## 9.5 India

URL:

- `/tools/crypto-tax/india/`

Currency:

- `INR`

Inputs:

- `Net crypto gain`
- `Surcharge rate`

Output logic:

- base tax `30%`
- cộng surcharge
- cộng `4%` cess

Page note:

- VDA regime
- cost basis assumed already resolved before input

Suggested title:

`India Crypto Tax Calculator: Estimate VDA Tax on Crypto Gains`

## 10. Thứ Tự Khối Nội Dung Trong HTML

Mỗi country page nên đi theo thứ tự này:

1. `H1`
2. short explainer
3. calculator
4. assumptions
5. methodology
6. official sources
7. FAQ
8. related guides

Đừng đảo ngược kiểu:

- show 5 màn ads
- rồi mới tới tool

## 11. FAQ Gợi Ý Cho Mỗi Country Page

Mỗi page nên có ít nhất 4-6 câu:

- Does this calculator file taxes for me?
- Is this a tax estimate or a final tax number?
- Does this include staking, mining, or DeFi?
- Do I need to add other taxable income?
- Which official sources was this calculator based on?

FAQ không nên viết generic y chang nhau 100%.

Mỗi nước nên tùy biến ít nhất 2 câu theo logic riêng.

## 12. Internal Link Map Nên Dùng

## 12.1 Từ hub page

Hub page link xuống:

- 5 country pages
- 1 comparison guide
- 1 methodology page nếu có

## 12.2 Từ country page

Country page link sang:

- country-specific guide
- broader crypto tax guide
- regulations category
- hub page

## 12.3 Từ guides

Guide pages link ngược về:

- đúng country calculator

Ví dụ:

- bài `Japan crypto tax rules` phải link về `/tools/crypto-tax/japan/`
- không nên chỉ link về hub page

## 13. Schema Và Search Presentation

Không cần phát minh schema kỳ lạ.

Có thể dùng:

- `FAQPage` nếu FAQ đúng là visible
- `BreadcrumbList`
- `WebPage`

Không nên spam schema.

Điểm quan trọng hơn schema là:

- page có text giải thích rõ
- title đúng intent
- tool render được
- internal links rõ

## 14. Technical Requirements Khi Build

Feature nên đảm bảo:

- URL trả `200`
- không chặn Googlebot
- không phụ thuộc fragment
- nội dung quan trọng thấy được sau render
- canonical self-referencing
- meta title và description riêng từng country page

Nếu dùng JS app:

- phần title
- copy chính
- assumptions
- sources

phải render tốt, không nên để trống rồi chờ client-side quá lâu.

## 15. Tracking Nên Gắn

Sự kiện nên track:

- country selected
- calculate clicked
- result viewed
- source clicked
- related guide clicked

Nếu có form nâng cấp sau này:

- save estimate
- email me my estimate

Nhưng v1 không cần làm lead capture nếu muốn ship nhanh.

## 16. Content Script Mẫu Cho Hub Page

### H1

`Crypto Tax Calculator by Country`

### Subheading

`Estimate crypto taxes in five high-tax jurisdictions using country-specific assumptions, local currencies, and official tax references.`

### Short disclaimer

`This tool provides educational estimates for resident individuals. It is not tax filing software or legal advice.`

### CTA labels

- `Open Japan Calculator`
- `Open Denmark Calculator`
- `Open South Africa Calculator`
- `Open Ireland Calculator`
- `Open India Calculator`

## 17. Content Script Mẫu Cho Country Page

Ví dụ Japan:

### H1

`Japan Crypto Tax Calculator`

### Intro

`Estimate the tax impact of crypto gains in Japan under a miscellaneous income scenario, including progressive national tax, reconstruction surtax, and local resident tax assumptions.`

### Assumption heading

`What this estimate assumes`

### Methodology heading

`How this Japan crypto tax estimate works`

### Disclaimer line

`This estimate is for educational use and does not replace professional tax advice.`

## 18. UX Script Của Calculator

Flow user nên là:

1. user vào country page
2. thấy ngay tool fold đầu
3. nhập gain
4. nếu applicable nhập `other income`
5. xem result
6. đọc assumptions
7. click sang guide liên quan

Nếu page bắt user đọc quá nhiều trước khi dùng tool:

- mất intent
- giảm conversion usage

## 19. Roadmap V1, V1.1, V1.2

### V1

- hub page
- 5 country pages
- calculator engine
- assumptions
- official sources

### V1.1

- 1 guide cho mỗi country
- FAQ tốt hơn
- compare page: `Japan vs India crypto tax`

### V1.2

- thêm scenarios:
  - staking
  - mining
  - DeFi basics
- save/share estimate

## 20. Điều Không Nên Làm

Không nên:

- làm 1 page có dropdown rồi nghĩ thế là đủ SEO
- viết copy quá mơ hồ
- nói `accurate for all crypto transactions`
- trộn 5 nước trong 1 URL duy nhất
- nhét tool vào homepage mà không có page riêng

## 21. Checklist Build Cho Dev / SEO

1. Tạo route hub page.
2. Tạo 5 route country pages.
3. Dùng chung tax engine, khác config từng nước.
4. Gắn title/description riêng từng page.
5. Gắn canonical self-referencing.
6. Render visible assumptions và sources.
7. Gắn FAQ nếu nội dung hiển thị thật.
8. Link từ menu `Tools`.
9. Link từ `Guides` và `Crypto Regulations`.
10. Submit vào sitemap sau khi publish.

## 22. Chốt Lại

Nếu build cho `CoinLineup`, hướng đúng không phải là:

- landing page rời
- hoặc widget ẩn trong site

Mà là:

`một feature tool thật trong IA của web, gồm 1 hub page + 5 country URLs + shared calculator engine + guide pages nuôi intent và internal links`

Đó là cách vừa hợp product, vừa hợp SEO, vừa hợp logic crawl/index của Google.
