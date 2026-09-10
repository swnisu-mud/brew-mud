from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Quiz:
    prompt: str
    options: tuple[str, ...]
    correct: int
    feedback: tuple[str, ...]
    explanation: str
    arrival_exclusions: tuple[str, ...] = ()


def Q(prompt, options, correct, explanation, exclusions=()):
    feedback = tuple("Review the underlying process relationship, not just the vocabulary." if i != correct else "" for i in range(4))
    return Quiz(prompt, options, correct, feedback, explanation, exclusions)


QUIZZES = {
 "germination_floor": Q("Which signal stimulates the barley aleurone to produce hydrolytic enzymes during germination?", ("Insulin", "Gibberellic acid", "Lactic acid", "Humulone"), 1, "Gibberellic acid from the embryo signals the aleurone to synthesize enzymes including alpha-amylase and proteases.", ("aleurone",)),
 "kiln": Q("What is a central tradeoff when malt is kilned more intensely?", ("More flavor/color but less surviving enzyme activity", "More oxygen but no drying", "More starch synthesis", "Complete removal of protein"), 0, "Hotter or longer kilning develops color and flavor while destroying a greater fraction of heat-sensitive enzyme activity."),
 "ion_gallery": Q("How does alkalinity differ from hardness?", ("They are always identical", "Alkalinity resists pH decrease; hardness mainly reflects polyvalent ions", "Hardness measures ethanol", "Alkalinity measures hop oil"), 1, "Alkalinity is acid-neutralizing capacity, often involving bicarbonate; hardness chiefly reflects ions such as calcium and magnesium.", ("ph_bench",)),
 "mash_tun": Q("A brewer wants a more fermentable wort. Which mash emphasis generally favors that goal?", ("A lower-temperature beta-amylase-favoring rest", "Maximum caramelization", "A covered wort boil", "Late oxygen exposure"), 0, "A lower saccharification rest preserves more beta-amylase activity and tends to yield more maltose and greater fermentability.", ("beta_rest",)),
 "conversion_bench": Q("Why does starch gelatinization matter during mashing?", ("It makes starch crystalline", "It improves enzyme access to glucan chains", "It makes nitrogen gas", "It is hop isomerization"), 1, "Gelatinization disrupts ordered granules so amylases can reach amylose and amylopectin more effectively.", ("beta_rest","alpha_rest")),
 "lauter_tun": Q("What normally serves as the principal filter medium during lautering?", ("Yeast sediment", "The malt husk grain bed", "Hop oil", "Bottle glass"), 1, "The spent-grain bed, supported by relatively intact husks, filters wort above the false bottom.", ("grain_bed",)),
 "kettle": Q("Which event is promoted by wort boiling?", ("Alpha-acid isomerization", "Maltose transport into yeast", "Barley germination", "Cold settling"), 0, "Kettle heat isomerizes hop alpha acids into more soluble bitter iso-alpha acids.", ("alpha_acid_bench",)),
 "hot_break": Q("What contributes to the hot break?", ("Heat-denatured and aggregated wort proteins", "New barley embryos", "Only dissolved CO2", "Intact yeast chromosomes"), 0, "Boiling denatures proteins and promotes aggregates with polyphenols and other material that form hot break."),
 "oxygenation_station": Q("Why is cooled pitching wort oxygenated?", ("To let yeast synthesize sterols and unsaturated fatty acids", "To isomerize hops", "To carbonate finished beer", "To create starch"), 0, "Early wort oxygen supports membrane-lipid synthesis and growth; oxygen introduced after fermentation promotes staling.", ("lipid_workshop",)),
 "maltose_gate": Q("How does brewing yeast typically bring maltose into the cell?", ("Simple diffusion through lipids", "Proton-linked active transport", "A DNA polymerase", "Endocytosis of starch"), 1, "Maltose permease uses the proton gradient; intracellular maltase then cleaves maltose into two glucose molecules.", ("maltase_bench",)),
 "nad_recycling": Q("Why must alcoholic fermentation regenerate NAD+?", ("So glycolysis can continue oxidizing substrate", "So hops can grow", "So starch can crystallize", "So bottles block light"), 0, "Reduction of acetaldehyde to ethanol reoxidizes NADH to NAD+, sustaining glycolytic flux."),
 "diacetyl_rest": Q("What is the purpose of a diacetyl rest?", ("Encourage active yeast to remove diacetyl", "Isomerize alpha acids", "Germinate barley", "Increase light exposure"), 0, "A warm period with active yeast promotes uptake and reduction of buttery diacetyl to less flavor-active compounds."),
 "sulfur_vent": Q("Which pairing is most accurate?", ("H2S—rotten egg; DMS—cooked corn/vegetable", "H2S—banana; DMS—vanilla", "H2S—bitterness; DMS—foam", "Both are always odorless"), 0, "Hydrogen sulfide is classically rotten-egg-like; dimethyl sulfide often evokes cooked corn or vegetables."),
 "alpha_acid_bench": Q("What happens to humulone during a productive kettle boil?", ("It becomes DNA", "It isomerizes to a more soluble bitter form", "It becomes maltose", "It makes oxygen"), 1, "Heat rearranges hop alpha acids into iso-alpha acids with greater solubility and characteristic bitterness.", ("kettle",)),
 "oil_lab": Q("Why do late hop additions usually retain more aroma than early additions?", ("Hop oils are volatile", "Alpha acids are proteins", "Yeast makes cellulose", "Late hops contain no water"), 0, "Many hop essential-oil components are volatile and are lost during prolonged vigorous boiling.", ("dry_hop_gallery",)),
 "lightstrike_booth": Q("Which package offers the strongest protection against lightstruck flavor?", ("Clear glass", "Green glass", "An opaque can", "An open pitcher"), 2, "An opaque can blocks the wavelengths that drive riboflavin/hop photochemistry and skunky MBT formation.", ("canning_line",)),
 "carbonation_station": Q("At the same applied CO2 pressure, which beer retains more dissolved CO2?", ("The colder beer", "The warmer beer", "They must be identical", "Only nitrogenated beer"), 0, "Carbon dioxide solubility increases as beer temperature decreases at a fixed pressure."),
 "foam_lab": Q("Which is most likely to damage beer foam?", ("A clean nucleation point", "A grease or detergent residue", "Foam-active barley proteins", "Appropriate carbonation"), 1, "Lipids, grease, and detergent residues destabilize bubble films and can rapidly collapse a beer's head."),
 "qa_chemistry": Q("Why should an unexpected brewery measurement be repeated with a calibrated method?", ("To distinguish a real process change from sampling or instrument error", "To make hops less volatile", "To germinate finished beer", "To eliminate all microbes"), 0, "Independent, calibrated measurements and traceable samples prevent bad data from triggering inappropriate process changes."),
}
