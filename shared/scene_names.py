SCENE_SUFFIX_MAP = {
  "Red Alert 2": "RA2",
  "Red Alert 2 - Infantry": "RA2.INF",
  "Red Alert 2 - Effects": "RA2.FX",
  "Tiberian Sun": "TS",
  "Tiberian Sun - Infantry": "TS.INF",
  "Tiberian Sun - Effects": "TS.FX",
  "ReWire": "RW",
  "ReWire - Infantry": "RW.INF",
  "ReWire - Effects": "RW.FX",
  "Red Alert / Tiberian Dawn": "RA1",
  "Red Alert / Tiberian Dawn - Infantry": "RA1.INF",
  "Red Alert / Tiberian Dawn - Effects": "RA1.FX",
  "Dune 2000": "D2K",
  "Dune 2000 - Infantry": "D2K.INF",
  "Dune 2000 - Effects": "D2K.FX",
  "C&C Remastered": "RM",
  "C&C Remastered - Infantry": "RM.INF",
  "C&C Remastered - Effects": "RM.FX",
}


def get_suffix_if_elif() -> str:
  lines = ['suffix = "RA2.INF"', "", "scenename = bpy.context.scene.name"]
  for name, suffix in SCENE_SUFFIX_MAP.items():
    keyword = "if" if lines[-1] == "scenename = bpy.context.scene.name" else "elif"
    lines.append(f'{keyword} scenename == "{name}": suffix = "{suffix}"')
  lines.append("")
  return "\n".join(lines)
