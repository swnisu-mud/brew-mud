"""Data-driven non-combat quests. Add content here without changing the engine."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    action: str                 # talk or escort
    target: str
    objective: str
    result: str
    destination: str | None = None


@dataclass(frozen=True)
class Quest:
    title: str
    giver: str
    offer: str
    steps: tuple[Step, ...]
    reward: int = 25
    requires: tuple[str, ...] = ()


def T(target: str, objective: str, result: str) -> Step:
    return Step("talk", target, objective, result)


def E(target: str, destination: str, objective: str, result: str) -> Step:
    return Step("escort", target, objective, result, destination)


QUESTS: dict[str, Quest] = {
    "orientation": Quest("First Day in the Brewery", "training_coordinator",
        "“A brewery is a linked biochemical system, not just a row of tanks. Meet each department lead and trace grain-to-glass production,” says the Training Coordinator.", (
        T("head_maltster", "Find and meet the Head Maltster.", "Malting makes stored reserves accessible while preserving useful enzymes."),
        T("water_chemist", "Find and meet the Water Chemist.", "Water establishes the chemical environment for mash enzymes, yeast, and flavor."),
        T("lauter_operator", "Find and meet the Lauter Operator.", "Lautering separates sweet wort from spent grain through a permeable husk bed."),
        T("cellar_manager", "Find and meet the Cellar Manager.", "Healthy yeast transform wort chemistry into beer chemistry."),
        T("hop_breeder", "Find and meet the Hop Breeder.", "Hop genetics influence acids, oils, disease resistance, and agronomic traits."),
        T("packaging_lead", "Find and meet the Packaging Lead.", "Packaging must preserve the beer against oxygen, light, and contamination."),
        T("training_coordinator", "Return to the Training Coordinator.", "“Now follow the problems. Every department has work for a biochemist.”")), 30),

    "malt_house": Quest("Wake the Sleeping Grain", "head_maltster",
        "“This lot is germinating unevenly. Trace the signal from hydrated embryo to starch-degrading enzymes,” says the Head Maltster.", (
        T("barley_inspector", "Ask the Barley Inspector about the grain.", "Uneven kernels hydrate unevenly; two-row barley is valued in part for kernel uniformity."),
        T("gibberellic_acid", "Find the gibberellic-acid messenger.", "Gibberellic acid carries the embryo's signal toward the aleurone."),
        T("aleurone_cell", "Ask the Aleurone Cell how it responds.", "The aleurone synthesizes and secretes hydrolytic enzymes including alpha-amylase and proteases."),
        T("starch_granule", "Check modification in the endosperm.", "Cell walls and storage material are opening to enzyme access."),
        E("beta_amylase", "head_maltster", "Escort Beta-Amylase's assay sample to the Head Maltster.", "The assay is sound. Inconsistent steeping, not absent enzyme, caused the patchy modification.")), 35),

    "water_profile": Quest("A Tale of Two Ions", "water_chemist",
        "“The pilot pale ale tastes sharp and thin. Build a useful profile from chemistry, not merely a city name,” says the Water Chemist.", (
        T("ph_meter", "Check mash pH.", "The pH is outside the most useful mash range."),
        T("bicarbonate", "Consult Bicarbonate.", "Alkalinity resists a fall in pH; it is not identical to hardness."),
        T("calcium_ion", "Ask Calcium about mash effects.", "Calcium can help reduce mash pH and stabilize alpha-amylase."),
        T("sulfate_ion", "Ask Sulfate about flavor.", "Sulfate emphasizes bitterness and dryness; excess can seem harsh."),
        T("chloride_ion", "Ask Chloride about flavor.", "Chloride tends to emphasize fullness and apparent sweetness."),
        T("water_chemist", "Return with a balanced recommendation.", "The chemist corrects alkalinity first, then adjusts sulfate and chloride deliberately.")), 35),

    "stalled_mash": Quest("The Stalled Mash", "head_brewer",
        "An iodine-dark sample worries the Head Brewer. “Decide whether access, temperature, pH, or enzyme activity is responsible.”", (
        T("miller", "Ask whether milling exposed the endosperm.", "The crush exposed starch while retaining husk pieces for the filter bed."),
        T("gelatinized_starch", "Check starch accessibility.", "The swollen granules have lost ordered structure and expose glucan chains."),
        T("beta_amylase", "Consult Beta-Amylase.", "Beta-amylase releases maltose from nonreducing ends but is relatively heat-sensitive."),
        T("alpha_amylase", "Consult Alpha-Amylase.", "Alpha-amylase cleaves internal alpha-1,4 bonds, lowers viscosity, and creates varied dextrins."),
        T("ph_meter", "Verify mash pH.", "The pH is corrected into the useful enzyme range."),
        T("head_brewer", "Return with the diagnosis.", "A hot dough-in damaged beta-amylase activity; the wort will be less fermentable and fuller-bodied than planned.")), 40),

    "clear_wort": Quest("The Stuck Runoff", "lauter_operator",
        "“The grant slowed to a trickle. Find out whether the bed needs patience, recirculation, or gentler sparging,” says the Lauter Operator.", (
        T("husk_keeper", "Examine the husk-supported bed.", "Intact husks make channels; excess flour and compaction obstruct them."),
        T("vorlauf_guide", "Ask about recirculation.", "Vorlauf returns cloudy first wort until the grain bed becomes an effective filter."),
        T("sparge_technician", "Check sparge flow.", "Overly aggressive flow disturbed and compacted the bed."),
        E("sparge_technician", "lauter_operator", "Escort the Sparge Technician to the operator.", "They slow and redistribute flow. Clear sweet wort begins moving.")), 30),

    "hop_timing": Quest("The Vanishing Hop Aroma", "kettle_brewer",
        "“The recipe has plenty of hops but almost no aroma. Follow the molecules through heat and time,” says the Kettle Brewer.", (
        T("humulone", "Ask Humulone what boiling does.", "Heat isomerizes alpha acids into more soluble bitter iso-alpha acids."),
        T("isomerization_chemist", "Ask why early additions favor bitterness.", "Long hot contact promotes isomerization and bitterness extraction."),
        T("myrcene", "Ask Myrcene why aroma disappears.", "Many hop-oil components are volatile and leave during vigorous boiling."),
        T("dry_hopper", "Ask how to retain aroma.", "Late and dry-hop additions retain more volatile aroma than long kettle boils."),
        T("kettle_brewer", "Return with a revised schedule.", "The brewer separates early bittering, later flavor, and late or cold-side aroma additions.")), 35),

    "fermentation": Quest("Save the Stalled Fermentation", "cellar_manager",
        "“Gravity stopped falling. Diagnose the wort and cells before anyone dumps oxygen into finished beer,” says the Cellar Manager.", (
        T("qa_technician", "Verify gravity and sampling.", "A calibrated second reading confirms genuine residual extract."),
        T("yeast_culturist", "Check viability and pitch history.", "The cells were underpitched and depleted in membrane reserves."),
        T("maltose_permease", "Inspect maltose uptake.", "Maltose uses proton-linked transport; glucose repression delays the needed machinery."),
        T("maltase", "Ask how intracellular maltose is used.", "Maltase hydrolyzes maltose into two glucose molecules."),
        T("lipid_specialist", "Ask why early wort oxygen matters.", "Early oxygen supports sterol and unsaturated-fatty-acid synthesis; late oxygen encourages staling."),
        E("yeast_culturist", "cellar_manager", "Escort the Yeast Culturist to the Cellar Manager.", "They prepare an active culture and controlled recovery plan. Fermentation resumes without aerating the beer.")), 45),

    "diacetyl": Quest("Butter in the Cellar", "sensory_analyst",
        "The Sensory Analyst detects butter and butterscotch. “Trace the compound to its precursor and choose a biochemical remedy.”", (
        T("diacetyl_molecule", "Question Diacetyl.", "Diacetyl has a low flavor threshold and a buttery sensory character."),
        T("alpha_acetolactate", "Find alpha-acetolactate.", "Yeast-derived alpha-acetolactate can leave the cell and form diacetyl."),
        T("maturation_operator", "Ask about a diacetyl rest.", "Warm active yeast can take up diacetyl and reduce it to less flavor-active products."),
        E("maturation_operator", "sensory_analyst", "Escort the operator to the Sensory Analyst.", "They schedule a warm rest and repeat sensory checks before cooling.")), 32),

    "sulfur": Quest("The Sulfur Alarm", "sulfur_engineer",
        "“One sample smells like eggs; another like cooked vegetables. Separate their origins,” says the Sulfur Engineer.", (
        T("hydrogen_sulfide", "Identify the rotten-egg compound.", "Hydrogen sulfide can arise from yeast sulfur metabolism."),
        T("dms_molecule", "Identify the cooked-vegetable compound.", "Dimethyl sulfide derives in part from malt SMM chemistry."),
        T("boil_engineer", "Ask how boiling affects DMS.", "An open vigorous boil helps volatilize DMS; a weak or covered boil retains it."),
        T("sulfur_engineer", "Return with the diagnosis.", "The engineer treats yeast-related H2S and boil-related DMS as distinct problems.")), 30),

    "lightstruck": Quest("The Sunlit Six-Pack", "packaging_lead",
        "“A display batch became skunky. Reconstruct the photochemistry and recommend a package,” says the Packaging Lead.", (
        T("light_tester", "Test the beer in the lightstrike booth.", "Blue-visible and near-UV light reproduce the fault in susceptible hopped beer."),
        T("riboflavin", "Ask Riboflavin about its role.", "Excited riboflavin participates in sulfur-radical photochemistry."),
        T("mbt_molecule", "Identify the skunky product.", "3-methyl-2-butene-1-thiol has an extremely low sensory threshold."),
        T("can_specialist", "Ask about package protection.", "Opaque cans block the relevant light and can provide an excellent oxygen barrier."),
        T("packaging_lead", "Return with a recommendation.", "The lead moves the release to cans and tightens light-exposure controls.")), 35),

    "foam": Quest("The Headless Pint", "taproom_manager",
        "“This beer pours lively, then collapses. Investigate proteins, gas, and glass,” says the Taproom Manager.", (
        T("ltp1", "Ask LTP1 about foam.", "Heat-modified barley LTP1 can support foam, while lipids are often foam-negative."),
        T("protein_z", "Ask Protein Z about foam.", "Protein Z is another barley protein associated with foam stability."),
        T("carbonation_operator", "Check carbonation and serving temperature.", "Gas level, nucleation, pressure, and temperature influence the pour."),
        T("glass_steward", "Inspect the glassware.", "A thin grease film is destroying bubbles at the surface."),
        T("taproom_manager", "Return to the Taproom Manager.", "Clean glassware restores the head; protein and carbonation checks are logged for future batches.")), 35),

    "styles": Quest("Two Yeasts, Two Cellars", "style_judge",
        "“Use physiology and process—not stereotypes—to identify these ale and lager paths,” says the Style Judge.", (
        T("ale_yeast", "Interview the warm-fermenting yeast.", "S. cerevisiae commonly ferments ales warmer and may make prominent esters."),
        T("lager_yeast", "Interview the cool-fermenting yeast.", "S. pastorianus is a hybrid lager yeast adapted to cool fermentation."),
        T("ester_chemist", "Ask what controls esters.", "Strain, temperature, oxygenation, pitch rate, and wort composition all matter."),
        T("cold_keeper", "Ask what lagering accomplishes.", "Cold maturation supports clarification and flavor maturation."),
        T("style_judge", "Return with the identification.", "The judge accepts the process-based answer without pretending every ale or lager is chemically identical.")), 35),

    "sanitation": Quest("The Uninvited Fermenter", "microbiologist",
        "“A package is overcarbonated and unexpectedly sour. Trace possible contaminants and their route,” says the Microbiologist.", (
        T("lactic_bacterium", "Assess the lactic bacterium.", "Lactic acid bacteria can acidify beer; hop iso-alpha acids inhibit many Gram-positive strains."),
        T("wild_yeast", "Assess the wild yeast.", "The isolate can consume carbohydrate left by the production strain and continue making package gas."),
        T("sanitation_lead", "Audit cleaning records.", "A transfer fitting retained soil before sanitizer was applied."),
        E("sanitation_lead", "microbiologist", "Escort the Sanitation Lead to the lab.", "They quarantine the lot and distinguish removing soil by cleaning from reducing microbes by sanitizing.")), 38),

    "mystery_batch": Quest("The Batch That Does Not Add Up", "qa_chemist",
        "“The production sheet and finished beer disagree. Recheck the batch across departments and build an evidence-based diagnosis,” says the QA Chemist.", (
        T("ph_meter", "Verify the recorded mash pH.", "The archived pH value is valid and does not explain the discrepancy."),
        T("qa_technician", "Verify original and final gravity readings.", "A transcription error swapped two digits in the original-gravity entry."),
        T("ibu_chemist", "Check the bitterness assay.", "The absorbance-based IBU estimate is internally consistent, though it is not identical to perceived bitterness."),
        T("carbonation_operator", "Check package temperature and CO2 pressure.", "The beer warmed during measurement, explaining the apparently low dissolved CO2."),
        T("sensory_analyst", "Compare the corrected records with a blind sample.", "The sensory profile now agrees with the corrected analytical record."),
        T("qa_chemist", "Return to the QA Chemist with the complete diagnosis.", "“Good. No single measurement tells the whole story; traceable records and independent checks prevented a needless process change.”")), 40),
}

GIVER_QUESTS = {q.giver: key for key, q in QUESTS.items()}
