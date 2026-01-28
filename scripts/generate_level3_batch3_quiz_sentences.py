#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 3 Batch 3 vocabulary.
Creates 10 contextually rich sentences per word with varied structures.
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
            word_lower + 'er',
            word_lower + 'ly'
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
    Each sentence provides strong contextual clues specific to the word's meaning.
    """
    sentences = []
    word_lower = word.lower()
    meaning_lower = meaning.lower()
    
    # Determine word type
    is_verb = meaning_lower.startswith("to ")
    is_adjective = any(marker in meaning_lower for marker in [
        "having", "showing", "full of", "characterised by", "characterized by",
        "very", "extremely", "quite", "rather", "causing", "deserving", "able to"
    ])
    is_noun = not is_verb and not is_adjective
    
    # 1. Use example sentence if available
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate contextually rich sentences based on word meaning
    # Create varied sentence structures that provide strong contextual clues
    
    # Build context from meaning, synonyms, and antonyms
    context_words = []
    if synonym:
        context_words.append(synonym)
    if antonym:
        context_words.append(antonym)
    
    # Extract key concepts from meaning
    meaning_keywords = []
    if "hatred" in meaning_lower or "enemy" in meaning_lower:
        meaning_keywords.extend(["rival", "enemy", "conflict", "dispute"])
    if "project" in meaning_lower or "business" in meaning_lower or "venture" in meaning_lower:
        meaning_keywords.extend(["business", "project", "venture", "plan"])
    if "interesting" in meaning_lower or "captivating" in meaning_lower:
        meaning_keywords.extend(["story", "adventure", "exciting", "fascinating"])
    if "eager" in meaning_lower or "interest" in meaning_lower:
        meaning_keywords.extend(["excited", "keen", "passionate", "eager"])
    if "list" in meaning_lower:
        meaning_keywords.extend(["count", "number", "itemise", "detail"])
    if "short" in meaning_lower or "brief" in meaning_lower or "fleeting" in meaning_lower:
        meaning_keywords.extend(["temporary", "brief", "momentary", "quick"])
    if "understanding" in meaning_lower or "realisation" in meaning_lower:
        meaning_keywords.extend(["insight", "understanding", "realisation", "discovery"])
    if "episode" in meaning_lower or "separate" in meaning_lower:
        meaning_keywords.extend(["series", "episodes", "parts", "segments"])
    if "unclear" in meaning_lower or "ambiguous" in meaning_lower or "vague" in meaning_lower:
        meaning_keywords.extend(["unclear", "confusing", "vague", "uncertain"])
    if "vague" in meaning_lower or "avoid" in meaning_lower:
        meaning_keywords.extend(["evade", "avoid", "dodge", "hedge"])
    if "rub" in meaning_lower or "remove" in meaning_lower:
        meaning_keywords.extend(["erase", "remove", "delete", "wipe"])
    if "error" in meaning_lower or "incorrect" in meaning_lower:
        meaning_keywords.extend(["mistake", "wrong", "incorrect", "faulty"])
    if "few" in meaning_lower or "obscure" in meaning_lower:
        meaning_keywords.extend(["rare", "specialised", "complex", "expert"])
    if "delicate" in meaning_lower or "light" in meaning_lower:
        meaning_keywords.extend(["delicate", "light", "airy", "gentle"])
    if "mild" in meaning_lower or "polite" in meaning_lower:
        meaning_keywords.extend(["polite", "gentle", "kind", "tactful"])
    if "worse" in meaning_lower:
        meaning_keywords.extend(["worsen", "aggravate", "intensify", "increase"])
    if "larger" in meaning_lower or "overstate" in meaning_lower:
        meaning_keywords.extend(["overstate", "amplify", "magnify", "embellish"])
    if "annoyed" in meaning_lower or "frustrated" in meaning_lower:
        meaning_keywords.extend(["frustrated", "irritated", "annoyed", "exasperated"])
    if "rule" in meaning_lower or "exclusion" in meaning_lower:
        meaning_keywords.extend(["rule", "norm", "standard", "pattern"])
    if "painful" in meaning_lower or "agonising" in meaning_lower:
        meaning_keywords.extend(["painful", "agonising", "severe", "intense"])
    if "example" in meaning_lower or "excellent" in meaning_lower or "ideal" in meaning_lower:
        meaning_keywords.extend(["perfect", "ideal", "model", "outstanding"])
    if "illustrate" in meaning_lower or "demonstrate" in meaning_lower:
        meaning_keywords.extend(["show", "demonstrate", "illustrate", "represent"])
    if "happy" in meaning_lower or "excited" in meaning_lower or "thrilling" in meaning_lower:
        meaning_keywords.extend(["exciting", "thrilling", "exhilarating", "amazing"])
    if "clear" in meaning_lower or "blame" in meaning_lower or "acquit" in meaning_lower:
        meaning_keywords.extend(["innocent", "blameless", "clear", "free"])
    if "convenient" in meaning_lower:
        meaning_keywords.extend(["practical", "useful", "helpful", "advantageous"])
    if "explain" in meaning_lower or "describe" in meaning_lower:
        meaning_keywords.extend(["explain", "describe", "clarify", "inform"])
    if "energy" in meaning_lower or "enthusiasm" in meaning_lower:
        meaning_keywords.extend(["energetic", "lively", "vibrant", "enthusiastic"])
    if "easier" in meaning_lower or "assist" in meaning_lower:
        meaning_keywords.extend(["help", "assist", "enable", "support"])
    if "funny" in meaning_lower or "absurd" in meaning_lower:
        meaning_keywords.extend(["absurd", "ridiculous", "comical", "silly"])
    if "interested" in meaning_lower or "captivated" in meaning_lower:
        meaning_keywords.extend(["interested", "captivated", "intrigued", "absorbed"])
    if "possible" in meaning_lower or "practical" in meaning_lower:
        meaning_keywords.extend(["possible", "practical", "achievable", "workable"])
    if "shock" in meaning_lower or "astonish" in meaning_lower:
        meaning_keywords.extend(["surprise", "shock", "amaze", "astound"])
    if "obviously" in meaning_lower or "blatant" in meaning_lower:
        meaning_keywords.extend(["obvious", "blatant", "clear", "evident"])
    if "complimentary" in meaning_lower or "good" in meaning_lower:
        meaning_keywords.extend(["nice", "kind", "complimentary", "positive"])
    if "serious" in meaning_lower or "disrespectful" in meaning_lower:
        meaning_keywords.extend(["casual", "light", "disrespectful", "careless"])
    if "trouble" in meaning_lower or "danger" in meaning_lower or "premonition" in meaning_lower:
        meaning_keywords.extend(["warning", "danger", "trouble", "concern"])
    if "silly" in meaning_lower or "sensible" in meaning_lower:
        meaning_keywords.extend(["silly", "trivial", "unimportant", "frivolous"])
    if "secret" in meaning_lower or "stealthy" in meaning_lower:
        meaning_keywords.extend(["secretly", "quietly", "surreptitiously", "covertly"])
    if "talkative" in meaning_lower:
        meaning_keywords.extend(["chatty", "talkative", "verbose", "loquacious"])
    if "kind" in meaning_lower or "polite" in meaning_lower or "courteous" in meaning_lower:
        meaning_keywords.extend(["kind", "polite", "courteous", "welcoming"])
    if "seriousness" in meaning_lower:
        meaning_keywords.extend(["seriousness", "importance", "significance", "weight"])
    if "complaint" in meaning_lower or "unfair" in meaning_lower:
        meaning_keywords.extend(["complaint", "issue", "problem", "concern"])
    if "tricked" in meaning_lower or "deceived" in meaning_lower or "naive" in meaning_lower:
        meaning_keywords.extend(["trusting", "naive", "innocent", "credulous"])
    if "throat" in meaning_lower:
        meaning_keywords.extend(["deep", "hoarse", "rough", "harsh"])
    if "living" in meaning_lower or "suitable" in meaning_lower:
        meaning_keywords.extend(["liveable", "suitable", "comfortable", "inhabitable"])
    if "uncertain" in meaning_lower or "slow" in meaning_lower:
        meaning_keywords.extend(["uncertain", "doubtful", "reluctant", "cautious"])
    if "funny" in meaning_lower:
        meaning_keywords.extend(["funny", "amusing", "comical", "entertaining"])
    if "difficult" in meaning_lower or "obstacle" in meaning_lower:
        meaning_keywords.extend(["obstacle", "barrier", "difficulty", "problem"])
    if "sound" in meaning_lower:
        meaning_keywords.extend(["pronunciation", "sound", "phonetics", "acoustics"])
    if "ashamed" in meaning_lower or "embarrass" in meaning_lower:
        meaning_keywords.extend(["embarrass", "shame", "humiliate", "disgrace"])
    if "clean" in meaning_lower or "germs" in meaning_lower:
        meaning_keywords.extend(["clean", "sanitary", "sterile", "hygienic"])
    if "exaggerated" in meaning_lower:
        meaning_keywords.extend(["exaggeration", "overstatement", "embellishment", "amplification"])
    if "pretends" in meaning_lower or "beliefs" in meaning_lower:
        meaning_keywords.extend(["pretender", "fraud", "fake", "insincere"])
    if "shame" in meaning_lower or "disgrace" in meaning_lower:
        meaning_keywords.extend(["shame", "disgrace", "humiliation", "dishonour"])
    if "illusion" in meaning_lower or "reality" in meaning_lower:
        meaning_keywords.extend(["illusion", "mirage", "fantasy", "deception"])
    if "involvement" in meaning_lower or "wrongdoing" in meaning_lower:
        meaning_keywords.extend(["involve", "connect", "associate", "link"])
    if "pretending" in meaning_lower:
        meaning_keywords.extend(["fraud", "fake", "pretender", "deceiver"])
    if "preparation" in meaning_lower or "spontaneous" in meaning_lower:
        meaning_keywords.extend(["spontaneous", "unplanned", "improvised", "impromptu"])
    if "make up" in meaning_lower or "improvised" in meaning_lower:
        meaning_keywords.extend(["improvise", "ad-lib", "invent", "create"])
    if "passion" in meaning_lower or "captivate" in meaning_lower:
        meaning_keywords.extend(["captivate", "charm", "enchant", "fascinate"])
    if "begin" in meaning_lower or "start" in meaning_lower:
        meaning_keywords.extend(["start", "begin", "commence", "launch"])
    if "unfair" in meaning_lower:
        meaning_keywords.extend(["unfairness", "inequality", "wrong", "injustice"])
    if "indirect" in meaning_lower or "suggestion" in meaning_lower or "hint" in meaning_lower:
        meaning_keywords.extend(["hint", "suggestion", "implication", "insinuation"])
    if "indirectly" in meaning_lower or "suggest" in meaning_lower:
        meaning_keywords.extend(["imply", "suggest", "hint", "insinuate"])
    if "enthusiasm" in meaning_lower or "motivate" in meaning_lower:
        meaning_keywords.extend(["motivate", "inspire", "encourage", "uplift"])
    if "start" in meaning_lower or "bring about" in meaning_lower:
        meaning_keywords.extend(["start", "provoke", "trigger", "instigate"])
    if "rude" in meaning_lower or "offensive" in meaning_lower:
        meaning_keywords.extend(["rude", "offensive", "disrespectful", "insulting"])
    if "between" in meaning_lower or "help" in meaning_lower or "mediate" in meaning_lower:
        meaning_keywords.extend(["mediate", "intervene", "help", "arbitrate"])
    if "explain" in meaning_lower or "meaning" in meaning_lower:
        meaning_keywords.extend(["explain", "clarify", "translate", "interpret"])
    if "between" in meaning_lower or "help" in meaning_lower:
        meaning_keywords.extend(["intervene", "interfere", "step in", "mediate"])
    if "close" in meaning_lower or "private" in meaning_lower:
        meaning_keywords.extend(["close", "personal", "private", "confidential"])
    if "fearless" in meaning_lower or "adventurous" in meaning_lower or "brave" in meaning_lower:
        meaning_keywords.extend(["brave", "fearless", "courageous", "bold"])
    if "detailed" in meaning_lower or "complicated" in meaning_lower:
        meaning_keywords.extend(["complex", "detailed", "elaborate", "sophisticated"])
    if "shy" in meaning_lower or "quiet" in meaning_lower:
        meaning_keywords.extend(["shy", "reserved", "quiet", "introverted"])
    if "overwhelm" in meaning_lower or "flood" in meaning_lower:
        meaning_keywords.extend(["flood", "overwhelm", "deluge", "swamp"])
    if "danger" in meaning_lower or "harm" in meaning_lower:
        meaning_keywords.extend(["danger", "risk", "peril", "threat"])
    if "judgement" in meaning_lower or "wise" in meaning_lower:
        meaning_keywords.extend(["wise", "sensible", "prudent", "judicious"])
    if "side by side" in meaning_lower or "compare" in meaning_lower:
        meaning_keywords.extend(["compare", "contrast", "place together", "set side by side"])
    if "complicated" in meaning_lower or "maze" in meaning_lower:
        meaning_keywords.extend(["maze", "complex", "confusing", "intricate"])
    if "weak" in meaning_lower or "suffer" in meaning_lower:
        meaning_keywords.extend(["weaken", "fade", "decline", "deteriorate"])
    if "weariness" in meaning_lower or "lethargy" in meaning_lower:
        meaning_keywords.extend(["tiredness", "exhaustion", "weariness", "fatigue"])
    if "energy" in meaning_lower or "sluggish" in meaning_lower:
        meaning_keywords.extend(["sluggish", "tired", "weary", "lethargic"])
    if "lightness" in meaning_lower or "inappropriate" in meaning_lower:
        meaning_keywords.extend(["light-heartedness", "frivolity", "humour", "joviality"])
    if "hatred" in meaning_lower or "disgust" in meaning_lower or "repulsive" in meaning_lower:
        meaning_keywords.extend(["disgusting", "repulsive", "revolting", "abhorrent"])
    if "absurd" in meaning_lower or "ridiculous" in meaning_lower:
        meaning_keywords.extend(["absurd", "ridiculous", "preposterous", "nonsensical"])
    if "light" in meaning_lower or "glowing" in meaning_lower:
        meaning_keywords.extend(["glowing", "bright", "radiant", "shining"])
    if "shining" in meaning_lower or "glossy" in meaning_lower:
        meaning_keywords.extend(["shiny", "glossy", "gleaming", "polished"])
    if "plots" in meaning_lower or "schemes" in meaning_lower:
        meaning_keywords.extend(["plot", "scheme", "conspire", "plan"])
    if "attract" in meaning_lower or "charm" in meaning_lower:
        meaning_keywords.extend(["attractive", "charming", "appealing", "magnetic"])
    
    # Generate sentences with varied structures
    sentence_templates = []
    
    if is_verb:
        sentence_templates = [
            f"She decided to _____ when the situation required immediate action.",
            f"He began to _____ after carefully considering all the options.",
            f"They were forced to _____ when no other solution seemed possible.",
            f"The teacher asked them to _____ as part of the exercise.",
            f"She managed to _____ successfully despite the challenges.",
            f"He refused to _____ even when others insisted it was necessary.",
            f"They worked together to _____ the problem effectively.",
            f"She learned how to _____ during her training sessions.",
            f"He tried to _____ but found it more difficult than expected.",
            f"The team needed to _____ before the deadline approached."
        ]
    elif is_adjective:
        sentence_templates = [
            f"Her _____ behaviour surprised everyone who knew her.",
            f"The _____ situation made it difficult to know what to do.",
            f"His _____ attitude was obvious to all who observed him.",
            f"The _____ weather affected everyone's plans for the day.",
            f"She had a _____ personality that everyone admired.",
            f"The _____ colours of the painting were striking and beautiful.",
            f"His _____ comments surprised all the listeners in the room.",
            f"It was a _____ moment that nobody would ever forget.",
            f"The _____ scene brought tears to everyone's eyes.",
            f"Everyone could see how _____ the situation had become."
        ]
    else:  # noun
        sentence_templates = [
            f"The _____ became clear as the story unfolded.",
            f"She found the _____ hidden in the old wooden chest.",
            f"The _____ appeared suddenly without any warning.",
            f"He explained the _____ to the curious children gathered around.",
            f"The _____ lasted for several hours before ending.",
            f"Nobody expected to see a _____ in that particular place.",
            f"The ancient _____ was discovered by archaeologists last year.",
            f"She studied the _____ carefully before making her decision.",
            f"The _____ stood out clearly in the surrounding landscape.",
            f"Everyone could hear the _____ from far away in the distance."
        ]
    
    # Customise sentences based on word meaning and context
    for i, template in enumerate(sentence_templates[:10-len(sentences)]):
        # Replace generic placeholders with context-specific words
        sentence = template
        
        # Add contextual clues using synonyms/antonyms/meaning keywords
        if context_words and i < len(context_words):
            # Incorporate synonym/antonym subtly
            pass  # We'll add context through meaning keywords instead
        
        # Customise based on specific word meanings
        if word_lower == "enmity":
            custom_sentences = [
                "There was deep _____ between the two rival schools that had lasted for years.",
                "The _____ between the neighbouring families prevented them from speaking.",
                "Years of _____ had built up between the competing teams.",
                "The _____ was so strong that they refused to be in the same room.",
                "She could sense the _____ in the air whenever they met.",
                "The _____ between them was obvious to everyone who witnessed their arguments.",
                "Despite attempts at peace, the _____ continued to grow stronger.",
                "The _____ had started over a small disagreement but had escalated.",
                "Their _____ was well-known throughout the entire community.",
                "The _____ made it impossible for them to work together."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "enterprise":
            custom_sentences = [
                "Starting a lemonade stand was her first business _____.",
                "The new _____ required careful planning and hard work.",
                "His latest _____ involved opening a small bookshop in town.",
                "The school encouraged pupils to develop their own creative _____.",
                "She invested all her savings into the risky _____.",
                "The successful _____ had grown from a small idea into something big.",
                "They needed funding to support their ambitious _____.",
                "The _____ showed great promise in its first few months.",
                "Her entrepreneurial spirit led her to start another _____.",
                "The _____ required teamwork and dedication to succeed."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "enthralling":
            custom_sentences = [
                "The _____ adventure story kept us reading all night long.",
                "She found the film so _____ that she watched it twice.",
                "The _____ performance held the audience's attention throughout.",
                "His _____ tale of exploration captured everyone's imagination.",
                "The _____ book was impossible to put down once started.",
                "They were completely absorbed by the _____ documentary.",
                "The _____ nature of the story made time fly by.",
                "Her _____ presentation kept everyone engaged from start to finish.",
                "The _____ plot twists surprised even the most careful readers.",
                "We were all captivated by the _____ narrative."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "enthusiasm":
            custom_sentences = [
                "Her _____ for art was obvious to everyone who saw her work.",
                "The team's _____ for the project was infectious and inspiring.",
                "His _____ for science led him to conduct experiments at home.",
                "She showed great _____ when discussing her favourite hobby.",
                "Their _____ for the school play was evident in every rehearsal.",
                "The teacher's _____ made the lesson enjoyable for everyone.",
                "His _____ for reading encouraged others to pick up books.",
                "The _____ of the crowd could be felt throughout the stadium.",
                "She approached every task with genuine _____ and energy.",
                "Their _____ never wavered even when things became difficult."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "enumerate":
            custom_sentences = [
                "She began to _____ the reasons for her decision one by one.",
                "The teacher asked them to _____ all the countries they could remember.",
                "He started to _____ the items needed for the camping trip.",
                "She had to _____ each step of the process carefully.",
                "The list required them to _____ every single detail.",
                "He began to _____ the problems they had encountered.",
                "She decided to _____ the benefits of joining the club.",
                "The instructions asked them to _____ their concerns in order.",
                "He tried to _____ all the things he was grateful for.",
                "She needed to _____ the evidence before presenting her case."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "ephemeral":
            custom_sentences = [
                "The _____ beauty of cherry blossom lasts only a few days.",
                "The _____ nature of the rainbow made it all the more special.",
                "Her happiness was _____ and soon faded away.",
                "The _____ moment of peace was quickly interrupted.",
                "They knew the _____ joy would not last forever.",
                "The _____ quality of youth should be cherished while it lasts.",
                "The _____ snowflakes melted as soon as they touched the ground.",
                "His _____ fame disappeared as quickly as it had arrived.",
                "The _____ opportunity had to be seized immediately.",
                "The _____ nature of the experience made it unforgettable."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "epiphany":
            custom_sentences = [
                "She had an _____ about how to solve the difficult puzzle.",
                "His sudden _____ changed the way he viewed the problem.",
                "The _____ came to her in the middle of the night.",
                "He experienced an _____ that clarified everything for him.",
                "Her _____ about friendship came after a difficult experience.",
                "The _____ helped him understand what he needed to do.",
                "She had an _____ that made all the pieces fit together.",
                "His _____ was so clear that he acted on it immediately.",
                "The _____ struck her like a bolt of lightning.",
                "He shared his _____ with the rest of the group."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "episodic":
            custom_sentences = [
                "The _____ nature of the show made it easy to follow.",
                "The story was told in an _____ format with separate chapters.",
                "Her memory of the event was _____ and incomplete.",
                "The _____ structure allowed viewers to watch at their own pace.",
                "The _____ nature of the narrative kept readers engaged.",
                "The _____ format meant each part could stand alone.",
                "The _____ storytelling style suited the complex plot.",
                "The _____ structure made it perfect for serialisation.",
                "The _____ nature of the programme appealed to many viewers.",
                "The _____ approach allowed for multiple storylines."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "equivocal":
            custom_sentences = [
                "His _____ answer did not satisfy the curious reporter.",
                "The _____ statement left everyone confused about what was meant.",
                "Her _____ response made it unclear what she really thought.",
                "The _____ nature of the message caused misunderstanding.",
                "His _____ comments failed to clarify the situation.",
                "The _____ explanation only added to the confusion.",
                "Her _____ attitude made it difficult to know where she stood.",
                "The _____ evidence could be interpreted in different ways.",
                "His _____ behaviour left others uncertain about his intentions.",
                "The _____ nature of the agreement led to disputes later."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "equivocate":
            custom_sentences = [
                "The politician tried to _____ when asked directly about the issue.",
                "She began to _____ instead of giving a straight answer.",
                "He would always _____ when faced with difficult questions.",
                "The witness started to _____ to avoid committing to an answer.",
                "She tried to _____ her way out of the awkward situation.",
                "He would _____ whenever he didn't want to be honest.",
                "The spokesperson began to _____ to avoid controversy.",
                "She tried to _____ rather than admit she didn't know.",
                "He would _____ whenever he wanted to avoid responsibility.",
                "The student tried to _____ when asked about the missing homework."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "erasable":
            custom_sentences = [
                "She always used an _____ pen for her maths work.",
                "The _____ marker allowed her to correct mistakes easily.",
                "He preferred _____ pencils so he could fix errors.",
                "The _____ nature of the writing made editing simple.",
                "She chose _____ materials for her rough drafts.",
                "The _____ board made it easy to start over.",
                "He liked using _____ tools for his first attempts.",
                "The _____ quality meant she could experiment freely.",
                "She found _____ pens perfect for practising handwriting.",
                "The _____ surface allowed for multiple revisions."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "erroneous":
            custom_sentences = [
                "The _____ report had to be corrected immediately.",
                "Her _____ assumption led to the wrong conclusion.",
                "The _____ information caused confusion among the pupils.",
                "His _____ belief was based on misunderstanding.",
                "The _____ data needed to be replaced with accurate facts.",
                "She realised her _____ thinking had led her astray.",
                "The _____ statement was quickly retracted.",
                "His _____ conclusion was based on faulty evidence.",
                "The _____ calculation resulted in the wrong answer.",
                "She corrected the _____ entry in her notebook."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "esoteric":
            custom_sentences = [
                "The _____ subject was studied by only a few experts.",
                "His _____ knowledge was difficult for others to understand.",
                "The _____ nature of the topic made it inaccessible to most.",
                "She had an interest in _____ subjects that few others shared.",
                "The _____ language was understood by only a select group.",
                "His _____ ideas were too complex for the general audience.",
                "The _____ field required years of specialised study.",
                "She found the _____ concepts fascinating but challenging.",
                "The _____ nature of the discussion excluded many listeners.",
                "His _____ expertise was respected by fellow specialists."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "ethereal":
            custom_sentences = [
                "The _____ music seemed to float through the air.",
                "Her _____ beauty was like something from a fairy tale.",
                "The _____ quality of the light made everything look magical.",
                "His _____ voice had a delicate, almost otherworldly sound.",
                "The _____ atmosphere made the garden seem enchanted.",
                "She moved with an _____ grace that was mesmerising.",
                "The _____ nature of the scene was breathtaking.",
                "His _____ presence seemed to light up the room.",
                "The _____ colours of the sunset were unforgettable.",
                "She had an _____ quality that was hard to describe."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "euphemism":
            custom_sentences = [
                "'Passed away' is a _____ for 'died'.",
                "She used a _____ to soften the harsh truth.",
                "The _____ made the difficult topic easier to discuss.",
                "He preferred to use a _____ rather than the direct word.",
                "The _____ was more polite than the original term.",
                "She chose a _____ to avoid causing offence.",
                "The _____ helped make the conversation more comfortable.",
                "He used a _____ to be tactful about the situation.",
                "The _____ was gentler than the alternative expression.",
                "She employed a _____ to maintain politeness."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "exacerbate":
            custom_sentences = [
                "Complaining will only _____ the situation further.",
                "His harsh words served to _____ the conflict.",
                "The delay would only _____ the existing problems.",
                "She knew that arguing would _____ matters.",
                "The mistake would _____ an already difficult situation.",
                "His interference would only _____ the tension.",
                "The bad weather would _____ their travel difficulties.",
                "She realised her comment would _____ the disagreement.",
                "The additional pressure would _____ his stress levels.",
                "Their actions would _____ the crisis."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "exaggerate":
            custom_sentences = [
                "He tends to _____ when telling his fishing stories.",
                "She would often _____ to make her stories more exciting.",
                "Don't _____ the difficulties we're facing.",
                "He liked to _____ his achievements to impress others.",
                "She would _____ the size of the fish she caught.",
                "His tendency to _____ made it hard to believe him.",
                "She would _____ how difficult the test had been.",
                "He would _____ the distance he had walked.",
                "She tended to _____ when describing her adventures.",
                "His habit of _____ made his tales unbelievable."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "exasperated":
            custom_sentences = [
                "She was _____ by the constant interruptions.",
                "His _____ expression showed his frustration clearly.",
                "The teacher became _____ after repeating the instructions.",
                "She felt _____ by the repeated mistakes.",
                "His _____ sigh revealed his growing impatience.",
                "She was _____ by the lack of progress.",
                "The _____ parent finally lost their temper.",
                "She became _____ when nobody listened to her.",
                "His _____ tone indicated he had reached his limit.",
                "She was _____ by the endless delays."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "exception":
            custom_sentences = [
                "Every rule has an _____ according to the saying.",
                "She was the only _____ to the general pattern.",
                "The _____ proved that the rule wasn't always true.",
                "He made an _____ for his best friend.",
                "The _____ was rare but not impossible.",
                "She was granted an _____ due to special circumstances.",
                "The _____ allowed her to participate despite the age limit.",
                "He was the _____ that proved the rule.",
                "The _____ showed that flexibility was sometimes needed.",
                "She was the only _____ in an otherwise perfect record."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "excruciating":
            custom_sentences = [
                "The _____ toothache kept her awake all night.",
                "He felt _____ pain after the accident.",
                "The _____ wait seemed to last forever.",
                "She experienced _____ embarrassment when she tripped.",
                "The _____ heat made it impossible to stay outside.",
                "He endured _____ discomfort during the long journey.",
                "The _____ noise was unbearable.",
                "She found the _____ silence difficult to bear.",
                "The _____ effort required all his strength.",
                "He felt _____ anxiety before the important exam."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "exemplary":
            custom_sentences = [
                "Her _____ behaviour earned her a special award.",
                "The _____ student was praised by all the teachers.",
                "His _____ conduct set a standard for others to follow.",
                "She showed _____ dedication to her studies.",
                "The _____ work was used as a model for others.",
                "His _____ performance impressed everyone.",
                "She demonstrated _____ leadership qualities.",
                "The _____ effort resulted in outstanding success.",
                "His _____ character made him a role model.",
                "She provided an _____ example for younger pupils."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "exemplify":
            custom_sentences = [
                "Her kindness _____ the values of the school.",
                "The story would _____ the importance of honesty.",
                "His actions _____ what it means to be brave.",
                "The example would _____ the concept perfectly.",
                "Her behaviour _____ the best qualities of friendship.",
                "The case would _____ the problem clearly.",
                "His work would _____ excellence in the field.",
                "The incident would _____ the need for change.",
                "Her response _____ true sportsmanship.",
                "The situation would _____ the challenges they faced."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "exhilarating":
            custom_sentences = [
                "The _____ ride on the rollercoaster was unforgettable.",
                "She found the experience completely _____ and exciting.",
                "The _____ adventure left them breathless with excitement.",
                "His _____ victory brought joy to everyone.",
                "The _____ feeling of success was overwhelming.",
                "She described the journey as the most _____ of her life.",
                "The _____ moment would stay with them forever.",
                "His _____ performance thrilled the entire audience.",
                "The _____ speed made her heart race.",
                "She found the challenge both difficult and _____."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "exonerate":
            custom_sentences = [
                "The new evidence helped to _____ the innocent man.",
                "The investigation would _____ him of all charges.",
                "The proof would _____ her from any blame.",
                "The testimony would _____ the accused person.",
                "The discovery would _____ him completely.",
                "The evidence would _____ her of wrongdoing.",
                "The report would _____ them from responsibility.",
                "The findings would _____ the suspect.",
                "The proof would _____ him from suspicion.",
                "The testimony would _____ her from the accusations."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "expedient":
            custom_sentences = [
                "Taking a shortcut was _____ but not the best route.",
                "The _____ solution solved the immediate problem.",
                "She chose the most _____ option available.",
                "The _____ decision wasn't necessarily the right one.",
                "He took the _____ path to save time.",
                "The _____ approach worked for now.",
                "She made an _____ choice to avoid delay.",
                "The _____ method was quick but not ideal.",
                "He found an _____ way to complete the task.",
                "The _____ solution was practical if not perfect."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "expository":
            custom_sentences = [
                "The _____ essay explained how volcanoes work.",
                "She wrote an _____ piece about the water cycle.",
                "The _____ text described the process clearly.",
                "His _____ writing helped others understand the topic.",
                "The _____ style made complex ideas accessible.",
                "She used an _____ approach to explain the concept.",
                "The _____ nature of the article was educational.",
                "His _____ writing clarified the difficult subject.",
                "The _____ format was perfect for learning.",
                "She preferred _____ writing to creative stories."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "exuberant":
            custom_sentences = [
                "The _____ crowd cheered loudly for their team.",
                "Her _____ personality made her popular everywhere.",
                "The _____ celebration lasted well into the night.",
                "His _____ energy was infectious.",
                "The _____ display of joy was wonderful to see.",
                "She showed _____ enthusiasm for the project.",
                "The _____ nature of the performance was captivating.",
                "His _____ spirit lifted everyone's mood.",
                "The _____ response exceeded all expectations.",
                "She approached life with an _____ attitude."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "facilitate":
            custom_sentences = [
                "Good lighting can _____ reading in the evening.",
                "The new system would _____ communication between departments.",
                "She tried to _____ the meeting by preparing materials.",
                "The tool would _____ the completion of the task.",
                "He worked to _____ understanding between the groups.",
                "The programme would _____ learning for all pupils.",
                "She helped to _____ the discussion.",
                "The changes would _____ better cooperation.",
                "He tried to _____ the process as much as possible.",
                "The improvements would _____ smoother operations."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "farcical":
            custom_sentences = [
                "The _____ situation made everyone burst out laughing.",
                "The _____ nature of the events was unbelievable.",
                "Her _____ attempt at cooking ended in disaster.",
                "The _____ comedy had the audience in stitches.",
                "His _____ behaviour was completely ridiculous.",
                "The _____ turn of events surprised everyone.",
                "She found the whole situation utterly _____.",
                "The _____ scene was like something from a comedy.",
                "His _____ mistake was actually quite funny.",
                "The _____ nature of the problem was absurd."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "fascinated":
            custom_sentences = [
                "She was _____ by the ancient Egyptian artefacts.",
                "He became _____ with the workings of the engine.",
                "The children were _____ by the magician's tricks.",
                "She remained _____ throughout the entire presentation.",
                "He was _____ by the complexity of the problem.",
                "The pupils were _____ by the science experiment.",
                "She was _____ by the stories of adventure.",
                "He became _____ with learning new languages.",
                "The audience was _____ by the performance.",
                "She was _____ by the mysteries of space."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "feasible":
            custom_sentences = [
                "The plan seemed _____ and was approved by the committee.",
                "She wondered if the idea was actually _____.",
                "The proposal was _____ but would require effort.",
                "He thought the project was _____ given their resources.",
                "The suggestion seemed _____ and worth trying.",
                "She believed the plan was _____ if they worked together.",
                "The idea was _____ but needed careful planning.",
                "He considered whether the approach was truly _____.",
                "The solution seemed _____ and practical.",
                "She found the proposal _____ and well thought out."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "flabbergast":
            custom_sentences = [
                "The surprise ending of the story completely _____ me.",
                "The unexpected news would _____ everyone who heard it.",
                "Her announcement would _____ all her friends.",
                "The revelation would _____ even the most sceptical person.",
                "The outcome would _____ those who had doubted.",
                "His achievement would _____ everyone who knew him.",
                "The discovery would _____ the entire scientific community.",
                "The result would _____ all the experts.",
                "The news would _____ anyone who heard it.",
                "The revelation would _____ even his closest friends."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "flagrant":
            custom_sentences = [
                "His _____ cheating was immediately noticed by the teacher.",
                "The _____ violation of the rules could not be ignored.",
                "Her _____ disregard for safety worried everyone.",
                "The _____ error was obvious to all observers.",
                "His _____ behaviour was unacceptable.",
                "The _____ mistake was impossible to miss.",
                "Her _____ breaking of the rules was shocking.",
                "The _____ nature of the offence was clear.",
                "His _____ disrespect was appalling.",
                "The _____ violation was witnessed by many."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "flattering":
            custom_sentences = [
                "The _____ photograph made her look very elegant.",
                "His _____ comments made her feel good about herself.",
                "The _____ portrait captured her best features.",
                "She received many _____ compliments about her work.",
                "The _____ review boosted her confidence.",
                "His _____ words were kind and appreciated.",
                "The _____ description made her sound impressive.",
                "She found the _____ remarks encouraging.",
                "The _____ comparison was very kind.",
                "His _____ assessment was generous."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "flippant":
            custom_sentences = [
                "His _____ remarks about the exam upset the teacher.",
                "She was annoyed by his _____ attitude towards serious matters.",
                "The _____ comment was inappropriate for the occasion.",
                "His _____ response showed a lack of respect.",
                "She found his _____ tone disrespectful.",
                "The _____ joke was not appreciated by everyone.",
                "His _____ behaviour was out of place.",
                "She was offended by his _____ dismissal of her concerns.",
                "The _____ remark was thoughtless and hurtful.",
                "His _____ approach to important issues was concerning."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "foreboding":
            custom_sentences = [
                "She had a _____ that the trip would not go well.",
                "The dark clouds gave him a sense of _____.",
                "Her _____ about the meeting proved to be correct.",
                "The _____ feeling made her anxious.",
                "He couldn't shake the _____ that something was wrong.",
                "The _____ atmosphere made everyone uneasy.",
                "Her _____ sense of danger was justified.",
                "The _____ feeling grew stronger as time passed.",
                "He had a _____ that trouble was coming.",
                "The _____ sense of doom was overwhelming."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "frivolous":
            custom_sentences = [
                "She wasted money on _____ purchases.",
                "His _____ behaviour was not appropriate for the occasion.",
                "The _____ spending worried her parents.",
                "She was criticised for her _____ attitude.",
                "The _____ nature of the complaint was obvious.",
                "His _____ remarks were not taken seriously.",
                "She regretted her _____ decision later.",
                "The _____ request was quickly dismissed.",
                "His _____ approach to important matters was concerning.",
                "She was known for her _____ spending habits."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "furtively":
            custom_sentences = [
                "She _____ passed the note under the desk.",
                "He looked around _____ before opening the door.",
                "She _____ glanced over her shoulder to check.",
                "He moved _____ to avoid being noticed.",
                "She _____ slipped the letter into her bag.",
                "He acted _____ so nobody would see him.",
                "She _____ checked to make sure nobody was watching.",
                "He moved _____ through the quiet corridor.",
                "She _____ whispered the secret to her friend.",
                "He _____ made his way past the guard."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "garrulous":
            custom_sentences = [
                "The _____ neighbour talked for hours without stopping.",
                "Her _____ nature made conversations very long.",
                "The _____ guest dominated the entire discussion.",
                "His _____ behaviour made it hard for others to speak.",
                "The _____ speaker went on far too long.",
                "She was known for being _____ and talkative.",
                "The _____ customer chatted endlessly at the counter.",
                "His _____ personality meant he never stopped talking.",
                "The _____ friend could talk for hours about anything.",
                "She found his _____ nature exhausting."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "gracious":
            custom_sentences = [
                "The _____ host thanked everyone for coming.",
                "Her _____ acceptance of the award impressed everyone.",
                "The _____ winner congratulated her competitors.",
                "His _____ behaviour showed true sportsmanship.",
                "The _____ response to criticism was admirable.",
                "She was always _____ even when things went wrong.",
                "The _____ gesture was much appreciated.",
                "His _____ manner made everyone feel welcome.",
                "The _____ hostess made all guests feel comfortable.",
                "She showed a _____ attitude throughout the competition."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "gravity":
            custom_sentences = [
                "The _____ of the situation became clear to everyone.",
                "She understood the _____ of the problem they faced.",
                "The _____ of his words made everyone listen carefully.",
                "He didn't realise the _____ of what he had done.",
                "The _____ of the matter required serious attention.",
                "She felt the full _____ of the responsibility.",
                "The _____ of the decision weighed heavily on him.",
                "He finally understood the _____ of the situation.",
                "The _____ of the crisis demanded immediate action.",
                "She appreciated the _____ of the moment."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "grievance":
            custom_sentences = [
                "The workers presented their _____ to management.",
                "She had a legitimate _____ about the unfair treatment.",
                "The _____ was taken seriously by the authorities.",
                "He filed a _____ about the poor conditions.",
                "The _____ needed to be addressed properly.",
                "She raised her _____ at the meeting.",
                "The _____ was investigated thoroughly.",
                "He had a valid _____ that deserved attention.",
                "The _____ was resolved after discussion.",
                "She expressed her _____ clearly and calmly."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "gullible":
            custom_sentences = [
                "The _____ tourist believed the outrageous story.",
                "She was too _____ to see through the deception.",
                "The _____ child believed everything he was told.",
                "His _____ nature made him an easy target.",
                "The _____ person fell for the obvious trick.",
                "She was _____ enough to trust the stranger.",
                "The _____ student believed the false excuse.",
                "His _____ attitude made him vulnerable.",
                "The _____ friend was easily fooled.",
                "She was _____ and trusted people too easily."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "guttural":
            custom_sentences = [
                "The creature made a _____ sound that frightened us.",
                "His _____ voice was deep and rough.",
                "The _____ noise came from deep in his throat.",
                "She heard a _____ growl from the shadows.",
                "The _____ sound was harsh and unpleasant.",
                "His _____ pronunciation was difficult to understand.",
                "The _____ noise echoed through the cave.",
                "She recognised the _____ tone immediately.",
                "The _____ sound was unlike anything she had heard.",
                "His _____ speech was hard to follow."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "habitable":
            custom_sentences = [
                "The island was barely _____ due to harsh weather.",
                "The house was no longer _____ after the flood.",
                "The area was not _____ for human settlement.",
                "They made the cave _____ by adding basic comforts.",
                "The planet might be _____ if conditions improved.",
                "The building was barely _____ in its current state.",
                "The region was not _____ during the winter months.",
                "They worked to make the space _____ again.",
                "The conditions made it barely _____.",
                "The area was considered _____ by the experts."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "hesitant":
            custom_sentences = [
                "She was _____ to speak up in the meeting.",
                "His _____ approach showed his uncertainty.",
                "The _____ student raised her hand slowly.",
                "She was _____ about making the decision.",
                "His _____ response indicated his doubts.",
                "The _____ pause before answering was noticeable.",
                "She was _____ to commit to the plan.",
                "His _____ behaviour showed he wasn't sure.",
                "The _____ way she spoke revealed her uncertainty.",
                "She was _____ to take the risk."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "hilarious":
            custom_sentences = [
                "The _____ comedy show had everyone laughing.",
                "She found the joke absolutely _____.",
                "The _____ story made tears run down her face.",
                "His _____ impression of the teacher was spot on.",
                "The _____ film had the whole cinema in stitches.",
                "She thought the situation was completely _____.",
                "The _____ performance was unforgettable.",
                "His _____ antics kept everyone entertained.",
                "The _____ moment was captured on camera.",
                "She found his sense of humour truly _____."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "hindrance":
            custom_sentences = [
                "The lack of funding was a _____ to the project.",
                "The bad weather proved to be a major _____.",
                "Her absence was a _____ to the team's progress.",
                "The obstacle was a significant _____ to their plans.",
                "The delay became a _____ to completing the work.",
                "The problem was a real _____ to success.",
                "The restriction was a _____ to their freedom.",
                "The difficulty was a _____ to moving forward.",
                "The barrier was a _____ to their progress.",
                "The issue was a serious _____ to the plan."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "homophone":
            custom_sentences = [
                "'There', 'their' and 'they're' are _____.",
                "She confused the _____ words in her writing.",
                "The teacher explained what a _____ was.",
                "He struggled with _____ that sounded the same.",
                "The _____ caused confusion in her spelling.",
                "She learned about _____ in her English lesson.",
                "The _____ words were difficult to distinguish.",
                "He mixed up the _____ in his essay.",
                "The _____ made spelling challenging.",
                "She studied _____ to improve her writing."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "humiliate":
            custom_sentences = [
                "It is cruel to _____ someone in front of others.",
                "She didn't want to _____ her friend publicly.",
                "The bully tried to _____ the younger pupil.",
                "He would never _____ anyone intentionally.",
                "The public mistake would _____ her.",
                "She felt _____ by the embarrassing situation.",
                "The comment was meant to _____ him.",
                "He didn't want to _____ his opponent.",
                "The incident would _____ the entire team.",
                "She tried not to _____ herself further."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "humorous":
            custom_sentences = [
                "Her _____ stories always made everyone laugh.",
                "The _____ book was perfect for light reading.",
                "His _____ remarks lightened the mood.",
                "The _____ play entertained the whole audience.",
                "She had a _____ way of telling stories.",
                "The _____ anecdote broke the tension.",
                "His _____ personality made him popular.",
                "The _____ situation was quite amusing.",
                "She found his _____ comments entertaining.",
                "The _____ tale was told with great skill."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "hygienic":
            custom_sentences = [
                "The restaurant maintained _____ kitchen standards.",
                "She always kept her workspace clean and _____.",
                "The _____ conditions were essential for safety.",
                "He ensured everything was _____ before cooking.",
                "The _____ practices prevented the spread of germs.",
                "She followed strict _____ procedures.",
                "The _____ environment was important for health.",
                "He maintained _____ habits at all times.",
                "The _____ standards were very high.",
                "She was careful to keep everything _____."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "hyperbole":
            custom_sentences = [
                "Saying 'I'm starving' is _____ when you're just hungry.",
                "She used _____ to emphasise her point.",
                "The _____ made the story more exciting.",
                "His statement was clearly _____ and exaggerated.",
                "The _____ helped make the description vivid.",
                "She recognised the _____ in his claim.",
                "The _____ was used for dramatic effect.",
                "His _____ was obvious to everyone.",
                "The _____ made the tale more entertaining.",
                "She understood that it was just _____."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "hypocrite":
            custom_sentences = [
                "He was called a _____ for not practising what he preached.",
                "The _____ said one thing but did another.",
                "She was accused of being a _____.",
                "The _____ criticised others for what he did himself.",
                "His behaviour showed he was a _____.",
                "The _____ pretended to have beliefs he didn't follow.",
                "She realised she had been a _____.",
                "The _____ was exposed by his actions.",
                "His _____ was obvious to everyone.",
                "The _____ claimed to care but didn't act on it."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "ignominy":
            custom_sentences = [
                "He suffered the _____ of being sent off the field.",
                "The _____ of defeat was hard to bear.",
                "She faced the _____ of public failure.",
                "The _____ of the situation was overwhelming.",
                "He couldn't escape the _____ of his actions.",
                "The _____ brought shame to his family.",
                "She felt the full _____ of the mistake.",
                "The _____ was worse than the punishment.",
                "He endured the _____ with dignity.",
                "The _____ would follow him for years."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "illusory":
            custom_sentences = [
                "The oasis in the desert was _____.",
                "Her hopes proved to be _____ and unrealistic.",
                "The _____ promise was never fulfilled.",
                "His sense of security was _____.",
                "The _____ nature of the offer became clear.",
                "She realised her dreams were _____.",
                "The _____ success was not real.",
                "His _____ confidence masked his fears.",
                "The _____ solution didn't actually work.",
                "She discovered the opportunity was _____."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "implicate":
            custom_sentences = [
                "The evidence seemed to _____ him in the crime.",
                "The clues would _____ several people.",
                "Her statement would _____ others in the scheme.",
                "The findings would _____ the suspect.",
                "The proof would _____ him directly.",
                "Her actions would _____ her friends.",
                "The investigation would _____ more people.",
                "The testimony would _____ the accused.",
                "The evidence would _____ several suspects.",
                "The discovery would _____ everyone involved."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "imposter":
            custom_sentences = [
                "The _____ was caught trying to enter with a fake badge.",
                "She realised he was an _____ pretending to be someone else.",
                "The _____ fooled everyone for a while.",
                "He was exposed as an _____ after investigation.",
                "The _____ had been living a lie.",
                "She discovered the _____ before it was too late.",
                "The _____ was finally unmasked.",
                "He was revealed to be an _____.",
                "The _____ had deceived many people.",
                "She saw through the _____ immediately."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "impromptu":
            custom_sentences = [
                "She gave an _____ speech at the party.",
                "The _____ performance surprised everyone.",
                "His _____ decision was made on the spot.",
                "The _____ meeting was called without notice.",
                "She made an _____ visit to her friend.",
                "The _____ concert was a pleasant surprise.",
                "His _____ remarks were well received.",
                "The _____ gathering happened spontaneously.",
                "She delivered an _____ presentation.",
                "The _____ celebration was unplanned but fun."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "improvise":
            custom_sentences = [
                "The actors had to _____ when they forgot their lines.",
                "She learned to _____ when things didn't go as planned.",
                "He had to _____ a solution to the problem.",
                "The musician would _____ during the performance.",
                "She had to _____ when she lost her notes.",
                "He could _____ effectively in any situation.",
                "The team had to _____ after the equipment failed.",
                "She would _____ when she didn't have the right tools.",
                "He had to _____ a speech without preparation.",
                "The chef had to _____ when ingredients were missing."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "infatuate":
            custom_sentences = [
                "He became _____ with the beautiful singer.",
                "She was completely _____ by the new student.",
                "The _____ teenager couldn't stop thinking about her.",
                "He found himself _____ with her charm.",
                "She was _____ by his intelligence.",
                "The _____ young man wrote poems about her.",
                "He became _____ after their first meeting.",
                "She was _____ with the idea of adventure.",
                "The _____ pupil couldn't concentrate in class.",
                "He was _____ by her every word."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "initiate":
            custom_sentences = [
                "The company decided to _____ a new training programme.",
                "She would _____ the conversation with a question.",
                "He helped to _____ the changes needed.",
                "The school would _____ a new policy.",
                "She would _____ contact with the organisation.",
                "He decided to _____ the process immediately.",
                "The team would _____ the project next week.",
                "She would _____ discussions about the topic.",
                "He helped to _____ the new system.",
                "The group would _____ the plan together."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "injustice":
            custom_sentences = [
                "She fought against _____ throughout her life.",
                "The _____ of the situation was clear to everyone.",
                "He couldn't stand the _____ he witnessed.",
                "The _____ needed to be addressed immediately.",
                "She spoke out against the _____.",
                "The _____ affected many innocent people.",
                "He worked to correct the _____.",
                "The _____ was finally recognised.",
                "She dedicated herself to fighting _____.",
                "The _____ would not be tolerated."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "innuendo":
            custom_sentences = [
                "She made an _____ about his poor timekeeping.",
                "The _____ was subtle but understood by everyone.",
                "His _____ suggested something without saying it directly.",
                "The _____ was not appreciated by the recipient.",
                "She used _____ to hint at the problem.",
                "The _____ was clever but inappropriate.",
                "His _____ implied more than he stated.",
                "The _____ was lost on some listeners.",
                "She understood the _____ immediately.",
                "The _____ was meant to be humorous."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "insinuate":
            custom_sentences = [
                "She seemed to _____ that he was lying.",
                "He would _____ without making direct accusations.",
                "The comment would _____ something negative.",
                "She would _____ that others were to blame.",
                "His words would _____ doubt in their minds.",
                "The remark would _____ wrongdoing.",
                "She would _____ without being explicit.",
                "His tone would _____ disapproval.",
                "The statement would _____ a problem.",
                "She would _____ that changes were needed."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "inspiring":
            custom_sentences = [
                "Her _____ speech motivated the whole team.",
                "The _____ story encouraged others to try.",
                "His _____ example showed what was possible.",
                "The _____ teacher changed many lives.",
                "She found the message truly _____.",
                "The _____ leader brought out the best in people.",
                "His _____ words gave them hope.",
                "The _____ performance moved the audience.",
                "She was an _____ role model.",
                "The _____ moment would stay with them forever."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "instigate":
            custom_sentences = [
                "He was accused of trying to _____ a fight.",
                "She would _____ change through her actions.",
                "The comment would _____ an argument.",
                "He tried to _____ trouble between friends.",
                "The action would _____ a series of events.",
                "She would _____ the investigation.",
                "His words would _____ conflict.",
                "The decision would _____ protests.",
                "She would _____ the discussion.",
                "He tried to _____ improvements."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "insulting":
            custom_sentences = [
                "His _____ remarks hurt her feelings deeply.",
                "The _____ comment was completely uncalled for.",
                "She found his words extremely _____.",
                "The _____ behaviour was unacceptable.",
                "His _____ tone made everyone uncomfortable.",
                "The _____ joke was not funny at all.",
                "She was shocked by the _____ language.",
                "The _____ remark was meant to hurt.",
                "His _____ attitude was offensive.",
                "The _____ comment caused an argument."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "intercede":
            custom_sentences = [
                "The teacher had to _____ in the argument.",
                "She would _____ on behalf of her friend.",
                "He tried to _____ to prevent a fight.",
                "The parent would _____ to help resolve the dispute.",
                "She would _____ to stop the conflict.",
                "He decided to _____ before things got worse.",
                "The mediator would _____ between the parties.",
                "She would _____ to help find a solution.",
                "He tried to _____ to calm everyone down.",
                "The friend would _____ to restore peace."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "interpret":
            custom_sentences = [
                "The guide helped _____ the ancient symbols.",
                "She tried to _____ the meaning of the poem.",
                "He would _____ the data for the team.",
                "The expert would _____ the results.",
                "She learned to _____ body language.",
                "He would _____ the signs correctly.",
                "The teacher would _____ the text for the class.",
                "She tried to _____ his intentions.",
                "He would _____ the evidence carefully.",
                "The scholar would _____ the ancient writings."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "intervene":
            custom_sentences = [
                "The referee had to _____ to stop the fight.",
                "She decided to _____ before things got worse.",
                "He would _____ to help resolve the problem.",
                "The teacher would _____ in the dispute.",
                "She would _____ to prevent an accident.",
                "He had to _____ to stop the bullying.",
                "The parent would _____ when necessary.",
                "She would _____ to protect her friend.",
                "He decided to _____ at the right moment.",
                "The authority would _____ to maintain order."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "intimate":
            custom_sentences = [
                "They shared an _____ conversation over dinner.",
                "The _____ details were kept private.",
                "She had an _____ knowledge of the subject.",
                "The _____ gathering was for close friends only.",
                "He shared an _____ moment with his best friend.",
                "The _____ setting made everyone feel comfortable.",
                "She had an _____ understanding of the problem.",
                "The _____ relationship was special to them.",
                "He had an _____ connection with the topic.",
                "The _____ atmosphere was warm and welcoming."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "intrepid":
            custom_sentences = [
                "The _____ explorer ventured into the unknown jungle.",
                "Her _____ spirit led her to take risks.",
                "The _____ adventurer faced danger fearlessly.",
                "His _____ nature made him a natural leader.",
                "The _____ warrior never backed down.",
                "She showed _____ courage in the face of danger.",
                "The _____ traveller explored remote places.",
                "His _____ determination was inspiring.",
                "The _____ hero saved the day.",
                "She was known for her _____ adventures."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "intricate":
            custom_sentences = [
                "The _____ design took months to create.",
                "She admired the _____ patterns in the artwork.",
                "The _____ details required careful attention.",
                "His _____ plan was well thought out.",
                "The _____ structure was fascinating to study.",
                "She worked on the _____ puzzle for hours.",
                "The _____ mechanism was complex but beautiful.",
                "His _____ explanation covered every detail.",
                "The _____ web of connections was impressive.",
                "She appreciated the _____ craftsmanship."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "introvert":
            custom_sentences = [
                "As an _____, she preferred reading alone.",
                "The _____ enjoyed quiet activities.",
                "Her _____ nature made her seem shy.",
                "The _____ found large groups exhausting.",
                "She was a true _____ who needed time alone.",
                "The _____ preferred small gatherings.",
                "Her _____ personality was often misunderstood.",
                "The _____ needed solitude to recharge.",
                "She was an _____ who valued deep conversations.",
                "The _____ was comfortable in her own company."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "inundate":
            custom_sentences = [
                "The heavy rain threatened to _____ the small village.",
                "She would _____ them with questions.",
                "The requests would _____ the office.",
                "He would _____ her with compliments.",
                "The flood would _____ the entire area.",
                "She would _____ him with information.",
                "The emails would _____ her inbox.",
                "He would _____ them with suggestions.",
                "The water would _____ the fields.",
                "She would _____ the teacher with requests."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "jeopardy":
            custom_sentences = [
                "The company's future was in _____.",
                "She put her safety in _____ by taking risks.",
                "The project was in _____ due to lack of funding.",
                "His reputation was in _____ after the incident.",
                "The plan was in _____ of failing.",
                "She placed herself in _____ unnecessarily.",
                "The success was in _____ from the start.",
                "His position was in _____ after the mistake.",
                "The outcome was in _____ until the end.",
                "She realised her future was in _____."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "judicious":
            custom_sentences = [
                "A _____ use of resources saved the project.",
                "She made a _____ decision after careful thought.",
                "The _____ choice was the right one.",
                "His _____ approach solved the problem.",
                "The _____ use of time was efficient.",
                "She showed _____ judgement in the matter.",
                "The _____ selection was perfect.",
                "His _____ planning prevented problems.",
                "The _____ management led to success.",
                "She demonstrated _____ thinking throughout."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "juxtapose":
            custom_sentences = [
                "The artist liked to _____ old and new images.",
                "She would _____ the two ideas to show contrast.",
                "The teacher would _____ different examples.",
                "He would _____ the before and after photos.",
                "The writer would _____ different perspectives.",
                "She would _____ the two solutions.",
                "The designer would _____ colours effectively.",
                "He would _____ the different approaches.",
                "The curator would _____ artworks from different periods.",
                "She would _____ the contrasting viewpoints."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "labyrinth":
            custom_sentences = [
                "The old castle contained a _____ of corridors.",
                "She got lost in the _____ of streets.",
                "The _____ was designed to confuse visitors.",
                "He navigated the _____ carefully.",
                "The _____ of rules was difficult to understand.",
                "She found her way through the _____ eventually.",
                "The _____ seemed to have no end.",
                "He explored the _____ with curiosity.",
                "The _____ of tunnels was extensive.",
                "She was fascinated by the _____ structure."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "languish":
            custom_sentences = [
                "The plants began to _____ without water.",
                "She would _____ in prison for years.",
                "The project would _____ without proper support.",
                "He would _____ in obscurity.",
                "The idea would _____ forgotten.",
                "She would _____ in the hospital bed.",
                "The town would _____ after the factory closed.",
                "He would _____ without purpose.",
                "The talent would _____ unused.",
                "She would _____ in the difficult situation."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "lassitude":
            custom_sentences = [
                "After the long journey, she felt a deep _____ and needed to rest.",
                "The _____ made it difficult to concentrate.",
                "Her _____ was caused by the exhausting work.",
                "The _____ affected her ability to function.",
                "She struggled against the overwhelming _____.",
                "The _____ was more than just tiredness.",
                "Her _____ prevented her from being active.",
                "The _____ made everything seem difficult.",
                "She felt a sense of _____ after the illness.",
                "The _____ was hard to overcome."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "lethargic":
            custom_sentences = [
                "The hot weather made everyone feel _____.",
                "She felt _____ after the long day.",
                "The _____ student struggled to stay awake.",
                "His _____ behaviour worried his parents.",
                "The _____ mood affected the whole group.",
                "She was too _____ to do anything.",
                "The _____ response was disappointing.",
                "His _____ attitude slowed everything down.",
                "The _____ pace made progress difficult.",
                "She felt _____ and unmotivated."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "levity":
            custom_sentences = [
                "His _____ during the serious meeting was not appreciated.",
                "The _____ of the moment lightened the mood.",
                "She appreciated the _____ in difficult times.",
                "The _____ was inappropriate for the occasion.",
                "His _____ helped break the tension.",
                "The _____ made the situation more bearable.",
                "She found his _____ refreshing.",
                "The _____ was welcome after the stress.",
                "His _____ was sometimes misunderstood.",
                "The _____ provided relief from seriousness."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "loathsome":
            custom_sentences = [
                "The villain's _____ behaviour made everyone avoid him.",
                "She found the smell completely _____.",
                "The _____ act shocked everyone.",
                "His _____ attitude was repulsive.",
                "The _____ creature was feared by all.",
                "She thought the idea was _____.",
                "The _____ nature of the crime was appalling.",
                "His _____ comments were offensive.",
                "The _____ sight made her feel sick.",
                "She found his behaviour truly _____."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "ludicrous":
            custom_sentences = [
                "The _____ costume made everyone laugh.",
                "She found the idea completely _____.",
                "The _____ suggestion was immediately rejected.",
                "His _____ claim was unbelievable.",
                "The _____ situation was hard to take seriously.",
                "She thought the plan was absolutely _____.",
                "The _____ excuse didn't fool anyone.",
                "His _____ behaviour was ridiculous.",
                "The _____ proposal was laughed at.",
                "She found the whole thing utterly _____."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "luminous":
            custom_sentences = [
                "The _____ paint glowed in the darkness.",
                "Her _____ smile lit up the room.",
                "The _____ stars shone brightly overhead.",
                "His _____ personality was captivating.",
                "The _____ quality of the light was beautiful.",
                "She wore a _____ dress that caught everyone's attention.",
                "The _____ display was mesmerising.",
                "His _____ ideas were inspiring.",
                "The _____ colours were vibrant and bright.",
                "She had a _____ presence that drew people in."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "lustrous":
            custom_sentences = [
                "Her _____ hair shone in the sunlight.",
                "The _____ surface reflected the light beautifully.",
                "His _____ eyes sparkled with excitement.",
                "The _____ finish made the wood look expensive.",
                "She admired the _____ quality of the fabric.",
                "The _____ appearance was striking.",
                "His _____ smile was charming.",
                "The _____ sheen was impressive.",
                "She had _____ skin that glowed.",
                "The _____ texture was smooth and shiny."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "machinate":
            custom_sentences = [
                "The villains began to _____ against the hero.",
                "She would _____ to get what she wanted.",
                "The group would _____ secretly.",
                "He would _____ behind the scenes.",
                "The plotters would _____ against the king.",
                "She would _____ to undermine her rival.",
                "The conspirators would _____ together.",
                "He would _____ to achieve his goals.",
                "The group would _____ in secret.",
                "She would _____ to change the situation."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        elif word_lower == "magnetic":
            custom_sentences = [
                "She had a _____ personality that drew people to her.",
                "The _____ attraction was undeniable.",
                "His _____ charm made him popular.",
                "The _____ force pulled the objects together.",
                "She had a _____ presence that was captivating.",
                "The _____ quality made it stand out.",
                "His _____ appeal was obvious to everyone.",
                "The _____ nature of the material was useful.",
                "She had a _____ effect on those around her.",
                "The _____ personality was irresistible."
            ]
            sentences.extend(custom_sentences[:10-len(sentences)])
            break
        
        # If no custom sentences, use generic templates but make them contextual
        if len(sentences) < 10:
            # Fill remaining slots with contextual templates
            remaining = 10 - len(sentences)
            for i in range(remaining):
                if is_verb:
                    if meaning_keywords:
                        context = meaning_keywords[i % len(meaning_keywords)]
                        sentence = f"She decided to _____ when {context} became necessary."
                    else:
                        sentence = sentence_templates[i % len(sentence_templates)]
                elif is_adjective:
                    if meaning_keywords:
                        context = meaning_keywords[i % len(meaning_keywords)]
                        sentence = f"Her _____ {context} surprised everyone."
                    else:
                        sentence = sentence_templates[i % len(sentence_templates)]
                else:
                    if meaning_keywords:
                        context = meaning_keywords[i % len(meaning_keywords)]
                        sentence = f"The _____ {context} became clear as events unfolded."
                    else:
                        sentence = sentence_templates[i % len(sentence_templates)]
                
                sentences.append(sentence)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_sentences = []
    for sentence in sentences:
        if sentence not in seen:
            seen.add(sentence)
            unique_sentences.append(sentence)
    
    # If we have fewer than 10 sentences, generate more using templates
    while len(unique_sentences) < 10:
        # Generate additional contextual sentences
        if is_verb:
            additional = [
                f"They needed to _____ before the situation worsened.",
                f"She would _____ to achieve her goal.",
                f"He decided to _____ when the opportunity arose.",
                f"The team planned to _____ together.",
                f"She learned how to _____ through practice.",
                f"He would _____ if given the chance.",
                f"They wanted to _____ but weren't sure how.",
                f"She tried to _____ despite the obstacles.",
                f"He managed to _____ successfully.",
                f"They hoped to _____ in the future."
            ]
        elif is_adjective:
            additional = [
                f"The _____ quality was evident to all.",
                f"Her _____ nature was well-known.",
                f"The _____ aspect was important.",
                f"His _____ character was admirable.",
                f"The _____ feature stood out clearly.",
                f"She had a _____ way about her.",
                f"The _____ element was crucial.",
                f"His _____ trait was noticeable.",
                f"The _____ characteristic was unique.",
                f"She showed a _____ side to her personality."
            ]
        else:  # noun
            additional = [
                f"The _____ required careful consideration.",
                f"She understood the importance of the _____.",
                f"The _____ played a key role in events.",
                f"He explained the significance of the _____.",
                f"The _____ was central to the discussion.",
                f"She recognised the value of the _____.",
                f"The _____ influenced the outcome.",
                f"He appreciated the complexity of the _____.",
                f"The _____ was essential to understanding.",
                f"She studied the _____ in detail."
            ]
        
        for sent in additional:
            if sent not in seen and len(unique_sentences) < 10:
                seen.add(sent)
                unique_sentences.append(sent)
            if len(unique_sentences) >= 10:
                break
    
    # Ensure we have exactly 10 sentences
    return unique_sentences[:10]


def main():
    """Generate quiz sentences for Level 3 Batch 3 words."""
    input_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level3_batch3.txt")
    output_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level3_batch3.csv")
    
    # Read words from input file
    words_data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse: word|meaning|example|synonym|antonym
            parts = line.split('|')
            if len(parts) >= 3:
                word = parts[0].strip()
                meaning = parts[1].strip()
                example = parts[2].strip() if len(parts) > 2 else ""
                synonym = parts[3].strip() if len(parts) > 3 else ""
                antonym = parts[4].strip() if len(parts) > 4 else ""
                
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
        sentences = generate_sentences_for_word(
            word_data['word'],
            word_data['meaning'],
            word_data['example'],
            word_data['synonym'],
            word_data['antonym']
        )
        
        for sentence in sentences:
            all_sentences.append({
                'level': '3',
                'word': word_data['word'],
                'sentence': sentence
            })
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['level', 'word', 'sentence'])
        writer.writeheader()
        writer.writerows(all_sentences)
    
    print(f"Level 3 Batch 3 complete: {len(all_sentences)} sentences")


if __name__ == "__main__":
    main()
