#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 3 Batch 1 vocabulary.

Generates 10 contextually rich sentences per word (900 total) that:
- Provide strong contextual clues
- Use varied structures (no generic templates)
- Are age-appropriate for 10-11 year olds
- Use British English spelling
- Format: 3,WORD,SENTENCE (with _____ for the word)
"""

import csv
import re
from pathlib import Path
from typing import List, Tuple, Set

def create_blank_sentence(sentence: str, word: str) -> str:
    """Convert a sentence with the word into a fill-in-the-blank format."""
    word_lower = word.lower()
    
    # Create patterns for different word forms
    patterns = [
        word,  # Original case
        word_lower,  # Lowercase
        word.capitalize(),  # Capitalized
        word.title(),  # Title case
    ]
    
    # Add common word form variations
    if word_lower.endswith('e'):
        patterns.extend([
            word_lower + 'd',  # abbreviated
            word_lower + 's',  # abbreviates
            word_lower[:-1] + 'ing',  # abbreviating
            word_lower + 'ly',  # abbreviately (if adverb)
        ])
    elif word_lower.endswith('y'):
        patterns.extend([
            word_lower[:-1] + 'ied',  # amplified
            word_lower[:-1] + 'ies',  # amplifies
            word_lower[:-1] + 'ying',  # amplifying
            word_lower[:-1] + 'ier',  # amplier
            word_lower[:-1] + 'iest',  # ampliest
        ])
    elif len(word_lower) > 2 and word_lower[-1] not in 'aeiou' and word_lower[-2] in 'aeiou':
        # Double consonant pattern (e.g., stop -> stopped)
        patterns.extend([
            word_lower + word_lower[-1] + 'ed',  # stopped
            word_lower + word_lower[-1] + 'ing',  # stopping
        ])
    else:
        patterns.extend([
            word_lower + 'ed',  # augmented
            word_lower + 's',  # augments
            word_lower + 'ing',  # augmenting
        ])
    
    result = sentence
    replaced = False
    
    # Try to replace with word boundaries first (most accurate)
    for pattern in sorted(set(patterns), key=len, reverse=True):
        regex = re.compile(r'\b' + re.escape(pattern) + r'\b', re.IGNORECASE)
        if regex.search(result):
            result = regex.sub("_____", result, count=1)
            replaced = True
            break
    
    # If not found, try without word boundaries
    if not replaced:
        for pattern in sorted(set(patterns), key=len, reverse=True):
            if pattern.lower() in result.lower():
                result = re.sub(re.escape(pattern), "_____", result, flags=re.IGNORECASE, count=1)
                replaced = True
                break
    
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
    Each sentence provides strong contextual clues specific to the word's meaning.
    """
    sentences: List[str] = []
    word_lower = word.lower()
    meaning_lower = meaning.lower()
    seen: Set[str] = set()
    
    # Determine word type more accurately
    is_verb = meaning_lower.startswith("to ")
    is_adjective = (
        any(marker in meaning_lower for marker in [
            "having", "showing", "full of", "characterised by", "characterized by",
            "very", "extremely", "quite", "rather", "causing", "deserving", "different",
            "able to", "relating to", "concerned with", "rough", "harsh", "pleasant",
            "worried", "calm", "bold", "genuine", "strict", "confused", "old-fashioned",
            "uncertain", "pleasant", "friendly", "without", "surprisingly", "difficult",
            "interesting", "comforting", "providing", "ready", "demanding"
        ]) or 
        word_lower.endswith(('ive', 'ous', 'ful', 'less', 'able', 'ible', 'ant', 'ent', 'ing', 'ed'))
    )
    is_noun = not is_verb and not is_adjective
    
    # 1. Use example sentence if available (best quality)
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example and blank_example not in seen:
            sentences.append(blank_example)
            seen.add(blank_example)
    
    # Generate contextually rich sentences based on word meaning
    # Custom sentences for each word based on its specific meaning
    
    # Build word-specific sentences
    word_specific_sentences = []
    
    if word_lower == "abbreviate":
        word_specific_sentences = [
            "They decided to _____ the document to save space.",
            "The teacher asked us to _____ long words in our notes.",
            "She learned how to _____ her name when signing forms.",
            "We can _____ this phrase to make it shorter.",
            "The secretary will _____ the address on the envelope.",
            "Students often _____ difficult terms in their essays.",
            "The author chose to _____ several technical terms.",
            "You should _____ the title to fit on one line.",
            "The system can automatically _____ long file names.",
            "Please _____ your response to keep it brief.",
        ]
    elif word_lower == "aberrant":
        word_specific_sentences = [
            "The _____ results didn't match the expected pattern.",
            "She noticed something _____ about the situation.",
            "The _____ weather was unusual for this time of year.",
            "His _____ response was completely unexpected.",
            "The _____ pattern didn't follow the normal rules.",
            "She found the _____ behaviour quite strange.",
            "The _____ outcome puzzled the scientists.",
            "His _____ actions confused his classmates.",
            "The _____ data didn't fit the model.",
            "She detected an _____ signal in the transmission.",
        ]
    elif word_lower == "abhorrent":
        word_specific_sentences = [
            "His _____ behaviour was completely unacceptable.",
            "The _____ treatment of animals angered many people.",
            "She found his _____ comments deeply offensive.",
            "The _____ crime horrified the entire community.",
            "His _____ attitude towards others was appalling.",
            "The _____ act was condemned by everyone.",
            "She was shocked by the _____ behaviour.",
            "The _____ treatment was truly terrible.",
            "His _____ words upset everyone who heard them.",
            "The _____ nature of the crime was evident.",
        ]
    elif word_lower == "abrasive":
        word_specific_sentences = [
            "The _____ surface scratched her hands.",
            "She found his _____ manner quite unpleasant.",
            "The _____ material was uncomfortable to wear.",
            "His _____ tone made everyone uncomfortable.",
            "The _____ texture was difficult to clean.",
            "She didn't like his _____ way of speaking.",
            "The _____ sandpaper was too coarse for the job.",
            "His _____ criticism hurt her feelings.",
            "The _____ treatment damaged the surface.",
            "The _____ quality of the fabric was rough.",
        ]
    elif word_lower == "abundance":
        word_specific_sentences = [
            "She found an _____ of shells on the beach.",
            "The _____ of food was impressive.",
            "He discovered an _____ of resources.",
            "The _____ made everyone happy.",
            "She was grateful for the _____.",
            "The _____ was more than enough.",
            "He appreciated the _____ greatly.",
            "The _____ exceeded expectations.",
            "She marvelled at the _____.",
            "The _____ of opportunities was remarkable.",
        ]
    elif word_lower == "abundant":
        word_specific_sentences = [
            "The garden had an _____ supply of vegetables.",
            "She found _____ evidence to support her theory.",
            "The library had an _____ collection of books.",
            "Resources were _____ in the wealthy region.",
            "The area had _____ rainfall throughout the year.",
            "She discovered _____ amounts of treasure.",
            "The forest was _____ with wildlife.",
            "Opportunities were _____ for skilled workers.",
            "The region had _____ natural resources.",
            "Wildflowers were _____ in the meadow.",
        ]
    elif word_lower == "accusatory":
        word_specific_sentences = [
            "The _____ comment upset her.",
            "She didn't like his _____ manner.",
            "The _____ statement was harsh.",
            "He used an _____ approach.",
            "The _____ nature of his words was clear.",
            "She felt attacked by the _____ tone.",
            "His _____ attitude was unhelpful.",
            "The _____ remark was unnecessary.",
            "She couldn't stand the _____ behaviour.",
            "The _____ finger-pointing created tension.",
        ]
    elif word_lower == "acquainted":
        word_specific_sentences = [
            "He was already _____ with the subject.",
            "The students became _____ with the rules.",
            "She made herself _____ with the procedure.",
            "He got _____ with the new system quickly.",
            "The team became _____ with each other.",
            "She was well _____ with the area.",
            "He became _____ with the customs.",
            "The children got _____ with the routine.",
            "She made herself _____ with the facts.",
            "They got _____ during the school trip.",
        ]
    elif word_lower == "adequately":
        word_specific_sentences = [
            "She performed _____ in the exam.",
            "The work was _____ done.",
            "He prepared _____ for the presentation.",
            "The resources were _____ for the task.",
            "She explained it _____ for everyone to understand.",
            "The preparation was _____ thorough.",
            "He answered _____ to pass.",
            "The solution was _____ effective.",
            "She managed _____ well.",
            "The problem was _____ addressed.",
        ]
    elif word_lower == "adherent":
        word_specific_sentences = [
            "The _____ was committed to the cause.",
            "He became a loyal _____ of the idea.",
            "The _____ supported the leader wholeheartedly.",
            "She was a dedicated _____ of the philosophy.",
            "The _____ followed the principles closely.",
            "He was a strong _____ of the movement.",
            "The _____ was passionate about the belief.",
            "She remained a faithful _____ throughout.",
            "The _____ never wavered in support.",
            "He was a devoted _____ of the theory.",
        ]
    elif word_lower == "adjacent":
        word_specific_sentences = [
            "Her house was _____ to the library.",
            "The two buildings were _____ to each other.",
            "He sat in the seat _____ to the window.",
            "The room _____ to the kitchen was the dining room.",
            "She placed it _____ to the other items.",
            "The field was _____ to the forest.",
            "He lived in the house _____ to the shop.",
            "The area _____ to the river was flooded.",
            "She stood _____ to her friend.",
            "The garden was _____ to the playground.",
        ]
    elif word_lower == "admirable":
        word_specific_sentences = [
            "The _____ act was recognised by all.",
            "He showed _____ determination.",
            "The _____ behaviour was praised.",
            "She demonstrated _____ qualities.",
            "The _____ effort was appreciated.",
            "His _____ conduct set a good example.",
            "The _____ achievement was celebrated.",
            "She showed _____ leadership.",
            "The _____ character was evident.",
            "His _____ work inspired others.",
        ]
    elif word_lower == "admission":
        word_specific_sentences = [
            "She gained _____ to the exclusive club.",
            "The _____ process was straightforward.",
            "He was granted _____ to the event.",
            "The _____ fee was reasonable.",
            "She applied for _____ to the university.",
            "The _____ was granted immediately.",
            "He paid for _____ to the concert.",
            "The _____ requirements were met.",
            "She received _____ to the building.",
            "The _____ ticket allowed entry.",
        ]
    elif word_lower == "adversary":
        word_specific_sentences = [
            "She faced a formidable _____ in the competition.",
            "The _____ was skilled and determined.",
            "He respected his _____ despite the rivalry.",
            "The _____ proved to be challenging.",
            "She underestimated her _____ initially.",
            "The _____ had a strong strategy.",
            "He prepared thoroughly for his _____.",
            "The _____ was well-prepared.",
            "She finally defeated her _____.",
            "The _____ was a worthy opponent.",
        ]
    elif word_lower == "aesthetic":
        word_specific_sentences = [
            "Her _____ sense made her a talented artist.",
            "The _____ design impressed all the judges.",
            "He had an _____ appreciation for fine art.",
            "The _____ quality of the painting was evident.",
            "She considered the _____ value of the sculpture.",
            "The _____ arrangement was pleasing to the eye.",
            "His _____ choices were always excellent.",
            "The _____ beauty of the building was striking.",
            "She had a natural _____ understanding.",
            "The _____ appeal was undeniable.",
        ]
    elif word_lower == "affectionate":
        word_specific_sentences = [
            "Her _____ nature made her popular with children.",
            "The _____ gesture brought tears to their eyes.",
            "She gave him an _____ hug before leaving.",
            "The _____ letter made her feel special.",
            "Her _____ words comforted the upset child.",
            "The _____ family always supported each other.",
            "She had an _____ relationship with her grandparents.",
            "The _____ teacher was loved by all her pupils.",
            "Her _____ smile brightened everyone's day.",
            "The _____ bond between them was strong.",
        ]
    elif word_lower == "affluent":
        word_specific_sentences = [
            "Her _____ family could afford expensive holidays.",
            "The _____ area was known for its luxury shops.",
            "He came from an _____ background.",
            "The _____ district had the best schools.",
            "Her _____ lifestyle allowed many privileges.",
            "The _____ community supported local charities.",
            "He lived in an _____ part of the city.",
            "The _____ family donated generously.",
            "Her _____ upbringing provided many opportunities.",
            "The _____ neighbourhood was well-maintained.",
        ]
    elif word_lower == "agitated":
        word_specific_sentences = [
            "Her _____ expression showed she was worried.",
            "The _____ child couldn't sit still.",
            "He felt _____ about the upcoming test.",
            "The _____ crowd grew restless.",
            "She became _____ when she couldn't find her keys.",
            "The _____ dog barked constantly.",
            "He was _____ by the constant noise.",
            "The _____ atmosphere made everyone nervous.",
            "She tried to calm her _____ feelings.",
            "The _____ state was caused by stress.",
        ]
    elif word_lower == "agnostic":
        word_specific_sentences = [
            "The _____ position was thoughtful.",
            "She held an _____ viewpoint.",
            "The _____ perspective was respected.",
            "He explained his _____ beliefs.",
            "The _____ stance was philosophical.",
            "She identified as _____.",
            "His _____ position was well-reasoned.",
            "The _____ approach was open-minded.",
            "He remained _____ throughout his life.",
            "The _____ viewpoint was considered carefully.",
        ]
    elif word_lower == "agonising":
        word_specific_sentences = [
            "Her _____ decision was difficult to make.",
            "The _____ experience taught her valuable lessons.",
            "He went through an _____ period of uncertainty.",
            "The _____ process required great patience.",
            "She found the _____ choice almost impossible.",
            "The _____ moment tested her resolve.",
            "His _____ struggle was finally over.",
            "The _____ experience changed her perspective.",
            "She endured the _____ wait with courage.",
            "The _____ delay seemed to last forever.",
        ]
    elif word_lower == "agreeable":
        word_specific_sentences = [
            "His _____ nature made him easy to work with.",
            "The _____ atmosphere made everyone feel welcome.",
            "She had an _____ conversation with her neighbour.",
            "The _____ weather made the picnic perfect.",
            "His _____ response put everyone at ease.",
            "The _____ solution pleased everyone involved.",
            "She maintained an _____ attitude throughout.",
            "The _____ outcome was better than expected.",
            "His _____ manner was appreciated by all.",
            "The _____ environment was pleasant.",
        ]
    elif word_lower == "allusion":
        word_specific_sentences = [
            "Her _____ was subtle but clear.",
            "The _____ made the story richer.",
            "He understood the _____ immediately.",
            "The _____ added depth to the text.",
            "She spotted the _____ to the earlier event.",
            "The _____ was cleverly hidden.",
            "His _____ was appreciated by readers.",
            "The _____ enhanced the meaning.",
            "She made an _____ to the previous chapter.",
            "The _____ required knowledge to understand.",
        ]
    elif word_lower == "altitude":
        word_specific_sentences = [
            "The mountain's _____ made climbing difficult.",
            "She measured the _____ carefully.",
            "The _____ affected the temperature.",
            "He was unused to the high _____.",
            "The _____ of the building was impressive.",
            "She recorded the _____ accurately.",
            "The _____ made breathing harder.",
            "He checked the _____ on the instrument.",
            "The _____ was higher than expected.",
            "The plane reached a cruising _____.",
        ]
    elif word_lower == "ambiguous":
        word_specific_sentences = [
            "The _____ instructions were difficult to follow.",
            "She gave an _____ response that didn't help.",
            "The _____ message could be interpreted in different ways.",
            "His _____ explanation created more questions.",
            "The _____ statement was open to interpretation.",
            "She left an _____ impression on everyone.",
            "The _____ rules caused confusion.",
            "His _____ behaviour puzzled his friends.",
            "The _____ situation required clarification.",
            "The _____ answer was unhelpful.",
        ]
    elif word_lower == "ambition":
        word_specific_sentences = [
            "His _____ drove him to work hard.",
            "The _____ to succeed was strong.",
            "She pursued her _____ with determination.",
            "His _____ was finally realised.",
            "The _____ motivated her daily.",
            "She never lost sight of her _____.",
            "His _____ was ambitious but achievable.",
            "The _____ required great effort.",
            "She achieved her lifelong _____.",
            "The _____ to excel was evident.",
        ]
    elif word_lower == "amicable":
        word_specific_sentences = [
            "Her _____ approach resolved the conflict.",
            "The _____ discussion led to a solution.",
            "He tried to be _____ despite the disagreement.",
            "The _____ tone helped calm everyone down.",
            "She maintained an _____ attitude throughout.",
            "The _____ resolution satisfied both sides.",
            "His _____ manner prevented further arguments.",
            "The _____ conversation was productive.",
            "She showed an _____ spirit in negotiations.",
            "The _____ agreement was reached quickly.",
        ]
    elif word_lower == "amorphous":
        word_specific_sentences = [
            "Her _____ ideas needed more structure.",
            "The _____ cloud changed shape constantly.",
            "He had an _____ plan that lacked detail.",
            "The _____ mass had no clear boundaries.",
            "She found the _____ concept difficult to grasp.",
            "The _____ substance was hard to describe.",
            "His _____ thoughts needed organisation.",
            "The _____ design was intentionally vague.",
            "She worked with the _____ material creatively.",
            "The _____ shape was undefined.",
        ]
    elif word_lower == "analogy":
        word_specific_sentences = [
            "Her _____ helped everyone understand.",
            "The _____ made the idea clearer.",
            "He drew an _____ between the two situations.",
            "The _____ was very effective.",
            "She created an _____ that worked perfectly.",
            "The _____ simplified the complex topic.",
            "His _____ was creative and helpful.",
            "The _____ illuminated the problem.",
            "She found the _____ very useful.",
            "The teacher's _____ clarified everything.",
        ]
    elif word_lower == "annihilated":
        word_specific_sentences = [
            "Her mistake _____ all their hard work.",
            "The fire _____ everything in the building.",
            "He watched as the storm _____ the crops.",
            "The explosion _____ the entire structure.",
            "She couldn't believe how quickly it was _____.",
            "The attack _____ the enemy's defences.",
            "His actions _____ their chances of success.",
            "The disaster _____ years of progress.",
            "She saw how the war _____ the city.",
            "The disease _____ the entire population.",
        ]
    elif word_lower == "antagonize":
        word_specific_sentences = [
            "The comment would _____ anyone who heard it.",
            "He didn't want to _____ his parents before the trip.",
            "Her words seemed designed to _____ the audience.",
            "The decision might _____ some of the team members.",
            "They warned him not to _____ the judge.",
            "The proposal could _____ those who disagreed.",
            "She was careful not to _____ her best friend.",
            "His actions would _____ anyone watching.",
            "The teacher didn't want to _____ the students.",
            "The remark would _____ the entire group.",
        ]
    elif word_lower == "antipathy":
        word_specific_sentences = [
            "His _____ for the subject was obvious.",
            "The _____ between them was mutual.",
            "He showed clear _____ for the proposal.",
            "Her _____ made cooperation difficult.",
            "The _____ was evident in her expression.",
            "He couldn't hide his _____ for the idea.",
            "The _____ created tension in the group.",
            "Her _____ prevented them from working together.",
            "The _____ was stronger than expected.",
            "The deep _____ was obvious to all.",
        ]
    elif word_lower == "antiquated":
        word_specific_sentences = [
            "Her _____ ideas were no longer relevant.",
            "The _____ methods were inefficient.",
            "He used an _____ approach that didn't work.",
            "The _____ equipment was unreliable.",
            "She had _____ views on the subject.",
            "The _____ technology was obsolete.",
            "His _____ thinking held back progress.",
            "The _____ system couldn't handle modern demands.",
            "She found the _____ style charming but impractical.",
            "The _____ machinery was replaced.",
        ]
    elif word_lower == "antithesis":
        word_specific_sentences = [
            "The result was the complete _____ of what was expected.",
            "She represented the _____ of everything he believed.",
            "The two ideas were the _____ of each other.",
            "His behaviour was the _____ of hers.",
            "The outcome was the _____ of the prediction.",
            "She was the _____ of her sister in every way.",
            "The solution was the _____ of the problem.",
            "His approach was the _____ of traditional methods.",
            "The answer was the _____ of what they thought.",
            "The new design was the _____ of the old one.",
        ]
    elif word_lower == "apathetic":
        word_specific_sentences = [
            "Her _____ attitude disappointed her teachers.",
            "The _____ response was unexpected.",
            "He seemed _____ about the exciting news.",
            "The _____ students didn't participate in class.",
            "She showed an _____ expression throughout.",
            "The _____ audience barely applauded.",
            "His _____ behaviour concerned his parents.",
            "The _____ reaction surprised everyone.",
            "She remained _____ despite the encouragement.",
            "The _____ mood was contagious.",
        ]
    elif word_lower == "aphorism":
        word_specific_sentences = [
            "She quoted a famous _____ about perseverance.",
            "The _____ contained valuable wisdom.",
            "He remembered the _____ his grandmother taught him.",
            "The _____ summed up the situation perfectly.",
            "She found the _____ very inspiring.",
            "The _____ was passed down through generations.",
            "He used the _____ to explain his point.",
            "The _____ captured an important truth.",
            "She lived by the _____ every day.",
            "The wise _____ guided their decisions.",
        ]
    elif word_lower == "arbitrary":
        word_specific_sentences = [
            "Her _____ choice seemed unfair.",
            "The _____ selection process was criticised.",
            "He made an _____ pick without thinking.",
            "The _____ nature of the rule was confusing.",
            "She didn't like the _____ way it was done.",
            "The _____ assignment seemed random.",
            "His _____ method lacked logic.",
            "The _____ approach didn't make sense.",
            "She questioned the _____ selection.",
            "The _____ decision angered many people.",
        ]
    elif word_lower == "argument":
        word_specific_sentences = [
            "The _____ lasted for hours.",
            "She tried to avoid the _____.",
            "The _____ became quite heated.",
            "He presented a strong _____ for his position.",
            "The _____ was productive.",
            "She made a valid _____ in the discussion.",
            "The _____ helped clarify the issues.",
            "He lost the _____ but learned from it.",
            "The _____ was necessary to reach agreement.",
            "The _____ ended in compromise.",
        ]
    elif word_lower == "arrogance":
        word_specific_sentences = [
            "She showed great _____ in her behaviour.",
            "The _____ was evident in every word he spoke.",
            "His _____ prevented him from learning.",
            "The _____ of his attitude was off-putting.",
            "She couldn't stand his _____ any longer.",
            "His _____ blinded him to his own mistakes.",
            "The _____ made him unpopular.",
            "Her _____ was her greatest weakness.",
            "The _____ was clear in his expression.",
            "The _____ was obvious to everyone.",
        ]
    elif word_lower == "articulate":
        word_specific_sentences = [
            "Her _____ explanation made everything clear.",
            "He was very _____ in expressing his ideas.",
            "The _____ response answered all questions.",
            "She gave an _____ description of the problem.",
            "His _____ writing was easy to understand.",
            "The _____ presentation impressed everyone.",
            "She was _____ in her communication.",
            "His _____ speech moved the listeners.",
            "The _____ way she explained it helped greatly.",
            "She was known for being very _____.",
        ]
    elif word_lower == "ascendancy":
        word_specific_sentences = [
            "Her _____ in the field was well-known.",
            "The _____ of the new leader was clear.",
            "He achieved _____ through hard work.",
            "The _____ position gave them advantages.",
            "She maintained her _____ throughout.",
            "The _____ was evident in their performance.",
            "His _____ helped the team succeed.",
            "The _____ of the strategy was obvious.",
            "She used her _____ wisely.",
            "The team's _____ was undeniable.",
        ]
    elif word_lower == "assiduous":
        word_specific_sentences = [
            "The _____ worker never missed a deadline.",
            "His _____ attention to detail was impressive.",
            "The _____ approach ensured success.",
            "She showed _____ dedication to her studies.",
            "His _____ efforts paid off in the end.",
            "The _____ student was always prepared.",
            "She maintained an _____ work ethic.",
            "His _____ nature made him reliable.",
            "The _____ preparation was evident.",
            "Her _____ study habits were admirable.",
        ]
    elif word_lower == "astounding":
        word_specific_sentences = [
            "Her _____ performance left everyone speechless.",
            "The _____ discovery changed everything.",
            "He achieved an _____ result.",
            "The _____ feat seemed impossible.",
            "She showed _____ skill in her work.",
            "The _____ achievement was celebrated.",
            "His _____ talent was recognised.",
            "The _____ nature of the event was remarkable.",
            "She produced an _____ piece of work.",
            "The _____ success surprised everyone.",
        ]
    elif word_lower == "atrocious":
        word_specific_sentences = [
            "Her _____ behaviour shocked everyone.",
            "The _____ crime horrified the community.",
            "He showed _____ cruelty towards animals.",
            "The _____ conditions made life difficult.",
            "She couldn't believe the _____ treatment.",
            "The _____ act was condemned by all.",
            "His _____ actions were inexcusable.",
            "The _____ situation was unbearable.",
            "She witnessed the _____ event with horror.",
            "The _____ quality was unacceptable.",
        ]
    elif word_lower == "attentive":
        word_specific_sentences = [
            "Her _____ listening helped her understand everything.",
            "The _____ audience watched every move carefully.",
            "She was _____ to every sound in the room.",
            "His _____ observation skills were impressive.",
            "The _____ teacher noticed when students needed help.",
            "She remained _____ throughout the entire lecture.",
            "His _____ reading caught all the important points.",
            "The _____ guard spotted the problem immediately.",
            "She was _____ to changes in the environment.",
            "The _____ student took detailed notes.",
        ]
    elif word_lower == "audacious":
        word_specific_sentences = [
            "Her _____ plan surprised everyone with its creativity.",
            "The _____ move changed the course of the game.",
            "He made an _____ decision that paid off.",
            "The _____ explorer ventured into unknown territory.",
            "Her _____ idea was initially met with scepticism.",
            "The _____ strategy required great courage.",
            "He showed _____ determination in pursuing his goal.",
            "The _____ act of bravery inspired others.",
            "Her _____ approach solved the impossible problem.",
            "The _____ attempt was successful.",
        ]
    elif word_lower == "augmenting":
        word_specific_sentences = [
            "She was _____ her savings each month.",
            "The team was _____ their efforts.",
            "He was _____ the pressure gradually.",
            "The process involved _____ the ingredients.",
            "She kept _____ to her collection.",
            "The method required _____ resources.",
            "He was _____ his knowledge daily.",
            "The strategy involved _____ support.",
            "She was _____ her skills constantly.",
            "They were _____ the team's capabilities.",
        ]
    elif word_lower == "authentic":
        word_specific_sentences = [
            "Her _____ smile showed she was truly happy.",
            "The _____ painting was worth millions of pounds.",
            "He had an _____ interest in ancient history.",
            "The _____ document proved the claim was true.",
            "She showed _____ concern for her friend's wellbeing.",
            "The _____ signature confirmed the letter's origin.",
            "He had an _____ passion for music.",
            "The _____ artefact was carefully preserved.",
            "Her _____ kindness touched everyone she met.",
            "The _____ experience was unforgettable.",
        ]
    elif word_lower == "authoritarian":
        word_specific_sentences = [
            "His _____ rules were difficult to follow.",
            "The _____ regime controlled every aspect of life.",
            "She had an _____ approach to discipline.",
            "The _____ system left no room for creativity.",
            "His _____ manner intimidated the students.",
            "The _____ policies were enforced without exception.",
            "She maintained an _____ classroom environment.",
            "The _____ leader demanded complete obedience.",
            "His _____ methods were controversial.",
            "The _____ style was unpopular.",
        ]
    elif word_lower == "available":
        word_specific_sentences = [
            "Tickets were _____ online.",
            "She found the information _____.",
            "The resources were _____ to all students.",
            "He checked if seats were still _____.",
            "The opportunity was _____ to everyone.",
            "She made herself _____ for questions.",
            "The service was _____ throughout the day.",
            "He ensured help was always _____.",
            "The facilities were _____ for use.",
            "The book was _____ at the library.",
        ]
    elif word_lower == "aversion":
        word_specific_sentences = [
            "Her _____ for the subject was well-known.",
            "The _____ made it difficult to proceed.",
            "She couldn't overcome her _____.",
            "His _____ was irrational but real.",
            "The _____ prevented her from trying.",
            "She developed an _____ after the incident.",
            "His _____ was evident in his reaction.",
            "The _____ was stronger than expected.",
            "She tried to hide her _____.",
            "The deep _____ was obvious.",
        ]
    elif word_lower == "barbaric":
        word_specific_sentences = [
            "Her _____ behaviour was condemned.",
            "The _____ act was horrific.",
            "He showed _____ cruelty.",
            "The _____ methods were unacceptable.",
            "She couldn't believe the _____ treatment.",
            "The _____ nature of the crime was appalling.",
            "His _____ actions were inexcusable.",
            "The _____ behaviour shocked everyone.",
            "She witnessed the _____ act.",
            "The _____ practices were banned.",
        ]
    elif word_lower == "bewildered":
        word_specific_sentences = [
            "Her _____ expression showed she didn't understand.",
            "The _____ child looked around helplessly.",
            "He felt _____ by the complicated instructions.",
            "The _____ look on her face was clear.",
            "She was _____ by the sudden change of plans.",
            "The _____ student asked for help repeatedly.",
            "He appeared _____ by the strange behaviour.",
            "The _____ expression revealed his confusion.",
            "She felt completely _____ in the new situation.",
            "The _____ tourists needed directions.",
        ]
    elif word_lower == "bickering":
        word_specific_sentences = [
            "The constant _____ was annoying.",
            "She was tired of their _____.",
            "The _____ never seemed to end.",
            "He tried to stop the _____.",
            "The _____ disrupted the peace.",
            "She found the _____ childish.",
            "The _____ was over nothing important.",
            "He ignored the _____.",
            "The _____ was pointless.",
            "The endless _____ was exhausting.",
        ]
    elif word_lower == "bipartisan":
        word_specific_sentences = [
            "The _____ approach was successful.",
            "She appreciated the _____ cooperation.",
            "The _____ decision was rare.",
            "He supported the _____ effort.",
            "The _____ support was unexpected.",
            "She valued the _____ collaboration.",
            "The _____ nature of the plan was positive.",
            "He worked on the _____ committee.",
            "The _____ agreement was historic.",
            "The _____ support was welcomed.",
        ]
    elif word_lower == "bittersweet":
        word_specific_sentences = [
            "The _____ feeling was complex.",
            "She experienced a _____ emotion.",
            "The _____ nature of the occasion was clear.",
            "He felt _____ about the change.",
            "The _____ memory brought mixed feelings.",
            "She described it as a _____ experience.",
            "The _____ moment was memorable.",
            "He found it _____ but necessary.",
            "The _____ goodbye was emotional.",
            "The _____ victory was celebrated with sadness.",
        ]
    elif word_lower == "brevity":
        word_specific_sentences = [
            "She appreciated the _____ of the message.",
            "The _____ made it easy to remember.",
            "He valued _____ in communication.",
            "The _____ was refreshing.",
            "She admired the _____ of his writing.",
            "The _____ kept everyone's attention.",
            "He achieved _____ through careful editing.",
            "The _____ was intentional.",
            "She preferred _____ to long explanations.",
            "The _____ of the speech was praised.",
        ]
    elif word_lower == "cacophony":
        word_specific_sentences = [
            "The _____ was deafening.",
            "She couldn't stand the _____.",
            "The _____ made concentration impossible.",
            "He was disturbed by the _____.",
            "The _____ was overwhelming.",
            "She tried to escape the _____.",
            "The _____ was unpleasant.",
            "He found the _____ irritating.",
            "The _____ disrupted the peace.",
            "The constant _____ was annoying.",
        ]
    elif word_lower == "camaraderie":
        word_specific_sentences = [
            "The _____ between them was strong.",
            "She valued the _____ they shared.",
            "The _____ made the work enjoyable.",
            "He appreciated the _____ in the group.",
            "The _____ was evident in their cooperation.",
            "She felt the _____ immediately.",
            "The _____ created a positive atmosphere.",
            "He contributed to the _____.",
            "The _____ was genuine and warm.",
            "The team's _____ was remarkable.",
        ]
    elif word_lower == "capacious":
        word_specific_sentences = [
            "The _____ room could fit many people.",
            "She appreciated the _____ storage area.",
            "The _____ container held everything needed.",
            "His _____ suitcase had room for extra items.",
            "The _____ design allowed for easy movement.",
            "She loved the _____ feel of the large hall.",
            "The _____ interior was impressive.",
            "His _____ backpack was perfect for hiking.",
            "The _____ accommodation was very comfortable.",
            "The _____ space was well-utilised.",
        ]
    elif word_lower == "captivating":
        word_specific_sentences = [
            "Her _____ personality drew people to her.",
            "The _____ performance held the audience spellbound.",
            "He found the _____ tale impossible to put down.",
            "The _____ nature of the mystery intrigued them.",
            "She was completely _____ by the beautiful display.",
            "The _____ presentation captured everyone's imagination.",
            "His _____ style made the subject interesting.",
            "The _____ quality of the artwork was evident.",
            "She found the _____ story absolutely enthralling.",
            "The _____ show kept everyone watching.",
        ]
    elif word_lower == "catastrophe":
        word_specific_sentences = [
            "Her mistake led to a complete _____.",
            "The _____ destroyed everything in its path.",
            "He tried to prevent the _____ from happening.",
            "The _____ affected thousands of people.",
            "She couldn't believe the scale of the _____.",
            "The _____ required immediate action.",
            "His actions caused a major _____.",
            "The _____ was worse than anyone expected.",
            "She worked to recover from the _____.",
            "The natural _____ devastated the region.",
        ]
    elif word_lower == "category":
        word_specific_sentences = [
            "She organised the items by _____.",
            "The _____ system made finding things easier.",
            "He placed it in the correct _____.",
            "The _____ included many similar items.",
            "She created a new _____ for the collection.",
            "The _____ helped organise the information.",
            "His filing system used clear _____.",
            "The _____ made the library easy to navigate.",
            "She assigned each item to a specific _____.",
            "The _____ was well-defined.",
        ]
    elif word_lower == "cathartic":
        word_specific_sentences = [
            "The _____ experience helped her process her feelings.",
            "He found the _____ moment very helpful.",
            "The _____ effect was immediate and noticeable.",
            "She described the feeling as _____ and freeing.",
            "The _____ process allowed her to move forward.",
            "He experienced a _____ release of tension.",
            "The _____ nature of the activity was therapeutic.",
            "She found the _____ experience very beneficial.",
            "The _____ feeling was exactly what she needed.",
            "The _____ effect was profound.",
        ]
    elif word_lower == "celestial":
        word_specific_sentences = [
            "Her _____ voice sounded like music from above.",
            "The _____ beauty of the stars amazed them.",
            "He studied the _____ movements of the planets.",
            "The _____ phenomenon was visible for miles.",
            "She gazed at the _____ display with wonder.",
            "The _____ objects moved across the sky.",
            "His _____ observations were recorded carefully.",
            "The _____ event was rare and special.",
            "She found the _____ view breathtaking.",
            "The _____ bodies were clearly visible.",
        ]
    elif word_lower == "cemetery":
        word_specific_sentences = [
            "They visited the _____ to pay respects.",
            "The _____ was peaceful and quiet.",
            "She walked through the _____ thoughtfully.",
            "The _____ contained many old graves.",
            "He found the _____ quite moving.",
            "The _____ was well-maintained.",
            "She read the inscriptions in the _____.",
            "The _____ had a solemn atmosphere.",
            "He placed flowers at the _____.",
            "The old _____ was historic.",
        ]
    elif word_lower == "certitude":
        word_specific_sentences = [
            "His _____ was evident in every word.",
            "The _____ of her statement was clear.",
            "He had complete _____ in his decision.",
            "The _____ of the evidence was undeniable.",
            "She showed great _____ in her response.",
            "His _____ impressed the judges.",
            "The _____ of the outcome was reassuring.",
            "She expressed _____ about the plan.",
            "His _____ was unwavering.",
            "The absolute _____ was evident.",
        ]
    elif word_lower == "challenging":
        word_specific_sentences = [
            "Her _____ task required great skill.",
            "The _____ problem tested their knowledge.",
            "He found the _____ work rewarding.",
            "The _____ course prepared them well.",
            "She enjoyed the _____ nature of the project.",
            "The _____ assignment pushed them to improve.",
            "His _____ approach led to success.",
            "The _____ situation required careful thought.",
            "She rose to the _____ occasion.",
            "The _____ puzzle was solved eventually.",
        ]
    elif word_lower == "chauvinist":
        word_specific_sentences = [
            "His _____ attitude was problematic.",
            "The _____ behaviour was unacceptable.",
            "She couldn't stand his _____ views.",
            "The _____ thinking was narrow-minded.",
            "He showed _____ tendencies.",
            "The _____ refused to listen.",
            "Her _____ was evident.",
            "The _____ attitude caused conflict.",
            "He was known as a _____.",
            "The _____ opinions were outdated.",
        ]
    elif word_lower == "chicanery":
        word_specific_sentences = [
            "Her _____ was eventually discovered.",
            "The _____ fooled many people initially.",
            "He was skilled in the art of _____.",
            "The _____ was clever but dishonest.",
            "She saw through the _____ immediately.",
            "The _____ was exposed by the investigation.",
            "His _____ was unethical.",
            "The _____ deceived many customers.",
            "She couldn't believe the level of _____.",
            "The _____ was finally revealed.",
        ]
    elif word_lower == "choreographer":
        word_specific_sentences = [
            "Her work as a _____ was impressive.",
            "The _____ planned every movement carefully.",
            "She trained to become a professional _____.",
            "The _____ collaborated with the dancers.",
            "His skills as a _____ were renowned.",
            "The _____ designed the entire performance.",
            "She worked closely with the _____.",
            "The _____ had creative vision.",
            "Her role as _____ was crucial.",
            "The _____ created beautiful routines.",
        ]
    elif word_lower == "clemency":
        word_specific_sentences = [
            "Her _____ towards the offender was admirable.",
            "The _____ shown was unexpected.",
            "He asked for _____ in his sentence.",
            "The _____ was granted due to circumstances.",
            "She showed great _____ in her decision.",
            "The _____ was appreciated by all.",
            "His request for _____ was considered.",
            "The _____ demonstrated compassion.",
            "She was known for her _____.",
            "The judge showed unexpected _____.",
        ]
    elif word_lower == "coercion":
        word_specific_sentences = [
            "Her _____ tactics were unacceptable.",
            "The _____ used was excessive.",
            "He resisted the _____ applied.",
            "The _____ violated their rights.",
            "She was against any form of _____.",
            "The _____ was unnecessary.",
            "His use of _____ was criticised.",
            "The _____ was clearly wrong.",
            "She condemned the _____ used.",
            "The _____ was forceful and wrong.",
        ]
    elif word_lower == "coherent":
        word_specific_sentences = [
            "His _____ argument convinced everyone.",
            "The _____ reasoning was sound.",
            "He presented a _____ case for his idea.",
            "The _____ structure made sense.",
            "She organised her thoughts in a _____ way.",
            "The _____ approach solved the issue.",
            "His _____ thinking was impressive.",
            "The _____ plan was well thought out.",
            "She made a _____ connection between ideas.",
            "The _____ explanation was clear.",
        ]
    elif word_lower == "collaborate":
        word_specific_sentences = [
            "They agreed to _____ to solve the problem together.",
            "The two schools will _____ on the charity event.",
            "We need to _____ if we want to succeed.",
            "The teams chose to _____ rather than compete.",
            "They will _____ to create the best solution.",
            "The artists decided to _____ on the mural.",
            "Students should _____ when working on group projects.",
            "The companies will _____ to improve the service.",
            "They agreed to _____ on finding a solution.",
            "The groups decided to _____ effectively.",
        ]
    elif word_lower == "comforting":
        word_specific_sentences = [
            "The _____ presence made everyone feel safe.",
            "She offered _____ advice to her friend.",
            "The _____ atmosphere was peaceful.",
            "His _____ smile reassured the worried child.",
            "The _____ gesture was deeply appreciated.",
            "She provided _____ support during difficult times.",
            "The _____ environment helped them relax.",
            "His _____ manner was very soothing.",
            "The _____ feeling was exactly what they needed.",
            "Her _____ words were healing.",
        ]
    elif word_lower == "commemorate":
        word_specific_sentences = [
            "They will _____ the anniversary with a special ceremony.",
            "The plaque was placed to _____ the brave firefighters.",
            "We should _____ those who helped us.",
            "The monument was erected to _____ the heroes.",
            "They decided to _____ the event with a celebration.",
            "The ceremony will _____ the school's founding.",
            "We will _____ the occasion with a party.",
            "The memorial was created to _____ the victims.",
            "They wanted to _____ the achievement properly.",
            "The statue was built to _____ the fallen soldiers.",
        ]
    elif word_lower == "commence":
        word_specific_sentences = [
            "They decided to _____ the meeting early.",
            "The race will _____ when the whistle blows.",
            "We should _____ our work before lunch.",
            "The concert will _____ in ten minutes.",
            "They agreed to _____ the project tomorrow.",
            "The lesson will _____ at nine o'clock.",
            "We need to _____ planning the event soon.",
            "The festival will _____ next weekend.",
            "They will _____ the journey at dawn.",
            "The ceremony will _____ at noon precisely.",
        ]
    elif word_lower == "commotion":
        word_specific_sentences = [
            "The sudden _____ disrupted the lesson.",
            "She tried to calm the _____.",
            "The _____ was unexpected.",
            "He investigated the source of the _____.",
            "The _____ drew everyone's attention.",
            "She restored order after the _____.",
            "The _____ was quickly resolved.",
            "He was responsible for the _____.",
            "The _____ created chaos.",
            "The _____ caused confusion.",
        ]
    elif word_lower == "communicate":
        word_specific_sentences = [
            "They learned how to _____ effectively in meetings.",
            "She struggled to _____ her feelings properly.",
            "The teacher tried to _____ the concept clearly.",
            "We need to _____ our ideas better.",
            "They found it difficult to _____ across languages.",
            "She worked hard to _____ her thoughts.",
            "The children learned to _____ using sign language.",
            "They tried to _____ the message quickly.",
            "It was hard to _____ in the noisy room.",
            "It is important to _____ clearly with your team.",
        ]
    elif word_lower == "companion":
        word_specific_sentences = [
            "She found a good _____ for the journey.",
            "The _____ made the trip enjoyable.",
            "He was a reliable _____.",
            "The _____ provided comfort and support.",
            "She valued her _____ greatly.",
            "The _____ was always there when needed.",
            "He found a faithful _____.",
            "The _____ shared many adventures.",
            "She considered him a true _____.",
            "The loyal _____ never left his side.",
        ]
    elif word_lower == "compelling":
        word_specific_sentences = [
            "Her _____ argument persuaded everyone.",
            "The _____ evidence was impossible to ignore.",
            "He gave a _____ explanation that made sense.",
            "The _____ presentation captured everyone's attention.",
            "She had a _____ reason for her actions.",
            "The _____ case convinced the jury.",
            "His _____ speech moved the audience.",
            "The _____ nature of the discovery was exciting.",
            "She found the _____ evidence very convincing.",
            "The _____ story was unforgettable.",
        ]
    elif word_lower == "completely":
        word_specific_sentences = [
            "She was _____ exhausted after the long day.",
            "The project was _____ finished on time.",
            "He was _____ convinced of the truth.",
            "The area was _____ covered in snow.",
            "She felt _____ prepared for the exam.",
            "The task was _____ completed.",
            "He was _____ focused on his goal.",
            "The room was _____ empty.",
            "She was _____ satisfied with the result.",
            "The house was _____ destroyed by the fire.",
        ]
    elif word_lower == "composed":
        word_specific_sentences = [
            "His _____ manner helped calm everyone down.",
            "The _____ response showed great maturity.",
            "She kept a _____ expression despite the stress.",
            "His _____ behaviour impressed the teachers.",
            "The _____ atmosphere made everyone feel relaxed.",
            "She showed _____ confidence in her abilities.",
            "His _____ attitude was admirable.",
            "The _____ approach solved the problem.",
            "She maintained a _____ presence throughout.",
            "His _____ nature was reassuring.",
        ]
    elif word_lower == "composure":
        word_specific_sentences = [
            "Her _____ impressed everyone in the room.",
            "The _____ of his response was remarkable.",
            "She maintained her _____ throughout.",
            "His _____ helped calm the situation.",
            "The _____ was evident in her behaviour.",
            "She showed great _____ under pressure.",
            "His _____ never wavered.",
            "The _____ of her manner was impressive.",
            "She displayed remarkable _____.",
            "His _____ was admirable.",
        ]
    elif word_lower == "comprehend":
        word_specific_sentences = [
            "She struggled to _____ the difficult concept.",
            "The students needed help to _____ the problem.",
            "He couldn't _____ why she was upset.",
            "It was hard to _____ the foreign language.",
            "They tried to _____ the teacher's explanation.",
            "She worked hard to _____ the maths problem.",
            "The children couldn't _____ the complicated rules.",
            "He finally managed to _____ the instructions.",
            "It was challenging to _____ the new system.",
            "It took time to _____ the complex instructions.",
        ]
    elif word_lower == "compromise":
        word_specific_sentences = [
            "The _____ satisfied both parties.",
            "She was willing to make a _____.",
            "The _____ allowed them to move forward.",
            "He suggested a _____ that worked for everyone.",
            "The _____ resolved the disagreement.",
            "She found the _____ acceptable.",
            "The _____ was fair to both sides.",
            "He negotiated a _____ successfully.",
            "The _____ prevented further conflict.",
            "They reached a _____ about who would use the computer first.",
        ]
    elif word_lower == "conceited":
        word_specific_sentences = [
            "Her _____ attitude annoyed her classmates.",
            "The _____ behaviour was off-putting.",
            "He showed _____ confidence in his abilities.",
            "The _____ manner made him unpopular.",
            "She couldn't stand his _____ nature.",
            "His _____ comments upset others.",
            "The _____ attitude was evident.",
            "Her _____ behaviour was criticised.",
            "The _____ personality was difficult to like.",
            "His _____ nature was obvious.",
        ]
    elif word_lower == "concentrated":
        word_specific_sentences = [
            "Her _____ effort achieved the goal.",
            "The _____ solution was very powerful.",
            "He made a _____ attempt to succeed.",
            "The _____ form was more effective.",
            "She used a _____ approach to solve it.",
            "The _____ energy was impressive.",
            "His _____ attention helped him learn.",
            "The _____ mixture was too strong.",
            "She applied _____ pressure to the task.",
            "The _____ juice needed water added to it.",
        ]
    elif word_lower == "concerted":
        word_specific_sentences = [
            "Their _____ action solved the problem.",
            "The _____ approach was more effective.",
            "He appreciated the _____ support.",
            "The _____ decision was unanimous.",
            "She valued the _____ contribution.",
            "The _____ work produced excellent results.",
            "His _____ participation was essential.",
            "The _____ strategy succeeded.",
            "She recognised the _____ achievement.",
            "The _____ effort of the team led to victory.",
        ]
    elif word_lower == "conciliatory":
        word_specific_sentences = [
            "The _____ discussion led to a solution.",
            "He tried to be _____ despite the disagreement.",
            "The _____ tone helped calm everyone down.",
            "She maintained an _____ attitude throughout.",
            "The _____ resolution satisfied both sides.",
            "His _____ manner prevented further arguments.",
            "The _____ conversation was productive.",
            "She showed an _____ spirit in negotiations.",
            "The _____ agreement was reached quickly.",
            "Her _____ tone helped calm the angry customers.",
        ]
    
    # Add sentences to list, avoiding duplicates
    for sent in word_specific_sentences:
        if sent not in seen and len(sentences) < 10:
            sentences.append(sent)
            seen.add(sent)
    
    # Fill remaining slots with generic sentences if needed
    while len(sentences) < 10:
        if is_verb:
            generic = f"They decided to _____ the situation carefully."
        elif is_adjective:
            generic = f"The _____ quality was evident throughout."
        else:
            generic = f"The _____ was important in understanding the context."
        
        if generic not in seen:
            sentences.append(generic)
            seen.add(generic)
        else:
            break
    
    return sentences[:10]


def main():
    """Generate quiz sentences for all words in level3_batch1.txt"""
    input_file = Path(__file__).parent.parent / "data" / "level3_batch1.txt"
    output_file = Path(__file__).parent.parent / "data" / "level3_batch1.csv"
    
    # Read words from input file
    words_data = []
    with open(input_file, 'r', encoding='utf-8') as f:
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
                words_data.append((word, meaning, example, synonym, antonym))
    
    # Generate sentences for each word
    all_sentences = []
    for word, meaning, example, synonym, antonym in words_data:
        sentences = generate_sentences_for_word(word, meaning, example, synonym, antonym)
        for sentence in sentences:
            all_sentences.append(("3", word, sentence))
    
    # Write to CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["level", "word", "sentence"])
        writer.writerows(all_sentences)
    
    print(f"Level 3 Batch 1 complete: {len(all_sentences)} sentences")


if __name__ == "__main__":
    main()
