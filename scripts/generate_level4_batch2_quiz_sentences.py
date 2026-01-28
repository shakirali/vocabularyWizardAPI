#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 4 Batch 2 vocabulary.
Creates 10 contextually rich sentences per word with varied structures.
"""

import csv
import re
from pathlib import Path

def create_blank_sentence(sentence: str, word: str) -> str:
    """Convert a sentence with the word into a fill-in-the-blank format."""
    if not sentence or not word:
        return ""
    
    word_lower = word.lower()
    word_patterns = [
        word,
        word.capitalize(),
        word.upper(),
        word_lower,
    ]
    
    # Add common word form variations
    if word_lower.endswith('e'):
        word_patterns.extend([
            word_lower + 'd',
            word_lower + 's',
            word_lower[:-1] + 'ing',
            word_lower[:-1] + 'ed',
            word_lower + 'ly',
            word_lower + 'ness',
        ])
    elif word_lower.endswith('y'):
        word_patterns.extend([
            word_lower[:-1] + 'ied',
            word_lower[:-1] + 'ies',
            word_lower[:-1] + 'ier',
            word_lower[:-1] + 'iest',
            word_lower + 'ly',
        ])
    elif word_lower.endswith('l'):
        word_patterns.extend([
            word_lower + 'ly',
            word_lower + 'ness',
        ])
    else:
        word_patterns.extend([
            word_lower + 'ed',
            word_lower + 's',
            word_lower + 'ing',
            word_lower + 'ly',
            word_lower + 'ness',
        ])
    
    # Handle doubling consonants
    if len(word_lower) > 2 and word_lower[-1] not in 'aeiou' and word_lower[-2] in 'aeiou':
        word_patterns.extend([
            word_lower + word_lower[-1] + "ed",
            word_lower + word_lower[-1] + "ing",
        ])
    
    result = sentence
    for pattern in sorted(set(word_patterns), key=len, reverse=True):
        regex = re.compile(r'\b' + re.escape(pattern) + r'\b', re.IGNORECASE)
        result = regex.sub("_____", result)
    
    return result


def generate_quiz_sentences(word: str, meaning: str, example: str, synonym: str, antonym: str) -> list:
    """
    Generate 10 high-quality quiz sentences for a word.
    Uses varied structures and strong contextual clues appropriate for Level 4.
    """
    sentences = []
    word_lower = word.lower()
    meaning_lower = meaning.lower()
    
    # Determine part of speech
    is_verb = meaning_lower.startswith("to ")
    is_adjective = any(marker in meaning_lower for marker in [
        "having", "showing", "full of", "characterised by", "characterized by",
        "very", "extremely", "quite", "rather", "causing", "deserving",
        "pleasant", "unpleasant", "friendly", "unfriendly", "poor", "rich",
        "large", "small", "important", "unimportant", "clear", "unclear"
    ])
    is_noun = not is_verb and not is_adjective
    
    # 1. Use the example sentence (convert to blank format)
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate additional sentences based on part of speech and meaning
    if is_verb:
        # Verb sentences - customize based on meaning
        if "light up" in meaning_lower or "make clear" in meaning_lower:
            verb_sentences = [
                f"The bright lamps _____ the entire hall during the evening performance.",
                f"Her explanation helped to _____ the complex problem for everyone.",
                f"The torch will _____ the dark path through the forest.",
                f"The teacher used diagrams to _____ the difficult concept.",
                f"Candles _____ the room with a warm, golden glow.",
                f"The streetlights _____ the road so drivers could see clearly.",
                f"Her detailed notes helped to _____ the confusing topic.",
                f"The sunrise began to _____ the eastern sky with brilliant colours.",
                f"The presentation slides helped to _____ the main points.",
                f"Flashlights _____ the cave entrance as they explored inside.",
            ]
        elif "begin" in meaning_lower or "introduce" in meaning_lower or "launch" in meaning_lower:
            verb_sentences = [
                f"The mayor will _____ the new library with a special ceremony.",
                f"They decided to _____ the school year with an assembly.",
                f"The headteacher will _____ the new policy next week.",
                f"They plan to _____ the festival with a grand opening.",
                f"The committee will _____ the new programme in September.",
                f"She was chosen to _____ the annual sports day.",
                f"The director will _____ the new play with a speech.",
                f"They will _____ the competition with a welcome address.",
                f"The president will _____ the conference tomorrow morning.",
                f"She was honoured to _____ the charity event.",
            ]
        else:
            # Generic verb sentences
            verb_sentences = [
                f"They decided to _____ after careful consideration.",
                f"She managed to _____ despite the challenges.",
                f"He refused to _____ even when pressured.",
                f"The team worked together to _____ the problem.",
                f"She learned to _____ through practice and patience.",
                f"They were forced to _____ when circumstances changed.",
                f"He chose to _____ because it was the right thing to do.",
                f"She hoped to _____ before the deadline.",
                f"They planned to _____ during the summer holidays.",
                f"He wanted to _____ to improve his skills.",
            ]
        
        for sent in verb_sentences:
            if len(sentences) < 10:
                blank_sent = create_blank_sentence(sent, word)
                if blank_sent and blank_sent not in sentences:
                    sentences.append(blank_sent)
    
    elif is_adjective:
        # Adjective sentences - customize based on meaning
        if "too high an opinion" in meaning_lower or "conceited" in meaning_lower:
            adj_sentences = [
                f"His _____ behaviour made it difficult for others to work with him.",
                f"The _____ actor only talked about his own achievements.",
                f"Her _____ attitude prevented her from making friends.",
                f"The _____ student thought he was better than everyone else.",
                f"His _____ comments about his own success annoyed the team.",
                f"She was so _____ that she couldn't accept any criticism.",
                f"The _____ musician refused to listen to others' suggestions.",
                f"His _____ manner made him unpopular with his classmates.",
                f"The _____ athlete boasted about every small victory.",
                f"Her _____ personality made it hard to have a conversation.",
            ]
        elif "great wickedness" in meaning_lower or "huge size" in meaning_lower:
            adj_sentences = [
                f"The _____ of the crime shocked the entire community.",
                f"People were stunned by the _____ of the natural disaster.",
                f"The _____ of the problem became clear over time.",
                f"Everyone was aware of the _____ of the challenge ahead.",
                f"The _____ of the mistake was only realised later.",
                f"They were overwhelmed by the _____ of the task.",
                f"The _____ of the situation required immediate action.",
                f"Nobody could ignore the _____ of what had happened.",
                f"The _____ of the decision weighed heavily on her mind.",
                f"They were shocked by the _____ of the damage.",
            ]
        elif "extremely large" in meaning_lower or "hugeness" in meaning_lower:
            adj_sentences = [
                f"The _____ of the whale amazed all the watchers.",
                f"Everyone was impressed by the _____ of the ancient tree.",
                f"The _____ of the mountain range stretched for miles.",
                f"They marvelled at the _____ of the cathedral.",
                f"The _____ of the ocean made them feel very small.",
                f"Visitors were stunned by the _____ of the castle.",
                f"The _____ of the dinosaur skeleton filled the museum hall.",
                f"They couldn't believe the _____ of the ancient monument.",
                f"The _____ of the waterfall was breathtaking.",
                f"Everyone was amazed by the _____ of the ancient ruins.",
            ]
        elif "mental calmness" in meaning_lower or "composure" in meaning_lower:
            adj_sentences = [
                f"She faced the difficult situation with remarkable _____.",
                f"His _____ during the crisis impressed everyone.",
                f"The teacher maintained her _____ despite the chaos.",
                f"She showed great _____ when receiving the bad news.",
                f"His _____ helped calm the worried students.",
                f"She handled the emergency with perfect _____.",
                f"His _____ in stressful situations was admirable.",
                f"She demonstrated _____ when others were panicking.",
                f"His _____ made him an excellent leader.",
                f"She showed _____ even when things went wrong.",
            ]
        elif "pleasant sounding" in meaning_lower or "melodious" in meaning_lower:
            adj_sentences = [
                f"The _____ melody drifted through the open window.",
                f"Her _____ voice made the song beautiful to hear.",
                f"The _____ sound of the birds filled the garden.",
                f"Everyone enjoyed the _____ music at the concert.",
                f"The _____ chimes rang out across the village.",
                f"Her _____ singing brought joy to everyone.",
                f"The _____ harmony of the choir was wonderful.",
                f"They listened to the _____ notes of the piano.",
                f"The _____ rhythm made everyone want to dance.",
                f"Her _____ laughter was music to their ears.",
            ]
        elif "careful assessment" in meaning_lower or "assessment" in meaning_lower:
            adj_sentences = [
                f"The teacher's _____ of her work was very positive.",
                f"After careful _____, they decided to proceed.",
                f"The _____ showed that improvements were needed.",
                f"Her _____ of the situation was thorough and fair.",
                f"The _____ revealed several important points.",
                f"After the _____, they made their final decision.",
                f"The _____ helped identify areas for improvement.",
                f"His _____ of the project was detailed and helpful.",
                f"The _____ process took several days to complete.",
                f"Her _____ was based on careful observation.",
            ]
        elif "quickly fading" in meaning_lower or "disappearing" in meaning_lower:
            adj_sentences = [
                f"The _____ rainbow disappeared within minutes.",
                f"Her _____ smile faded as she remembered the problem.",
                f"The _____ mist cleared as the sun rose.",
                f"His _____ hope vanished when he heard the news.",
                f"The _____ colours of the sunset were beautiful but brief.",
                f"Her _____ enthusiasm didn't last very long.",
                f"The _____ memory slipped away before he could capture it.",
                f"His _____ interest in the topic soon waned.",
                f"The _____ beauty of the flower lasted only a day.",
                f"Her _____ joy was replaced by disappointment.",
            ]
        elif "thorough and complete" in meaning_lower or "comprehensive" in meaning_lower:
            adj_sentences = [
                f"The police conducted an _____ search of the area.",
                f"Her _____ research covered every aspect of the topic.",
                f"The _____ investigation lasted for several months.",
                f"His _____ study of the subject impressed his teachers.",
                f"The _____ examination revealed all the details.",
                f"Her _____ analysis left no stone unturned.",
                f"The _____ review covered every possible angle.",
                f"His _____ preparation ensured he was ready for anything.",
                f"The _____ report included every relevant detail.",
                f"Her _____ approach to the problem was admirable.",
            ]
        elif "dying out" in meaning_lower or "disappearance" in meaning_lower:
            adj_sentences = [
                f"The _____ of dinosaurs happened millions of years ago.",
                f"Scientists are working to prevent the _____ of rare species.",
                f"The _____ of the ancient language was a great loss.",
                f"Conservation efforts aim to stop the _____ of endangered animals.",
                f"The _____ of traditional crafts worries many people.",
                f"They studied the causes of the _____ of the ancient civilisation.",
                f"The _____ of the old customs saddened the elders.",
                f"Efforts to prevent the _____ of the species are ongoing.",
                f"The _____ of the rare plant concerned botanists.",
                f"They documented the _____ of many historical traditions.",
            ]
        elif "not essential" in meaning_lower or "irrelevant" in meaning_lower:
            adj_sentences = [
                f"Remove any _____ details from your essay.",
                f"The teacher asked them to ignore _____ information.",
                f"His _____ comments didn't help solve the problem.",
                f"She removed all _____ elements from her presentation.",
                f"The _____ data was not included in the final report.",
                f"His _____ questions distracted from the main topic.",
                f"She focused on important points and ignored _____ ones.",
                f"The _____ material was cut from the final version.",
                f"His _____ remarks were not relevant to the discussion.",
                f"She eliminated all _____ information from her notes.",
            ]
        elif "very unusual" in meaning_lower or "remarkable" in meaning_lower:
            adj_sentences = [
                f"The _____ sunrise painted the sky pink and gold.",
                f"Her _____ talent amazed everyone who heard her play.",
                f"The _____ discovery changed everything they knew.",
                f"His _____ achievement was celebrated by everyone.",
                f"The _____ event would be remembered for years.",
                f"Her _____ courage inspired all who knew her.",
                f"The _____ performance left the audience speechless.",
                f"His _____ kindness touched many people's lives.",
                f"The _____ story captured everyone's imagination.",
                f"Her _____ determination helped her overcome every obstacle.",
            ]
        elif "lively energy" in meaning_lower or "enthusiasm" in meaning_lower:
            adj_sentences = [
                f"The children's _____ filled the playground with joy.",
                f"Her _____ for learning was infectious.",
                f"The _____ of the crowd was overwhelming.",
                f"His _____ made everyone feel more energetic.",
                f"The _____ of the celebration was wonderful to see.",
                f"Her _____ brightened everyone's day.",
                f"The _____ of the team was evident in their performance.",
                f"His _____ for the project inspired others.",
                f"The _____ of the festival was incredible.",
                f"Her _____ was matched only by her talent.",
            ]
        elif "based on false idea" in meaning_lower or "mistaken" in meaning_lower:
            adj_sentences = [
                f"The _____ argument did not convince anyone.",
                f"Her _____ reasoning led to the wrong conclusion.",
                f"The _____ belief was quickly disproven.",
                f"His _____ thinking caused many problems.",
                f"The _____ assumption turned out to be completely wrong.",
                f"Her _____ logic didn't stand up to scrutiny.",
                f"The _____ conclusion was based on incorrect information.",
                f"His _____ ideas were easily refuted.",
                f"The _____ theory was rejected by scientists.",
                f"Her _____ statements were proven false.",
            ]
        elif "excessive enthusiasm" in meaning_lower or "extremism" in meaning_lower:
            adj_sentences = [
                f"His _____ for the team was sometimes worrying.",
                f"The _____ of the supporters went too far.",
                f"Her _____ about the subject made others uncomfortable.",
                f"The _____ of the group was concerning.",
                f"His _____ prevented him from seeing other viewpoints.",
                f"The _____ of their beliefs was extreme.",
                f"Her _____ made it difficult to have a balanced discussion.",
                f"The _____ of the movement was well-known.",
                f"His _____ blinded him to reason.",
                f"The _____ of their approach was problematic.",
            ]
        elif "very concerned about accuracy" in meaning_lower or "meticulous" in meaning_lower:
            adj_sentences = [
                f"The _____ editor checked every word carefully.",
                f"Her _____ attention to detail impressed everyone.",
                f"The _____ scientist recorded every observation.",
                f"His _____ work was always flawless.",
                f"The _____ craftsman took great care with each piece.",
                f"Her _____ approach ensured perfect results.",
                f"The _____ student never missed a single detail.",
                f"His _____ nature made him excellent at his job.",
                f"The _____ artist spent hours on each brushstroke.",
                f"Her _____ preparation left nothing to chance.",
            ]
        elif "qualities associated with women" in meaning_lower or "womanhood" in meaning_lower:
            adj_sentences = [
                f"The ballet celebrated grace and _____.",
                f"Her _____ was evident in her gentle manner.",
                f"The _____ of her character was admired by many.",
                f"Her _____ shone through in everything she did.",
                f"The _____ of the performance was beautiful.",
                f"Her _____ was matched by her strength.",
                f"The _____ of her approach was appreciated.",
                f"Her _____ made her a role model for others.",
                f"The _____ of her nature was evident.",
                f"Her _____ was one of her greatest qualities.",
            ]
        elif "fierce and violent" in meaning_lower or "fierceness" in meaning_lower:
            adj_sentences = [
                f"The _____ of the storm surprised weather forecasters.",
                f"The _____ of the lion's roar was terrifying.",
                f"Her _____ in defending her friends was admirable.",
                f"The _____ of the attack shocked everyone.",
                f"His _____ on the football pitch was legendary.",
                f"The _____ of the debate was intense.",
                f"Her _____ determination helped her succeed.",
                f"The _____ of the competition was unexpected.",
                f"His _____ passion for justice was clear.",
                f"The _____ of her response surprised them all.",
            ]
        elif "not literal" in meaning_lower or "metaphorical" in meaning_lower:
            adj_sentences = [
                f"The poet used _____ language to describe his feelings.",
                f"Her _____ expression made the story more interesting.",
                f"The _____ meaning was different from the literal one.",
                f"His _____ speech was full of imagery.",
                f"The _____ description painted a vivid picture.",
                f"Her _____ way of speaking was poetic.",
                f"The _____ interpretation added depth to the text.",
                f"His _____ style made his writing unique.",
                f"The _____ language enriched the narrative.",
                f"Her _____ approach made the lesson memorable.",
            ]
        elif "bright colourful" in meaning_lower or "showy" in meaning_lower:
            adj_sentences = [
                f"The _____ costume attracted everyone's attention.",
                f"Her _____ personality made her stand out.",
                f"The _____ decorations brightened the entire room.",
                f"His _____ style was impossible to ignore.",
                f"The _____ display was spectacular.",
                f"Her _____ fashion sense was unique.",
                f"The _____ performance was unforgettable.",
                f"His _____ behaviour always drew attention.",
                f"The _____ colours of the painting were striking.",
                f"Her _____ entrance made everyone turn and look.",
            ]
        elif "gas in digestive system" in meaning_lower:
            adj_sentences = [
                f"The doctor asked about symptoms including _____.",
                f"Certain foods can cause uncomfortable _____.",
                f"The medication helped reduce the _____ problem.",
                f"Her diet changes improved the _____ issue.",
                f"The _____ was a side effect of the treatment.",
                f"Proper eating habits can prevent excessive _____.",
                f"The _____ discomfort was temporary.",
                f"Her _____ problem improved with dietary changes.",
                f"The _____ was caused by eating too quickly.",
                f"Reducing certain foods helped with the _____.",
            ]
        elif "inspiring fear or respect" in meaning_lower or "impressive" in meaning_lower:
            adj_sentences = [
                f"The _____ opponent seemed impossible to beat.",
                f"Her _____ reputation preceded her.",
                f"The _____ challenge required all their skills.",
                f"His _____ presence commanded attention.",
                f"The _____ task tested their abilities.",
                f"Her _____ knowledge impressed everyone.",
                f"The _____ obstacle blocked their path.",
                f"His _____ achievements were well-known.",
                f"The _____ mountain peak loomed ahead.",
                f"Her _____ determination was unmatched.",
            ]
        elif "direct and honest" in meaning_lower:
            adj_sentences = [
                f"Her _____ manner made her easy to trust.",
                f"His _____ answer surprised everyone.",
                f"The _____ approach was refreshing.",
                f"Her _____ honesty was appreciated.",
                f"His _____ comments were always welcome.",
                f"The _____ discussion cleared up misunderstandings.",
                f"Her _____ way of speaking was respected.",
                f"His _____ response showed his character.",
                f"The _____ conversation was productive.",
                f"Her _____ feedback helped improve the work.",
            ]
        elif "happening by lucky chance" in meaning_lower or "lucky" in meaning_lower:
            adj_sentences = [
                f"Their _____ meeting led to a lifelong friendship.",
                f"The _____ discovery changed everything.",
                f"Her _____ arrival saved the day.",
                f"The _____ timing was perfect.",
                f"His _____ encounter was unexpected.",
                f"The _____ coincidence amazed everyone.",
                f"Her _____ find was valuable.",
                f"The _____ opportunity came at just the right time.",
                f"His _____ success was unexpected.",
                f"The _____ turn of events was welcome.",
            ]
        elif "obtained by deception" in meaning_lower or "fake" in meaning_lower:
            adj_sentences = [
                f"The _____ documents were discovered by the police.",
                f"Her _____ claims were exposed.",
                f"The _____ signature was easily detected.",
                f"His _____ behaviour was illegal.",
                f"The _____ transaction was stopped.",
                f"Her _____ activities were uncovered.",
                f"The _____ scheme was discovered.",
                f"His _____ actions had serious consequences.",
                f"The _____ certificate was worthless.",
                f"Her _____ attempt failed.",
            ]
        elif "careful use of money" in meaning_lower or "thriftiness" in meaning_lower:
            adj_sentences = [
                f"Their _____ during hard times helped them survive.",
                f"Her _____ allowed her to save money.",
                f"The _____ approach prevented waste.",
                f"His _____ habits were admirable.",
                f"The _____ lifestyle suited them well.",
                f"Her _____ management of resources was wise.",
                f"The _____ spending kept them out of debt.",
                f"His _____ nature helped the family.",
                f"The _____ use of materials was efficient.",
                f"Her _____ planning ensured success.",
            ]
        elif "enormous in size" in meaning_lower or "huge" in meaning_lower:
            adj_sentences = [
                f"The _____ meal could feed an entire family.",
                f"Her _____ appetite surprised everyone.",
                f"The _____ building dominated the skyline.",
                f"His _____ collection filled several rooms.",
                f"The _____ task required many helpers.",
                f"Her _____ effort paid off in the end.",
                f"The _____ project took years to complete.",
                f"His _____ achievement was celebrated.",
                f"The _____ structure was impressive.",
                f"Her _____ contribution was invaluable.",
            ]
        elif "study of family history" in meaning_lower or "ancestry" in meaning_lower:
            adj_sentences = [
                f"She spent years researching her family's _____.",
                f"The _____ revealed interesting connections.",
                f"His _____ research traced back centuries.",
                f"The _____ showed their royal heritage.",
                f"Her _____ project was fascinating.",
                f"The _____ records were carefully preserved.",
                f"His _____ investigation uncovered secrets.",
                f"The _____ tree was extensive.",
                f"Her _____ work was published.",
                f"The _____ documents were valuable.",
            ]
        elif "politeness and good manners" in meaning_lower or "refinement" in meaning_lower:
            adj_sentences = [
                f"Her _____ and grace impressed everyone at dinner.",
                f"The _____ of her behaviour was evident.",
                f"His _____ made him popular.",
                f"The _____ of the occasion was clear.",
                f"Her _____ was natural and genuine.",
                f"The _____ of her speech was admirable.",
                f"His _____ manners were well-known.",
                f"The _____ of her approach was appreciated.",
                f"Her _____ character shone through.",
                f"The _____ of the gathering was notable.",
            ]
        elif "eating and drinking excessively" in meaning_lower or "greedy" in meaning_lower:
            adj_sentences = [
                f"His _____ appetite amazed everyone at the feast.",
                f"The _____ behaviour was concerning.",
                f"Her _____ consumption was unhealthy.",
                f"The _____ eating habits needed to change.",
                f"His _____ nature was well-known.",
                f"The _____ indulgence was excessive.",
                f"Her _____ appetite was remarkable.",
                f"The _____ consumption worried doctors.",
                f"His _____ habits were problematic.",
                f"The _____ behaviour was inappropriate.",
            ]
        elif "giving pleasure" in meaning_lower or "satisfying" in meaning_lower:
            adj_sentences = [
                f"It was _____ to see all the hard work pay off.",
                f"Her _____ smile showed her happiness.",
                f"The _____ result made everyone happy.",
                f"His _____ achievement was celebrated.",
                f"The _____ outcome was worth the effort.",
                f"Her _____ success inspired others.",
                f"The _____ moment was unforgettable.",
                f"His _____ progress was evident.",
                f"The _____ experience was rewarding.",
                f"Her _____ accomplishment was impressive.",
            ]
        elif "unnecessary" in meaning_lower or "uncalled for" in meaning_lower:
            adj_sentences = [
                f"The violence in the film was _____ and disturbing.",
                f"Her _____ comments were inappropriate.",
                f"The _____ addition didn't improve the story.",
                f"His _____ remarks offended people.",
                f"The _____ scene was unnecessary.",
                f"Her _____ behaviour was unwelcome.",
                f"The _____ detail added nothing.",
                f"His _____ actions were pointless.",
                f"The _____ element was removed.",
                f"Her _____ gesture was misunderstood.",
            ]
        elif "enjoying company" in meaning_lower or "sociable" in meaning_lower:
            adj_sentences = [
                f"The _____ puppy loved playing with other dogs.",
                f"Her _____ nature made her popular.",
                f"The _____ child made friends easily.",
                f"His _____ personality was infectious.",
                f"The _____ atmosphere was welcoming.",
                f"Her _____ behaviour was natural.",
                f"The _____ gathering was enjoyable.",
                f"His _____ manner put people at ease.",
                f"The _____ event brought people together.",
                f"Her _____ character made her a good friend.",
            ]
        elif "forming pleasant whole" in meaning_lower or "peaceful" in meaning_lower:
            adj_sentences = [
                f"The _____ colours created a beautiful painting.",
                f"Her _____ voice blended perfectly with the music.",
                f"The _____ relationship worked well.",
                f"His _____ approach resolved conflicts.",
                f"The _____ atmosphere was calming.",
                f"Her _____ nature made her easy to work with.",
                f"The _____ combination was perfect.",
                f"His _____ style complemented others.",
                f"The _____ blend was successful.",
                f"Her _____ manner created peace.",
            ]
        elif "proud and arrogant" in meaning_lower or "arrogance" in meaning_lower:
            adj_sentences = [
                f"Her _____ made it difficult to make friends.",
                f"The _____ of his behaviour was off-putting.",
                f"His _____ attitude alienated others.",
                f"The _____ in her voice was clear.",
                f"Her _____ prevented her from learning.",
                f"The _____ of his manner was obvious.",
                f"His _____ comments offended people.",
                f"The _____ in her expression was evident.",
                f"Her _____ made her unpopular.",
                f"The _____ of his behaviour was unacceptable.",
            ]
        elif "arranged in order" in meaning_lower or "ranked" in meaning_lower:
            adj_sentences = [
                f"The _____ structure had many levels of management.",
                f"Her _____ organisation was efficient.",
                f"The _____ system made sense.",
                f"His _____ approach was logical.",
                f"The _____ arrangement was clear.",
                f"Her _____ method worked well.",
                f"The _____ order was established.",
                f"His _____ structure was effective.",
                f"The _____ organisation was successful.",
                f"Her _____ system was well-designed.",
            ]
        elif "all of same kind" in meaning_lower or "uniform" in meaning_lower:
            adj_sentences = [
                f"The _____ mixture had no visible differences.",
                f"Her _____ group worked well together.",
                f"The _____ population shared similar characteristics.",
                f"His _____ collection was impressive.",
                f"The _____ sample was consistent.",
                f"Her _____ approach was standardised.",
                f"The _____ nature of the group was clear.",
                f"His _____ selection was uniform.",
                f"The _____ composition was identical.",
                f"Her _____ method produced consistent results.",
            ]
        elif "extremely unpleasant" in meaning_lower or "terrible" in meaning_lower:
            adj_sentences = [
                f"The _____ weather ruined the outdoor event.",
                f"Her _____ mistake caused problems.",
                f"The _____ accident shocked everyone.",
                f"His _____ behaviour was unacceptable.",
                f"The _____ conditions made work difficult.",
                f"Her _____ performance disappointed everyone.",
                f"The _____ situation was dire.",
                f"His _____ actions had consequences.",
                f"The _____ outcome was devastating.",
                f"Her _____ error was costly.",
            ]
        elif "friendly and welcoming" in meaning_lower or "welcoming" in meaning_lower:
            adj_sentences = [
                f"The _____ family invited us to stay for dinner.",
                f"Her _____ nature made visitors feel at home.",
                f"The _____ atmosphere was pleasant.",
                f"His _____ manner was appreciated.",
                f"The _____ reception was warm.",
                f"Her _____ behaviour was genuine.",
                f"The _____ environment was comfortable.",
                f"His _____ attitude was welcoming.",
                f"The _____ treatment was kind.",
                f"Her _____ personality made her popular.",
            ]
        elif "unfriendly and aggressive" in meaning_lower or "aggression" in meaning_lower:
            adj_sentences = [
                f"There was open _____ between the rival groups.",
                f"The _____ of his response was unexpected.",
                f"Her _____ made others uncomfortable.",
                f"The _____ in the room was palpable.",
                f"His _____ behaviour was concerning.",
                f"The _____ between them was clear.",
                f"Her _____ attitude created problems.",
                f"The _____ of the situation was tense.",
                f"His _____ response escalated the conflict.",
                f"The _____ made cooperation impossible.",
            ]
        elif "behaving like hypocrite" in meaning_lower or "insincere" in meaning_lower:
            adj_sentences = [
                f"It was _____ to criticise others for being late.",
                f"Her _____ behaviour was exposed.",
                f"The _____ nature of his actions was clear.",
                f"His _____ comments were insincere.",
                f"The _____ attitude was obvious.",
                f"Her _____ stance was inconsistent.",
                f"The _____ behaviour was disappointing.",
                f"His _____ words didn't match his actions.",
                f"The _____ nature was revealed.",
                f"Her _____ approach was criticised.",
            ]
        elif "based on imagination" in meaning_lower or "theoretical" in meaning_lower:
            adj_sentences = [
                f"We discussed a _____ situation in class.",
                f"Her _____ question made everyone think.",
                f"The _____ scenario was interesting.",
                f"His _____ example helped explain the concept.",
                f"The _____ case study was useful.",
                f"Her _____ approach was creative.",
                f"The _____ situation was unlikely.",
                f"His _____ thinking was advanced.",
                f"The _____ problem was challenging.",
                f"Her _____ idea was innovative.",
            ]
        elif "wildly emotional" in meaning_lower or "frantic" in meaning_lower:
            adj_sentences = [
                f"The children became _____ with excitement.",
                f"Her _____ reaction was over the top.",
                f"The _____ laughter filled the room.",
                f"His _____ behaviour was concerning.",
                f"The _____ response was unexpected.",
                f"Her _____ state made others worried.",
                f"The _____ reaction was extreme.",
                f"His _____ manner was unusual.",
                f"The _____ behaviour was inappropriate.",
                f"Her _____ response was excessive.",
            ]
        elif "peculiar personal habit" in meaning_lower or "quirk" in meaning_lower:
            adj_sentences = [
                f"Her _____ of humming while working amused colleagues.",
                f"The _____ was endearing.",
                f"His _____ made him unique.",
                f"The _____ was harmless but noticeable.",
                f"Her _____ became well-known.",
                f"The _____ was part of his character.",
                f"His _____ amused everyone.",
                f"The _____ was charming.",
                f"Her _____ was distinctive.",
                f"The _____ made him memorable.",
            ]
        elif "deserving public disgrace" in meaning_lower or "shameful" in meaning_lower:
            adj_sentences = [
                f"The team suffered an _____ defeat.",
                f"Her _____ behaviour was exposed.",
                f"The _____ end was humiliating.",
                f"His _____ actions were condemned.",
                f"The _____ failure was public.",
                f"Her _____ mistake was embarrassing.",
                f"The _____ outcome was disgraceful.",
                f"His _____ conduct was unacceptable.",
                f"The _____ result was shameful.",
                f"Her _____ performance was poor.",
            ]
        elif "famous and admired" in meaning_lower:
            adj_sentences = [
                f"The _____ scientist won many awards.",
                f"Her _____ career was celebrated.",
                f"The _____ author was well-known.",
                f"His _____ achievements were recognised.",
                f"The _____ leader was respected.",
                f"Her _____ reputation was deserved.",
                f"The _____ artist was honoured.",
                f"His _____ work was influential.",
                f"The _____ figure was admired.",
                f"Her _____ status was earned.",
            ]
        elif "lack of balance" in meaning_lower or "inequality" in meaning_lower:
            adj_sentences = [
                f"There was an _____ in the distribution of resources.",
                f"The _____ was noticeable.",
                f"Her _____ approach caused problems.",
                f"The _____ in power was clear.",
                f"His _____ lifestyle affected his health.",
                f"The _____ made things difficult.",
                f"Her _____ diet was unhealthy.",
                f"The _____ was corrected.",
                f"His _____ work schedule was problematic.",
                f"The _____ needed to be addressed.",
            ]
        elif "perfectly clean" in meaning_lower or "spotless" in meaning_lower:
            adj_sentences = [
                f"Her _____ bedroom impressed her parents.",
                f"The _____ kitchen sparkled.",
                f"His _____ uniform was perfect.",
                f"The _____ condition was maintained.",
                f"Her _____ appearance was impressive.",
                f"The _____ state was remarkable.",
                f"His _____ work was flawless.",
                f"The _____ cleanliness was notable.",
                f"Her _____ organisation was perfect.",
                f"The _____ presentation was excellent.",
            ]
        elif "about to happen" in meaning_lower or "impending" in meaning_lower:
            adj_sentences = [
                f"The _____ storm forced everyone indoors.",
                f"Her _____ arrival was expected.",
                f"The _____ deadline was approaching.",
                f"His _____ departure was announced.",
                f"The _____ change was inevitable.",
                f"Her _____ exam was next week.",
                f"The _____ event was scheduled.",
                f"His _____ decision was awaited.",
                f"The _____ arrival was imminent.",
                f"Her _____ success was certain.",
            ]
        elif "unchangeable" in meaning_lower or "unchanging" in meaning_lower:
            adj_sentences = [
                f"The laws of physics are _____.",
                f"Her _____ principles guided her.",
                f"The _____ rules were followed.",
                f"His _____ nature was well-known.",
                f"The _____ truth was accepted.",
                f"Her _____ commitment was clear.",
                f"The _____ fact was undeniable.",
                f"His _____ stance was firm.",
                f"The _____ law was absolute.",
                f"Her _____ belief was strong.",
            ]
        elif "fair and not favouring" in meaning_lower:
            adj_sentences = [
                f"The judge must be _____ when deciding cases.",
                f"Her _____ opinion was valued.",
                f"The _____ decision was fair.",
                f"His _____ approach was respected.",
                f"The _____ treatment was equal.",
                f"Her _____ judgement was trusted.",
                f"The _____ assessment was accurate.",
                f"His _____ view was balanced.",
                f"The _____ evaluation was fair.",
                f"Her _____ analysis was objective.",
            ]
        elif "showing no emotion" in meaning_lower or "emotionless" in meaning_lower:
            adj_sentences = [
                f"Her _____ face revealed nothing about her thoughts.",
                f"The _____ expression was unreadable.",
                f"His _____ manner was unusual.",
                f"The _____ response was unexpected.",
                f"Her _____ behaviour was puzzling.",
                f"The _____ reaction was strange.",
                f"His _____ appearance was calm.",
                f"The _____ demeanour was controlled.",
                f"Her _____ attitude was neutral.",
                f"The _____ response was blank.",
            ]
        elif "faultless and perfect" in meaning_lower or "flawless" in meaning_lower:
            adj_sentences = [
                f"His _____ manners impressed everyone at dinner.",
                f"Her _____ performance was perfect.",
                f"The _____ execution was flawless.",
                f"His _____ work was excellent.",
                f"The _____ record was impressive.",
                f"Her _____ behaviour was exemplary.",
                f"The _____ quality was outstanding.",
                f"His _____ style was refined.",
                f"The _____ presentation was perfect.",
                f"Her _____ character was admirable.",
            ]
        elif "having little money" in meaning_lower or "poor" in meaning_lower:
            adj_sentences = [
                f"The _____ student worked part-time to pay for books.",
                f"Her _____ circumstances were difficult.",
                f"The _____ family needed help.",
                f"His _____ situation was temporary.",
                f"The _____ conditions were challenging.",
                f"Her _____ state was known.",
                f"The _____ background was humble.",
                f"His _____ status didn't stop him.",
                f"The _____ situation improved.",
                f"Her _____ means were limited.",
            ]
        elif "extremely important" in meaning_lower or "essential" in meaning_lower:
            adj_sentences = [
                f"It is _____ to follow the safety instructions.",
                f"Her _____ role was crucial.",
                f"The _____ task must be completed.",
                f"His _____ contribution was vital.",
                f"The _____ need was urgent.",
                f"Her _____ duty was clear.",
                f"The _____ requirement was mandatory.",
                f"His _____ action was necessary.",
                f"The _____ step was critical.",
                f"Her _____ responsibility was important.",
            ]
        elif "impossible to see" in meaning_lower or "unnoticeable" in meaning_lower:
            adj_sentences = [
                f"The change was so gradual it was almost _____.",
                f"Her _____ improvement was slow.",
                f"The _____ difference was tiny.",
                f"His _____ progress was steady.",
                f"The _____ shift was subtle.",
                f"Her _____ change was gradual.",
                f"The _____ movement was slight.",
                f"His _____ adjustment was minor.",
                f"The _____ variation was minimal.",
                f"Her _____ modification was small.",
            ]
        elif "arrogant and domineering" in meaning_lower or "commanding" in meaning_lower:
            adj_sentences = [
                f"Her _____ manner made her unpopular with colleagues.",
                f"The _____ attitude was off-putting.",
                f"His _____ behaviour was unacceptable.",
                f"The _____ tone was harsh.",
                f"Her _____ style was disliked.",
                f"The _____ approach was resented.",
                f"His _____ manner was arrogant.",
                f"The _____ attitude was domineering.",
                f"Her _____ behaviour was criticised.",
                f"The _____ style was inappropriate.",
            ]
        elif "not allowing liquid" in meaning_lower or "waterproof" in meaning_lower:
            adj_sentences = [
                f"The _____ material kept the water out.",
                f"Her _____ coat protected her from rain.",
                f"The _____ barrier was effective.",
                f"His _____ boots stayed dry.",
                f"The _____ layer prevented leaks.",
                f"Her _____ covering was reliable.",
                f"The _____ seal was tight.",
                f"His _____ protection worked well.",
                f"The _____ surface repelled water.",
                f"Her _____ material was durable.",
            ]
        elif "not affected by" in meaning_lower or "unaffected" in meaning_lower:
            adj_sentences = [
                f"He seemed _____ to criticism and continued regardless.",
                f"Her _____ attitude was remarkable.",
                f"The _____ surface resisted damage.",
                f"His _____ nature was unusual.",
                f"The _____ material was strong.",
                f"Her _____ response was calm.",
                f"The _____ barrier was effective.",
                f"His _____ character was resilient.",
                f"The _____ coating protected it.",
                f"Her _____ manner was impressive.",
            ]
        elif "acting quickly without thinking" in meaning_lower or "rash" in meaning_lower:
            adj_sentences = [
                f"His _____ decision caused many problems later.",
                f"Her _____ action was regretted.",
                f"The _____ choice was unwise.",
                f"His _____ behaviour was risky.",
                f"The _____ move was dangerous.",
                f"Her _____ response was hasty.",
                f"The _____ act was foolish.",
                f"His _____ nature caused trouble.",
                f"The _____ decision was regretted.",
                f"Her _____ impulse was wrong.",
            ]
        elif "not believable" in meaning_lower or "unbelievable" in meaning_lower:
            adj_sentences = [
                f"The _____ excuse did not convince anyone.",
                f"Her _____ story was rejected.",
                f"The _____ claim was dismissed.",
                f"His _____ explanation was doubted.",
                f"The _____ account was false.",
                f"Her _____ statement was questioned.",
                f"The _____ theory was rejected.",
                f"His _____ argument was weak.",
                f"The _____ reason was unconvincing.",
                f"Her _____ excuse was unbelievable.",
            ]
        elif "without being directly stated" in meaning_lower or "indirectly" in meaning_lower:
            adj_sentences = [
                f"She _____ agreed by not objecting.",
                f"Her _____ consent was understood.",
                f"The _____ approval was assumed.",
                f"His _____ agreement was implied.",
                f"The _____ acceptance was clear.",
                f"Her _____ permission was given.",
                f"The _____ consent was inferred.",
                f"His _____ approval was understood.",
                f"The _____ agreement was unspoken.",
                f"Her _____ acceptance was assumed.",
            ]
        elif "extremely poor" in meaning_lower:
            adj_sentences = [
                f"The _____ village needed urgent aid.",
                f"Her _____ circumstances were dire.",
                f"The _____ conditions were terrible.",
                f"His _____ state was concerning.",
                f"The _____ area needed help.",
                f"Her _____ situation was desperate.",
                f"The _____ community required assistance.",
                f"His _____ background was difficult.",
                f"The _____ region was struggling.",
                f"Her _____ family needed support.",
            ]
        elif "soaked with substance" in meaning_lower or "saturated" in meaning_lower:
            adj_sentences = [
                f"The cloth was _____ with waterproofing liquid.",
                f"Her hair was _____ with water.",
                f"The sponge was _____ with cleaning solution.",
                f"His clothes were _____ with sweat.",
                f"The material was _____ with oil.",
                f"Her towel was _____ with moisture.",
                f"The paper was _____ with ink.",
                f"His bandage was _____ with medicine.",
                f"The fabric was _____ with dye.",
                f"Her sponge was _____ with soap.",
            ]
        elif "not showing care" in meaning_lower or "unwise" in meaning_lower:
            adj_sentences = [
                f"It was _____ to spend all his savings at once.",
                f"Her _____ decision was regretted.",
                f"The _____ choice was foolish.",
                f"His _____ behaviour was risky.",
                f"The _____ action was unwise.",
                f"Her _____ spending was problematic.",
                f"The _____ move was dangerous.",
                f"His _____ approach was careless.",
                f"The _____ decision was regretted.",
                f"Her _____ choice was unwise.",
            ]
        elif "rude behaviour" in meaning_lower or "rudeness" in meaning_lower:
            adj_sentences = [
                f"His _____ in answering back shocked the teacher.",
                f"The _____ of his response was unacceptable.",
                f"Her _____ was inappropriate.",
                f"The _____ in his tone was clear.",
                f"His _____ behaviour was punished.",
                f"The _____ of her comment was shocking.",
                f"His _____ made him unpopular.",
                f"The _____ was not tolerated.",
                f"Her _____ resulted in detention.",
                f"The _____ was disrespectful.",
            ]
        elif "rude and disrespectful" in meaning_lower or "cheeky" in meaning_lower:
            adj_sentences = [
                f"The _____ child refused to apologise.",
                f"Her _____ behaviour was unacceptable.",
                f"The _____ response was inappropriate.",
                f"His _____ attitude was punished.",
                f"The _____ comment was rude.",
                f"Her _____ manner was disrespectful.",
                f"The _____ reply was cheeky.",
                f"His _____ behaviour was unacceptable.",
                f"The _____ answer was insolent.",
                f"Her _____ attitude was wrong.",
            ]
        elif "not correct" in meaning_lower or "incorrect" in meaning_lower:
            adj_sentences = [
                f"The _____ report contained several errors.",
                f"Her _____ answer was marked wrong.",
                f"The _____ information was misleading.",
                f"His _____ statement was false.",
                f"The _____ data was corrected.",
                f"Her _____ calculation was wrong.",
                f"The _____ measurement was off.",
                f"His _____ assumption was incorrect.",
                f"The _____ record was updated.",
                f"Her _____ information was revised.",
            ]
        elif "not enough" in meaning_lower or "insufficient" in meaning_lower:
            adj_sentences = [
                f"The _____ lighting made reading difficult.",
                f"Her _____ preparation showed.",
                f"The _____ resources were a problem.",
                f"His _____ effort was disappointing.",
                f"The _____ supply ran out quickly.",
                f"Her _____ knowledge was evident.",
                f"The _____ amount was insufficient.",
                f"His _____ response was weak.",
                f"The _____ support was lacking.",
                f"Her _____ explanation was incomplete.",
            ]
        elif "by accident" in meaning_lower or "accidentally" in meaning_lower:
            adj_sentences = [
                f"She _____ deleted the important file.",
                f"Her _____ mistake was understandable.",
                f"The _____ error was corrected.",
                f"His _____ action caused problems.",
                f"The _____ deletion was unfortunate.",
                f"Her _____ slip was harmless.",
                f"The _____ omission was noticed.",
                f"His _____ mistake was fixed.",
                f"The _____ error was accidental.",
                f"Her _____ action was unintentional.",
            ]
        elif "not paying attention" in meaning_lower or "distracted" in meaning_lower:
            adj_sentences = [
                f"The _____ student missed the instructions.",
                f"Her _____ behaviour was noticed.",
                f"The _____ pupil was daydreaming.",
                f"His _____ manner was obvious.",
                f"The _____ attitude was problematic.",
                f"Her _____ state was concerning.",
                f"The _____ behaviour was disruptive.",
                f"His _____ nature affected his work.",
                f"The _____ student needed help.",
                f"Her _____ approach was ineffective.",
            ]
        elif "too quiet to be heard" in meaning_lower or "silent" in meaning_lower:
            adj_sentences = [
                f"Her whisper was _____ in the noisy room.",
                f"The _____ sound was inaudible.",
                f"His _____ voice couldn't be heard.",
                f"The _____ noise was too quiet.",
                f"Her _____ speech was unheard.",
                f"The _____ comment was missed.",
                f"His _____ remark was silent.",
                f"The _____ sound was imperceptible.",
                f"Her _____ voice was too soft.",
                f"The _____ whisper was inaudible.",
            ]
        elif "marking the beginning" in meaning_lower or "opening" in meaning_lower:
            adj_sentences = [
                f"The _____ meeting of the new club was well attended.",
                f"Her _____ speech was inspiring.",
                f"The _____ event was successful.",
                f"His _____ performance was memorable.",
                f"The _____ ceremony was grand.",
                f"Her _____ address was well-received.",
                f"The _____ celebration was festive.",
                f"His _____ appearance was notable.",
                f"The _____ gathering was important.",
                f"Her _____ presentation was excellent.",
            ]
        elif "something that motivates" in meaning_lower or "motivation" in meaning_lower:
            adj_sentences = [
                f"The bonus was a good _____ to work harder.",
                f"Her _____ was strong.",
                f"The _____ reward encouraged effort.",
                f"His _____ was clear.",
                f"The _____ prize motivated everyone.",
                f"Her _____ was effective.",
                f"The _____ benefit was attractive.",
                f"His _____ was powerful.",
                f"The _____ opportunity was appealing.",
                f"Her _____ was compelling.",
            ]
        elif "continuing without stopping" in meaning_lower or "constant" in meaning_lower:
            adj_sentences = [
                f"The _____ rain lasted for three days.",
                f"Her _____ talking was annoying.",
                f"The _____ noise was disturbing.",
                f"His _____ complaints were tiresome.",
                f"The _____ chatter was endless.",
                f"Her _____ questions were exhausting.",
                f"The _____ interruptions were disruptive.",
                f"His _____ demands were unreasonable.",
                f"The _____ activity was non-stop.",
                f"Her _____ energy was remarkable.",
            ]
        elif "happening by chance" in meaning_lower or "accidental" in meaning_lower:
            adj_sentences = [
                f"The _____ costs were more than expected.",
                f"Her _____ discovery was valuable.",
                f"The _____ meeting was fortunate.",
                f"His _____ find was interesting.",
                f"The _____ benefit was welcome.",
                f"Her _____ encounter was unexpected.",
                f"The _____ advantage was helpful.",
                f"His _____ discovery was important.",
                f"The _____ outcome was positive.",
                f"Her _____ benefit was useful.",
            ]
        elif "surgical cut" in meaning_lower:
            adj_sentences = [
                f"The surgeon made a small _____ to begin the operation.",
                f"Her _____ healed quickly.",
                f"The _____ was precise.",
                f"His _____ was necessary.",
                f"The _____ was clean.",
                f"Her _____ was small.",
                f"The _____ was made carefully.",
                f"His _____ was successful.",
                f"The _____ was neat.",
                f"Her _____ was expertly done.",
            ]
        elif "clear and direct" in meaning_lower or "sharp" in meaning_lower:
            adj_sentences = [
                f"Her _____ questions revealed the truth quickly.",
                f"The _____ analysis was helpful.",
                f"His _____ comments were valuable.",
                f"The _____ observation was accurate.",
                f"Her _____ thinking was clear.",
                f"The _____ critique was constructive.",
                f"His _____ remarks were insightful.",
                f"The _____ assessment was precise.",
                f"Her _____ analysis was sharp.",
                f"The _____ comment was penetrating.",
            ]
        elif "including everyone" in meaning_lower or "comprehensive" in meaning_lower:
            adj_sentences = [
                f"The school promotes _____ education for all abilities.",
                f"Her _____ approach was welcomed.",
                f"The _____ policy was fair.",
                f"His _____ attitude was appreciated.",
                f"The _____ environment was supportive.",
                f"Her _____ method was effective.",
                f"The _____ programme was successful.",
                f"His _____ view was balanced.",
                f"The _____ approach was positive.",
                f"Her _____ style was inclusive.",
            ]
        elif "unclear and difficult" in meaning_lower or "confused" in meaning_lower:
            adj_sentences = [
                f"His _____ explanation made no sense at all.",
                f"Her _____ speech was confusing.",
                f"The _____ message was unclear.",
                f"His _____ response was muddled.",
                f"The _____ argument was jumbled.",
                f"Her _____ writing was difficult to follow.",
                f"The _____ statement was confusing.",
                f"His _____ reasoning was unclear.",
                f"The _____ explanation was garbled.",
                f"Her _____ answer was incoherent.",
            ]
        elif "not fitting" in meaning_lower or "inappropriate" in meaning_lower:
            adj_sentences = [
                f"The modern building looked _____ next to the old church.",
                f"Her _____ comment was out of place.",
                f"The _____ choice was wrong.",
                f"His _____ behaviour was inappropriate.",
                f"The _____ style didn't match.",
                f"Her _____ remark was unsuitable.",
                f"The _____ addition was odd.",
                f"His _____ suggestion was misplaced.",
                f"The _____ element was wrong.",
                f"Her _____ approach was out of place.",
            ]
        elif "not important" in meaning_lower or "trivial" in meaning_lower:
            adj_sentences = [
                f"The mistake was _____ and easily fixed.",
                f"Her _____ comment was ignored.",
                f"The _____ detail was unimportant.",
                f"His _____ remark was minor.",
                f"The _____ error was insignificant.",
                f"Her _____ point was trivial.",
                f"The _____ issue was negligible.",
                f"His _____ concern was minor.",
                f"The _____ matter was unimportant.",
                f"Her _____ observation was irrelevant.",
            ]
        elif "not easily noticed" in meaning_lower or "unnoticeable" in meaning_lower:
            adj_sentences = [
                f"She tried to remain _____ at the back of the room.",
                f"Her _____ presence was unnoticed.",
                f"The _____ change was subtle.",
                f"His _____ behaviour was discreet.",
                f"The _____ difference was minimal.",
                f"Her _____ approach was subtle.",
                f"The _____ modification was slight.",
                f"His _____ manner was unobtrusive.",
                f"The _____ adjustment was minor.",
                f"Her _____ change was imperceptible.",
            ]
        elif "causing difficulty" in meaning_lower or "awkward" in meaning_lower:
            adj_sentences = [
                f"The meeting was scheduled at an _____ time.",
                f"Her _____ request was problematic.",
                f"The _____ timing was bad.",
                f"His _____ demand was difficult.",
                f"The _____ situation was awkward.",
                f"Her _____ timing was unfortunate.",
                f"The _____ request was troublesome.",
                f"His _____ requirement was problematic.",
                f"The _____ circumstance was difficult.",
                f"Her _____ timing was inopportune.",
            ]
        elif "to include as part" in meaning_lower or "include" in meaning_lower:
            adj_sentences = [
                f"The design will _____ several new features.",
                f"Her plan will _____ all suggestions.",
                f"The programme will _____ everyone.",
                f"His proposal will _____ improvements.",
                f"The system will _____ updates.",
                f"Her approach will _____ changes.",
                f"The plan will _____ modifications.",
                f"His design will _____ enhancements.",
                f"The programme will _____ additions.",
                f"Her system will _____ improvements.",
            ]
        elif "impossible to change" in meaning_lower or "hopeless" in meaning_lower:
            adj_sentences = [
                f"The _____ troublemaker was always in detention.",
                f"Her _____ behaviour was persistent.",
                f"The _____ student was difficult.",
                f"His _____ nature was problematic.",
                f"The _____ attitude was unchangeable.",
                f"Her _____ habits were fixed.",
                f"The _____ character was stubborn.",
                f"His _____ ways were set.",
                f"The _____ behaviour was constant.",
                f"Her _____ nature was unalterable.",
            ]
        elif "unable to believe" in meaning_lower or "disbelieving" in meaning_lower:
            adj_sentences = [
                f"She gave him an _____ look when he told the story.",
                f"Her _____ expression showed doubt.",
                f"The _____ response was expected.",
                f"His _____ reaction was natural.",
                f"The _____ stare was questioning.",
                f"Her _____ face showed disbelief.",
                f"The _____ look was sceptical.",
                f"His _____ expression was doubtful.",
                f"The _____ reaction was understandable.",
                f"Her _____ gaze was questioning.",
            ]
        elif "currently holding" in meaning_lower or "necessary" in meaning_lower:
            adj_sentences = [
                f"It is _____ upon all citizens to vote.",
                f"The _____ responsibility was clear.",
                f"Her _____ duty was important.",
                f"The _____ obligation was mandatory.",
                f"His _____ role was essential.",
                f"The _____ requirement was necessary.",
                f"Her _____ task was required.",
                f"The _____ duty was expected.",
                f"His _____ responsibility was clear.",
                f"The _____ obligation was important.",
            ]
        elif "having no interest" in meaning_lower or "uncaring" in meaning_lower:
            adj_sentences = [
                f"He seemed _____ to the outcome of the game.",
                f"Her _____ attitude was noticeable.",
                f"The _____ response was apathetic.",
                f"His _____ manner was cold.",
                f"The _____ attitude was unenthusiastic.",
                f"Her _____ behaviour was disinterested.",
                f"The _____ reaction was neutral.",
                f"His _____ response was uninterested.",
                f"The _____ attitude was unconcerned.",
                f"Her _____ manner was detached.",
            ]
        elif "very poor" in meaning_lower:
            adj_sentences = [
                f"The charity helps _____ families find housing.",
                f"Her _____ circumstances were difficult.",
                f"The _____ situation was dire.",
                f"His _____ state was concerning.",
                f"The _____ conditions were terrible.",
                f"Her _____ background was humble.",
                f"The _____ family needed help.",
                f"His _____ situation was desperate.",
                f"The _____ community required assistance.",
                f"Her _____ means were limited.",
            ]
        elif "angry about unfair" in meaning_lower or "angry" in meaning_lower:
            adj_sentences = [
                f"She was _____ when accused of something she didn't do.",
                f"Her _____ response was justified.",
                f"The _____ reaction was understandable.",
                f"His _____ protest was valid.",
                f"The _____ complaint was reasonable.",
                f"Her _____ objection was warranted.",
                f"The _____ reaction was expected.",
                f"His _____ response was appropriate.",
                f"The _____ protest was justified.",
                f"Her _____ objection was valid.",
            ]
        elif "without careful judgement" in meaning_lower or "random" in meaning_lower:
            adj_sentences = [
                f"The _____ use of chemicals harmed wildlife.",
                f"Her _____ selection was careless.",
                f"The _____ choice was unwise.",
                f"His _____ approach was dangerous.",
                f"The _____ application was harmful.",
                f"Her _____ use was problematic.",
                f"The _____ selection was random.",
                f"His _____ method was careless.",
                f"The _____ application was indiscriminate.",
                f"Her _____ use was unselective.",
            ]
        else:
            # Generic adjective sentences
            adj_sentences = [
                f"Her _____ behaviour was noticeable.",
                f"The _____ situation required attention.",
                f"His _____ attitude was clear.",
                f"The _____ response was expected.",
                f"Her _____ manner was evident.",
                f"The _____ condition was obvious.",
                f"His _____ nature was apparent.",
                f"The _____ state was visible.",
                f"Her _____ character was known.",
                f"The _____ quality was recognised.",
            ]
        
        for sent in adj_sentences:
            if len(sentences) < 10:
                blank_sent = create_blank_sentence(sent, word)
                if blank_sent and blank_sent not in sentences:
                    sentences.append(blank_sent)
    
    else:
        # Noun sentences - customize based on meaning
        if "great wickedness" in meaning_lower or "huge size" in meaning_lower:
            noun_sentences = [
                f"The _____ of the crime shocked the entire community.",
                f"People were stunned by the _____ of the natural disaster.",
                f"The _____ of the problem became clear over time.",
                f"Everyone was aware of the _____ of the challenge ahead.",
                f"The _____ of the mistake was only realised later.",
                f"They were overwhelmed by the _____ of the task.",
                f"The _____ of the situation required immediate action.",
                f"Nobody could ignore the _____ of what had happened.",
                f"The _____ of the decision weighed heavily on her mind.",
                f"They were shocked by the _____ of the damage.",
            ]
        elif "extremely large size" in meaning_lower or "hugeness" in meaning_lower:
            noun_sentences = [
                f"The _____ of the whale amazed all the watchers.",
                f"Everyone was impressed by the _____ of the ancient tree.",
                f"The _____ of the mountain range stretched for miles.",
                f"They marvelled at the _____ of the cathedral.",
                f"The _____ of the ocean made them feel very small.",
                f"Visitors were stunned by the _____ of the castle.",
                f"The _____ of the dinosaur skeleton filled the museum hall.",
                f"They couldn't believe the _____ of the ancient monument.",
                f"The _____ of the waterfall was breathtaking.",
                f"Everyone was amazed by the _____ of the ancient ruins.",
            ]
        elif "mental calmness" in meaning_lower or "composure" in meaning_lower:
            noun_sentences = [
                f"She faced the difficult situation with remarkable _____.",
                f"His _____ during the crisis impressed everyone.",
                f"The teacher maintained her _____ despite the chaos.",
                f"She showed great _____ when receiving the bad news.",
                f"His _____ helped calm the worried students.",
                f"She handled the emergency with perfect _____.",
                f"His _____ in stressful situations was admirable.",
                f"She demonstrated _____ when others were panicking.",
                f"His _____ made him an excellent leader.",
                f"She showed _____ even when things went wrong.",
            ]
        elif "careful assessment" in meaning_lower or "assessment" in meaning_lower:
            noun_sentences = [
                f"The teacher's _____ of her work was very positive.",
                f"After careful _____, they decided to proceed.",
                f"The _____ showed that improvements were needed.",
                f"Her _____ of the situation was thorough and fair.",
                f"The _____ revealed several important points.",
                f"After the _____, they made their final decision.",
                f"The _____ helped identify areas for improvement.",
                f"His _____ of the project was detailed and helpful.",
                f"The _____ process took several days to complete.",
                f"Her _____ was based on careful observation.",
            ]
        elif "dying out" in meaning_lower or "disappearance" in meaning_lower:
            noun_sentences = [
                f"The _____ of dinosaurs happened millions of years ago.",
                f"Scientists are working to prevent the _____ of rare species.",
                f"The _____ of the ancient language was a great loss.",
                f"Conservation efforts aim to stop the _____ of endangered animals.",
                f"The _____ of traditional crafts worries many people.",
                f"They studied the causes of the _____ of the ancient civilisation.",
                f"The _____ of the old customs saddened the elders.",
                f"Efforts to prevent the _____ of the species are ongoing.",
                f"The _____ of the rare plant concerned botanists.",
                f"They documented the _____ of many historical traditions.",
            ]
        elif "lively energy" in meaning_lower or "enthusiasm" in meaning_lower:
            noun_sentences = [
                f"The children's _____ filled the playground with joy.",
                f"Her _____ for learning was infectious.",
                f"The _____ of the crowd was overwhelming.",
                f"His _____ made everyone feel more energetic.",
                f"The _____ of the celebration was wonderful to see.",
                f"Her _____ brightened everyone's day.",
                f"The _____ of the team was evident in their performance.",
                f"His _____ for the project inspired others.",
                f"The _____ of the festival was incredible.",
                f"Her _____ was matched only by her talent.",
            ]
        elif "excessive enthusiasm" in meaning_lower or "extremism" in meaning_lower:
            noun_sentences = [
                f"His _____ for the team was sometimes worrying.",
                f"The _____ of the supporters went too far.",
                f"Her _____ about the subject made others uncomfortable.",
                f"The _____ of the group was concerning.",
                f"His _____ prevented him from seeing other viewpoints.",
                f"The _____ of their beliefs was extreme.",
                f"Her _____ made it difficult to have a balanced discussion.",
                f"The _____ of the movement was well-known.",
                f"His _____ blinded him to reason.",
                f"The _____ of their approach was problematic.",
            ]
        elif "qualities associated with women" in meaning_lower or "womanhood" in meaning_lower:
            noun_sentences = [
                f"The ballet celebrated grace and _____.",
                f"Her _____ was evident in her gentle manner.",
                f"The _____ of her character was admired by many.",
                f"Her _____ shone through in everything she did.",
                f"The _____ of the performance was beautiful.",
                f"Her _____ was matched by her strength.",
                f"The _____ of her approach was appreciated.",
                f"Her _____ made her a role model for others.",
                f"The _____ of her nature was evident.",
                f"Her _____ was one of her greatest qualities.",
            ]
        elif "fierce and violent" in meaning_lower or "fierceness" in meaning_lower:
            noun_sentences = [
                f"The _____ of the storm surprised weather forecasters.",
                f"The _____ of the lion's roar was terrifying.",
                f"Her _____ in defending her friends was admirable.",
                f"The _____ of the attack shocked everyone.",
                f"His _____ on the football pitch was legendary.",
                f"The _____ of the debate was intense.",
                f"Her _____ determination helped her succeed.",
                f"The _____ of the competition was unexpected.",
                f"His _____ passion for justice was clear.",
                f"The _____ of her response surprised them all.",
            ]
        elif "gas in digestive system" in meaning_lower:
            noun_sentences = [
                f"The doctor asked about symptoms including _____.",
                f"Certain foods can cause uncomfortable _____.",
                f"The medication helped reduce the _____ problem.",
                f"Her diet changes improved the _____ issue.",
                f"The _____ was a side effect of the treatment.",
                f"Proper eating habits can prevent excessive _____.",
                f"The _____ discomfort was temporary.",
                f"Her _____ problem improved with dietary changes.",
                f"The _____ was caused by eating too quickly.",
                f"Reducing certain foods helped with the _____.",
            ]
        elif "careful use of money" in meaning_lower or "thriftiness" in meaning_lower:
            noun_sentences = [
                f"Their _____ during hard times helped them survive.",
                f"Her _____ allowed her to save money.",
                f"The _____ approach prevented waste.",
                f"His _____ habits were admirable.",
                f"The _____ lifestyle suited them well.",
                f"Her _____ management of resources was wise.",
                f"The _____ spending kept them out of debt.",
                f"His _____ nature helped the family.",
                f"The _____ use of materials was efficient.",
                f"Her _____ planning ensured success.",
            ]
        elif "study of family history" in meaning_lower or "ancestry" in meaning_lower:
            noun_sentences = [
                f"She spent years researching her family's _____.",
                f"The _____ revealed interesting connections.",
                f"His _____ research traced back centuries.",
                f"The _____ showed their royal heritage.",
                f"Her _____ project was fascinating.",
                f"The _____ records were carefully preserved.",
                f"His _____ investigation uncovered secrets.",
                f"The _____ tree was extensive.",
                f"Her _____ work was published.",
                f"The _____ documents were valuable.",
            ]
        elif "politeness and good manners" in meaning_lower or "refinement" in meaning_lower:
            noun_sentences = [
                f"Her _____ and grace impressed everyone at dinner.",
                f"The _____ of her behaviour was evident.",
                f"His _____ made him popular.",
                f"The _____ of the occasion was clear.",
                f"Her _____ was natural and genuine.",
                f"The _____ of her speech was admirable.",
                f"His _____ manners were well-known.",
                f"The _____ of her approach was appreciated.",
                f"Her _____ character shone through.",
                f"The _____ of the gathering was notable.",
            ]
        elif "proud and arrogant" in meaning_lower or "arrogance" in meaning_lower:
            noun_sentences = [
                f"Her _____ made it difficult to make friends.",
                f"The _____ of his behaviour was off-putting.",
                f"His _____ attitude alienated others.",
                f"The _____ in her voice was clear.",
                f"Her _____ prevented her from learning.",
                f"The _____ of his manner was obvious.",
                f"His _____ comments offended people.",
                f"The _____ in her expression was evident.",
                f"Her _____ made her unpopular.",
                f"The _____ of his behaviour was unacceptable.",
            ]
        elif "unfriendly and aggressive" in meaning_lower or "aggression" in meaning_lower:
            noun_sentences = [
                f"There was open _____ between the rival groups.",
                f"The _____ of his response was unexpected.",
                f"Her _____ made others uncomfortable.",
                f"The _____ in the room was palpable.",
                f"His _____ behaviour was concerning.",
                f"The _____ between them was clear.",
                f"Her _____ attitude created problems.",
                f"The _____ of the situation was tense.",
                f"His _____ response escalated the conflict.",
                f"The _____ made cooperation impossible.",
            ]
        elif "peculiar personal habit" in meaning_lower or "quirk" in meaning_lower:
            noun_sentences = [
                f"Her _____ of humming while working amused colleagues.",
                f"The _____ was endearing.",
                f"His _____ made him unique.",
                f"The _____ was harmless but noticeable.",
                f"Her _____ became well-known.",
                f"The _____ was part of his character.",
                f"His _____ amused everyone.",
                f"The _____ was charming.",
                f"Her _____ was distinctive.",
                f"The _____ made him memorable.",
            ]
        elif "lack of balance" in meaning_lower or "inequality" in meaning_lower:
            noun_sentences = [
                f"There was an _____ in the distribution of resources.",
                f"The _____ was noticeable.",
                f"Her _____ approach caused problems.",
                f"The _____ in power was clear.",
                f"His _____ lifestyle affected his health.",
                f"The _____ made things difficult.",
                f"Her _____ diet was unhealthy.",
                f"The _____ was corrected.",
                f"His _____ work schedule was problematic.",
                f"The _____ needed to be addressed.",
            ]
        elif "something that motivates" in meaning_lower or "motivation" in meaning_lower:
            noun_sentences = [
                f"The bonus was a good _____ to work harder.",
                f"Her _____ was strong.",
                f"The _____ reward encouraged effort.",
                f"His _____ was clear.",
                f"The _____ prize motivated everyone.",
                f"Her _____ was effective.",
                f"The _____ benefit was attractive.",
                f"His _____ was powerful.",
                f"The _____ opportunity was appealing.",
                f"Her _____ was compelling.",
            ]
        elif "surgical cut" in meaning_lower:
            noun_sentences = [
                f"The surgeon made a small _____ to begin the operation.",
                f"Her _____ healed quickly.",
                f"The _____ was precise.",
                f"His _____ was necessary.",
                f"The _____ was clean.",
                f"Her _____ was small.",
                f"The _____ was made carefully.",
                f"His _____ was successful.",
                f"The _____ was neat.",
                f"Her _____ was expertly done.",
            ]
        elif "rude behaviour" in meaning_lower or "rudeness" in meaning_lower:
            noun_sentences = [
                f"His _____ in answering back shocked the teacher.",
                f"The _____ of his response was unacceptable.",
                f"Her _____ was inappropriate.",
                f"The _____ in his tone was clear.",
                f"His _____ behaviour was punished.",
                f"The _____ of her comment was shocking.",
                f"His _____ made him unpopular.",
                f"The _____ was not tolerated.",
                f"Her _____ resulted in detention.",
                f"The _____ was disrespectful.",
            ]
        else:
            # Generic noun sentences
            noun_sentences = [
                f"The _____ was important to everyone.",
                f"Her _____ was evident.",
                f"The _____ of the situation was clear.",
                f"His _____ was noticeable.",
                f"The _____ made a difference.",
                f"Her _____ was appreciated.",
                f"The _____ was significant.",
                f"His _____ was recognised.",
                f"The _____ was valuable.",
                f"Her _____ was important.",
            ]
        
        for sent in noun_sentences:
            if len(sentences) < 10:
                blank_sent = create_blank_sentence(sent, word)
                if blank_sent and blank_sent not in sentences:
                    sentences.append(blank_sent)
    
    # Ensure we have exactly 10 sentences
    while len(sentences) < 10:
        # Add generic fallback sentences if needed
        if is_verb:
            fallback = f"They decided to _____ after careful thought."
        elif is_adjective:
            fallback = f"Her _____ behaviour was noticeable."
        else:
            fallback = f"The _____ was important."
        
        blank_fallback = create_blank_sentence(fallback, word)
        if blank_fallback and blank_fallback not in sentences:
            sentences.append(blank_fallback)
        else:
            break
    
    return sentences[:10]


def main():
    """Generate quiz sentences for Level 4 Batch 2."""
    input_file = Path(__file__).parent.parent / "data" / "level4_batch2.txt"
    output_file = Path(__file__).parent.parent / "data" / "level4_batch2.csv"
    
    sentences_generated = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        with open(output_file, 'w', encoding='utf-8', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(['level', 'word', 'sentence'])
            
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                # Parse the line: word|meaning|example|synonym|antonym
                parts = line.split('|')
                if len(parts) < 3:
                    print(f"Warning: Line {line_num} has insufficient parts: {line}")
                    continue
                
                word = parts[0].strip()
                meaning = parts[1].strip() if len(parts) > 1 else ""
                example = parts[2].strip() if len(parts) > 2 else ""
                synonym = parts[3].strip() if len(parts) > 3 else ""
                antonym = parts[4].strip() if len(parts) > 4 else ""
                
                # Generate sentences
                quiz_sentences = generate_quiz_sentences(word, meaning, example, synonym, antonym)
                
                # Write each sentence to CSV
                for sentence in quiz_sentences:
                    writer.writerow(['4', word, sentence])
                    sentences_generated += 1
    
    print(f"Level 4 Batch 2 complete: {sentences_generated} sentences")


if __name__ == "__main__":
    main()
