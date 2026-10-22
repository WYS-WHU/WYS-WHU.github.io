---
name: "Yishan Wang Academic Homepage"
description: "A quiet scholarly profile with direct research records and intact scientific figures."
colors:
  ink: "#252c2e"
  muted: "#596366"
  accent: "#215e68"
  accent-hover: "#123f47"
  rule: "#dce3e3"
  soft: "#f3f7f7"
  paper: "#ffffff"
  review-ink: "#665523"
  resource-hover: "#e8f0f0"
typography:
  display:
    fontFamily: '"Source Serif 4", Georgia, serif'
    fontSize: "35px"
    fontWeight: 600
    lineHeight: 1.18
    letterSpacing: "-.025em"
  headline:
    fontFamily: '"Source Serif 4", Georgia, serif'
    fontSize: "28px"
    fontWeight: 600
    lineHeight: 1.24
    letterSpacing: "-.025em"
  title:
    fontFamily: '"Source Sans 3", "Segoe UI", sans-serif'
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1.4
  body:
    fontFamily: '"Source Sans 3", "Segoe UI", sans-serif'
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.62
  label:
    fontFamily: '"Source Sans 3", "Segoe UI", sans-serif'
    fontSize: "14px"
    fontWeight: 500
    lineHeight: 1.62
  profile-degree:
    fontFamily: '"Source Sans 3", "Segoe UI", sans-serif'
    fontSize: "14px"
    fontWeight: 500
    lineHeight: 1.62
  profile-university:
    fontFamily: '"Source Sans 3", "Segoe UI", sans-serif'
    fontSize: "16px"
    fontWeight: 600
    lineHeight: 1.62
  profile-school:
    fontFamily: '"Source Sans 3", "Segoe UI", sans-serif'
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.62
  profile-date:
    fontFamily: '"Source Sans 3", "Segoe UI", sans-serif'
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.62
rounded:
  focus: "2px"
  media: "3px"
  dialog: "5px"
spacing:
  section: "48px"
  section-mobile: "40px"
  heading-gap: "22px"
  record-padding: "20px"
  publication-padding: "24px"
components:
  resource-link:
    backgroundColor: "{colors.soft}"
    textColor: "{colors.accent}"
    rounded: "{rounded.media}"
    padding: "7px 12px"
  resource-link-hover:
    backgroundColor: "{colors.resource-hover}"
    textColor: "{colors.accent-hover}"
  navigation-link:
    textColor: "{colors.muted}"
    typography: "{typography.label}"
    padding: "25px 0 23px"
  navigation-link-current:
    textColor: "{colors.accent}"
  menu-toggle:
    textColor: "{colors.accent}"
    padding: "8px 0 8px 14px"
  dialog-close:
    textColor: "{colors.ink}"
    width: "44px"
    height: "44px"
  dialog-close-hover:
    backgroundColor: "{colors.soft}"
  publication-record:
    textColor: "{colors.ink}"
    padding: "24px 0"
  resource-container:
    padding: "24px 0"
  education-record:
    textColor: "{colors.ink}"
    padding: "20px 0"
  profile-bio:
    textColor: "{colors.muted}"
  section-heading:
    typography: "{typography.headline}"
  figure-dialog:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.dialog}"
    padding: "24px"
---

# Design System: Yishan Wang Academic Homepage

## Overview

**Creative North Star: "The Scholarly Profile"**

An understated, content-rich academic homepage, grounded in the user's selected scholarly references. White space, readable research records, a personal portrait, and direct links provide the visual identity. The built system is restrained and useful, with a compact identity rail beside an open reading column on larger screens.

Serif names and section headings establish hierarchy; sans-serif paragraphs and metadata keep the research record easy to scan. Original scientific figures are evidence to inspect, rather than decorative hero artwork. The English interface retains the supplied Chinese personal name as an identity detail.

**Key Characteristics:**

- White ground, dark readable text, restrained ocean-teal links.
- Serif identity and section headings; sans-serif research records.
- Fine rules and open rows rather than a repeated card grid.
- Supplied portrait and uncropped scientific diagrams.
- Mobile reading order with the profile above the research record.

Initially recorded from the local build and supplied desktop/mobile captures. This incremental revision follows the current `site/styles.css`, `scripts/build_site.py`, and `site/index.template.html`; the earlier ship disposition in `work/finish-review.md` describes the preceding reviewed snapshot. No new screenshot review or remote deployment is claimed by this revision. `PRODUCT.md` and `work/homepage-direction.md` remain the product and visual context.

## Colors

One muted teal accent sits on a white field; darker text and cool gray rules carry most of the page.

### Primary

- **Ocean Teal** (`accent`): links, the wordmark dot, publication venues, current navigation, and small date or status details.
- **Deep Ocean Teal** (`accent-hover`): interactive link hover.
- **Pale Teal Wash** (`resource-hover`): resource-link hover background.

### Secondary

- **Review Ochre** (`review-ink`): the explicit under-review publication status. This is a semantic exception, not a second decorative accent.

### Neutral

- **Charcoal Ink** (`ink`): primary text, names, and record titles.
- **Slate Gray** (`muted`): secondary metadata, dates, summaries, and default navigation.
- **Cool Rule** (`rule`): section and record separators.
- **Cool Figure Ground** (`soft`): publication figure wells, resource actions, and close-button hover.
- **White Paper** (`paper`): the page and modal ground.

**The Link Accent Rule.** Teal identifies navigation, links, and compact research metadata; the reading field stays white.

## Typography

**Display Font:** Source Serif 4, with Georgia and serif fallbacks.

**Body Font:** Source Sans 3, with Segoe UI and sans-serif fallbacks.

**Identity Detail:** KaiTi, STKaiti, Noto Serif CJK SC, and serif fallbacks for the Chinese personal name only. This is not the display face for interface headings.

**Character:** Scholarly serif headings give the page a personal, editorial cadence. The sans-serif text carries long paragraphs and dense bibliographic details without competing with the figures. Both Source families are self-hosted with `font-display: swap`.

### Hierarchy

- **Display:** the profile name uses the `display` token; it becomes 30px at widths up to 1000px.
- **Headline:** section headings use `headline`; mobile headings become 26px. The header wordmark is a compact 23px serif, becoming 21px on mobile.
- **Title:** publication titles use `title`, increasing to 18px at widths up to 1000px. Institution titles use 18px; the resource title uses 23px serif, becoming 22px on mobile.
- **Body:** the `body` token carries introductory paragraphs, capped at 74ch. Mobile body text is 16px. Resource prose is 16px with 1.65 line height and a 70ch maximum measure.
- **Label:** `label` describes desktop navigation. Publication authors, summaries, links, and venues use 14px, with line heights between 1.4 and 1.55; venues and the highlighted author use weight 600. Dates use 13px; the wrapping author-symbol legend and footer use 12px. There is no visible statistics-date annotation.
- **Affiliation hierarchy:** degree/status uses `profile-degree` (teal, weight 500), university uses `profile-university` (ink, weight 600), school uses `profile-school` (muted), and date uses `profile-date` (muted and italic). Current and incoming study use the same four-line hierarchy. Education records mirror the roles with an 18px institution title, muted 14px school, teal 15px degree/program at weight 500, and muted italic 13px date.
- **Numbers:** dates and resource counts use tabular numerals, without a distinct mono font.

**The Heading Pair Rule.** Serif type belongs to personal identity, section headings, and the resource title; research titles and metadata remain sans-serif.

## Layout

The desktop header has a 1208px maximum outer width, 32px horizontal padding, and a 76px minimum height. The main page has a 1152px maximum outer width, 32px horizontal padding, a 226px identity column, a flexible reading column, and a 72px gap. Its top padding and section rhythm use `section`; headings are separated from content by `heading-gap`.

The header sticks above 1000px. The profile sticks at 110px in that mode, but becomes static when the viewport height is 850px or less, keeping the rail reachable. At widths up to 1160px, the identity column is 210px and the gap is 45px; publication figures occupy 175px rather than 200px. At widths up to 1000px, the identity column becomes 190px with a 36px gap, the header becomes nonsticky, the section menu replaces the full navigation when JavaScript is available, and publication figures stack above their text. Navigation remains available without JavaScript.

At widths up to 720px, the page becomes a single reading column with 22px side padding and 30px top padding. The profile becomes a compact two-column block with a 120 × 151px portrait and identity text, followed by affiliation and contact information across the full width. Sidebar interests are hidden; interests remain in the introductory text. Section spacing uses `section-mobile`. Publication figures fill the column, record dates move above their text, and the footer stacks.

Desktop publication rows use a 200px figure column and a 25px gap, with `publication-padding` between records. Experience and education rows reserve 142px for a right-aligned date and use a 20px column gap. Honors use a small year column rather than badges. Print removes navigation and modal controls, uses a single flow, reduces the body to 10pt, and avoids splitting publication rows.

## Elevation & Depth

Page content is flat. Fine rules, whitespace, and pale figure wells provide separation without card shadows. The native figure dialog is the sole elevated surface, with a dark translucent backdrop and a diffuse shadow (`0 14px 70px #101a2440`). Its entrance is a 160ms scale-and-fade using `cubic-bezier(.16, 1, .3, 1)`, from scale .98 / opacity .65 to scale 1 / opacity 1. Reduced-motion preferences remove that animation. There is no general transition or animation system beyond this interaction.

**The Inspection Depth Rule.** Elevation supports enlarged figure inspection; ordinary research records stay flat.

## Shapes

The page uses mostly rectangular, unboxed content. Subtle corners soften the portrait, figure wells, and resource links through `media`; the dialog uses `dialog`, while focus styling and small zoom controls use `focus`. Rules are thin (1px), and the current navigation marker is a 2px bottom border. Inline icons are simple stroke SVGs rather than text glyph substitutes. Section headings pair their existing serif text with a 21px teal SVG using the same 1.6 stroke, round caps/joins, a 10px text gap, and a -1px vertical alignment. The icons are decorative (`aria-hidden="true"`); the text remains the section label.

The desktop portrait is 216 × 252px with `object-fit: cover` and a center 30% crop. Publication diagrams use `object-fit: contain` in pale wells so their scientific content is intact. These are deliberately different image treatments.

## Components

### Resource actions

Quiet filled links, not prominent call-to-action buttons. They use `resource-link` and its hover variant, inline SVG external-link indicators, and a 7px icon gap. Links wrap with 8px vertical and 12px horizontal gaps. Mobile actions have a 42px minimum height. Ordinary paper links remain underlined text; there is no filled primary-button family.

### Navigation and menu

Compact text navigation uses `navigation-link`. Hover and current-section states share teal text and a teal bottom border. The current item is exposed with `aria-current="location"`. The mobile “Sections” control is a transparent text-and-chevron button with a 44px minimum height, controlled through `aria-expanded`; Escape closes the menu and returns focus to it.

### Publication records

An open figure-and-text row with a fine bottom rule. The first and last records remove outer padding and the last rule. Each record presents a title, available authors, explicit venue/status, a short summary, and available links. The author's name uses weight 600. Confirmed equal-contribution authors receive a compact `*` superscript and confirmed corresponding authors receive `†`, with descriptive `title` attributes. The section legend reads “* Equal contribution · † Corresponding author” and wraps with the heading when needed. These are bibliographic symbols, not substitutes for interface icons. Under-review information is readable text, with review ochre as a supporting cue. Missing author rows, empty summaries and absent links are omitted. Accepted papers retain explicit Accepted text in the same teal treatment as published items; preprints retain their review state.

### Resource container

A flat full-width block bounded by top and bottom rules, with a serif title, the original project banner directly beneath it at its natural aspect ratio, short explanatory prose, compact inventory, resource actions, and a count line without a visible statistics-date note. Counts use normal text scale and tabular numerals. No raised card or giant statistic treatment appears here.

### Experience, education, and honors

The identity rail contains two concise biography sentences in muted 14px text, followed by a 16px location icon and Wuhan location. It has no separate education blocks or divider. Education records retain bold university names, muted school names, teal degrees/programs, and italic dates. Each education or research heading has its original university or laboratory logo at the left, contained in a 56px square (46px on mobile). Only surrounding white space of the official Tsinghua emblem asset is cropped by CSS. Education omits laboratory affiliation. Research retains linked labs and supervision. Honors retain the narrow year column.

### Section headings

Existing serif headings now include a small, thin-line SVG appropriate to the section: profile, paper, code, experience, education, honor, or music. The icon uses the existing teal accent and line language; heading type and reading hierarchy remain unchanged. The publication heading's author-symbol legend stays secondary at 12px and can wrap.

### Conference news

The concise conference news retains the 8/33 finalist statement and prize. There is no finalist-team disclosure or expanded list.

### Figure inspection

Figure previews are ordinary links to the original image. Supported browsers enhance them into a native modal dialog; the image remains contained, with a descriptive title, original-image link, close button, and backdrop. The dialog is at most 1220px wide with 32px viewport clearance per side, reduced to 12px on mobile. The close control is 44 × 44px and gains a pale hover background. Escape and outside-click dismissal restore focus to the initiating figure link. Preview snippets in the sidecar show static visual states only; site JavaScript owns modal and menu behavior.

### Focus and reading access

Links and buttons use a 2px teal `:focus-visible` outline with a 5px offset. A keyboard-visible skip link leads to the main reading region. Primary content is visible by default and the figure link works without the modal enhancement. The site has no input fields, filters, selectable chips, or form component family to document.

## Do's and Don'ts

### Do:

- **Do** keep the white reading field, restrained teal links, and fine rule separators.
- **Do** use the serif/sans-serif role split and the existing compact metadata hierarchy.
- **Do** preserve the supplied portrait and contain scientific diagrams without cropping their content.
- **Do** retain visible status text, direct links, keyboard focus, and reduced-motion behavior.
- **Do** let the identity rail and records reflow into the mobile reading order.

### Don't:

- **Don't** turn the academic reading page into a marketing hero or a repeated raised-card grid.
- **Don't** replace original figures with decorative artwork or oversize platform counts.
- **Don't** use color alone to distinguish publication or affiliation status.
- **Don't** substitute glyph characters for the existing SVG icon language.

Not canonized: this incremental source-based synchronization records no new screenshot or craft-review verdict. It does not extend the earlier review to the changed build. No implementation or public-content repairs were made in this documentation pass.
