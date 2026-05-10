# Kế Hoạch Build Hubpage Cho Coincu

Last updated: 2026-05-10

## Mục tiêu

Kế hoạch này tóm tắt:

- các hubpage Coincu đang ưu tiên build
- dự án pillar/cluster đang build song song
- từng hub dùng để gom loại bài nào
- thứ tự rollout hợp lý
- các file draft public-ready đã có sẵn để tiếp tục triển khai

## Trạng thái hiện tại

Đã có bản public-ready cho 4 hub ưu tiên:

1. `Coin Reviews`
2. `Protocol Reviews`
3. `Exchange Reviews`
4. `Wallet Reviews`

Các hub này là lớp nền để:

- tăng topical authority đúng chủ đề crypto
- gom bớt content đang nằm rải rác ở archive
- tạo internal linking sạch hơn giữa review, ecosystem, glossary, guide

Song song với đó, Coincu cũng đang có một nhánh **pillar consumer-style** riêng:

- `What 1 Bitcoin Can Buy`

Đây không phải hub review truyền thống. Nó là một cụm pillar/cluster dùng góc nhìn purchasing power của BTC để mở rộng traffic theo hướng consumer, finance-adjacent, và topical bridge giữa crypto với các chủ đề đời sống có thể quy đổi hợp lý.

## Thứ tự rollout đề xuất

### Giai đoạn 1: Build ngay

1. `Coin Reviews`
2. `Exchange Reviews`
3. `Protocol Reviews`
4. `Wallet Reviews`
5. `What 1 Bitcoin Can Buy`

### Giai đoạn 2: Build sau khi 4 hub nền ổn

6. `Ecosystem Hubs`
7. `Crypto Glossary` tối ưu lại
8. `On-chain Movers / Why Is X Pumping`

### Giai đoạn 3: Chỉ làm nếu có đủ lực cập nhật

9. `Airdrop Guides`
10. `DeFi Strategy / Staking / Yield`
11. `Security / Scam / Incident Guides`

## 1. Coin Reviews

### Vai trò

Hub này dùng để gom các bài review token, coin, project-level coin thesis, và các bài kiểu `what is x coin` hoặc `x token review`.

### Loại bài nên nằm trong hub này

- coin review
- token explainer
- `what is x coin`
- tokenomics explainer
- risk / catalyst pages cho từng coin
- meme coin review
- AI coin review
- legacy coin / recovery-thesis coin

### Ví dụ bài phù hợp

- `What Is Humanity Protocol?`
- `BUILDon (B) Review`
- `Terra Classic (LUNC) Explained`
- `What Is USD.AI (CHIP)?`
- `Bittensor Review`
- `Ethena Review`

### Không nên nhét vào hub này

- protocol-level architecture pages nếu trọng tâm là sản phẩm
- exchange reviews
- wallet reviews
- glossary pages

### File draft hiện có

- `coincu_coin_reviews_hubpage_public_ready.md`

## 2. Protocol Reviews

### Vai trò

Hub này dùng để gom các bài đánh giá dự án, network, app-layer system, hạ tầng, protocol, Layer 1, AI protocol, DeFi protocol.

### Loại bài nên nằm trong hub này

- protocol review
- Layer 1 / Layer 2 project review
- DeFi protocol review
- AI protocol review
- storage / infrastructure protocol review
- app-layer product explainer
- ecosystem-level project analysis nếu trọng tâm là hệ thống

### Ví dụ bài phù hợp

- `The Open Network Review`
- `What is Kaito.ai?`
- `Walrus Protocol Review`
- `Aave Review`
- `Aleo Review`
- `Agility Protocol Review`

### Không nên nhét vào hub này

- pure token pages nếu chủ yếu nói coin price thesis
- exchange reviews
- wallet guides

### File draft hiện có

- `coincu_protocol_reviews_hubpage_public_ready.md`

## 3. Exchange Reviews

### Vai trò

Hub này dùng để gom các bài review sàn giao dịch crypto theo intent rất rõ: phí, thanh khoản, bảo mật, KYC, sản phẩm, beginner fit, trader fit.

### Loại bài nên nằm trong hub này

- exchange review
- CEX review
- DEX review nếu review theo hướng sàn
- beginner exchange comparison
- derivatives exchange review
- regional exchange review
- exchange feature comparison

### Ví dụ bài phù hợp

- `Bitfinex Review`
- `KuCoin Review`
- `Coincheck Review`
- `CoinW Review`
- `Binance Review`
- `P2B Review`
- `Tapbit Review`

### Không nên nhét vào hub này

- wallet articles
- protocol pages
- token pages

### File draft hiện có

- `coincu_exchange_reviews_hubpage_public_ready.md`

## 4. Wallet Reviews

### Vai trò

Hub này dùng để gom các bài review ví, self-custody workflow, ecosystem wallet picks, beginner wallet picks, security-oriented wallet guides.

### Loại bài nên nằm trong hub này

- wallet review
- hot wallet review
- hardware wallet guide/review
- chain-specific wallet pages
- wallet setup guide
- wallet recovery / wallet security basics

### Ví dụ bài phù hợp

- `Tonkeeper Wallet Review`
- `Rabby Wallet Review`
- `Argent Wallet Review`
- `How to Create and Use TON Wallets`
- `How to Find Your Trust Wallet Recovery Phrase`

### Không nên nhét vào hub này

- exchange pages
- coin pages
- protocol pages

### File draft hiện có

- `coincu_wallet_reviews_hubpage_public_ready.md`

## 5. What 1 Bitcoin Can Buy

### Vai trò

Đây là một **pillar project** riêng, không phải review hub thuần crypto. Nó dùng một framework rất dễ hiểu với người dùng phổ thông:

- `1 BTC hiện tại mua được gì`

Mục tiêu của cụm này là:

- tạo một pillar mạnh xoay quanh sức mua của Bitcoin
- mở rộng ra nhiều cluster consumer-friendly nhưng vẫn giữ BTC là trung tâm
- tránh rơi vào generic lifestyle traffic quá xa chủ đề crypto bằng cách luôn giữ góc nhìn quy đổi từ BTC

### Loại bài nên nằm trong cụm này

- pillar gốc `What 1 Bitcoin Can Buy`
- comparison article theo từng ngành hàng
- category edition pages
- listicle so sánh theo budget 1 BTC
- bài quy đổi BTC sang tài sản/đồ vật/collectible có thị trường rõ ràng

### Cấu trúc nên có

#### Pillar gốc

- `What 1 Bitcoin Can Buy`

#### Cluster nên ưu tiên

- `Cars Edition`
- `Cards Edition`
- `Watches Edition`
- `Real Estate Edition`
- `Luxury Goods Edition`

### Loại bài con phù hợp

- `What 1 Bitcoin Can Buy in 2026: 10 Luxury Cars Compared`
- `What 1 Bitcoin Can Buy: Pokemon Cards Edition`
- `What 1 Bitcoin Can Buy: Football Cards Edition`
- `What 1 Bitcoin Can Buy: Baseball Cards Edition`
- `What 1 Bitcoin Can Buy: Basketball Cards Edition`
- `What 1 Bitcoin Can Buy: One Piece Cards Edition`

### Ghi chú chiến lược

Đây là hướng mở rộng hợp lý hơn nhiều so với:

- generic luxury content không gắn BTC
- generic card content không gắn BTC
- traffic play kiểu celebrity/networth quá xa crypto

Nói ngắn:

- nếu làm `luxury`, `cards`, `watches`, `real estate`
- thì nên làm dưới chiếc ô `What 1 Bitcoin Can Buy`
- không nên tách thành các hub lifestyle độc lập quá sớm

### Không nên làm

- bài generic kiểu chỉ nói về luxury cars mà không gắn BTC
- bài generic collectibles không có angle Bitcoin
- bài lifestyle không có quan hệ rõ với purchasing power của BTC

### File draft hiện có

- `coincu_what_1_bitcoin_can_buy_pillar_skeleton.md`
- `coincu_what_can_1_bitcoin_buy_pillar_draft.md`
- `coincu_bitcoin_luxury_cars_internal_link_map.md`

## 6. Ecosystem Hubs

### Vai trò

Đây là lớp build sau, dùng để gom toàn bộ content theo ecosystem thay vì theo content type.

### Parent hub đề xuất

- `/ecosystems/`

### Child hub nên ưu tiên

- `TON`
- `Sui`
- `Solana`
- `Base`

### Loại bài nên nằm trong ecosystem hub

- ecosystem overview
- best projects in ecosystem
- top wallets for ecosystem
- ecosystem-specific exchange or launchpad pages
- ecosystem token / protocol / guide pages

### Ví dụ

- `TON ecosystem overview`
- `Tonkeeper Wallet Review`
- `The Open Network Review`
- `TONUP review`
- `TON Place review`

## 7. Crypto Glossary

### Vai trò

Hub reference/evergreen dùng để đỡ toàn site và hỗ trợ internal link cho review, guide, on-chain explainer.

### Loại bài nên nằm trong glossary

- định nghĩa thuật ngữ crypto
- market structure terms
- DeFi terms
- wallet/security terms
- tokenomics terms

### Ghi chú

Hub này đã tồn tại công khai nhưng nên được tối ưu điều hướng lại thay vì làm mới từ đầu.

## 8. On-chain Movers / Why Is X Pumping

### Vai trò

Dùng để gom series bài tin ngắn kiểu biến động giá, catalyst, market structure, on-chain narrative.

### Loại bài nên nằm trong hub này

- `why is x pumping`
- `why is x surging`
- catalyst-driven market explainer
- short mover recap

### Ví dụ

- `Why is BUILDon pumping?`
- `Why is Humanity Protocol surging?`
- `Why is SKYAI pumping today?`

### Ghi chú

Chỉ nên build sau khi 4 hub nền đã ổn.

## Mapping nhanh: Hub nào gom loại bài nào

### Coin Reviews

- coin review
- token review
- meme coin review
- AI coin review
- tokenomics

### Protocol Reviews

- protocol review
- network review
- DeFi protocol
- AI protocol
- infrastructure protocol

### Exchange Reviews

- exchange review
- CEX / DEX comparison
- fees
- liquidity
- trading experience

### Wallet Reviews

- wallet review
- self-custody
- setup guide
- recovery guide
- ecosystem wallet picks

### What 1 Bitcoin Can Buy

- BTC purchasing-power pillar
- consumer comparison pages gắn BTC
- cars / cards / watches / real estate / luxury cluster
- evergreen comparison content có angle quy đổi 1 BTC
- topical bridge giữa crypto và consumer intent

### Ecosystem Hubs

- TON / Sui / Solana / Base clusters
- best projects
- ecosystem overview
- chain-specific wallet/protocol/project links

## File public-ready hiện có

- `coincu_coin_reviews_hubpage_public_ready.md`
- `coincu_protocol_reviews_hubpage_public_ready.md`
- `coincu_exchange_reviews_hubpage_public_ready.md`
- `coincu_wallet_reviews_hubpage_public_ready.md`

## File pillar / cluster hiện có

- `coincu_what_1_bitcoin_can_buy_pillar_skeleton.md`
- `coincu_what_can_1_bitcoin_buy_pillar_draft.md`
- `coincu_bitcoin_luxury_cars_internal_link_map.md`

## Kết luận thực dụng

Nếu Coincu chỉ làm đúng hướng trong giai đoạn này, nên coi 2 trục dưới đây là xương sống:

### Trục 1: Review authority

1. `Coin Reviews`
2. `Protocol Reviews`
3. `Exchange Reviews`
4. `Wallet Reviews`

### Trục 2: Consumer pillar mở rộng từ BTC

5. `What 1 Bitcoin Can Buy`

Sau đó mới mở rộng sang:

- `Ecosystem Hubs`
- `Crypto Glossary`
- `On-chain Movers`

Làm theo thứ tự này sẽ sạch topical authority hơn, đỡ loãng hơn, và dễ internal link hơn nhiều so với việc tiếp tục để mọi thứ nằm chung trong archive.
