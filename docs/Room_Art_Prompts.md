# Illustrated room art prompts

The first 20 `ROOM_DATA` locations have static backgrounds in `brewmud/static/art/`. The 17 new backgrounds in this iteration were made with the built-in image-generation tool. Each used this common prompt prefix, followed by its room-specific scene:

> Use case: stylized-concept. Asset type: static background for a point-and-click educational brewery adventure game. Style: detailed warm retro pixel-art inspired by late-1980s adventure games, polished brewery environment with amber and teal highlights. Composition: wide 16:9 eye-level scene, center foreground clear for clickable overlays and visible doorways for exits. No people, no text, no labels, no UI, no logos, no watermark. Scene:

| Room | Scene appended to the common prompt |
| --- | --- |
| Steep House | Steep House, a tall maltings hall with large open water steep tanks containing swelling barley, timber walkways, overhead hoses and clear doorway |
| Steep Air Rest | Steep Air Rest, drained steeping vessel full of moist barley with an aeration manifold and visible air pipes, floor grates and side doorway |
| Germination Floor | Germination Floor, broad low room of moist barley spread in shallow even layers, hand turning rake, daylight windows and walkways |
| Aleurone Workshop | Aleurone Workshop, imaginative educational micro-scale interior of a barley kernel: thin living aleurone layer, secretory vesicle-like glowing organelles and enzyme droplets facing starch endosperm; biologically plausible rather than fantasy magic |
| Starchy Endosperm | Starchy Endosperm, educational close-up landscape inside a barley kernel with densely packed starch granules in a protein matrix and partly opened cell walls, warm biological microscopy-inspired pixel art |
| Malt Kiln | Malt Kiln, tiered perforated grain-drying floor above a furnace, rising warm airflow indicated visually by heat shimmer, visible temperature gauge without legible text and doorways |
| Brewing Water Laboratory | Brewing Water Laboratory, brewery analytical bench with water sample bottles, conductivity and mineral testing apparatus, copper pipes and windows |
| pH Bench | pH Bench, close brewery laboratory station with a pH electrode dipped in a sample beaker, buffer bottles and simple instruments, no readable numerals |
| Ion Gallery | Ion Gallery, brewery water chemistry room with jars of mineral salts, glass water vessels, chalky limestone sample and schematic wall tiles with abstract shapes but no writing |
| Historic Water Profiles | Historic Water Profiles gallery inside a brewery, two contrasting water-source exhibits evoking Burton mineral-rich water and Pilsen soft water, maps without readable labels, barrels and stone samples |
| Water Treatment Bay | Water Treatment Bay, brewery pipes, carbon filter cylinders, clean water tanks and valves arranged around a clear service aisle |
| Malt Mill | Malt Mill, old industrial brewery grain mill with visible twin crushing rollers, barley feed hopper, intact husks and cracked endosperm in collection tray |
| Mash Tun | Mash Tun, large copper mash vessel with stirring rake, warm wet grain-and-water mash visible under an open lid, steam and overhead process pipes |
| Carbohydrate and Starch Laboratory | Carbohydrate and Starch Laboratory, brewery teaching laboratory with physical molecular bead models showing one sugar unit, paired units, and branched versus straight long chains; no writing |
| Glucose Bench | Glucose Bench, intimate teaching laboratory with a large scientifically plausible glucose ring molecular model as central object, barley starch chain model nearby, no text |
| Disaccharide Gallery | Disaccharide Gallery, brewery teaching room with three distinct paired sugar molecular models on separate plinths, maltose, sucrose, lactose represented by different colored bead patterns, no labels |

The Two-Row Barley Laboratory used a separate prompt:

> Use case: stylized-concept. Asset type: static background for a point-and-click educational brewery adventure game. Primary request: Two-Row Barley Laboratory: a rustic maltings laboratory with a large scientifically plausible cutaway barley kernel specimen on a workbench, jars of two-row barley, hand lens and simple measuring tools. Style: detailed warm retro pixel-art inspired by late-1980s adventure games, matching a polished brewery environment; natural amber light, brick and timber. Composition: wide 16:9 eye-level room, clear center foreground for clickable NPC and object overlays; doorways visible for exits. Constraints: no people, no text, no labels, no UI, no logos, no watermark.

The existing Brewery Gate, Grain Receiving, and Malt Curing Floor illustrations were generated for the earlier three-room pilot. All 20 backgrounds were downsampled to 960 × 540 WebP files for deployment. The interface adds live object and exit targets over each background; their labels are intentionally not embedded in the art.

## Integrated staff edits

Eleven existing backgrounds were subsequently edited with the built-in image-generation tool to place their human NPCs naturally in the scene. Each edit used the room's existing image as **Image 1: edit target**, this common prompt frame, and the subject in the table:

> Use case: compositing. Asset type: BrewMUD illustrated room background. Image 1 is the edit target. Add exactly one integrated NPC: [subject]. Match the existing warm retro pixel-art style, perspective, scale, lighting, and cast shadow. Keep the room architecture, apparatus, pathways, framing, colors, and all other objects unchanged. The NPC should be clearly visible at human scale but not obscure the educational equipment. No floating markers, no labels, no UI, no other people, no logos, no watermark.

| Room | NPC subject |
| --- | --- |
| Grain Receiving | Barley Inspector, a brewery worker in practical apron, kneeling beside the sampling table and splitting a few barley kernels, positioned on the open cobblestones without covering the cart or doorway |
| Steep House | Steep-House Maltster, a brewery worker in practical apron and boots, standing on the central walkway between the steep tanks and checking a small barley sample |
| Malt Kiln | Kiln Operator, an experienced brewery worker in practical heat-safe clothing, standing beside the temperature gauge at the right side and monitoring the drying grain |
| Malt Curing Floor | Head Maltster, an experienced brewery worker in practical maltings clothes, standing beside the front grain-curing tray and examining a handful of dried malt |
| Brewing Water Laboratory | Water Chemist, a brewery scientist in a practical lab coat, standing behind the central workbench and inspecting a clear water sample |
| Historic Water Profiles | Burton Water Guide, a brewery guide in practical period-neutral clothing, standing between the two water-source exhibits and gesturing to their contrasting geology |
| Water Treatment Bay | Treatment Chemist, a brewery scientist in practical work clothes and safety glasses, standing next to the left-side carbon filter cylinders and checking a valve |
| Malt Mill | Miller, a brewery worker in practical apron and safety glasses, standing to one side of the roller mill and checking the roller-gap adjustment |
| Mash Tun | Head Brewer, a brewery worker in practical brewing clothes, standing at the right side of the copper mash tun holding a long stirring rake |
| Carbohydrate and Starch Laboratory | Carbohydrate Curator, a friendly brewery teaching scientist in a practical lab coat, standing behind the central bench of molecular models and gesturing toward the different chain structures |

The Brewery Gate had the same compositing goal with this more specific prompt:

> Use case: compositing. Asset type: BrewMUD illustrated room background. Image 1 is the edit target. Add one Training Coordinator naturally standing on the cobblestones just inside the brewery gate, dressed as a practical brewery staff member and holding a clipboard with a small process diagram (no legible writing). Match the existing warm retro pixel-art style, perspective, scale, lighting, and shadow. Keep the buildings, gate, pathways, framing, colors, and all other objects unchanged. No floating markers, no labels, no UI, no other people, no logos, no watermark.

The original room backgrounds remain as source assets. The web interface uses the `-with-npc.webp` variants in staff rooms and places a `Talk to …` button below the image. Nonhuman NPCs, such as glucose and the Two-Row Kernel, are represented by the existing scientific models or apparatus in their room art.
