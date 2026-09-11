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
    lead: str = ""


def T(target: str, objective: str, result: str) -> Step:
    return Step("talk", target, objective, result)


def E(target: str, destination: str, objective: str, result: str) -> Step:
    return Step("escort", target, objective, result, destination)


QUESTS: dict[str, Quest] = {
    "orientation": Quest("First Day in the Brewery", "training_coordinator",
        "“A brewery is a linked biochemical system, not just a row of tanks. For your first assignment, trace grain from malting through mash separation,” says the Training Coordinator.", (
        T("head_maltster", "Find and meet the Head Maltster.", "“Ah, you found me! Welcome to the maltings. Before I can judge this batch, I need to know whether the incoming grain was uniform. Find the Barley Inspector and ask what varied across the load,” says the Head Maltster."),
        T("barley_inspector", "Find the Barley Inspector and ask what varied across the incoming grain.", "“I sampled across the load, not just from the top. Kernel size and moisture were consistent enough for even steeping. Next, ask the Water Chemist what chemical environment those kernels and their enzymes will encounter,” says the Barley Inspector."),
        T("water_chemist", "Find the Water Chemist and ask how water affects mashing.", "“The grist and water react together to establish mash pH. Once that environment is understood, the grain still needs physical access—ask the Miller how the crush exposes endosperm without destroying the husks,” says the Water Chemist."),
        T("miller", "Find the Miller and ask how the crush exposes endosperm.", "“The rollers opened the endosperm but left useful husk pieces. The Head Brewer can now explain how temperature and pH turn that access into a particular balance of sugars and dextrins,” says the Miller."),
        T("head_brewer", "Find the Head Brewer and ask how mash conditions control fermentability.", "“Mash conditions shift which enzymes survive and which products accumulate. When conversion is complete, the Lauter Operator must separate that dissolved extract from the grain bed,” says the Head Brewer."),
        T("lauter_operator", "Find the Lauter Operator and ask how sweet wort is separated.", "“The husk-supported bed retains solids while sweet wort passes through. You have now traced grain from raw material to separated wort; take that process framework back to the Training Coordinator,” says the Lauter Operator."),
        T("training_coordinator", "Return to the Training Coordinator.", "“Good. You have the process framework; now investigate each biochemical problem in sequence.”")), 30,
        lead="The Training Coordinator has a first assignment tracing grain from malting through mash separation."),

    "malt_house": Quest("Wake the Sleeping Grain", "head_maltster",
        "“This lot is germinating unevenly. Trace the signal from hydrated embryo to starch-degrading enzymes,” says the Head Maltster.", (
        T("barley_inspector", "Ask the Barley Inspector about the grain.", "Uneven kernels hydrate unevenly; two-row barley is valued in part for kernel uniformity."),
        T("gibberellic_acid", "Find the gibberellic-acid messenger.", "Gibberellic acid carries the embryo's signal toward the aleurone."),
        T("aleurone_cell", "Ask the Aleurone Cell how it responds.", "The aleurone synthesizes and secretes hydrolytic enzymes including alpha-amylase and proteases."),
        T("starch_granule", "Check modification in the endosperm.", "Cell walls and storage material are opening to enzyme access."),
        E("beta_amylase", "head_maltster", "Escort Beta-Amylase's assay sample to the Head Maltster.", "The assay is sound. Inconsistent steeping, not absent enzyme, caused the patchy modification.")), 35, ("orientation",),
        lead="A barley lot is germinating unevenly, and the Head Maltster needs a biochemical diagnosis."),

    "water_profile": Quest("A Tale of Two Ions", "water_chemist",
        "“The pilot pale ale tastes sharp and thin. Build a useful profile from chemistry, not merely a city name,” says the Water Chemist.", (
        T("ph_meter", "Check mash pH.", "The pH is outside the most useful mash range."),
        T("bicarbonate", "Consult Bicarbonate.", "Alkalinity resists a fall in pH; it is not identical to hardness."),
        T("calcium_ion", "Ask Calcium about mash effects.", "Calcium can help reduce mash pH and stabilize alpha-amylase."),
        T("sulfate_ion", "Ask Sulfate about flavor.", "Sulfate emphasizes bitterness and dryness; excess can seem harsh."),
        T("chloride_ion", "Ask Chloride about flavor.", "Chloride tends to emphasize fullness and apparent sweetness."),
        T("water_chemist", "Return with a balanced recommendation.", "The chemist corrects alkalinity first, then adjusts sulfate and chloride deliberately. Before you diagnose the production mash, the Carbohydrate Curator wants you in the laboratory inside the Mash Tun.")), 35, ("malt_house",),
        lead="A pilot pale ale tastes sharp and thin, and the Water Chemist needs help correcting its chemistry."),

    "starch_structure": Quest("Rebuild the Carbohydrate Map", "carbohydrate_curator",
        "The Carbohydrate Curator gestures toward a scrambled set of molecular labels. “Before you diagnose a mash, prove that you can distinguish its substrate, products, and structural look-alikes. Rebuild this map from monomer to hydrated starch.”", (
        T("glucose", "Identify the monomer used to build barley starch.", "“I am glucose, a single sugar unit. Thousands or millions of copies of me can be linked into polysaccharides with very different properties,” says Glucose."),
        T("maltose", "Identify the brewing disaccharide released from starch.", "“I am maltose: two glucose units joined alpha-1,4. Beta-amylase releases me repeatedly from nonreducing starch-chain ends,” says Maltose."),
        T("sucrose", "Determine which monosaccharides make sucrose.", "“I am a disaccharide of glucose and fructose,” says Sucrose. “The number of sugar units alone does not identify a molecule.”"),
        T("lactose", "Compare lactose with sucrose.", "“I contain galactose and glucose, not fructose and glucose,” says Lactose. “I am useful here as a comparison, not as the principal sugar extracted from malt.”"),
        T("amylose", "Trace the structure and packing of amylose.", "“I am mostly an unbranched alpha-1,4 glucose chain. I can form a left-handed helix and pack into hydrogen-bonded regions that exclude water,” says Amylose."),
        T("amylopectin", "Trace amylopectin and locate its branch points.", "“I supply roughly seventy to eighty percent of ordinary starch. Alpha-1,6 branch points interrupt my alpha-1,4 chains every few dozen glucose units,” says Amylopectin."),
        T("glycogen", "Compare glycogen with amylopectin.", "“Animals store glucose in my chains. I resemble amylopectin but branch more frequently, supporting rapid glucose mobilization,” says Glycogen."),
        T("cellulose", "Explain why cellulose behaves unlike starch.", "“My glucose units use beta-1,4 linkages, producing straight structural chains rather than the alpha-linked substrate recognized by starch-degrading amylases,” says Cellulose."),
        T("crystallinity_analyst", "Ask why packed starch can resist amylases.", "“Aligned, hydrogen-bonded chains exclude water and form ordered regions. Enzymes cannot efficiently attack bonds they cannot physically reach,” says the Crystallinity Analyst."),
        T("gelatinization_specialist", "Determine what gelatinization changes.", "“Heat and water disrupt ordered packing and hydrate the glucan chains. That improves enzyme access, but gelatinization itself does not hydrolyze starch into sugar,” says the Gelatinization Specialist."),
        T("grain_stress_agronomist", "Ask how growing conditions can change gelatinization.", "“Heat and drought during grain filling can raise starch gelatinization temperature. If access requires temperatures that damage the malt's amylases, self-conversion becomes difficult,” says the Grain-Stress Agronomist."),
        T("carbohydrate_curator", "Return to the Carbohydrate Curator and rebuild the map.", "“Correct: composition identifies the building blocks, linkage and branching determine architecture, and heat plus water determine accessibility. Now you are ready to diagnose the stalled mash,” says the Carbohydrate Curator.")), 45, ("water_profile",),
        lead="A scrambled molecular map must be rebuilt before the production mash can be diagnosed."),

    "stalled_mash": Quest("The Stalled Mash", "head_brewer",
        "An iodine-dark sample worries the Head Brewer. “Decide whether access, temperature, pH, or enzyme activity is responsible.”", (
        T("miller", "Find the Miller and ask whether milling exposed the endosperm.", "The crush exposed starch while retaining husk pieces for the filter bed."),
        T("gelatinized_starch", "Check starch accessibility.", "The swollen granules have lost ordered structure and expose glucan chains."),
        T("beta_amylase", "Consult Beta-Amylase.", "Beta-amylase releases maltose from nonreducing ends but is relatively heat-sensitive."),
        T("alpha_amylase", "Consult Alpha-Amylase.", "Alpha-amylase cleaves internal alpha-1,4 bonds, lowers viscosity, and creates varied dextrins."),
        T("ph_meter", "Verify mash pH.", "The pH is corrected into the useful enzyme range."),
        T("head_brewer", "Return with the diagnosis.", "A hot dough-in damaged beta-amylase activity; the wort will be less fermentable and fuller-bodied than planned.")), 40, ("starch_structure",),
        lead="An iodine-dark mash is not converting as expected, and the Head Brewer needs the cause identified."),

    "clear_wort": Quest("The Stuck Runoff", "lauter_operator",
        "“The grant slowed to a trickle. Find out whether the bed needs patience, recirculation, or gentler sparging,” says the Lauter Operator.", (
        T("husk_keeper", "Examine the husk-supported bed.", "Intact husks make channels; excess flour and compaction obstruct them."),
        T("vorlauf_guide", "Ask about recirculation.", "Vorlauf returns cloudy first wort until the grain bed becomes an effective filter."),
        T("sparge_technician", "Check sparge flow.", "Overly aggressive flow disturbed and compacted the bed."),
        E("sparge_technician", "lauter_operator", "Escort the Sparge Technician to the operator.", "They slow and redistribute flow. Clear sweet wort begins moving.")), 30, ("stalled_mash",),
        lead="The lauter runoff has slowed to a trickle, and the Lauter Operator needs the obstruction diagnosed."),

    "hop_timing": Quest("The Vanishing Hop Aroma", "kettle_brewer",
        "“The recipe has plenty of hops but almost no aroma. Follow the molecules through heat and time,” says the Kettle Brewer.", (
        T("humulone", "Ask Humulone what boiling does.", "Heat isomerizes alpha acids into more soluble bitter iso-alpha acids."),
        T("isomerization_chemist", "Ask why early additions favor bitterness.", "Long hot contact promotes isomerization and bitterness extraction."),
        T("myrcene", "Ask Myrcene why aroma disappears.", "Many hop-oil components are volatile and leave during vigorous boiling."),
        T("dry_hopper", "Ask how to retain aroma.", "Late and dry-hop additions retain more volatile aroma than long kettle boils."),
        T("kettle_brewer", "Return with a revised schedule.", "The brewer separates early bittering, later flavor, and late or cold-side aroma additions.")), 35, ("clear_wort",),
        lead="A heavily hopped batch has almost no hop aroma, and the Kettle Brewer needs to know where it went."),

    "fermentation": Quest("Save the Stalled Fermentation", "cellar_manager",
        "“Gravity stopped falling. Diagnose the wort and cells before anyone dumps oxygen into finished beer,” says the Cellar Manager.", (
        T("qa_technician", "Verify gravity and sampling.", "A calibrated second reading confirms genuine residual extract."),
        T("yeast_culturist", "Check viability and pitch history.", "The cells were underpitched and depleted in membrane reserves."),
        T("maltose_permease", "Inspect maltose uptake.", "Maltose uses proton-linked transport; glucose repression delays the needed machinery."),
        T("maltase", "Ask how intracellular maltose is used.", "Maltase hydrolyzes maltose into two glucose molecules."),
        T("lipid_specialist", "Ask why early wort oxygen matters.", "Early oxygen supports sterol and unsaturated-fatty-acid synthesis; late oxygen encourages staling."),
        E("yeast_culturist", "cellar_manager", "Escort the Yeast Culturist to the Cellar Manager.", "They prepare an active culture and controlled recovery plan. Fermentation resumes without aerating the beer.")), 45, ("hop_timing",),
        lead="A fermentation has stopped with residual extract remaining, and the Cellar Manager needs a recovery plan."),

    "diacetyl": Quest("Butter in the Cellar", "sensory_analyst",
        "The Sensory Analyst detects butter and butterscotch. “Trace the compound to its precursor and choose a biochemical remedy.”", (
        T("diacetyl_molecule", "Question Diacetyl.", "Diacetyl has a low flavor threshold and a buttery sensory character."),
        T("alpha_acetolactate", "Find alpha-acetolactate.", "Yeast-derived alpha-acetolactate can leave the cell and form diacetyl."),
        T("maturation_operator", "Ask about a diacetyl rest.", "Warm active yeast can take up diacetyl and reduce it to less flavor-active products."),
        E("maturation_operator", "sensory_analyst", "Escort the operator to the Sensory Analyst.", "They schedule a warm rest and repeat sensory checks before cooling.")), 32, ("fermentation",),
        lead="A cellar sample tastes strongly of butter and butterscotch, and the Sensory Analyst needs its biochemical source traced."),

    "sulfur": Quest("The Sulfur Alarm", "sulfur_engineer",
        "“One sample smells like eggs; another like cooked vegetables. Separate their origins,” says the Sulfur Engineer.", (
        T("hydrogen_sulfide", "Identify the rotten-egg compound.", "Hydrogen sulfide can arise from yeast sulfur metabolism."),
        T("dms_molecule", "Identify the cooked-vegetable compound.", "Dimethyl sulfide derives in part from malt SMM chemistry."),
        T("boil_engineer", "Ask how boiling affects DMS.", "An open vigorous boil helps volatilize DMS; a weak or covered boil retains it."),
        T("sulfur_engineer", "Return with the diagnosis.", "The engineer treats yeast-related H2S and boil-related DMS as distinct problems.")), 30, ("diacetyl",),
        lead="Two samples have different sulfur faults, and the Sulfur Engineer needs their identities and origins separated."),

    "lightstruck": Quest("The Sunlit Six-Pack", "packaging_lead",
        "“A display batch became skunky. Reconstruct the photochemistry and recommend a package,” says the Packaging Lead.", (
        T("light_tester", "Test the beer in the lightstrike booth.", "Blue-visible and near-UV light reproduce the fault in susceptible hopped beer."),
        T("riboflavin", "Ask Riboflavin about its role.", "Excited riboflavin participates in sulfur-radical photochemistry."),
        T("mbt_molecule", "Identify the skunky product.", "3-methyl-2-butene-1-thiol has an extremely low sensory threshold."),
        T("can_specialist", "Ask about package protection.", "Opaque cans block the relevant light and can provide an excellent oxygen barrier."),
        T("packaging_lead", "Return with a recommendation.", "The lead moves the release to cans and tightens light-exposure controls.")), 35, ("styles",),
        lead="A display batch became skunky, and the Packaging Lead needs the photochemistry reconstructed."),

    "foam": Quest("The Headless Pint", "taproom_manager",
        "“This beer pours lively, then collapses. Investigate proteins, gas, and glass,” says the Taproom Manager.", (
        T("ltp1", "Ask LTP1 about foam.", "Heat-modified barley LTP1 can support foam, while lipids are often foam-negative."),
        T("protein_z", "Ask Protein Z about foam.", "Protein Z is another barley protein associated with foam stability."),
        T("carbonation_operator", "Check carbonation and serving temperature.", "Gas level, nucleation, pressure, and temperature influence the pour."),
        T("glass_steward", "Inspect the glassware.", "A thin grease film is destroying bubbles at the surface."),
        T("taproom_manager", "Return to the Taproom Manager.", "Clean glassware restores the head; protein and carbonation checks are logged for future batches.")), 35, ("lightstruck",),
        lead="A lively pint rapidly loses its foam, and the Taproom Manager needs to know why."),

    "styles": Quest("Two Yeasts, Two Cellars", "style_judge",
        "“Use physiology and process—not stereotypes—to identify these ale and lager paths,” says the Style Judge.", (
        T("ale_yeast", "Interview the warm-fermenting yeast.", "S. cerevisiae commonly ferments ales warmer and may make prominent esters."),
        T("lager_yeast", "Interview the cool-fermenting yeast.", "S. pastorianus is a hybrid lager yeast adapted to cool fermentation."),
        T("ester_chemist", "Ask what controls esters.", "Strain, temperature, oxygenation, pitch rate, and wort composition all matter."),
        T("cold_keeper", "Ask what lagering accomplishes.", "Cold maturation supports clarification and flavor maturation."),
        T("style_judge", "Return with the identification.", "The judge accepts the process-based answer without pretending every ale or lager is chemically identical.")), 35, ("sulfur",),
        lead="Two unidentified cellar paths must be distinguished using yeast physiology and process evidence."),

    "sanitation": Quest("The Uninvited Fermenter", "microbiologist",
        "“A package is overcarbonated and unexpectedly sour. Trace possible contaminants and their route,” says the Microbiologist.", (
        T("lactic_bacterium", "Assess the lactic bacterium.", "Lactic acid bacteria can acidify beer; hop iso-alpha acids inhibit many Gram-positive strains."),
        T("wild_yeast", "Assess the wild yeast.", "The isolate can consume carbohydrate left by the production strain and continue making package gas."),
        T("sanitation_lead", "Audit cleaning records.", "A transfer fitting retained soil before sanitizer was applied."),
        E("sanitation_lead", "microbiologist", "Escort the Sanitation Lead to the lab.", "They quarantine the lot and distinguish removing soil by cleaning from reducing microbes by sanitizing.")), 38, ("foam",),
        lead="A package is unexpectedly sour and overcarbonated, suggesting that an uninvited fermenter got inside."),

    "mystery_batch": Quest("The Batch That Does Not Add Up", "qa_chemist",
        "“The production sheet and finished beer disagree. Recheck the batch across departments and build an evidence-based diagnosis,” says the QA Chemist.", (
        T("ph_meter", "Verify the recorded mash pH.", "The archived pH value is valid and does not explain the discrepancy."),
        T("qa_technician", "Verify original and final gravity readings.", "A transcription error swapped two digits in the original-gravity entry."),
        T("ibu_chemist", "Check the bitterness assay.", "The absorbance-based IBU estimate is internally consistent, though it is not identical to perceived bitterness."),
        T("carbonation_operator", "Check package temperature and CO2 pressure.", "The beer warmed during measurement, explaining the apparently low dissolved CO2."),
        T("sensory_analyst", "Compare the corrected records with a blind sample.", "The sensory profile now agrees with the corrected analytical record."),
        T("qa_chemist", "Return to the QA Chemist with the complete diagnosis.", "“Good. No single measurement tells the whole story; traceable records and independent checks prevented a needless process change.”")), 40, ("sanitation",),
        lead="The production record and finished beer disagree, and the QA Chemist needs an independent investigation."),
}

GIVER_QUESTS = {q.giver: key for key, q in QUESTS.items()}
