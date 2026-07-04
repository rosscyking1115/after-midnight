# Power BI → Microsoft Copilot handoff

A self-contained brief for handing the **polish and review** of
`powerbi/community_energy_dashboard.pbix` to **Microsoft Copilot** (Copilot in
Power BI / Fabric, Copilot in Power BI Desktop, or Copilot Chat). Power BI is a
Microsoft product, so Copilot is the natural tool to refine and critique it.

You (the human) drive Copilot; this file is the context to paste in, plus a set
of specific, copy-paste **asks**. Nothing here needs a shell or this repo — it's
all judgment and prompts.

---

## 0. How to use this

Pick the Copilot surface you have:

| Surface | Needs | Best for |
|---|---|---|
| **Copilot in Power BI Desktop / Service** | a Fabric capacity (F2+ trial or paid) assigned to the workspace | building/summarising pages, Smart Narrative, DAX in the model, measure descriptions, Q&A synonyms |
| **Copilot in Power BI Desktop — DAX query view** | Fabric capacity | writing / explaining / fixing DAX against the real model |
| **Microsoft 365 Copilot / Copilot Chat** (copilot.microsoft.com) | none (free tier works) | critiquing the exported PDF, drafting narrative copy, reviewing pasted DAX, layout advice |

If you have no Fabric capacity, use **Copilot Chat**: upload
`powerbi/screenshots/community_energy_dashboard.pdf` and paste the "Context to
give Copilot" block below, then run the review asks in §7.

**Paste this context first, then one ask at a time** (Copilot does better with a
single focused task than a list).

---

## 1. Context to give Copilot (paste verbatim)

> I'm polishing a Power BI report called **Community Energy Flexibility OS**. It
> shows how much **cost and carbon** UK households/communities save by shifting
> flexible electricity loads (washing machine, EV charge, dishwasher) to cleaner,
> cheaper half-hours. It is **decision support, not automation** — the product
> line everywhere is *"planning advice only — no guaranteed savings."* Keep that
> caveat visible and never phrase a number as a promise. Savings are always shown
> **beside their basis** (baseline vs optimised, tariff, confidence). Audience for
> *this dashboard* is analysts and community managers (not end households), so
> conventional dashboard colour is fine — but it must stay colour-blind-safe.

---

## 2. Data model (star schema)

Fact **`fct_daily_savings`** — grain: **one optimised task per household per
day** (demo seed data). Columns:

- `cost_saving_p` (pence), `carbon_saving_g` (grams), `baseline_cost_p` (pence)
- `peak_slots_avoided` (count), `confidence` (0–1), `household_id`
- keys: `date_key`, `device_key`, `community_key`

Dimensions (each **one-to-many → fact**, single filter direction):

| Dimension | Key | Notable columns |
|---|---|---|
| `dim_date` | `date_key` | `full_date` (marked as date table — contiguous full-year spine), `day_name` (sort by `day_of_week`) |
| `dim_device` | `device_key` | `device_type` |
| `dim_community` | `community_key` | `community_name` |

## 3. Measures (already written — in `powerbi/measures.dax`)

`Total Cost Saving (GBP)`, `Total Carbon Saving (kg)`, `Peak Slots Avoided`,
`Tasks Optimised`, `Households Participating`, `Avg Recommendation Confidence`,
`Cost Saving %`, `Cost Saving (GBP) MoM %`, and **`Trusted Cost Saving (GBP)`**
(only confidence ≥ 0.5 — the "how much of the saving is high-confidence" story).
All use `DIVIDE` for safe division and `VAR` for shared sub-expressions.

## 4. The five pages (current)

1. **Executive Summary** — headline cards (cost, carbon, peak slots, tasks, avg confidence).
2. **Cost & Carbon Timeline** — savings over `full_date`; `MoM %` KPI; baseline-vs-optimised; date slicer.
3. **Device Contribution** — cost saving + peak slots by `device_type`.
4. **Community Comparison** — savings by `community_name`; households; averages.
5. **Recommendation Quality** — confidence distribution; `Trusted` vs `Total`; freshness/constraint indicators.

## 5. Theme

`powerbi/theme.json` — green `#1B7A5A` = savings/good, amber `#E9A23B` = neutral,
red `#C44536` = warnings; Segoe UI; 8px card radius, soft `#E2E8F0` borders.

---

## 6. Polish asks (run one at a time, in Copilot with model access)

1. **Layout & alignment.** "Align the five summary cards on the Executive
   Summary page to a shared grid — equal size, equal spacing, top-aligned — and
   give each a plain-English title instead of the default 'Sum of…'."
2. **Plain-English titles everywhere.** "Rewrite every visual title on all five
   pages as a short plain-English phrase a non-analyst would understand (e.g.
   'Cost saved per day', not 'Sum of cost_saving_p by full_date')."
3. **Smart Narrative / summary.** "Add a Smart Narrative (or Copilot summary
   visual) to the Executive Summary that states total cost and carbon saved,
   households participating, and how much of the saving is high-confidence — in
   two or three sentences, no promises, planning-advice framing."
4. **Colour-blind safety (important).** "This theme uses green for good and red
   for warnings. Make every good/bad signal carry a second channel besides
   colour — an icon, a data label, or a shape — so it's readable with red-green
   colour blindness. Check the Recommendation Quality and Timeline pages first."
5. **Measure descriptions + Q&A synonyms.** "Write a one-line description for
   each of these measures and suggest natural-language synonyms so Q&A/Copilot
   can answer questions about them: [paste the 9 names from §3]."
6. **Report-page tooltips.** "Design a report-page tooltip for the device bar
   chart that shows, for the hovered device: cost saved, carbon saved, peak
   slots avoided, and average confidence — each with its unit."
7. **Trust framing.** "On Recommendation Quality, show `Trusted Cost Saving
   (GBP)` as a proportion of `Total Cost Saving (GBP)` in a way that makes clear
   most/least of the saving is high-confidence — and label it as confidence, not
   certainty."
8. **Mobile layout.** "Create a phone layout for the Executive Summary with the
   cards stacked and the narrative on top."
9. **Persistent caveat.** "Add a small, consistent footer text box to every
   page: 'Planning advice only — no guaranteed savings. Figures are modelled
   from forecasts.' Same position on each page."

## 7. Review / "view" asks (works in free Copilot Chat with the PDF)

Upload `powerbi/screenshots/community_energy_dashboard.pdf`, paste §1, then:

- "Critique this dashboard for an executive audience: is the headline clear in
  five seconds? What's cluttered? What's missing?"
- "Check it for accessibility issues you can see: colour-only signals, low
  contrast, tiny text, unlabelled axes."
- "Is anything phrased as a guarantee rather than a forecast/estimate? Flag it."
- "Suggest the single highest-impact change to each page."

## 8. DAX asks (Power BI Desktop DAX query view, or paste into Copilot Chat)

- "Explain what `Trusted Cost Saving (GBP)` does and when it returns blank."
- "Suggest a `Trusted Saving %` measure = Trusted ÷ Total, safe against divide-by-zero."
- "Review these measures for performance and correctness: [paste measures.dax]."

---

## 9. Constraints (do not let Copilot break these)

- **Never** turn a modelled figure into a promise. "Estimated / modelled /
  planning advice" framing stays.
- Savings always appear **beside their basis** (baseline, tariff, confidence).
- Keep `dim_date` marked as the date table and the single-direction
  relationships — don't let an auto-suggestion add bidirectional filters.
- Colour may signal good/bad here, but **never colour alone** — always a second
  channel.

## Done when

Cards aligned with plain-English titles; an exec narrative on page 1; every
good/bad signal colour-blind-safe; a persistent planning-advice caveat on every
page; a fresh PDF + screenshots exported to `powerbi/screenshots/` for the
README and case study.
