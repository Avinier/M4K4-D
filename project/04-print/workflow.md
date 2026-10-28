# Print workflow

The steps every printed part goes through, from a `DESIGN` row in a `03-build`
BOM to a weighed part in the robot.

## Steps

1. **Export.** Export the part as an STL from the final v1 assembly with the
   droid edits applied ([README rule 3](README.md#rules)), in its print
   orientation. The leaf label in the CAD names the part; the labels already
   matched by `final/v1/cad/finish_colours.py` are the list of printed parts.
2. **Orient and check.** Choose the face on the bed, the supports, and the
   faces that must stay clean (mating faces, bearing seats, insert bosses).
   Check the 1.2 mm minimum wall and the lab's 250 mm limit.
3. **Settings.** Write the slicer settings on the part card: material profile,
   walls, infill, any hole offset, where fuzzy skin goes, and the
   colour split for two-tone parts. The lab slices at the printer from the STL
   and these notes.
4. **Request.** Email the lab at least 4 days ahead with the purpose,
   dimensions, material and print type, and the faculty member CC'd
   ([lab.md](lab.md)). Group parts onto plates: every plate needs a supervised
   start.
5. **Print.** Dry the filament (4–6 h at 60 °C). Stay for the first 5 layers.
6. **Inspect.** Remove supports, check the clean faces, fit the inserts, weigh
   the part, and measure the dimensions listed on its part card.
7. **Record.** Add a log row. A failed print or a bad fit gets a row too, with
   the cause.

## Part card

Each subsystem README has one row per printed part. The columns are:

| Column | Meaning |
|---|---|
| ID | The `03-build` BOM ID (`CH-004`) |
| Label | The leaf label in the CAD (`WHEEL_L_RIM_PETG`) |
| Qty | Installed quantity |
| Material, colour | From the print guide |
| Printer | The planned machine |
| Orientation | The face on the bed, and supports |
| Critical | The dimensions and faces to check after printing |
| Settings | Slicer settings: walls, infill, offsets, fuzzy skin, colour split |
| Status | See below |

**Status values**, in order: `TODO` (not exported) → `EXPORTED` → `SLICED` →
`PRINTED` → `FITTED` (inserts in and the mating part tried) → `ACCEPTED`
(passes its test). `REPRINT` means a printed part was rejected; the log says
why.

## Print log

Each subsystem keeps a `log.md`, one row per print:

| Date | Plate | Parts | Printer | Filament (brand, colour, lot) | Settings | Time | Result | Mass (g) | Notes |
|---|---|---|---|---|---|---|---|---|---|

## Files

Each subsystem folder holds only:

| Path | Contents |
|---|---|
| `README.md` | Part cards and plates |
| `stl/` | One raw STL per part, exported from the CAD in its print orientation |
| `log.md` | The print log |
| `photos/` | Small photos of prints, failures and fits |

All of it is in Git. STL names use the BOM ID and the CAD label:
`CH-004_WHEEL_L_RIM_PETG.stl`. An STL is replaced only by a fresh export after
a CAD change in `final/v1`, never edited; the commit that replaces it names the
decision.

## Print-ready means

A part is print-ready when:

- its STL matches the current final v1 CAD (exported after the last change);
- its orientation, supports and clean faces are on its part card;
- its slicer settings, with any hole offset for that printer and material, are
  on its part card;
- the purchased parts it must fit (bearings, motors, inserts) are in hand and
  measured.
