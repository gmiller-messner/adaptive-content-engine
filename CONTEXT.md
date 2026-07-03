# Adaptive Content Engine — Project Context

A technical reference for interviews and portfolio conversations.

---

## What It Does

The Adaptive Content Engine takes a single source document and generates meaningfully different lessons from it depending on who's reading. A lesson for a software developer covers implementation details, specific tools, and code-level defenses. The same source material for an engineering manager becomes a lesson about organizational risk, team exposure, and the right questions to ask. The same content, restructured for the reader's actual context.

The driving insight: adaptive learning isn't about simplifying content for some learners and complicating it for others. It's about connecting the same underlying concepts to different prior knowledge, different job responsibilities, and different threat models.

---

## Pipeline Architecture

The engine is structured as a staged pipeline. Each stage is independently runnable, which makes it easier to iterate on one stage without touching the others.

```
Source Document + Persona Profile
         ↓
    Stage 3: Lesson Generation     ← Claude Opus 4.8 (adaptive thinking)
         ↓
    Stage 4: Rendering             ← Tag processing + Jekyll/GitHub Pages
         ↓
    Delivered as a GitHub Pages site
```

Stages 1 (document ingestion) and 2 (persona parsing) are planned but not yet built — the current pipeline takes already-structured source documents and persona profiles as inputs.

The entry point is `run.py` at the project root, which accepts `generate`, `render`, or `all` as commands.

---

## Stage 3: Lesson Generation

### How It Works

The generator calls the Anthropic API with three types of inputs assembled into a structured prompt:

1. **Source document** — the subject matter to teach from
2. **Persona profile** — who the learner is: their role, technical level, existing knowledge, tools they use, and their specific risk exposure
3. **Supporting inputs** — style standards, learning objectives, and an examples bank of real-world incidents the model can draw from

These are assembled into a user message with XML-tagged blocks (`<source_document>`, `<persona_profile>`, `<examples_bank>`, etc.) to give the model clear structure over what each piece of content is.

### Model and Configuration

- **Model**: Claude Opus 4.8
- **Thinking**: Adaptive thinking mode (`"type": "adaptive"`) — the model decides how much reasoning to apply based on the complexity of the task
- **Max tokens**: 16,000 — set high to prevent lesson truncation on longer source material
- **Streaming**: Lessons stream to the terminal as they generate, then save to `outputs/` with a timestamped filename

### Prompt Design

The system prompt establishes the instructional designer role and specifies the structural expectations for the lesson: an introduction that connects to the learner's context, concepts at the right technical depth, examples drawn from the learner's actual tools, and actionable takeaways.

The system prompt deliberately does not over-specify the lesson format — structural tags (attack model cards, term callouts, image placeholders) are specified in the style standards input rather than the system prompt, which keeps the system prompt stable while allowing style iteration.

### Learning Objectives (Adaptive)

Each content set has a hand-authored `learning_objectives.md` holding **generic, topic-level** objectives — the outcomes for the subject, independent of any persona. The engine adapts them to each learner rather than relying on hand-authored per-persona sections.

This adaptation is an explicit pre-step in generation (a two-call design). Before the lesson is written, `adapt_objectives()` makes a lightweight call (Claude Sonnet 4.6, kept in a separate `ADAPT_MODEL` constant so it can be tuned independently of the Opus lesson model) that takes the generic objectives plus the persona profile and rewrites them into objectives specific to that learner's role, tools, and risk exposure. The adapted objectives are:

1. **Saved as an artifact** — `outputs/<set>/objectives_<persona>_<timestamp>.md`, sharing the timestamp of the lesson it belongs to, so the adaptation is inspectable and reusable rather than hidden inside the lesson.
2. **Fed into the lesson call** — the `<learning_objectives>` block passed to the Opus generation contains the *adapted* objectives, not the generic ones.

This was chosen over an implicit single-call approach (where the model would adapt objectives silently while writing the lesson) so the adaptation is a visible, demonstrable stage. It also removes a redundancy in the earlier design, where the full objectives file — including every other persona's sections — was passed on every run. If a set has no `learning_objectives.md`, the adaptation step is skipped entirely.

### Style Standards

The style standards input (`inputs/style_standards.md`) was developed iteratively based on reviewing actual lesson output. Key standards:

- **Soften presumptive language** — "if you're using X" rather than assuming the learner's stack
- **Avoid LLM writing tics** — an explicit avoid list (rhetorical section transitions, urgency mandates, "it's worth noting")
- **Heading conventions** — short and scannable, no more than 6–7 words
- **Technical depth** — for technical personas, every defense must include at least one concrete implementation example with named tools (e.g. BeautifulSoup, LangSmith, Dependabot) rather than abstract descriptions
- **Part structure** — each lesson uses `## Part N:` headings as top-level dividers, with `###` subsections underneath; no Part should exceed 4–5 subsections

### Structured Tags

The model outputs lessons with custom tags at identified locations, which the renderer later processes:

| Tag | Purpose |
|---|---|
| `[TERM: term — definition]` | Inline term callout for specialized vocabulary on first use |
| `[ATTACK MODEL CARD: Name]...[/ATTACK MODEL CARD]` | Structured card for attack vectors with Vector, Mechanism, Example, Risk level, Who's at risk |
| `[IMAGE: description]` | Image placeholder at recommended visual insertion points |
| `[TAKEAWAYS]...[/TAKEAWAYS]` | Structured key takeaways block at lesson end |

These tags let the model produce content in a structured format that is still readable as plain text, while giving the renderer clear hooks for visual treatment.

---

## Stage 4: Rendering

### The Hybrid Approach

The renderer converts tagged lesson markdown into GitHub Pages-compatible markdown. Rather than converting everything to HTML, it uses a hybrid approach:

- **Prose content** (paragraphs, headings, lists) stays as markdown — kramdown handles it
- **Structured blocks** (attack cards, term callouts, image placeholders, takeaways, nav) are converted to pure HTML

This approach was chosen because kramdown's markdown rendering is good for prose but offers no styling hooks for custom components. The HTML blocks get styled via custom SCSS.

An early approach used kramdown's `parse_block_html: true` setting to allow markdown inside HTML blocks. This was removed after it caused recurring issues (closing tags rendering as visible text, paragraph wrappers breaking flex layouts). All structured blocks now output pure HTML, with a custom `md_to_html_inline()` function handling bold, italic, and code formatting inside card content.

### Tag Processing

`renderer.py` processes each tag type with a regex replacement:

- **Attack model cards**: Parsed into a `<div class="attack-card">` with a `data-name` attribute; field lines converted to `<p><strong>Label:</strong> value</p>` blocks
- **Term callouts**: Converted to `<span class="term-callout">` with an inline `<span class="term-badge">TERM</span>` badge
- **Image placeholders**: Converted to `<div class="image-placeholder" data-caption="..."></div>`; caption stored as a data attribute to avoid nested div issues
- **Takeaways**: Converted to a `<div class="takeaways">` with an unordered list; list items run through `md_to_html_inline()` for inline formatting

### Pagination

Each lesson is split into multiple pages at `## Part` heading boundaries. The intro content (before the first Part heading) becomes `index.md`; each Part becomes `part-N.md`. This keeps individual pages to a readable length and produces a navigable hierarchy in Just the Docs.

Pages get Jekyll front matter injected at render time:
- Index pages get `has_children: true` and `parent: Lessons`
- Part pages get `nav_order`, `parent` (the lesson title), and `grand_parent: Lessons`

### Navigation

Each page gets a prev/next nav bar rendered as a `<div class="lesson-nav">` with anchor links. URL generation accounts for the directory structure difference between the index page and part pages — the index page uses relative paths like `part-1/`, while part pages use `../part-2/` to navigate between siblings.

A key lesson from this: `permalink: pretty` must be set in `_config.yml` for Jekyll to generate directory-style URLs (`/part-1/` rather than `/part-1.html`). Without it, nav links 404.

### GitHub Pages Delivery

The rendered output goes into `docs/lessons/` and is served via GitHub Pages using the Just the Docs theme. The `docs/_config.yml` configures:

- `permalink: pretty` — directory-style URLs
- `url` and `baseurl` — required for correct absolute URL generation on a project site
- No `parse_block_html` — removed after causing kramdown parsing issues

---

## Design System

The site uses a custom SCSS layer (`docs/_sass/custom/custom.scss`) on top of Just the Docs. All component colors are defined as CSS custom properties with explicit values for light and dark mode:

```scss
:root {
  --attack-card-bg: #fad5d5;   /* light mode */
}

[data-theme="dark"] {
  --attack-card-bg: #6b3030;   /* dark mode — elevated, not just tinted */
}
```

Dark mode card backgrounds are chosen for luminance elevation (~1.5:1 contrast against the page background), not just hue tinting. Earlier iterations used `rgba()` transparency, which was abandoned because both the card and page background have low absolute luminance in dark mode, making the tint imperceptible.

### Dark/Light Toggle

A JavaScript toggle (`docs/assets/js/theme-toggle.js`) handles theme switching:

1. An inline script in `_includes/head_custom.html` reads `localStorage` and sets `data-theme` on `<html>` before the page renders — preventing a flash of the wrong theme on load
2. The toggle button calls both `jtd.setTheme()` (for Just the Docs' own chrome) and updates `data-theme` (for custom component variables)
3. The preference persists in `localStorage` under the key `ace-theme`

---

## Key Technical Decisions

**Why a separate, cheaper model for objective adaptation?** The objectives pre-step is a bounded rewriting task, not the open-ended synthesis the lesson itself requires. Running it on Sonnet 4.6 (via the `ADAPT_MODEL` constant) keeps it fast and inexpensive while reserving Opus for the lesson, where the reasoning actually pays off.

**Why Claude Opus with adaptive thinking?** Lesson generation involves synthesizing a source document against a detailed persona — understanding what to include, what to skip, what framing fits the reader's mental model. Adaptive thinking lets the model reason through those choices without the overhead of extended thinking on every generation.

**Why a custom tag system instead of prompting for HTML directly?** Tags keep the model's output human-readable and editable. A lesson with `[TERM: SBOM — Software Bill of Materials]` inline is easy to review and edit. A lesson with raw HTML spans is not.

**Why Jekyll/GitHub Pages instead of a more dynamic stack?** The output is static educational content. A static site generator is appropriate — no database, no server, no auth. GitHub Pages provides free hosting with automated deployment on push.

**Why CSS custom properties for theming instead of separate stylesheets?** One stylesheet with variable overrides is easier to maintain than two parallel stylesheets. The `[data-theme]` attribute approach also supports a runtime toggle without a page reload, which separate compiled stylesheets don't.
