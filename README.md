# Gifts — webapp 56 of 59

Served at https://bucklerfamily.estate/gifts/ (the estate build reads this repository's `main`, folder `public/`).

One chronology, 1877 onwards, of the known title chain and custody of Parcels A (A1 north woods, A2 house and garden), B (meadow) and C (the green, VG41) at Tŷ Mawr (Great House), Llandough. Title (freeholder) and custody (tenant / occupier) sit side by side. Bute and Cardiff Corporation, Daniel Thomas & Son, Mountjoy Ltd, Western Ground Rents, BP and the Williams family are drawn as one continuous band with no dividing line between their hand-offs.

Gift markers: ● recorded as a gift (or for a nominal sum) · ◐ no price stated in the source · ○ consideration not checked · – no transfer on the record.

## Files
- `public/data/chronology.json` — the rows (date, event, title holder, custody, parcels, gift marker and note, our catalogue record IDs, what has been seen). Edit this, then rebuild.
- `tools/build.py` — writes `public/index.html` from the data (static; works without JavaScript; the filter chips are a small enhancement).
- `public/index.html` — the built page.

## Rules for editors (human or agent)
- Every row links our own catalogue record (`https://bucklerfamily.estate/catalogue/?id=<ID>`). A row with no primary record seen says "not checked".
- Add-only: never reword or remove an existing catalogue record; correct a row here with a dated change-log line.
- Present the record in neutral dated wording; no conclusions on the page beyond the labelled Interpretation box. Follow the site's editorial memory and banned-word list.
- Apex paths only (`https://bucklerfamily.estate/<path>`), never a subdomain.
- Tracking issue: https://github.com/unclehowell/cedwyn/issues/551

## Change log
| Version | Date | Change |
|---|---|---|
| 0.0.1 | 2026-11-10 | First release (takes slot 56, was coming-soon-56). |

— Sion's Tab agent
