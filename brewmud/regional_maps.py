from __future__ import annotations

from dataclasses import dataclass

from .world import ROOMS


@dataclass(frozen=True)
class RegionalMap:
    title: str
    rows: tuple[tuple[tuple[str, str], ...], ...]
    transitions: str

    @property
    def nodes(self) -> dict[str, str]:
        return {code: room for row in self.rows for code, room in row}

    def render(self, current: str) -> str:
        diagrams = []
        for index, row in enumerate(self.rows):
            diagrams.append("---".join(f"<{code}>" if room == current else f"[{code}]" for code,room in row))
            if index < len(self.rows) - 1:
                columns = min(len(row), len(self.rows[index + 1]))
                diagrams.append("  |     " * (columns - 1) + "  |")
        legend = "\n".join(f"  {code}  {ROOMS[room].name}" for row in self.rows for code,room in row)
        return (f"REGIONAL MAP — {self.title}    <CODE> = YOU ARE HERE\n"
                + "\n".join(diagrams)
                + f"\n\nLocations:\n{legend}\n\nRegional Transitions: {self.transitions}")


REGIONAL_MAPS = {
 "malt": RegionalMap("MALTINGS", ((('GRN','grain_receiving'),('BAR','barley_lab'),('STP','steep_house'),('AIR','air_rest'),('GER','germination_floor')),
                                      (('GAT','brewery_gate'),('CUR','cure_floor'),('KLN','kiln'),('END','endosperm'),('ALE','aleurone'))),
                     "GER leads DOWN to the Water Laboratory; GAT leads IN from the Shipping Dock."),
 "mash": RegionalMap("WATER AND MASH", ((('WAT','water_lab'),('PHB','ph_bench'),('ION','ion_gallery'),('CTY','city_profiles')),
                                            (('TRT','treatment_bay'),('MIL','mill_room'),('MSH','mash_tun'),('PRO','protein_rest')),
                                            (('BET','beta_rest'),('ALP','alpha_rest'),('CNV','conversion_bench'),('OUT','mash_out'))),
                     "WAT leads UP to Germination; MSH leads IN to the Carbohydrate Lab; CNV leads IN to the Gelatinization Chamber; OUT leads DOWN to the Lauter Tun."),
 "starch": RegionalMap("CARBOHYDRATE AND STARCH LAB",
                       ((('CAR','carbohydrate_lab'),('GLU','glucose_bench'),('DIS','disaccharide_gallery'),('POL','polymer_comparison')),
                        (('GEL','gelatinization_chamber'),('CRY','crystallinity_lab'),('AMY','amylose_helix'),('AMP','amylopectin_arbor'))),
                       "CAR leads OUT to the Mash Tun; GEL leads OUT to the Starch Conversion Bench."),
 "brew": RegionalMap("BREWHOUSE", ((('LAU','lauter_tun'),('BED','grain_bed'),('SPA','sparge_arm'),('GRA','wort_grant'),('KET','kettle')),
                                          (('BRK','hot_break'),('HOP','hop_dosing'),('WHL','whirlpool'),('HEX','heat_exchanger'),('OXY','oxygenation_station'))),
                     "LAU leads UP to Mash-Out; HOP leads IN to the Hop Lab; OXY leads DOWN to Fermentation."),
 "ferment": RegionalMap("FERMENTATION CELLAR", ((('PIT','pitching_deck'),('ALE','ale_fermenter'),('LAG','lager_fermenter'),('YLB','yeast_lab'),('MEM','yeast_membrane'),('MGP','maltose_gate'),('MLT','maltase_bench')),
                                                    (('GLY','glycolysis_lane'),('NAD','nad_recycling'),('LIP','lipid_workshop'),('EST','ester_lab'),('DIA','diacetyl_rest'),('SUL','sulfur_vent'),('MAT','maturation_cellar'))),
                     "PIT leads UP to wort oxygenation; YLB leads IN to Microbiology; MAT leads DOWN to Packaging."),
 "hops": RegionalMap("HOP YARD AND FLAVOR LAB", ((('YRD','hop_yard'),('CON','female_cone'),('LUP','lupulin_gland'),('AAC','alpha_acid_bench')),
                                                   (('OIL','oil_lab'),('IBU','ibu_station'),('DRY','dry_hop_gallery'),('LGT','lightstrike_booth'))),
                     "AAC leads OUT to the Brewhouse Hop-Dosing Balcony."),
 "pack": RegionalMap("PACKAGING AND SENSORY", ((('BRT','brite_tank'),('CO2','carbonation_station'),('BOT','bottle_line'),('CAN','canning_line'),('NIT','nitrogen_tap')),
                                                   (('FOM','foam_lab'),('SNS','sensory_room'),('STY','style_taproom'),('CLD','cold_storage'),('SHP','shipping_dock'))),
                     "BRT leads UP to Maturation; STY leads DOWN to QA; SHP leads OUT to the Brewery Gate."),
 "quality": RegionalMap("QUALITY AND TRAINING", ((('MIC','microbiology_lab'),('SAN','sanitation_bay'),('QAC','qa_chemistry')),
                                                    (('BNK','yeast_bank'),('PIL','pilot_brewery'),('CLS','training_classroom'))),
                     "MIC leads OUT to the Yeast Lab; QAC leads UP to the Style Taproom."),
}

ALIASES = {"malting":"malt","maltings":"malt","malt":"malt", "water":"mash","mash":"mash",
           "starch":"starch","carbohydrate":"starch","carbohydrates":"starch","sugar":"starch",
           "brewhouse":"brew","brew":"brew", "fermentation":"ferment","cellar":"ferment","ferment":"ferment",
           "hop":"hops","hops":"hops", "packaging":"pack","sensory":"pack","pack":"pack",
           "quality":"quality","qa":"quality","training":"quality"}
ROOM_REGION = {room: region for region,m in REGIONAL_MAPS.items() for room in m.nodes.values()}


def map_index() -> str:
    return ("BREWMUD REGIONAL MAPS\n  MAP MALT       Maltings\n  MAP MASH       Water and mash chemistry\n"
            "  MAP STARCH     Carbohydrate and starch lab\n  MAP BREW       Brewhouse\n"
            "  MAP FERMENT    Fermentation cellar\n  MAP HOPS       Hop yard and flavor lab\n"
            "  MAP PACK       Packaging and sensory\n  MAP QUALITY    Quality and training")


def render_map(current: str, requested: str = "") -> str:
    query = " ".join(requested.casefold().split())
    if query in {"all","regions","list","help"}: return map_index()
    region = ALIASES.get(query) if query else ROOM_REGION[current]
    return REGIONAL_MAPS[region].render(current) if region else f"Unknown map region: {requested}.\n\n{map_index()}"
