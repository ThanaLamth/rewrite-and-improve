# Google-Official-Informed Hub Page Template

Last updated: 2026-05-05

## Important note

Google does not publish a special "hub page" specification or ranking factor.

This template is an inferred best-practice layout based on official Google Search Central guidance about:

- people-first content
- clear site focus
- crawlable internal links
- title and heading clarity
- breadcrumb hierarchy

Official sources:

- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://developers.google.com/search/docs/fundamentals/how-search-works
- https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- https://developers.google.com/search/docs/appearance/title-link
- https://developers.google.com/search/docs/appearance/structured-data/breadcrumb

---

# Template

## 1. SEO title

Keep it descriptive, concise, and specific to the hub.

**Formula**

`[Topic] Hub: [Primary value] | [Brand]`

**Example**

`Coin Reviews: Tokenomics, Risks, and Best Crypto Coins Explained | Coincu`

## 2. Meta description

Summarize who the page is for, what the page covers, and why it is useful.

**Formula**

`Explore [topic] with [coverage type 1], [coverage type 2], and [coverage type 3] for [target audience or use case].`

**Example**

`Explore Coincu's coin reviews covering tokenomics, use cases, catalysts, and risks across major crypto coins and emerging tokens.`

## 3. Breadcrumb

Use a breadcrumb that reflects a real user path, not just the raw URL structure.

**Example**

`Home > Reviews > Coin Reviews`

## 4. Main H1

Use one clear visible H1 that matches the page's real purpose.

**Example**

`Coin Reviews`

## 5. Opening section

This is the most important editorial block on the page.

It should answer:

- what this hub is about
- who it is for
- what problem it helps solve
- what makes this page worth reading instead of bouncing to a single article

**Template**

`[Topic] moves fast, but most readers do not need more noise. They need a reliable place to understand the subject, compare important angles, and find the right next page. This hub brings together [content type A], [content type B], and [content type C] so readers can move from overview to detail without losing context.`

## 6. Featured content block

Show the most important evergreen or cornerstone pages first.

Each item should include:

- article title
- one-sentence summary
- why it matters
- link

**Template**

### [Featured page title]

`[1-2 sentence summary of what the page helps the reader understand.]`

`Read more: [URL]`

## 7. Browse by category

This helps both users and Google understand page relationships.

Only create sections that reflect real intent splits.

**Template**

### [Category name]

`[Short explanation of why this category exists and who should use it.]`

Read next:

- `[Live URL 1]`
- `[Live URL 2]`
- `[Live URL 3]`

Coming soon:

- `[Planned cornerstone page 1]`
- `[Planned cornerstone page 2]`

## 8. Methodology or evaluation framework

For review or comparison hubs, this section adds credibility and helps satisfy people-first expectations.

**Template**

## How We Evaluate [Topic]

`We focus on the factors that matter most to readers trying to understand [topic]. Depending on the subject, that may include [factor 1], [factor 2], [factor 3], and [factor 4].`

### 1. [Factor name]

`[Short explanation]`

### 2. [Factor name]

`[Short explanation]`

### 3. [Factor name]

`[Short explanation]`

## 9. Best next pages to build

This section is optional for public pages, but useful if the hub is still growing and you want a soft editorial CTA.

**Template**

## Best [Topic] Pages to Read Next

### [Planned page title]

`[Why this page matters to the reader and how it fits the hub.]`

## 10. Related hubs

Use this block to connect the hub into the wider site structure.

**Template**

## Related Hubs

- `[Related hub 1]`
- `[Related hub 2]`
- `[Related hub 3]`

`These pages help readers move from [current topic] into adjacent subjects without starting over.`

## 11. FAQ

Add only questions that serve reader intent, not filler.

**Template**

## FAQ

### What is the difference between [A] and [B]?

`[Answer]`

### Who should use this hub?

`[Answer]`

### What should I read first?

`[Answer]`

## 12. Closing CTA

End with a useful next step, not a generic marketing line.

**Template**

`If you are starting your research, begin with the featured pages above. If you already know what angle you care about, jump into the category that best matches your goal.`

---

# Minimal Page Skeleton

You can use this as a clean starting point for almost any hub.

```md
SEO title: [Topic Hub: Primary Value | Brand]
Meta description: [One-sentence summary]
Breadcrumb: Home > [Parent] > [Hub]

# [Hub Title / H1]

[Opening section: what this page is, who it helps, and what it covers]

## Featured [Topic] Pages

### [Page 1]
[Short summary]
Read more: [URL]

### [Page 2]
[Short summary]
Read more: [URL]

## Browse by Category

### [Category 1]
[Short explanation]
- [URL]
- [URL]

### [Category 2]
[Short explanation]
- [URL]
- [URL]

## How We Evaluate [Topic]

### 1. [Criterion]
[Explanation]

### 2. [Criterion]
[Explanation]

### 3. [Criterion]
[Explanation]

## Related Hubs

- [Hub URL]
- [Hub URL]

## FAQ

### [Question]
[Answer]

### [Question]
[Answer]

[Closing CTA]
```

---

# What to avoid

Based on official Google guidance, avoid these patterns:

- turning the hub into a thin archive with no editorial value
- stuffing the title with repeated keywords
- mixing too many unrelated topics on one hub
- hiding important links behind non-crawlable JavaScript patterns
- creating a page mainly to capture search traffic without helping a real audience
- giving the page multiple competing H1-like headings with equal visual prominence

---

# Quick checklist before publishing

- One clear H1
- Descriptive `<title>`
- Helpful intro written for people first
- Crawlable `<a href>` links to child pages
- Logical category sections
- Breadcrumbs that reflect real hierarchy
- Featured evergreen pages, not only fresh news
- FAQ only if useful
- No empty or placeholder-heavy sections
