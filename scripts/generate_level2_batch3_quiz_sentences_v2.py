#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 2 Batch 3 vocabulary.
Creates 10 contextually rich sentences per word with strong contextual clues.
Uses example sentences and word-specific logic for better quality.
"""

import csv
import re
from pathlib import Path
from typing import List, Dict


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
            word_lower[:-1] + 'ed'
        ])
    elif word_lower.endswith('y'):
        patterns.extend([
            word_lower[:-1] + 'ied',
            word_lower[:-1] + 'ies',
            word_lower[:-1] + 'ying'
        ])
    elif word_lower.endswith('ise') or word_lower.endswith('ize'):
        patterns.extend([
            word_lower[:-2] + 'ised',
            word_lower[:-2] + 'ized',
            word_lower[:-2] + 'ising',
            word_lower[:-2] + 'izing'
        ])
    else:
        patterns.extend([
            word_lower + 'ed',
            word_lower + 's',
            word_lower + 'ing',
            word_lower + 'ly',
            word_lower + 'er'
        ])
    
    # Replace word forms with blank
    result = sentence
    for pattern in sorted(set(patterns), key=len, reverse=True):
        regex = re.compile(r'\b' + re.escape(pattern) + r'\b', re.IGNORECASE)
        result = regex.sub("_____", result)
    
    return result


def generate_sentences_for_word(
    word: str, 
    meaning: str, 
    example: str, 
    synonym: str, 
    antonym: str
) -> List[str]:
    """
    Generate 10 contextually rich quiz sentences for a word.
    Uses the example sentence and creates varied, contextually appropriate sentences.
    """
    sentences = []
    word_lower = word.lower()
    meaning_lower = meaning.lower()
    
    # Always use example sentence first if available
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Determine word type
    is_verb = meaning_lower.startswith("to ")
    is_adjective = any(marker in meaning_lower for marker in [
        "having", "showing", "full of", "characterised by", "characterized by",
        "very", "extremely", "quite", "rather", "causing", "deserving",
        "feeling", "unwilling", "willing", "fond of", "eager to"
    ]) or meaning_lower.startswith(("an ", "a ")) and not is_verb
    
    # Create word-specific sentences based on meaning
    # Use synonyms and antonyms for contextual clues
    
    # Word-specific sentence generation
    word_specific_sentences = {
        "envelop": [
            "The fog began to _____ the entire valley completely.",
            "Darkness started to _____ the forest as night fell.",
            "The mist would _____ the mountains every morning.",
            "Silence began to _____ the room after the announcement.",
            "The smoke started to _____ the building quickly.",
            "Warmth began to _____ her as she sat by the fire.",
            "The sound would _____ the entire neighbourhood.",
            "Peace began to _____ the troubled area.",
            "The light started to _____ the dark corners.",
            "Calm began to _____ the anxious crowd."
        ],
        "eponym": [
            "Sandwich is an _____ from the Earl of Sandwich.",
            "The word 'boycott' is an _____ named after Captain Boycott.",
            "Her name became an _____ for the new product.",
            "The scientist's name became an _____ for the discovery.",
            "Many words are _____ derived from people's names.",
            "The _____ honoured the person who first created it.",
            "His surname became an _____ used worldwide.",
            "The _____ remembered the inventor's contribution.",
            "She was surprised to learn her name was an _____.",
            "The _____ celebrated the person's achievement."
        ],
        "equipped": [
            "The fully _____ kitchen had everything we needed.",
            "The expedition was well _____ with supplies.",
            "She felt _____ to handle the challenge ahead.",
            "The team was poorly _____ for the difficult task.",
            "They made sure they were _____ before starting.",
            "The school was fully _____ with modern technology.",
            "He wasn't properly _____ for the cold weather.",
            "The laboratory was _____ with the latest equipment.",
            "She arrived _____ with all necessary documents.",
            "The soldiers were fully _____ for the mission."
        ],
        "erratic": [
            "His _____ behaviour worried his friends and family.",
            "The _____ weather made planning difficult.",
            "Her _____ mood changed from moment to moment.",
            "The _____ pattern made it hard to predict.",
            "His _____ performance varied greatly each time.",
            "The _____ schedule caused confusion for everyone.",
            "Her _____ responses were difficult to understand.",
            "The _____ results surprised the researchers.",
            "His _____ movements were hard to follow.",
            "The _____ nature of the problem made it challenging."
        ],
        "erudite": [
            "The _____ professor knew everything about ancient history.",
            "Her _____ lecture impressed all the students.",
            "The _____ scholar had read thousands of books.",
            "His _____ comments showed his deep knowledge.",
            "The _____ discussion was fascinating to listen to.",
            "Her _____ writing was admired by academics.",
            "The _____ expert answered every question.",
            "His _____ manner impressed everyone he met.",
            "The _____ teacher made complex topics clear.",
            "Her _____ analysis revealed new insights."
        ],
        "escalate": [
            "The small disagreement began to _____ into a major argument.",
            "Tensions started to _____ between the two groups.",
            "The conflict would _____ if not addressed quickly.",
            "The problem began to _____ beyond their control.",
            "The situation started to _____ rapidly.",
            "The debate would _____ as more people joined in.",
            "The crisis began to _____ throughout the region.",
            "The issue started to _____ unexpectedly.",
            "The argument would _____ without intervention.",
            "The dispute began to _____ into violence."
        ],
        "eulogy": [
            "The _____ celebrated the life of the much-loved teacher.",
            "Her _____ moved everyone to tears.",
            "The _____ honoured the memory of the hero.",
            "His _____ praised the achievements of the team.",
            "The _____ remembered all the good times.",
            "Her _____ was heartfelt and sincere.",
            "The _____ captured the essence of the person.",
            "His _____ was eloquent and touching.",
            "The _____ brought comfort to the family.",
            "Her _____ was beautifully written and delivered."
        ],
        "euphoria": [
            "The team felt _____ after winning the championship.",
            "Her _____ was obvious from her expression.",
            "The _____ overwhelmed everyone in the room.",
            "His _____ showed clearly on his face.",
            "The _____ made her feel wonderful.",
            "Her _____ was contagious and spread to others.",
            "The _____ filled the entire stadium.",
            "His _____ was genuine and heartfelt.",
            "The _____ lifted everyone's spirits.",
            "Her _____ was evident to all."
        ],
        "exacting": [
            "The _____ teacher expected perfect homework every time.",
            "His _____ standards were difficult to meet.",
            "The _____ requirements made the task challenging.",
            "Her _____ approach ensured high quality work.",
            "The _____ boss expected excellence from everyone.",
            "His _____ methods produced excellent results.",
            "The _____ examination tested all their knowledge.",
            "Her _____ expectations pushed them to improve.",
            "The _____ training prepared them well.",
            "His _____ attitude made him respected."
        ],
        "expedite": [
            "They worked overtime to _____ the delivery process.",
            "She tried to _____ the completion of her homework.",
            "The manager wanted to _____ the project timeline.",
            "He found ways to _____ the approval process.",
            "They needed to _____ the response time significantly.",
            "She managed to _____ the decision-making process.",
            "The team worked hard to _____ the final deadline.",
            "He was able to _____ the paperwork completion.",
            "They tried to _____ the construction work.",
            "She found a method to _____ the entire procedure."
        ],
        "expertise": [
            "Her _____ in coding helped build the website.",
            "The _____ required years of practice to develop.",
            "His _____ was evident in his work.",
            "The _____ made him valuable to the team.",
            "Her _____ impressed all the experts.",
            "The _____ was essential for success.",
            "His _____ set him apart from others.",
            "The _____ required dedication and hard work.",
            "Her _____ was recognised by everyone.",
            "The _____ was crucial for the project."
        ],
        "explicit": [
            "The instructions were _____ and easy to follow.",
            "Her _____ explanation left no room for confusion.",
            "The _____ details helped everyone understand.",
            "His _____ directions were very clear.",
            "The _____ statement removed all doubt.",
            "Her _____ description was thorough.",
            "The _____ rules were clearly stated.",
            "His _____ answer addressed every question.",
            "The _____ guidelines prevented mistakes.",
            "Her _____ words left nothing unclear."
        ],
        "exquisite": [
            "The _____ jewellery sparkled brilliantly in the display case.",
            "Her _____ dress was admired by everyone at the party.",
            "The _____ garden was full of colourful flowers.",
            "His _____ painting won first prize in the competition.",
            "The _____ sunset filled the sky with vibrant colours.",
            "Her _____ smile brightened everyone's day.",
            "The _____ architecture impressed all the visitors.",
            "His _____ handwriting was neat and elegant.",
            "The _____ melody was pleasant to listen to.",
            "Her _____ voice was clear and melodious."
        ],
        "extricate": [
            "They managed to _____ the cat from the tree branches.",
            "She tried to _____ herself from the difficult situation.",
            "He worked hard to _____ the trapped bird.",
            "The rescue team attempted to _____ the hikers.",
            "They needed to _____ the stuck door carefully.",
            "She was able to _____ the knot after several tries.",
            "He tried to _____ the jammed drawer.",
            "They managed to _____ the vehicle from the mud.",
            "She worked to _____ the tangled rope.",
            "He was able to _____ the situation successfully."
        ],
        "extrovert": [
            "The _____ loved meeting new people at parties.",
            "Her reputation as a _____ was well-known.",
            "The _____ spent all evening chatting with strangers.",
            "His behaviour showed he was a true _____.",
            "The _____ couldn't resist social gatherings.",
            "Her actions revealed she was an _____.",
            "The _____ was admired by everyone.",
            "His character showed he was a genuine _____.",
            "The _____ made a significant contribution.",
            "Her nature indicated she was a real _____."
        ],
        "fateful": [
            "The _____ decision changed the course of history.",
            "Her _____ choice affected everyone involved.",
            "The _____ moment determined their future.",
            "His _____ action had lasting effects.",
            "The _____ event shaped everything that followed.",
            "Her _____ step was irreversible.",
            "The _____ turning point was significant.",
            "His _____ move changed everything.",
            "The _____ choice was crucial.",
            "Her _____ decision was momentous."
        ],
        "flawless": [
            "Her _____ performance earned her the gold medal.",
            "The _____ diamond had no visible imperfections.",
            "His _____ timing was crucial to their success.",
            "The _____ execution impressed all the judges.",
            "Her _____ memory helped her recall every detail.",
            "The _____ conditions made it ideal for the event.",
            "His _____ aim hit the target every time.",
            "The _____ symmetry of the building was remarkable.",
            "Her _____ technique was admired by all.",
            "The _____ quality exceeded everyone's expectations."
        ],
        "fluctuate": [
            "Temperatures can _____ greatly during spring.",
            "The prices began to _____ throughout the day.",
            "Her mood would _____ depending on the weather.",
            "The numbers started to _____ unexpectedly.",
            "His energy levels would _____ during the week.",
            "The value began to _____ in the market.",
            "Her confidence would _____ with each test.",
            "The results started to _____ significantly.",
            "His interest would _____ from day to day.",
            "The levels began to _____ without warning."
        ],
        "foolhardy": [
            "It was _____ to swim in the rough sea.",
            "His _____ attempt endangered everyone.",
            "The _____ decision led to disaster.",
            "Her _____ actions worried her friends.",
            "The _____ plan was doomed to fail.",
            "His _____ behaviour was reckless.",
            "The _____ choice showed poor judgement.",
            "Her _____ stunt was dangerous.",
            "The _____ adventure was ill-advised.",
            "His _____ move was unwise."
        ],
        "foremost": [
            "She was the _____ expert on ancient Egyptian history.",
            "His position as the _____ authority was undisputed.",
            "The _____ leader guided them successfully.",
            "Her role as the _____ specialist was important.",
            "The _____ figure was respected by all.",
            "His status as the _____ professional was clear.",
            "The _____ pioneer opened new possibilities.",
            "Her reputation as the _____ expert was well-known.",
            "The _____ champion defended their rights.",
            "His position as the _____ advocate was crucial."
        ],
        "foresight": [
            "His _____ helped the company avoid many problems.",
            "Her _____ to see ahead was remarkable.",
            "The _____ prevented several disasters.",
            "His _____ saved them from making mistakes.",
            "The _____ was a valuable skill.",
            "Her _____ impressed all the managers.",
            "The _____ helped plan for the future.",
            "His _____ was well-developed.",
            "The _____ made him successful.",
            "Her _____ was recognised by everyone."
        ],
        "forestall": [
            "She tried to _____ any arguments by explaining clearly.",
            "He worked to _____ the problem before it worsened.",
            "They attempted to _____ the conflict from starting.",
            "She managed to _____ the disaster from happening.",
            "He tried to _____ the misunderstanding early.",
            "They worked to _____ the crisis from developing.",
            "She attempted to _____ the problem in advance.",
            "He managed to _____ the issue before it escalated.",
            "They tried to _____ the situation from worsening.",
            "She worked to _____ the conflict from arising."
        ],
        "frightful": [
            "The _____ storm kept everyone awake all night.",
            "Her _____ scream echoed through the house.",
            "The _____ accident shocked everyone.",
            "His _____ appearance frightened the children.",
            "The _____ noise made them cover their ears.",
            "Her _____ story gave them nightmares.",
            "The _____ scene was hard to forget.",
            "His _____ behaviour was unacceptable.",
            "The _____ weather forced them indoors.",
            "Her _____ mistake cost them dearly."
        ],
        "fulfilled": [
            "She felt _____ after helping the charity.",
            "His _____ expression showed his satisfaction.",
            "The _____ feeling made her happy.",
            "Her _____ dreams came true.",
            "The _____ promise brought joy.",
            "His _____ wish was granted.",
            "The _____ goal was achieved.",
            "Her _____ desire was satisfied.",
            "The _____ need was met.",
            "His _____ hope was realised."
        ],
        "galvanise": [
            "The speech _____ the team into immediate action.",
            "The news would _____ people to help the victims.",
            "Her words began to _____ the audience into responding.",
            "The event would _____ the community into volunteering.",
            "The announcement started to _____ everyone into action.",
            "His speech would _____ the students into studying harder.",
            "The crisis began to _____ the nation into helping.",
            "The story would _____ readers into donating money.",
            "The situation started to _____ people into changing.",
            "The message would _____ listeners into taking action."
        ],
        "galvanize": [
            "The news _____ people to help the victims.",
            "The speech would _____ the team into action.",
            "Her words began to _____ the audience.",
            "The event would _____ the community.",
            "The announcement started to _____ everyone.",
            "His speech would _____ the students.",
            "The crisis began to _____ the nation.",
            "The story would _____ readers.",
            "The situation started to _____ people.",
            "The message would _____ listeners."
        ],
        "grandeur": [
            "The _____ of the palace took everyone's breath away.",
            "Her appreciation for the _____ was evident.",
            "The _____ impressed all the visitors.",
            "His sense of _____ was overwhelming.",
            "The _____ made them feel small.",
            "Her description captured the _____ perfectly.",
            "The _____ was truly magnificent.",
            "His reaction to the _____ was amazement.",
            "The _____ was beyond description.",
            "Her experience of the _____ was unforgettable."
        ],
        "grandiose": [
            "His _____ plans seemed impossible to achieve.",
            "The _____ scheme was unrealistic.",
            "Her _____ ideas were too ambitious.",
            "The _____ project was doomed to fail.",
            "His _____ vision was impressive but impractical.",
            "The _____ design was overly complex.",
            "Her _____ ambitions were admirable but unattainable.",
            "The _____ proposal was rejected.",
            "His _____ dreams were beyond reach.",
            "The _____ concept was too elaborate."
        ],
        "granular": [
            "The _____ texture of the sand made it ideal for building.",
            "Her _____ skin showed signs of sun damage.",
            "The _____ surface felt rough to the touch.",
            "His _____ photograph was slightly blurred.",
            "The _____ material was perfect for the project.",
            "His _____ voice had a rough quality.",
            "The _____ appearance indicated poor quality.",
            "Her _____ drawing lacked smooth lines.",
            "The _____ finish needed more sanding.",
            "His _____ handwriting was hard to read."
        ],
        "grotesque": [
            "The _____ mask frightened the young children.",
            "His _____ appearance shocked everyone who saw him.",
            "The _____ sculpture was intentionally disturbing.",
            "Her _____ expression showed her anger clearly.",
            "The _____ building was an eyesore in the neighbourhood.",
            "His _____ behaviour was unacceptable.",
            "The _____ painting was meant to provoke thought.",
            "Her _____ words hurt everyone's feelings.",
            "The _____ design was deliberately shocking.",
            "His _____ actions were condemned by all."
        ],
        "grudging": [
            "He gave only _____ approval to the plan.",
            "Her _____ agreement showed she wasn't happy.",
            "The _____ nod indicated his hesitation.",
            "His _____ acceptance was clear from his expression.",
            "The _____ response suggested she didn't want to.",
            "Her _____ participation was obvious to everyone.",
            "The _____ smile showed her true feelings.",
            "His _____ cooperation made the task difficult.",
            "The _____ attitude slowed down progress.",
            "Her _____ consent was given under pressure."
        ],
        "guarantee": [
            "The shop offered a money-back _____ on all products.",
            "Her _____ gave them confidence in the purchase.",
            "The _____ ensured customer satisfaction.",
            "His _____ was written in the contract.",
            "The _____ covered all possible problems.",
            "Her _____ was honoured by the company.",
            "The _____ provided peace of mind.",
            "His _____ was unconditional and reliable.",
            "The _____ protected the buyer's rights.",
            "Her _____ was backed by the manufacturer."
        ],
        "hackneyed": [
            "The speech was full of _____ phrases.",
            "Her _____ expressions bored the audience.",
            "The _____ saying was overused.",
            "His _____ words lacked originality.",
            "The _____ cliché was tiresome.",
            "Her _____ language was uncreative.",
            "The _____ expression was stale.",
            "His _____ phrase was predictable.",
            "The _____ saying was trite.",
            "Her _____ words were clichéd."
        ],
        "hallowed": [
            "The _____ grounds of the ancient temple.",
            "Her respect for the _____ place was evident.",
            "The _____ site was protected.",
            "His reverence for the _____ space was clear.",
            "The _____ hall was treated with respect.",
            "Her visit to the _____ location was meaningful.",
            "The _____ area was sacred.",
            "His understanding of the _____ tradition was deep.",
            "The _____ ceremony was important.",
            "Her appreciation for the _____ custom was genuine."
        ],
        "handsome": [
            "The _____ prince arrived on a white horse.",
            "Her _____ reward was generous.",
            "The _____ donation helped many people.",
            "His _____ appearance impressed everyone.",
            "The _____ sum was more than expected.",
            "Her _____ gift was appreciated.",
            "The _____ amount covered all expenses.",
            "His _____ contribution was significant.",
            "The _____ payment was fair.",
            "Her _____ offer was accepted."
        ],
        "heartless": [
            "It was _____ to ignore the suffering of others.",
            "Her _____ actions shocked everyone.",
            "The _____ decision showed no compassion.",
            "His _____ behaviour was cruel.",
            "The _____ comment hurt deeply.",
            "Her _____ attitude was unkind.",
            "The _____ treatment was unacceptable.",
            "His _____ words were harsh.",
            "The _____ response lacked empathy.",
            "Her _____ nature was disturbing."
        ],
        "hedonist": [
            "The _____ spent all his money on luxuries.",
            "Her reputation as a _____ was well-known.",
            "The _____ lived only for pleasure.",
            "His behaviour showed he was a true _____.",
            "The _____ couldn't resist temptation.",
            "Her actions revealed she was a _____.",
            "The _____ was admired by some.",
            "His character showed he was a genuine _____.",
            "The _____ made no sacrifices.",
            "Her nature indicated she was a real _____."
        ],
        "heedless": [
            "He was _____ of the danger and continued walking.",
            "Her _____ attitude worried her parents.",
            "The _____ behaviour was reckless.",
            "His _____ actions showed no concern.",
            "The _____ decision was unwise.",
            "Her _____ approach was dangerous.",
            "The _____ mistake was costly.",
            "His _____ nature caused problems.",
            "The _____ choice was foolish.",
            "Her _____ disregard was concerning."
        ],
        "heresy": [
            "In medieval times _____ was punished severely.",
            "Her _____ shocked the religious community.",
            "The _____ was considered blasphemous.",
            "His _____ challenged traditional beliefs.",
            "The _____ was condemned by authorities.",
            "Her _____ was controversial.",
            "The _____ went against accepted doctrine.",
            "His _____ was revolutionary.",
            "The _____ was dangerous to express.",
            "Her _____ was heretical."
        ],
        "hierarchy": [
            "The military has a strict _____ of command.",
            "Her understanding of the _____ helped her succeed.",
            "The _____ ensured everything ran smoothly.",
            "His position in the _____ gave him authority.",
            "The _____ was clearly defined and understood.",
            "Her role in the _____ was important.",
            "The _____ maintained order and structure.",
            "His knowledge of the _____ was extensive.",
            "The _____ provided clear guidelines.",
            "Her place in the _____ was well-established."
        ],
        "homograph": [
            "'Bow' and 'bow' are _____ with different meanings.",
            "Her understanding of _____ helped her in English class.",
            "The _____ confused many students.",
            "His knowledge of _____ was impressive.",
            "The _____ made the text more interesting.",
            "Her explanation of _____ was clear.",
            "The _____ were fun to learn about.",
            "His examples of _____ helped others understand.",
            "The _____ showed the complexity of English.",
            "Her study of _____ improved her reading."
        ],
        "homonym": [
            "The word 'bank' is a _____ meaning both river edge and financial institution.",
            "Her understanding of _____ helped her comprehension.",
            "The _____ confused many readers.",
            "His knowledge of _____ was extensive.",
            "The _____ made the sentence ambiguous.",
            "Her explanation of _____ was helpful.",
            "The _____ were interesting to study.",
            "His examples of _____ clarified the concept.",
            "The _____ showed language complexity.",
            "Her analysis of _____ was thorough."
        ],
        "idyllic": [
            "They spent an _____ summer in the countryside.",
            "Her _____ life seemed perfect.",
            "The _____ setting was beautiful.",
            "His _____ existence was peaceful.",
            "The _____ scene was picturesque.",
            "Her _____ home was charming.",
            "The _____ atmosphere was relaxing.",
            "His _____ retreat was tranquil.",
            "The _____ environment was serene.",
            "Her _____ experience was wonderful."
        ],
        "illicit": [
            "The police discovered an _____ operation.",
            "Her _____ activities were illegal.",
            "The _____ trade was stopped.",
            "His _____ behaviour was criminal.",
            "The _____ deal was exposed.",
            "Her _____ actions were forbidden.",
            "The _____ practice was banned.",
            "His _____ scheme was uncovered.",
            "The _____ activity was prohibited.",
            "Her _____ conduct was unlawful."
        ],
        "immoral": [
            "Cheating on exams is considered _____ behaviour.",
            "Her _____ actions shocked everyone.",
            "The _____ decision was wrong.",
            "His _____ conduct was unacceptable.",
            "The _____ practice was condemned.",
            "Her _____ choices were unethical.",
            "The _____ act was reprehensible.",
            "His _____ behaviour was disgraceful.",
            "The _____ deed was shameful.",
            "Her _____ nature was disturbing."
        ],
        "implied": [
            "Her silence _____ that she agreed with the decision.",
            "The _____ meaning was clear.",
            "His _____ suggestion was understood.",
            "The _____ message was subtle.",
            "Her _____ consent was assumed.",
            "The _____ agreement was unspoken.",
            "His _____ promise was inferred.",
            "The _____ threat was real.",
            "Her _____ approval was given.",
            "The _____ criticism was indirect."
        ],
        "inertia": [
            "Overcoming _____ is the hardest part of starting exercise.",
            "Her _____ prevented her from acting.",
            "The _____ kept them stuck.",
            "His _____ was difficult to overcome.",
            "The _____ slowed down progress.",
            "Her _____ was frustrating.",
            "The _____ resisted change.",
            "His _____ was strong.",
            "The _____ maintained the status quo.",
            "Her _____ was hard to break."
        ],
        "infamy": [
            "He achieved _____ for his terrible deeds.",
            "Her _____ spread quickly.",
            "The _____ was well-deserved.",
            "His _____ was notorious.",
            "The _____ was remembered.",
            "Her _____ was infamous.",
            "The _____ was lasting.",
            "His _____ was earned.",
            "The _____ was deserved.",
            "Her _____ was known."
        ],
        "ingrate": [
            "Only an _____ would complain after receiving such help.",
            "Her behaviour showed she was an _____.",
            "The _____ was ungrateful.",
            "His actions revealed he was an _____.",
            "The _____ showed no appreciation.",
            "Her attitude marked her as an _____.",
            "The _____ was unthankful.",
            "His character showed he was an _____.",
            "The _____ was thankless.",
            "Her nature revealed she was an _____."
        ],
        "innate": [
            "She had an _____ talent for music.",
            "His _____ ability was remarkable.",
            "The _____ skill was natural.",
            "Her _____ gift was evident.",
            "The _____ quality was inborn.",
            "His _____ talent was inherited.",
            "The _____ ability was present from birth.",
            "Her _____ skill was instinctive.",
            "The _____ gift was inherent.",
            "His _____ talent was genetic."
        ],
        "insipid": [
            "The _____ soup needed more seasoning.",
            "His _____ speech bored the audience.",
            "The _____ meal had no flavour.",
            "Her _____ presentation failed to engage.",
            "The _____ book was difficult to finish.",
            "His _____ personality was forgettable.",
            "The _____ conversation went nowhere.",
            "Her _____ writing lacked excitement.",
            "The _____ performance received no applause.",
            "His _____ response showed no enthusiasm."
        ],
        "insular": [
            "Their _____ attitude prevented new ideas.",
            "His _____ thinking limited understanding.",
            "The _____ approach missed opportunities.",
            "Her _____ views were outdated.",
            "The _____ perspective ignored possibilities.",
            "His _____ mindset prevented progress.",
            "The _____ community resisted change.",
            "Her _____ beliefs were challenged.",
            "The _____ outlook restricted options.",
            "His _____ approach failed to consider alternatives."
        ],
        "ironic": [
            "It was _____ that the fire station burned down.",
            "Her _____ comment was sarcastic.",
            "The _____ situation was unexpected.",
            "His _____ remark was witty.",
            "The _____ twist surprised everyone.",
            "Her _____ observation was clever.",
            "The _____ outcome was amusing.",
            "His _____ statement was paradoxical.",
            "The _____ coincidence was remarkable.",
            "Her _____ humour was appreciated."
        ],
        "jittery": [
            "She felt _____ before her first day at school.",
            "His _____ hands shook as he waited.",
            "The _____ student couldn't sit still.",
            "Her _____ expression showed worry.",
            "The _____ atmosphere made everyone uncomfortable.",
            "His _____ behaviour indicated anxiety.",
            "The _____ feeling wouldn't go away.",
            "Her _____ voice trembled as she spoke.",
            "The _____ anticipation kept them awake.",
            "His _____ movements showed his anxiety."
        ],
        "jocular": [
            "His _____ manner made everyone laugh.",
            "The _____ comment lightened the mood.",
            "Her _____ personality was cheerful.",
            "The _____ remark was amusing.",
            "His _____ nature was fun-loving.",
            "The _____ joke was well-received.",
            "Her _____ attitude was playful.",
            "The _____ humour was appreciated.",
            "His _____ style was entertaining.",
            "The _____ banter was enjoyable."
        ],
        "laconic": [
            "His _____ reply revealed nothing.",
            "The _____ response was brief.",
            "Her _____ answer was concise.",
            "The _____ statement was short.",
            "His _____ comment was terse.",
            "The _____ explanation was minimal.",
            "Her _____ reply was curt.",
            "The _____ answer was pithy.",
            "His _____ response was succinct.",
            "The _____ comment was economical."
        ],
        "legacy": [
            "The ancient buildings are part of our cultural _____.",
            "Her family's _____ included valuable antiques.",
            "The _____ was passed down through generations.",
            "His grandfather's _____ was carefully preserved.",
            "The _____ represented years of tradition.",
            "Her _____ included important historical documents.",
            "The _____ was a source of pride.",
            "His family's _____ was well-documented.",
            "The _____ connected them to their past.",
            "Her _____ was cherished by all."
        ],
        "litotes": [
            "Saying 'not bad' when something is excellent is an example of _____.",
            "Her use of _____ made her writing interesting.",
            "The _____ added humour to the conversation.",
            "His understanding of _____ improved his writing.",
            "The _____ was cleverly used in the poem.",
            "Her knowledge of _____ helped her analyse texts.",
            "The _____ made the statement more effective.",
            "His use of _____ showed his skill with language.",
            "The _____ was a common literary device.",
            "Her explanation of _____ helped others understand."
        ],
        "malady": [
            "The doctor identified the _____ as flu.",
            "Her _____ required immediate treatment.",
            "The _____ spread quickly through the school.",
            "His _____ kept him home from school.",
            "The _____ affected many people.",
            "Her _____ was difficult to diagnose.",
            "The _____ caused her to feel unwell.",
            "His _____ needed medical attention.",
            "The _____ was contagious and dangerous.",
            "Her _____ prevented her from participating."
        ],
        "mariner": [
            "The experienced _____ had sailed across many oceans.",
            "Her father was a skilled _____ who loved the sea.",
            "The _____ navigated through the storm successfully.",
            "His grandfather had been a famous _____.",
            "The _____ told exciting stories of his adventures.",
            "Her uncle was a retired _____.",
            "The _____ knew how to read the stars.",
            "His friend wanted to become a _____.",
            "The _____ had travelled to many countries.",
            "Her neighbour was an experienced _____."
        ],
        "marred": [
            "The beautiful view was _____ by the construction site.",
            "Her perfect day was _____ by the sudden rain.",
            "The celebration was _____ by the argument.",
            "His reputation was _____ by false rumours.",
            "The event was _____ by technical problems.",
            "Her performance was _____ by the mistake.",
            "The occasion was _____ by unexpected guests.",
            "His success was _____ by the controversy.",
            "The moment was _____ by the interruption.",
            "Her achievement was _____ by the criticism."
        ],
        "mayhem": [
            "The children created _____ in the classroom when the teacher left.",
            "Her actions caused complete _____ in the room.",
            "The _____ made it impossible to work.",
            "His behaviour led to total _____.",
            "The _____ disrupted everything.",
            "Her arrival caused _____ among the group.",
            "The _____ was overwhelming and chaotic.",
            "His actions resulted in absolute _____.",
            "The _____ prevented any progress.",
            "Her mistake led to complete _____."
        ],
        "meander": [
            "The river _____ through the green valley.",
            "Her path began to _____ through the forest.",
            "The road would _____ around the mountain.",
            "His journey started to _____ unexpectedly.",
            "The trail began to _____ up the hillside.",
            "Her route would _____ past many landmarks.",
            "The stream began to _____ between the rocks.",
            "His walk would _____ through the park.",
            "The path started to _____ away from the main road.",
            "Her drive would _____ through the countryside."
        ],
        "measly": [
            "He received only a _____ amount of pocket money.",
            "The _____ portion left everyone hungry.",
            "Her _____ contribution was barely noticeable.",
            "The _____ number of participants disappointed them.",
            "His _____ effort wasn't enough to succeed.",
            "The _____ quantity was insufficient.",
            "Her _____ share seemed unfair.",
            "The _____ amount couldn't cover expenses.",
            "His _____ collection was just a few items.",
            "The _____ size made it difficult to see."
        ],
        "meddle": [
            "Please do not _____ in matters that do not concern you.",
            "She refused to _____ in their private affairs.",
            "The teacher warned them not to _____.",
            "His tendency to _____ caused problems.",
            "The _____ disrupted the process.",
            "Her attempt to _____ was unwelcome.",
            "The _____ interfered with progress.",
            "His habit of _____ annoyed everyone.",
            "The _____ created confusion.",
            "Her refusal to _____ was wise."
        ],
        "mediate": [
            "The teacher tried to _____ between the two arguing students.",
            "She was asked to _____ the dispute.",
            "The _____ helped resolve the conflict.",
            "His role was to _____ between parties.",
            "The _____ brought about agreement.",
            "Her attempt to _____ was successful.",
            "The _____ prevented further arguments.",
            "His skill in _____ was valuable.",
            "The _____ found a solution.",
            "Her ability to _____ was appreciated."
        ],
        "medley": [
            "The chef prepared a _____ of vegetables for the salad.",
            "Her collection was a _____ of different styles.",
            "The _____ included many different elements.",
            "His playlist was a _____ of various genres.",
            "The _____ combined different flavours perfectly.",
            "Her selection was a _____ of options.",
            "The _____ offered something for everyone.",
            "His work was a _____ of techniques.",
            "The _____ was well-balanced.",
            "Her creation was a _____ of ideas."
        ],
        "mellow": [
            "The _____ light of the evening sun filled the room.",
            "Her _____ voice was pleasant to listen to.",
            "The _____ texture felt nice.",
            "His _____ manner put everyone at ease.",
            "The _____ surface was perfect.",
            "Her _____ transition surprised everyone.",
            "The _____ music created a relaxing atmosphere.",
            "His _____ approach avoided conflicts.",
            "The _____ finish looked professional.",
            "Her _____ personality made her easy to talk to."
        ],
        "mimic": [
            "The parrot could _____ human speech perfectly.",
            "She tried to _____ her favourite singer.",
            "The actor could _____ different accents.",
            "His ability to _____ was impressive.",
            "The _____ was very accurate.",
            "Her attempt to _____ was amusing.",
            "The _____ sounded exactly like the original.",
            "His skill in _____ was remarkable.",
            "The _____ fooled everyone.",
            "Her talent for _____ was natural."
        ],
        "miserly": [
            "The _____ old man refused to buy new clothes.",
            "Her _____ behaviour was well-known.",
            "The _____ attitude saved money but lost friends.",
            "His _____ nature prevented generosity.",
            "The _____ approach was excessive.",
            "Her _____ ways were extreme.",
            "The _____ behaviour was unkind.",
            "His _____ habits were legendary.",
            "The _____ nature was obvious.",
            "Her _____ attitude was criticised."
        ],
        "mollify": [
            "He tried to _____ his angry friend with an apology.",
            "She attempted to _____ the upset customer.",
            "The _____ calmed the situation.",
            "His words helped to _____ her.",
            "The _____ soothed tempers.",
            "Her actions tried to _____ them.",
            "The _____ eased tensions.",
            "His approach helped to _____ the conflict.",
            "The _____ reduced anger.",
            "Her efforts to _____ were successful."
        ],
        "morbid": [
            "He had a _____ fascination with horror films.",
            "Her _____ curiosity worried her parents.",
            "The _____ interest was unhealthy.",
            "His _____ preoccupation was disturbing.",
            "The _____ obsession consumed his thoughts.",
            "Her _____ attraction was concerning.",
            "The _____ focus was inappropriate.",
            "His _____ attention was misplaced.",
            "The _____ concern was excessive.",
            "Her _____ interest was unhealthy."
        ],
        "morose": [
            "She sat in _____ silence after the bad news.",
            "His _____ expression showed unhappiness.",
            "The _____ weather matched her sad mood.",
            "Her _____ attitude affected everyone.",
            "The _____ atmosphere made the room depressing.",
            "His _____ outlook worried his friends.",
            "The _____ day made everything seem dull.",
            "Her _____ response showed disappointment.",
            "The _____ clouds overhead suggested rain.",
            "His _____ mood lasted all afternoon."
        ],
        "mundane": [
            "She longed to escape her _____ daily routine.",
            "The _____ task seemed endless.",
            "His _____ life lacked excitement.",
            "The _____ conversation didn't interest anyone.",
            "Her _____ job provided little challenge.",
            "The _____ meal was nothing special.",
            "His _____ appearance didn't stand out.",
            "The _____ day passed without events.",
            "Her _____ existence felt empty.",
            "The _____ routine became tiresome."
        ],
        "mutual": [
            "They had a _____ respect for each other's opinions.",
            "Her _____ agreement was shared.",
            "The _____ understanding helped them work together.",
            "His _____ feeling was reciprocated.",
            "The _____ benefit was clear.",
            "Her _____ interest was common.",
            "The _____ trust was important.",
            "His _____ admiration was returned.",
            "The _____ goal united them.",
            "Her _____ support was appreciated."
        ],
        "naivete": [
            "Her _____ about the world was both charming and concerning.",
            "The child's _____ was evident.",
            "His _____ showed lack of experience.",
            "The _____ made her vulnerable.",
            "Her _____ was refreshing but risky.",
            "The _____ prevented understanding.",
            "His _____ was both endearing and worrying.",
            "The _____ made her trust everyone.",
            "Her _____ was obvious to adults.",
            "The _____ needed protection."
        ],
        "nauseam": [
            "He repeated the same story ad _____ until everyone was bored.",
            "Her complaints went on ad _____ without stopping.",
            "The explanation continued ad _____ for hours.",
            "His talking ad _____ annoyed everyone.",
            "The repetition ad _____ was unbearable.",
            "Her questions ad _____ exhausted the teacher.",
            "The discussion ad _____ seemed endless.",
            "His comments ad _____ were unnecessary.",
            "The details ad _____ were too much.",
            "Her stories ad _____ bored the listeners."
        ]
    }
    
    # Check if we have word-specific sentences
    if word_lower in word_specific_sentences:
        specific = word_specific_sentences[word_lower]
        # Use example sentence first if available, then fill with specific sentences
        if len(sentences) < 10:
            needed = 10 - len(sentences)
            sentences.extend(specific[:needed])
    
    # Fill remaining slots with contextually appropriate sentences
    while len(sentences) < 10:
        if is_verb:
            if synonym:
                sentences.append(f"They had to _____ (similar to {synonym}) before the situation worsened.")
            elif antonym:
                sentences.append(f"She refused to _____ (opposite of {antonym}) despite the pressure.")
            else:
                sentences.append(f"They decided to _____ the situation carefully.")
        elif is_adjective:
            if synonym:
                sentences.append(f"His _____ (similar to {synonym}) attitude impressed everyone.")
            elif antonym:
                sentences.append(f"It was not _____ (opposite of {antonym}) as everyone expected.")
            else:
                sentences.append(f"Her _____ quality was evident to everyone.")
        else:  # noun
            if synonym:
                sentences.append(f"The _____ (similar to {synonym}) became clear to everyone.")
            elif antonym:
                sentences.append(f"The _____ (opposite of {antonym}) was not what they expected.")
            else:
                sentences.append(f"The _____ was important in understanding what happened.")
    
    return sentences[:10]


def parse_vocabulary_file(file_path: Path) -> List[Dict]:
    """Parse the vocabulary file and extract word information"""
    words = []
    
    with file_path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('|')
            if len(parts) >= 3:
                word = parts[0].strip()
                meaning = parts[1].strip()
                example = parts[2].strip() if len(parts) > 2 else ""
                synonym = parts[3].strip() if len(parts) > 3 else ""
                antonym = parts[4].strip() if len(parts) > 4 else ""
                
                words.append({
                    'word': word,
                    'meaning': meaning,
                    'example': example,
                    'synonym': synonym,
                    'antonym': antonym
                })
    
    return words


def main():
    """Main function to generate quiz sentences"""
    data_dir = Path(__file__).parent.parent / 'data'
    input_file = data_dir / 'level2_batch3.txt'
    output_file = data_dir / 'level2_batch3.csv'
    
    print(f"Reading vocabulary from: {input_file}")
    words = parse_vocabulary_file(input_file)
    print(f"Found {len(words)} words")
    
    all_sentences = []
    
    for i, word_data in enumerate(words, 1):
        word = word_data['word']
        meaning = word_data['meaning']
        example = word_data['example']
        synonym = word_data['synonym']
        antonym = word_data['antonym']
        
        print(f"Generating sentences for {i}/77: {word}")
        
        sentences = generate_sentences_for_word(word, meaning, example, synonym, antonym)
        
        for sentence in sentences:
            all_sentences.append({
                'level': '2',
                'word': word,
                'sentence': sentence
            })
    
    # Write to CSV
    print(f"\nWriting {len(all_sentences)} sentences to: {output_file}")
    with output_file.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['level', 'word', 'sentence'])
        writer.writeheader()
        writer.writerows(all_sentences)
    
    print(f"\n✅ Level 2 Batch 3 complete: {len(all_sentences)} sentences")
    print(f"   Generated 10 sentences for each of {len(words)} words")


if __name__ == '__main__':
    main()
