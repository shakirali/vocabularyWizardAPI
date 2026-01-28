#!/usr/bin/env python3
"""
Generate quiz sentences for Level 4 Batch 4 vocabulary words.
Generates 10 contextually rich sentences per word.
"""

import csv
import re
from pathlib import Path
from typing import List, Tuple


def create_blank_sentence(sentence: str, word: str) -> str:
    """Replace the word in a sentence with _____."""
    # Case-insensitive replacement
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    return pattern.sub("_____", sentence)


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
    seen: set = set()
    
    # Determine word type
    is_verb = meaning_lower.startswith("to ")
    is_adjective = (
        any(marker in meaning_lower for marker in [
            "having", "showing", "full of", "characterised by", "characterized by",
            "very", "extremely", "quite", "rather", "causing", "deserving",
            "relating to", "willing", "unwilling", "avoiding", "expressing",
            "treating", "done", "on the edge", "harmful", "completely",
            "remarkable", "a person who", "visually", "giving", "the state of",
            "the quality of", "an earlier", "dangerously", "advanced", "someone who",
            "a difficult", "a preference", "mainly", "an attempt", "trying",
            "widespread", "causing", "a tendency", "wastefully", "remarkably",
            "recklessly", "an abundance", "rapid", "producing", "the state of",
            "accurately", "the leading", "nearness", "eager", "a state of",
            "isolation", "representing", "a complex", "aggressively", "opposing",
            "a refutation", "stubbornly", "a container", "to recover", "the action of",
            "no longer", "relating to", "to give", "in relation", "to give up",
            "tending to", "unintended", "deserving", "extremely", "the capacity",
            "deep, clear", "attractive", "the state of"
        ]) or
        word_lower.endswith(('ous', 'ful', 'less', 'able', 'ible', 'ant', 'ent', 'ing', 'ed', 'ive', 'ic', 'al'))
    )
    is_noun = not is_verb and not is_adjective
    
    # 1. Use example sentence if available (best quality)
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example and blank_example not in seen:
            sentences.append(blank_example)
            seen.add(blank_example)
    
    # Generate word-specific sentences based on meaning
    word_specific_sentences = []
    
    if word_lower == "obsequious":
        word_specific_sentences = [
            "The _____ assistant agreed with everything his boss said, never questioning any decision.",
            "She found his _____ behaviour towards the headteacher quite uncomfortable to watch.",
            "The _____ waiter kept bowing and complimenting the customers excessively.",
            "His _____ manner made it clear he was trying too hard to please.",
            "The _____ employee would always agree, even when he knew the boss was wrong.",
            "She was annoyed by his _____ attitude, which seemed insincere.",
            "The _____ student praised the teacher's every word, hoping for better grades.",
            "His _____ response to every request showed he lacked confidence.",
            "The _____ servant was overly eager to help, which became irritating.",
            "She couldn't stand his _____ way of always saying yes to everything.",
        ]
    elif word_lower == "obstreperous":
        word_specific_sentences = [
            "The _____ children disrupted the entire class with their shouting.",
            "His _____ behaviour at the restaurant embarrassed his parents.",
            "The _____ dog barked loudly and refused to obey commands.",
            "She found the _____ toddler difficult to control in the shop.",
            "The _____ student constantly interrupted the lesson with loud comments.",
            "His _____ attitude made group work impossible.",
            "The _____ crowd made so much noise that the speaker couldn't be heard.",
            "She struggled to manage the _____ class during the school trip.",
            "The _____ child's tantrum disturbed everyone in the library.",
            "His _____ nature meant he was always causing trouble.",
        ]
    elif word_lower == "onomatopoeia":
        word_specific_sentences = [
            "Words like 'buzz' and 'hiss' are examples of _____.",
            "The teacher explained that 'bang' and 'pop' demonstrate _____.",
            "She loved using _____ in her creative writing to make it more vivid.",
            "The poet used _____ to help readers hear the sounds described.",
            "Words such as 'crash' and 'whisper' show _____ in action.",
            "The author's clever use of _____ made the story come alive.",
            "He learned about _____ when studying sound words in English class.",
            "The _____ in the poem helped create a sense of atmosphere.",
            "She identified several examples of _____ in the text.",
            "The writer's _____ made the description of the storm very effective.",
        ]
    elif word_lower == "opportunist":
        word_specific_sentences = [
            "The _____ quickly took advantage of the situation when others hesitated.",
            "She realised he was an _____ when he jumped at every chance to benefit.",
            "The _____ saw the opening and immediately seized the opportunity.",
            "His _____ nature meant he was always looking for ways to get ahead.",
            "The _____ businessman bought the company when it was struggling.",
            "She didn't trust him because he was such an obvious _____.",
            "The _____ politician changed his views to match popular opinion.",
            "His _____ approach helped him succeed, but made him unpopular.",
            "The _____ was always ready to exploit any situation for personal gain.",
            "She recognised the _____ in him when he took credit for her idea.",
        ]
    elif word_lower == "orthodontist":
        word_specific_sentences = [
            "The _____ fitted braces to straighten her crooked teeth.",
            "She visited the _____ every month to have her braces adjusted.",
            "The _____ explained that the treatment would take two years.",
            "His job as an _____ involved helping children with misaligned teeth.",
            "The _____ showed her X-rays of her teeth before starting treatment.",
            "She was nervous about seeing the _____ for the first time.",
            "The _____ recommended braces to fix her overbite.",
            "His _____ suggested wearing a retainer after the braces came off.",
            "The _____ specialised in correcting dental alignment problems.",
            "She thanked the _____ for giving her a beautiful, straight smile.",
        ]
    elif word_lower == "ostentatious":
        word_specific_sentences = [
            "His _____ display of wealth was vulgar and unnecessary.",
            "The _____ mansion had gold decorations everywhere.",
            "She found his _____ jewellery too flashy and attention-seeking.",
            "The _____ party was designed to show off his success.",
            "His _____ car with its bright colours drew unwanted attention.",
            "The _____ wedding had expensive decorations that seemed excessive.",
            "She thought his _____ behaviour was just showing off.",
            "The _____ display of expensive gifts made others uncomfortable.",
            "His _____ way of dressing was designed to impress others.",
            "The _____ celebration was more about showing off than celebrating.",
        ]
    elif word_lower == "outrageous":
        word_specific_sentences = [
            "The _____ prices made shopping impossible for most families.",
            "His _____ behaviour at the party shocked everyone.",
            "The _____ claim that he could fly was clearly untrue.",
            "She found the _____ demands completely unreasonable.",
            "The _____ amount of homework upset all the students.",
            "His _____ comments offended many people in the audience.",
            "The _____ decision seemed unfair to everyone involved.",
            "She was appalled by the _____ treatment of the animals.",
            "The _____ proposal was immediately rejected by the committee.",
            "His _____ excuse for being late was completely unbelievable.",
        ]
    elif word_lower == "overbearing":
        word_specific_sentences = [
            "His _____ attitude made it difficult to work with him.",
            "The _____ manager never listened to anyone else's ideas.",
            "She found her _____ older brother impossible to live with.",
            "The _____ teacher dominated every conversation in the staff room.",
            "His _____ personality meant he always had to be in charge.",
            "The _____ coach shouted instructions constantly during training.",
            "She avoided the _____ neighbour who always told her what to do.",
            "The _____ boss made all decisions without consulting the team.",
            "His _____ manner made others feel small and unimportant.",
            "The _____ parent controlled every aspect of her child's life.",
        ]
    elif word_lower == "painstaking":
        word_specific_sentences = [
            "The restoration required _____ attention to detail.",
            "She took a _____ approach to her revision, checking every fact.",
            "The _____ research took months but produced excellent results.",
            "His _____ work on the model ship showed incredible patience.",
            "The _____ investigation uncovered important evidence.",
            "She admired his _____ efforts to get everything perfect.",
            "The _____ preparation ensured the event ran smoothly.",
            "His _____ method meant the project took longer but was better.",
            "The _____ care he took with the painting was impressive.",
            "She showed _____ dedication to learning the piano piece perfectly.",
        ]
    elif word_lower == "palaeontologist":
        word_specific_sentences = [
            "The _____ discovered a new species of dinosaur in the desert.",
            "She dreamed of becoming a _____ and studying ancient fossils.",
            "The _____ carefully brushed away the dirt to reveal the bone.",
            "His job as a _____ involved digging for fossils in remote locations.",
            "The _____ explained how the dinosaur bones had been preserved.",
            "She visited the museum to see the _____'s latest discoveries.",
            "The _____ spent years studying the fossilised remains.",
            "His work as a _____ helped scientists understand prehistoric life.",
            "The _____ used special tools to carefully extract the fossil.",
            "She was fascinated by the _____'s stories about ancient creatures.",
        ]
    elif word_lower == "palindrome":
        word_specific_sentences = [
            "'Madam' is a _____ because it reads the same both ways.",
            "The teacher challenged the class to find examples of a _____.",
            "She discovered that 'racecar' is a _____ when written backwards.",
            "The _____ 'level' spelled backwards is still 'level'.",
            "He enjoyed finding _____ words like 'radar' and 'civic'.",
            "The author used a _____ as the title of her book.",
            "She explained that 'noon' is a simple example of a _____.",
            "The _____ puzzle required finding words that read the same forwards and backwards.",
            "He was proud when he created his own _____ word.",
            "The _____ fascinated her because of its symmetry.",
        ]
    elif word_lower == "parliament":
        word_specific_sentences = [
            "The new law was debated in _____ before being passed.",
            "She watched the _____ session on television to learn about politics.",
            "The members of _____ discussed the important issues facing the country.",
            "His dream was to be elected to _____ and represent his community.",
            "The _____ building in London is famous for its clock tower.",
            "She learned about how _____ makes laws in her citizenship class.",
            "The Prime Minister addressed _____ about the new policy.",
            "His visit to _____ gave him insight into how government works.",
            "The _____ session lasted for hours as they debated the bill.",
            "She was excited to see _____ in action during the school trip.",
        ]
    elif word_lower == "patronising" or word_lower == "patronizing":
        word_specific_sentences = [
            "His _____ tone made her feel belittled and frustrated.",
            "The _____ comment suggested she wasn't capable of understanding.",
            "She found his _____ attitude towards younger students annoying.",
            "The _____ way he explained things implied she was stupid.",
            "His _____ smile made it clear he thought he was superior.",
            "The _____ teacher spoke to the class as if they were babies.",
            "She was offended by his _____ assumption that she needed help.",
            "The _____ manner in which he corrected her was humiliating.",
            "His _____ behaviour showed he didn't respect her intelligence.",
            "The _____ tone of his voice made everyone uncomfortable.",
        ]
    elif word_lower == "pejorative":
        word_specific_sentences = [
            "Using _____ terms to describe someone is unkind and hurtful.",
            "The _____ word he used was inappropriate and offensive.",
            "She avoided _____ language when discussing different groups.",
            "The teacher explained that _____ words can be harmful.",
            "His _____ comment about her appearance was completely unacceptable.",
            "The _____ term was meant to insult rather than describe.",
            "She was shocked by the _____ language used in the argument.",
            "The _____ expression showed his prejudice and lack of respect.",
            "His _____ remark revealed his negative attitude.",
            "The _____ word was clearly intended to cause offence.",
        ]
    elif word_lower == "perceptive":
        word_specific_sentences = [
            "The _____ teacher noticed the student's distress immediately.",
            "Her _____ observation helped solve the mystery quickly.",
            "The _____ child understood the situation better than the adults.",
            "His _____ comments showed he was paying close attention.",
            "The _____ detective noticed clues that others had missed.",
            "She was known for being _____ and understanding others' feelings.",
            "The _____ student asked insightful questions during the lesson.",
            "His _____ analysis of the problem impressed everyone.",
            "The _____ friend realised something was wrong before she said anything.",
            "She showed a _____ understanding of the complex issue.",
        ]
    elif word_lower == "perfunctory":
        word_specific_sentences = [
            "He gave only a _____ glance at the report before signing it.",
            "The _____ apology didn't seem sincere or heartfelt.",
            "She did a _____ job of cleaning, missing many spots.",
            "The _____ handshake showed he wasn't really interested.",
            "His _____ attempt at homework was rushed and careless.",
            "The _____ inspection missed several important problems.",
            "She gave a _____ response without really thinking about it.",
            "The _____ way he listened showed he wasn't paying attention.",
            "His _____ effort was clearly just to get it done quickly.",
            "The _____ review didn't catch any of the errors.",
        ]
    elif word_lower == "peripheral":
        word_specific_sentences = [
            "The _____ issues were discussed later, after the main topics.",
            "She noticed something in her _____ vision but couldn't see it clearly.",
            "The _____ details weren't as important as the main point.",
            "His role was _____ to the main project, but still useful.",
            "The _____ characters in the story didn't affect the plot much.",
            "She focused on the central problem, ignoring the _____ concerns.",
            "The _____ information was interesting but not essential.",
            "His contribution was _____ to the team's success.",
            "The _____ areas of the town were less developed.",
            "She dealt with the main issue first, then the _____ matters.",
        ]
    elif word_lower == "pernicious":
        word_specific_sentences = [
            "The _____ rumours damaged her reputation slowly over time.",
            "His _____ influence on the younger students was worrying.",
            "The _____ effects of the pollution weren't immediately obvious.",
            "She warned about the _____ nature of the online content.",
            "The _____ habit seemed harmless at first but became serious.",
            "His _____ comments undermined her confidence gradually.",
            "The _____ disease spread quietly through the population.",
            "She recognised the _____ impact of the negative attitudes.",
            "The _____ problem grew worse without anyone noticing.",
            "His _____ behaviour had a subtle but harmful effect.",
        ]
    elif word_lower == "perpetuate":
        word_specific_sentences = [
            "We must not _____ harmful stereotypes about different groups.",
            "The school tried to _____ good values through its teaching.",
            "She didn't want to _____ the cycle of bullying.",
            "The tradition helped _____ the customs of their ancestors.",
            "His actions would _____ the problem rather than solve it.",
            "The story helped _____ the legend for future generations.",
            "She worked to _____ positive attitudes towards learning.",
            "The system seemed designed to _____ inequality.",
            "His behaviour would only _____ the conflict between them.",
            "The ceremony helped _____ the memory of those who had served.",
        ]
    elif word_lower == "perplexing":
        word_specific_sentences = [
            "The _____ riddle took hours to solve.",
            "She found the _____ puzzle completely baffling.",
            "The _____ situation confused everyone involved.",
            "His _____ behaviour made no sense to his friends.",
            "The _____ mystery kept the detectives guessing.",
            "She was faced with a _____ problem that seemed impossible.",
            "The _____ question had no obvious answer.",
            "His _____ explanation only made things more confusing.",
            "The _____ nature of the problem required careful thought.",
            "She found the _____ instructions difficult to follow.",
        ]
    elif word_lower == "phenomenon":
        word_specific_sentences = [
            "The northern lights are a spectacular natural _____.",
            "She observed the interesting _____ of birds migrating south.",
            "The _____ of the rainbow appeared after the storm.",
            "His success was a rare _____ in the world of sport.",
            "The _____ of the eclipse fascinated everyone who watched.",
            "She studied the _____ of how plants grow towards light.",
            "The _____ of the shooting stars was beautiful to see.",
            "His recovery was a medical _____ that surprised doctors.",
            "The _____ of the double rainbow was captured in photos.",
            "She was amazed by the _____ of the bioluminescent waves.",
        ]
    elif word_lower == "philanthropist":
        word_specific_sentences = [
            "The _____ donated millions to help the poor and needy.",
            "She aspired to become a _____ and help others.",
            "The _____'s generosity changed many people's lives.",
            "His work as a _____ focused on education for children.",
            "The _____ established a foundation to support charities.",
            "She admired the _____ for giving away most of his wealth.",
            "The _____'s contributions helped build the new hospital.",
            "His reputation as a _____ was well-known throughout the country.",
            "The _____ dedicated her life to helping those less fortunate.",
            "She learned about the famous _____ in her history lesson.",
        ]
    elif word_lower == "philosophical":
        word_specific_sentences = [
            "He took a _____ approach to life's challenges.",
            "The _____ discussion about the meaning of life was interesting.",
            "She enjoyed reading _____ books that made her think deeply.",
            "The _____ question had no simple answer.",
            "His _____ attitude helped him accept the difficult situation.",
            "The _____ debate explored important questions about existence.",
            "She found the _____ text challenging but rewarding.",
            "The _____ way he viewed problems was quite mature.",
            "His _____ nature meant he often questioned everything.",
            "The _____ approach to the problem considered deeper meanings.",
        ]
    elif word_lower == "physiotherapy":
        word_specific_sentences = [
            "After the accident, she needed _____ to regain movement.",
            "The _____ sessions helped strengthen his injured leg.",
            "She attended _____ twice a week to recover from her surgery.",
            "The _____ exercises were designed to improve flexibility.",
            "His _____ treatment lasted for six months.",
            "She was grateful for the _____ that helped her walk again.",
            "The _____ programme was tailored to her specific needs.",
            "His progress in _____ was slow but steady.",
            "The _____ techniques helped reduce her pain significantly.",
            "She completed her _____ and was able to return to sport.",
        ]
    elif word_lower == "picturesque":
        word_specific_sentences = [
            "The _____ village attracted many tourists with its charm.",
            "She painted the _____ landscape during her holiday.",
            "The _____ countryside was perfect for photography.",
            "His cottage was in a _____ location by the river.",
            "The _____ scene looked like something from a postcard.",
            "She loved the _____ beauty of the old stone bridge.",
            "The _____ town had cobbled streets and colourful houses.",
            "His photo captured the _____ sunset over the mountains.",
            "The _____ garden was full of flowers and butterflies.",
            "She described the _____ view from the hilltop.",
        ]
    elif word_lower == "plagiarise" or word_lower == "plagiarize":
        word_specific_sentences = [
            "It is wrong to _____ other people's writing without credit.",
            "The student was caught trying to _____ an essay from the internet.",
            "She learned that to _____ someone's work is dishonest.",
            "The teacher explained that to _____ is a form of cheating.",
            "His attempt to _____ the story was discovered immediately.",
            "The school had strict rules against students who _____.",
            "She was warned not to _____ any content in her research project.",
            "The consequences of trying to _____ were severe.",
            "His decision to _____ showed a lack of integrity.",
            "The teacher could tell he had tried to _____ because the writing style changed.",
        ]
    elif word_lower == "pleasurable":
        word_specific_sentences = [
            "Reading was a _____ way to spend the afternoon.",
            "She found the _____ experience of swimming very relaxing.",
            "The _____ walk through the park lifted her spirits.",
            "His _____ hobby of painting brought him great joy.",
            "The _____ meal was enjoyed by everyone at the table.",
            "She described the _____ feeling of finishing her exams.",
            "The _____ music made the journey more enjoyable.",
            "His _____ conversation with friends made the time pass quickly.",
            "The _____ activity was something she looked forward to each week.",
            "She found the _____ task of gardening very satisfying.",
        ]
    elif word_lower == "polarity":
        word_specific_sentences = [
            "There was a clear _____ between the two political parties.",
            "The _____ of opinions created tension in the discussion.",
            "She noticed the _____ between her parents' views on the topic.",
            "The _____ in the classroom showed divided opinions.",
            "His views created a _____ with those of his classmates.",
            "The _____ between the two groups was obvious.",
            "She studied the _____ of magnetic fields in science class.",
            "The _____ of the debate made compromise difficult.",
            "His position created a clear _____ with the opposing side.",
            "The _____ between their beliefs was too great to bridge.",
        ]
    elif word_lower == "pomposity":
        word_specific_sentences = [
            "His _____ made him unpopular with his colleagues.",
            "The _____ of his speech was off-putting to the audience.",
            "She found his _____ irritating and unnecessary.",
            "The _____ with which he spoke suggested he thought himself superior.",
            "His _____ was evident in every word he said.",
            "The _____ of his manner made others avoid him.",
            "She couldn't stand the _____ of his self-important attitude.",
            "The _____ in his voice was clear to everyone listening.",
            "His _____ prevented him from making real friends.",
            "The _____ of his behaviour was matched only by his arrogance.",
        ]
    elif word_lower == "precedent":
        word_specific_sentences = [
            "The court decision set an important _____ for future cases.",
            "She researched the _____ before making her argument.",
            "The _____ established a new way of handling such situations.",
            "His actions created a _____ that others would follow.",
            "The _____ from the previous year guided their decision.",
            "She cited the _____ to support her point of view.",
            "The _____ showed how similar cases had been handled.",
            "His success set a _____ for other students to aim for.",
            "The _____ was important in determining the outcome.",
            "She followed the _____ set by her predecessor.",
        ]
    elif word_lower == "precipitate":
        word_specific_sentences = [
            "The argument seemed to _____ the end of their friendship.",
            "His careless words would _____ a crisis.",
            "The decision might _____ unexpected consequences.",
            "She didn't want to _____ a conflict with her comment.",
            "The news would _____ a series of events.",
            "His actions could _____ a major problem.",
            "The change would _____ a complete transformation.",
            "She feared her question might _____ an argument.",
            "The announcement would _____ widespread discussion.",
            "His mistake could _____ serious trouble.",
        ]
    elif word_lower == "precipitous":
        word_specific_sentences = [
            "The _____ cliff made climbing dangerous.",
            "She was careful near the _____ drop at the edge.",
            "The _____ slope was difficult to descend safely.",
            "His _____ fall from grace surprised everyone.",
            "The _____ path required careful navigation.",
            "She avoided the _____ edge of the mountain.",
            "The _____ decline in sales worried the company.",
            "His _____ decision was made too quickly.",
            "The _____ terrain made the hike challenging.",
            "She was warned about the _____ nature of the path.",
        ]
    elif word_lower == "precocious":
        word_specific_sentences = [
            "The _____ child could read at age three.",
            "Her _____ talent for music was evident from an early age.",
            "The _____ student was already studying advanced topics.",
            "His _____ understanding of mathematics impressed his teachers.",
            "The _____ young artist's work was displayed in a gallery.",
            "She showed _____ ability in languages, speaking three by age ten.",
            "The _____ child's questions were surprisingly sophisticated.",
            "His _____ development meant he skipped a year at school.",
            "The _____ student's essay was written at university level.",
            "She was known for being _____ in her academic achievements.",
        ]
    elif word_lower == "predecessor":
        word_specific_sentences = [
            "The new manager improved on her _____'s work.",
            "She studied the methods used by her _____.",
            "The _____ had left detailed notes for the next person.",
            "His _____ had established the system he now used.",
            "The _____'s achievements were hard to match.",
            "She compared her results with those of her _____.",
            "The _____ had set high standards for the role.",
            "His _____'s legacy was still visible in the organisation.",
            "The _____ had worked there for twenty years.",
            "She learned from the mistakes of her _____.",
        ]
    elif word_lower == "predicament":
        word_specific_sentences = [
            "The hikers found themselves in a dangerous _____.",
            "She was in a difficult _____ with no easy solution.",
            "The _____ required careful thought to resolve.",
            "His _____ became worse when he lost his map.",
            "The _____ seemed impossible to escape from.",
            "She found herself in an awkward _____ at the party.",
            "The _____ of being lost in the forest was frightening.",
            "His _____ meant he had to choose between two bad options.",
            "The _____ required help from others to solve.",
            "She was stuck in a _____ that needed immediate attention.",
        ]
    elif word_lower == "predilection":
        word_specific_sentences = [
            "She had a _____ for classical music.",
            "His _____ for adventure stories was well-known.",
            "The child showed a clear _____ for drawing.",
            "Her _____ for sweet foods was obvious from her choices.",
            "The student's _____ for science subjects was evident.",
            "She developed a _____ for reading mystery novels.",
            "His _____ for outdoor activities kept him busy.",
            "The teacher noticed her _____ for helping others.",
            "She had a natural _____ for languages.",
            "His _____ for collecting stamps began in childhood.",
        ]
    elif word_lower == "predominantly":
        word_specific_sentences = [
            "The class was _____ made up of girls.",
            "The area was _____ residential, with few shops.",
            "She found the book _____ interesting, with some boring parts.",
            "The weather was _____ sunny during their holiday.",
            "His diet was _____ vegetarian, with occasional fish.",
            "The population was _____ young families.",
            "She spent her time _____ studying, with breaks for exercise.",
            "The forest was _____ oak trees, with some birch mixed in.",
            "His collection was _____ stamps, though he had some coins too.",
            "The discussion was _____ about the main topic, with brief tangents.",
        ]
    elif word_lower == "prejudiced":
        word_specific_sentences = [
            "His _____ views prevented him from seeing the truth.",
            "The _____ comment showed his unfair bias.",
            "She was shocked by the _____ attitude displayed.",
            "The _____ opinion was based on stereotypes, not facts.",
            "His _____ behaviour towards others was unacceptable.",
            "The _____ way he judged people was wrong.",
            "She worked to overcome her own _____ thoughts.",
            "The _____ remark revealed his narrow-mindedness.",
            "His _____ perspective limited his understanding.",
            "The _____ treatment of certain groups was unfair.",
        ]
    elif word_lower == "preposterous":
        word_specific_sentences = [
            "The _____ idea made everyone laugh.",
            "She found the _____ claim completely unbelievable.",
            "The _____ suggestion was immediately rejected.",
            "His _____ excuse for being late was ridiculous.",
            "The _____ story couldn't possibly be true.",
            "She thought the _____ proposal was absurd.",
            "The _____ plan would never work in reality.",
            "His _____ behaviour was completely inappropriate.",
            "The _____ notion defied all logic.",
            "She dismissed the _____ argument as nonsense.",
        ]
    elif word_lower == "presumptuous":
        word_specific_sentences = [
            "It was _____ of him to assume he would win.",
            "The _____ comment showed he thought too highly of himself.",
            "She found his _____ behaviour quite rude.",
            "The _____ way he took charge was inappropriate.",
            "His _____ assumption that he was invited was wrong.",
            "The _____ request showed a lack of respect.",
            "She was offended by his _____ attitude.",
            "The _____ manner in which he spoke was arrogant.",
            "His _____ actions suggested he felt entitled.",
            "The _____ way he behaved made others uncomfortable.",
        ]
    elif word_lower == "pretence":
        word_specific_sentences = [
            "She kept up the _____ of being happy despite her sadness.",
            "The _____ that everything was fine fooled no one.",
            "His _____ of knowledge was quickly exposed.",
            "The _____ of friendship hid his true intentions.",
            "She dropped the _____ and told the truth.",
            "The _____ was maintained for weeks before the truth emerged.",
            "His _____ of innocence was not convincing.",
            "The _____ that he was qualified was a lie.",
            "She saw through the _____ immediately.",
            "The _____ was elaborate but ultimately transparent.",
        ]
    elif word_lower == "pretentious":
        word_specific_sentences = [
            "His _____ behaviour irritated everyone.",
            "The _____ way he spoke was designed to impress.",
            "She found his _____ attitude quite annoying.",
            "The _____ display of knowledge was unnecessary.",
            "His _____ manner made him seem fake.",
            "The _____ language he used was overly complicated.",
            "She avoided his _____ company at parties.",
            "The _____ way he presented himself was off-putting.",
            "His _____ attempts to seem cultured were obvious.",
            "The _____ nature of his speech was clear to all.",
        ]
    elif word_lower == "prevalent":
        word_specific_sentences = [
            "Flu is _____ during the winter months.",
            "The problem was _____ throughout the school.",
            "She noticed that mobile phones were _____ among teenagers.",
            "The attitude was _____ in that generation.",
            "His views were _____ among his peer group.",
            "The trend was _____ in urban areas.",
            "She found the practice _____ in many countries.",
            "The issue was _____ and needed addressing.",
            "His behaviour was _____ among students that age.",
            "The phenomenon was _____ in the region.",
        ]
    elif word_lower == "problematic":
        word_specific_sentences = [
            "The situation was becoming increasingly _____.",
            "She found the _____ issue difficult to resolve.",
            "The _____ behaviour needed to be addressed.",
            "His _____ attitude was causing problems.",
            "The _____ decision would have negative consequences.",
            "She identified several _____ areas in the plan.",
            "The _____ nature of the task made it challenging.",
            "His _____ approach was not working.",
            "The _____ situation required careful handling.",
            "She was concerned about the _____ implications.",
        ]
    elif word_lower == "proclivity":
        word_specific_sentences = [
            "He had a _____ for getting into trouble.",
            "The child showed a _____ for breaking things.",
            "Her _____ for helping others was well-known.",
            "The student's _____ for asking questions was evident.",
            "His _____ for adventure led him into risky situations.",
            "She had a natural _____ for mathematics.",
            "The _____ for procrastination was his weakness.",
            "His _____ for telling jokes made him popular.",
            "The _____ for creativity showed in her artwork.",
            "She noticed his _____ for arriving late.",
        ]
    elif word_lower == "prodigal":
        word_specific_sentences = [
            "The _____ son spent all his inheritance quickly.",
            "His _____ spending habits worried his parents.",
            "The _____ use of resources was wasteful.",
            "She was shocked by his _____ lifestyle.",
            "The _____ way he spent money was unsustainable.",
            "His _____ behaviour left him with nothing.",
            "The _____ approach to resources was short-sighted.",
            "She warned him about his _____ tendencies.",
            "The _____ spending spree emptied his savings.",
            "His _____ nature meant he never saved anything.",
        ]
    elif word_lower == "prodigious":
        word_specific_sentences = [
            "The child had _____ musical talent.",
            "Her _____ memory allowed her to remember everything.",
            "The _____ amount of work completed was impressive.",
            "His _____ strength surprised everyone.",
            "The _____ effort required was enormous.",
            "She showed _____ ability in multiple subjects.",
            "The _____ collection filled several rooms.",
            "His _____ achievements were recognised worldwide.",
            "The _____ size of the task was daunting.",
            "She possessed _____ knowledge of the subject.",
        ]
    elif word_lower == "profligate":
        word_specific_sentences = [
            "His _____ spending left him in debt.",
            "The _____ use of resources was wasteful.",
            "She was concerned about his _____ habits.",
            "The _____ lifestyle was unsustainable.",
            "His _____ behaviour showed no restraint.",
            "The _____ way he lived was reckless.",
            "She warned him about his _____ tendencies.",
            "The _____ approach to money was dangerous.",
            "His _____ spending was out of control.",
            "The _____ waste of materials was shocking.",
        ]
    elif word_lower == "profusion":
        word_specific_sentences = [
            "A _____ of flowers covered the garden.",
            "The _____ of colours in the sunset was beautiful.",
            "She was amazed by the _____ of wildlife.",
            "The _____ of options made choosing difficult.",
            "His collection showed a _____ of different items.",
            "The _____ of books filled the library shelves.",
            "She enjoyed the _____ of flavours in the meal.",
            "The _____ of stars in the night sky was spectacular.",
            "His garden had a _____ of vegetables.",
            "The _____ of ideas in the discussion was impressive.",
        ]
    elif word_lower == "proliferation":
        word_specific_sentences = [
            "The _____ of mobile phones changed how people communicate.",
            "She noticed the _____ of new shops in the area.",
            "The _____ of social media platforms was rapid.",
            "His concern was the _____ of fake news online.",
            "The _____ of technology in schools was evident.",
            "She studied the _____ of plant species in the region.",
            "The _____ of online courses offered more opportunities.",
            "His research focused on the _____ of the disease.",
            "The _____ of apps made choosing difficult.",
            "She observed the _____ of recycling schemes.",
        ]
    elif word_lower == "prolific":
        word_specific_sentences = [
            "The _____ author wrote over fifty books.",
            "Her _____ output of artwork was impressive.",
            "The _____ composer created hundreds of pieces.",
            "His _____ writing career spanned decades.",
            "The _____ garden produced vegetables all summer.",
            "She was known as a _____ contributor to the project.",
            "The _____ tree bore fruit every year.",
            "His _____ production of ideas was remarkable.",
            "The _____ artist's work was displayed everywhere.",
            "She admired the _____ nature of his creativity.",
        ]
    elif word_lower == "prominence":
        word_specific_sentences = [
            "The actor rose to _____ after his first major film.",
            "She achieved _____ in her field through hard work.",
            "The _____ of the issue made it front-page news.",
            "His rise to _____ was rapid and unexpected.",
            "The _____ of the building made it easy to find.",
            "She gained _____ through her charitable work.",
            "The _____ of the problem could not be ignored.",
            "His _____ as a scientist was well-deserved.",
            "The _____ of the topic in discussions was clear.",
            "She reached _____ in the world of literature.",
        ]
    elif word_lower == "prophetic":
        word_specific_sentences = [
            "His words proved to be _____ when the disaster occurred.",
            "The _____ warning was ignored at the time.",
            "She made a _____ statement about the future.",
            "The _____ dream seemed to predict events.",
            "His _____ insight into the situation was accurate.",
            "The _____ nature of her words became clear later.",
            "She had a _____ sense of what would happen.",
            "The _____ comment turned out to be true.",
            "His _____ ability to foresee problems was useful.",
            "The _____ message was understood only in hindsight.",
        ]
    elif word_lower == "protagonist":
        word_specific_sentences = [
            "The _____ of the story was a brave young girl.",
            "She identified with the _____ of the novel.",
            "The _____'s journey was the focus of the book.",
            "His role as the _____ required courage and determination.",
            "The _____ faced many challenges throughout the story.",
            "She admired the _____ for her strength and wisdom.",
            "The _____'s character developed throughout the narrative.",
            "His favourite part was when the _____ overcame the obstacle.",
            "The _____ of the play was played by a talented actor.",
            "She wrote an essay analysing the _____'s motivations.",
        ]
    elif word_lower == "provincial":
        word_specific_sentences = [
            "The _____ town was far from the capital city.",
            "She moved from the _____ area to the city.",
            "The _____ lifestyle was quieter than city life.",
            "His _____ accent revealed where he came from.",
            "The _____ newspaper covered local news.",
            "She preferred the _____ charm to urban bustle.",
            "The _____ government handled regional matters.",
            "His _____ background gave him a different perspective.",
            "The _____ setting was perfect for the story.",
            "She enjoyed visiting the _____ countryside.",
        ]
    elif word_lower == "provisional":
        word_specific_sentences = [
            "The _____ agreement would be reviewed next month.",
            "She received a _____ offer that might change.",
            "The _____ plan was subject to approval.",
            "His _____ acceptance depended on his exam results.",
            "The _____ arrangement was temporary.",
            "She made a _____ booking that could be cancelled.",
            "The _____ decision would be confirmed later.",
            "His _____ status would be reviewed annually.",
            "The _____ nature of the agreement was clear.",
            "She understood that the _____ terms might change.",
        ]
    elif word_lower == "provocative":
        word_specific_sentences = [
            "His _____ comments started an argument.",
            "The _____ question made everyone think deeply.",
            "She found the _____ artwork challenging.",
            "The _____ statement was designed to provoke discussion.",
            "His _____ behaviour was intended to get a reaction.",
            "The _____ nature of the topic led to debate.",
            "She avoided making _____ remarks.",
            "The _____ way he spoke caused controversy.",
            "His _____ approach was meant to challenge opinions.",
            "The _____ content of the article sparked discussion.",
        ]
    elif word_lower == "proximity":
        word_specific_sentences = [
            "The _____ of the shops was convenient.",
            "She chose the school because of its _____ to home.",
            "The _____ of the two buildings made walking easy.",
            "His house's _____ to the park was a bonus.",
            "The _____ of the stations made travel simple.",
            "She appreciated the _____ of her friends' houses.",
            "The _____ of the library encouraged frequent visits.",
            "His office's _____ to the train station was helpful.",
            "The _____ of the facilities made everything accessible.",
            "She valued the _____ of the school to her home.",
        ]
    elif word_lower == "pugnacious":
        word_specific_sentences = [
            "His _____ nature made him difficult to work with.",
            "The _____ student was always ready to argue.",
            "She avoided his _____ company at break time.",
            "The _____ way he responded to criticism was aggressive.",
            "His _____ attitude created conflict wherever he went.",
            "The _____ behaviour was not tolerated in the classroom.",
            "She found his _____ manner intimidating.",
            "The _____ way he approached debates was confrontational.",
            "His _____ personality made him unpopular.",
            "The _____ nature of his comments was off-putting.",
        ]
    elif word_lower == "quandary" or word_lower == "quondary":
        word_specific_sentences = [
            "She was in a _____ about which university to choose.",
            "The difficult _____ required careful consideration.",
            "His _____ about the decision kept him awake at night.",
            "The _____ seemed impossible to resolve.",
            "She found herself in a _____ with no clear answer.",
            "The _____ of choosing between two good options was tricky.",
            "His _____ about what to do next was understandable.",
            "The _____ required advice from others.",
            "She was stuck in a _____ that needed solving.",
            "The _____ made decision-making very difficult.",
        ]
    elif word_lower == "quarantine":
        word_specific_sentences = [
            "The sick animals were kept in _____.",
            "She had to stay in _____ after returning from abroad.",
            "The _____ period lasted for two weeks.",
            "His pet was placed in _____ at the vet's.",
            "The _____ prevented the disease from spreading.",
            "She followed the _____ rules carefully.",
            "The _____ area was clearly marked.",
            "His time in _____ was boring but necessary.",
            "The _____ helped protect others from illness.",
            "She understood the importance of the _____ measures.",
        ]
    elif word_lower == "quintessential":
        word_specific_sentences = [
            "She was the _____ English teacher.",
            "The _____ example of kindness was shown by her actions.",
            "His behaviour was the _____ definition of politeness.",
            "The _____ British afternoon tea was served.",
            "She represented the _____ student everyone admired.",
            "The _____ nature of the scene was perfect.",
            "His work was the _____ representation of the style.",
            "The _____ character of the place was evident.",
            "She embodied the _____ qualities of a leader.",
            "The _____ moment captured everything perfectly.",
        ]
    elif word_lower == "ramification":
        word_specific_sentences = [
            "The _____ of his decision affected many people.",
            "She considered the _____ before making her choice.",
            "The _____ of the policy change were significant.",
            "His actions had serious _____ for everyone involved.",
            "The _____ of the problem were complex.",
            "She didn't anticipate all the _____ of her actions.",
            "The _____ spread throughout the organisation.",
            "His mistake had _____ that lasted for years.",
            "The _____ of the issue were far-reaching.",
            "She studied the _____ carefully before deciding.",
        ]
    elif word_lower == "rapacious":
        word_specific_sentences = [
            "The _____ landlord raised the rent unfairly.",
            "His _____ appetite for power was concerning.",
            "The _____ way he took everything was greedy.",
            "She was shocked by his _____ behaviour.",
            "The _____ nature of his demands was excessive.",
            "His _____ approach to business was unethical.",
            "The _____ way he consumed resources was wasteful.",
            "She found his _____ attitude towards money disturbing.",
            "The _____ greed was evident in all his actions.",
            "His _____ desire for more was never satisfied.",
        ]
    elif word_lower == "reactionary":
        word_specific_sentences = [
            "The _____ politician opposed all changes.",
            "His _____ views were outdated and unpopular.",
            "The _____ group resisted modern ideas.",
            "She found his _____ attitude frustrating.",
            "The _____ approach rejected progress.",
            "His _____ beliefs were from a different era.",
            "The _____ nature of his opinions was clear.",
            "She disagreed with his _____ stance on the issue.",
            "The _____ movement opposed social reforms.",
            "His _____ thinking prevented innovation.",
        ]
    elif word_lower == "rebuttal":
        word_specific_sentences = [
            "Her _____ of the accusation was convincing.",
            "The _____ addressed each point systematically.",
            "His _____ of the argument was well-prepared.",
            "The _____ showed flaws in the original claim.",
            "She prepared a strong _____ to defend herself.",
            "The _____ effectively countered the criticism.",
            "His _____ was clear and logical.",
            "The _____ of the theory was supported by evidence.",
            "She delivered her _____ with confidence.",
            "The _____ successfully refuted the allegations.",
        ]
    elif word_lower == "recalcitrant":
        word_specific_sentences = [
            "The _____ student refused to follow rules.",
            "His _____ behaviour caused problems in class.",
            "The _____ child wouldn't do as he was told.",
            "She found his _____ attitude frustrating.",
            "The _____ way he resisted authority was problematic.",
            "His _____ nature made him difficult to manage.",
            "The _____ response showed he wouldn't cooperate.",
            "She struggled with the _____ pupil's disobedience.",
            "The _____ behaviour required intervention.",
            "His _____ refusal to comply was stubborn.",
        ]
    elif word_lower == "receptacle":
        word_specific_sentences = [
            "She placed the flowers in a beautiful _____.",
            "The _____ was used to collect the rubbish.",
            "His _____ for storing tools was well-organised.",
            "The _____ held all the necessary items.",
            "She found a suitable _____ for the collection.",
            "The _____ was large enough for everything.",
            "His _____ for papers kept his desk tidy.",
            "The _____ served its purpose well.",
            "She chose a decorative _____ for the display.",
            "The _____ was made of sturdy material.",
        ]
    elif word_lower == "receptive":
        word_specific_sentences = [
            "She was _____ to the new suggestions.",
            "The _____ audience listened carefully to the speaker.",
            "His _____ attitude helped him learn quickly.",
            "The _____ way she considered ideas was helpful.",
            "She showed a _____ approach to feedback.",
            "The _____ nature of the group encouraged discussion.",
            "His _____ mind was open to new possibilities.",
            "The _____ response showed willingness to change.",
            "She was _____ to different points of view.",
            "The _____ attitude made collaboration easier.",
        ]
    elif word_lower == "reclusive":
        word_specific_sentences = [
            "The _____ author rarely gave interviews.",
            "His _____ lifestyle meant he avoided social events.",
            "The _____ neighbour kept to himself.",
            "She lived a _____ existence in the countryside.",
            "The _____ way he avoided people was unusual.",
            "His _____ nature meant he had few friends.",
            "The _____ behaviour showed he preferred solitude.",
            "She respected his _____ choice to live alone.",
            "The _____ lifestyle suited his personality.",
            "His _____ habits made him hard to get to know.",
        ]
    elif word_lower == "recuperate":
        word_specific_sentences = [
            "She needed time to _____ after the operation.",
            "The patient took weeks to _____ from the illness.",
            "His time to _____ was essential for recovery.",
            "The _____ period allowed her body to heal.",
            "She went to the countryside to _____ from stress.",
            "The _____ process was slow but steady.",
            "His ability to _____ quickly surprised the doctors.",
            "The _____ time was necessary for full recovery.",
            "She used the holiday to _____ from work.",
            "The _____ period helped restore his strength.",
        ]
    elif word_lower == "redemption":
        word_specific_sentences = [
            "He sought _____ for his past mistakes.",
            "The _____ of his reputation took years.",
            "Her act of kindness was a form of _____.",
            "The _____ story showed how people can change.",
            "He worked hard to achieve _____ for his errors.",
            "The _____ of the character was the story's theme.",
            "Her _____ came through helping others.",
            "The _____ process required genuine change.",
            "He found _____ in his charitable work.",
            "The _____ of his actions was recognised by all.",
        ]
    elif word_lower == "redundant":
        word_specific_sentences = [
            "Several workers were made _____.",
            "The _____ information was removed from the report.",
            "His role became _____ after the restructuring.",
            "The _____ words were deleted to improve clarity.",
            "She found her job was _____ due to automation.",
            "The _____ system was replaced with a new one.",
            "His _____ comment added nothing to the discussion.",
            "The _____ equipment was no longer needed.",
            "She realised her help was _____ as they had finished.",
            "The _____ process was eliminated to save time.",
        ]
    elif word_lower == "reflective":
        word_specific_sentences = [
            "She was in a _____ mood after the exam.",
            "The _____ surface showed her reflection clearly.",
            "His _____ thinking helped him understand the problem.",
            "The _____ way she considered her actions was mature.",
            "She took a _____ approach to learning from mistakes.",
            "The _____ nature of the discussion was thoughtful.",
            "His _____ attitude showed he was learning.",
            "The _____ material made the jacket visible at night.",
            "She showed _____ behaviour by considering others' feelings.",
            "The _____ process helped improve her work.",
        ]
    elif word_lower == "reinvigorate":
        word_specific_sentences = [
            "The holiday helped to _____ her enthusiasm.",
            "The new project would _____ the team's energy.",
            "His speech helped _____ the audience's interest.",
            "The change would _____ the old system.",
            "She hoped the break would _____ her motivation.",
            "The new approach would _____ their efforts.",
            "His ideas helped _____ the discussion.",
            "The renovation would _____ the building.",
            "She found the exercise helped _____ her mind.",
            "The fresh start would _____ their commitment.",
        ]
    elif word_lower == "relatively":
        word_specific_sentences = [
            "The task was _____ easy compared to the previous one.",
            "She found the work _____ simple after practice.",
            "The problem was _____ minor compared to others.",
            "His score was _____ high for his age group.",
            "The distance was _____ short, so they walked.",
            "She considered the price _____ reasonable.",
            "The weather was _____ mild for winter.",
            "His performance was _____ good considering the circumstances.",
            "The issue was _____ unimportant in the grand scheme.",
            "She found the book _____ interesting, though not her favourite.",
        ]
    elif word_lower == "relinquish":
        word_specific_sentences = [
            "He had to _____ his position as captain.",
            "She was unwilling to _____ control of the project.",
            "The decision to _____ power was difficult.",
            "He refused to _____ his claim to the title.",
            "She had to _____ her hold on the rope.",
            "The _____ of his responsibilities was necessary.",
            "He was forced to _____ his ownership of the property.",
            "She finally agreed to _____ her grip on the situation.",
            "The _____ of control was hard for him.",
            "She had to _____ her role to someone else.",
        ]
    elif word_lower == "reluctant":
        word_specific_sentences = [
            "He was _____ to admit his mistake.",
            "The _____ student finally agreed to participate.",
            "She was _____ to share her ideas at first.",
            "The _____ way he approached the task showed hesitation.",
            "He remained _____ about changing his mind.",
            "The _____ acceptance came only after persuasion.",
            "She was _____ to leave her friends behind.",
            "The _____ agreement was given with reservations.",
            "He showed a _____ attitude towards the new plan.",
            "The _____ response indicated she wasn't fully convinced.",
        ]
    elif word_lower == "reminiscent":
        word_specific_sentences = [
            "The old house was _____ of her childhood home.",
            "The scene was _____ of a painting she had seen.",
            "His story was _____ of adventures from books.",
            "The smell was _____ of her grandmother's kitchen.",
            "She found the situation _____ of a previous experience.",
            "The style was _____ of an earlier period.",
            "His behaviour was _____ of his father's.",
            "The atmosphere was _____ of happier times.",
            "She noticed the pattern was _____ of something familiar.",
            "The feeling was _____ of being at home.",
        ]
    elif word_lower == "repentant":
        word_specific_sentences = [
            "The _____ thief returned the stolen goods.",
            "His _____ attitude showed genuine remorse.",
            "The _____ way he apologised was sincere.",
            "She hoped he was truly _____ for his actions.",
            "The _____ student promised to do better.",
            "His _____ behaviour indicated he had learned.",
            "The _____ expression showed he was sorry.",
            "She accepted his _____ apology.",
            "The _____ nature of his response was clear.",
            "His _____ words showed he understood his mistake.",
        ]
    elif word_lower == "repercussions":
        word_specific_sentences = [
            "The decision had serious _____ for everyone involved.",
            "She didn't anticipate the _____ of her actions.",
            "The _____ of the policy change were widespread.",
            "His mistake had _____ that affected many people.",
            "The _____ spread throughout the organisation.",
            "She considered the possible _____ before deciding.",
            "The _____ of the problem were complex.",
            "His actions had _____ that lasted for years.",
            "The _____ were more severe than expected.",
            "She faced the _____ of her choices.",
        ]
    elif word_lower == "reprehensible":
        word_specific_sentences = [
            "His _____ behaviour shocked everyone.",
            "The _____ act was condemned by all.",
            "She found his _____ actions completely unacceptable.",
            "The _____ way he treated others was disgraceful.",
            "His _____ conduct deserved punishment.",
            "The _____ nature of the crime was evident.",
            "She was appalled by his _____ behaviour.",
            "The _____ treatment of animals was wrong.",
            "His _____ attitude was inexcusable.",
            "The _____ actions were met with disapproval.",
        ]
    elif word_lower == "repugnant":
        word_specific_sentences = [
            "The idea was _____ to everyone.",
            "She found the _____ smell unbearable.",
            "The _____ suggestion was immediately rejected.",
            "His _____ behaviour disgusted those around him.",
            "The _____ nature of the proposal was clear.",
            "She thought the _____ idea was completely unacceptable.",
            "The _____ taste made her feel sick.",
            "His _____ attitude was offensive to all.",
            "The _____ concept was against her values.",
            "She found the _____ thought deeply disturbing.",
        ]
    elif word_lower == "repulsive":
        word_specific_sentences = [
            "The _____ smell came from the rubbish bin.",
            "She found the _____ sight difficult to look at.",
            "The _____ behaviour made everyone uncomfortable.",
            "His _____ attitude drove people away.",
            "The _____ nature of the crime was shocking.",
            "She thought the _____ idea was disgusting.",
            "The _____ appearance was off-putting.",
            "His _____ comments were completely inappropriate.",
            "The _____ way he acted was unacceptable.",
            "She found the _____ smell overwhelming.",
        ]
    elif word_lower == "resilience":
        word_specific_sentences = [
            "Her _____ helped her overcome many challenges.",
            "The _____ of the material made it durable.",
            "His _____ in the face of adversity was admirable.",
            "The _____ shown by the team was impressive.",
            "She demonstrated great _____ during difficult times.",
            "The _____ of the structure withstood the storm.",
            "His _____ helped him bounce back quickly.",
            "The _____ of her spirit was remarkable.",
            "She showed _____ by continuing despite setbacks.",
            "The _____ of the community was tested and proven.",
        ]
    elif word_lower == "resonant":
        word_specific_sentences = [
            "The _____ bell could be heard across the valley.",
            "Her _____ voice filled the concert hall.",
            "The _____ sound echoed through the cave.",
            "His _____ words stayed with her for days.",
            "The _____ quality of the music was beautiful.",
            "She found his _____ speech moving.",
            "The _____ tone of his voice was memorable.",
            "His _____ message had a lasting impact.",
            "The _____ nature of the sound was impressive.",
            "She appreciated the _____ quality of the performance.",
        ]
    elif word_lower == "resplendent":
        word_specific_sentences = [
            "The queen appeared in _____ robes.",
            "The _____ display of colours was magnificent.",
            "Her _____ appearance at the ball was stunning.",
            "The _____ sunset painted the sky beautifully.",
            "His _____ costume was the most elaborate.",
            "The _____ garden was full of vibrant flowers.",
            "She looked _____ in her wedding dress.",
            "The _____ decorations transformed the hall.",
            "His _____ uniform showed his rank clearly.",
            "The _____ beauty of the scene was breathtaking.",
        ]
    elif word_lower == "responsibility":
        word_specific_sentences = [
            "Taking care of the pet was her _____.",
            "The _____ of leadership was heavy.",
            "His _____ for the project was clear.",
            "The _____ weighed on her shoulders.",
            "She took her _____ seriously.",
            "The _____ of being captain was important to him.",
            "His _____ included looking after younger students.",
            "The _____ was shared among the team members.",
            "She understood the _____ that came with the role.",
            "The _____ of making the decision was hers alone.",
        ]
    elif word_lower == "reticent":
        word_specific_sentences = [
            "He was _____ about his personal life.",
            "The _____ student rarely spoke in class.",
            "Her _____ nature made her seem shy.",
            "The _____ way he answered suggested he was hiding something.",
            "He remained _____ even when asked directly.",
            "The _____ response didn't reveal much.",
            "She was _____ about sharing her feelings.",
            "The _____ attitude made communication difficult.",
            "His _____ behaviour was unusual for someone so outgoing before.",
            "The _____ nature of her response was frustrating.",
        ]
    elif word_lower == "reverence":
        word_specific_sentences = [
            "They showed _____ for the ancient monument.",
            "The _____ with which he spoke was respectful.",
            "Her _____ for her teacher was evident.",
            "The _____ shown to the elderly was touching.",
            "He treated the old book with great _____.",
            "The _____ for tradition was important to them.",
            "She showed _____ when visiting the memorial.",
            "The _____ in his voice showed deep respect.",
            "His _____ for nature was clear from his actions.",
            "The _____ with which they approached the ceremony was appropriate.",
        ]
    else:
        # Fallback: generate generic sentences based on word type
        if is_verb:
            word_specific_sentences = [
                f"She learned how to _____ properly.",
                f"The teacher asked them to _____ carefully.",
                f"He tried to _____ but found it difficult.",
                f"They needed to _____ before proceeding.",
                f"She wanted to _____ but wasn't sure how.",
                f"The instructions explained how to _____.",
                f"He decided to _____ after thinking about it.",
                f"They were told to _____ immediately.",
                f"She helped him _____ correctly.",
                f"The goal was to _____ effectively.",
            ]
        elif is_adjective:
            word_specific_sentences = [
                f"The _____ student worked hard.",
                f"Her _____ attitude was appreciated.",
                f"The _____ way he behaved was noticeable.",
                f"She found the _____ approach helpful.",
                f"The _____ nature of the problem was clear.",
                f"His _____ behaviour surprised everyone.",
                f"The _____ quality made it special.",
                f"She showed a _____ understanding.",
                f"The _____ character was evident.",
                f"His _____ manner was distinctive.",
            ]
        else:  # noun
            word_specific_sentences = [
                f"The _____ was important to understand.",
                f"She learned about the _____ in class.",
                f"The _____ helped explain the concept.",
                f"His understanding of the _____ was clear.",
                f"The _____ was discussed in detail.",
                f"She studied the _____ carefully.",
                f"The _____ played a key role.",
                f"His knowledge of the _____ was impressive.",
                f"The _____ was the focus of attention.",
                f"She explained the _____ clearly.",
            ]
    
    # Add word-specific sentences, avoiding duplicates
    for sent in word_specific_sentences:
        blank_sent = create_blank_sentence(sent, word)
        if "_____" in blank_sent and blank_sent not in seen:
            sentences.append(blank_sent)
            seen.add(blank_sent)
            if len(sentences) >= 10:
                break
    
    # If we still don't have 10 sentences, generate more using meaning and context
    while len(sentences) < 10:
        # Use meaning, synonym, and antonym to create contextual sentences
        if is_verb:
            base = f"She needed to {word_lower} the situation carefully."
        elif is_adjective:
            base = f"The {word_lower} approach was effective."
        else:
            base = f"The {word_lower} was important."
        
        blank_base = create_blank_sentence(base, word)
        if "_____" in blank_base and blank_base not in seen:
            sentences.append(blank_base)
            seen.add(blank_base)
        else:
            break
    
    return sentences[:10]


def main():
    """Generate quiz sentences for all words in level4_batch4.txt."""
    input_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level4_batch4.txt")
    output_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level4_batch4.csv")
    
    sentences_generated = 0
    
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        
        writer = csv.writer(f_out)
        writer.writerow(['level', 'word', 'sentence'])
        
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            
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
            
            # Write sentences to CSV
            for sentence in sentences:
                writer.writerow(['4', word, sentence])
                sentences_generated += 1
    
    print(f"Level 4 Batch 4 complete: {sentences_generated} sentences")


if __name__ == "__main__":
    main()
