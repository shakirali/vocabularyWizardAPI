#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Batch 4 words.
Creates contextually rich sentences with strong clues for 11+ vocabulary.
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
    patterns = [word, word_lower, word.capitalize()]
    
    # Add common word form variations
    if word_lower.endswith('e'):
        patterns.extend([
            word_lower + 'd',
            word_lower + 's',
            word_lower[:-1] + 'ing',
            word_lower[:-1] + 'ed'
        ])
    elif word_lower.endswith('y'):
        patterns.extend([
            word_lower[:-1] + 'ied',
            word_lower[:-1] + 'ies',
            word_lower[:-1] + 'ying'
        ])
    else:
        patterns.extend([
            word_lower + 'ed',
            word_lower + 's',
            word_lower + 'ing',
            word_lower + 'er'
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
        "brave", "friendly", "dark", "enthusiastic", "busy", "wicked", "unfriendly",
        "kind", "silly", "angry", "incompetent", "inactive", "whole", "furious"
    ]) or any(marker in meaning_lower for marker in [
        "having", "showing", "full of", "characterised by", "characterized by",
        "very", "extremely", "quite", "rather", "causing", "deserving"
    ])
    is_noun = not is_verb and not is_adjective
    
    # 1. Use example sentence if available
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate contextually rich sentences based on word meaning
    # Each word gets custom sentences that demonstrate its specific meaning
    
    word_sentences = {
        "gallant": [
            "The _____ knight charged fearlessly into battle to save the village.",
            "Her _____ act of rescuing the kitten from the tree impressed everyone.",
            "The soldier's _____ behaviour earned him a medal for bravery.",
            "He showed a _____ spirit by standing up to the bullies.",
            "The _____ prince risked his life to protect the kingdom.",
            "She made a _____ effort to help the elderly woman cross the busy road.",
            "His _____ rescue of the drowning child was truly heroic.",
            "The _____ firefighter rushed into the burning building without hesitation.",
            "They praised her _____ courage in facing the difficult challenge.",
            "The _____ warrior defended the castle gates against all attackers."
        ],
        "garbled": [
            "The _____ message was impossible to understand due to static interference.",
            "His speech became _____ after he spoke too quickly into the microphone.",
            "The telephone connection was so poor that her words came out completely _____.",
            "The _____ instructions confused everyone trying to assemble the furniture.",
            "She tried to read the _____ text but couldn't make sense of it.",
            "The radio signal was _____ and distorted by the storm.",
            "His explanation was so _____ that nobody understood what he meant.",
            "The _____ recording made it difficult to hear what was being said.",
            "The message became _____ when it was passed through too many people.",
            "The _____ handwriting was illegible and impossible to decipher."
        ],
        "gasket": [
            "The mechanic replaced the worn _____ in the car engine to stop the leak.",
            "A new _____ was needed to seal the pipe connection properly.",
            "The broken _____ caused oil to leak from the machinery.",
            "She tightened the _____ to prevent water from escaping.",
            "The rubber _____ created a watertight seal between the two surfaces.",
            "Without a proper _____, the engine would overheat quickly.",
            "The plumber installed a new _____ to fix the leaking joint.",
            "The _____ prevented air from escaping the pressurised container.",
            "They checked the _____ for any signs of wear or damage.",
            "The damaged _____ needed immediate replacement to avoid further problems."
        ],
        "genial": [
            "The _____ shopkeeper always greeted customers with a warm smile.",
            "Her _____ personality made her popular with everyone she met.",
            "The _____ host made sure all guests felt comfortable at the party.",
            "His _____ manner put the nervous children at ease immediately.",
            "The _____ teacher was always patient and encouraging with her pupils.",
            "She had a _____ nature that made people want to be around her.",
            "The _____ neighbour offered to help with gardening every weekend.",
            "His _____ welcome made the new family feel at home straight away.",
            "The _____ atmosphere in the café made it a pleasant place to visit.",
            "She responded with a _____ laugh that brightened everyone's day."
        ],
        "gloomy": [
            "The _____ weather matched her sad mood perfectly.",
            "The _____ room had dark curtains blocking out all sunlight.",
            "His _____ expression showed that he was feeling very down.",
            "The _____ forest path seemed mysterious and slightly frightening.",
            "She felt _____ after hearing the disappointing news.",
            "The _____ clouds overhead suggested rain was coming soon.",
            "The _____ atmosphere in the house made everyone feel depressed.",
            "His _____ outlook on life worried his friends and family.",
            "The _____ basement was dark and filled with shadows.",
            "The _____ day made everything seem dull and colourless."
        ],
        "glutton": [
            "He was such a _____ that he ate three helpings of dessert.",
            "The _____ devoured everything on the table without leaving any for others.",
            "She called him a _____ after he finished the entire cake by himself.",
            "The _____ couldn't resist eating all the biscuits in one sitting.",
            "His reputation as a _____ was well-known throughout the school.",
            "The _____ ate so much that he felt unwell afterwards.",
            "She scolded her brother for being a _____ at the buffet.",
            "The _____ finished everyone's leftovers without asking permission.",
            "His _____ behaviour at mealtimes embarrassed his family.",
            "The _____ never seemed satisfied no matter how much he ate."
        ],
        "gnarled": [
            "The _____ old oak tree had been standing for over three hundred years.",
            "His _____ hands showed the hard work he had done throughout his life.",
            "The _____ branches twisted and turned in every direction.",
            "She admired the _____ beauty of the ancient tree trunk.",
            "The _____ roots of the tree spread out across the forest floor.",
            "His _____ fingers struggled to grip the small button.",
            "The _____ appearance of the old tree made it look mysterious.",
            "The _____ bark was rough and covered in deep grooves.",
            "The _____ wood was difficult to carve because of its twisted grain.",
            "The _____ branches created interesting shadows on the ground."
        ],
        "goaded": [
            "He was _____ into losing his temper by constant teasing from classmates.",
            "The bullies _____ him into fighting by calling him names repeatedly.",
            "She felt _____ into making a hasty decision she later regretted.",
            "His friends _____ him into jumping into the cold water on a dare.",
            "The persistent questions _____ her into revealing the secret.",
            "He was _____ into action by their repeated challenges to his courage.",
            "The teasing _____ him into doing something he knew was wrong.",
            "She felt _____ into buying the expensive item by the pushy salesperson.",
            "The constant pressure _____ him into agreeing against his better judgement.",
            "His brother _____ him into staying up past bedtime by daring him."
        ],
        "grata": [
            "She became persona non _____ after betraying her friend's trust.",
            "The unwelcome guest was clearly persona non _____ at the family gathering.",
            "His rude behaviour made him persona non _____ among the other pupils.",
            "After the argument, he was persona non _____ in their social circle.",
            "The troublemaker was persona non _____ at school events.",
            "Her dishonesty made her persona non _____ with the group.",
            "The disruptive student became persona non _____ in the classroom.",
            "His negative attitude made him persona non _____ at team meetings.",
            "After breaking the rules, she was persona non _____ at the club.",
            "The rude customer was persona non _____ in the shop after that incident."
        ],
        "grieve": [
            "The family continued to _____ for their beloved grandmother.",
            "She needed time to _____ after losing her best friend.",
            "The whole community came together to _____ for the tragic loss.",
            "He found it difficult to _____ properly after the sudden death.",
            "The children were too young to fully understand how to _____.",
            "She allowed herself to _____ before trying to move forward.",
            "The memorial service helped everyone _____ together as a community.",
            "It's natural to _____ when someone important to you passes away.",
            "The support of friends helped her _____ more easily.",
            "They would _____ for many months before feeling better."
        ],
        "gung-ho": [
            "The _____ new employee volunteered for every task enthusiastically.",
            "Her _____ attitude made her stand out among the other candidates.",
            "The _____ team members were eager to start the project immediately.",
            "His _____ approach to learning impressed all his teachers.",
            "The _____ volunteers worked tirelessly throughout the entire day.",
            "She was so _____ about the school play that she memorised all the lines.",
            "The _____ pupils were first to raise their hands for every question.",
            "His _____ spirit inspired others to work harder too.",
            "The _____ attitude of the new members brought fresh energy to the group.",
            "She approached every challenge with a _____ determination to succeed."
        ],
        "hamper": [
            "The heavy rain began to _____ the rescue efforts significantly.",
            "The fallen tree would _____ traffic for several hours.",
            "Her injury would _____ her ability to compete in the race.",
            "The lack of supplies would _____ their progress on the project.",
            "Bad weather could _____ their plans for a picnic in the park.",
            "The broken equipment would _____ production at the factory.",
            "His absence would _____ the team's chances of winning.",
            "The confusing instructions would _____ their ability to complete the task.",
            "Limited resources would _____ the charity's ability to help everyone.",
            "The delay would _____ their journey to the airport."
        ],
        "harass": [
            "It is wrong to _____ anyone because of their differences.",
            "The bullies continued to _____ the new pupil every day.",
            "She reported the person who tried to _____ her online.",
            "The school has a zero-tolerance policy for anyone who tries to _____ others.",
            "He felt uncomfortable when older pupils would _____ him in the corridor.",
            "The teacher intervened when she saw someone trying to _____ a classmate.",
            "It's important to speak up if someone tries to _____ you.",
            "The persistent phone calls began to _____ the family.",
            "Nobody should have to put up with someone trying to _____ them.",
            "The school took action against those who tried to _____ others."
        ],
        "harbour": [
            "The ships sailed into the safe _____ before the storm arrived.",
            "She began to _____ doubts about whether the plan would work.",
            "The fishing boats returned to the _____ at sunset each evening.",
            "He tried not to _____ negative feelings towards his classmates.",
            "The small _____ provided shelter for boats during rough weather.",
            "She couldn't help but _____ resentment after the unfair treatment.",
            "The deep _____ could accommodate large cargo ships easily.",
            "It's unhealthy to _____ grudges against people for too long.",
            "The natural _____ was protected by high cliffs on both sides.",
            "The sailors were relieved to reach the safety of the _____."
        ],
        "hardy": [
            "The _____ plants survived the harsh winter frost without any protection.",
            "The _____ explorer endured extreme conditions during his journey.",
            "These _____ flowers can grow in almost any type of soil.",
            "The _____ mountaineer climbed peaks that others found impossible.",
            "The _____ breed of sheep thrived in the cold mountain climate.",
            "She was _____ enough to walk to school even in heavy snow.",
            "The _____ tree withstood the strong winds without breaking.",
            "These _____ vegetables can be grown even in poor conditions.",
            "The _____ athlete trained in all weather conditions.",
            "The _____ survivors managed to endure the difficult circumstances."
        ],
        "haughty": [
            "The _____ princess refused to speak to anyone she considered beneath her.",
            "His _____ attitude made him unpopular with the other pupils.",
            "The _____ manner in which she spoke offended many people.",
            "She looked down on others with a _____ expression on her face.",
            "The _____ nobleman treated servants as if they were invisible.",
            "His _____ behaviour showed he thought he was better than everyone else.",
            "The _____ way she dismissed their ideas angered the team.",
            "She walked past with a _____ air, ignoring everyone around her.",
            "The _____ student refused to work with anyone she considered less intelligent.",
            "His _____ comments about their background were completely unacceptable."
        ],
        "hearth": [
            "The family gathered around the warm _____ on cold winter evenings.",
            "The crackling fire in the _____ filled the room with cosy warmth.",
            "The cat curled up near the _____ to stay warm.",
            "The old _____ had been used by generations of the same family.",
            "She placed another log on the fire in the _____.",
            "The warm glow from the _____ lit up the entire room.",
            "The children sat by the _____ listening to stories from their grandmother.",
            "The stone _____ was the centrepiece of the old cottage.",
            "The fire in the _____ provided the only light during the power cut.",
            "The family's Christmas stockings hung above the _____."
        ],
        "hectic": [
            "The _____ morning rush left everyone feeling exhausted.",
            "The _____ schedule meant she had no time for lunch.",
            "The _____ pace of city life was overwhelming for the country girl.",
            "The _____ day at school included three tests and a sports match.",
            "The _____ preparations for the party kept everyone busy all afternoon.",
            "The _____ atmosphere in the kitchen made cooking stressful.",
            "The _____ rush hour traffic delayed their journey significantly.",
            "The _____ week before the exam was filled with revision sessions.",
            "The _____ activity in the playground during break time was chaotic.",
            "The _____ period before the holidays was always the busiest time."
        ],
        "heeding": [
            "Not _____ the warning signs, she continued walking into danger.",
            "By _____ her teacher's advice, she improved her grades significantly.",
            "The driver avoided an accident by _____ the traffic signals.",
            "She got into trouble for not _____ her parents' instructions.",
            "By _____ the safety guidelines, they prevented any accidents.",
            "The pupils were praised for _____ the school rules properly.",
            "Not _____ the weather forecast, they got caught in heavy rain.",
            "By _____ the expert's recommendations, the project succeeded.",
            "She avoided mistakes by carefully _____ the instructions.",
            "The team succeeded by _____ their coach's strategic advice."
        ],
        "heinous": [
            "The _____ crime shocked the entire community deeply.",
            "The _____ act of cruelty to animals was reported to the authorities.",
            "The _____ nature of the offence meant it would be severely punished.",
            "Everyone was horrified by the _____ behaviour of the criminals.",
            "The _____ deed was something that could never be forgiven.",
            "The _____ attack on innocent people outraged the whole nation.",
            "The _____ crime was considered one of the worst in recent history.",
            "The _____ act violated every principle of decency and respect.",
            "The _____ nature of the offence meant it would be remembered for years.",
            "The _____ crime was so terrible that it made headlines everywhere."
        ],
        "helix": [
            "DNA is arranged in a double _____ structure that looks like a twisted ladder.",
            "The spiral staircase formed a perfect _____ shape as it wound upwards.",
            "The scientist studied the _____ pattern found in the molecule.",
            "The _____ structure of the DNA was visible under the microscope.",
            "The twisted rope formed a loose _____ as it hung from the ceiling.",
            "The _____ shape of the spring allowed it to compress and expand.",
            "The DNA's double _____ contains all the genetic information.",
            "The staircase's _____ design was both beautiful and functional.",
            "The _____ pattern was repeated throughout the crystal structure.",
            "The twisted wire formed a tight _____ around the post."
        ],
        "heroic": [
            "The _____ firefighter rescued the family from the burning building.",
            "Her _____ act of saving the drowning child earned her a medal.",
            "The _____ effort of the rescue team saved many lives.",
            "His _____ behaviour during the emergency inspired everyone.",
            "The _____ sacrifice of the soldier would never be forgotten.",
            "She showed _____ courage when facing the dangerous situation.",
            "The _____ deed was celebrated throughout the entire community.",
            "His _____ actions during the crisis prevented a greater disaster.",
            "The _____ rescue mission was successful despite the risks.",
            "She was praised for her _____ response to the emergency."
        ],
        "hiatus": [
            "The band took a _____ from touring to spend time with their families.",
            "After the long _____, she returned to school feeling refreshed.",
            "The _____ in their friendship lasted for several months.",
            "The television series went on _____ between seasons.",
            "The _____ in rainfall caused the river to dry up completely.",
            "During the summer _____, the pupils forgot some of what they had learned.",
            "The _____ in communication made it difficult to coordinate plans.",
            "After a brief _____, the team resumed their training schedule.",
            "The _____ in the conversation made everyone feel uncomfortable.",
            "The school took a _____ from normal lessons for the special event."
        ],
        "hinder": [
            "The heavy traffic would _____ their journey to school significantly.",
            "The bad weather began to _____ their progress on the building project.",
            "Her injury would _____ her ability to participate in the race.",
            "The lack of resources would _____ their efforts to help others.",
            "The confusing instructions would _____ their ability to complete the task.",
            "The broken equipment would _____ production at the factory.",
            "His absence would _____ the team's chances of winning the match.",
            "The delay would _____ their plans for the weekend trip.",
            "Limited funding would _____ the charity's ability to expand.",
            "The obstacles would _____ their progress towards the goal."
        ],
        "hostile": [
            "The _____ crowd made the visitors feel unwelcome and uncomfortable.",
            "The _____ environment made it difficult for new pupils to settle in.",
            "His _____ attitude towards newcomers was completely unacceptable.",
            "The _____ reaction to their suggestion surprised everyone.",
            "The _____ atmosphere in the room made everyone feel tense.",
            "She faced a _____ reception when she tried to join the group.",
            "The _____ behaviour of the other team shocked the spectators.",
            "The _____ comments made during the debate were inappropriate.",
            "The _____ environment made it impossible to have a productive discussion.",
            "The _____ response to their idea discouraged them from speaking up again."
        ],
        "hubris": [
            "His _____ led to his eventual downfall after he ignored all warnings.",
            "The leader's _____ caused him to make disastrous decisions.",
            "Her _____ prevented her from listening to good advice from others.",
            "The athlete's _____ made him underestimate his opponents completely.",
            "His _____ blinded him to the risks of his dangerous plan.",
            "The general's _____ led to a catastrophic defeat in battle.",
            "Her _____ made her refuse help even when she desperately needed it.",
            "The politician's _____ caused him to lose the support of voters.",
            "His _____ prevented him from seeing his own weaknesses.",
            "The student's _____ made him ignore the teacher's helpful suggestions."
        ],
        "humane": [
            "The _____ treatment of animals is very important to responsible pet owners.",
            "She believed in _____ methods of teaching that encouraged rather than punished.",
            "The _____ approach to discipline focused on understanding and guidance.",
            "The _____ way they cared for the elderly showed great compassion.",
            "The _____ treatment of prisoners was a priority for the new governor.",
            "She advocated for more _____ conditions in the animal shelter.",
            "The _____ response to the crisis saved many lives.",
            "The _____ way they handled the difficult situation impressed everyone.",
            "The _____ care provided to patients made the hospital highly respected.",
            "The _____ treatment of all living creatures was their core principle."
        ],
        "hybrid": [
            "The _____ car uses both petrol and electricity to reduce emissions.",
            "The _____ plant combined features from two different species.",
            "The _____ approach blended traditional and modern teaching methods.",
            "The _____ animal was a cross between a lion and a tiger.",
            "The _____ vehicle could switch between fuel sources automatically.",
            "The _____ solution combined the best ideas from both proposals.",
            "The _____ flower had characteristics of both parent plants.",
            "The _____ system used elements from different technologies.",
            "The _____ design merged classic and contemporary styles beautifully.",
            "The _____ breed of dog combined traits from two popular breeds."
        ],
        "idiom": [
            "Raining cats and dogs is a common English _____ meaning heavy rain.",
            "She used the _____ 'break a leg' to wish him good luck.",
            "The teacher explained that an _____ has a figurative meaning.",
            "The _____ 'once in a blue moon' means something very rare.",
            "He struggled to understand the _____ because he took it literally.",
            "The _____ 'piece of cake' means something is very easy.",
            "She loved learning new _____ expressions in English class.",
            "The _____ 'cost an arm and a leg' means something is very expensive.",
            "The _____ 'hit the nail on the head' means to be exactly right.",
            "Understanding _____ helps you understand English culture better."
        ],
        "immerse": [
            "He liked to _____ himself in books during the school holidays.",
            "She would _____ herself completely in her art projects for hours.",
            "The best way to learn a language is to _____ yourself in it daily.",
            "She decided to _____ herself in studying for the important exam.",
            "The warm bath allowed her to _____ herself in relaxation.",
            "He would _____ himself in music, listening for hours on end.",
            "The pupils were encouraged to _____ themselves in the story.",
            "She would _____ herself in nature by spending time in the garden.",
            "The best way to understand a culture is to _____ yourself in it.",
            "He would _____ himself in his hobby, forgetting about everything else."
        ],
        "impair": [
            "Loud music can _____ your hearing if you listen for too long.",
            "The injury would _____ his ability to play football for several weeks.",
            "Lack of sleep can _____ your ability to concentrate in class.",
            "The fog began to _____ visibility on the roads significantly.",
            "The damage would _____ the machine's performance considerably.",
            "Poor lighting can _____ your ability to read small print.",
            "The medication might _____ your reaction time temporarily.",
            "The noise would _____ their ability to hear the instructions.",
            "The injury would _____ her mobility for the next few months.",
            "The interference began to _____ the radio signal quality."
        ],
        "impede": [
            "The fallen tree would _____ traffic for several hours.",
            "The bad weather began to _____ their progress on the journey.",
            "The obstacles would _____ their ability to reach the finish line.",
            "The confusion would _____ their efforts to complete the project.",
            "The delay would _____ their plans for the weekend trip.",
            "The restrictions would _____ their freedom to explore.",
            "The problems would _____ the smooth running of the event.",
            "The complications would _____ their progress significantly.",
            "The barriers would _____ access to the building site.",
            "The difficulties would _____ their ability to succeed."
        ],
        "impel": [
            "Her curiosity _____ her to investigate the mysterious noise.",
            "The urgent situation _____ them to act quickly without delay.",
            "His sense of duty _____ him to help those in need.",
            "The strong desire _____ her to pursue her dreams.",
            "The emergency _____ everyone to evacuate the building immediately.",
            "Her passion for justice _____ her to speak out against unfairness.",
            "The need to succeed _____ him to work harder than ever.",
            "The crisis _____ the government to take immediate action.",
            "Her love of learning _____ her to read constantly.",
            "The opportunity _____ him to take a chance he wouldn't normally take."
        ],
        "impose": [
            "The government decided to _____ new taxes on luxury items.",
            "The school had to _____ stricter rules after the incident.",
            "The teacher didn't want to _____ her views on the pupils.",
            "The judge would _____ a fine for breaking the law.",
            "The parents had to _____ limits on screen time.",
            "The council decided to _____ restrictions on parking.",
            "The manager would _____ penalties for arriving late.",
            "The school would _____ consequences for breaking the rules.",
            "The government had to _____ measures to protect public health.",
            "The teacher would _____ deadlines to ensure work was completed."
        ],
        "inane": [
            "His _____ comments contributed nothing useful to the discussion.",
            "The _____ television programme was a complete waste of time.",
            "She grew tired of listening to his _____ chatter all day.",
            "The _____ questions showed he hadn't been paying attention.",
            "The _____ conversation bored everyone who had to listen.",
            "His _____ jokes weren't funny and annoyed everyone.",
            "The _____ remarks were completely irrelevant to the topic.",
            "She found his _____ observations to be pointless and silly.",
            "The _____ programme had no educational value whatsoever.",
            "His _____ suggestions were immediately dismissed by the group."
        ],
        "incense": [
            "The unfair decision _____ all the players who felt cheated.",
            "The rude comment _____ her so much that she walked away.",
            "The broken promise _____ him more than he expected.",
            "The disrespectful behaviour _____ the teacher greatly.",
            "The false accusation _____ the innocent person completely.",
            "The unfair treatment _____ everyone who witnessed it.",
            "The thoughtless remark _____ her family members.",
            "The dishonest action _____ those who discovered the truth.",
            "The ungrateful attitude _____ the person who had helped them.",
            "The cruel joke _____ the victim and all their friends."
        ],
        "incite": [
            "It is illegal to _____ violence against others in any situation.",
            "The speaker tried to _____ the crowd to protest peacefully.",
            "His words were designed to _____ anger among the listeners.",
            "The inflammatory comments could _____ trouble at the event.",
            "She refused to _____ others to break the school rules.",
            "The provocative speech tried to _____ rebellion among the people.",
            "His actions could _____ conflict between the two groups.",
            "The misleading information could _____ panic among the public.",
            "She warned him not to _____ others to behave badly.",
            "The irresponsible comments could _____ dangerous behaviour."
        ],
        "incline": [
            "The hill began to _____ steeply towards the top.",
            "The road would _____ upwards for the next two miles.",
            "She had a natural _____ towards helping others in need.",
            "The path would _____ gradually through the forest.",
            "His personality showed an _____ towards being optimistic.",
            "The slope would _____ at a sharp angle near the summit.",
            "She had an _____ to believe the best about people.",
            "The track would _____ steadily as they climbed higher.",
            "His character showed an _____ towards being generous.",
            "The surface would _____ slightly, making it difficult to stand."
        ],
        "induce": [
            "The warm weather _____ everyone to go outside and play.",
            "The persuasive argument _____ her to change her mind.",
            "The medicine would _____ sleep within thirty minutes.",
            "The beautiful music _____ feelings of peace and calm.",
            "The promise of reward _____ him to work harder.",
            "The relaxing atmosphere _____ a sense of tranquillity.",
            "The exciting story _____ her to read until late at night.",
            "The delicious smell _____ everyone's appetite immediately.",
            "The encouraging words _____ him to try again after failing.",
            "The peaceful setting _____ a feeling of contentment."
        ],
        "indulge": [
            "She decided to _____ in a piece of chocolate cake for dessert.",
            "He would _____ his love of reading by visiting the library daily.",
            "The parents decided to _____ their children with a special treat.",
            "She would _____ herself by buying a new book every week.",
            "He would _____ his hobby of collecting stamps on weekends.",
            "The grandparents loved to _____ their grandchildren with presents.",
            "She would _____ her passion for art by painting every evening.",
            "He decided to _____ in a long hot bath after the busy day.",
            "The teacher would _____ the pupils with extra break time.",
            "She would _____ herself with a day off from all responsibilities."
        ],
        "inept": [
            "The _____ goalkeeper let in five goals during the match.",
            "His _____ attempts at cooking resulted in burnt food.",
            "The _____ handling of the situation made things worse.",
            "She was completely _____ at playing the piano despite practising.",
            "The _____ worker caused more problems than he solved.",
            "His _____ management of the project led to its failure.",
            "The _____ teacher couldn't control the class effectively.",
            "She felt _____ when trying to fix the broken computer.",
            "The _____ response to the emergency endangered everyone.",
            "His _____ performance cost the team the championship."
        ],
        "inert": [
            "The _____ gas does not react with other chemicals easily.",
            "The _____ object remained motionless on the table.",
            "The _____ substance showed no signs of activity.",
            "The _____ material was completely unresponsive to heat.",
            "The _____ body lay still without any movement.",
            "The _____ compound remained stable under normal conditions.",
            "The _____ state of the machine meant it wasn't working.",
            "The _____ matter showed no chemical reactions.",
            "The _____ position of the statue made it seem lifeless.",
            "The _____ nature of the material made it safe to handle."
        ],
        "infer": [
            "From the clues, we can _____ who committed the crime.",
            "She could _____ from his expression that he was upset.",
            "The detective tried to _____ what happened from the evidence.",
            "From the context, we can _____ the meaning of the word.",
            "She could _____ from the silence that something was wrong.",
            "The scientist tried to _____ the answer from the data.",
            "From her behaviour, we can _____ that she was nervous.",
            "The teacher helped pupils _____ meaning from the text.",
            "She could _____ from the clues that it was a surprise party.",
            "From the results, we can _____ that the experiment worked."
        ],
        "infuse": [
            "The tea was _____ with the flavour of fresh mint leaves.",
            "The teacher tried to _____ confidence into her nervous pupils.",
            "The chef would _____ the oil with herbs for extra flavour.",
            "The speech tried to _____ hope into the discouraged audience.",
            "The warm sunlight seemed to _____ the room with golden light.",
            "The mentor tried to _____ enthusiasm into the new team members.",
            "The artist would _____ her paintings with emotion and feeling.",
            "The leader tried to _____ courage into his worried followers.",
            "The music seemed to _____ the atmosphere with energy.",
            "The teacher tried to _____ a love of learning into her pupils."
        ],
        "inhale": [
            "She _____ the fresh mountain air deeply into her lungs.",
            "The doctor asked him to _____ slowly and then exhale.",
            "She would _____ the sweet scent of flowers in the garden.",
            "The swimmer had to _____ quickly before diving underwater.",
            "She _____ the delicious smell of freshly baked bread.",
            "The yoga instructor told them to _____ through their noses.",
            "She would _____ the calming scent of lavender before bed.",
            "The runner had to _____ deeply to get enough oxygen.",
            "She _____ the invigorating sea air during her walk.",
            "The firefighter had to be careful not to _____ the smoke."
        ],
        "intact": [
            "Remarkably, the ancient vase remained _____ despite the earthquake.",
            "The old building stayed _____ even after the strong winds.",
            "The package arrived _____ with nothing broken or damaged.",
            "The fragile egg remained _____ after falling from the table.",
            "The historical document was preserved _____ in the museum.",
            "The toy survived _____ even after being dropped many times.",
            "The ancient ruins remained _____ for thousands of years.",
            "The delicate flower stayed _____ despite the heavy rain.",
            "The old photograph remained _____ in its frame for decades.",
            "The fragile structure stayed _____ against all expectations."
        ],
        "irate": [
            "The _____ customer demanded to see the manager immediately.",
            "His _____ response showed he was extremely angry about the mistake.",
            "The _____ parent complained about the unfair treatment.",
            "She became _____ when she discovered what had happened.",
            "The _____ teacher sent the disruptive pupil to the headteacher.",
            "His _____ reaction surprised everyone who knew his calm nature.",
            "The _____ driver honked his horn repeatedly at the traffic.",
            "She was _____ about the broken promise and refused to listen.",
            "The _____ customer's complaints were heard throughout the shop.",
            "His _____ behaviour made everyone around him feel uncomfortable."
        ],
        "jabber": [
            "The excited children began to _____ all at once about their day.",
            "She would _____ on the phone for hours with her best friend.",
            "The nervous speaker began to _____ when asked a difficult question.",
            "The monkeys would _____ loudly in the trees above them.",
            "She would _____ excitedly about her favourite television programme.",
            "The pupils would _____ during break time about their weekend plans.",
            "She began to _____ when she saw something exciting happen.",
            "The children would _____ simultaneously, making it hard to understand.",
            "She would _____ quickly when telling an exciting story.",
            "The excited crowd began to _____ as they waited for the announcement."
        ],
        "jargon": [
            "Medical _____ can be confusing for patients who aren't doctors.",
            "The technical _____ made the instructions impossible to understand.",
            "She struggled with the legal _____ in the contract.",
            "The computer _____ confused everyone who wasn't a programmer.",
            "The scientific _____ required a dictionary to understand properly.",
            "She tried to avoid using _____ when explaining things to children.",
            "The business _____ made the presentation difficult to follow.",
            "The educational _____ was unfamiliar to parents at the meeting.",
            "She simplified the technical _____ so everyone could understand.",
            "The specialist _____ was only understood by experts in that field."
        ],
        "jewel": [
            "The diamond was a beautiful _____ in her engagement ring.",
            "She was the _____ of her grandmother's eye, meaning she was treasured.",
            "The rare _____ was worth more than the entire collection.",
            "The museum displayed a priceless _____ from ancient times.",
            "She wore a precious _____ that had been in her family for generations.",
            "The crown was decorated with many valuable _____.",
            "The antique _____ was carefully protected in a secure display case.",
            "She found a hidden _____ in her great-grandmother's jewellery box.",
            "The royal _____ was kept under heavy security at all times.",
            "The beautiful _____ sparkled brilliantly in the sunlight."
        ]
    }
    
    # Get custom sentences for this word
    if word_lower in word_sentences:
        custom_sentences = word_sentences[word_lower]
        # Add custom sentences, ensuring we have exactly 10
        for sent in custom_sentences:
            if len(sentences) < 10:
                # Replace the word with blank
                blank_sent = create_blank_sentence(sent, word)
                if "_____" in blank_sent and blank_sent not in sentences:
                    sentences.append(blank_sent)
            else:
                break
    
    # If we still don't have 10 sentences, generate more based on word type
    while len(sentences) < 10:
        if is_verb:
            # Generate verb-specific sentences
            verb_sentences = [
                f"They had to _____ the situation before it got worse.",
                f"She decided to _____ the problem quickly and efficiently.",
                f"He tried to _____ what was happening, but it was difficult.",
                f"We need to _____ this matter carefully and thoughtfully.",
                f"You should _____ before making any important decisions.",
            ]
            for sent in verb_sentences:
                blank_sent = create_blank_sentence(sent, word)
                if "_____" in blank_sent and blank_sent not in sentences:
                    sentences.append(blank_sent)
                    break
        elif is_adjective:
            # Generate adjective-specific sentences
            adj_sentences = [
                f"The situation was very _____ and quite concerning to everyone.",
                f"She showed a _____ attitude that impressed her teachers.",
                f"His behaviour was quite _____ and rather unexpected.",
                f"It was a _____ experience that everyone remembered fondly.",
                f"The _____ nature of the event surprised us all greatly.",
            ]
            for sent in adj_sentences:
                blank_sent = create_blank_sentence(sent, word)
                if "_____" in blank_sent and blank_sent not in sentences:
                    sentences.append(blank_sent)
                    break
        else:  # noun
            # Generate noun-specific sentences
            noun_sentences = [
                f"The _____ was clear to everyone present at the meeting.",
                f"She understood the _____ of the situation immediately.",
                f"His _____ surprised those around him greatly.",
                f"The _____ became evident very quickly to all observers.",
                f"Everyone noticed the _____ in the way he spoke.",
            ]
            for sent in noun_sentences:
                blank_sent = create_blank_sentence(sent, word)
                if "_____" in blank_sent and blank_sent not in sentences:
                    sentences.append(blank_sent)
                    break
    
    return sentences[:10]


def main():
    """Generate quiz sentences for all words in batch4_words.txt"""
    batch_file = Path(__file__).parent.parent / "data" / "batch4_words.txt"
    output_file = Path(__file__).parent.parent / "data" / "quiz_sentences_batch4.csv"
    
    # Read batch file
    words_data = []
    with open(batch_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) >= 5:
                word = parts[0].strip()
                meaning = parts[1].strip()
                example = parts[2].strip()
                synonym = parts[3].strip()
                antonym = parts[4].strip()
                words_data.append({
                    'word': word,
                    'meaning': meaning,
                    'example': example,
                    'synonym': synonym,
                    'antonym': antonym
                })
    
    # Generate sentences for each word
    all_sentences = []
    for word_data in words_data:
        word = word_data['word']
        meaning = word_data['meaning']
        example = word_data['example']
        synonym = word_data['synonym']
        antonym = word_data['antonym']
        
        sentences = generate_sentences_for_word(word, meaning, example, synonym, antonym)
        
        for sentence in sentences:
            all_sentences.append({
                'level': '1',
                'word': word,
                'sentence': sentence
            })
    
    # Write to CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['level', 'word', 'sentence'])
        writer.writeheader()
        writer.writerows(all_sentences)
    
    print(f"Batch 4 complete: {len(all_sentences)} sentences generated for {len(words_data)} words")


if __name__ == "__main__":
    main()
