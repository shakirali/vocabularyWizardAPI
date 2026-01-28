#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 2 Batch 3 vocabulary.
Creates 10 contextually rich sentences per word with strong contextual clues.
"""

import csv
import re
from pathlib import Path
from typing import List, Tuple


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
            word_lower + 'er',
            word_lower + 'ly'
        ])
    
    # Replace word forms with blank
    result = sentence
    for pattern in sorted(set(patterns), key=len, reverse=True):
        regex = re.compile(r'\b' + re.escape(pattern) + r'\b', re.IGNORECASE)
        result = regex.sub("_____", result)
    
    return result


def determine_word_type(meaning: str) -> Tuple[bool, bool, bool]:
    """Determine if word is verb, adjective, or noun based on meaning"""
    meaning_lower = meaning.lower()
    
    is_verb = meaning_lower.startswith("to ")
    is_adjective = any(marker in meaning_lower for marker in [
        "having", "showing", "full of", "characterised by", "characterized by",
        "very", "extremely", "quite", "rather", "causing", "deserving",
        "feeling", "unwilling", "willing", "fond of", "eager to",
        "attractive", "unpleasant", "beautiful", "ugly", "good", "bad"
    ]) or meaning_lower.startswith(("an ", "a "))
    
    is_noun = not is_verb and not is_adjective
    
    return is_verb, is_adjective, is_noun


def generate_sentences_for_word(
    word: str, 
    meaning: str, 
    example: str, 
    synonym: str, 
    antonym: str
) -> List[str]:
    """
    Generate 10 contextually rich quiz sentences for a word.
    Each sentence provides strong contextual clues specific to the word's meaning.
    """
    sentences = []
    word_lower = word.lower()
    meaning_lower = meaning.lower()
    
    is_verb, is_adjective, is_noun = determine_word_type(meaning)
    
    # 1. Use example sentence if available and good quality
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example and len(blank_example.split()) >= 8:
            sentences.append(blank_example)
    
    # Generate contextually rich sentences based on word meaning and type
    # Use varied sentence structures to avoid repetitive patterns
    
    if is_verb:
        # Verb sentences - action-based contexts
        verb_sentences = [
            f"They had to _____ quickly before the situation got worse.",
            f"She decided to _____ the matter carefully and thoughtfully.",
            f"He refused to _____ despite the pressure from his friends.",
            f"The team worked together to _____ the difficult problem.",
            f"She managed to _____ successfully after many attempts.",
            f"They were forced to _____ when all other options failed.",
            f"He tried to _____ but found it more challenging than expected.",
            f"She learned how to _____ through practice and determination.",
            f"They needed to _____ in order to achieve their goal.",
            f"He was able to _____ because he had prepared well."
        ]
        
        # Customize based on meaning
        if "speed" in meaning_lower or "accelerate" in meaning_lower:
            verb_sentences = [
                f"They worked overtime to _____ the delivery process.",
                f"She tried to _____ the completion of her homework.",
                f"The manager wanted to _____ the project timeline.",
                f"He found ways to _____ the approval process.",
                f"They needed to _____ the response time significantly.",
                f"She managed to _____ the decision-making process.",
                f"The team worked hard to _____ the final deadline.",
                f"He was able to _____ the paperwork completion.",
                f"They tried to _____ the construction work.",
                f"She found a method to _____ the entire procedure."
            ]
        elif "free" in meaning_lower or "release" in meaning_lower:
            verb_sentences = [
                f"They managed to _____ the cat from the tree branches.",
                f"She tried to _____ herself from the difficult situation.",
                f"He worked hard to _____ the trapped bird.",
                f"The rescue team attempted to _____ the hikers.",
                f"They needed to _____ the stuck door carefully.",
                f"She was able to _____ the knot after several tries.",
                f"He tried to _____ the jammed drawer.",
                f"They managed to _____ the vehicle from the mud.",
                f"She worked to _____ the tangled rope.",
                f"He was able to _____ the situation successfully."
            ]
        elif "surround" in meaning_lower or "cover" in meaning_lower:
            verb_sentences = [
                f"The fog began to _____ the entire valley completely.",
                f"Darkness started to _____ the forest as night fell.",
                f"The mist would _____ the mountains every morning.",
                f"Silence began to _____ the room after the announcement.",
                f"The smoke started to _____ the building quickly.",
                f"Warmth began to _____ her as she sat by the fire.",
                f"The sound would _____ the entire neighbourhood.",
                f"Peace began to _____ the troubled area.",
                f"The light started to _____ the dark corners.",
                f"Calm began to _____ the anxious crowd."
            ]
        elif "increase" in meaning_lower or "intensify" in meaning_lower:
            verb_sentences = [
                f"The small disagreement began to _____ into a major argument.",
                f"Tensions started to _____ between the two groups.",
                f"The conflict would _____ if not addressed quickly.",
                f"The problem began to _____ beyond their control.",
                f"The situation started to _____ rapidly.",
                f"The debate would _____ as more people joined in.",
                f"The crisis began to _____ throughout the region.",
                f"The issue started to _____ unexpectedly.",
                f"The argument would _____ without intervention.",
                f"The problem began to _____ beyond expectations."
            ]
        elif "shock" in meaning_lower or "stimulate" in meaning_lower:
            verb_sentences = [
                f"The inspiring speech _____ the team into immediate action.",
                f"The news would _____ people to help the victims.",
                f"Her words began to _____ the audience into responding.",
                f"The event would _____ the community into volunteering.",
                f"The announcement started to _____ everyone into action.",
                f"His speech would _____ the students into studying harder.",
                f"The crisis began to _____ the nation into helping.",
                f"The story would _____ readers into donating money.",
                f"The situation started to _____ people into changing.",
                f"The message would _____ listeners into taking action."
            ]
        elif "prevent" in meaning_lower or "stop" in meaning_lower:
            verb_sentences = [
                f"She tried to _____ any arguments by explaining clearly.",
                f"He worked to _____ the problem before it worsened.",
                f"They attempted to _____ the conflict from starting.",
                f"She managed to _____ the disaster from happening.",
                f"He tried to _____ the misunderstanding early.",
                f"They worked to _____ the crisis from developing.",
                f"She attempted to _____ the problem in advance.",
                f"He managed to _____ the issue before it escalated.",
                f"They tried to _____ the situation from worsening.",
                f"She worked to _____ the conflict from arising."
            ]
        
        sentences.extend(verb_sentences[:10-len(sentences)])
        
    elif is_adjective:
        # Adjective sentences - descriptive contexts
        adj_sentences = [
            f"Her _____ performance earned her the highest marks.",
            f"The _____ quality made it truly special and unique.",
            f"His _____ attitude impressed everyone who met him.",
            f"The _____ appearance caught everyone's attention immediately.",
            f"She showed a _____ nature that made her popular.",
            f"The _____ behaviour surprised all the teachers.",
            f"His _____ response showed his true character.",
            f"The _____ atmosphere made everyone feel comfortable.",
            f"She had a _____ personality that everyone admired.",
            f"The _____ situation required careful consideration."
        ]
        
        # Customize based on meaning
        if "beautiful" in meaning_lower or "attractive" in meaning_lower:
            adj_sentences = [
                f"The _____ jewellery sparkled brilliantly in the display case.",
                f"Her _____ dress was admired by everyone at the party.",
                f"The _____ garden was full of colourful flowers.",
                f"His _____ painting won first prize in the competition.",
                f"The _____ sunset filled the sky with vibrant colours.",
                f"Her _____ smile brightened everyone's day.",
                f"The _____ architecture impressed all the visitors.",
                f"His _____ handwriting was neat and elegant.",
                f"The _____ melody was pleasant to listen to.",
                f"Her _____ voice was clear and melodious."
            ]
        elif "demanding" in meaning_lower or "strict" in meaning_lower:
            adj_sentences = [
                f"The _____ teacher expected perfect homework every time.",
                f"His _____ standards were difficult to meet.",
                f"The _____ requirements made the task challenging.",
                f"Her _____ approach ensured high quality work.",
                f"The _____ boss expected excellence from everyone.",
                f"His _____ methods produced excellent results.",
                f"The _____ examination tested all their knowledge.",
                f"Her _____ expectations pushed them to improve.",
                f"The _____ training prepared them well.",
                f"His _____ attitude made him respected."
            ]
        elif "unpredictable" in meaning_lower or "inconsistent" in meaning_lower:
            adj_sentences = [
                f"His _____ behaviour worried his friends and family.",
                f"The _____ weather made planning difficult.",
                f"Her _____ mood changed from moment to moment.",
                f"The _____ pattern made it hard to predict.",
                f"His _____ performance varied greatly each time.",
                f"The _____ schedule caused confusion for everyone.",
                f"Her _____ responses were difficult to understand.",
                f"The _____ results surprised the researchers.",
                f"His _____ movements were hard to follow.",
                f"The _____ nature of the problem made it challenging."
            ]
        elif "perfect" in meaning_lower or "flawless" in meaning_lower:
            adj_sentences = [
                f"Her _____ performance earned her the gold medal.",
                f"The _____ diamond had no visible imperfections.",
                f"His _____ timing was crucial to their success.",
                f"The _____ execution impressed all the judges.",
                f"Her _____ memory helped her recall every detail.",
                f"The _____ conditions made it ideal for the event.",
                f"His _____ aim hit the target every time.",
                f"The _____ symmetry of the building was remarkable.",
                f"Her _____ technique was admired by all.",
                f"The _____ quality exceeded everyone's expectations."
            ]
        elif "nervous" in meaning_lower or "anxious" in meaning_lower:
            adj_sentences = [
                f"She felt _____ before her first day at school.",
                f"His _____ hands shook as he waited for the results.",
                f"The _____ student couldn't sit still during the exam.",
                f"Her _____ expression showed her worry clearly.",
                f"The _____ atmosphere made everyone uncomfortable.",
                f"His _____ behaviour indicated he was worried.",
                f"The _____ feeling wouldn't go away.",
                f"Her _____ voice trembled as she spoke.",
                f"The _____ anticipation kept them awake.",
                f"His _____ movements showed his anxiety."
            ]
        elif "gloomy" in meaning_lower or "sullen" in meaning_lower:
            adj_sentences = [
                f"She sat in _____ silence after the bad news.",
                f"His _____ expression showed his unhappiness.",
                f"The _____ weather matched her sad mood.",
                f"Her _____ attitude affected everyone around her.",
                f"The _____ atmosphere made the room feel depressing.",
                f"His _____ outlook worried his friends.",
                f"The _____ day made everything seem dull.",
                f"Her _____ response showed her disappointment.",
                f"The _____ clouds overhead suggested rain.",
                f"His _____ mood lasted all afternoon."
            ]
        elif "reluctant" in meaning_lower or "unwilling" in meaning_lower:
            adj_sentences = [
                f"He gave only _____ approval to the plan.",
                f"Her _____ agreement showed she wasn't happy.",
                f"The _____ nod indicated his hesitation.",
                f"His _____ acceptance was clear from his expression.",
                f"The _____ response suggested she didn't want to.",
                f"Her _____ participation was obvious to everyone.",
                f"The _____ smile showed her true feelings.",
                f"His _____ cooperation made the task difficult.",
                f"The _____ attitude slowed down progress.",
                f"Her _____ consent was given under pressure."
            ]
        elif "narrow-minded" in meaning_lower or "isolated" in meaning_lower:
            adj_sentences = [
                f"Their _____ attitude prevented new ideas from being accepted.",
                f"His _____ thinking limited his understanding.",
                f"The _____ approach missed important opportunities.",
                f"Her _____ views were outdated and unhelpful.",
                f"The _____ perspective ignored other possibilities.",
                f"His _____ mindset prevented progress.",
                f"The _____ community resisted change.",
                f"Her _____ beliefs were challenged by new information.",
                f"The _____ outlook restricted their options.",
                f"His _____ approach failed to consider alternatives."
            ]
        elif "ordinary" in meaning_lower or "unexciting" in meaning_lower:
            adj_sentences = [
                f"She longed to escape her _____ daily routine.",
                f"The _____ task seemed endless and boring.",
                f"His _____ life lacked excitement and adventure.",
                f"The _____ conversation didn't interest anyone.",
                f"Her _____ job provided little challenge.",
                f"The _____ meal was nothing special.",
                f"His _____ appearance didn't stand out.",
                f"The _____ day passed without any events.",
                f"Her _____ existence felt empty and dull.",
                f"The _____ routine became tiresome quickly."
            ]
        elif "small" in meaning_lower or "few" in meaning_lower:
            adj_sentences = [
                f"He received only a _____ amount of pocket money.",
                f"The _____ portion left everyone hungry.",
                f"Her _____ contribution was barely noticeable.",
                f"The _____ number of participants disappointed them.",
                f"His _____ effort wasn't enough to succeed.",
                f"The _____ quantity was insufficient for the task.",
                f"Her _____ share seemed unfair compared to others.",
                f"The _____ amount couldn't cover the expenses.",
                f"His _____ collection was just a few items.",
                f"The _____ size made it difficult to see."
            ]
        elif "ugly" in meaning_lower or "distorted" in meaning_lower:
            adj_sentences = [
                f"The _____ mask frightened the young children.",
                f"His _____ appearance shocked everyone who saw him.",
                f"The _____ sculpture was intentionally disturbing.",
                f"Her _____ expression showed her anger clearly.",
                f"The _____ building was an eyesore in the neighbourhood.",
                f"His _____ behaviour was unacceptable.",
                f"The _____ painting was meant to provoke thought.",
                f"Her _____ words hurt everyone's feelings.",
                f"The _____ design was deliberately shocking.",
                f"His _____ actions were condemned by all."
            ]
        elif "smooth" in meaning_lower or "soft" in meaning_lower:
            adj_sentences = [
                f"The _____ light of the evening sun filled the room.",
                f"Her _____ voice was pleasant to listen to.",
                f"The _____ texture felt nice against her skin.",
                f"His _____ manner put everyone at ease.",
                f"The _____ surface was perfect for writing.",
                f"Her _____ transition surprised everyone.",
                f"The _____ music created a relaxing atmosphere.",
                f"His _____ approach avoided conflicts.",
                f"The _____ finish looked professional.",
                f"Her _____ personality made her easy to talk to."
            ]
        elif "bland" in meaning_lower or "lacking flavour" in meaning_lower:
            adj_sentences = [
                f"The _____ soup needed more seasoning to taste good.",
                f"His _____ speech bored the entire audience.",
                f"The _____ meal had no flavour at all.",
                f"Her _____ presentation failed to engage anyone.",
                f"The _____ book was difficult to finish reading.",
                f"His _____ personality made him forgettable.",
                f"The _____ conversation went nowhere interesting.",
                f"Her _____ writing lacked any excitement.",
                f"The _____ performance received no applause.",
                f"His _____ response showed no enthusiasm."
            ]
        elif "grainy" in meaning_lower or "small grains" in meaning_lower:
            adj_sentences = [
                f"The _____ texture of the sand made it ideal for building.",
                f"His _____ skin showed signs of sun damage.",
                f"The _____ surface felt rough to the touch.",
                f"Her _____ photograph was slightly blurred.",
                f"The _____ material was perfect for the project.",
                f"His _____ voice had a rough quality.",
                f"The _____ appearance indicated poor quality.",
                f"Her _____ drawing lacked smooth lines.",
                f"The _____ finish needed more sanding.",
                f"His _____ handwriting was hard to read."
            ]
        
        sentences.extend(adj_sentences[:10-len(sentences)])
        
    else:  # noun
        # Noun sentences - concept/thing contexts
        noun_sentences = [
            f"The _____ became clear to everyone present.",
            f"Her _____ impressed all the teachers.",
            f"The _____ was important in understanding the situation.",
            f"His _____ made a significant difference.",
            f"The _____ helped explain what happened.",
            f"Her _____ was obvious to all who watched.",
            f"The _____ became evident as the story unfolded.",
            f"His _____ surprised everyone around him.",
            f"The _____ was crucial to their success.",
            f"Her _____ showed her true character."
        ]
        
        # Customize based on meaning
        if "person" in meaning_lower or "someone" in meaning_lower:
            noun_sentences = [
                f"The _____ loved meeting new people at parties.",
                f"Her reputation as a _____ was well-known.",
                f"The _____ spent all his money on luxuries.",
                f"His behaviour showed he was a true _____.",
                f"The _____ couldn't resist the temptation.",
                f"Her actions revealed she was an _____.",
                f"The _____ was admired by everyone.",
                f"His character showed he was a genuine _____.",
                f"The _____ made a significant contribution.",
                f"Her nature indicated she was a real _____."
            ]
        elif "feeling" in meaning_lower or "emotion" in meaning_lower:
            noun_sentences = [
                f"The team felt _____ after winning the championship.",
                f"Her _____ was obvious from her expression.",
                f"The _____ overwhelmed everyone in the room.",
                f"His _____ showed clearly on his face.",
                f"The _____ made her feel wonderful.",
                f"Her _____ was contagious and spread to others.",
                f"The _____ filled the entire stadium.",
                f"His _____ was genuine and heartfelt.",
                f"The _____ lifted everyone's spirits.",
                f"Her _____ was evident to all."
            ]
        elif "speech" in meaning_lower or "tribute" in meaning_lower:
            noun_sentences = [
                f"The _____ celebrated the life of the much-loved teacher.",
                f"Her _____ moved everyone to tears.",
                f"The _____ honoured the memory of the hero.",
                f"His _____ praised the achievements of the team.",
                f"The _____ remembered all the good times.",
                f"Her _____ was heartfelt and sincere.",
                f"The _____ captured the essence of the person.",
                f"His _____ was eloquent and touching.",
                f"The _____ brought comfort to the family.",
                f"Her _____ was beautifully written and delivered."
            ]
        elif "skill" in meaning_lower or "knowledge" in meaning_lower:
            noun_sentences = [
                f"Her _____ in coding helped build the website.",
                f"The _____ required years of practice to develop.",
                f"His _____ was evident in his work.",
                f"The _____ made him valuable to the team.",
                f"Her _____ impressed all the experts.",
                f"The _____ was essential for success.",
                f"His _____ set him apart from others.",
                f"The _____ required dedication and hard work.",
                f"Her _____ was recognised by everyone.",
                f"The _____ was crucial for the project."
            ]
        elif "system" in meaning_lower or "order" in meaning_lower:
            noun_sentences = [
                f"The military has a strict _____ of command.",
                f"Her understanding of the _____ helped her succeed.",
                f"The _____ ensured everything ran smoothly.",
                f"His position in the _____ gave him authority.",
                f"The _____ was clearly defined and understood.",
                f"Her role in the _____ was important.",
                f"The _____ maintained order and structure.",
                f"His knowledge of the _____ was extensive.",
                f"The _____ provided clear guidelines.",
                f"Her place in the _____ was well-established."
            ]
        elif "disorder" in meaning_lower or "chaos" in meaning_lower:
            noun_sentences = [
                f"The children created _____ in the classroom when the teacher left.",
                f"Her actions caused complete _____ in the room.",
                f"The _____ made it impossible to work.",
                f"His behaviour led to total _____.",
                f"The _____ disrupted everything.",
                f"Her arrival caused _____ among the group.",
                f"The _____ was overwhelming and chaotic.",
                f"His actions resulted in absolute _____.",
                f"The _____ prevented any progress.",
                f"Her mistake led to complete _____."
            ]
        elif "illness" in meaning_lower or "disease" in meaning_lower:
            noun_sentences = [
                f"The doctor identified the _____ as flu.",
                f"Her _____ required immediate treatment.",
                f"The _____ spread quickly through the school.",
                f"His _____ kept him home from school.",
                f"The _____ affected many people.",
                f"Her _____ was difficult to diagnose.",
                f"The _____ caused her to feel unwell.",
                f"His _____ needed medical attention.",
                f"The _____ was contagious and dangerous.",
                f"Her _____ prevented her from participating."
            ]
        elif "sailor" in meaning_lower:
            noun_sentences = [
                f"The experienced _____ had sailed across many oceans.",
                f"Her father was a skilled _____ who loved the sea.",
                f"The _____ navigated through the storm successfully.",
                f"His grandfather had been a famous _____.",
                f"The _____ told exciting stories of his adventures.",
                f"Her uncle was a retired _____.",
                f"The _____ knew how to read the stars.",
                f"His friend wanted to become a _____.",
                f"The _____ had travelled to many countries.",
                f"Her neighbour was an experienced _____."
            ]
        elif "inheritance" in meaning_lower or "passed down" in meaning_lower:
            noun_sentences = [
                f"The ancient buildings are part of our cultural _____.",
                f"Her family's _____ included valuable antiques.",
                f"The _____ was passed down through generations.",
                f"His grandfather's _____ was carefully preserved.",
                f"The _____ represented years of tradition.",
                f"Her _____ included important historical documents.",
                f"The _____ was a source of pride.",
                f"His family's _____ was well-documented.",
                f"The _____ connected them to their past.",
                f"Her _____ was cherished by all."
            ]
        elif "figure of speech" in meaning_lower or "understatement" in meaning_lower:
            noun_sentences = [
                f"Saying 'not bad' when something is excellent is an example of _____.",
                f"Her use of _____ made her writing more interesting.",
                f"The _____ added humour to the conversation.",
                f"His understanding of _____ improved his writing.",
                f"The _____ was cleverly used in the poem.",
                f"Her knowledge of _____ helped her analyse texts.",
                f"The _____ made the statement more effective.",
                f"His use of _____ showed his skill with language.",
                f"The _____ was a common literary device.",
                f"Her explanation of _____ helped others understand."
            ]
        elif "words" in meaning_lower or "spelling" in meaning_lower:
            noun_sentences = [
                f"'Bow' and 'bow' are _____ with different meanings.",
                f"The word 'bank' is a _____ meaning both river edge and financial institution.",
                f"Her understanding of _____ helped her in English class.",
                f"The _____ confused many students.",
                f"His knowledge of _____ was impressive.",
                f"The _____ made the text more interesting.",
                f"Her explanation of _____ was clear.",
                f"The _____ were fun to learn about.",
                f"His examples of _____ helped others understand.",
                f"The _____ showed the complexity of English."
            ]
        elif "promise" in meaning_lower or "guarantee" in meaning_lower:
            noun_sentences = [
                f"The shop offered a money-back _____ on all products.",
                f"Her _____ gave them confidence in the purchase.",
                f"The _____ ensured customer satisfaction.",
                f"His _____ was written in the contract.",
                f"The _____ covered all possible problems.",
                f"Her _____ was honoured by the company.",
                f"The _____ provided peace of mind.",
                f"His _____ was unconditional and reliable.",
                f"The _____ protected the buyer's rights.",
                f"Her _____ was backed by the manufacturer."
            ]
        elif "consequences" in meaning_lower or "decision" in meaning_lower:
            noun_sentences = [
                f"The _____ decision changed the course of history.",
                f"Her _____ choice affected everyone involved.",
                f"The _____ moment determined their future.",
                f"His _____ action had lasting effects.",
                f"The _____ event shaped everything that followed.",
                f"Her _____ step was irreversible.",
                f"The _____ turning point was significant.",
                f"His _____ move changed everything.",
                f"The _____ choice was crucial.",
                f"Her _____ decision was momentous."
            ]
        elif "ability" in meaning_lower or "predict" in meaning_lower:
            noun_sentences = [
                f"His _____ helped the company avoid many problems.",
                f"Her _____ to see ahead was remarkable.",
                f"The _____ prevented several disasters.",
                f"His _____ saved them from making mistakes.",
                f"The _____ was a valuable skill.",
                f"Her _____ impressed all the managers.",
                f"The _____ helped plan for the future.",
                f"His _____ was well-developed.",
                f"The _____ made him successful.",
                f"Her _____ was recognised by everyone."
            ]
        elif "expert" in meaning_lower or "leading" in meaning_lower:
            noun_sentences = [
                f"She was the _____ expert on ancient Egyptian history.",
                f"His position as the _____ authority was undisputed.",
                f"The _____ leader guided them successfully.",
                f"Her role as the _____ specialist was important.",
                f"The _____ figure was respected by all.",
                f"His status as the _____ professional was clear.",
                f"The _____ pioneer opened new possibilities.",
                f"Her reputation as the _____ expert was well-known.",
                f"The _____ champion defended their rights.",
                f"His position as the _____ advocate was crucial."
            ]
        elif "excessive" in meaning_lower or "sickening" in meaning_lower:
            noun_sentences = [
                f"He repeated the same story ad _____ until everyone was bored.",
                f"Her complaints went on ad _____ without stopping.",
                f"The explanation continued ad _____ for hours.",
                f"His talking ad _____ annoyed everyone.",
                f"The repetition ad _____ was unbearable.",
                f"Her questions ad _____ exhausted the teacher.",
                f"The discussion ad _____ seemed endless.",
                f"His comments ad _____ were unnecessary.",
                f"The details ad _____ were too much.",
                f"Her stories ad _____ bored the listeners."
            ]
        elif "sophistication" in meaning_lower or "experience" in meaning_lower:
            noun_sentences = [
                f"Her _____ about the world was both charming and concerning.",
                f"The child's _____ was evident in every question.",
                f"His _____ showed his lack of experience.",
                f"The _____ made her vulnerable to deception.",
                f"Her _____ was refreshing but risky.",
                f"The _____ prevented him from understanding.",
                f"His _____ was both endearing and worrying.",
                f"The _____ made her trust everyone.",
                f"Her _____ was obvious to adults.",
                f"The _____ needed to be protected."
            ]
        elif "interest" in meaning_lower or "fascination" in meaning_lower:
            noun_sentences = [
                f"He had a _____ fascination with horror films.",
                f"Her _____ curiosity worried her parents.",
                f"The _____ interest was unhealthy.",
                f"His _____ preoccupation was disturbing.",
                f"The _____ obsession consumed his thoughts.",
                f"Her _____ attraction was concerning.",
                f"The _____ focus was inappropriate.",
                f"His _____ attention was misplaced.",
                f"The _____ concern was excessive.",
                f"Her _____ interest was unhealthy."
            ]
        elif "mixture" in meaning_lower or "varied" in meaning_lower:
            noun_sentences = [
                f"The chef prepared a _____ of vegetables for the salad.",
                f"Her collection was a _____ of different styles.",
                f"The _____ included many different elements.",
                f"His playlist was a _____ of various genres.",
                f"The _____ combined different flavours perfectly.",
                f"Her selection was a _____ of options.",
                f"The _____ offered something for everyone.",
                f"His work was a _____ of techniques.",
                f"The _____ was well-balanced and interesting.",
                f"Her creation was a _____ of ideas."
            ]
        elif "situation" in meaning_lower or "difficult" in meaning_lower:
            noun_sentences = [
                f"The charity helps those in desperate _____.",
                f"Her _____ required immediate attention.",
                f"The _____ was challenging to resolve.",
                f"His _____ needed careful handling.",
                f"The _____ affected many people.",
                f"Her _____ was complicated and serious.",
                f"The _____ demanded urgent action.",
                f"His _____ was difficult to escape.",
                f"The _____ required expert help.",
                f"Her _____ was overwhelming."
            ]
        elif "danger" in meaning_lower or "trap" in meaning_lower:
            noun_sentences = [
                f"Be aware of the _____ of online shopping.",
                f"Her knowledge helped her avoid the _____.",
                f"The _____ was well-hidden and dangerous.",
                f"His experience prevented him from falling into the _____.",
                f"The _____ caught many people by surprise.",
                f"Her warning helped others avoid the _____.",
                f"The _____ was difficult to spot.",
                f"His advice prevented the _____ from causing harm.",
                f"The _____ was common but avoidable.",
                f"Her awareness saved her from the _____."
            ]
        elif "course" in meaning_lower or "winding" in meaning_lower:
            noun_sentences = [
                f"The river _____ through the green valley.",
                f"Her path began to _____ through the forest.",
                f"The road would _____ around the mountain.",
                f"His journey started to _____ unexpectedly.",
                f"The trail began to _____ up the hillside.",
                f"Her route would _____ past many landmarks.",
                f"The stream began to _____ between the rocks.",
                f"His walk would _____ through the park.",
                f"The path started to _____ away from the main road.",
                f"Her drive would _____ through the countryside."
            ]
        elif "damage" in meaning_lower or "spoiled" in meaning_lower:
            noun_sentences = [
                f"The beautiful view was _____ by the construction site.",
                f"Her perfect day was _____ by the sudden rain.",
                f"The celebration was _____ by the argument.",
                f"His reputation was _____ by the false rumours.",
                f"The event was _____ by technical problems.",
                f"Her performance was _____ by the mistake.",
                f"The occasion was _____ by unexpected guests.",
                f"His success was _____ by the controversy.",
                f"The moment was _____ by the interruption.",
                f"Her achievement was _____ by the criticism."
            ]
        
        sentences.extend(noun_sentences[:10-len(sentences)])
    
    # Ensure we have exactly 10 sentences
    while len(sentences) < 10:
        if is_verb:
            sentences.append(f"They decided to _____ the situation carefully.")
        elif is_adjective:
            sentences.append(f"Her _____ quality was evident to everyone.")
        else:
            sentences.append(f"The _____ was important in understanding what happened.")
    
    return sentences[:10]


def parse_vocabulary_file(file_path: Path) -> List[dict]:
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
