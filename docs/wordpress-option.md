# WordPress Deployment Option

This landing is intentionally easy to port into WordPress later.

## Recommended order

1. Launch the first version as a static page.
2. Validate copy and conversion around `DIY Free`, `Pro Setup`, and `Managed`.
3. Move it into WordPress only if CMS workflows or marketing operations justify it.

## Why it ports cleanly

- flat semantic sections;
- no framework lock-in;
- clear hero, offers, FAQ, and CTA blocks;
- structured data that can be preserved in a template.

## Option A: custom page template

Best if you want full visual control.

Approach:

- create a minimal theme or child theme;
- move `index.html` sections into a page template;
- load `styles.css` as the landing stylesheet;
- keep structured data in the head or template partial.

## Option B: WP-CLI bootstrap

Best if you want to create the landing page from a deployment script.

Example:

```bash
wp post create \
  --post_type=page \
  --post_status=publish \
  --post_title="ClawStack" \
  --post_name="clawstack"
```

Then load the HTML into a template or a sanitized page-body pipeline.

## Option C: WordPress REST API

Best if the content is published from another system.

Example endpoint:

```text
POST /wp-json/wp/v2/pages
```

Recommended usage:

- send section content or sanitized HTML fragments;
- keep SEO fields managed by your SEO plugin or meta integration;
- preserve the same offer structure and FAQ content.

## Practical recommendation

Do not start with WordPress unless you already need:

- editor workflows;
- SEO plugin operations;
- marketing forms or content publishing;
- a broader CMS stack around the landing.

For the first release, static is faster and easier to control.
