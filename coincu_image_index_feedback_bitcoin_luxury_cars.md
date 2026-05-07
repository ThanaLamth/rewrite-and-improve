# Coincu Image Index Feedback

## URL Reviewed

- `https://coincu.com/what-1-bitcoin-can-buy-in-2026-10-luxury-cars-compared/`

## Summary

The page itself appears able to expose a primary image clearly enough, but several body images are implemented with placeholder-based lazy loading. That creates a higher risk that Google will crawl the page while discovering fewer article images for image indexing.

## Main Finding

### Featured image is relatively strong

The main article image has multiple supporting signals:

- `og:image`
- `twitter:image`
- `ImageObject` in schema
- descriptive caption
- a real `src` image in the article HTML

Primary image observed:

- `https://coincu.com/wp-content/uploads/2026/05/top-luxury-car-buy-bitcoin.png`

### Body images are weaker for indexing

Several important body images use a placeholder `src` and move the real image URL into lazy-load attributes such as:

- `data-lazy-src`
- `data-lazy-srcset`

Example pattern:

```html
<img
  src="data:image/svg+xml,..."
  data-lazy-src="https://coincu.com/wp-content/uploads/2026/05/image-36-1024x782.png"
  data-lazy-srcset="..."
>
```

That means Google may initially see a placeholder rather than the actual image URL in `src`.

## Evidence Found

### Stronger image

The hero image near the top of the article uses a real image URL in `src`:

- `top-luxury-car-buy-bitcoin-1024x575.png`

### Weaker images

These body images were observed using placeholder-based lazy loading:

- `bitcoin-luxury-cars-real-grid-capture.png`
- `image-36.png`
- `image-37.png`
- `image-38.png`
- `genesis-g90.png`

## Why These Images May Be Harder to Index

### 1. Placeholder-based lazy loading

Important article images should ideally expose the real image URL directly in `src`.

Safer pattern:

```html
<img src="real-image.jpg" loading="lazy">
```

Higher-risk pattern:

```html
<img src="placeholder" data-lazy-src="real-image.jpg">
```

### 2. Generic filenames

Some filenames are too generic:

- `image-36.png`
- `image-37.png`
- `image-38.png`

More descriptive filenames would create better semantic signals, for example:

- `bitcoin-luxury-cars-bmw-x5.png`
- `bitcoin-luxury-cars-mercedes-e450.png`
- `bitcoin-luxury-cars-volvo-ex90-threshold.png`

### 3. Screenshot-heavy visuals

Some article visuals are screenshots of official brand pages. Those may be less distinctive than custom charts, infographics, or original comparison visuals.

### 4. Many additional lazy-loaded images on the page

The page also contains related-post and listing thumbnails using the same lazy-load pattern, which may dilute the prominence of the article's key images.

## Recommended Fixes

### Must Fix Now

1. Render important in-article images with a real image URL in `src`.
2. Keep lazy loading only in the safer form:

```html
<img src="real-image.jpg" loading="lazy">
```

3. Update generic image filenames to descriptive filenames before upload.

### Good To Improve

1. Replace screenshot-style images with custom visuals where possible.
2. Keep strong `alt` text and `figcaption` for each important image.
3. Place each important image near the most relevant surrounding text.

### Nice To Have

1. Reduce the number of non-essential images in the article.
2. Reserve the strongest image treatment for the cover image and one or two core body visuals.

## Practical Priority For This Article

Prioritize fixes for:

1. `bitcoin-luxury-cars-real-grid-capture.png`
2. `image-36.png`
3. `image-37.png`
4. `image-38.png`
5. `genesis-g90.png`

The cover image is already in better shape than the rest of the article images.

## Conclusion

This article does not appear to have a complete image-indexing failure. The more specific issue is that the page's primary image is reasonably exposed, while many important body images are hidden behind placeholder-based lazy loading.

For Coincu, the highest-impact improvement is straightforward:

- expose the actual image URL in `src`
- keep lazy loading in a standards-friendly form
- use descriptive filenames
- rely more on original visuals than screenshots
