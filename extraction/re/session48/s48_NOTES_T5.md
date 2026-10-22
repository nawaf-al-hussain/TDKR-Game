# s48 T5 — trigger BuiltinBox template path: HONEST NEGATIVE + STOP (no size source exists)

## What was checked (time-boxed)

1. **gol.bin templates** (s30 parse, lvc_gol_templates.json): the trigger tids DO
   carry a box component in their template:
   - 9803 BoxTrigger: components [[0, 0x37f7a8ae], [0, 0x729ec572=BuiltinBox]]
   - 18250 DistrictZone: [[0, 0x37f7a8ae], [0, 0x729ec572=BuiltinBox]]
   - 9809 CylinderTrigger: [[0, 0x37f7a8ae], [0, 0x749126c3]]
   The BuiltinBox entry's flag is **0** — the task's premise ("non-zero flag reads
   nothing from the record") does not apply: a flag-0 component is record-driven.
2. **GenerateComponentTemplate @0x368ac0** (`_Z25GenerateComponentTemplateiP13CMemoryStream`,
   11,308 B, ARM mode — the earlier junk disassembly was a Thumb-mode artifact):
   a giant binary-search switch over class ids; each branch is `operator new(size)`
   + constructor (e.g. id 0x69540db7 -> new 0x2c B). It is an INSTANTIATION factory —
   the CMemoryStream* argument is passed through for record-driven Load, not read
   for defaults at the dispatch level. **There is NO branch for BuiltinBox
   0x729ec572 anywhere in the function** (exhaustive movw/movt scan) — the factory
   never creates BuiltinBox components, so no template-default sizes flow from it.
   (CylinderTrigger's box class 0x749126c3 IS dispatched @0x36932c, but that class
   was never part of the s36 BuiltinBox volume model.)
3. s47 T5 (standing): the trigger objects' own lvc record blocks contain ZERO
   BuiltinBox component blocks (both neighbor directions; 0 pairs < 100 required).

## Conclusion (STOP per the task rule)

With flag 0 the component would read from the object's record; the records carry
no such block; the component factory neither creates nor defaults the class.
**No per-instance BuiltinBox extents exist in any data source reachable from the
trigger objects** — the region-preserving test cannot be run (needs >= 100 pairs)
and the trigger-volume model stays **"unvalidated, engine-derived only"**,
exactly as session 47 left it. Nothing removed.

## Artifacts

s48_t5_gct.py, s48_t5_sym.py, s48_t5_branch2.py, s48_t5_branch3.py
(+ note: libKRHP.so lives at /tmp/my-project/work/re29/libKRHP.so; ELF PT_LOAD
maps vaddr==file offset for the code segment; the function is ARM, not Thumb).
