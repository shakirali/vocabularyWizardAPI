#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 3 Batch 5 vocabulary.
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
        "feeling", "arousing", "suggesting", "intending", "evoking",
        "capable of", "perceptible by", "the quality of", "the state of",
        "the practice of", "the action of", "the branch of", "a person who",
        "a group of", "a piece of", "a cancellation of", "a final"
    ])
    is_noun = not is_verb and not is_adjective
    
    # Use the example sentence if available
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate word-specific sentences
    word_sentences = {
        "regretful": [
            "He felt _____ after realising he had hurt his friend's feelings.",
            "The _____ expression on her face showed she wished she hadn't said those words.",
            "She was _____ about missing her best friend's birthday party.",
            "His _____ apology was sincere and heartfelt.",
            "The _____ look in his eyes revealed his deep sorrow.",
            "She felt _____ for not studying harder before the important exam.",
            "His _____ tone suggested he knew he had made a mistake.",
            "The _____ student wished she had listened to her teacher's advice.",
            "He was _____ that he hadn't thanked his grandmother for the gift.",
            "Her _____ attitude showed she understood the consequences of her actions."
        ],
        "reiterate": [
            "Let me _____ the main points so everyone understands clearly.",
            "The teacher had to _____ the instructions because some students weren't listening.",
            "She felt the need to _____ her position on the matter.",
            "The speaker will _____ his key arguments in the conclusion.",
            "I must _____ that this is a very important rule.",
            "The coach had to _____ the game plan before the final match.",
            "She decided to _____ her request one more time.",
            "The manager will _____ the company's policy at the meeting.",
            "He had to _____ his point because nobody seemed to understand.",
            "The presenter will _____ the main findings at the end of the talk."
        ],
        "relegate": [
            "The team will be _____ to a lower division if they lose this match.",
            "The manager decided to _____ the old files to the storage room.",
            "They had to _____ the less important tasks to next week.",
            "The company chose to _____ the project to a junior team.",
            "She didn't want to _____ her dreams to the back of her mind.",
            "The coach threatened to _____ him to the bench if he didn't improve.",
            "They had to _____ the broken furniture to the garage.",
            "The school decided to _____ the outdated books to storage.",
            "He was _____ to a less important role in the organisation.",
            "The committee voted to _____ the proposal to a later meeting."
        ],
        "remnants": [
            "Only the _____ of the ancient castle remained after the fire.",
            "The _____ of the meal were carefully wrapped and saved for later.",
            "Archaeologists found _____ of pottery from the ancient civilisation.",
            "The _____ of the storm were visible in the damaged trees.",
            "She collected the _____ of fabric to make a patchwork quilt.",
            "The _____ of the old wall could still be seen in the garden.",
            "Only small _____ of the original painting survived the fire.",
            "The _____ of the party were scattered across the room.",
            "They discovered _____ of an old settlement in the field.",
            "The _____ of the broken vase were carefully gathered up."
        ],
        "renegade": [
            "The _____ soldier abandoned his unit and joined the enemy.",
            "The _____ politician broke away from his party's policies.",
            "She was considered a _____ for refusing to follow the school's strict rules.",
            "The _____ scientist challenged the accepted theories of his time.",
            "The _____ member of the group caused trouble wherever he went.",
            "The _____ artist created works that defied all traditional styles.",
            "He was labelled a _____ for his unconventional methods.",
            "The _____ explorer ventured into forbidden territory.",
            "The _____ student refused to conform to the school's expectations.",
            "The _____ warrior fought against his own people."
        ],
        "renounce": [
            "She decided to _____ her claim to the family inheritance.",
            "The prince had to _____ his right to the throne.",
            "He chose to _____ his citizenship and move to another country.",
            "She will _____ her membership in the club if they don't change their rules.",
            "The athlete had to _____ his title after the scandal.",
            "He decided to _____ his old ways and start fresh.",
            "She will _____ her support for the project if it continues this way.",
            "The politician was forced to _____ his previous statements.",
            "He chose to _____ violence and pursue peace instead.",
            "She will _____ her position if the situation doesn't improve."
        ],
        "renowned": [
            "The _____ author's books were read by millions worldwide.",
            "The _____ scientist won the Nobel Prize for her discoveries.",
            "The _____ chef's restaurant was booked months in advance.",
            "The _____ artist's paintings were displayed in galleries across the world.",
            "The _____ musician performed to sold-out audiences.",
            "The _____ explorer was famous for his daring adventures.",
            "The _____ doctor was known for saving countless lives.",
            "The _____ teacher inspired generations of students.",
            "The _____ architect designed some of the world's most beautiful buildings.",
            "The _____ actor received standing ovations wherever he performed."
        ],
        "repelled": [
            "She was _____ by the foul smell coming from the rubbish bin.",
            "The soldiers were _____ by the enemy's fierce attack.",
            "He was _____ by the sight of the decaying food.",
            "The magnet _____ the other magnet when they were turned the wrong way.",
            "She was _____ by his cruel and unkind behaviour.",
            "The strong smell _____ all the insects from the area.",
            "He was _____ by the thought of eating insects.",
            "The repellent spray _____ the mosquitoes effectively.",
            "She was _____ by the idea of cheating on the exam.",
            "The negative charges _____ each other when brought close together."
        ],
        "reprieve": [
            "The prisoner received a last-minute _____ from the governor.",
            "The rain provided a welcome _____ from the scorching heat.",
            "The deadline extension gave her a brief _____ from the pressure.",
            "The holiday was a much-needed _____ from her busy schedule.",
            "The judge granted a _____ so new evidence could be examined.",
            "The weekend offered a temporary _____ from schoolwork.",
            "The cancellation of the test was an unexpected _____ for the students.",
            "The break in the storm provided a brief _____ before it continued.",
            "The delay gave them a _____ to finish their preparations.",
            "The pause in the argument offered a brief _____ from the tension."
        ],
        "reproach": [
            "Her look of _____ made him realise he had done something wrong.",
            "He felt the weight of her silent _____ after breaking his promise.",
            "The teacher's tone was full of _____ when she spoke about the cheating.",
            "She couldn't bear the _____ in her mother's eyes.",
            "His actions brought _____ upon his entire family.",
            "The _____ in her voice was clear when she discovered the mess.",
            "He faced the _____ of his friends after letting them down.",
            "The _____ from his coach made him determined to improve.",
            "She felt deep _____ for not helping when she could have.",
            "The _____ in the letter made him reconsider his decision."
        ],
        "repudiate": [
            "She had to _____ the false rumours that were spreading about her.",
            "The politician was forced to _____ his earlier statements.",
            "He chose to _____ the contract because it was unfair.",
            "The company will _____ any claims that their product is unsafe.",
            "She decided to _____ the inheritance and give it to charity.",
            "The scientist had to _____ the flawed research findings.",
            "He will _____ any connection to the criminal organisation.",
            "The government was quick to _____ the false accusations.",
            "She chose to _____ her family's traditional beliefs.",
            "The organisation will _____ any member who breaks the rules."
        ],
        "resigned": [
            "She was _____ to the fact that she would have to repeat the year.",
            "He felt _____ about the situation and stopped trying to change it.",
            "The _____ expression on his face showed he had given up hope.",
            "She was _____ to waiting in the long queue.",
            "His _____ attitude suggested he had accepted his fate.",
            "The _____ look in her eyes showed she had stopped fighting.",
            "He was _____ to the idea that things wouldn't get better.",
            "She felt _____ about the outcome and prepared for the worst.",
            "The _____ tone in his voice revealed his acceptance.",
            "He was _____ to the fact that he couldn't change what had happened."
        ],
        "resonates": [
            "The music _____ throughout the entire concert hall.",
            "Her powerful speech _____ with everyone in the audience.",
            "The bell's sound _____ across the quiet valley.",
            "The message _____ deeply with people of all ages.",
            "The sound of the drum _____ through the building.",
            "His words _____ with her own experiences.",
            "The theme of the story _____ with young readers.",
            "The vibration _____ through the entire structure.",
            "The idea _____ strongly with the committee members.",
            "The sound _____ beautifully in the cathedral."
        ],
        "restraint": [
            "He showed great _____ by not responding to the insult.",
            "The police used _____ when dealing with the peaceful protest.",
            "She exercised _____ in not eating all the sweets at once.",
            "The dog showed remarkable _____ despite the tempting treats.",
            "He demonstrated _____ by waiting his turn patiently.",
            "The _____ of the rope prevented the boat from drifting away.",
            "She showed admirable _____ in difficult circumstances.",
            "The _____ of the seatbelt saved his life in the crash.",
            "He used _____ to control his anger during the argument.",
            "The _____ of the rules kept everyone safe."
        ],
        "retiring": [
            "The _____ student preferred to work alone rather than in groups.",
            "Her _____ nature made it difficult for her to make friends.",
            "The _____ teacher avoided the staff room during breaks.",
            "His _____ personality meant he rarely spoke in class.",
            "The _____ child sat quietly in the corner reading.",
            "She was too _____ to join the school play.",
            "The _____ librarian preferred the quiet of the bookshelves.",
            "His _____ manner made him seem unfriendly, though he wasn't.",
            "The _____ student excelled in independent projects.",
            "She had a _____ disposition that made her seem aloof."
        ],
        "retrieve": [
            "The dog managed to _____ the ball from the deep water.",
            "She had to _____ her forgotten homework from her locker.",
            "The diver tried to _____ the lost treasure from the shipwreck.",
            "He needed to _____ the important documents from the safe.",
            "The computer can _____ information quickly from its memory.",
            "She had to _____ her umbrella from the lost property office.",
            "The rescue team worked to _____ the trapped miners.",
            "He managed to _____ his lost phone from the taxi.",
            "The system can _____ deleted files if needed.",
            "She had to _____ her bicycle from the repair shop."
        ],
        "rhapsody": [
            "She went into _____ about the beautiful sunset over the sea.",
            "The music critic wrote a _____ praising the young pianist's performance.",
            "He burst into _____ when describing his favourite book.",
            "The poem was a _____ celebrating the beauty of nature.",
            "She spoke in _____ about her trip to the mountains.",
            "The composer wrote a _____ inspired by the countryside.",
            "He went into _____ describing the delicious meal.",
            "The review was a _____ extolling the film's virtues.",
            "She burst into _____ about the wonderful surprise party.",
            "The speech became a _____ praising the achievements of the team."
        ],
        "rhetoric": [
            "The politician's powerful _____ convinced many voters.",
            "The teacher explained how _____ can be used to persuade people.",
            "His empty _____ didn't match his actual actions.",
            "The speech was full of impressive _____ but lacked substance.",
            "She studied the _____ of great historical speeches.",
            "The debate team learned how to use _____ effectively.",
            "His _____ was persuasive but not entirely truthful.",
            "The _____ of the advertisement made the product seem essential.",
            "She was skilled in the art of political _____.",
            "The _____ of the campaign speech inspired the crowd."
        ],
        "rigorous": [
            "The _____ training programme prepared the athletes for competition.",
            "The school had _____ standards for admission.",
            "The _____ examination tested every aspect of their knowledge.",
            "She followed a _____ study schedule to prepare for the exam.",
            "The _____ inspection found several problems with the building.",
            "The _____ testing ensured the product was safe to use.",
            "He maintained a _____ exercise routine to stay fit.",
            "The _____ analysis revealed important details.",
            "The _____ discipline helped the students succeed.",
            "The _____ requirements meant only the best candidates were accepted."
        ],
        "ruthless": [
            "The _____ villain showed no mercy to his enemies.",
            "The _____ dictator ruled with an iron fist.",
            "The _____ competitor would do anything to win.",
            "The _____ business owner fired employees without warning.",
            "The _____ general ordered the attack without hesitation.",
            "The _____ hunter showed no compassion for the animals.",
            "The _____ critic destroyed the young writer's confidence.",
            "The _____ coach pushed his team beyond their limits.",
            "The _____ pirate plundered ships without remorse.",
            "The _____ ruler crushed any opposition to his power."
        ],
        "sabotage": [
            "The spy tried to _____ the enemy's communication system.",
            "The disgruntled employee attempted to _____ the company's computer network.",
            "They discovered someone had tried to _____ the experiment.",
            "The rebels planned to _____ the bridge to stop the enemy advance.",
            "He was accused of trying to _____ the peace negotiations.",
            "The competitor tried to _____ the other team's equipment.",
            "She was caught trying to _____ her rival's chances of winning.",
            "The traitor attempted to _____ the military operation.",
            "They feared someone would _____ the important meeting.",
            "The criminal tried to _____ the evidence against him."
        ],
        "sanguine": [
            "Despite the setbacks, she remained _____ about the project's success.",
            "His _____ outlook helped him through difficult times.",
            "The _____ forecast predicted sunny weather for the weekend.",
            "She was _____ that everything would work out in the end.",
            "His _____ attitude was infectious and lifted everyone's spirits.",
            "The _____ report suggested the economy would improve.",
            "She remained _____ even when others were losing hope.",
            "His _____ nature made him popular with his classmates.",
            "The _____ prediction gave everyone confidence.",
            "She was _____ about her chances of passing the exam."
        ],
        "sarcastic": [
            "His _____ remarks hurt her feelings more than he realised.",
            "The teacher's _____ comment made the student feel embarrassed.",
            "She replied with a _____ tone that showed her annoyance.",
            "His _____ sense of humour wasn't appreciated by everyone.",
            "The _____ review criticised the film harshly.",
            "She made a _____ comment about his messy room.",
            "His _____ response suggested he didn't take the situation seriously.",
            "The _____ letter mocked the company's policies.",
            "She couldn't help making a _____ remark about the delay.",
            "His _____ jokes often offended people unintentionally."
        ],
        "saturate": [
            "The heavy rain began to _____ the dry soil.",
            "The sponge will _____ with water if you leave it in the sink.",
            "The market was _____ with similar products.",
            "The advertising campaign will _____ all media channels.",
            "The floodwaters began to _____ the lower floors of the building.",
            "The cloth will _____ quickly if you dip it in the dye.",
            "The news coverage will _____ all television channels.",
            "The water began to _____ through the old roof.",
            "The market became _____ with cheap imitations.",
            "The rain continued to _____ the already wet ground."
        ],
        "secluded": [
            "The _____ beach was hidden away from the main tourist areas.",
            "They found a _____ spot in the forest for their picnic.",
            "The _____ cottage was miles from the nearest village.",
            "She preferred the _____ corner of the library for studying.",
            "The _____ garden was surrounded by tall hedges.",
            "The _____ path led to a secret waterfall.",
            "The _____ island was only accessible by boat.",
            "They discovered a _____ clearing in the middle of the woods.",
            "The _____ location made it perfect for a quiet retreat.",
            "The _____ valley was untouched by modern development."
        ],
        "sectarian": [
            "The _____ violence divided the once peaceful community.",
            "The _____ conflict had been going on for generations.",
            "The _____ differences caused tension between the groups.",
            "The _____ disputes made it difficult to find common ground.",
            "The _____ divisions prevented cooperation between the groups.",
            "The _____ tensions escalated into open conflict.",
            "The _____ groups refused to work together.",
            "The _____ hatred was passed down through families.",
            "The _____ boundaries were strictly enforced.",
            "The _____ issues dominated the political debate."
        ],
        "semantics": [
            "They argued about the _____ of the word 'freedom'.",
            "The _____ of the sentence changed depending on the context.",
            "The linguist studied the _____ of ancient languages.",
            "The debate was really about _____ rather than facts.",
            "She explained the _____ of the technical term.",
            "The _____ of the contract needed careful examination.",
            "They discussed the _____ of the philosophical concept.",
            "The _____ of the word varied between different regions.",
            "The study of _____ helps us understand how meaning works.",
            "The _____ of the message was clear despite the confusing words."
        ],
        "sequester": [
            "The jury was _____ during the high-profile trial.",
            "They had to _____ the contaminated area to prevent spread.",
            "The witness was _____ in a safe location.",
            "The government decided to _____ the dangerous chemicals.",
            "The judge ordered to _____ the jury until a verdict was reached.",
            "They had to _____ the infected patients from the others.",
            "The evidence was _____ in a secure vault.",
            "The committee was _____ to make their decision in private.",
            "They decided to _____ the valuable artwork in a museum.",
            "The scientists had to _____ the rare specimens carefully."
        ],
        "singular": [
            "His _____ talent for music set him apart from others.",
            "The _____ achievement had never been accomplished before.",
            "She possessed a _____ ability to understand people.",
            "The _____ event changed everything for the better.",
            "His _____ focus on his goal impressed everyone.",
            "The _____ beauty of the landscape took her breath away.",
            "She had a _____ way of solving problems.",
            "The _____ moment would be remembered forever.",
            "His _____ dedication to his studies was remarkable.",
            "The _____ nature of the discovery amazed scientists."
        ],
        "sinister": [
            "The _____ figure lurked in the shadows of the alleyway.",
            "The _____ plot was discovered just in time.",
            "The _____ music created an atmosphere of fear.",
            "The _____ smile on his face made her nervous.",
            "The _____ building had been abandoned for years.",
            "The _____ plan threatened to destroy everything.",
            "The _____ clouds gathered overhead before the storm.",
            "The _____ character in the story was the villain.",
            "The _____ atmosphere made everyone feel uneasy.",
            "The _____ warning sent shivers down her spine."
        ],
        "slothful": [
            "The _____ student never completed his homework on time.",
            "His _____ attitude towards work got him into trouble.",
            "The _____ employee was always the last to arrive.",
            "She was too _____ to clean her room properly.",
            "The _____ cat spent all day sleeping in the sun.",
            "His _____ behaviour disappointed his parents.",
            "The _____ worker was eventually dismissed.",
            "She was criticised for her _____ approach to studying.",
            "The _____ student missed many opportunities.",
            "His _____ nature prevented him from achieving his goals."
        ],
        "slovenly": [
            "His _____ appearance concerned his teachers.",
            "The _____ room was a mess of clothes and books.",
            "Her _____ handwriting was difficult to read.",
            "The _____ way he dressed showed he didn't care.",
            "The _____ condition of the house shocked visitors.",
            "His _____ habits made him unpopular with his flatmates.",
            "The _____ work was returned for improvement.",
            "She was embarrassed by her _____ presentation.",
            "The _____ garden was overgrown with weeds.",
            "His _____ attitude towards personal hygiene worried his parents."
        ],
        "sluggish": [
            "The _____ traffic made them late for the appointment.",
            "The _____ economy showed little growth.",
            "The _____ computer took ages to load programs.",
            "The _____ river barely moved through the valley.",
            "The _____ response to the emergency was criticised.",
            "The _____ pace of the lesson bored the students.",
            "The _____ start to the race surprised everyone.",
            "The _____ internet connection made streaming impossible.",
            "The _____ movement of the sloth fascinated the children.",
            "The _____ recovery from the illness worried the doctors."
        ],
        "sociable": [
            "She was very _____ and made friends wherever she went.",
            "The _____ student enjoyed group projects.",
            "His _____ nature made him popular at parties.",
            "The _____ dog loved meeting new people.",
            "She had a _____ personality that attracted others.",
            "The _____ atmosphere at the event made everyone feel welcome.",
            "His _____ behaviour helped break the ice.",
            "The _____ gathering brought people together.",
            "She was too _____ to enjoy being alone.",
            "The _____ character of the café encouraged conversation."
        ],
        "solitude": [
            "She enjoyed the peaceful _____ of the early morning.",
            "The writer sought _____ to work on her novel.",
            "The _____ of the mountain cabin appealed to him.",
            "She found _____ in the quiet library corner.",
            "The _____ of the desert was both beautiful and lonely.",
            "He needed _____ to think about his decision.",
            "The _____ of the garden provided a place for reflection.",
            "She valued her _____ and didn't like constant interruptions.",
            "The _____ of the empty beach was perfect for meditation.",
            "He found _____ in his daily walk through the park."
        ],
        "soothing": [
            "The _____ music helped her fall asleep quickly.",
            "The _____ voice of the narrator calmed the children.",
            "The _____ balm relieved the pain in her muscles.",
            "The _____ colours of the room created a peaceful atmosphere.",
            "The _____ sound of rain helped her relax.",
            "The _____ touch of her mother's hand comforted her.",
            "The _____ words reassured the worried patient.",
            "The _____ effect of the warm bath was immediate.",
            "The _____ melody played softly in the background.",
            "The _____ presence of her friend made everything better."
        ],
        "spiteful": [
            "Her _____ comments hurt his feelings deeply.",
            "The _____ act of vandalism shocked the community.",
            "His _____ behaviour towards his classmates was unacceptable.",
            "The _____ remark was designed to cause maximum hurt.",
            "She couldn't understand why he was so _____.",
            "The _____ prank went too far and caused damage.",
            "His _____ actions were motivated by jealousy.",
            "The _____ letter contained many hurtful accusations.",
            "She regretted her _____ words as soon as she said them.",
            "The _____ nature of the attack was completely unnecessary."
        ],
        "sporadic": [
            "_____ showers are expected throughout the day.",
            "The _____ power cuts made it difficult to work.",
            "The _____ attendance at meetings was concerning.",
            "_____ gunfire could be heard in the distance.",
            "The _____ internet connection was frustrating.",
            "_____ outbreaks of the disease were reported.",
            "The _____ applause showed mixed reactions to the performance.",
            "_____ bursts of energy helped him finish the race.",
            "The _____ nature of the attacks made them unpredictable.",
            "_____ sightings of the rare bird excited birdwatchers."
        ],
        "spurious": [
            "His _____ claims were quickly disproven by experts.",
            "The _____ evidence was rejected by the court.",
            "The _____ argument didn't convince anyone.",
            "The _____ report contained many false statements.",
            "The _____ excuse didn't fool the teacher.",
            "The _____ information spread quickly on the internet.",
            "The _____ document was exposed as a forgery.",
            "The _____ theory had no scientific basis.",
            "The _____ allegations were completely unfounded.",
            "The _____ data led to incorrect conclusions."
        ],
        "squabble": [
            "The children began to _____ over who would go first.",
            "The siblings would _____ about everything.",
            "The _____ over the last biscuit lasted several minutes.",
            "They continued to _____ about trivial matters.",
            "The _____ between the neighbours was getting worse.",
            "The children would _____ whenever they were bored.",
            "The _____ over the remote control was silly.",
            "They would _____ about whose turn it was to wash up.",
            "The _____ disrupted the peaceful atmosphere.",
            "The children would _____ constantly during long car journeys."
        ],
        "squander": [
            "Don't _____ your talents on trivial pursuits.",
            "He managed to _____ his entire inheritance in just one year.",
            "She didn't want to _____ her opportunity to study abroad.",
            "The team would _____ their lead by making careless mistakes.",
            "Don't _____ your time on meaningless activities.",
            "He would _____ his money on unnecessary purchases.",
            "She refused to _____ her chance to make a difference.",
            "The company would _____ its resources on failed projects.",
            "Don't _____ your energy on things that don't matter.",
            "He would _____ his potential by not working hard enough."
        ],
        "stagnant": [
            "The _____ water in the pond bred mosquitoes.",
            "The _____ economy showed no signs of improvement.",
            "The _____ air in the room made it hard to breathe.",
            "The _____ job market offered few opportunities.",
            "The _____ pond had a foul smell.",
            "The _____ situation seemed impossible to change.",
            "The _____ water had turned green with algae.",
            "The _____ business showed no growth for years.",
            "The _____ atmosphere in the office was depressing.",
            "The _____ career offered no chance for advancement."
        ],
        "steadfast": [
            "She remained _____ in her support for the cause.",
            "His _____ loyalty never wavered despite the difficulties.",
            "The _____ friend stood by her through everything.",
            "She was _____ in her determination to succeed.",
            "His _____ commitment to his principles was admirable.",
            "The _____ soldier never abandoned his post.",
            "She remained _____ in her beliefs despite opposition.",
            "His _____ resolve helped him overcome all obstacles.",
            "The _____ supporter never lost faith.",
            "She was _____ in her refusal to compromise her values."
        ],
        "strenuous": [
            "The _____ hike up the mountain exhausted everyone.",
            "The _____ exercise routine required great dedication.",
            "The _____ training prepared the athletes for competition.",
            "The _____ climb tested their physical limits.",
            "The _____ work left him feeling tired but satisfied.",
            "The _____ effort finally paid off with success.",
            "The _____ journey through the desert was challenging.",
            "The _____ practice sessions improved their skills.",
            "The _____ activity required proper preparation.",
            "The _____ task demanded all their energy and focus."
        ],
        "strident": [
            "His _____ voice dominated the entire meeting.",
            "The _____ tone of her complaint was hard to ignore.",
            "The _____ sound of the alarm woke everyone up.",
            "The _____ criticism was harsh but necessary.",
            "The _____ music was too loud for the small room.",
            "The _____ demands were met with resistance.",
            "The _____ voice cut through the noise of the crowd.",
            "The _____ protest could be heard from blocks away.",
            "The _____ argument caused tension in the room.",
            "The _____ call for action mobilised the community."
        ],
        "stringent": [
            "_____ safety measures were introduced after the accident.",
            "The _____ rules were strictly enforced.",
            "The _____ requirements meant only the best were accepted.",
            "The _____ testing ensured the product was safe.",
            "The _____ standards were difficult to meet.",
            "The _____ regulations protected the environment.",
            "The _____ controls prevented unauthorised access.",
            "The _____ guidelines had to be followed exactly.",
            "The _____ conditions made it hard to qualify.",
            "The _____ policies were necessary but unpopular."
        ],
        "subtlety": [
            "The _____ of her argument impressed the judges.",
            "The _____ of the joke was lost on most people.",
            "The _____ of the painting's colours was beautiful.",
            "The _____ of his approach made it more effective.",
            "The _____ of the difference was hard to notice.",
            "The _____ of her performance showed great skill.",
            "The _____ of the flavour made the dish special.",
            "The _____ of the message required careful reading.",
            "The _____ of the design was appreciated by experts.",
            "The _____ of her writing style was sophisticated."
        ],
        "succinct": [
            "Her _____ reply answered the question perfectly.",
            "The _____ summary covered all the main points.",
            "The _____ explanation was clear and to the point.",
            "The _____ message conveyed everything necessary.",
            "The _____ report was easy to understand.",
            "The _____ instructions were followed without confusion.",
            "The _____ description captured the essence perfectly.",
            "The _____ speech was well received by the audience.",
            "The _____ note contained all the important information.",
            "The _____ answer satisfied the examiner."
        ],
        "supersede": [
            "The new law will _____ the old regulations.",
            "The updated version will _____ the previous edition.",
            "The modern method will _____ traditional techniques.",
            "The new system will _____ the outdated one.",
            "The revised policy will _____ the existing rules.",
            "The improved design will _____ the original model.",
            "The new technology will _____ older methods.",
            "The updated software will _____ the current version.",
            "The new agreement will _____ the previous contract.",
            "The modern approach will _____ conventional practices."
        ],
        "suppress": [
            "She tried to _____ her laughter during the serious meeting.",
            "The government tried to _____ the rebellion.",
            "He had to _____ his anger to remain calm.",
            "The medication helped _____ the symptoms.",
            "She tried to _____ her excitement about the surprise.",
            "The authorities tried to _____ the spread of the disease.",
            "He had to _____ his fear to complete the task.",
            "The fire service worked to _____ the flames.",
            "She tried to _____ her disappointment.",
            "The system was designed to _____ errors automatically."
        ],
        "surmount": [
            "She managed to _____ all the obstacles in her path.",
            "The team worked together to _____ the challenges.",
            "He was determined to _____ every difficulty.",
            "The climbers hoped to _____ the mountain peak.",
            "She would _____ any barrier to achieve her goal.",
            "The engineers found a way to _____ the technical problems.",
            "He managed to _____ his fear of public speaking.",
            "The organisation worked to _____ the funding crisis.",
            "She would _____ all setbacks with determination.",
            "The students worked hard to _____ the learning difficulties."
        ],
        "swindler": [
            "The _____ tricked many elderly people out of their savings.",
            "The _____ was finally caught and sent to prison.",
            "The _____ used clever schemes to deceive his victims.",
            "The _____ posed as a charity worker to gain trust.",
            "The _____ was exposed when one victim reported him.",
            "The _____ targeted vulnerable people in the community.",
            "The _____ used fake documents to convince people.",
            "The _____ was known for his smooth talking.",
            "The _____ disappeared after taking people's money.",
            "The _____ was eventually brought to justice."
        ],
        "sycophant": [
            "The _____ always agreed with whatever the boss said.",
            "The _____ flattered the teacher to get better grades.",
            "The _____ was disliked by everyone except his target.",
            "The _____ would do anything to gain favour.",
            "The _____ praised the leader excessively.",
            "The _____ was known for his insincere compliments.",
            "The _____ followed the popular student everywhere.",
            "The _____ would change his opinion to match others.",
            "The _____ was transparent in his attempts to please.",
            "The _____ was eventually exposed for his false loyalty."
        ],
        "symbolism": [
            "The _____ in the poem added depth to its meaning.",
            "The _____ of the colours represented different emotions.",
            "The _____ in the story helped convey the theme.",
            "The _____ of the flag represented national unity.",
            "The _____ in the painting was open to interpretation.",
            "The _____ of the journey represented personal growth.",
            "The _____ in the novel was carefully crafted.",
            "The _____ of the seasons reflected the character's mood.",
            "The _____ in the play enhanced its meaning.",
            "The _____ of the light represented hope."
        ],
        "symmetry": [
            "The butterfly's wings showed perfect _____.",
            "The _____ of the building's design was impressive.",
            "The _____ of her face was considered beautiful.",
            "The _____ of the pattern was pleasing to the eye.",
            "The _____ of the snowflake fascinated the children.",
            "The _____ of the garden layout was carefully planned.",
            "The _____ of the mathematical equation was elegant.",
            "The _____ of the dance movements was precise.",
            "The _____ of the architectural design was striking.",
            "The _____ of the flower's petals was perfect."
        ],
        "taciturn": [
            "The _____ man rarely spoke to anyone.",
            "The _____ student preferred to work alone.",
            "The _____ character in the book was mysterious.",
            "The _____ teacher didn't say much but was very wise.",
            "The _____ nature of the guide made the tour quiet.",
            "The _____ response suggested he didn't want to discuss it.",
            "The _____ farmer worked in silence all day.",
            "The _____ guest sat quietly in the corner.",
            "The _____ employee did his work without conversation.",
            "The _____ grandfather spoke only when necessary."
        ],
        "tangible": [
            "There was no _____ evidence of the crime.",
            "The _____ benefits of exercise were clear to see.",
            "The _____ results showed the experiment was successful.",
            "The _____ proof was needed to convince the jury.",
            "The _____ improvements were noticeable immediately.",
            "The _____ object could be held and examined.",
            "The _____ rewards motivated the students to work harder.",
            "The _____ evidence supported the theory.",
            "The _____ results proved the method worked.",
            "The _____ benefits made the effort worthwhile."
        ],
        "tapestry": [
            "The ancient _____ told a story of battles and heroes.",
            "The beautiful _____ hung on the castle wall.",
            "The intricate _____ took years to complete.",
            "The colourful _____ depicted scenes from history.",
            "The medieval _____ was a work of art.",
            "The woven _____ showed detailed patterns.",
            "The historical _____ was displayed in the museum.",
            "The elaborate _____ covered the entire wall.",
            "The traditional _____ was passed down through generations.",
            "The magnificent _____ was the centrepiece of the room."
        ],
        "terminate": [
            "The company decided to _____ his contract.",
            "The train will _____ its journey at the final station.",
            "The school had to _____ the problematic programme.",
            "The contract will _____ at the end of the month.",
            "The manager decided to _____ the unsuccessful project.",
            "The agreement will _____ if conditions aren't met.",
            "The school had to _____ the student's enrolment.",
            "The service will _____ automatically after the trial period.",
            "The relationship will _____ if trust isn't restored.",
            "The subscription will _____ unless renewed."
        ],
        "thrilled": [
            "She was _____ to receive the award.",
            "The children were _____ about the school trip.",
            "He was _____ when he heard the good news.",
            "She was _____ to meet her favourite author.",
            "The team was _____ with their victory.",
            "He was _____ to discover he had won the competition.",
            "She was _____ about the surprise party.",
            "The students were _____ to learn about the field trip.",
            "He was _____ when his application was accepted.",
            "She was _____ to see her best friend after so long."
        ],
        "tractable": [
            "The _____ horse was easy to train.",
            "The _____ student followed instructions willingly.",
            "The _____ material was easy to shape.",
            "The _____ child was a pleasure to teach.",
            "The _____ problem was solved quickly.",
            "The _____ employee adapted to changes easily.",
            "The _____ metal could be bent without breaking.",
            "The _____ nature of the situation made it manageable.",
            "The _____ student was eager to learn.",
            "The _____ clay was perfect for the pottery class."
        ],
        "treachery": [
            "His _____ shocked everyone who trusted him.",
            "The _____ of the betrayal was hard to forgive.",
            "The _____ of the spy endangered many lives.",
            "The _____ was discovered before it could cause harm.",
            "The _____ of his actions was unforgivable.",
            "The _____ was exposed when the truth came out.",
            "The _____ of the double agent was revealed.",
            "The _____ caused irreparable damage to relationships.",
            "The _____ of the plot was carefully planned.",
            "The _____ was met with anger and disappointment."
        ],
        "trifling": [
            "The _____ matter was not worth arguing about.",
            "The _____ amount of money was insignificant.",
            "The _____ detail didn't affect the overall result.",
            "The _____ mistake was easily corrected.",
            "The _____ issue was quickly resolved.",
            "The _____ sum was barely noticeable.",
            "The _____ problem was soon forgotten.",
            "The _____ concern didn't warrant attention.",
            "The _____ error was of no consequence.",
            "The _____ difference was barely perceptible."
        ],
        "ultimatum": [
            "The boss gave him an _____: improve or be fired.",
            "The _____ was clear: comply or face consequences.",
            "The _____ left no room for negotiation.",
            "The _____ forced him to make a difficult decision.",
            "The _____ was delivered with finality.",
            "The _____ gave him one last chance.",
            "The _____ was met with resistance.",
            "The _____ required an immediate response.",
            "The _____ was the final demand.",
            "The _____ made the situation very clear."
        ],
        "uncaring": [
            "His _____ attitude towards the homeless was shocking.",
            "The _____ response showed a lack of compassion.",
            "The _____ behaviour upset many people.",
            "The _____ nature of the comment was hurtful.",
            "The _____ approach ignored people's feelings.",
            "The _____ treatment of animals was unacceptable.",
            "The _____ remark showed no empathy.",
            "The _____ attitude was difficult to understand.",
            "The _____ response lacked any warmth.",
            "The _____ behaviour demonstrated a lack of concern."
        ],
        "undermine": [
            "The constant criticism began to _____ her confidence.",
            "The leaks tried to _____ the government's position.",
            "The rumours would _____ his reputation.",
            "The problems began to _____ the project's success.",
            "The setbacks would _____ their progress.",
            "The criticism would _____ his self-esteem.",
            "The delays began to _____ the schedule.",
            "The errors would _____ the system's reliability.",
            "The doubts began to _____ their trust.",
            "The failures would _____ their determination."
        ],
        "untoward": [
            "Nothing _____ happened during the journey.",
            "The _____ incident caused concern among the staff.",
            "The _____ event disrupted the peaceful atmosphere.",
            "The _____ behaviour was reported to the authorities.",
            "The _____ situation required immediate attention.",
            "The _____ development surprised everyone.",
            "The _____ occurrence was unexpected.",
            "The _____ circumstances made things difficult.",
            "The _____ turn of events worried them.",
            "The _____ incident was quickly resolved."
        ],
        "unwitting": [
            "She was an _____ participant in the scheme.",
            "The _____ victim had no idea what was happening.",
            "The _____ accomplice didn't realise the crime.",
            "The _____ helper was used without their knowledge.",
            "The _____ witness saw more than they understood.",
            "The _____ participant was completely innocent.",
            "The _____ helper was unaware of the deception.",
            "The _____ person was caught up in the situation.",
            "The _____ involvement was discovered later.",
            "The _____ helper had no malicious intent."
        ],
        "unworthy": [
            "He felt _____ of the honour bestowed upon him.",
            "The _____ behaviour disappointed everyone.",
            "The _____ treatment was unacceptable.",
            "The _____ candidate was rejected.",
            "The _____ act brought shame to the family.",
            "The _____ response showed poor character.",
            "The _____ conduct was criticised.",
            "The _____ person didn't deserve the reward.",
            "The _____ behaviour was beneath him.",
            "The _____ action was quickly regretted."
        ],
        "vacillate": [
            "He continued to _____ between the two options.",
            "The committee would _____ on the decision.",
            "She would _____ whenever asked to choose.",
            "The government would _____ on the policy.",
            "He would _____ between hope and despair.",
            "The team would _____ about the strategy.",
            "She would _____ when making important decisions.",
            "The opinion would _____ with each new piece of information.",
            "He would _____ between staying and leaving.",
            "The mood would _____ throughout the day."
        ],
        "vanadium": [
            "_____ is used in making steel stronger.",
            "The element _____ has many industrial applications.",
            "_____ is found in certain minerals.",
            "The metal _____ is important for manufacturing.",
            "_____ compounds are used in various industries.",
            "The element _____ was discovered in the 19th century.",
            "_____ is used to strengthen alloys.",
            "The chemical _____ has specific properties.",
            "_____ is extracted from certain ores.",
            "The element _____ is essential for some processes."
        ],
        "vanguard": [
            "The scientists were at the _____ of medical research.",
            "The company was at the _____ of technology innovation.",
            "The explorers were at the _____ of discovery.",
            "The artists were at the _____ of the new movement.",
            "The students were at the _____ of change.",
            "The team was at the _____ of scientific advancement.",
            "The organisation was at the _____ of social reform.",
            "The researchers were at the _____ of knowledge.",
            "The innovators were at the _____ of progress.",
            "The leaders were at the _____ of the movement."
        ],
        "venerate": [
            "The people _____ their ancestors.",
            "They _____ the memory of the great leader.",
            "The community would _____ the ancient traditions.",
            "They _____ the wisdom of their elders.",
            "The students would _____ their inspiring teacher.",
            "They _____ the heroes who saved the town.",
            "The nation would _____ its founding fathers.",
            "They _____ the principles of justice and freedom.",
            "The community would _____ the local saint.",
            "They _____ the achievements of their predecessors."
        ],
        "vengeance": [
            "He sought _____ for the wrong done to his family.",
            "The _____ was swift and severe.",
            "The desire for _____ consumed him.",
            "The act of _____ brought no satisfaction.",
            "The _____ was planned carefully.",
            "The thirst for _____ drove his actions.",
            "The _____ was disproportionate to the offence.",
            "The cycle of _____ seemed endless.",
            "The _____ was carried out in secret.",
            "The desire for _____ was eventually replaced by forgiveness."
        ],
        "venomous": [
            "The _____ snake posed a danger to hikers.",
            "The _____ spider's bite could be fatal.",
            "The _____ creature was handled with extreme care.",
            "The _____ animal was kept in a secure enclosure.",
            "The _____ insect's sting was very painful.",
            "The _____ reptile was native to the region.",
            "The _____ bite required immediate medical attention.",
            "The _____ species was well documented.",
            "The _____ attack was unexpected.",
            "The _____ nature of the animal was well known."
        ],
        "vigilant": [
            "The _____ guard noticed the suspicious activity.",
            "The _____ watch kept everyone safe.",
            "The _____ security prevented the break-in.",
            "The _____ parent watched over the children.",
            "The _____ monitoring detected the problem early.",
            "The _____ observer noticed the subtle changes.",
            "The _____ guard remained alert throughout the night.",
            "The _____ attention prevented accidents.",
            "The _____ supervision ensured everything went smoothly.",
            "The _____ care protected the valuable items."
        ],
        "vigorous": [
            "The _____ exercise left him feeling refreshed.",
            "The _____ debate continued for hours.",
            "The _____ growth of the plants was impressive.",
            "The _____ activity kept them fit and healthy.",
            "The _____ defence of his position was convincing.",
            "The _____ campaign raised awareness effectively.",
            "The _____ effort produced excellent results.",
            "The _____ workout challenged even the fittest athletes.",
            "The _____ discussion covered many important points.",
            "The _____ approach solved the problem quickly."
        ],
        "vindicate": [
            "The new evidence helped to _____ the suspect.",
            "The results would _____ her decision.",
            "The investigation would _____ his claims.",
            "The proof would _____ their actions.",
            "The findings would _____ the theory.",
            "The evidence would _____ her reputation.",
            "The outcome would _____ his position.",
            "The results would _____ their approach.",
            "The proof would _____ the strategy.",
            "The evidence would _____ their innocence."
        ],
        "virtuoso": [
            "The _____ pianist gave an outstanding performance.",
            "The _____ musician's skill was extraordinary.",
            "The _____ violinist played with incredible technique.",
            "The _____ performer received a standing ovation.",
            "The _____ artist's work was masterful.",
            "The _____ guitarist amazed the audience.",
            "The _____ singer's voice was beautiful.",
            "The _____ conductor led the orchestra brilliantly.",
            "The _____ cellist's performance was flawless.",
            "The _____ flautist's playing was exquisite."
        ],
        "virulent": [
            "The _____ disease spread quickly through the population.",
            "The _____ infection required immediate treatment.",
            "The _____ strain was particularly dangerous.",
            "The _____ virus affected many people.",
            "The _____ illness spread rapidly.",
            "The _____ bacteria were resistant to treatment.",
            "The _____ outbreak caused widespread concern.",
            "The _____ pathogen was highly contagious.",
            "The _____ nature of the disease was alarming.",
            "The _____ infection needed urgent medical attention."
        ],
        "vitriolic": [
            "His _____ attack on the proposal shocked everyone.",
            "The _____ criticism was harsh and bitter.",
            "The _____ comments were filled with anger.",
            "The _____ response was completely unexpected.",
            "The _____ attack was personal and hurtful.",
            "The _____ criticism destroyed her confidence.",
            "The _____ words were spoken with venom.",
            "The _____ attack was unprovoked.",
            "The _____ response was disproportionate.",
            "The _____ criticism was difficult to bear."
        ],
        "voyeurism": [
            "_____ is considered an invasion of privacy.",
            "The act of _____ is illegal and unethical.",
            "The _____ was discovered and reported to the police.",
            "The practice of _____ violates people's rights.",
            "The _____ was caught and prosecuted.",
            "The act of _____ is a serious offence.",
            "The _____ was condemned by everyone.",
            "The practice of _____ is unacceptable.",
            "The _____ was exposed and stopped.",
            "The act of _____ is morally wrong."
        ],
        "whinging": [
            "The _____ child never stopped complaining.",
            "The _____ tone was annoying to everyone.",
            "The constant _____ got on everyone's nerves.",
            "The _____ complaints were never-ending.",
            "The _____ voice was hard to listen to.",
            "The persistent _____ was tiresome.",
            "The _____ attitude didn't help the situation.",
            "The _____ behaviour was immature.",
            "The _____ complaints achieved nothing.",
            "The _____ child needed to learn to be more positive."
        ],
        "withered": [
            "The _____ flowers had lost their beauty.",
            "The _____ leaves fell from the tree.",
            "The _____ plant needed water desperately.",
            "The _____ appearance showed neglect.",
            "The _____ branches were brittle and dry.",
            "The _____ garden looked sad and abandoned.",
            "The _____ petals crumbled to dust.",
            "The _____ condition was due to lack of care.",
            "The _____ state was irreversible.",
            "The _____ flowers were removed from the vase."
        ],
        "withhold": [
            "The teacher decided to _____ the results until later.",
            "The company would _____ payment until the work was complete.",
            "The parent would _____ privileges as punishment.",
            "The government would _____ information for security reasons.",
            "The judge would _____ judgment until all evidence was heard.",
            "The school would _____ certificates until fees were paid.",
            "The employer would _____ wages for poor performance.",
            "The authority would _____ permission for safety reasons.",
            "The parent would _____ approval until conditions were met.",
            "The organisation would _____ support until requirements were fulfilled."
        ],
        "yearning": [
            "His _____ for adventure led him to travel the world.",
            "The _____ to see her family was overwhelming.",
            "The deep _____ for home made her homesick.",
            "The _____ for knowledge drove her studies.",
            "The _____ to succeed motivated him daily.",
            "The intense _____ for freedom was powerful.",
            "The _____ to belong made her join the club.",
            "The strong _____ for change inspired action.",
            "The _____ to understand kept her researching.",
            "The persistent _____ for peace united them."
        ]
    }
    
    # Return word-specific sentences if available
    if word_lower in word_sentences:
        return word_sentences[word_lower][:10]
    
    # Fallback: generate generic sentences based on word type
    if is_verb:
        sentences.extend([
            f"She decided to _____ when the situation became difficult.",
            f"He learned to _____ after many years of practice.",
            f"They will _____ before it's too late.",
            f"The team worked together to _____ the challenge.",
            f"Nobody wanted to _____ in such circumstances.",
            f"She managed to _____ despite the obstacles.",
            f"They were forced to _____ when they had no choice.",
            f"He refused to _____ even when others insisted.",
            f"She will _____ if the conditions are met.",
            f"The group will _____ to solve the problem."
        ])
    elif is_adjective:
        sentences.extend([
            f"The _____ student worked hard every day.",
            f"Her _____ attitude impressed everyone.",
            f"The _____ situation required careful handling.",
            f"His _____ behaviour surprised his classmates.",
            f"The _____ nature of the problem was clear.",
            f"She showed a _____ approach to the task.",
            f"The _____ quality made it stand out.",
            f"His _____ response was unexpected.",
            f"The _____ character of the place was obvious.",
            f"She had a _____ way of solving problems."
        ])
    else:  # noun
        sentences.extend([
            f"The _____ was clear from the context.",
            f"She showed great _____ in the situation.",
            f"His _____ surprised everyone around him.",
            f"The _____ became evident as the story unfolded.",
            f"They demonstrated _____ throughout the challenge.",
            f"Her _____ was obvious to all who watched.",
            f"The situation required _____ from everyone.",
            f"His _____ made a significant difference.",
            f"The _____ was apparent in their actions.",
            f"She expressed _____ in her response."
        ])
    
    return sentences[:10]


def main():
    """Generate quiz sentences for all words in level3_batch5.txt"""
    input_file = Path(__file__).parent.parent / "data" / "level3_batch5.txt"
    output_file = Path(__file__).parent.parent / "data" / "level3_batch5.csv"
    
    sentences_data = []
    
    # Read words from input file
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('|')
            if len(parts) >= 3:
                word = parts[0].strip()
                meaning = parts[1].strip()
                example = parts[2].strip() if len(parts) > 2 else ""
                synonym = parts[3].strip() if len(parts) > 3 else ""
                antonym = parts[4].strip() if len(parts) > 4 else ""
                
                # Generate 10 sentences for this word
                word_sentences = generate_sentences_for_word(word, meaning, example, synonym, antonym)
                
                # Add each sentence to the data
                for sentence in word_sentences:
                    sentences_data.append({
                        'level': '3',
                        'word': word,
                        'sentence': sentence
                    })
    
    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['level', 'word', 'sentence'])
        writer.writeheader()
        writer.writerows(sentences_data)
    
    print(f"Level 3 Batch 5 complete: {len(sentences_data)} sentences")


if __name__ == "__main__":
    main()
