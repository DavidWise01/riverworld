#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Upgrade roster.json: add six-W fields to every member, append note sentence."""
import json
import io

PATH = r"C:\repos\riverworld\roster.json"

# name -> {who, what, where, why, when, how}
SIX = {
    "Sir Richard Francis Burton": {
        "who": "The Victorian explorer, swordsman, and master linguist, first of the dead to wake before the resurrection was finished.",
        "what": "Lead Seeker — the questing spearhead driving up-River toward the tower and the truth.",
        "where": "Everywhere along the ten-million-mile River, ever northward toward the headwaters.",
        "why": "He cannot abide an unsolved mystery, and the secret of who built this world and why is the greatest unsolved mystery of all.",
        "when": "From the very first morning of the resurrection through the final reckoning at the tower.",
        "how": "By questing, fighting, and dying a thousand deaths up the River, rising each time and climbing on.",
    },
    "Alice Hargreaves": {
        "who": "The real-life Alice who inspired Wonderland, resurrected at twenty-five rather than as a child.",
        "what": "First Companion — the partner who joins Burton on the bank at the dawn of the new world.",
        "where": "At Burton's side on the riverbank and on the long journey north.",
        "why": "To make her own way in a second life, on her own terms and no one else's.",
        "when": "From the opening morning of the resurrection onward.",
        "how": "With composure, dignity, and a will that refuses to be mistaken for the child of the storybooks.",
    },
    "Peter Jairus Frigate": {
        "who": "A twentieth-century writer who serves as the author's own shadow walking the River.",
        "what": "Chronicler — the keeper of the record of the quest.",
        "where": "Among Burton's band, notebook of the mind always open.",
        "why": "To witness and preserve the story of the greatest journey ever undertaken.",
        "when": "Throughout the up-River quest from early in the saga.",
        "how": "By observing, remembering, and setting down the chronicle of all that passes.",
    },
    "Nur ed-Din el-Musafir": {
        "who": "A Moorish Sufi master, the still and centering presence of the band.",
        "what": "Teacher — the spiritual anchor whose discipline even the Ethicals came to fear.",
        "where": "At the calm center of the questing company.",
        "why": "To guide companions toward mastery of self, the one path the world-builders could not foresee.",
        "when": "Through the long middle and late stages of the quest.",
        "how": "By the quiet discipline of Sufi practice, teaching by stillness rather than force.",
    },
    "Samuel Clemens (Mark Twain)": {
        "who": "Samuel Clemens, the American humorist known as Mark Twain, haunted by a vision of a great riverboat.",
        "what": "Builder-in-chief — architect of the steamboat Not For Hire bound for the headwaters.",
        "where": "At the fallen meteorite and the boatyards along the bank.",
        "why": "Driven by the dream of the riverboat and the longing to reach the tower at the source.",
        "when": "Through the boat-building heart of the saga.",
        "how": "By bargaining for the iron of a fallen meteorite and forging it into a vessel to steam ten million miles.",
    },
    "Lothar von Richthofen": {
        "who": "The Red Baron's brother, an airman and aristocrat of the Great War.",
        "what": "Aviator — the wings of the builders' dream and Clemens's loyal friend.",
        "where": "Aloft above the River and aboard the great riverboat.",
        "why": "For loyalty to Clemens and the thrill of flight over a world without end.",
        "when": "During the building and voyage of the riverboat.",
        "how": "By flying the machines the builders raise from River-metal and ingenuity.",
    },
    "Milton Firebrass": {
        "who": "An engineer of the impossible, master of machines beyond his era.",
        "what": "Chief engineer — maker of aircraft, airship, and the long iron machine bound for the tower.",
        "where": "In the workshops and hangars of the builders' enterprise.",
        "why": "To bend River-metal and salvaged science toward reaching the headwaters.",
        "when": "Through the construction era of the saga.",
        "how": "By engineering flying craft and vessels from scarce materials and sheer skill.",
    },
    "King John": {
        "who": "John Plantagenet, the treacherous medieval king of England, resurrected wholly unchanged.",
        "what": "Usurper — the tyrant who steals Clemens's first riverboat and races him north.",
        "where": "Aboard the stolen vessel, fleeing and scheming up the River.",
        "why": "For power and dominion, the same appetites that ruined his first life.",
        "when": "During the riverboat-building and pursuit phase of the saga.",
        "how": "By treachery, betrayal, and the seizure of what others built.",
    },
    "The River Kingdoms": {
        "who": "The slaver-states and petty tyrannies that rise along the banks.",
        "what": "Oppressor-states — living proof that a second life grants no second soul by itself.",
        "where": "Scattered across the endless banks of the River.",
        "why": "To seize grailstones, labor, and power in a world meant to offer everyone a fresh start.",
        "when": "Throughout the saga, wherever the questers pass.",
        "how": "By conquest, enslavement, and the old cruelties carried over from Earth.",
    },
    "La Viro (Jacques Gillot)": {
        "who": "Jacques Gillot, founder of the Church of the Second Chance.",
        "what": "Prophet — preacher that the resurrection is an offer to become better.",
        "where": "In the temples and missions of the Church along the River.",
        "why": "Because the second life is a chance for redemption that violence forfeits.",
        "when": "Across the saga as the Church spreads along the banks.",
        "how": "By preaching nonviolence and the discipline of renouncing harm.",
    },
    "Hermann Göring": {
        "who": "The Nazi Reichsmarschall, resurrected as the tyrant and addict he was.",
        "what": "Penitent — the saga's hardest case, clawing through the Church toward something like redemption.",
        "where": "From the tyrannies of the bank to the missions of the Second Chance.",
        "why": "To escape his own ruin and reach the redemption the Church insists even he may earn.",
        "when": "Across the long arc from his early River-tyranny to his slow turning.",
        "how": "By the agonizing discipline of the Church of the Second Chance, falling and rising again.",
    },
    "Kazz": {
        "who": "Kazzintuitruaabemss, a Paleolithic man and nearly the last of his ancient kind.",
        "what": "First friend — Burton's fierce, loyal companion from the very first morning.",
        "where": "At Burton's side on the bank and through the quest.",
        "why": "Out of fierce loyalty to the man who first stood with him in the new world.",
        "when": "From the opening morning of the resurrection onward.",
        "how": "By raw strength, courage, and the unbreakable bond of an old loyalty.",
    },
    "Monat Grrautut": {
        "who": "The Tau Cetan, the alien who once sterilized Earth and now wanders the River in sorrow.",
        "what": "Wise counselor — Burton's wisest friend and conscience.",
        "where": "Among Burton's band along the River.",
        "why": "Out of sorrow and a longing to atone for the destruction his people once wrought.",
        "when": "From early in the quest alongside Burton.",
        "how": "By counsel, wisdom, and the long perspective of a being from beyond Earth.",
    },
    "Cyrano de Bergerac": {
        "who": "The historical duelist and poet, finer with a blade and a verse than his legend allows.",
        "what": "Champion — the finest swordsman on the River and a true poet.",
        "where": "At the band's side wherever steel or wit is needed.",
        "why": "For honor, loyalty, and the joy of living fully as exactly who he is.",
        "when": "Through the companionship of the quest.",
        "how": "By peerless swordsmanship paired with genuine poetry, proud and loyal.",
    },
    "Tom Mix": {
        "who": "The American cowboy film star, resurrected on the River.",
        "what": "Frontiersman — the rider who treats the endless bank like a back lot.",
        "where": "Along the banks of the River.",
        "why": "To live the second life with the same easy grit and showmanship as the first.",
        "when": "Through his stretch of the companions' journey.",
        "how": "By rope, grin, and grit, carrying his on-screen daring into a real world.",
    },
    "Gilgamesh": {
        "who": "The ancient king of Uruk, oldest of the named, made twenty-five again.",
        "what": "Ancient king — the eldest legend beginning a second time among the resurrected.",
        "where": "Naked on the grass of the bank, like every other risen soul.",
        "why": "To begin anew, the immortality he once chased now granted to all the dead at once.",
        "when": "From the resurrection morning that levels even the oldest of kings.",
        "how": "By starting over from nothing, stripped of throne and legend alike.",
    },
    "The Council of Twelve": {
        "who": "The posthuman world-builders who raised every human who ever lived.",
        "what": "Architects — the gods of Riverworld who watch the experiment from the tower.",
        "where": "In the tower at the headwaters at the source of the River.",
        "why": "To shepherd the resurrected toward an ethical end the saga slowly unveils.",
        "when": "Across the whole saga, presiding from before the first morning.",
        "how": "By raising the dead with vast technology and observing from the headwaters.",
    },
    "The Agents": {
        "who": "Ethical operatives who walk the River disguised as ordinary resurrected souls.",
        "what": "Watchers — the hidden guardians of the secret of why any of this was done.",
        "where": "Among the resurrected anywhere along the River, indistinguishable from them.",
        "why": "To guard the world-builders' purpose and steer the experiment from within.",
        "when": "Throughout the saga, unseen until the quest exposes them.",
        "how": "By disguise, infiltration, and quiet intervention among the resurrected.",
    },
    "X · the Mysterious Stranger": {
        "who": "Loga, one of the Twelve who broke faith with his own kind — the renegade god of the second chance.",
        "what": "Hidden hand — the secret architect on whom the whole saga turns.",
        "where": "Behind the scenes of the quest and within the tower itself.",
        "why": "Because he broke faith with his fellow Ethicals to give humanity a true path to the truth.",
        "when": "From before Burton's early waking through the saga's final revelation.",
        "how": "By waking Burton early, recruiting a chosen few, and secretly guiding them toward the tower.",
    },
}

NOTE_APPEND = " Every ACI now carries the full DLW tag with an authored six-W .spun."

with io.open(PATH, "r", encoding="utf-8") as f:
    R = json.load(f)

names_in_file = [m["name"] for m in R["members"]]
unmatched_members = [n for n in names_in_file if n not in SIX]
unmatched_map = [n for n in SIX if n not in names_in_file]
if unmatched_members:
    raise ValueError("Members with no six-W mapping: %r" % unmatched_members)
if unmatched_map:
    raise ValueError("Mappings with no matching member: %r" % unmatched_map)

count = 0
for m in R["members"]:
    six = SIX[m["name"]]
    for k in ("who", "what", "where", "why", "when", "how"):
        m[k] = six[k]
    count += 1

R["note"] = R["note"] + NOTE_APPEND

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(json.dumps(R, ensure_ascii=False, indent=2) + "\n")

# Re-parse to confirm validity
with io.open(PATH, "r", encoding="utf-8") as f:
    json.load(f)

print("Patched %d members; all six-W fields added; JSON re-parses cleanly." % count)
