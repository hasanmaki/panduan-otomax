# Using the glossary (ezglossary)

This page shows how to define terms, link to them, create summaries, and configure the plugin.

## Defining terms
- Use Markdown definition lists:

  term
  :   Short definition.

  long_term
  :   First paragraph.

      Second paragraph (blank line above).

## Linking terms
- Inline: `<section:term>` or with label: `<section:term|read more>`.
- If `markdown_links: true` in `mkdocs.yml` you can use `[label](section:term)`.

## Generating summaries
- Jinja-style block:

  `{% glossary-summary section="otomax" theme="detailed" %}`

- Examples:
  - Detailed theme: `{% glossary-summary section="otomax" theme="detailed" %}`
  - Table theme, hide references: `{% glossary-summary section="otomax" theme="table" no_refs %}`

## Modifiers
- `no_refs` / `no_defs` — hide references or definitions in the summary.
- `do_refs` / `do_defs` — explicitly include them (some configs default to hide).
- `theme=<name>` — `detailed` (full view) or `table` (compact table).

## mkdocs.yml (global and per-section overrides)
- Global example:

```yaml
plugins:
  - ezglossary:
      inline_refs: short
      markdown_links: true
      ignore_case: true
      tooltip: full
```

- Per-section example:

```yaml
plugins:
  - ezglossary:
      section_config:
        - name: otomax
          theme: table
          list_definitions: true
```

## Troubleshooting
- Restart `mkdocs serve` after config changes.
- Ensure `markdown.extensions.def_list` is enabled (`def_list`) so definition lists parse correctly.
- Escape `|` in table cells as `\|` or `&#124;`.
- Check `mkdocs serve`/logs for missing reference warnings or duplicate term messages.

---

If you want the file localized to Bahasa Indonesia or prefer different examples, tell me and I'll update it.
