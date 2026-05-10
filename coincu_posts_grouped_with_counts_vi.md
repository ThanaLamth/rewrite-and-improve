# Coincu: Nhóm Bài Viết Kèm Số Lượng

Last updated: 2026-05-10

## Tổng quan

Nguồn dựa trên inventory đã parse từ bộ export Coincu trước đó.

- Tổng số post unique: `1484`
- Trạng thái `publish`: `1448`
- Trạng thái `draft`: `26`
- Trạng thái `private`: `6`
- Trạng thái `pending`: `4`

## Nhóm theo cluster chính

### 1. General Crypto Content

- Số lượng: `612`
- Trạng thái: `603 publish`, `5 draft`, `3 private`, `1 pending`
- Hướng xử lý: `selective_keep`
- Đây là bucket lớn nhất, nhưng rất rộng. Không nên coi đây là một hub riêng. Cần tách dần vào các hub phù hợp hơn như `Protocol Reviews`, `Coin Reviews`, `On-chain Movers`, `Crypto Glossary`, `Ecosystem Hubs`.

Ví dụ:

- `"Pig Butchering" New Crypto Scams Delivered "Massive Losses" to Victims`
- `A Compilation Of 5 DeFi Option Protocols Worth Noting`
- `A Comprehensive Analysis Of Lido V2: A Further Shift To Decentralization`

### 2. Listicles / Roundups

- Số lượng: `265`
- Trạng thái: `263 publish`, `2 pending`
- Hướng xử lý: `merge_or_selective_keep`
- Đây là nhóm listicle lớn, nhưng chất lượng intent không đồng đều. Chỉ nên giữ các bài thật sự hỗ trợ topical cluster hoặc có thể đưa về pillar/hub phù hợp.

Ví dụ:

- `2024 Cryptocurrency Market Outlook: Top 5 Emerging Themes To Watch Out`
- `3 Features of Crypto That Traditional Finance Lacks`
- `30-50X Meme Coin List! (That Potentially Work)`

### 3. Protocol / Ecosystem Reviews

- Số lượng: `179`
- Trạng thái: `177 publish`, `2 draft`
- Hướng xử lý: `keep`
- Đây là một trong những bucket mạnh nhất để build authority dài hạn.
- Đây là nguồn bài chính cho hub `Protocol Reviews`.

Ví dụ:

- `Aave Reviews: Earn Interest, Borrow Assets, And Build Applications?`
- `Agility Protocol Review: Potential Platform To Solve LSD Liquidity Challenge`
- `Alchemix Review: Pioneering A Revolution In DeFi With Multi-Chain Stability`
- `Aleo Review: Top Blockchain Projects Applying ZKP Technology Are Expected`

### 4. Exchange Reviews

- Số lượng: `117`
- Trạng thái: `117 publish`
- Hướng xử lý: `keep`
- Đây là bucket sạch nhất và rõ intent nhất.
- Đây là nguồn bài chính cho hub `Exchange Reviews`.

Ví dụ:

- `Bitfinex Review`
- `KuCoin Review`
- `Coincheck Review`
- `CoinW Review`
- `Binance Review`

### 5. Wallet Reviews

- Số lượng: `83`
- Trạng thái: `82 publish`, `1 pending`
- Hướng xử lý: `keep`
- Đây là bucket rất hợp để build hub riêng vì intent tách biệt rõ với exchange và protocol.
- Đây là nguồn bài chính cho hub `Wallet Reviews`.

Ví dụ:

- `Tonkeeper Wallet Review`
- `Rabby Wallet Review`
- `Argent Wallet Review`
- `How to Create and Use TON Wallets`

### 6. Coin / Project Reviews

- Số lượng: `68`
- Trạng thái: `68 publish`
- Hướng xử lý: `keep`
- Đây là nguồn bài chính cho hub `Coin Reviews`.
- Nên ưu tiên gom các bài token-level, coin thesis, meme coin, AI coin, legacy coin vào đây.

Ví dụ:

- `Ankr Review: Making Web3 Grow Stronger`
- `Bittensor Review: Machine Intelligence's Future Unveiled?`
- `BUILDon (B) Review 2026`
- `Ethena Review`

### 7. Net Worth / Celebrity

- Số lượng: `62`
- Trạng thái: `44 publish`, `17 draft`, `1 private`
- Hướng xử lý: `deprioritize`
- Đây là bucket lệch topical authority rõ nhất với hướng Coincu nên theo.
- Nếu có bài nào giữ lại thì chỉ nên là các trường hợp thật sự liên quan mạnh tới crypto figure.

Ví dụ:

- `Akon Net Worth`
- `Andre Hakkak Net Worth`
- `Balaji Srinivasan Net Worth`

### 8. Casino / Gambling

- Số lượng: `39`
- Trạng thái: `38 publish`, `1 private`
- Hướng xử lý: `deprioritize`
- Đây là vertical riêng, không nên coi là trọng tâm nếu mục tiêu là làm Coincu mạnh theo crypto research / review / guide.

Ví dụ:

- `1xBit – Growing Popularity of Crypto Casinos`
- `BC.GAME Crypto Casino Launches New Website With Better Features`
- `Best Telegram Casinos You Need To Know`

### 9. Company / Service Reviews

- Số lượng: `29`
- Trạng thái: `27 publish`, `1 draft`, `1 private`
- Hướng xử lý: `selective_keep`
- Nhóm này không nên gom thô thành một hub lớn ngay. Chỉ chọn những bài thật sự bổ trợ cho review ecosystem hoặc market infrastructure.

Ví dụ:

- `a16z Review`
- `Animoca Brands Review`
- `Binance Labs Review`

### 10. GameFi

- Số lượng: `19`
- Trạng thái: `18 publish`, `1 draft`
- Hướng xử lý: `merge_or_selective_keep`
- Đây là sub-cluster có thể gắn vào `Coin Reviews`, `Protocol Reviews`, hoặc `Ecosystem Hubs` tùy bài.

Ví dụ:

- `Apeiron Review`
- `Big Time Review`
- `Catizen Review`

### 11. Price Predictions

- Số lượng: `11`
- Trạng thái: `11 publish`
- Hướng xử lý: `deprioritize`
- Đây là nhóm trust-sensitive và không nên coi là trụ cột authority.

Ví dụ:

- `Bitcoin Price Prediction For 2024, 2025, 2026 and 2030`
- `DOGS Listing Price Prediction`

## Nhóm theo hub đang build

Đây là cách map lại inventory vào các hub chiến lược chính của Coincu.

### Coin Reviews

- Số bài mapped sạch: `55` trong `coincu_hub_candidates.csv`
- Bucket nguồn chính: `Coin / Project Reviews` (`68`)
- Loại bài:
  - coin review
  - token explainer
  - meme coin review
  - AI coin review
  - legacy/recovery coin page

### Protocol Reviews

- Số bài mapped sạch: `169`
- Bucket nguồn chính: `Protocol / Ecosystem Reviews` (`179`)
- Loại bài:
  - protocol review
  - network review
  - DeFi protocol review
  - AI protocol review
  - infrastructure/storage protocol review

### Exchange Reviews

- Số bài mapped sạch: `117`
- Bucket nguồn chính: `Exchange Reviews` (`117`)
- Loại bài:
  - CEX review
  - DEX review
  - beginner exchange review
  - derivatives exchange review
  - regional/specialized exchange review

### Wallet Reviews

- Số bài nguồn phù hợp: `83`
- Bucket nguồn chính: `Wallet Reviews` (`83`)
- Loại bài:
  - wallet review
  - setup guide
  - recovery guide
  - ecosystem-specific wallet page
  - security/self-custody page

## Nhóm theo hướng xử lý chiến lược

### Keep

- `447` bài
- Bao gồm các cluster mạnh nhất:
  - `Protocol / Ecosystem Reviews`
  - `Exchange Reviews`
  - `Wallet Reviews`
  - `Coin / Project Reviews`

### Selective Keep

- `641` bài
- Chủ yếu là:
  - `General Crypto Content`
  - `Company / Service Reviews`
- Cần chọn lại để bơm vào hub phù hợp thay vì giữ dạng archive tạp.

### Merge or Selective Keep

- `284` bài
- Chủ yếu là:
  - `Listicles / Roundups`
  - `GameFi`
- Chỉ nên giữ nếu hỗ trợ rõ cho cluster hoặc pillar.

### Deprioritize

- `112` bài
- Chủ yếu là:
  - `Net Worth / Celebrity`
  - `Casino / Gambling`
  - `Price Predictions`

## Nhóm content nên đẩy mạnh trước

### Trụ cột authority

1. `Protocol / Ecosystem Reviews` - `179`
2. `Exchange Reviews` - `117`
3. `Wallet Reviews` - `83`
4. `Coin / Project Reviews` - `68`

### Trụ cột mở rộng có chọn lọc

5. `General Crypto Content` - chọn lọc từ `612`
6. `Listicles / Roundups` - chọn lọc từ `265`

### Trụ cột nên hạ ưu tiên

7. `Net Worth / Celebrity` - `62`
8. `Casino / Gambling` - `39`
9. `Price Predictions` - `11`

## Dự án pillar riêng: What 1 Bitcoin Can Buy

Nhóm này không xuất phát từ một cluster export lớn sẵn có như các hub review ở trên. Đây là một trục build riêng theo hướng:

- `1 BTC mua được gì`

Loại bài nằm trong trục này:

- pillar gốc `What 1 Bitcoin Can Buy`
- cars edition
- cards edition
- watches edition
- luxury goods edition
- real estate edition

Các file draft đang có:

- `coincu_what_1_bitcoin_can_buy_pillar_skeleton.md`
- `coincu_what_can_1_bitcoin_buy_pillar_draft.md`
- `coincu_bitcoin_luxury_cars_internal_link_map.md`

## Kết luận thực dụng

Nếu nhìn toàn bộ inventory Coincu theo hướng build hub, có thể chia ra 3 lớp:

### Lớp 1: Hub nên build ngay

- `Coin Reviews`
- `Protocol Reviews`
- `Exchange Reviews`
- `Wallet Reviews`

### Lớp 2: Content pool để chọn lọc đưa vào hub

- `General Crypto Content`
- `Listicles / Roundups`
- `GameFi`
- `Company / Service Reviews`

### Lớp 3: Bucket nên giảm ưu tiên

- `Net Worth / Celebrity`
- `Casino / Gambling`
- `Price Predictions`

Điểm quan trọng nhất là:

- Coincu đã có đủ lượng bài để dựng 4 hub review cốt lõi ngay
- phần còn lại nên được chọn lọc lại để hỗ trợ hub, không nên tiếp tục để ở dạng archive loãng
