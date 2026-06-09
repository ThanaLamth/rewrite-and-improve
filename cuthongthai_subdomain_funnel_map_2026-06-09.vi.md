# Cuthongthai.vn Subdomain Funnel Map

Date: 2026-06-09
Domain: `https://cuthongthai.vn/`
Scope: root domain plus `vimo`, `thue`, `tamlinh`, `muanha`, `suckhoe`
Verdict: `house-of-products model with intent-specific subdomain funnels`

## Executive Summary

`cuthongthai.vn` is not behaving like a single content site that happens to have a few subdomains. It behaves more like an umbrella brand routing users into separate vertical products.

The core pattern is:

1. long-tail content or category pages capture search demand
2. article templates push users into vertical-specific tools
3. each subdomain keeps users inside a tighter navigation and brand context
4. footer and related-link modules cross-sell the rest of the ecosystem

This means the subdomain split is tied directly to UX, UI, and conversion design, not just technical SEO.

## Google Context

Official Google guidance does not say subdomains rank better than subfolders. However, Google does support site-level signals such as site names at the subdomain level, and Search Console can track either per-subdomain or at the full-domain level.

Relevant official references:

- Site names: `https://developers.google.com/search/docs/appearance/site-names`
- Search Console property types: `https://support.google.com/webmasters/answer/34592`
- AI features guidance: `https://developers.google.com/search/docs/appearance/ai-features`

Implication for this case:

- the split can help branding, measurement, and UX clarity
- it does not automatically help ranking
- it only works if each subdomain is strong enough to justify separate site treatment

## Funnel Table

| Subdomain | Primary query cluster | Main landing type | Main CTA pattern | Likely KPI | SEO upside | SEO downside |
| --- | --- | --- | --- | --- | --- | --- |
| `cuthongthai.vn` | brand and ecosystem queries | brand hub homepage | route users into verticals | click-through to product verticals | clear umbrella brand | weak topical focus if root tries to rank broadly |
| `vimo.cuthongthai.vn` | macro, stocks, BCTC, assets, live investment data | app-like homepage, dashboards, community pages | navigate to dashboard modules and community | active usage, repeat visits, premium/product expansion | strong site-level product identity | authority split from other finance content |
| `thue.cuthongthai.vn` | tax, TNCN, online selling tax, salary, family deductions | blog plus calculator hub | move readers from article to calculator | tool starts, tax workflow depth | strong intent alignment for tax queries | duplicates effort if root also keeps tax article versions |
| `muanha.cuthongthai.vn` | mortgage, home affordability, flip, ROI, land price | blog plus real-estate tools | move readers from article to home-buying tools | tool usage, lead-like high-intent sessions | clean property-investment topical silo | splits authority from finance/tax support content |
| `tamlinh.cuthongthai.vn` | van khan, xem ngay, tu vi, phong thuy, gieo que | blog, ritual library, divination tools | move readers from article to ritual or divination tools | repeat visits, session depth, tool usage | high intent clarity and strong library expansion | hard to share authority with commercial verticals |
| `suckhoe.cuthongthai.vn` | stress, lifestyle, summer health, nutrition | seasonal health blog and tools | content-first, then ecosystem/tool discovery | traffic acquisition, article depth, health tool usage | broad traffic capture potential | weakest visible tool funnel among sampled verticals |

## Subdomain Breakdown

### 1. `cuthongthai.vn`

Role:

- umbrella brand
- ecosystem router
- high-level navigation across verticals

Observed evidence:

- homepage title positions the site as a multi-vertical ecosystem
- homepage links directly to `dautu`, `muanha`, `os`, `suckhoe`, `tamlinh`, `thue`, and `vimo`

Interpretation:

- the root domain is not the main content silo
- it works as a distribution layer for the rest of the network

Evidence URLs:

- `https://cuthongthai.vn/`

### 2. `vimo.cuthongthai.vn`

Primary query cluster:

- macro data
- stock analysis
- BCTC
- asset tracking
- community signals

Landing and UX pattern:

- app shell, sticky navigation, mobile bottom nav, search, chat, cards, dashboards
- sections like `Vĩ Mô`, `Soi Kèo`, `BCTC`, `WarWatch`, `Quản Lý Tài Sản`, `Community`

Main CTA pattern:

- users are pulled deeper into modules, not just to another article
- strong product behavior instead of standard content-site behavior

Likely KPI:

- module visits
- repeat sessions
- product retention
- premium expansion

Why the subdomain matters here:

- this vertical feels like a standalone product
- subdomain-level site identity is coherent with the UX

Evidence URLs:

- `https://vimo.cuthongthai.vn/`
- `https://vimo.cuthongthai.vn/macro`
- `https://vimo.cuthongthai.vn/assets`
- `https://vimo.cuthongthai.vn/community`
- `https://vimo.cuthongthai.vn/terms-of-use`

### 3. `thue.cuthongthai.vn`

Primary query cluster:

- `thuế TNCN`
- `thu nhập vãng lai`
- `giảm trừ gia cảnh`
- `mã số thuế`
- `thuế bán online`

Landing and content pattern:

- article titles use strong curiosity and problem framing
- article body explains the issue, then injects tool links directly into key paragraphs
- FAQ and source sections increase depth and trust framing

Main CTA pattern:

- `Tính Thuế TNCN`
- `Giảm Trừ Gia Cảnh`
- `Thuế TMĐT`
- `Tính Lương Net`

Likely KPI:

- calculator starts
- tool-assisted tax sessions
- deeper workflow usage across multiple tax tools

Why the subdomain matters here:

- the reading context stays fully tax-specific
- users do not get mixed with unrelated spiritual or health navigation
- tool links feel natural because the full environment is about tax

Observed extra note:

- root-domain article versions redirect into the tax subdomain, suggesting a deliberate migration of topical ownership

Evidence URLs:

- `https://thue.cuthongthai.vn/finance/tax`
- `https://thue.cuthongthai.vn/blog`
- `https://thue.cuthongthai.vn/blog/thu-nhap-vang-lai-khi-nao-phai-dang-ky-ma-so-thue`
- `https://cuthongthai.vn/thu-nhap-vang-lai-khi-nao-phai-dang-ky-ma-so-thue/`

### 4. `muanha.cuthongthai.vn`

Primary query cluster:

- mortgage
- home affordability
- house flipping
- land valuation
- ROI for property
- legal and planning checks

Landing and content pattern:

- blog headlines are high-curiosity and high-stakes
- article body ties every key decision point to a specific calculator or evaluation tool
- real-estate cases are used to bridge narrative content into tools

Main CTA pattern:

- `Tra Cứu Giá Đất`
- `Flip BĐS`
- `ROI Đầu Tư`
- `Khả Năng Mua`
- `Tính Trả Góp`

Likely KPI:

- high-intent tool starts
- property decision support sessions
- possible lead-like behavior for later monetization

Why the subdomain matters here:

- one user problem cluster stays together: affordability, valuation, ROI, rates, and legal prep
- article-to-tool motion is much cleaner than on a mixed-domain architecture

Observed extra note:

- root-domain article versions redirect into the home-buying subdomain

Evidence URLs:

- `https://muanha.cuthongthai.vn/`
- `https://muanha.cuthongthai.vn/blog`
- `https://muanha.cuthongthai.vn/cong-cu/kha-nang-mua`
- `https://muanha.cuthongthai.vn/blog/98-nguoi-bo-qua-ho-bien-nha-cu-hien-dai-ban-gia-cao`
- `https://cuthongthai.vn/98-nguoi-bo-qua-ho-bien-nha-cu-hien-dai-ban-gia-cao/`

### 5. `tamlinh.cuthongthai.vn`

Primary query cluster:

- `văn khấn`
- `xem ngày`
- `tử vi`
- `gieo quẻ`
- `phong thủy`

Landing and content pattern:

- blog posts frame emotional or fate-related problems
- the body pushes directly into ritual, divination, and calendar tools
- a very large `văn khấn` library expands indexable long-tail coverage

Main CTA pattern:

- `Văn Khấn`
- `La Bàn Phong Thủy`
- `Xem Ngày Tốt Xấu`
- `Tử Vi`
- `Gieo Quẻ Online`

Likely KPI:

- repeat visits
- session depth
- multi-tool engagement

Why the subdomain matters here:

- ritual and divination queries benefit from one consistent thematic environment
- users can move from content to library to tool without breaking context

Observed extra note:

- this is one of the strongest examples where the subdomain acts like a complete intent silo

Evidence URLs:

- `https://tamlinh.cuthongthai.vn/`
- `https://tamlinh.cuthongthai.vn/van-khan`
- `https://tamlinh.cuthongthai.vn/blog`
- `https://tamlinh.cuthongthai.vn/blog/7-bi-quyet-giup-tuoi-ngo-hoa-giai-tieu-nhan-thang-6-vung-tam-an-nhien`

### 6. `suckhoe.cuthongthai.vn`

Primary query cluster:

- summer health
- stress
- lifestyle
- nutrition
- family health

Landing and content pattern:

- blog-first structure
- seasonal and curiosity-driven headlines
- broader informational tone than the sharper tool-first verticals

Main CTA pattern:

- weaker tool surfacing in the sampled pages
- more cross-links to the ecosystem than obvious in-article conversion to one dominant tool

Likely KPI:

- traffic acquisition
- article depth
- eventual tool discovery

Why the subdomain matters here:

- it separates broad health content from finance and spirituality
- this may help editorial clarity, even if the product funnel is less mature

Evidence URLs:

- `https://suckhoe.cuthongthai.vn/`
- `https://suckhoe.cuthongthai.vn/blog`
- `https://suckhoe.cuthongthai.vn/blog/su-that-ngo-doc-thuc-pham-mua-nang-nong-den-tu-nhung-sai-lam-nho`

## Shared UX and Content Traits

These traits repeat across the verticals:

- dark UI theme with vertical-specific accents
- author persona naming per vertical
- strong problem-aware, curiosity-heavy article titles
- article template with FAQ, sources, related content, and share buttons
- footer-level cross-links across the ecosystem
- in-article links to vertical-specific tools

This confirms that the site is using a repeatable `content -> tool -> ecosystem` funnel model.

## Strongest Strategic Benefits

### 1. Cleaner intent environments

Each subdomain preserves a tight problem space:

- tax users stay inside tax
- home-buying users stay inside real-estate calculations
- spiritual users stay inside ritual and divination

### 2. Better CTA relevance

The most important benefit is not ranking. It is that every article can send users into a highly relevant tool without looking out of place.

### 3. More coherent site-level branding

Google supports site names at the subdomain level. This model lets `Vimo`, `Cú Tiên Sinh`, and the other verticals act more like independent products.

### 4. Easier product packaging

The site can present each vertical as its own mini-product, with its own navigation, UX, and possible monetization path.

## Main Risks

### 1. Authority fragmentation

Subdomains do not automatically share ranking strength like one tightly integrated subfolder architecture might.

### 2. Duplicate or overlapping content flows

Some root-domain article URLs still exist or redirect into subdomains, which suggests migration or overlap. This can be manageable, but only if consolidation rules stay clean.

### 3. Template reuse can blur brand separation

The article framework is very similar across verticals. The funnel logic is strong, but the distinctiveness of each product could be undermined if every page feels structurally identical.

### 4. Cross-linking is a semi-silo, not a pure silo

The ecosystem footer cross-links nearly everything. This helps discovery, but it also weakens the purity of each vertical as a tightly bounded topical cluster.

## Conclusion

The subdomain split is strongly connected to the site's content and UX strategy.

This is the operating model:

- `root domain` = umbrella brand and router
- `subdomain` = intent silo
- `blog` = traffic acquisition
- `tool` = activation
- `cross-links` = ecosystem expansion and retention

If judged only as traditional SEO architecture, the model has consolidation tradeoffs.

If judged as a productized search acquisition system, the model is coherent and deliberate.
