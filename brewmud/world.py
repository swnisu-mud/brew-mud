"""The BrewMUD world: 70 connected locations from grain receiving to taproom."""

from __future__ import annotations

from .models import Feature, NPC, Room


DIRECTION_ALIASES = {"n":"north", "s":"south", "e":"east", "w":"west", "u":"up", "d":"down", "i":"in", "o":"out"}


# key, display name, examinable feature, course-grounded field note
ROOM_DATA = (
    ("brewery_gate", "Brewery Gate", "process board", "Brewing links malting, milling, mashing, lautering, boiling, cooling, fermentation, maturation, and packaging."),
    ("grain_receiving", "Grain Receiving", "sampling spear", "Uniform barley kernels hydrate and germinate more consistently than a highly variable lot."),
    ("barley_lab", "Two-Row Barley Laboratory", "kernel cross-section", "Two-row barley is often favored by brewers for large, relatively uniform kernels and useful malting properties."),
    ("steep_house", "Steep House", "steep tank", "Alternating water steeps and air rests raise kernel moisture while maintaining oxygen for the living grain."),
    ("air_rest", "Steep Air Rest", "aeration manifold", "Germinating barley is metabolically active and needs oxygen; uncontrolled waterlogging can impede healthy modification."),
    ("germination_floor", "Germination Floor", "turning rake", "The embryo releases gibberellic-acid signals that stimulate hydrolytic-enzyme production in the aleurone."),
    ("aleurone", "Aleurone Workshop", "secretory vesicles", "Aleurone cells synthesize alpha-amylase and proteases in response to germination signals."),
    ("endosperm", "Starchy Endosperm", "starch granules", "Malting modifies cell walls and protein matrix so enzymes can reach endosperm starch during mashing."),
    ("kiln", "Malt Kiln", "kiln schedule", "Initial drying preserves enzymes; higher-temperature kilning develops color and flavor but sacrifices more enzyme activity."),
    ("cure_floor", "Malt Curing Floor", "rootlet screen", "Drying stops germination, and curing/outgassing lets newly kilned malt lose harsh volatile notes before use."),

    ("water_lab", "Brewing Water Laboratory", "water report", "Beer is mostly water, and dissolved ions affect mash pH, enzyme performance, yeast, and sensory balance."),
    ("ph_bench", "pH Bench", "pH electrode", "The pH scale is logarithmic; a one-unit change represents a tenfold change in hydrogen-ion activity."),
    ("ion_gallery", "Ion Gallery", "ion chart", "Alkalinity describes resistance to acidification, while hardness chiefly reflects polyvalent ions such as calcium and magnesium."),
    ("city_profiles", "Historic Water Profiles", "Burton and Pilsen display", "Historic brewing centers adapted styles to local water, but modern brewers can build water to fit a recipe."),
    ("treatment_bay", "Water Treatment Bay", "carbon filter", "Chlorine, chloramine, iron, and unwanted alkalinity may require different treatments; one method does not solve every problem."),
    ("mill_room", "Malt Mill", "roller gap", "A good crush exposes endosperm while retaining husk pieces that later support the lauter filter bed."),
    ("mash_tun", "Mash Tun", "temperature rake", "Mash temperature and pH change the balance of enzyme activities and therefore wort fermentability and body."),
    ("protein_rest", "Protein Rest", "protease window", "Proteases are most useful below typical saccharification temperatures and can affect FAN, haze, and foam-active proteins."),
    ("beta_rest", "Beta-Amylase Rest", "maltose assay", "Beta-amylase attacks nonreducing ends to release maltose and is less heat-stable than alpha-amylase."),
    ("alpha_rest", "Alpha-Amylase Rest", "dextrin trace", "Alpha-amylase makes internal alpha-1,4 cleavages, rapidly lowering viscosity and producing dextrins of varied size."),
    ("conversion_bench", "Starch Conversion Bench", "iodine plate", "Gelatinization disrupts ordered starch granules and improves enzyme access to amylose and amylopectin."),
    ("mash_out", "Mash-Out Platform", "mash-out gauge", "Heating for mash-out reduces viscosity and largely arrests the enzyme balance established during the mash."),

    ("lauter_tun", "Lauter Tun", "false bottom", "Lautering separates sweet wort from insoluble grain material through a husk-supported filter bed."),
    ("grain_bed", "Grain-Bed Gallery", "husk channels", "Compaction, an excessively fine crush, or rapid runoff can reduce permeability and cause a stuck mash."),
    ("sparge_arm", "Sparge Arm", "spray pattern", "Sparging rinses retained extract, but excessive volume, heat, or pH can promote undesirable extraction."),
    ("wort_grant", "Wort Grant", "clarity glass", "Vorlauf recirculates early turbid wort until the grain bed establishes effective filtration."),
    ("kettle", "Copper Kettle", "rolling boil", "Boiling sterilizes wort, stops mash enzymes, volatilizes compounds, coagulates protein, and drives hop-alpha-acid isomerization."),
    ("hot_break", "Hot-Break Deck", "protein floc", "Heat-denatured proteins aggregate with polyphenols and other material into a hot break that can be separated from wort."),
    ("hop_dosing", "Hop-Dosing Balcony", "addition clock", "Early hop additions chiefly support bitterness; later additions preserve more flavor and volatile aroma."),
    ("whirlpool", "Whirlpool", "trub cone", "Tangential flow collects hop matter and coagulated material into a central trub cone before wort transfer."),
    ("heat_exchanger", "Wort Heat Exchanger", "plate stack", "Rapid cooling limits contamination opportunity, arrests thermal reactions, and prepares wort for yeast."),
    ("oxygenation_station", "Wort Oxygenation Station", "oxygen stone", "Pitching wort is oxygenated so yeast can synthesize sterols and unsaturated fatty acids needed for membrane growth."),

    ("pitching_deck", "Yeast Pitching Deck", "pitch calculator", "Pitch rate, viability, vitality, strain, wort gravity, oxygenation, and temperature jointly influence fermentation."),
    ("ale_fermenter", "Ale Fermenter", "warm jacket", "Saccharomyces cerevisiae generally ferments ales warmer and often contributes a more evident ester profile."),
    ("lager_fermenter", "Lager Fermenter", "cool jacket", "Saccharomyces pastorianus is a hybrid yeast used for cool lager fermentation."),
    ("yeast_lab", "Yeast Culture Laboratory", "counting chamber", "Cell counts and viability staining help distinguish an adequate pitch from an apparently large but unhealthy culture."),
    ("yeast_membrane", "Yeast Membrane Walk", "membrane model", "Sterols and unsaturated fatty acids maintain membrane properties needed for growth and nutrient transport."),
    ("maltose_gate", "Maltose Transport Gate", "proton symporter", "Maltose uptake uses active proton-linked transport and is delayed while glucose repression is strong."),
    ("maltase_bench", "Maltase Bench", "hydrolysis model", "Intracellular maltase cleaves maltose into two glucose molecules that can enter glycolysis."),
    ("glycolysis_lane", "Glycolysis Lane", "carbon ledger", "Glycolysis converts glucose to pyruvate with a net gain of two ATP and reduced NADH per glucose."),
    ("nad_recycling", "NAD+ Recycling Junction", "redox wheel", "Alcoholic fermentation converts pyruvate to ethanol and carbon dioxide while regenerating NAD+ for glycolysis."),
    ("lipid_workshop", "Sterol and Lipid Workshop", "ergosterol model", "Brewing yeast primarily needs early oxygen for lipid synthesis, not for extracting large amounts of energy by respiration."),
    ("ester_lab", "Ester Laboratory", "aroma standards", "Esters arise from acids and alcohol-derived metabolism; strain and fermentation conditions alter their abundance."),
    ("diacetyl_rest", "Diacetyl Rest", "warm-rest schedule", "Active yeast can reabsorb diacetyl and reduce it to less flavor-active products during maturation."),
    ("sulfur_vent", "Sulfur Vent", "aroma hood", "Hydrogen sulfide suggests rotten egg, while dimethyl sulfide is often described as cooked corn or vegetables."),
    ("maturation_cellar", "Maturation Cellar", "lagering tank", "Maturation permits yeast cleanup, flavor integration, clarification, and—during lagering—cold settling."),

    ("hop_yard", "Hop Yard", "training wire", "Hops are perennial plants trained as bines; brewing cones usually come from unfertilized female plants."),
    ("female_cone", "Female Cone Arbor", "cone bracts", "Hop cones protect lupulin glands rich in resins and essential oils."),
    ("lupulin_gland", "Lupulin Gland", "yellow lupulin", "Lupulin contains alpha and beta acids plus volatile essential-oil components."),
    ("alpha_acid_bench", "Alpha-Acid Bench", "humulone structure", "Heat rearranges alpha acids such as humulone into more soluble bitter iso-alpha acids."),
    ("oil_lab", "Hop Essential-Oil Lab", "oil chromatogram", "Myrcene, humulene, caryophyllene, and farnesene contribute to hop aroma but are volatile."),
    ("ibu_station", "IBU Spectrophotometer", "275-nm display", "The common IBU assay estimates iso-alpha-acid-related absorbance near 275 nm rather than directly measuring perceived bitterness."),
    ("dry_hop_gallery", "Dry-Hop Gallery", "cold-side doser", "Dry hopping extracts aroma without kettle isomerization and may also support enzymatic or yeast-mediated changes."),
    ("lightstrike_booth", "Lightstrike Booth", "blue-light chamber", "Light, riboflavin, hop-derived compounds, and sulfur chemistry can form intensely skunky MBT."),

    ("brite_tank", "Brite Beer Tank", "bright-beer sightglass", "A brite tank holds clarified, conditioned beer for carbonation and packaging."),
    ("carbonation_station", "Carbonation Station", "solubility chart", "At a given pressure, colder beer retains more dissolved carbon dioxide than warmer beer."),
    ("bottle_line", "Bottle-Conditioning Line", "priming doser", "Bottle conditioning uses residual or added yeast and fermentable sugar to generate package carbon dioxide."),
    ("canning_line", "Canning Line", "seam gauge", "Cans exclude light and, with sound seams and low oxygen pickup, protect beer effectively."),
    ("nitrogen_tap", "Nitrogen Service Tap", "restrictor plate", "Nitrogen is much less soluble than carbon dioxide and supports a fine-bubbled creamy presentation."),
    ("foam_lab", "Beer Foam Laboratory", "foam column", "Foam depends on surface-active proteins, hop compounds, gas, nucleation, and the absence of foam-negative lipids or detergents."),
    ("sensory_room", "Sensory Evaluation Room", "blind tasting booths", "Analytical sensory work uses controlled samples, shared vocabulary, replication, and awareness of thresholds and bias."),
    ("style_taproom", "Style Taproom", "style board", "Beer styles describe recurring ingredient and process choices; they are guides, not substitutes for biochemical reasoning."),
    ("cold_storage", "Cold Storage", "temperature logger", "Cool stable storage slows many staling reactions and helps preserve packaged-beer quality."),
    ("shipping_dock", "Packaging and Shipping Dock", "oxygen ledger", "Dissolved oxygen and package oxygen can accelerate aldehyde formation and loss of fresh flavor."),

    ("microbiology_lab", "Brewery Microbiology Lab", "agar plates", "Selective media and microscopy can help distinguish production yeast from bacteria and wild yeast."),
    ("sanitation_bay", "Cleaning and Sanitation Bay", "CIP loop", "Cleaning removes soil; sanitizing reduces microorganisms on an already clean surface."),
    ("qa_chemistry", "Analytical Chemistry Lab", "instrument log", "Analytical results require calibration, controls, traceable sampling, and interpretation in the context of the process."),
    ("yeast_bank", "Production Yeast Bank", "cryovial rack", "A well-managed yeast bank preserves authenticated strains and reduces genetic drift and contamination across repitches."),
    ("pilot_brewery", "Pilot Brewery", "small-scale brewhouse", "Pilot batches test ingredient and process changes at manageable scale before production equipment and beer are committed."),
    ("training_classroom", "Brewery Training Classroom", "batch record", "A complete batch record connects raw materials, time, temperature, pH, gravity, sensory results, and corrective actions."),
)


PLACEMENTS = {
    "brewery_gate": ("training_coordinator",), "grain_receiving": ("barley_inspector",),
    "barley_lab": ("two_row_kernel",), "steep_house": ("steep_master",), "air_rest": ("oxygen_sensor",),
    "germination_floor": ("gibberellic_acid",), "aleurone": ("aleurone_cell",),
    "endosperm": ("starch_granule",), "kiln": ("kiln_operator",), "cure_floor": ("head_maltster",),
    "water_lab": ("water_chemist",), "ph_bench": ("ph_meter",),
    "ion_gallery": ("bicarbonate", "calcium_ion", "sulfate_ion", "chloride_ion"),
    "city_profiles": ("burton_guide",), "treatment_bay": ("treatment_chemist",),
    "mill_room": ("miller",), "mash_tun": ("head_brewer",), "protein_rest": ("protease",),
    "beta_rest": ("beta_amylase",), "alpha_rest": ("alpha_amylase",),
    "conversion_bench": ("gelatinized_starch",), "mash_out": ("mash_out_operator",),
    "lauter_tun": ("lauter_operator",), "grain_bed": ("husk_keeper",),
    "sparge_arm": ("sparge_technician",), "wort_grant": ("vorlauf_guide",),
    "kettle": ("kettle_brewer",), "hot_break": ("boil_engineer",), "hop_dosing": ("dosing_brewer",),
    "whirlpool": ("whirlpool_operator",), "heat_exchanger": ("cooling_operator",),
    "oxygenation_station": ("oxygenation_tech",), "pitching_deck": ("qa_technician",),
    "ale_fermenter": ("ale_yeast",), "lager_fermenter": ("lager_yeast",),
    "yeast_lab": ("yeast_culturist",), "yeast_membrane": ("lipid_specialist",),
    "maltose_gate": ("maltose_permease",), "maltase_bench": ("maltase",),
    "glycolysis_lane": ("alpha_acetolactate",), "nad_recycling": ("alcohol_dehydrogenase",),
    "lipid_workshop": ("ergosterol",), "ester_lab": ("ester_chemist",),
    "diacetyl_rest": ("diacetyl_molecule",),
    "sulfur_vent": ("hydrogen_sulfide", "dms_molecule", "sulfur_engineer"),
    "maturation_cellar": ("cellar_manager", "maturation_operator", "cold_keeper"),
    "hop_yard": ("hop_breeder",), "female_cone": ("hop_grower",), "lupulin_gland": ("lupulin_keeper",),
    "alpha_acid_bench": ("humulone", "isomerization_chemist"), "oil_lab": ("myrcene",), "ibu_station": ("ibu_chemist",),
    "dry_hop_gallery": ("dry_hopper",),
    "lightstrike_booth": ("light_tester", "riboflavin", "mbt_molecule"),
    "brite_tank": ("brite_operator",), "carbonation_station": ("carbonation_operator",),
    "bottle_line": ("bottle_conditioner",), "canning_line": ("can_specialist",),
    "nitrogen_tap": ("nitrogen_operator",), "foam_lab": ("ltp1", "protein_z"),
    "sensory_room": ("sensory_analyst",),
    "style_taproom": ("style_judge", "taproom_manager", "glass_steward"),
    "cold_storage": ("cold_storekeeper",), "shipping_dock": ("packaging_lead",),
    "microbiology_lab": ("microbiologist", "lactic_bacterium", "wild_yeast"),
    "sanitation_bay": ("sanitation_lead",), "qa_chemistry": ("qa_chemist",),
    "yeast_bank": ("yeast_banker",), "pilot_brewery": ("pilot_brewer",),
    "training_classroom": ("instructor",),
}


NAMES = {
    "training_coordinator":"Training Coordinator", "barley_inspector":"Barley Inspector", "two_row_kernel":"Two-Row Kernel",
    "steep_master":"Steep-House Maltster", "oxygen_sensor":"Dissolved-Oxygen Sensor", "gibberellic_acid":"Gibberellic Acid",
    "aleurone_cell":"Aleurone Cell", "starch_granule":"Starch Granule", "kiln_operator":"Kiln Operator", "head_maltster":"Head Maltster",
    "water_chemist":"Water Chemist", "ph_meter":"pH Meter", "bicarbonate":"Bicarbonate", "calcium_ion":"Calcium Ion",
    "sulfate_ion":"Sulfate Ion", "chloride_ion":"Chloride Ion", "burton_guide":"Burton Water Guide", "treatment_chemist":"Treatment Chemist",
    "miller":"Miller", "head_brewer":"Head Brewer", "protease":"Protease", "beta_amylase":"Beta-Amylase", "alpha_amylase":"Alpha-Amylase",
    "gelatinized_starch":"Gelatinized Starch", "mash_out_operator":"Mash-Out Operator", "lauter_operator":"Lauter Operator",
    "husk_keeper":"Husk Keeper", "sparge_technician":"Sparge Technician", "vorlauf_guide":"Vorlauf Guide", "kettle_brewer":"Kettle Brewer",
    "boil_engineer":"Boil Engineer", "dosing_brewer":"Hop-Dosing Brewer", "whirlpool_operator":"Whirlpool Operator",
    "cooling_operator":"Cooling Operator", "oxygenation_tech":"Oxygenation Technician", "qa_technician":"QA Technician",
    "ale_yeast":"Saccharomyces cerevisiae", "lager_yeast":"Saccharomyces pastorianus", "yeast_culturist":"Yeast Culturist",
    "lipid_specialist":"Membrane-Lipid Specialist", "maltose_permease":"Maltose Permease", "maltase":"Maltase",
    "alpha_acetolactate":"Alpha-Acetolactate", "alcohol_dehydrogenase":"Alcohol Dehydrogenase", "ergosterol":"Ergosterol",
    "ester_chemist":"Ester Chemist", "diacetyl_molecule":"Diacetyl", "hydrogen_sulfide":"Hydrogen Sulfide",
    "dms_molecule":"Dimethyl Sulfide", "sulfur_engineer":"Sulfur Engineer", "cellar_manager":"Cellar Manager",
    "maturation_operator":"Maturation Operator", "cold_keeper":"Lagering Cellar Keeper", "hop_breeder":"Hop Breeder",
    "hop_grower":"Hop Grower", "lupulin_keeper":"Lupulin Keeper", "humulone":"Humulone", "isomerization_chemist":"Isomerization Chemist", "myrcene":"Myrcene",
    "ibu_chemist":"IBU Chemist", "dry_hopper":"Dry Hopper", "light_tester":"Lightstrike Technician", "riboflavin":"Riboflavin",
    "mbt_molecule":"3-MBT", "brite_operator":"Brite-Tank Operator", "carbonation_operator":"Carbonation Operator",
    "bottle_conditioner":"Bottle-Conditioning Yeast", "can_specialist":"Can Specialist", "nitrogen_operator":"Nitrogen Tap Operator",
    "ltp1":"Lipid Transfer Protein 1 (LTP1)", "protein_z":"Protein Z", "sensory_analyst":"Sensory Analyst",
    "style_judge":"Style Judge", "taproom_manager":"Taproom Manager", "glass_steward":"Glass Steward",
    "cold_storekeeper":"Cold-Storage Keeper", "packaging_lead":"Packaging Lead", "microbiologist":"Brewery Microbiologist",
    "lactic_bacterium":"Lactic Acid Bacterium", "wild_yeast":"Wild Yeast Isolate", "sanitation_lead":"Sanitation Lead",
    "qa_chemist":"QA Chemist", "yeast_banker":"Yeast Bank Curator", "pilot_brewer":"Pilot Brewer", "instructor":"Brewery Instructor",
}


# Natural synonyms that are not simple prefixes of an NPC's displayed name.
EXTRA_NPC_ALIASES = {
    "training_coordinator": ("trainer",),
}


def aliases(key: str, name: str) -> tuple[str, ...]:
    values = {key, key.replace("_", " "), name.casefold()}
    values.update(part.strip("()") for part in name.casefold().split() if len(part.strip("()")) > 2)
    values.update(EXTRA_NPC_ALIASES.get(key, ()))
    return tuple(sorted(values))


NPC_DESCRIPTIONS = {
    "training_coordinator": "A brewery process map covers the coordinator's clipboard, with arrows linking every operation to measurements made downstream.",
    "barley_inspector": "The inspector splits representative kernels to compare size, moisture, protein, germination capacity, and signs of pre-harvest damage.",
    "two_row_kernel": "A magnified barley kernel displays husk, embryo, aleurone, and a starch-rich endosperm in cross-section.",
    "steep_master": "The maltster tracks kernel moisture and alternates immersion with air rests rather than leaving the living grain continuously submerged.",
    "oxygen_sensor": "A probe monitors dissolved oxygen during steeping; a falling reading warns that respiring kernels may become oxygen-limited unless water is drained and the grain aerated.",
    "gibberellic_acid": "A small diterpenoid hormone carries the embryo's germination signal toward receptors in the aleurone layer.",
    "aleurone_cell": "Secretory vesicles crowd this living cell as it responds to gibberellin by producing alpha-amylase, proteases, and other hydrolases.",
    "starch_granule": "Concentric semicrystalline layers of amylose and branched amylopectin pack glucose densely inside the endosperm.",
    "kiln_operator": "The operator balances drying rate, cure temperature, color, flavor development, and survival of malt enzymes.",
    "head_maltster": "The Head Maltster judges modification by moisture, acrospire growth, friability, aroma, and the accessibility of the endosperm.",
    "water_chemist": "A water report beside the chemist separates calcium, magnesium, sulfate, chloride, sodium, alkalinity, and pH instead of reducing water to 'hard' or 'soft.'",
    "ph_meter": "A glass electrode responds to hydrogen-ion activity and reports the logarithmic pH of a cooled, representative sample.",
    "bicarbonate": "This tetrahedral ion accepts added protons and contributes strongly to the acid-neutralizing capacity called alkalinity.",
    "calcium_ion": "The divalent ion associates with phosphate chemistry, can help lower mash pH, and stabilizes alpha-amylase against thermal inactivation.",
    "sulfate_ion": "Sulfate carries no aroma of its own here, but shifts sensory balance toward drier, sharper hop bitterness when present at useful concentrations.",
    "chloride_ion": "Chloride tends to support palate fullness and apparent sweetness, providing a sensory counterpoint to sulfate rather than literal sugar.",
    "burton_guide": "The guide compares sulfate-rich Burton water with very soft Pilsen water and bicarbonate-rich waters suited historically to darker grists.",
    "treatment_chemist": "Activated carbon, acid, salts, reverse osmosis, and dechlorination reagents are labeled by the specific problem each can solve.",
    "miller": "The miller adjusts paired rollers to crack kernels and expose endosperm while avoiding both intact grain and excessive flour.",
    "head_brewer": "The brewer compares time, temperature, pH, and iodine tests to determine whether starch conversion follows the intended mash profile.",
    "protease": "A catalytic cleft positions peptide bonds for hydrolysis, releasing smaller peptides and amino nitrogen during a suitable low-temperature rest.",
    "beta_amylase": "The enzyme grips a nonreducing starch-chain end and removes maltose units sequentially, stopping at branch-imposed limits.",
    "alpha_amylase": "The enzyme binds within an alpha-1,4 glucan chain and makes internal cuts that reduce viscosity and create new chain ends.",
    "gelatinized_starch": "Water and heat have disrupted this granule's ordered packing, exposing flexible glucan chains to amylases.",
    "mash_out_operator": "The operator raises mash temperature to reduce viscosity and arrest most of the enzymatic balance before separation.",
    "lauter_operator": "The operator watches pressure and flow above a slotted false bottom, treating the grain itself as the main filter medium.",
    "husk_keeper": "Interlocking husk fragments hold open liquid channels through the spent-grain bed; crushed flour fills the smallest spaces.",
    "sparge_technician": "A rotating arm distributes hot liquor gently so extract is rinsed without channeling, compacting the bed, or overextracting husk compounds.",
    "vorlauf_guide": "The guide returns cloudy first runnings to the top of the bed until suspended particles are captured and wort clarity improves.",
    "kettle_brewer": "A boil schedule marks sterilization, enzyme inactivation, hot-break formation, volatile removal, and hop additions by purpose.",
    "boil_engineer": "The engineer checks boil vigor and vapor escape because weak or covered boiling can retain unwanted volatile sulfur compounds.",
    "dosing_brewer": "Separate bins labeled bittering, flavor, and aroma show how contact time changes the contribution of the same hops.",
    "whirlpool_operator": "The operator directs tangential wort flow that gathers dense hop and proteinaceous trub into a central cone.",
    "cooling_operator": "Thin alternating plates exchange heat rapidly while keeping cooling water physically separate from sanitary wort.",
    "oxygenation_tech": "A sterile stone disperses small oxygen bubbles into cooled wort before pitching, when yeast membrane synthesis can use them.",
    "qa_technician": "Calibrated hydrometers, density meters, sample labels, and duplicate records surround a technician who distrusts unverified single readings.",
    "ale_yeast": "An oval budding S. cerevisiae cell carries transporters and metabolic regulation suited to comparatively warm ale fermentation.",
    "lager_yeast": "This S. pastorianus cell combines ancestry from two Saccharomyces species and performs well in cool lager fermentation.",
    "yeast_culturist": "The culturist counts stained cells in a hemocytometer, distinguishing cell number from the fraction still viable.",
    "lipid_specialist": "A membrane model shows ergosterol and unsaturated fatty acids controlling fluidity, permeability, and transporter function.",
    "maltose_permease": "The transmembrane carrier couples downhill proton movement to uphill maltose uptake across the yeast plasma membrane.",
    "maltase": "The intracellular alpha-glucosidase closes around maltose and hydrolyzes its glycosidic bond to release two glucose molecules.",
    "alpha_acetolactate": "This unstable branched-chain-amino-acid-pathway intermediate can escape the cell and form diacetyl by oxidative decarboxylation.",
    "alcohol_dehydrogenase": "The enzyme transfers reducing equivalents from NADH to acetaldehyde, producing ethanol while restoring NAD+ for glycolysis.",
    "ergosterol": "A rigid fungal sterol nests among membrane lipids, moderating membrane order much as cholesterol does in animal cells.",
    "ester_chemist": "Standards of isoamyl acetate and ethyl acetate accompany pathways that join alcohol-derived and acyl groups into volatile esters.",
    "diacetyl_molecule": "Two adjacent carbonyl groups give this small vicinal diketone a striking buttery aroma at low concentration.",
    "hydrogen_sulfide": "A tiny volatile sulfur compound emerges from yeast sulfur metabolism with the unmistakable warning of rotten eggs.",
    "dms_molecule": "Dimethyl sulfide rises readily from warm wort and evokes cooked corn or vegetables rather than hydrogen sulfide's rotten egg.",
    "sulfur_engineer": "The engineer sorts sulfur aromas by identity, source, timing, volatility, yeast health, and boil performance before proposing a remedy.",
    "cellar_manager": "Gravity curves, temperature traces, pitch records, and sensory notes let the manager distinguish slow fermentation from a truly stalled batch.",
    "maturation_operator": "The operator schedules warm cleanup before cooling so metabolically active yeast can reduce diacetyl and other intermediates.",
    "cold_keeper": "The keeper lowers temperature only after fermentation and cleanup goals are met, promoting settling and lager maturation.",
    "hop_breeder": "The breeder crosses selected plants for resin and oil profiles, disease resistance, yield, and adaptation while propagating desired females clonally.",
    "hop_grower": "The grower trains clockwise-climbing bines and inspects papery female cones for maturity and damage.",
    "lupulin_keeper": "Yellow resinous glands at the base of cone bracts hold alpha acids, beta acids, and concentrated essential oils.",
    "humulone": "The principal hop alpha acid displays an acylphloroglucinol framework poised to rearrange under kettle heat.",
    "isomerization_chemist": "Structural diagrams trace humulone's heat-driven rearrangement into more soluble cis- and trans-iso-alpha-acid products.",
    "myrcene": "This volatile terpene hydrocarbon contributes fresh hop aroma but readily escapes with steam during a long boil.",
    "ibu_chemist": "The chemist extracts bitter compounds and reads absorbance near 275 nm, while noting that the result does not equal perceived bitterness.",
    "dry_hopper": "The brewer adds hops after the kettle, protecting many volatiles while monitoring oxygen pickup, extraction, and possible hop creep.",
    "light_tester": "A shielded chamber exposes matched beer samples to controlled wavelengths so lightstruck chemistry can be separated from oxidation.",
    "riboflavin": "The yellow flavin absorbs visible light and enters an excited state capable of initiating hop-derived sulfur photochemistry.",
    "mbt_molecule": "3-methyl-2-butene-1-thiol is a potent sulfur odorant whose skunky aroma is detectable at extraordinarily low concentration.",
    "brite_operator": "The operator confirms clarity, temperature, carbonation readiness, and dissolved oxygen before releasing beer to packaging.",
    "carbonation_operator": "A pressure-temperature chart guides CO2 dissolution; cold beer reaches a higher dissolved concentration at the same pressure.",
    "bottle_conditioner": "A small viable yeast population consumes measured priming sugar in the sealed bottle, trapping fermentation CO2.",
    "can_specialist": "The specialist measures seam overlap, oxygen pickup, fill height, and lid integrity on an opaque light-blocking package.",
    "nitrogen_operator": "A restrictor plate shears low-solubility nitrogen from solution into many fine bubbles that build a dense creamy head.",
    "ltp1": "Barley lipid-transfer protein 1 survives brewing in modified forms that can migrate to bubble surfaces and support foam.",
    "protein_z": "This heat-stable barley serpin persists into beer and contributes to the protein network associated with foam stability.",
    "sensory_analyst": "Identically coded glasses, randomized serving order, and aroma references help the analyst separate observation from expectation.",
    "style_judge": "The judge links sensory traits to ingredients, yeast strain, fermentation temperature, attenuation, maturation, and serving practice.",
    "taproom_manager": "The manager compares beer temperature, gas pressure, faucet condition, glass cleanliness, and foam behavior before blaming the recipe.",
    "glass_steward": "Under angled light, the steward finds grease and detergent films that disrupt the protein-stabilized walls between bubbles.",
    "cold_storekeeper": "A continuous temperature logger reveals every warm excursion that could accelerate packaged-beer staling.",
    "packaging_lead": "The lead tracks dissolved oxygen, total package oxygen, seam or closure integrity, fill level, light exposure, and sanitation together.",
    "microbiologist": "The microbiologist compares colony morphology, microscopy, acid production, and carbohydrate use to identify brewery isolates.",
    "lactic_bacterium": "A small Gram-positive cell converts carbohydrate to lactic acid but faces inhibition from hop iso-alpha acids in many beers.",
    "wild_yeast": "The isolate carries metabolic capabilities absent from the production strain and may continue consuming residual carbohydrate in package.",
    "sanitation_lead": "The lead opens a transfer fitting to expose hidden soil, demonstrating why sanitizer cannot compensate for inadequate cleaning.",
    "qa_chemist": "Control charts and instrument logs let the chemist ask whether a surprising number reflects the beer, the sample, the method, or transcription.",
    "yeast_banker": "Barcoded cryovials preserve authenticated master cultures so production does not depend on endless repitching and accumulated drift.",
    "pilot_brewer": "A small instrumented brewhouse reproduces production variables while limiting the cost of a failed trial.",
    "instructor": "The instructor annotates a batch record with links among raw materials, time, temperature, pH, gravity, cell health, and sensory outcome.",
}


_npc_home = {npc: room for room, residents in PLACEMENTS.items() for npc in residents}
_room_fact = {room: fact for room, _name, _feature, fact in ROOM_DATA}


def npc_dialogue(key: str, name: str) -> str:
    return f'“{_room_fact[_npc_home[key]].rstrip(".")},” says {name}.'


NPCS = {
    key: NPC(key, name, aliases(key, name),
             NPC_DESCRIPTIONS[key],
             npc_dialogue(key, name))
    for key, name in NAMES.items()
}


FACTS = {key: fact for key, _name, _feature, fact in ROOM_DATA}
ITEMS: dict[str, tuple[str, str]] = {}


_room_info = {key: (name, feature, fact) for key, name, feature, fact in ROOM_DATA}
_exits: dict[str, dict[str, str]] = {key: {} for key in _room_info}
_opposite = {"north":"south", "south":"north", "east":"west", "west":"east", "up":"down", "down":"up", "in":"out", "out":"in"}


def connect(a: str, direction: str, b: str) -> None:
    reverse = _opposite[direction]
    if direction in _exits[a] or reverse in _exits[b]:
        raise ValueError(f"Conflicting connection: {a} {direction} {b}")
    _exits[a][direction] = b
    _exits[b][reverse] = a


def grid(rows: tuple[tuple[str, ...], ...]) -> None:
    for row in rows:
        for left, right in zip(row, row[1:]):
            connect(left, "east", right)
    for upper, lower in zip(rows, rows[1:]):
        for a, b in zip(upper, lower):
            connect(a, "south", b)


grid((("grain_receiving","barley_lab","steep_house","air_rest","germination_floor"),
      ("brewery_gate","cure_floor","kiln","endosperm","aleurone")))
grid((("water_lab","ph_bench","ion_gallery","city_profiles"),
      ("treatment_bay","mill_room","mash_tun","protein_rest"),
      ("beta_rest","alpha_rest","conversion_bench","mash_out")))
grid((("lauter_tun","grain_bed","sparge_arm","wort_grant","kettle"),
      ("hot_break","hop_dosing","whirlpool","heat_exchanger","oxygenation_station")))
grid((("pitching_deck","ale_fermenter","lager_fermenter","yeast_lab","yeast_membrane","maltose_gate","maltase_bench"),
      ("glycolysis_lane","nad_recycling","lipid_workshop","ester_lab","diacetyl_rest","sulfur_vent","maturation_cellar")))
grid((("hop_yard","female_cone","lupulin_gland","alpha_acid_bench"),
      ("oil_lab","ibu_station","dry_hop_gallery","lightstrike_booth")))
grid((("brite_tank","carbonation_station","bottle_line","canning_line","nitrogen_tap"),
      ("foam_lab","sensory_room","style_taproom","cold_storage","shipping_dock")))
grid((("microbiology_lab","sanitation_bay","qa_chemistry"),
      ("yeast_bank","pilot_brewery","training_classroom")))

# Regional transitions follow the production process and add useful shortcuts.
connect("germination_floor", "down", "water_lab")
connect("mash_out", "down", "lauter_tun")
connect("oxygenation_station", "down", "pitching_deck")
connect("hop_dosing", "in", "alpha_acid_bench")
connect("maturation_cellar", "down", "brite_tank")
connect("style_taproom", "down", "qa_chemistry")
connect("yeast_lab", "in", "microbiology_lab")
connect("shipping_dock", "out", "brewery_gate")


ROOMS = {}
for key, (name, feature_name, fact) in _room_info.items():
    feature = Feature(feature_name, (feature_name.casefold(), *feature_name.casefold().split()), fact, key)
    ROOMS[key] = Room(key, name, fact, _exits[key], (feature,), PLACEMENTS.get(key, ()))


AMBIENT_SPEECH = {
    "brewery_gate": 'The Training Coordinator calls, “Talk to me when you are ready to get started.”',
    "cure_floor": 'The Head Maltster mutters, “Another uneven lot. I could use a biochemist.”',
    "water_lab": 'The Water Chemist says, “Never copy a city profile without asking what each ion is doing.”',
    "mash_tun": 'The Head Brewer frowns at an iodine test. “Conversion should be further along.”',
    "lauter_tun": 'The Lauter Operator complains, “The runoff is slowing again.”',
    "kettle": 'The Kettle Brewer says, “All those hops, and the aroma still vanished.”',
    "maturation_cellar": 'The Cellar Manager calls, “I have a fermentation that stopped early.”',
    "diacetyl_rest": 'Diacetyl announces, “Butter, butterscotch—I do make an entrance.”',
    "sulfur_vent": 'The Sulfur Engineer says, “Rotten eggs and cooked corn are different clues.”',
    "hop_yard": 'The Hop Breeder waves from beneath the bines. “Mind the training wires.”',
    "lightstrike_booth": 'A warning lamp flashes: PROTECT HOPPED BEER FROM LIGHT.',
    "sensory_room": 'The Sensory Analyst says, “I have a buttery sample that needs tracing.”',
    "style_taproom": 'The Taproom Manager sighs, “This pint cannot hold a head.”',
    "shipping_dock": 'The Packaging Lead holds up a skunky display canary sample. “Light found this one.”',
    "microbiology_lab": 'The Microbiologist says, “Something uninvited kept fermenting in package.”',
    "qa_chemistry": 'The QA Chemist says, “This batch record does not agree with the beer. I need an independent investigation.”',
}
