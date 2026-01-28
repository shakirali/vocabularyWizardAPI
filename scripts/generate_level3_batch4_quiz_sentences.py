#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 3 Batch 4 vocabulary.
Creates 10 contextually rich sentences per word with strong clues for 11+ vocabulary.
"""

import csv
import re
from pathlib import Path


def create_blank_sentence(sentence: str, word: str) -> str:
    """Convert a sentence with the word into fill-in-the-blank format"""
    if not sentence or not word:
        return ""
    
    word_lower = word.lower()
    
    # Create patterns for different word forms
    patterns = [word, word_lower, word.capitalize(), word.upper()]
    
    # Add common word form variations
    if word_lower.endswith('e'):
        patterns.extend([
            word_lower + 'd',
            word_lower + 's',
            word_lower[:-1] + 'ing',
            word_lower[:-1] + 'ed',
            word_lower[:-1] + 'es'
        ])
    elif word_lower.endswith('y'):
        patterns.extend([
            word_lower[:-1] + 'ied',
            word_lower[:-1] + 'ies',
            word_lower[:-1] + 'ying'
        ])
    elif word_lower.endswith('s'):
        # For words ending in s (like meanders)
        patterns.extend([
            word_lower,
            word_lower + 'ed',
            word_lower + 'ing'
        ])
    else:
        patterns.extend([
            word_lower + 'ed',
            word_lower + 's',
            word_lower + 'ing',
            word_lower + 'er',
            word_lower + 'ly'
        ])
    
    # Replace word forms with blank
    result = sentence
    for pattern in sorted(set(patterns), key=len, reverse=True):
        regex = re.compile(r'\b' + re.escape(pattern) + r'\b', re.IGNORECASE)
        result = regex.sub("_____", result)
    
    return result


def generate_sentences_for_word(word: str, meaning: str, example: str, synonym: str, antonym: str) -> list:
    """
    Generate 10 contextually rich quiz sentences for a word.
    Each sentence provides strong contextual clues specific to the word's meaning.
    """
    sentences = []
    word_lower = word.lower()
    meaning_lower = meaning.lower()
    
    # Determine word type
    is_verb = meaning_lower.startswith("to ")
    is_adjective = any(marker in meaning_lower for marker in [
        "having", "showing", "full of", "characterised by", "characterized by",
        "very", "extremely", "quite", "rather", "causing", "deserving",
        "feeling", "arousing", "suggesting", "intending", "evoking"
    ])
    is_noun = not is_verb and not is_adjective
    
    # Generate contextually rich sentences based on word meaning
    # Each word gets custom sentences that demonstrate its specific meaning
    
    word_sentences = {
        "majestic": [
            "The _____ mountains rose above the clouds.",
            "The _____ castle stood proudly on the hilltop overlooking the kingdom.",
            "Her _____ appearance as she entered the ballroom captured everyone's attention.",
            "The _____ eagle soared high above the valley with its wings spread wide.",
            "The _____ cathedral's spires reached towards the sky like ancient fingers.",
            "His _____ voice filled the concert hall with powerful, impressive sound.",
            "The _____ waterfall cascaded down the rocky cliff in a breathtaking display.",
            "The _____ lion surveyed its territory from the highest rock.",
            "The _____ sunset painted the sky in brilliant shades of orange and gold.",
            "The _____ procession moved slowly through the streets with great dignity."
        ],
        "maladroit": [
            "His _____ attempt to fix the computer only made things worse.",
            "The _____ handling of the situation caused more problems than it solved.",
            "Her _____ movements on the dance floor showed she needed more practice.",
            "The _____ way he tried to help only created confusion for everyone.",
            "His _____ approach to the problem demonstrated his lack of skill.",
            "The _____ performance embarrassed the entire team during the competition.",
            "She felt _____ when she dropped the tray of drinks in front of everyone.",
            "His _____ efforts to repair the bicycle resulted in more broken parts.",
            "The _____ manner in which he spoke offended several people unintentionally.",
            "Her _____ attempt at cooking left the kitchen in complete disarray."
        ],
        "malicious": [
            "Spreading _____ rumours can hurt people badly.",
            "The _____ intent behind his actions was clear to everyone who witnessed them.",
            "Her _____ comments were designed to cause harm and upset.",
            "The _____ software was created to damage computer systems deliberately.",
            "His _____ behaviour towards his classmates got him into serious trouble.",
            "The _____ plot to sabotage the school play was discovered just in time.",
            "She was shocked by the _____ nature of the false accusations.",
            "The _____ attack on her reputation was completely unfounded.",
            "His _____ smile revealed that he was planning something unpleasant.",
            "The _____ gossip spread quickly through the school, causing much distress."
        ],
        "malignant": [
            "The _____ tumour required immediate treatment.",
            "The _____ disease spread rapidly through the patient's body.",
            "The _____ growth needed to be removed before it caused more damage.",
            "The doctor explained that the _____ cells were very dangerous.",
            "The _____ nature of the illness worried the medical team greatly.",
            "Early detection of the _____ condition was crucial for successful treatment.",
            "The _____ infection threatened to spread to other parts of the body.",
            "The _____ tumour had grown significantly since the last examination.",
            "The _____ disease required aggressive treatment to prevent further harm.",
            "The _____ cells were multiplying at an alarming rate."
        ],
        "malleable": [
            "Gold is a highly _____ metal.",
            "The _____ clay was easy to shape into beautiful pottery.",
            "Young children's minds are particularly _____ and can learn quickly.",
            "The _____ material could be bent and twisted without breaking.",
            "Her _____ personality meant she adapted easily to new situations.",
            "The _____ metal could be hammered into thin sheets without cracking.",
            "His _____ nature made him open to new ideas and suggestions.",
            "The _____ substance could be moulded into any form desired.",
            "The _____ character of the student made her easy to teach.",
            "The _____ plastic could be shaped when heated and would harden when cooled."
        ],
        "manifest": [
            "His talent _____ itself at an early age.",
            "The symptoms began to _____ themselves after a few days of illness.",
            "Her excitement _____ in her bright eyes and wide smile.",
            "The problem will _____ if we don't address it soon.",
            "His anger _____ itself in his clenched fists and red face.",
            "The effects of the drought began to _____ in the wilting crops.",
            "Her leadership skills _____ during the group project.",
            "The truth will eventually _____ itself despite attempts to hide it.",
            "His determination _____ in his refusal to give up.",
            "The changes began to _____ after the new policy was introduced."
        ],
        "maverick": [
            "The _____ scientist challenged the accepted theories.",
            "The _____ politician refused to follow the party line.",
            "Her _____ approach to teaching inspired her students.",
            "The _____ artist created works that broke all traditional rules.",
            "His _____ ideas often led to innovative solutions.",
            "The _____ inventor was never afraid to try unconventional methods.",
            "She was known as a _____ for her independent thinking.",
            "The _____ entrepreneur started a business that nobody believed would succeed.",
            "His _____ behaviour made him stand out from the crowd.",
            "The _____ musician played instruments in ways nobody had tried before."
        ],
        "meanders": [
            "The river _____ through the valley before reaching the sea.",
            "The path _____ up the hillside, taking the scenic route.",
            "The conversation _____ from topic to topic without any clear direction.",
            "The stream _____ through the forest, creating beautiful curves.",
            "Her thoughts _____ as she tried to focus on the difficult problem.",
            "The road _____ through the countryside, avoiding the steepest hills.",
            "The trail _____ around the ancient oak trees.",
            "The river _____ lazily through the peaceful countryside.",
            "The path _____ between the flowerbeds in the garden.",
            "The stream _____ down the mountainside, following the natural contours."
        ],
        "mediocre": [
            "The film received _____ reviews from the critics.",
            "His _____ performance disappointed those who expected better.",
            "The _____ quality of the work was evident to everyone.",
            "She refused to accept _____ results and worked harder.",
            "The _____ meal was neither terrible nor excellent.",
            "His _____ attempt at the exam showed he hadn't studied enough.",
            "The _____ weather was neither sunny nor rainy, just cloudy.",
            "The _____ book failed to capture the reader's interest.",
            "Her _____ skills were not good enough for the advanced class.",
            "The _____ painting lacked the detail and skill of better works."
        ],
        "melodious": [
            "The _____ song was beautiful to hear.",
            "The _____ voice of the singer filled the concert hall.",
            "The _____ sound of the birds greeted the morning.",
            "Her _____ laughter was like music to his ears.",
            "The _____ tune played softly in the background.",
            "The _____ notes from the piano drifted through the open window.",
            "The _____ harmony of the choir brought tears to many eyes.",
            "The _____ sound of the violin was enchanting.",
            "The _____ melody was stuck in everyone's head for days.",
            "The _____ chimes of the bell tower could be heard across the village."
        ],
        "menacing": [
            "The dark clouds looked _____ as the storm approached.",
            "The _____ growl of the dog warned them to stay away.",
            "His _____ expression frightened the younger children.",
            "The _____ shadow moved slowly across the wall.",
            "The _____ tone of his voice made everyone nervous.",
            "The _____ figure in the dark alley made her quicken her pace.",
            "The _____ storm clouds gathered overhead, threatening rain.",
            "His _____ stare made it clear he was very angry.",
            "The _____ sound of breaking glass startled everyone.",
            "The _____ atmosphere in the room made conversation difficult."
        ],
        "merciless": [
            "The _____ ruler showed no kindness to his enemies.",
            "The _____ sun beat down on the desert travellers.",
            "Her _____ criticism destroyed his confidence completely.",
            "The _____ judge showed no leniency to the criminals.",
            "The _____ storm destroyed everything in its path.",
            "His _____ teasing made the new student feel unwelcome.",
            "The _____ heat made it impossible to work outside.",
            "The _____ attack left no survivors.",
            "Her _____ determination to win at all costs worried her teammates.",
            "The _____ wind tore through the village, causing widespread damage."
        ],
        "mercurial": [
            "His _____ temperament made him hard to work with.",
            "The _____ weather changed from sunny to stormy in minutes.",
            "Her _____ moods shifted rapidly throughout the day.",
            "The _____ nature of the situation made planning difficult.",
            "His _____ personality meant you never knew how he would react.",
            "The _____ stock market made investors nervous.",
            "Her _____ behaviour confused her friends constantly.",
            "The _____ politician changed his position on issues frequently.",
            "His _____ character made him unpredictable and exciting.",
            "The _____ changes in her attitude worried her parents."
        ],
        "mesmerise": [
            "The magician's tricks seemed to _____ the audience.",
            "The beautiful dance performance seemed to _____ everyone watching.",
            "The flickering flames of the fire began to _____ the tired campers.",
            "The hypnotist's voice seemed to _____ the volunteer on stage.",
            "The stunning sunset appeared to _____ all who witnessed it.",
            "The rhythmic drumming began to _____ the listeners.",
            "The graceful movements of the swan seemed to _____ the onlookers.",
            "The storyteller's voice seemed to _____ the children completely.",
            "The swirling patterns seemed to _____ anyone who looked at them.",
            "The beautiful music seemed to _____ the entire audience."
        ],
        "metaphor": [
            "Saying 'time is money' is a _____ that compares time to currency.",
            "The author used a _____ to describe her feelings as a storm.",
            "The teacher explained that 'her heart is a garden' is a _____.",
            "The _____ helped the students understand the difficult concept.",
            "The poet's use of _____ made the poem more interesting.",
            "The _____ 'life is a journey' is commonly used in literature.",
            "She used a _____ to explain how she felt about the situation.",
            "The _____ made the abstract idea easier to visualise.",
            "The writer's clever _____ added depth to the story.",
            "The _____ 'the world is a stage' comes from Shakespeare."
        ],
        "metonymy": [
            "Using 'the crown' to refer to the monarchy is an example of _____.",
            "The _____ 'the pen is mightier than the sword' uses this figure of speech.",
            "When we say 'the White House announced', we're using _____.",
            "The _____ 'suits' to mean businesspeople is common in English.",
            "The teacher explained how _____ works by using associated words.",
            "The _____ 'Downing Street' refers to the British government.",
            "The poet's use of _____ added layers of meaning to the poem.",
            "The _____ 'the press' to mean journalists is widely understood.",
            "The author's clever use of _____ made the writing more interesting.",
            "The _____ 'Hollywood' often refers to the American film industry."
        ],
        "miniscule": [
            "The _____ insect was barely visible.",
            "The _____ details in the painting required a magnifying glass to see.",
            "Her handwriting was so _____ that it was difficult to read.",
            "The _____ amount of sugar wouldn't affect the recipe.",
            "The _____ print in the contract was almost impossible to read.",
            "The _____ particles floated in the air like dust.",
            "The _____ difference between the two options was negligible.",
            "The _____ creature scurried across the kitchen floor.",
            "The _____ font size made reading the document very difficult.",
            "The _____ crack in the window was barely noticeable."
        ],
        "mitigate": [
            "Trees can help _____ the effects of pollution.",
            "The medicine helped _____ the pain in her injured leg.",
            "They tried to _____ the damage caused by the flood.",
            "The new policy was designed to _____ the problems in the system.",
            "Her apology helped _____ his anger about the situation.",
            "The cushion helped _____ the impact of the fall.",
            "They worked hard to _____ the consequences of their mistake.",
            "The warning system helped _____ the danger from the approaching storm.",
            "The compromise helped _____ the conflict between the two groups.",
            "The safety measures helped _____ the risks involved."
        ],
        "mnemonic": [
            "The rhyme 'i before e except after c' is a _____ for spelling.",
            "She created a _____ to help remember the planets in order.",
            "The _____ device helped him memorise all the capital cities.",
            "The teacher taught them a _____ to remember the multiplication tables.",
            "The _____ 'My Very Educated Mother Just Served Us Noodles' helps recall planets.",
            "He used a _____ to remember the colours of the rainbow.",
            "The _____ made it much easier to learn the historical dates.",
            "She invented a _____ to help with the difficult vocabulary words.",
            "The _____ technique improved her ability to remember facts.",
            "The _____ 'Every Good Boy Deserves Fruit' helps remember musical notes."
        ],
        "momentous": [
            "The moon landing was a _____ achievement.",
            "The _____ decision would change the course of history.",
            "The _____ occasion called for a grand celebration.",
            "The _____ event was remembered for generations to come.",
            "The _____ discovery revolutionised the field of science.",
            "The _____ announcement shocked everyone in the room.",
            "The _____ day marked the beginning of a new era.",
            "The _____ victory was celebrated throughout the country.",
            "The _____ meeting would determine the future of the company.",
            "The _____ moment was captured in photographs and paintings."
        ],
        "monotony": [
            "The _____ of the daily routine made him long for adventure.",
            "The _____ of doing the same task repeatedly bored her.",
            "The _____ of the long journey made everyone restless.",
            "The _____ of the repetitive work was broken by occasional breaks.",
            "The _____ of the grey sky matched his mood perfectly.",
            "The _____ of the endless fields stretched to the horizon.",
            "The _____ of the daily schedule needed some variety.",
            "The _____ of the constant rain made everyone feel gloomy.",
            "The _____ of the routine was relieved by unexpected events.",
            "The _____ of the repetitive pattern became hypnotic."
        ],
        "mournful": [
            "The _____ music brought tears to her eyes.",
            "The _____ expression on his face showed his deep sadness.",
            "The _____ sound of the bell echoed across the empty churchyard.",
            "The _____ atmosphere in the room made everyone feel sombre.",
            "The _____ cry of the bird sounded like a lament.",
            "The _____ tone of her voice revealed her grief.",
            "The _____ melody expressed the composer's sorrow.",
            "The _____ look in his eyes showed he was thinking of lost friends.",
            "The _____ silence filled the room after the sad news.",
            "The _____ poem captured the feeling of loss perfectly."
        ],
        "nauseous": [
            "The bumpy car ride made her feel _____.",
            "The smell of the spoiled food made him feel _____.",
            "The _____ feeling in her stomach made it hard to concentrate.",
            "The motion of the boat made several passengers feel _____.",
            "The _____ sensation passed after she got some fresh air.",
            "The thought of eating made her feel even more _____.",
            "The _____ feeling was caused by the strong medication.",
            "The spinning ride made many children feel _____.",
            "The _____ sensation made her lie down for a while.",
            "The combination of heat and exhaustion made him feel _____."
        ],
        "nefarious": [
            "The villain had a _____ plan to steal the crown jewels.",
            "The _____ scheme was discovered before it could be carried out.",
            "His _____ activities were finally exposed by the police.",
            "The _____ plot involved several criminal acts.",
            "The _____ character in the story was truly evil.",
            "The _____ intentions behind his actions were clear.",
            "The _____ plan was designed to cause maximum harm.",
            "The _____ deeds of the criminal shocked the community.",
            "The _____ scheme was more complex than anyone imagined.",
            "The _____ nature of the crime made it particularly serious."
        ],
        "negotiate": [
            "They began to _____ a peace agreement.",
            "The two sides agreed to _____ a settlement.",
            "She learned to _____ better deals at the market.",
            "The diplomats worked hard to _____ a treaty.",
            "He tried to _____ a better price for the car.",
            "The union leaders met to _____ with the company.",
            "They had to _____ the terms of the contract carefully.",
            "The countries agreed to _____ an end to the conflict.",
            "She managed to _____ a shorter working day.",
            "The teams met to _____ the rules of the competition."
        ],
        "nostalgia": [
            "Looking at old photos filled her with _____.",
            "The _____ for her childhood home made her feel homesick.",
            "The old song brought back feelings of _____.",
            "The _____ for simpler times was evident in his writing.",
            "The visit to her old school filled her with _____.",
            "The _____ for the past made her wish she could go back.",
            "The old film evoked a sense of _____ in the audience.",
            "The _____ for her grandmother's cooking made her sad.",
            "The familiar smell triggered feelings of _____.",
            "The _____ for her school days grew stronger as she got older."
        ],
        "notoriety": [
            "The criminal gained _____ for his daring escapes.",
            "The _____ of the haunted house spread throughout the town.",
            "His _____ as a troublemaker preceded him wherever he went.",
            "The _____ of the incident made it difficult to forget.",
            "The _____ of the place made tourists curious to visit.",
            "Her _____ as a brilliant scientist was well-deserved.",
            "The _____ of the event attracted media attention.",
            "His _____ for being late was legendary among his friends.",
            "The _____ of the restaurant drew customers from far away.",
            "The _____ of the legend grew with each retelling."
        ],
        "obdurate": [
            "Despite the evidence, he remained _____ in his beliefs.",
            "The _____ refusal to change frustrated everyone.",
            "Her _____ attitude made compromise impossible.",
            "The _____ stance on the issue prevented any progress.",
            "His _____ nature meant he never admitted he was wrong.",
            "The _____ resistance to new ideas slowed down the project.",
            "Her _____ determination to succeed impressed everyone.",
            "The _____ position made negotiations very difficult.",
            "His _____ insistence on his way caused many arguments.",
            "The _____ refusal to listen to reason was problematic."
        ],
        "obedient": [
            "The _____ dog followed every command.",
            "The _____ child always did as she was told.",
            "The _____ student never caused any trouble in class.",
            "The _____ servant carried out all instructions promptly.",
            "The _____ behaviour pleased the strict teacher.",
            "The _____ pet never wandered far from home.",
            "The _____ response showed she understood the rules.",
            "The _____ manner in which he followed orders was impressive.",
            "The _____ attitude made her popular with authority figures.",
            "The _____ way she completed tasks made her reliable."
        ],
        "obfuscate": [
            "The politician tried to _____ the truth with complicated language.",
            "The confusing explanation seemed designed to _____ the real issue.",
            "The technical jargon was used to _____ the simple facts.",
            "He tried to _____ his mistake by changing the subject.",
            "The long-winded speech seemed intended to _____ the main point.",
            "The complicated instructions served to _____ the simple process.",
            "She tried to _____ her real intentions with vague statements.",
            "The misleading information was meant to _____ the truth.",
            "The complex language was used to _____ the basic meaning.",
            "He attempted to _____ his role in the incident."
        ],
        "oblivion": [
            "The old building fell into _____ after it was abandoned.",
            "The forgotten artist's work sank into _____.",
            "The ancient language faded into _____ over the centuries.",
            "The old custom fell into _____ as times changed.",
            "The once-famous actor drifted into _____ after his last film.",
            "The old tradition was in danger of falling into _____.",
            "The ancient civilisation disappeared into _____.",
            "The old song had fallen into _____ until someone rediscovered it.",
            "The forgotten hero's deeds had passed into _____.",
            "The old technique had fallen into _____ until recently."
        ],
        "oblivious": [
            "She was _____ to the noise around her.",
            "He remained _____ to the problems he was causing.",
            "The _____ student didn't notice the teacher's warning look.",
            "She was completely _____ to the danger ahead.",
            "The _____ driver didn't see the warning sign.",
            "He seemed _____ to the fact that he was being rude.",
            "The _____ child didn't notice everyone was waiting for her.",
            "She was _____ to the changes happening around her.",
            "The _____ tourist didn't realise he was breaking local customs.",
            "He remained _____ to the effect his words had on others."
        ],
        "obnoxious": [
            "His _____ behaviour annoyed everyone.",
            "The _____ smell from the rubbish bin made her feel sick.",
            "The _____ comments offended several people.",
            "The _____ noise from the construction site disturbed the neighbourhood.",
            "Her _____ attitude made her very unpopular.",
            "The _____ way he interrupted others was rude.",
            "The _____ taste of the medicine made it hard to swallow.",
            "His _____ personality made it difficult to work with him.",
            "The _____ sound of the alarm clock woke everyone up.",
            "The _____ manner in which he spoke to people was unacceptable."
        ],
        "obsessive": [
            "His _____ behaviour about cleanliness worried his family.",
            "The _____ attention to detail made the work perfect.",
            "Her _____ interest in the subject consumed all her time.",
            "The _____ need to check everything slowed down the process.",
            "His _____ focus on winning made him ignore everything else.",
            "The _____ way she organised her books was impressive.",
            "His _____ concern about safety was sometimes excessive.",
            "The _____ dedication to the project was admirable but concerning.",
            "Her _____ need for perfection made her very stressed.",
            "The _____ behaviour patterns were difficult to break."
        ],
        "officious": [
            "The _____ security guard kept telling everyone what to do.",
            "The _____ way she interfered annoyed her colleagues.",
            "The _____ manner in which he gave orders was irritating.",
            "The _____ behaviour of the supervisor made everyone uncomfortable.",
            "Her _____ attempts to help were actually unhelpful.",
            "The _____ way he managed things was overbearing.",
            "The _____ attitude made her very unpopular with the team.",
            "The _____ interference in others' work was resented.",
            "His _____ approach to organising the event was too controlling.",
            "The _____ way she took charge was not appreciated."
        ],
        "omnivore": [
            "Humans are _____, able to digest both vegetables and meat.",
            "The bear is an _____ that eats berries, fish, and small animals.",
            "The _____ diet includes both plant and animal foods.",
            "As an _____, the raccoon will eat almost anything it finds.",
            "The _____ can survive in many different environments.",
            "The _____ has a varied diet that includes many food types.",
            "The _____ nature of humans allows for flexible eating habits.",
            "The _____ will eat fruits, nuts, insects, and small creatures.",
            "The _____ diet provides a wide range of nutrients.",
            "The _____ can adapt its diet based on what's available."
        ],
        "operandi": [
            "The detective studied the criminal's modus _____ carefully.",
            "The modus _____ of the thief was always the same.",
            "The criminal's modus _____ involved breaking in through windows.",
            "The modus _____ revealed patterns in the crimes.",
            "The police identified the modus _____ used in the robberies.",
            "The modus _____ showed how the criminal always worked.",
            "The detective recognised the modus _____ from previous cases.",
            "The modus _____ was distinctive and easy to identify.",
            "The modus _____ involved careful planning and timing.",
            "The modus _____ helped link several crimes together."
        ],
        "optimist": [
            "Even in difficult times, the _____ remained cheerful.",
            "The _____ always saw the bright side of every situation.",
            "As an _____, she believed things would work out well.",
            "The _____ refused to be discouraged by setbacks.",
            "The _____ outlook helped her through difficult times.",
            "The _____ always expected the best possible outcome.",
            "The _____ found hope even in the darkest moments.",
            "The _____ attitude was infectious and lifted everyone's spirits.",
            "The _____ believed that tomorrow would be better.",
            "The _____ never lost faith that things would improve."
        ],
        "optional": [
            "The school trip was _____, so not everyone attended.",
            "The _____ homework assignment could be completed for extra credit.",
            "The _____ uniform items were not required but could be worn.",
            "The _____ reading was recommended but not compulsory.",
            "The _____ activities were available for those who wanted them.",
            "The _____ field trip was open to all interested students.",
            "The _____ workshop was available but not mandatory.",
            "The _____ course could be taken in addition to required subjects.",
            "The _____ equipment was nice to have but not essential.",
            "The _____ meeting was open to anyone who wanted to attend."
        ],
        "opulence": [
            "The _____ of the palace amazed all the visitors.",
            "The _____ of the wealthy family was evident in their home.",
            "The _____ of the decorations made the ballroom magnificent.",
            "The _____ of the feast impressed all the guests.",
            "The _____ of the royal court was legendary.",
            "The _____ of the mansion was overwhelming.",
            "The _____ of the lifestyle was beyond most people's imagination.",
            "The _____ of the jewellery collection was remarkable.",
            "The _____ of the furnishings showed great wealth.",
            "The _____ of the celebration was fit for royalty."
        ],
        "ordained": [
            "The new law was _____ by the government last month.",
            "The ceremony _____ the new priest into the church.",
            "The rules were _____ by the school board.",
            "The tradition was _____ by ancient custom.",
            "The procedure was _____ by the official regulations.",
            "The practice was _____ by long-standing tradition.",
            "The ritual was _____ by religious law.",
            "The ceremony _____ the beginning of the new era.",
            "The rules were _____ by the governing body.",
            "The custom was _____ by generations of practice."
        ],
        "oscillate": [
            "The pendulum began to _____ when released.",
            "The fan blades _____ back and forth in the breeze.",
            "The temperature seemed to _____ between hot and cold.",
            "His opinion seemed to _____ depending on who he was talking to.",
            "The needle on the compass began to _____ wildly.",
            "The decision seemed to _____ between two options.",
            "The swing continued to _____ in the gentle wind.",
            "The mood seemed to _____ between excitement and worry.",
            "The light seemed to _____ as the power fluctuated.",
            "The debate seemed to _____ between the two sides."
        ],
        "overwhelm": [
            "The kindness of strangers _____ her.",
            "The amount of homework began to _____ the students.",
            "The flood waters threatened to _____ the small village.",
            "The news seemed to _____ him with emotion.",
            "The responsibilities began to _____ the new manager.",
            "The beauty of the view seemed to _____ all who saw it.",
            "The support from friends helped but didn't _____ the sadness.",
            "The number of tasks seemed to _____ her completely.",
            "The force of the wave threatened to _____ the small boat.",
            "The generosity of the donation seemed to _____ the charity workers."
        ],
        "oxymoron": [
            "'Bittersweet' is an _____ that combines opposite meanings.",
            "The phrase 'deafening silence' is an example of an _____.",
            "The _____ 'jumbo shrimp' seems contradictory but makes sense.",
            "The teacher explained that 'pretty ugly' is an _____.",
            "The _____ 'living dead' is commonly used in stories.",
            "The phrase 'open secret' is an example of an _____.",
            "The _____ 'awfully good' combines contradictory words.",
            "The phrase 'original copy' is an _____.",
            "The _____ 'seriously funny' seems to contradict itself.",
            "The phrase 'alone together' is an example of an _____."
        ],
        "pacifist": [
            "The _____ refused to join the army, believing in peaceful solutions.",
            "The _____ protested against the war with peaceful demonstrations.",
            "The _____ believed that violence was never the answer.",
            "The _____ worked to promote peace and understanding.",
            "The _____ opposed all forms of conflict and fighting.",
            "The _____ dedicated their life to peaceful causes.",
            "The _____ refused to use violence even in self-defence.",
            "The _____ believed in solving problems through discussion.",
            "The _____ worked tirelessly for world peace.",
            "The _____ was committed to non-violent solutions."
        ],
        "pacifying": [
            "The _____ music helped the baby fall asleep.",
            "The _____ words calmed the frightened child.",
            "The _____ effect of the medicine helped reduce the pain.",
            "The _____ tone of her voice soothed the anxious patient.",
            "The _____ gesture helped ease the tension in the room.",
            "The _____ atmosphere of the garden helped her relax.",
            "The _____ effect of the warm bath was immediate.",
            "The _____ words helped resolve the conflict peacefully.",
            "The _____ influence of the teacher calmed the noisy classroom.",
            "The _____ effect of the sunset made everyone feel peaceful."
        ],
        "palpable": [
            "The tension in the room was _____.",
            "The excitement was _____ as the results were announced.",
            "The relief was _____ when the good news arrived.",
            "The fear was _____ in the dark, silent house.",
            "The joy was _____ at the surprise party.",
            "The anger was _____ in his voice as he spoke.",
            "The disappointment was _____ after the team lost.",
            "The anticipation was _____ before the performance began.",
            "The sadness was _____ in her expression.",
            "The enthusiasm was _____ among the students."
        ],
        "paradigm": [
            "The new teaching method became a _____ for other schools.",
            "The successful business model became a _____ for others to follow.",
            "The _____ shift changed how people thought about the problem.",
            "The _____ of modern education has evolved significantly.",
            "The new _____ revolutionised the field of science.",
            "The _____ example showed others how to succeed.",
            "The _____ shift required everyone to adapt.",
            "The successful approach became a _____ for future projects.",
            "The _____ model was copied by many competitors.",
            "The new _____ changed the way things were done."
        ],
        "parsimony": [
            "His _____ meant he never spent money on anything unnecessary.",
            "The _____ of the old man was legendary in the village.",
            "Her extreme _____ made her very wealthy but not very happy.",
            "The _____ prevented him from enjoying life's simple pleasures.",
            "The _____ was so extreme that he reused everything possible.",
            "His _____ meant he never bought anything new if he could help it.",
            "The _____ made him very careful with every penny.",
            "Her _____ was evident in her refusal to spend money.",
            "The _____ meant he saved every possible expense.",
            "His _____ made him reluctant to share with others."
        ],
        "partisan": [
            "The _____ crowd cheered only for their team.",
            "The _____ support was divided along political lines.",
            "The _____ debate showed strong loyalty to each side.",
            "The _____ nature of the discussion prevented compromise.",
            "The _____ crowd was completely biased in their support.",
            "The _____ attitude made neutral discussion impossible.",
            "The _____ supporters refused to consider other viewpoints.",
            "The _____ nature of the conflict made resolution difficult.",
            "The _____ crowd showed clear favouritism.",
            "The _____ support was unwavering despite the evidence."
        ],
        "pathetic": [
            "The _____ attempt at an excuse convinced no one.",
            "The _____ sight of the abandoned puppy made her cry.",
            "The _____ performance disappointed everyone who watched.",
            "The _____ excuse was so weak that nobody believed it.",
            "The _____ attempt to help only made things worse.",
            "The _____ display of effort was barely noticeable.",
            "The _____ condition of the old house was sad to see.",
            "The _____ excuse was met with disbelief.",
            "The _____ attempt showed a complete lack of skill.",
            "The _____ sight moved everyone to pity."
        ],
        "pedantic": [
            "His _____ corrections annoyed his colleagues.",
            "The _____ attention to minor details slowed everything down.",
            "Her _____ way of speaking made conversations tedious.",
            "The _____ focus on rules frustrated the creative students.",
            "His _____ insistence on proper grammar was excessive.",
            "The _____ corrections interrupted the flow of conversation.",
            "Her _____ nature made her unpopular with her peers.",
            "The _____ approach to teaching stifled creativity.",
            "His _____ behaviour made him seem like a know-it-all.",
            "The _____ way she corrected everyone was irritating."
        ],
        "penchant": [
            "She had a _____ for Italian food.",
            "His _____ for adventure led him to travel the world.",
            "The child had a _____ for asking difficult questions.",
            "Her _____ for reading meant she always had a book.",
            "His _____ for collecting stamps filled several albums.",
            "The student had a _____ for mathematics and science.",
            "Her _____ for helping others made her very popular.",
            "His _____ for music was evident in his extensive collection.",
            "The teacher had a _____ for making learning fun.",
            "Her _____ for organisation made her very efficient."
        ],
        "perchance": [
            "_____ we will meet again in the future.",
            "_____ the weather will improve by tomorrow.",
            "_____ you might reconsider your decision.",
            "_____ the lost item will be found eventually.",
            "_____ they will arrive before the meeting starts.",
            "_____ the problem will solve itself in time.",
            "_____ we can find a solution that works for everyone.",
            "_____ the situation will improve with patience.",
            "_____ they will understand our point of view.",
            "_____ fortune will smile upon our efforts."
        ],
        "perpetual": [
            "The _____ motion of the waves was soothing to watch.",
            "The _____ noise from the construction site was annoying.",
            "The _____ cycle of seasons continued year after year.",
            "The _____ smile on her face never seemed to fade.",
            "The _____ problem seemed to have no solution.",
            "The _____ movement of the clock's hands marked the time.",
            "The _____ struggle for perfection was exhausting.",
            "The _____ rain made the ground constantly muddy.",
            "The _____ motion machine was an impossible dream.",
            "The _____ state of change made planning difficult."
        ],
        "persevere": [
            "If you _____, you will eventually succeed.",
            "She had to _____ through many difficulties to reach her goal.",
            "The team had to _____ despite the setbacks.",
            "He encouraged her to _____ with her studies.",
            "The climbers had to _____ through the harsh weather.",
            "She learned to _____ when things got difficult.",
            "The students had to _____ to complete the challenging project.",
            "He had to _____ through the pain to finish the race.",
            "The team had to _____ despite being behind.",
            "She had to _____ through the criticism to achieve her dream."
        ],
        "perturbed": [
            "She was _____ by the strange noises coming from the attic.",
            "The unexpected news _____ him greatly.",
            "The disturbing discovery _____ everyone who heard about it.",
            "She was _____ by the sudden change in plans.",
            "The unusual behaviour _____ his parents.",
            "She was _____ by the thought of the upcoming exam.",
            "The mysterious disappearance _____ the entire community.",
            "She was _____ by the lack of response to her message.",
            "The unexpected turn of events _____ all involved.",
            "She was _____ by the strange expression on his face."
        ],
        "pervasive": [
            "The influence of technology is _____.",
            "The _____ smell of flowers filled the entire garden.",
            "The _____ nature of the problem affected everyone.",
            "The _____ influence of social media is evident everywhere.",
            "The _____ feeling of excitement spread through the crowd.",
            "The _____ use of mobile phones has changed society.",
            "The _____ nature of the issue made it difficult to ignore.",
            "The _____ influence of the teacher inspired many students.",
            "The _____ atmosphere of tension made everyone nervous.",
            "The _____ spread of the idea changed how people thought."
        ],
        "pessimism": [
            "His constant _____ made it difficult to stay positive.",
            "The _____ in her outlook worried her friends.",
            "The _____ of the situation made everyone feel hopeless.",
            "His _____ prevented him from seeing any good outcomes.",
            "The _____ in his attitude was contagious.",
            "Her _____ made it hard to find solutions.",
            "The _____ of the forecast discouraged everyone.",
            "His _____ blinded him to opportunities.",
            "The _____ in her thinking limited her possibilities.",
            "His _____ made him expect the worst in every situation."
        ],
        "pessimist": [
            "The _____ always expected the worst to happen.",
            "The _____ predicted failure before even trying.",
            "The _____ saw problems where others saw opportunities.",
            "The _____ refused to believe things could improve.",
            "The _____ always focused on what could go wrong.",
            "The _____ discouraged others with negative predictions.",
            "The _____ found fault with every plan.",
            "The _____ expected disappointment at every turn.",
            "The _____ saw the glass as half empty.",
            "The _____ always anticipated problems and difficulties."
        ],
        "petulant": [
            "The _____ child refused to play.",
            "The _____ behaviour showed immaturity.",
            "Her _____ response to the request was childish.",
            "The _____ way he reacted surprised everyone.",
            "The _____ outburst embarrassed his parents.",
            "Her _____ attitude made her difficult to work with.",
            "The _____ refusal to cooperate caused problems.",
            "The _____ manner in which she spoke was inappropriate.",
            "His _____ behaviour was unbecoming for someone his age.",
            "The _____ reaction showed a lack of self-control."
        ],
        "phenomena": [
            "Lightning and thunder are natural _____.",
            "The Northern Lights are one of nature's most beautiful _____.",
            "The scientific _____ was observed and recorded carefully.",
            "The unusual _____ puzzled the researchers.",
            "The natural _____ occurred regularly during the summer months.",
            "The rare _____ attracted scientists from around the world.",
            "The mysterious _____ had no clear explanation.",
            "The fascinating _____ was studied for many years.",
            "The natural _____ was captured on camera.",
            "The unusual _____ defied explanation."
        ],
        "plaintiff": [
            "The _____ claimed damages for the accident.",
            "The _____ brought the case to court.",
            "The _____ sought compensation for the injury.",
            "The _____ presented evidence to support the claim.",
            "The _____ waited anxiously for the court's decision.",
            "The _____ hoped for a fair settlement.",
            "The _____ argued that the defendant was responsible.",
            "The _____ provided testimony about what happened.",
            "The _____ sought justice for the wrong that was done.",
            "The _____ presented the case before the judge."
        ],
        "platitude": [
            "His speech was full of empty _____.",
            "The _____ 'time heals all wounds' didn't help much.",
            "The _____ sounded good but meant nothing.",
            "The _____ was repeated so often it lost all meaning.",
            "The _____ 'everything happens for a reason' offered little comfort.",
            "The _____ was clichéd and unhelpful.",
            "The _____ 'it could be worse' didn't make anyone feel better.",
            "The _____ was overused and meaningless.",
            "The _____ 'what doesn't kill you makes you stronger' was trite.",
            "The _____ added nothing useful to the conversation."
        ],
        "plausible": [
            "Her excuse seemed _____ so we believed her.",
            "The _____ explanation made sense to everyone.",
            "The _____ story was easy to believe.",
            "The _____ reason for the delay was accepted.",
            "The _____ theory seemed reasonable.",
            "The _____ account of events matched the evidence.",
            "The _____ excuse was believable.",
            "The _____ explanation satisfied everyone's questions.",
            "The _____ story was consistent with the facts.",
            "The _____ reason seemed logical and reasonable."
        ],
        "pleasing": [
            "The _____ melody filled the room with joy.",
            "The _____ appearance of the garden delighted visitors.",
            "The _____ sound of laughter made everyone smile.",
            "The _____ colours of the sunset were beautiful.",
            "The _____ taste of the meal satisfied everyone.",
            "The _____ sight of the flowers brightened the day.",
            "The _____ aroma of fresh bread filled the bakery.",
            "The _____ effect of the music was immediate.",
            "The _____ view from the window was spectacular.",
            "The _____ atmosphere made everyone feel welcome."
        ],
        "plethora": [
            "There was a _____ of books to choose from.",
            "The _____ of options made decision-making difficult.",
            "The garden had a _____ of colourful flowers.",
            "The _____ of information was overwhelming.",
            "The _____ of choices confused the customers.",
            "The _____ of food at the buffet was impressive.",
            "The _____ of activities kept everyone busy.",
            "The _____ of opportunities was exciting.",
            "The _____ of resources made the project easier.",
            "The _____ of ideas generated much discussion."
        ],
        "poignancy": [
            "The _____ of the farewell brought tears to everyone's eyes.",
            "The _____ of the moment was deeply felt by all.",
            "The _____ of the story touched everyone's heart.",
            "The _____ of the memory made her smile sadly.",
            "The _____ of the scene was overwhelming.",
            "The _____ of the words moved the audience.",
            "The _____ of the situation was not lost on anyone.",
            "The _____ of the moment created a lasting impression.",
            "The _____ of the farewell was bittersweet.",
            "The _____ of the memory brought back strong emotions."
        ],
        "poignant": [
            "The film had a _____ ending.",
            "The _____ moment brought tears to many eyes.",
            "The _____ story touched everyone who heard it.",
            "The _____ scene was difficult to watch.",
            "The _____ memory stayed with her for years.",
            "The _____ words expressed deep emotion.",
            "The _____ farewell was emotional for everyone.",
            "The _____ moment captured the essence of the story.",
            "The _____ scene was beautifully written.",
            "The _____ ending left a lasting impression."
        ],
        "ponderous": [
            "The _____ elephant moved slowly.",
            "The _____ book was too heavy to carry easily.",
            "The _____ speech bored the audience.",
            "The _____ machinery moved with great effort.",
            "The _____ style of writing made reading difficult.",
            "The _____ movement of the old truck was noticeable.",
            "The _____ pace of the lesson made time drag.",
            "The _____ weight of the responsibility was felt.",
            "The _____ manner of speaking was tedious.",
            "The _____ clouds moved slowly across the sky."
        ],
        "potential": [
            "She has the _____ to become a great scientist.",
            "The _____ for growth was evident in the young plant.",
            "The _____ of the idea excited everyone.",
            "The student showed great _____ in mathematics.",
            "The _____ energy stored in the battery was significant.",
            "The _____ for success was clear from the start.",
            "The _____ of the discovery was enormous.",
            "The young athlete showed great _____.",
            "The _____ of the project was promising.",
            "The _____ for improvement was obvious."
        ],
        "pragmatic": [
            "The _____ solution solved the problem quickly.",
            "The _____ approach focused on what would actually work.",
            "Her _____ attitude helped find practical solutions.",
            "The _____ decision was based on what was feasible.",
            "The _____ method was more effective than the theoretical one.",
            "The _____ way of thinking solved many problems.",
            "The _____ approach avoided unnecessary complications.",
            "The _____ solution was simple and effective.",
            "The _____ attitude made her a good problem-solver.",
            "The _____ method got results quickly."
        ],
        "preclude": [
            "His injury _____ him from playing in the match.",
            "The bad weather might _____ outdoor activities.",
            "The rules _____ certain types of behaviour.",
            "The lack of funds might _____ the project.",
            "The conflict would _____ any chance of cooperation.",
            "The deadline might _____ further changes.",
            "The restrictions _____ certain actions.",
            "The circumstances might _____ success.",
            "The conditions would _____ participation.",
            "The limitations might _____ progress."
        ],
        "predator": [
            "The lion is a fierce _____ in the African savannah.",
            "The _____ hunted its prey with skill and patience.",
            "The _____ waited silently for the right moment to strike.",
            "The _____ was at the top of the food chain.",
            "The _____ moved stealthily through the undergrowth.",
            "The _____ was known for its hunting abilities.",
            "The _____ stalked its prey carefully.",
            "The _____ was feared by all smaller animals.",
            "The _____ was perfectly adapted for hunting.",
            "The _____ dominated its territory completely."
        ],
        "prestige": [
            "The university has great _____ worldwide.",
            "The _____ of the award made it highly sought after.",
            "The _____ of the position attracted many applicants.",
            "The _____ of the school was well-known.",
            "The _____ of winning the competition was significant.",
            "The _____ of the title meant a lot to him.",
            "The _____ of the institution was unquestioned.",
            "The _____ of the achievement was recognised by all.",
            "The _____ of the honour was deeply felt.",
            "The _____ of the role was evident to everyone."
        ],
        "pristine": [
            "The _____ beach had no litter at all.",
            "The _____ condition of the old book was remarkable.",
            "The _____ snow covered everything in white.",
            "The _____ state of the ancient artefact amazed archaeologists.",
            "The _____ quality of the water was perfect for swimming.",
            "The _____ appearance of the new building was impressive.",
            "The _____ condition of the vintage car was exceptional.",
            "The _____ environment was untouched by human activity.",
            "The _____ state of the forest was beautiful.",
            "The _____ quality of the air was refreshing."
        ],
        "proclaim": [
            "The town crier would _____ the news loudly.",
            "The king would _____ new laws to the people.",
            "The mayor will _____ the winner of the competition.",
            "The herald would _____ important announcements.",
            "The speaker will _____ the results to the audience.",
            "The leader will _____ the beginning of the celebration.",
            "The official will _____ the new regulations.",
            "The judge will _____ the verdict in court.",
            "The captain will _____ the ship's arrival.",
            "The announcer will _____ the start of the event."
        ],
        "profound": [
            "The book had a _____ effect on her thinking.",
            "The _____ silence showed everyone's respect.",
            "The _____ meaning of the poem was difficult to understand.",
            "The _____ impact of the discovery was significant.",
            "The _____ wisdom of the old teacher was appreciated.",
            "The _____ change transformed everything.",
            "The _____ effect of the experience stayed with her.",
            "The _____ understanding came after much study.",
            "The _____ nature of the problem required deep thought.",
            "The _____ influence shaped her entire life."
        ],
        "prologue": [
            "The _____ set the scene for the story.",
            "The _____ introduced the main characters.",
            "The _____ provided background information.",
            "The _____ explained what happened before the story began.",
            "The _____ gave context to the events that followed.",
            "The _____ prepared readers for what was to come.",
            "The _____ established the setting and time period.",
            "The _____ introduced the themes of the book.",
            "The _____ set the tone for the entire novel.",
            "The _____ gave readers important information."
        ],
        "propriety": [
            "She always behaved with perfect _____.",
            "The _____ of her actions was never questioned.",
            "The _____ of the behaviour was important in formal settings.",
            "The _____ of the decision was carefully considered.",
            "The _____ of her conduct impressed everyone.",
            "The sense of _____ guided her actions.",
            "The _____ of the occasion required formal dress.",
            "The _____ of the response was appropriate.",
            "The _____ of the behaviour was expected.",
            "The _____ of her manners was exemplary."
        ],
        "protract": [
            "The negotiations threatened to _____ the dispute.",
            "The delay would _____ the meeting unnecessarily.",
            "The complications might _____ the process.",
            "The disagreement would _____ the discussion.",
            "The problems might _____ the project timeline.",
            "The issues would _____ the resolution.",
            "The difficulties might _____ the completion date.",
            "The obstacles would _____ the journey.",
            "The complications might _____ the decision-making.",
            "The delays would _____ the wait."
        ],
        "prudence": [
            "She showed great _____ in her financial decisions.",
            "The _____ of the approach prevented problems.",
            "The _____ in planning avoided many difficulties.",
            "The _____ of the decision was wise.",
            "The _____ shown in the situation was admirable.",
            "The _____ of her actions prevented disaster.",
            "The _____ in handling the matter was evident.",
            "The _____ of the choice was clear.",
            "The _____ shown was characteristic of her careful nature.",
            "The _____ of the strategy ensured success."
        ],
        "pseudonym": [
            "The author wrote under a _____ to remain anonymous.",
            "The _____ allowed the writer to publish without revealing identity.",
            "The famous author used a _____ for her children's books.",
            "The _____ protected the writer's privacy.",
            "The author chose a _____ that sounded mysterious.",
            "The _____ was carefully selected to match the writing style.",
            "The writer's _____ became well-known over time.",
            "The _____ helped the author explore different genres.",
            "The _____ was used to separate different types of writing.",
            "The author's _____ was eventually revealed to the public."
        ],
        "punitive": [
            "The _____ measures were considered too harsh.",
            "The _____ action was taken to discourage bad behaviour.",
            "The _____ nature of the punishment was severe.",
            "The _____ measures were intended as a deterrent.",
            "The _____ action was meant to teach a lesson.",
            "The _____ nature of the response was criticised.",
            "The _____ measures were designed to prevent repetition.",
            "The _____ action was taken seriously.",
            "The _____ nature of the sanctions was debated.",
            "The _____ measures were enforced strictly."
        ],
        "quagmire": [
            "The soldiers got stuck in the _____.",
            "The _____ made progress impossible.",
            "The _____ trapped the vehicle completely.",
            "The _____ was deeper than anyone expected.",
            "The _____ slowed down the entire expedition.",
            "The _____ made walking very difficult.",
            "The _____ was impossible to cross without help.",
            "The _____ threatened to swallow everything.",
            "The _____ was a dangerous obstacle.",
            "The _____ made the journey treacherous."
        ],
        "querulous": [
            "The _____ child never stopped complaining.",
            "The _____ tone of voice was irritating.",
            "The _____ way she spoke annoyed everyone.",
            "The _____ complaints were constant and tiresome.",
            "The _____ manner made her difficult to be around.",
            "The _____ voice whined about everything.",
            "The _____ attitude made cooperation impossible.",
            "The _____ nature of the complaints was exhausting.",
            "The _____ way he questioned everything was annoying.",
            "The _____ behaviour made her very unpopular."
        ],
        "raconteur": [
            "The _____ entertained everyone with his stories.",
            "The _____ had a talent for storytelling.",
            "The _____ kept the audience captivated with tales.",
            "The _____ was known for his entertaining anecdotes.",
            "The _____ had a gift for making stories come alive.",
            "The _____ was popular at every gathering.",
            "The _____ could make any story interesting.",
            "The _____ had a way with words that enchanted listeners.",
            "The _____ was always the centre of attention.",
            "The _____ brought stories to life with vivid details."
        ],
        "rarity": [
            "The _____ of the gemstone made it very valuable.",
            "The _____ of the event made it special.",
            "The _____ of the find excited the archaeologists.",
            "The _____ of the opportunity was not lost on anyone.",
            "The _____ of the species made conservation important.",
            "The _____ of the occurrence was remarkable.",
            "The _____ of the book made it a collector's item.",
            "The _____ of the moment was appreciated by all.",
            "The _____ of the discovery was significant.",
            "The _____ of the experience made it memorable."
        ],
        "rationale": [
            "She explained the _____ behind her decision.",
            "The _____ for the change was clearly explained.",
            "The _____ behind the plan made sense.",
            "The _____ for the action was well thought out.",
            "The _____ behind the choice was logical.",
            "The _____ for the approach was sound.",
            "The _____ behind the strategy was explained carefully.",
            "The _____ for the decision was reasonable.",
            "The _____ behind the method was clear.",
            "The _____ for the policy was well documented."
        ],
        "ravenous": [
            "After the long hike, they were _____.",
            "The _____ appetite made him eat everything in sight.",
            "The _____ hunger was impossible to ignore.",
            "The _____ feeling made her eat quickly.",
            "The _____ appetite showed how hungry they were.",
            "The _____ hunger drove them to find food immediately.",
            "The _____ feeling made them eat more than usual.",
            "The _____ appetite was satisfied by the large meal.",
            "The _____ hunger was evident in their behaviour.",
            "The _____ feeling made them appreciate the food."
        ]
    }
    
    # Check if we have custom sentences for this word
    if word_lower in word_sentences:
        custom_sentences = word_sentences[word_lower]
        # Add example sentence first if available and different
        if example:
            blank_example = create_blank_sentence(example, word)
            if "_____" in blank_example and blank_example not in custom_sentences:
                sentences.append(blank_example)
        
        # Add custom sentences (skip if already added as example)
        for sent in custom_sentences:
            if len(sentences) >= 10:
                break
            if sent not in sentences:  # Avoid duplicates
                sentences.append(sent)
    else:
        # No custom sentences, use example if available
        if example:
            blank_example = create_blank_sentence(example, word)
            if "_____" in blank_example:
                sentences.append(blank_example)
    
    # Fill remaining slots with contextually appropriate sentences
    while len(sentences) < 10:
        if is_verb:
            new_sent = f"They had to _____ carefully to avoid problems."
        elif is_adjective:
            new_sent = f"The _____ appearance was noticeable to everyone."
        else:
            new_sent = f"The _____ was important to understand."
        
        if new_sent not in sentences:  # Avoid duplicates
            sentences.append(new_sent)
        else:
            # If duplicate, try a variation
            if is_verb:
                new_sent = f"She learned to _____ after much practice."
            elif is_adjective:
                new_sent = f"His _____ behaviour surprised everyone."
            else:
                new_sent = f"The _____ became clear after careful study."
            if new_sent not in sentences:
                sentences.append(new_sent)
            else:
                break  # Avoid infinite loop
    
    return sentences[:10]


def main():
    """Generate quiz sentences for Level 3 Batch 4"""
    input_file = Path(__file__).parent.parent / "data" / "level3_batch4.txt"
    output_file = Path(__file__).parent.parent / "data" / "level3_batch4.csv"
    
    sentences_generated = 0
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        
        writer = csv.writer(f_out)
        writer.writerow(['level', 'word', 'sentence'])
        
        for line_num, line in enumerate(f_in, 1):
            line = line.strip()
            if not line:
                continue
            
            # Parse: word|meaning|example|synonym|antonym
            parts = line.split('|')
            if len(parts) < 3:
                continue
            
            word = parts[0].strip()
            meaning = parts[1].strip() if len(parts) > 1 else ""
            example = parts[2].strip() if len(parts) > 2 else ""
            synonym = parts[3].strip() if len(parts) > 3 else ""
            antonym = parts[4].strip() if len(parts) > 4 else ""
            
            # Generate sentences
            sentences = generate_sentences_for_word(word, meaning, example, synonym, antonym)
            
            # Write to CSV
            for sentence in sentences:
                writer.writerow(['3', word.capitalize(), sentence])
                sentences_generated += 1
    
    print(f"Level 3 Batch 4 complete: {sentences_generated} sentences")


if __name__ == "__main__":
    main()
