
from ai import call_gpt

# ============================================================
# THE CASE OF THE MISSING HOUR
# A Story-Driven AI Detective Mystery
# ============================================================

import textwrap

# ------------------------ GAME STATE -------------------------

score = 0
collected_clues = []
visited_locations = []
interrogated_suspects = []
conversation_history = {}

game_finished = False
accusation_made = False

# ------------------------ UTILITIES --------------------------

def divider():
    print("\n" + "=" * 68)


def narrate(text):
    print(textwrap.dedent(text).strip())


def pause():
    input("\nPress Enter to continue...")


def normalize(text):
    return text.lower().strip()


def print_wrapped(text):
    print(textwrap.fill(text, width=68))


# ------------------------ INTRO STORY ------------------------

def opening_scene():
    divider()
    print("THE CASE OF THE MISSING HOUR".center(68))
    divider()

    narrate("""
    15 AUGUST 2026
    SHANTINIKETAN, WEST BENGAL

    The monsoon has been relentless.

    Rain lashes against the windows of Roy Chowdhury Bari,
    an old ancestral mansion surrounded by trees, ponds,
    and narrow mud roads.

    At 11:05 PM, a frantic phone call reaches the police.

    Dr. Arindam Roy Chowdhury, a respected engineer,
    entrepreneur, and owner of the mansion, has been found dead.

    His study door was locked.

    The windows were shut.

    The wall clock has stopped at exactly 10:17 PM.

    Four people were inside the mansion that evening.

    His wife.
    His caretaker.
    His business partner.
    And the scientist who helped create his greatest invention.

    A storm has cut off the road to the mansion.

    Until morning, you are the only detective available.

    Somewhere inside Roy Chowdhury Bari lies the truth.

    And someone is hoping you never find it.
    """)

    divider()

    narrate("""
    Your objective:

    Investigate the mansion.
    Discover clues.
    Interrogate suspects.
    Connect the evidence.
    Identify the murderer.

    Be careful.

    Not everyone who lies is a murderer.
    And not every truth is easy to uncover.
    """)

    pause()


# ------------------------ LOCATIONS ---------------------------

locations = {

    "study": {
        "name": "The Study",
        "scene": """
        The study smells of old paper, sandalwood,
        and something metallic.

        Dr. Arindam's body has already been removed.

        A chair lies overturned beside the desk.
        Papers are scattered across the floor.
        A large clock hangs crookedly on the wall.

        The clock has stopped at 10:17 PM.

        The main door appears to have been locked
        from the inside.

        Rainwater streaks the window glass.
        Yet the windows appear undisturbed.
        """,
        "clue_id": "watch"
    },

    "library": {
        "name": "The Library",
        "scene": """
        A long corridor leads to the library.

        Hundreds of books line the walls.
        A desk lamp flickers above a pile of documents.

        Several financial records have been removed
        from a cabinet.

        One drawer has been left slightly open.
        """,
        "clue_id": "ledger"
    },

    "laboratory": {
        "name": "Project Surya Laboratory",
        "scene": """
        Behind the eastern wing lies the laboratory.

        Project Surya was Dr. Arindam's life's work:
        a revolutionary energy-storage technology.

        The room contains experimental batteries,
        electrical equipment, and confidential research.

        A computer terminal is still running.
        """,
        "clue_id": "lab"
    },

    "puja room": {
        "name": "The Puja Room",
        "scene": """
        Brass lamps glow softly.

        The scent of incense lingers in the room.
        A framed photograph of the family sits
        beside the altar.

        Ananya claims she spent the evening praying here.
        """,
        "clue_id": "puja"
    },

    "kitchen": {
        "name": "The Kitchen",
        "scene": """
        The kitchen is quiet.

        A cup of tea sits on the counter.
        The kettle has cooled.

        Suman Das, the caretaker, claims he was
        preparing tea around the time of the murder.
        """,
        "clue_id": "tea"
    },

    "courtyard": {
        "name": "The Courtyard",
        "scene": """
        The courtyard is soaked by rain.

        The old stone path is slippery.
        Mud has collected near the rear entrance.

        A lantern flickers beside a wooden gate.
        """,
        "clue_id": "footprints"
    },

    "service passage": {
        "name": "The Hidden Service Passage",
        "scene": """
        Behind an old wooden panel lies a narrow passage.

        The walls are damp.
        Dust covers the floor, except for a disturbed trail.

        This passage was built decades ago
        for servants to move quietly through the mansion.

        It connects parts of the house
        that appear inaccessible from the main corridors.
        """,
        "clue_id": "passage"
    },

    "guest room": {
        "name": "Rohan's Guest Room",
        "scene": """
        Rohan Sen's guest room appears unusually tidy.

        His suitcase rests beside the wardrobe.
        A jacket hangs over a chair.

        A desk contains engineering papers,
        business correspondence, and a laptop.

        Something about the room feels hurried.
        """,
        "clue_id": "usb"
    }
}


# ------------------------ CLUES ------------------------------

clues = {

    "watch": {
        "name": "The Broken Watch",
        "description": """
        A broken wristwatch lies near the study desk.

        Its hands are frozen at 10:17 PM.

        Beneath the desk is a torn document.

        The surviving words read:

        "Technology Transfer"
        "Mumbai"
        "R.S."

        A faint patch of machine oil is visible
        near the desk.
        """
    },

    "ledger": {
        "name": "The Financial Ledger",
        "description": """
        A financial ledger reveals suspicious payments
        to Meridian Tech Pvt. Ltd., a company in Mumbai.

        The transfers were authorized by Rohan Sen.

        The amounts are unusually large.

        The transactions were made without the knowledge
        of the other Project Surya stakeholders.
        """
    },

    "lab": {
        "name": "Laboratory Access Records",
        "description": """
        The laboratory access logs show that Rohan Sen
        accessed confidential Project Surya files
        after normal working hours.

        The machine oil found in the study is consistent
        with oil used to maintain equipment in the laboratory.

        The records establish access,
        but do not alone prove murder.
        """
    },

    "puja": {
        "name": "The Incomplete Alibi",
        "description": """
        The puja room shows evidence of recent use.

        However, the evidence cannot establish
        that Ananya remained here continuously
        during the entire period of the murder.

        Her alibi is incomplete.

        An incomplete alibi is suspicious,
        but it is not proof of guilt.
        """
    },

    "tea": {
        "name": "The Untouched Tea",
        "description": """
        A cup of tea prepared for Dr. Arindam
        remains untouched.

        Suman claims he was preparing it
        around 10:00 PM.

        The tea appears to have been prepared
        earlier than his claimed timeline suggests.

        This raises a question about his timeline,
        but does not prove he murdered anyone.
        """
    },

    "footprints": {
        "name": "The Muddy Footprints",
        "description": """
        Muddy footprints lead from the courtyard
        toward the rear service corridor.

        They appear to have been made during the storm.

        Someone may have moved through this route
        while the mansion was under heavy rain.
        """
    },

    "passage": {
        "name": "The Hidden Passage",
        "description": """
        The hidden passage connects the study
        to the rear service corridor.

        A person familiar with the mansion
        could leave the study without using
        the main door.

        The locked-room mystery may not have been
        as impossible as it first appeared.
        """
    },

    "usb": {
        "name": "The Missing USB Drive",
        "description": """
        A compartment in Rohan's suitcase
        contains an empty USB-drive case.

        The case is labelled:

        PROJECT SURYA — CONFIDENTIAL

        The drive itself is missing.

        The research may have been copied
        before Dr. Arindam's death.
        """
    }
}


# ------------------------ SUSPECTS ---------------------------

suspects = {

    "ananya": {
        "name": "Ananya Roy Chowdhury",
        "role": "The Wife",
        "personality": "Reserved, emotional, and dignified.",
        "motive": "Her marriage had deteriorated, and she was considering leaving.",
        "alibi": "She claims she was praying in the puja room.",
        "secret": """
        She had been planning to leave her husband.

        She had recently discussed changes to the family will.

        She was distressed, but she did not murder him.
        """
    },

    "suman": {
        "name": "Suman Das",
        "role": "The Caretaker",
        "personality": "Quiet, loyal, cautious, and deeply familiar with the mansion.",
        "motive": "He knew the mansion's hidden passages and secrets.",
        "alibi": "He claims he was preparing tea in the kitchen.",
        "secret": """
        Suman knew about the hidden service passage.

        He had concealed its existence because he feared
        that renovations would destroy it.

        He did not murder Dr. Arindam.
        """
    },

    "rohan": {
        "name": "Rohan Sen",
        "role": "The Business Partner",
        "personality": "Charming, confident, intelligent, and defensive.",
        "motive": "He wanted financial gain and access to Project Surya.",
        "alibi": "He claims he was in the library.",
        "secret": """
        Rohan was secretly selling Project Surya research
        to Meridian Tech Pvt. Ltd. in Mumbai.

        He had received substantial payments.

        Dr. Arindam discovered the betrayal
        and planned to expose him the following morning.

        Rohan murdered Dr. Arindam at 10:17 PM.

        He escaped using the hidden service passage.

        He attempted to manipulate the scene
        to make the study appear locked from inside.
        """
    },

    "meera": {
        "name": "Dr. Meera Banerjee",
        "role": "The Scientist",
        "personality": "Brilliant, blunt, frustrated, and passionate about her work.",
        "motive": "She was removed from the Project Surya patent.",
        "alibi": "She claims she was reviewing research documents.",
        "secret": """
        Meera was furious about being removed
        from the patent application.

        She confronted Dr. Arindam earlier that evening.

        She did not murder him.
        """
    }
}


# ------------------------ COMMANDS --------------------------

def show_help():
    divider()

    narrate("""
    COMMAND GUIDE

    help
        Show this command guide.

    locations
        List all locations.

    suspects
        List all suspects.

    investigate <location>
        Explore a location and search for clues.

    interrogate <suspect>
        Question a suspect using AI dialogue.

    inventory
        Review the evidence you collected.

    journal
        Review your detective progress.

    analyze
        Ask the AI detective assistant to connect evidence.

    accuse <suspect>
        Make your final accusation.

    quit
        Leave the investigation.
    """)

    divider()


def show_locations():
    divider()
    print("LOCATIONS")
    divider()

    for key, location in locations.items():
        status = " [Investigated]" if key in visited_locations else ""
        print(f"- {location['name']}{status}")


def show_suspects():
    divider()
    print("THE FOUR SUSPECTS")
    divider()

    for key, suspect in suspects.items():
        print(f"\n{suspect['name']} — {suspect['role']}")
        print_wrapped(suspect["personality"])


# ------------------------ INVESTIGATION ----------------------

def investigate(location_name):
    global score

    location_name = normalize(location_name)

    if location_name not in locations:
        print("\nThat location is not recognized.")
        print("Type 'locations' to see available locations.")
        return

    location = locations[location_name]

    divider()
    print(location["name"].upper())
    divider()

    narrate(location["scene"])

    clue_id = location["clue_id"]

    if location_name in visited_locations:
        print("\nYou have already searched this location.")
        print("You notice nothing new.")
        return

    visited_locations.append(location_name)

    clue = clues[clue_id]

    if clue_id not in collected_clues:

        collected_clues.append(clue_id)

        score += 10

        divider()
        print("NEW EVIDENCE DISCOVERED")
        divider()

        print(clue["name"])
        narrate(clue["description"])

        print("\n+10 Detective Points")

    else:
        print("\nYou have already collected this evidence.")


# ------------------------ INVENTORY -------------------------

def show_inventory():
    divider()
    print("EVIDENCE INVENTORY")
    divider()

    if not collected_clues:
        print("\nYour evidence bag is empty.")
        return

    for number, clue_id in enumerate(collected_clues, 1):
        clue = clues[clue_id]

        print(f"\n{number}. {clue['name']}")
        narrate(clue["description"])


# ------------------------ JOURNAL ---------------------------

def show_journal():
    divider()
    print("DETECTIVE JOURNAL")
    divider()

    print(f"\nDetective Score: {score}")
    print(f"Rank: {get_rank()}")

    print(f"\nLocations explored: {len(visited_locations)}/{len(locations)}")
    print(f"Suspects questioned: {len(interrogated_suspects)}/{len(suspects)}")
    print(f"Clues collected: {len(collected_clues)}/{len(clues)}")

    print("\nLocations explored:")

    if visited_locations:
        for location in visited_locations:
            print(f"- {locations[location]['name']}")
    else:
        print("- None")

    print("\nSuspects questioned:")

    if interrogated_suspects:
        for suspect in interrogated_suspects:
            print(f"- {suspects[suspect]['name']}")
    else:
        print("- None")

    print("\nEvidence collected:")

    if collected_clues:
        for clue_id in collected_clues:
            print(f"- {clues[clue_id]['name']}")
    else:
        print("- None")


# ------------------------ RANKING ---------------------------

def get_rank():

    if score >= 100:
        return "Legendary Detective"

    elif score >= 75:
        return "Master Detective"

    elif score >= 50:
        return "Senior Investigator"

    elif score >= 25:
        return "Investigator"

    else:
        return "Novice Detective"


# ------------------------ INTERROGATION ---------------------

def interrogate(suspect_name):
    global score

    suspect_name = normalize(suspect_name)

    if suspect_name not in suspects:
        print("\nSuspect not found.")
        show_suspects()
        return

    suspect = suspects[suspect_name]

    divider()
    print(f"INTERROGATION: {suspect['name'].upper()}")
    divider()

    narrate(f"""
    You sit across from {suspect['name']}.

    {suspect['personality']}

    Their claimed alibi:

    {suspect['alibi']}
    """)

    if suspect_name not in conversation_history:
        conversation_history[suspect_name] = []

    if suspect_name not in interrogated_suspects:

        interrogated_suspects.append(suspect_name)
        score += 5

        print("\n+5 Detective Points for questioning a new suspect!")

    print("""
Ask your questions.

You may discuss:
- The victim
- Their alibi
- Their motive
- Specific clues
- Their relationships
- The events of the evening

Type 'back' to leave.
""")

    while True:

        question = input("\nDetective: ").strip()

        if normalize(question) in ["back", "exit", "leave", "quit"]:
            print(f"\nYou end the interrogation with {suspect['name']}.")
            break

        if not question:
            print("Ask a question.")
            continue

        conversation_history[suspect_name].append(
            {"role": "Detective", "content": question}
        )

        evidence_text = ""

        for clue_id in collected_clues:
            evidence_text += f"""
            {clues[clue_id]['name']}:
            {clues[clue_id]['description']}
            """

        conversation_text = ""

        for message in conversation_history[suspect_name]:
            conversation_text += (
                f"\n{message['role']}: {message['content']}"
            )

        prompt = f"""
You are roleplaying as a character in a fictional
Indian detective mystery game.

GAME:
The Case of the Missing Hour.

SETTING:
Roy Chowdhury Bari near Shantiniketan, West Bengal.
15 August 2026. Monsoon night.

CHARACTER:
Name: {suspect['name']}
Role: {suspect['role']}
Personality: {suspect['personality']}

MOTIVE:
{suspect['motive']}

ALIBI:
{suspect['alibi']}

PRIVATE CHARACTER SECRET:
{suspect['secret']}

EVIDENCE THE DETECTIVE HAS FOUND:
{evidence_text}

INTERROGATION HISTORY:
{conversation_text}

STRICT RULES:

1. Stay in character.
2. Respond naturally and conversationally.
3. Keep the response around 2-6 sentences.
4. Do not narrate the entire story.
5. Do not invent clues, locations, or suspects.
6. Do not change established facts.
7. Do not automatically confess.
8. Innocent characters must not falsely confess.
9. Rohan should be defensive and evasive.
10. Rohan must not reveal that he is the murderer
    unless the detective presents strong evidence
    and directly confronts him.
11. Do not reveal information the character
    would not reasonably know.
12. Do not reveal the complete mystery to the player.
13. React to the detective's questions and evidence.
14. Use Indian cultural context naturally when appropriate.
15. Do not break character.

Respond only as {suspect['name']}.
"""

        try:

            response = call_gpt(prompt)

            print(f"\n{suspect['name']}:")
            print_wrapped(str(response))

            conversation_history[suspect_name].append(
                {"role": "Suspect", "content": str(response)}
            )

        except Exception as error:

            print("\nThe suspect is unwilling to respond right now.")
            print("AI response unavailable.")
            print("Error:", error)


# ------------------------ AI ANALYSIS ------------------------

def analyze_evidence():
    divider()
    print("THE DETECTIVE'S ANALYSIS")
    divider()

    if len(collected_clues) < 2:
        print("\nYou need at least two clues to analyze.")
        print("Investigate more locations first.")
        return

    evidence_text = ""

    for clue_id in collected_clues:
        evidence_text += f"""
        {clues[clue_id]['name']}:

        {clues[clue_id]['description']}
        """

    suspect_text = ""

    for suspect in suspects.values():
        suspect_text += f"""
        Name: {suspect['name']}
        Role: {suspect['role']}
        Motive: {suspect['motive']}
        Alibi: {suspect['alibi']}
        """

    prompt = f"""
You are an evidence-analysis assistant
in a detective mystery game.

The player is investigating the murder
of Dr. Arindam Roy Chowdhury.

SETTING:
Roy Chowdhury Bari near Shantiniketan,
West Bengal, India.

EVIDENCE COLLECTED:
{evidence_text}

SUSPECTS:
{suspect_text}

RULES:

1. Analyze only evidence actually collected.
2. Do not invent evidence.
3. Do not reveal the murderer.
4. Do not spoil the solution.
5. Do not change story facts.
6. Do not assume guilt from motive alone.
7. Clearly distinguish facts from speculation.
8. Explain possible connections.
9. Suggest useful locations to investigate.
10. Keep the response useful and concise.

STRUCTURE YOUR RESPONSE:

Evidence Connections:
Suspicious Details:
Questions Still Unanswered:
Recommended Next Investigation:
"""

    try:

        response = call_gpt(prompt)
        print_wrapped(str(response))

    except Exception as error:

        print("\nEvidence analysis is currently unavailable.")
        print("Error:", error)


# ------------------------ ACCUSATION ------------------------

def accuse(suspect_name):
    global game_finished, score, accusation_made

    suspect_name = normalize(suspect_name)

    if suspect_name not in suspects:
        print("\nUnknown suspect.")
        show_suspects()
        return

    suspect = suspects[suspect_name]

    divider()
    print("YOUR FINAL ACCUSATION")
    divider()

    print(f"\nYou accuse {suspect['name']}.")

    narrate("""
    The rain grows louder.

    Every person in the mansion turns toward you.

    You place your evidence on the table.

    The truth must now stand on its own.
    """)

    accusation_made = True

    # The correct suspect is Rohan
    if suspect_name == "rohan":

        required_evidence = ["ledger", "lab", "passage"]

        evidence_count = 0

        for evidence in required_evidence:
            if evidence in collected_clues:
                evidence_count += 1

        # Require at least 2 important clues
        if evidence_count >= 2:

            divider()
            print("THE TRUTH")
            divider()

            narrate("""
            Rohan's smile disappears.

            The financial ledger establishes
            the secret payments to Meridian Tech.

            The laboratory records establish
            his access to confidential research.

            The hidden passage explains
            how the murderer escaped the locked study.

            The pieces finally fit together.

            Rohan Sen murdered Dr. Arindam Roy Chowdhury.

            At 10:17 PM, he confronted Arindam
            after discovering that the betrayal
            would be exposed the following morning.

            He killed his business partner.

            He then used the hidden service passage
            to leave the study.

            The locked room was a deception.

            The missing USB drive contained
            stolen Project Surya research.

            Rohan had planned to sell it
            to Meridian Tech Pvt. Ltd. in Mumbai.
            """)

            print("""
            ROHAN SEN:

            "I... I didn't think it would come to this.

            He was going to destroy everything.

            The company, the deal, my future...

            I only wanted the research.

            I never thought..."
            """)

            print("\nCASE SOLVED!")

            if evidence_count == 3:

                score += 30

                print("""
                Your investigation was exceptional.

                You connected the financial betrayal,
                laboratory access, and hidden escape route.

                You presented a complete chain of evidence.
                """)

            else:

                score += 20

                print("""
                You identified the murderer.

                However, some important evidence
                was still missing from your investigation.
                """)

        else:

            print("""
            Rohan denies your accusation.

            Your suspicion may be correct,
            but you have not established
            a convincing chain of evidence.

            The police cannot confidently proceed.

            The case remains unresolved.
            """)

            print("""
            You were close.

            But suspicion is not proof.
            """)

    else:

        print("""
        Your accusation falls apart.

        The evidence does not establish
        that this suspect committed the murder.

        The real murderer remains free.

        Somewhere in the mansion,
        the truth is still waiting.
        """)

        print("""
        THE CASE REMAINS UNSOLVED.

        The murderer was Rohan Sen.

        He secretly sold Project Surya research
        to Meridian Tech Pvt. Ltd.

        Dr. Arindam discovered his betrayal.

        Rohan murdered him at 10:17 PM
        and escaped through the hidden passage.
        """)

    game_finished = True

    show_final_score()


# ------------------------ FINAL SCORE ------------------------

def show_final_score():

    divider()
    print("YOUR DETECTIVE REPORT")
    divider()

    print(f"\nScore: {score}")
    print(f"Rank: {get_rank()}")

    print(f"\nLocations explored: {len(visited_locations)}")
    print(f"Suspects interrogated: {len(interrogated_suspects)}")
    print(f"Evidence collected: {len(collected_clues)}")

    print("\nEvidence discovered:")

    for clue_id in collected_clues:
        print(f"- {clues[clue_id]['name']}")

    print("\nYour final rank:", get_rank())


# ------------------------ AI EPILOGUE ------------------------

def generate_epilogue():

    divider()
    print("EPILOGUE")
    divider()

    prompt = f"""
Write a cinematic but concise epilogue
for the detective mystery game
"The Case of the Missing Hour".

SETTING:
Roy Chowdhury Bari near Shantiniketan,
West Bengal, India.

MONSOON:
The storm is finally calming.

PLAYER RESULTS:
Score: {score}
Rank: {get_rank()}
Locations explored: {visited_locations}
Suspects interrogated: {interrogated_suspects}
Clues discovered: {[clues[c]['name'] for c in collected_clues]}

THE ESTABLISHED STORY:
Dr. Arindam Roy Chowdhury was murdered.
Rohan Sen was the murderer.
The murder occurred at 10:17 PM.
Rohan was secretly selling Project Surya research.
The hidden passage was used to escape.

Write a short atmospheric ending.

Mention the mansion, the rain, and the detective's
achievement or failure depending on the result.

Do not introduce new story facts.
Do not change the established mystery.
"""

    try:

        response = call_gpt(prompt)
        print_wrapped(str(response))

    except Exception:

        narrate("""
        Dawn slowly rises over Shantiniketan.

        The storm has passed.

        Roy Chowdhury Bari stands silent.

        The missing hour has finally been uncovered.
        """)


# ------------------------ MAIN GAME LOOP ---------------------

def main():

    global game_finished

    opening_scene()

    show_help()

    while not game_finished:

        command = input("\nDetective > ").strip()

        if not command:
            continue

        command_lower = normalize(command)

        if command_lower == "help":
            show_help()

        elif command_lower == "locations":
            show_locations()

        elif command_lower == "suspects":
            show_suspects()

        elif command_lower == "inventory":
            show_inventory()

        elif command_lower == "journal":
            show_journal()

        elif command_lower == "analyze":
            analyze_evidence()

        elif command_lower == "quit":

            print("""
            You leave Roy Chowdhury Bari.

            The storm continues.

            The case remains open.
            """)

            game_finished = True

        elif command_lower.startswith("investigate "):

            location_name = command[12:].strip()
            investigate(location_name)

        elif command_lower.startswith("interrogate "):

            suspect_name = command[11:].strip()

            # Support full names and aliases
            for key, suspect in suspects.items():

                if suspect_name in key or suspect_name in normalize(suspect["name"]):
                    suspect_name = key
                    break

            interrogate(suspect_name)

        elif command_lower.startswith("accuse "):

            suspect_name = command[7:].strip()

            # Support full names and aliases
            for key, suspect in suspects.items():

                if suspect_name in key or suspect_name in normalize(suspect["name"]):
                    suspect_name = key
                    break

            accuse(suspect_name)

        else:

            print("\nI don't understand that command.")
            print("Type 'help' to see available commands.")

    if accusation_made:
        generate_epilogue()

    divider()

    print("THANK YOU FOR PLAYING")
    print("THE CASE OF THE MISSING HOUR")

    divider()


# ------------------------ START ------------------------------

main()
