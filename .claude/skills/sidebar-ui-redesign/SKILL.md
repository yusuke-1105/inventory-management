---
name: sidebar-ui-redesign
description: Redesign a Vue 3 application's UI into a modern SaaS-style interface with a left vertical sidebar nav (replacing a top nav bar), a consistent spacing scale, and a polished professional look. Use when asked to redesign, modernize, restyle, or overhaul a Vue app's navigation/layout, or to convert a top-nav layout into a sidebar layout.
---

# Sidebar UI Redesign

Turns a Vue 3 app's top-nav layout into a modern SaaS-style shell: fixed left sidebar for primary navigation, a clean content area with consistent spacing, and small polish details (shadows, hover/active states, transitions) that read as "professional product" rather than "demo app."

This is an **implementation skill** — when invoked, actually perform the redesign (don't just describe it), then verify it in the browser.

## Process

### 1. Audit the current layout

Before touching anything, establish the baseline:
- Find the app shell component that currently renders the top nav (commonly `App.vue`) and read it in full.
- List every nav item / route it links to, and how the active route is highlighted (`$route.path` comparison, a router `active-class`, etc.).
- Check whether anything else lives in that same header band (search bar, filters, profile menu, language switcher, notifications) — all of it needs a new home in the redesigned shell.
- Find where global/shared CSS lives (an unscoped `<style>` block in the shell component is common in smaller apps; a dedicated `styles/` directory is common in larger ones). This is where new design tokens and sidebar styles should go, to stay consistent with the existing convention rather than inventing a second one.
- Skim 2-3 representative page/view components to see the current spacing conventions (padding on cards, gaps between sections, table density) — you're about to standardize this, so know what you're standardizing away from.

### 2. Design the target shell

**Sidebar** (left, fixed width, full viewport height):
- Width: 240-260px is the sweet spot for a text+icon nav — narrow enough to feel efficient, wide enough that labels don't wrap.
- Structure top-to-bottom: brand/logo block → primary nav list → (optional) secondary/utility nav → user/account block pinned to the bottom.
- Nav items: icon + label, generous vertical padding (10-12px) for click target size, a clear active state (filled/tinted background + accent-colored left border or icon, not just a color change on text alone — it needs to be scannable at a glance).
- Use the app's existing router-link/active-route pattern (found in step 1) — don't introduce a different routing mechanism.

**Content area** (right of sidebar, fills remaining width):
- If the old top nav also held page-level controls (filters, search, page title), give the content area its own slim top bar for those — separate from primary navigation, so the two don't compete visually. Primary nav = "where am I in the app," content top bar = "what can I do on this page."
- Consistent horizontal max-width or padding so every page's content aligns, even if individual pages have different widths of tables/cards.

**Spacing scale** — define it once as CSS custom properties and use it everywhere, rather than ad hoc `rem`/`px` values scattered per component:
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-7: 48px;
}
```
Apply this scale to card padding, section gaps, table cell padding, and form control spacing across every view you touch — this consistency is most of what makes a UI read as "polished" rather than "assembled."

**Polish details** (small things, large perceived-quality impact):
- Subtle shadows on cards/sidebar (`box-shadow: 0 1px 3px rgba(0,0,0,0.06)` — restrained, not skeuomorphic).
- Consistent border-radius scale (e.g. 6px small elements, 10-12px cards).
- Hover and active states on every clickable element, with a `transition` (150-200ms ease) so state changes feel deliberate rather than instant/jarring.
- One accent color used consistently for active nav state, primary buttons, and focus rings — don't let a second "accidental" accent color creep in.
- Respect whatever the project already forbids/requires (check its CLAUDE.md) — e.g. this project's design system explicitly bans emojis in the UI and specifies its slate/gray palette; carry constraints like that into every new component you write rather than defaulting to generic web-template styling.

### 3. Implement

- If the project's own CLAUDE.md mandates delegating `.vue` file creation/edits to a specialized subagent (check for a rule like "ANY time you need to create or significantly modify a .vue file, you MUST delegate to `vue-expert`") — follow that rule. Bundle the whole shell restructure (new sidebar component, app-shell template changes, updated global styles) into one delegated task so the result is internally consistent, rather than splitting it across several disjoint edits.
- If no such rule exists, implement directly, matching the codebase's existing component conventions (Composition API vs Options API, `<script setup>` vs `setup()`, scoped vs global styles) — infer the convention from the files you read in step 1, don't impose a different one.
- Typical file changes:
  - New `Sidebar.vue` (or similar) component containing the nav markup/logic extracted from the old top nav.
  - The app shell component updated to a flex/grid layout: sidebar + content area side by side, replacing the old header-on-top structure.
  - Global stylesheet updated with the new design tokens (spacing scale, any new color/shadow/radius variables) and sidebar-specific styles.
  - Each existing page/view nudged onto the new spacing scale where it's cheap to do so — don't do a wall-to-wall rewrite of every view's internal layout unless asked; the shell + spacing tokens are the core deliverable.
- Preserve everything that isn't about layout/navigation: keep every route working, keep any i18n translation calls intact, keep filter bars / search / profile menus functional (just relocated), keep accessibility basics (nav is keyboard-reachable, active route is programmatically indicated via `aria-current` or similar, not color alone).

### 4. Verify

- Start (or confirm already running) the dev server.
- If browser automation tooling (e.g. a Playwright MCP integration) is connected, use it to open the app, click through every nav item, and confirm each route renders correctly inside the new content area with no layout breakage. If it isn't connected, do a build/compile check (e.g. `npm run build`) at minimum and say so explicitly — don't claim visual verification you didn't actually do.
- Check a narrow viewport width doesn't cause horizontal scrolling of the whole page (tables/wide content should scroll within their own container, not blow out the layout).
- Confirm nothing that lived in the old top nav got silently dropped (search, filters, profile/account menu, language switcher, notifications, etc.).

## Common pitfalls

- Sidebar and content area both trying to manage the same padding, causing doubled whitespace — pick one to own the outer margin.
- Active-state styling that's too subtle (a 5% background tint) to scan quickly down a list of 6-8 nav items — err toward a clearer state (filled background, left accent bar, bold weight) over pure subtlety.
- Introducing a second, slightly-different shade of the accent color for hover vs. active vs. focus states instead of reusing one token with opacity/lightness variants.
- Forgetting `overflow-y: auto` on the sidebar itself once the nav list grows longer than the viewport (common once "secondary nav" or "recently viewed" sections get added later).
- Hardcoding the sidebar width in multiple places instead of a single CSS variable — makes a later width tweak require hunting through every file.
