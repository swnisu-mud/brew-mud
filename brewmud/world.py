"""The BrewMUD world: connected locations from grain receiving to taproom."""

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
    ("carbohydrate_lab", "Carbohydrate and Starch Laboratory", "molecular sorting board", "Carbohydrates are classified by their component monosaccharides, glycosidic linkages, chain architecture, and resulting physical properties."),
    ("glucose_bench", "Glucose Bench", "glucose model", "Glucose is a monosaccharide: one sugar unit that serves both as a biological fuel and as the repeating building block of barley starch."),
    ("disaccharide_gallery", "Disaccharide Gallery", "paired sugar models", "Maltose contains two glucose units, sucrose contains glucose plus fructose, and lactose contains glucose plus galactose; all are distinct disaccharides."),
    ("polymer_comparison", "Glucose-Polymer Comparison Hall", "linkage comparison", "Starch, glycogen, and cellulose are all glucose polymers, but differences in linkage and branching produce very different structures and biological roles."),
    ("gelatinization_chamber", "Gelatinization Chamber", "heated hydration cell", "Heating starch in water disrupts ordered granule packing and permits hydration, making glucan chains more accessible to amylases without itself hydrolyzing them."),
    ("crystallinity_lab", "Starch Crystallinity Laboratory", "diffraction pattern", "Hydrogen-bonded packing can exclude water and form starch crystallites that resist amylase access until sufficient heat and hydration disrupt them."),
    ("amylose_helix", "Amylose Helix Walk", "helical chain model", "Amylose is a mostly unbranched polymer of alpha-1,4-linked glucose that can coil into a hydrogen-bonded left-handed helix."),
    ("amylopectin_arbor", "Amylopectin Branching Arbor", "branch-point model", "Amylopectin forms most barley starch and contains alpha-1,4-linked glucose chains joined by alpha-1,6 branch points roughly every few dozen residues."),
    ("protein_rest", "Protein Rest", "protease window", "Proteases are most useful below typical saccharification temperatures and can affect FAN, haze, and foam-active proteins."),
    ("beta_rest", "Beta-Amylase Rest", "maltose assay", "Beta-amylase attacks nonreducing ends to release maltose and is less heat-stable than alpha-amylase."),
    ("alpha_rest", "Alpha-Amylase Rest", "dextrin trace", "Alpha-amylase makes internal alpha-1,4 cleavages, rapidly lowering viscosity and producing dextrins of varied size."),
    ("conversion_bench", "Starch Conversion Bench", "iodine plate", "Gelatinization disrupts ordered starch granules and improves enzyme access to amylose and amylopectin."),
    ("mash_out", "Mash-Out Platform", "mash-out gauge", "Heating for mash-out reduces viscosity and largely arrests the enzyme balance established during the mash."),

    ("amino_acid_gallery", "Amino Acid Gallery", "side-chain display", "Proteins are linear heteropolymers assembled from the same twenty amino-acid building blocks, whose varied side chains give proteins their chemical diversity."),
    ("peptide_bond_bench", "Peptide Bond Bench", "condensation model", "Peptide bonds join amino acids into polypeptides; peptide-bond hydrolysis is the reverse chemical process and is accelerated by proteases."),
    ("protein_structure_gallery", "Protein Structure Gallery", "four-level model", "Primary structure is amino-acid sequence, secondary structure is local alpha-helix or beta-sheet folding, tertiary structure is the global fold, and quaternary structure is subunit assembly."),
    ("folding_chamber", "Protein Folding Chamber", "folding cage", "Hydrophobic collapse tends to bury nonpolar side chains and expose polar groups to water, while chaperones limit inappropriate contacts and aggregation during folding."),
    ("denaturation_bay", "Denaturation and Aggregation Bay", "heat-treated protein sample", "Heat or extreme chemical conditions can disrupt a protein's higher-order structure without normally breaking its peptide backbone, causing loss of function and sometimes aggregation."),
    ("enzyme_catalysis_lab", "Enzyme Catalysis Laboratory", "energy-profile diagram", "Enzymes accelerate reactions by lowering activation energy; they do not change the reaction equilibrium or the overall free-energy difference between reactants and products."),
    ("active_site_workshop", "Active-Site Workshop", "substrate-binding pocket", "An enzyme active site uses a small subset of amino acids to bind and orient substrates and to perform catalysis, producing strong substrate selectivity and reaction specificity."),
    ("enzyme_conditions_lab", "Enzyme Conditions Laboratory", "temperature and pH chart", "Brewing enzymes have different useful ranges: beta-glucanase about 98–113°F, proteases 115–135°F, beta-amylase 130–150°F, and alpha-amylase 155–167°F, each with its own pH range."),
    ("amylase_mechanism_lab", "Amylase Mechanism Laboratory", "endo-exo chain model", "Alpha-amylase is an endo-acting enzyme that liquefies starch into shorter dextrins, whereas beta-amylase works from nonreducing ends to release maltose during saccharification."),
    ("mash_thickness_station", "Mash-Thickness Control Station", "liquor-to-grist gauges", "A very thick mash can inhibit beta-amylase as maltose accumulates, while an excessively thin mash dilutes protective barley phosphate and can reduce amylase stability."),
    ("accessory_enzyme_lab", "Accessory Enzyme Laboratory", "enzyme dosing cabinet", "Beta-glucanase reduces gummy cell-wall glucans, proteases hydrolyze proteins, and glucoamylase can cleave alpha-1,4 and alpha-1,6 linkages to produce highly fermentable glucose."),
    ("iodine_test_alcove", "Starch–Iodine Test Alcove", "blue-black assay", "Linear triiodide fits within the amylose helix to form a blue-black complex, so loss of that color is used to follow the disappearance of longer starch chains during mashing."),

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
    "carbohydrate_lab": ("carbohydrate_curator",), "glucose_bench": ("glucose",),
    "disaccharide_gallery": ("maltose", "sucrose", "lactose"),
    "polymer_comparison": ("glycogen", "cellulose"),
    "gelatinization_chamber": ("gelatinization_specialist", "grain_stress_agronomist"),
    "crystallinity_lab": ("crystallinity_analyst",),
    "amylose_helix": ("amylose",), "amylopectin_arbor": ("amylopectin",),
    "beta_rest": ("beta_amylase",), "alpha_rest": ("alpha_amylase",),
    "conversion_bench": ("gelatinized_starch",), "mash_out": ("mash_out_operator",),
    "amino_acid_gallery": ("protein_chemist", "amino_acid_guide"),
    "peptide_bond_bench": ("peptide_bond",),
    "protein_structure_gallery": ("protein_architect",),
    "folding_chamber": ("molecular_chaperone",),
    "denaturation_bay": ("denatured_protein",),
    "enzyme_catalysis_lab": ("enzyme_catalyst",),
    "active_site_workshop": ("active_site",),
    "enzyme_conditions_lab": ("condition_controller",),
    "amylase_mechanism_lab": ("amylase_mechanist",),
    "mash_thickness_station": ("mash_thickness_technician",),
    "accessory_enzyme_lab": ("beta_glucanase", "glucoamylase"),
    "iodine_test_alcove": ("iodine_analyst",),
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
    "carbohydrate_curator":"Carbohydrate Curator", "glucose":"Glucose", "sucrose":"Sucrose", "lactose":"Lactose",
    "maltose":"Maltose", "glycogen":"Glycogen", "cellulose":"Cellulose", "gelatinization_specialist":"Gelatinization Specialist",
    "grain_stress_agronomist":"Grain-Stress Agronomist",
    "crystallinity_analyst":"Crystallinity Analyst", "amylose":"Amylose", "amylopectin":"Amylopectin",
    "gelatinized_starch":"Gelatinized Starch", "mash_out_operator":"Mash-Out Operator", "lauter_operator":"Lauter Operator",
    "protein_chemist":"Protein Chemist", "amino_acid_guide":"Amino Acid Guide", "peptide_bond":"Peptide Bond",
    "protein_architect":"Protein Architect", "molecular_chaperone":"Molecular Chaperone", "denatured_protein":"Denatured Protein",
    "enzyme_catalyst":"Enzyme Catalyst", "active_site":"Active Site", "condition_controller":"Enzyme-Condition Controller",
    "amylase_mechanist":"Amylase Mechanist", "mash_thickness_technician":"Mash-Thickness Technician",
    "beta_glucanase":"Beta-Glucanase", "glucoamylase":"Glucoamylase", "iodine_analyst":"Iodine-Test Analyst",
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
    "carbohydrate_curator": "The curator stands beside molecular models from single sugar rings to million-residue polymers, sorting them by composition, linkage, and branching rather than by name alone.",
    "glucose": "A single hexose ring marks the monosaccharide that supplies carbon and energy to cells and repeats thousands of times within barley starch.",
    "maltose": "Two glucose units joined by an alpha-1,4 glycosidic bond form the fermentable disaccharide released repeatedly by beta-amylase from starch-chain ends.",
    "sucrose": "A glucose unit and a fructose unit meet across the glycosidic bond of this common table-sugar disaccharide.",
    "lactose": "A galactose unit joined to glucose forms this milk-sugar disaccharide, chemically distinct from sucrose despite sharing the same broad classification.",
    "glycogen": "A densely branched alpha-glucose polymer displays more frequent branch points than amylopectin, allowing animals to mobilize stored glucose rapidly.",
    "cellulose": "Long beta-1,4-linked glucose chains align into straight, hydrogen-bonded bundles that provide structural strength to plant cell walls.",
    "gelatinization_specialist": "The specialist tracks granule swelling and loss of ordered structure as heat allows water to penetrate between starch chains.",
    "grain_stress_agronomist": "Field-temperature and drought records sit beside starch tests showing how the environment during grain filling can alter granule crystallinity and gelatinization temperature.",
    "crystallinity_analyst": "Diffraction traces and hydration measurements reveal ordered, hydrogen-bonded regions that exclude water and limit amylase access.",
    "amylose": "A mostly unbranched alpha-1,4 glucan winds into a left-handed helix whose aligned chains can form enzyme-resistant crystalline regions.",
    "amylopectin": "A vast alpha-glucose polymer extends through many alpha-1,4 chains connected by alpha-1,6 branch points, accounting for most ordinary starch.",
    "protein_chemist": "The chemist compares a heat-damaged enzyme sample with an intact control while tracing how amino-acid sequence supports a functional three-dimensional fold.",
    "amino_acid_guide": "Twenty standard amino-acid models share a common backbone but display chemically varied side chains, the source of much protein structural and functional diversity.",
    "peptide_bond": "A planar covalent linkage joins the carbonyl carbon of one amino-acid residue to the nitrogen of the next along a polypeptide backbone.",
    "protein_architect": "Nested models label amino-acid sequence, local helices and sheets, a complete folded chain, and a multisubunit assembly as four distinct levels of protein structure.",
    "molecular_chaperone": "A chaperone encloses an exposed folding intermediate, limiting aggregation and inappropriate contacts without becoming part of the completed protein.",
    "denatured_protein": "The unfolded sample has lost the precise higher-order structure required for function, exposing hydrophobic surfaces that make aggregation increasingly likely.",
    "enzyme_catalyst": "An energy diagram beside the catalyst shows a lower transition-state barrier but unchanged reactant and product free energies and unchanged equilibrium.",
    "active_site": "A pocket on the protein surface positions substrate through multiple binding contacts while a smaller set of residues directly performs catalysis.",
    "condition_controller": "Four assay traces compare the distinct temperature and pH windows of beta-glucanase, proteases, beta-amylase, and alpha-amylase.",
    "amylase_mechanist": "A chain model contrasts alpha-amylase cutting internal alpha-1,4 bonds with beta-amylase removing maltose successively from nonreducing ends.",
    "mash_thickness_technician": "Side-by-side mashes show maltose product inhibition in a concentrated mash and reduced phosphate protection in an excessively diluted mash.",
    "beta_glucanase": "The enzyme hydrolyzes beta-linked barley cell-wall glucans whose persistence can raise viscosity and produce a gummy, difficult-to-lauter mash.",
    "glucoamylase": "This added enzyme works from glucan ends and can hydrolyze both alpha-1,4 and alpha-1,6 linkages, converting dextrins toward glucose and very high fermentability.",
    "iodine_analyst": "The analyst compares blue-black starch-positive samples with converted controls while a molecular model places linear triiodide inside an amylose helix.",
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


# Spoken observations are deliberately different from both room summaries and
# LOOK descriptions. The first study unit receives fully authored dialogue;
# later residents use an educational fallback until their course unit is tuned.
NPC_DIALOGUE = {
    "training_coordinator": "Start with the grain. If you can explain what changes inside a kernel, the choices made later in the mash will make much more sense.",
    "barley_inspector": "I sample kernels from several parts of the load; one convenient handful can hide differences in moisture, protein, size, and germination capacity.",
    "two_row_kernel": "My embryo is alive, my endosperm stores starch and protein, and my aleurone will help mobilize those reserves when germination begins.",
    "steep_master": "Water wakes the kernel, but continuous submersion can starve it of oxygen. That is why I alternate wet steeps with air rests.",
    "oxygen_sensor": "A declining oxygen reading is metabolic evidence: these kernels are respiring, and they need drainage and aeration before oxygen becomes limiting.",
    "gibberellic_acid": "I carry the embryo's signal to the aleurone; I do not digest starch myself, but I trigger cells that produce the required hydrolases.",
    "aleurone_cell": "When gibberellin reaches me, I increase synthesis and secretion of alpha-amylase, proteases, and enzymes that open the endosperm matrix.",
    "starch_granule": "My glucose is densely packed as amylose and amylopectin. Modification and later gelatinization determine how easily amylases can reach it.",
    "kiln_operator": "I dry gently at first to preserve enzyme activity, then use the curing schedule to develop the malt's intended color and flavor.",
    "head_maltster": "Good malt is not simply germinated grain. I stop growth when modification is sufficient, before the embryo consumes too much extract.",
    "water_chemist": "Do not confuse starting-water pH with alkalinity. The grist reacts with the water, and that combined chemistry determines mash pH.",
    "ph_meter": "Cool and mix the sample before trusting me. Temperature, calibration, and poor sampling can turn a precise-looking number into a bad decision.",
    "bicarbonate": "I consume added acid and resist a pH decrease. That buffering behavior is why my concentration matters more than a casual hard-water label.",
    "calcium_ion": "I can promote phosphate reactions that lower mash pH, support yeast and flocculation later, and help stabilize alpha-amylase during heating.",
    "sulfate_ion": "I can sharpen the impression of hop bitterness and dryness, but I do not create bitterness by myself and too much may taste harsh.",
    "chloride_ion": "Brewers use me to support fullness and malt emphasis. Think of sulfate-to-chloride balance as a sensory tool, not a rigid recipe law.",
    "burton_guide": "Historic water profiles explain adaptations, not commandments. Modern treatment lets a brewer choose chemistry for the beer rather than imitate a city blindly.",
    "treatment_chemist": "Name the problem before choosing the treatment: carbon, acid, salts, dechlorination, and reverse osmosis solve different chemical problems.",
    "miller": "I want fractured endosperm and recognizable husk pieces. Intact kernels hide extract, while excessive flour can make lautering painfully slow.",
    "head_brewer": "Mash temperature is a choice about enzyme survival and product distribution, not merely a number to hit on the thermometer.",
    "carbohydrate_curator": "Calling everything here a sugar hides the useful distinctions. Count the sugar units, identify their monomers, then inspect the bonds and branches.",
    "glucose": "I am one monosaccharide, not a short starch. Link many copies of me in different ways and you can build amylose, amylopectin, glycogen, or cellulose.",
    "maltose": "I am two glucose units joined alpha-1,4. Beta-amylase releases me from nonreducing starch-chain ends, making me especially relevant to wort fermentability.",
    "sucrose": "I pair glucose with fructose. Lactose is also a disaccharide, but its second unit is galactose, so the two names are not interchangeable.",
    "lactose": "I am milk sugar: galactose linked to glucose. My presence here is comparative—the principal extract from malt is not lactose.",
    "glycogen": "Animals store glucose in my highly branched chains. I resemble amylopectin, but my branch points occur more frequently.",
    "cellulose": "My glucose units use beta-1,4 linkages. That geometry makes straight structural chains that brewing amylases cannot treat like alpha-linked starch.",
    "gelatinization_specialist": "Heat does not convert starch into sugar by itself. Heat and water disrupt ordered packing so amylases can reach bonds they can hydrolyze.",
    "grain_stress_agronomist": "Heat and drought during starch formation can raise barley's gelatinization temperature. If access comes only after amylases are damaged, the malt may struggle to self-convert.",
    "crystallinity_analyst": "When aligned starch chains hydrogen-bond tightly, they exclude water and resist enzymes. A warmer, well-hydrated granule loses that order.",
    "amylose": "Most of my glucose units form one alpha-1,4-linked chain. I can coil into a left-handed helix and pack with neighboring chains.",
    "amylopectin": "I usually make up seventy to eighty percent of starch. My alpha-1,6 branches interrupt an alpha-1,4-linked backbone and create many chain ends.",
    "protein_chemist": "An enzyme is a protein whose activity depends on its structure. Trace how the amino-acid chain folds before deciding what the heat pulse did to this sample.",
    "amino_acid_guide": "Every protein is a linear heteropolymer built from the same set of twenty amino acids. Their different side chains make one sequence behave unlike another.",
    "peptide_bond": "I connect amino-acid residues into a polypeptide. Proteases catalyze my hydrolysis; ordinary protein denaturation usually leaves me intact.",
    "protein_architect": "Primary means sequence, secondary means local helices and sheets, tertiary means one chain's global fold, and quaternary means multiple subunits assembled together.",
    "molecular_chaperone": "I prevent exposed folding intermediates from aggregating and help them reach or recover useful conformations, especially during cellular stress.",
    "denatured_protein": "Heat disrupted the weak interactions maintaining my fold. My sequence remains, but my active shape and function are gone, and my exposed surfaces may stick together.",
    "enzyme_catalyst": "I lower activation energy and accelerate approach to equilibrium. I do not make an unfavorable equilibrium favorable or change the reaction's overall free-energy difference.",
    "active_site": "Only a few residues may perform chemistry, while others bind and orient the substrate. Shape and chemical complementarity help enzymes discriminate among similar molecules.",
    "condition_controller": "The useful windows rise from beta-glucanase to protease to beta-amylase to alpha-amylase. A temperature that favors one activity may rapidly damage another enzyme.",
    "amylase_mechanist": "Alpha-amylase cuts inside and liquefies starch into dextrins. Beta-amylase works from nonreducing ends, saccharifying those chains into maltose but unfolding at lower temperatures.",
    "mash_thickness_technician": "Too thick, and accumulated maltose can compete at beta-amylase's active site. Too thin, and protective phosphate is diluted; calcium and ionic conditions also affect stability.",
    "beta_glucanase": "I work near 98 to 113 degrees Fahrenheit to reduce gummy beta-glucans. Most are removed during malting, but a stubborn remainder can obstruct the mash and runoff.",
    "glucoamylase": "Unlike the malt amylases, I can drive dextrins nearly to glucose by attacking alpha-1,4 and branch-point alpha-1,6 linkages, producing a very dry beer.",
    "iodine_analyst": "The blue-black signal arises when linear triiodide occupies an amylose helix. As long chains disappear, the assay loses that characteristic color.",
    "protease": "At a suitable lower-temperature rest I release peptides and amino nitrogen, but an unnecessary or excessive rest can weaken foam-supporting proteins.",
    "beta_amylase": "Give me accessible nonreducing chain ends and moderate heat, and I release maltose repeatedly until a branch or damaged activity stops me.",
    "alpha_amylase": "I cut alpha-1,4 bonds within starch chains. Those internal cleavages reduce viscosity and create additional ends for other enzymes to use.",
    "gelatinized_starch": "Heat and water disrupted my ordered granule, so flexible glucan chains are now exposed. Gelatinization enables access; it is not itself hydrolysis.",
    "mash_out_operator": "I raise the temperature after the desired fermentability is established, reducing viscosity while largely freezing the enzyme balance in place.",
    "lauter_operator": "The false bottom supports the grain, but the husk bed performs most of the filtration. Flow too aggressively and that bed compacts.",
    "husk_keeper": "My overlapping pieces preserve channels through the bed. Pulverize me in the mill and flour will occupy the spaces wort needs for runoff.",
    "sparge_technician": "I rinse retained extract gently and evenly. Excess heat, high pH, or too much sparge water can extract compounds the brewer did not want.",
    "vorlauf_guide": "The first runnings carry particles, so I return them above the bed. Clarity improves as the grain establishes its own filter structure.",
}


def npc_dialogue(key: str, name: str) -> str:
    dialogue = NPC_DIALOGUE.get(key)
    if dialogue:
        return f'“{dialogue.rstrip(".")},” says {name}.'
    return f'{name} adds a technical observation: “{NPC_DESCRIPTIONS[key]}”'


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
grid((("carbohydrate_lab","glucose_bench","disaccharide_gallery","polymer_comparison"),
      ("gelatinization_chamber","crystallinity_lab","amylose_helix","amylopectin_arbor")))
grid((("amino_acid_gallery","peptide_bond_bench","protein_structure_gallery","folding_chamber","denaturation_bay","enzyme_catalysis_lab"),
      ("active_site_workshop","enzyme_conditions_lab","amylase_mechanism_lab","mash_thickness_station","accessory_enzyme_lab","iodine_test_alcove")))
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
connect("mash_tun", "in", "carbohydrate_lab")
connect("gelatinization_chamber", "out", "conversion_bench")
connect("protein_rest", "in", "amino_acid_gallery")
connect("amylase_mechanism_lab", "out", "beta_rest")
connect("iodine_test_alcove", "out", "alpha_rest")
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
    "carbohydrate_lab": 'The Carbohydrate Curator calls, “Before we diagnose the mash, rebuild this molecular map.”',
    "amino_acid_gallery": 'The Protein Chemist calls, “A heat pulse silenced this enzyme panel. Help me determine exactly what was lost.”',
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
