#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 3 Batch 2 vocabulary words.
Creates 10 contextually rich sentences per word with varied structures.
"""

import csv
import re
from pathlib import Path
from typing import List, Tuple


def parse_word_line(line: str) -> Tuple[str, str, str, str, str]:
    """Parse a line from the word list file."""
    parts = line.strip().split('|')
    if len(parts) >= 5:
        word = parts[0].strip()
        meaning = parts[1].strip()
        example = parts[2].strip()
        synonym = parts[3].strip() if len(parts) > 3 else ""
        antonym = parts[4].strip() if len(parts) > 4 else ""
        return word, meaning, example, synonym, antonym
    return None, None, None, None, None


def determine_part_of_speech(word: str, meaning: str) -> str:
    """Determine if word is verb, adjective, or noun based on word form and meaning."""
    meaning_lower = meaning.lower()
    word_lower = word.lower()
    
    # Priority 1: Check for explicit verb indicators (most specific first)
    if meaning_lower.startswith("to "):
        return "verb"
    
    # Check for verb action words
    verb_action_words = [
        "discussed or gave", "to take", "to think", "to give", "to confirm",
        "to spread", "to disappear", "to cause", "to make more", "to criticise",
        "to express", "to become", "to decline", "to break", "to describe",
        "to outline", "to destroy", "to move", "to make", "to weaken",
        "to support", "to waste", "to give rise", "to decorate", "to belittle"
    ]
    
    if any(action in meaning_lower for action in verb_action_words):
        return "verb"
    
    # Check for past participle adjectives (state descriptions)
    past_participle_adjectives = [
        "taken away", "seized", "returned", "demolished", "confiscated"
    ]
    
    if any(adj in meaning_lower for adj in past_participle_adjectives):
        # Verify it's describing a state, not an action
        if any(state_word in meaning_lower for state_word in [
            "by authority", "were kept", "was", "items were"
        ]):
            return "adjective"
    
    # Priority 2: Check for noun indicators (specific patterns)
    if meaning_lower.startswith(("an ", "a ")):
        return "noun"
    
    noun_patterns = [
        "an expert", "a limit", "a restriction", "a conclusion", "a belief",
        "an attitude", "a behaviour", "the length", "an outpouring", "the ability",
        "people who", "something that", "a state of", "a difference"
    ]
    
    if any(pattern in meaning_lower for pattern in noun_patterns):
        return "noun"
    
    # Priority 3: Check for adjective indicators
    adjective_patterns = [
        "helping to", "pleasant", "friendly", "awake", "aware", "happy", 
        "satisfied", "artificial", "complex", "confusing", "causing",
        "willing", "sad", "disappointed", "deserving", "usual", "distrustful",
        "weak", "luxurious", "able to", "respectful", "bold", "done on purpose",
        "very pleasant", "wildly excited", "completely", "morally bad",
        "making one feel", "insane", "mocking", "empty", "in a very urgent",
        "strongly disliked", "not connected", "becoming progressively",
        "lacking confidence", "in a state of", "showing good", "confused",
        "untidy", "impartial", "very different", "not influenced", "unpleasant",
        "respected", "causing worry", "developing in different", "asserting",
        "cheerful", "unconventional", "selecting from", "expressing ideas",
        "deeply involved", "expressing something", "delightfully", "lasting",
        "fully absorbed", "mysterious", "continuous", "unchanging"
    ]
    
    if any(pattern in meaning_lower for pattern in adjective_patterns):
        return "adjective"
    
    # Default to noun if unclear
    return "noun"


def create_blank_sentence(sentence: str, word: str) -> str:
    """Replace word with blank in sentence, handling case variations."""
    # Create pattern that matches word with word boundaries, case-insensitive
    pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
    return pattern.sub("_____", sentence)


def generate_verb_sentences(word: str, meaning: str, example: str, synonym: str, antonym: str) -> List[str]:
    """Generate 10 varied sentences for verbs."""
    sentences = []
    word_lower = word.lower()
    
    # Use example sentence if available
    if example and word.lower() in example.lower():
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate contextually rich verb sentences
    verb_patterns = [
        # Action scenarios
        f"The teacher had to _____ the mobile phone because the student was using it during the lesson.",
        f"Before making such an important decision, you should _____ all the possible outcomes carefully.",
        f"The scientists needed to _____ their findings with additional evidence from other studies.",
        f"Her parents would _____ any electronic devices if she didn't complete her homework on time.",
        f"The committee members will _____ about the best approach to solve this difficult problem.",
        f"To improve your skills, you must _____ regularly and stay focused on your goals.",
        f"The detective tried to _____ what had happened by examining all the clues carefully.",
        f"Students are expected to _____ their ideas during group discussions in class.",
        f"The headteacher had to _____ the situation before deciding on the appropriate action.",
        f"Parents often _____ with teachers to discuss their children's progress at school.",
        f"The judge must _____ all the evidence before reaching a final decision.",
        f"Scientists work hard to _____ new information that can help solve important problems.",
        f"The team captain will _____ with the coach about the best strategy for the match.",
        f"Teachers sometimes need to _____ items that distract students from their learning.",
        f"Before the meeting, they decided to _____ the main points they wanted to discuss.",
    ]
    
    # Add context-specific sentences based on meaning
    meaning_lower = meaning.lower()
    
    if "take away" in meaning_lower or "confiscate" in meaning_lower or "seize" in meaning_lower:
        sentences.extend([
            f"The librarian will _____ any books that are overdue for more than two weeks.",
            f"School rules state that teachers can _____ mobile phones if they are used inappropriately.",
            f"The headteacher had to _____ the contraband items found in the student's bag.",
            f"Parents were informed that the school would _____ any dangerous items immediately.",
            f"The teacher warned that she would _____ any toys brought into the classroom.",
        ])
    elif "discuss" in meaning_lower or "confer" in meaning_lower or "gave" in meaning_lower:
        sentences.extend([
            f"The two friends decided to _____ about where to go for their school trip.",
            f"Before the school play, the director needed to _____ with all the actors about their roles.",
            f"The teachers will _____ about the best way to help struggling students.",
            f"They decided to _____ the award to the most deserving candidate.",
            f"The committee members will _____ honours upon the winners at the ceremony.",
        ])
    elif "think" in meaning_lower or "consider" in meaning_lower:
        sentences.extend([
            f"She sat quietly in the garden to _____ her future plans for secondary school.",
            f"Before choosing a book, he liked to _____ which story would be most interesting.",
        ])
    elif "confirm" in meaning_lower or "support" in meaning_lower:
        sentences.extend([
            f"The witness was able to _____ what the other person had seen at the scene.",
            f"Several students could _____ that the event had happened exactly as described.",
        ])
    elif "spread" in meaning_lower:
        sentences.extend([
            f"The school newsletter helps to _____ important information to all parents.",
            f"Social media can quickly _____ news throughout the entire school community.",
        ])
    elif "disappear" in meaning_lower or "waste" in meaning_lower:
        sentences.extend([
            f"The morning fog began to _____ as the sun rose higher in the sky.",
            f"His enthusiasm seemed to _____ after he received disappointing test results.",
        ])
    elif "cause" in meaning_lower or "give rise" in meaning_lower:
        sentences.extend([
            f"Kindness can _____ trust and friendship among classmates.",
            f"Good leadership can _____ loyalty and respect from team members.",
        ])
    elif "make more attractive" in meaning_lower or "decorate" in meaning_lower:
        sentences.extend([
            f"The author liked to _____ her stories with vivid descriptions of the settings.",
            f"He decided to _____ his presentation with colourful illustrations and diagrams.",
        ])
    elif "criticise" in meaning_lower or "belittle" in meaning_lower:
        sentences.extend([
            f"It's unkind to _____ someone's efforts when they are trying their best.",
            f"She didn't want to _____ her friend's artwork, even though it wasn't perfect.",
        ])
    elif "express disapproval" in meaning_lower:
        sentences.extend([
            f"The teacher didn't want to _____ the student's creative approach to the problem.",
            f"Parents should not _____ their children's honest attempts to help others.",
        ])
    
    # Fill remaining slots with generic patterns if needed
    while len(sentences) < 10:
        for pattern in verb_patterns:
            if pattern not in sentences and len(sentences) < 10:
                sentences.append(pattern)
            if len(sentences) >= 10:
                break
    
    return sentences[:10]


def generate_adjective_sentences(word: str, meaning: str, example: str, synonym: str, antonym: str) -> List[str]:
    """Generate 10 varied sentences for adjectives."""
    sentences = []
    word_lower = word.lower()
    
    # Use example sentence if available
    if example and word.lower() in example.lower():
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate contextually rich adjective sentences
    meaning_lower = meaning.lower()
    
    # Context-specific sentences based on meaning
    if "taken away" in meaning_lower or "seized" in meaning_lower or "confiscated" in meaning_lower:
        sentences.extend([
            f"The _____ items were kept safely in the headteacher's office until collection.",
            f"All _____ mobile phones would be returned at the end of the school day.",
            f"The _____ equipment remained locked away in the storage cupboard.",
            f"Parents were notified about the _____ belongings found in their child's bag.",
            f"The _____ toys were placed in a box to be collected later.",
        ])
    elif "pleasant" in meaning_lower or "friendly" in meaning_lower:
        sentences.extend([
            f"The new student found the classroom atmosphere very _____ and welcoming.",
            f"Her _____ smile made everyone feel comfortable and at ease.",
            f"The _____ teacher always greeted students with enthusiasm each morning.",
            f"They enjoyed the _____ conversation during their lunch break together.",
            f"The _____ environment helped everyone work together successfully.",
        ])
    elif "helping to make" in meaning_lower or "conducive" in meaning_lower:
        sentences.extend([
            f"A quiet study area is _____ to better concentration and learning.",
            f"The peaceful library atmosphere was _____ to completing homework effectively.",
            f"Regular practice is _____ to improving your skills over time.",
        ])
    elif "awake" in meaning_lower or "aware" in meaning_lower:
        sentences.extend([
            f"She was fully _____ after the short nap and ready to continue studying.",
            f"The patient became _____ shortly after the operation was completed.",
            f"He remained _____ of everything happening around him during the lesson.",
        ])
    elif "happy" in meaning_lower or "satisfied" in meaning_lower:
        sentences.extend([
            f"The _____ cat purred contentedly while sitting on the warm windowsill.",
            f"After receiving excellent marks, she felt completely _____ with her efforts.",
            f"His _____ expression showed that he was pleased with the results.",
        ])
    elif "artificial" in meaning_lower or "not genuine" in meaning_lower:
        sentences.extend([
            f"The happy ending felt _____ and didn't match the rest of the story.",
            f"Her smile seemed _____ because her eyes showed she was actually upset.",
            f"The _____ dialogue in the play made it difficult to believe the characters.",
        ])
    elif "complex" in meaning_lower or "confusing" in meaning_lower:
        sentences.extend([
            f"The _____ plot of the mystery novel confused many readers.",
            f"His explanation was so _____ that nobody could understand it properly.",
            f"The _____ instructions made it nearly impossible to complete the task.",
        ])
    elif "willing to believe" in meaning_lower or "gullible" in meaning_lower:
        sentences.extend([
            f"The _____ child believed every story her older brother told her.",
            f"Being too _____ can sometimes lead to believing things that aren't true.",
            f"Her _____ nature made her an easy target for practical jokes.",
        ])
    elif "sad" in meaning_lower or "disappointed" in meaning_lower:
        sentences.extend([
            f"He looked _____ when he discovered he hadn't won the competition.",
            f"Her _____ expression showed how disappointed she was with the news.",
            f"The _____ team walked slowly off the pitch after losing the match.",
        ])
    elif "deserving blame" in meaning_lower or "guilty" in meaning_lower:
        sentences.extend([
            f"He was found _____ for breaking the school window with his football.",
            f"The investigation showed that she was _____ of the mistake.",
            f"Being _____ meant he had to face the consequences of his actions.",
        ])
    elif "usual" in meaning_lower or "according to custom" in meaning_lower:
        sentences.extend([
            f"It is _____ to bring a small gift when visiting someone's home.",
            f"The _____ greeting in their culture involves shaking hands firmly.",
            f"Following _____ practice, they celebrated the occasion with a special meal.",
        ])
    elif "distrustful" in meaning_lower or "sceptical" in meaning_lower:
        sentences.extend([
            f"His _____ attitude made him question everyone's motives.",
            f"The _____ student doubted that the excuse was genuine.",
            f"Her _____ nature prevented her from trusting the stranger's story.",
        ])
    elif "weak" in meaning_lower:
        sentences.extend([
            f"The illness began to make her feel _____ and tired.",
            f"Lack of exercise can _____ even the strongest person over time.",
        ])
    elif "luxurious" in meaning_lower or "indulgent" in meaning_lower:
        sentences.extend([
            f"The _____ chocolate cake was too tempting to resist.",
            f"They enjoyed the _____ meal at the fancy restaurant.",
            f"The _____ decorations made the party feel very special indeed.",
        ])
    elif "able to make decisions" in meaning_lower:
        sentences.extend([
            f"The _____ captain quickly chose the best strategy for the team.",
            f"Her _____ leadership helped the group complete the project on time.",
            f"Being _____ is an important quality for any good leader.",
        ])
    elif "respectful" in meaning_lower:
        sentences.extend([
            f"The students showed _____ behaviour towards their elderly teacher.",
            f"Her _____ attitude impressed everyone at the school assembly.",
            f"They listened with _____ attention to the guest speaker's presentation.",
        ])
    elif "bold resistance" in meaning_lower:
        sentences.extend([
            f"His _____ refusal to follow the rules resulted in a detention.",
            f"The student's _____ attitude towards authority caused problems.",
            f"Her _____ behaviour showed she wasn't afraid to stand up for herself.",
        ])
    elif "done on purpose" in meaning_lower or "intentional" in meaning_lower:
        sentences.extend([
            f"The _____ mistake was actually part of his clever plan.",
            f"She made a _____ choice to help her friend despite the consequences.",
            f"His _____ decision to speak up showed great courage.",
        ])
    elif "very pleasant" in meaning_lower:
        sentences.extend([
            f"The _____ garden was full of colourful flowers and singing birds.",
            f"They had a _____ time exploring the new adventure playground.",
            f"Her _____ personality made her popular with all her classmates.",
        ])
    elif "wildly excited" in meaning_lower or "confused" in meaning_lower:
        sentences.extend([
            f"The fans were _____ with joy when their team scored the winning goal.",
            f"After winning the competition, she felt _____ with happiness.",
            f"The _____ crowd cheered loudly as the band took the stage.",
        ])
    elif "completely destroyed" in meaning_lower:
        sentences.extend([
            f"The old building was _____ to make space for a new playground.",
            f"After the storm, many trees were _____ by the strong winds.",
        ])
    elif "morally bad" in meaning_lower or "wicked" in meaning_lower:
        sentences.extend([
            f"The villain's _____ actions shocked everyone in the story.",
            f"His _____ behaviour showed he had no concern for others.",
        ])
    elif "making one feel sad" in meaning_lower:
        sentences.extend([
            f"The _____ news about the school closure spread quickly.",
            f"Watching the _____ film made her feel very emotional.",
            f"The _____ weather matched everyone's gloomy mood perfectly.",
        ])
    elif "insane" in meaning_lower or "mentally disturbed" in meaning_lower:
        sentences.extend([
            f"The _____ character in the story frightened all the readers.",
            f"His _____ behaviour worried everyone who knew him.",
        ])
    elif "mocking" in meaning_lower or "scornful" in meaning_lower:
        sentences.extend([
            f"Her _____ laughter made him feel embarrassed and upset.",
            f"The _____ comments hurt the young performer's feelings.",
            f"His _____ tone showed he didn't take the situation seriously.",
        ])
    elif "empty" in meaning_lower or "bleak" in meaning_lower or "lonely" in meaning_lower:
        sentences.extend([
            f"The _____ landscape stretched for miles without any trees or buildings.",
            f"They walked through the _____ countryside feeling quite alone.",
            f"The _____ beach had no visitors except for a few seagulls.",
        ])
    elif "in a very urgent" in meaning_lower:
        sentences.extend([
            f"He _____ searched for his lost puppy throughout the entire park.",
            f"She _____ needed help with her homework before the deadline.",
            f"They _____ tried to finish the project before the bell rang.",
        ])
    elif "strongly disliked" in meaning_lower or "hated" in meaning_lower:
        sentences.extend([
            f"The _____ villain finally received the punishment he deserved.",
            f"Her _____ behaviour made her very unpopular with classmates.",
        ])
    elif "not connected" in meaning_lower or "emotionally uninvolved" in meaning_lower:
        sentences.extend([
            f"She remained emotionally _____ during the sad film, showing no reaction.",
            f"The _____ observer watched the events without getting involved.",
            f"His _____ attitude made it seem like he didn't care about the problem.",
        ])
    elif "becoming progressively worse" in meaning_lower:
        sentences.extend([
            f"The weather began to _____ as dark clouds gathered overhead.",
            f"Her health started to _____ after she stopped exercising regularly.",
        ])
    elif "lacking confidence" in meaning_lower or "shy" in meaning_lower:
        sentences.extend([
            f"The _____ student rarely raised her hand to answer questions.",
            f"His _____ manner made it difficult for him to make new friends.",
            f"Being so _____ prevented her from joining the school play.",
        ])
    elif "in a state of disrepair" in meaning_lower:
        sentences.extend([
            f"The _____ cottage needed extensive repairs before anyone could live there.",
            f"They explored the _____ building carefully, watching for loose floorboards.",
        ])
    elif "showing careful effort" in meaning_lower or "hardworking" in meaning_lower:
        sentences.extend([
            f"The _____ student always completed her homework on time and thoroughly.",
            f"Her _____ approach to studying led to excellent examination results.",
            f"His _____ work ethic impressed all his teachers greatly.",
        ])
    elif "state of disorder" in meaning_lower:
        sentences.extend([
            f"The classroom was in complete _____ after the end-of-term party.",
            f"Her bedroom was in such _____ that she couldn't find anything.",
        ])
    elif "showing good judgement" in meaning_lower or "perceptive" in meaning_lower:
        sentences.extend([
            f"The _____ reader noticed all the hidden clues in the mystery story.",
            f"Her _____ eye for detail helped her spot mistakes others missed.",
            f"Being _____ helped him choose the best books to read.",
        ])
    elif "confused" in meaning_lower or "disconcerted" in meaning_lower:
        sentences.extend([
            f"The sudden announcement left everyone feeling completely _____.",
            f"After the confusing instructions, the students looked rather _____.",
        ])
    elif "untidy" in meaning_lower:
        sentences.extend([
            f"He arrived at school looking _____ after oversleeping and rushing.",
            f"Her _____ appearance suggested she had been playing outside all day.",
        ])
    elif "impartial" in meaning_lower or "without bias" in meaning_lower:
        sentences.extend([
            f"The judge must remain _____ to ensure a fair trial for everyone.",
            f"Her _____ opinion helped resolve the disagreement between friends.",
        ])
    elif "very different" in meaning_lower:
        sentences.extend([
            f"The two artists had _____ styles of painting and drawing.",
            f"Their _____ opinions made it difficult to reach an agreement.",
        ])
    elif "not influenced by emotion" in meaning_lower:
        sentences.extend([
            f"The scientist took a _____ view of the experimental results.",
            f"Her _____ analysis helped solve the problem objectively.",
        ])
    elif "unpleasant" in meaning_lower or "offensive" in meaning_lower:
        sentences.extend([
            f"She found his rude jokes quite _____ and inappropriate.",
            f"The _____ smell coming from the kitchen made everyone feel ill.",
        ])
    elif "respected" in meaning_lower or "eminent" in meaning_lower:
        sentences.extend([
            f"The _____ scientist received many awards for her important research.",
            f"His _____ career in education inspired many young people.",
        ])
    elif "causing worry" in meaning_lower or "upsetting" in meaning_lower:
        sentences.extend([
            f"The _____ news spread quickly through the entire school.",
            f"Watching the _____ documentary made her feel very concerned.",
        ])
    elif "causing worry" in meaning_lower or "unease" in meaning_lower:
        sentences.extend([
            f"The _____ film gave her nightmares for several nights afterwards.",
            f"His _____ behaviour made everyone feel uncomfortable.",
        ])
    elif "developing in different directions" in meaning_lower:
        sentences.extend([
            f"Their _____ opinions made it impossible to reach a compromise.",
            f"The two paths were _____ and led to completely different destinations.",
        ])
    elif "asserting opinions" in meaning_lower or "opinionated" in meaning_lower:
        sentences.extend([
            f"His _____ approach made it difficult to have a proper discussion.",
            f"The _____ teacher refused to consider any alternative viewpoints.",
        ])
    elif "cheerful" in meaning_lower or "full of energy" in meaning_lower:
        sentences.extend([
            f"The _____ puppy bounced around the garden with great enthusiasm.",
            f"Her _____ personality brightened everyone's day at school.",
        ])
    elif "unconventional" in meaning_lower or "slightly strange" in meaning_lower:
        sentences.extend([
            f"The _____ inventor had many unusual and creative ideas.",
            f"Her _____ fashion sense made her stand out from the crowd.",
        ])
    elif "selecting from various sources" in meaning_lower:
        sentences.extend([
            f"Her _____ taste in music included jazz, rock, and classical pieces.",
            f"The _____ collection of books covered many different topics.",
        ])
    elif "expressing ideas clearly" in meaning_lower or "persuasive" in meaning_lower:
        sentences.extend([
            f"The _____ speaker moved the entire audience with her words.",
            f"His _____ writing style made the story very engaging to read.",
        ])
    elif "deeply involved" in meaning_lower:
        sentences.extend([
            f"The two countries became _____ in a long and difficult dispute.",
            f"She didn't want to become _____ in the argument between her friends.",
        ])
    elif "expressing something forcefully" in meaning_lower:
        sentences.extend([
            f"She gave an _____ yes to the exciting invitation to the party.",
            f"His _____ response showed he felt very strongly about the issue.",
        ])
    elif "delightfully charming" in meaning_lower:
        sentences.extend([
            f"The _____ fairy tale captivated all the young listeners.",
            f"Her _____ smile made everyone feel happy and welcome.",
        ])
    elif "lasting for a long time" in meaning_lower:
        sentences.extend([
            f"Their _____ friendship lasted throughout their entire school years.",
            f"The _____ impact of her kindness was remembered by everyone.",
        ])
    elif "fully absorbed" in meaning_lower:
        sentences.extend([
            f"She was so _____ in her book that she missed her bus stop.",
            f"His _____ attention to the game showed how much he enjoyed it.",
        ])
    elif "mysterious" in meaning_lower or "difficult to understand" in meaning_lower:
        sentences.extend([
            f"The _____ smile on her face puzzled everyone who saw it.",
            f"The _____ puzzle took hours to solve completely.",
        ])
    
    # Generic adjective patterns if we need more
    generic_patterns = [
        f"The situation was very _____ and quite concerning to everyone present.",
        f"She showed a _____ attitude that impressed all her teachers greatly.",
        f"His behaviour was quite _____ and rather unexpected for someone his age.",
        f"It was a _____ experience that everyone remembered fondly for years.",
        f"The _____ nature of the event surprised us all greatly indeed.",
        f"They found it _____ and quite interesting to observe carefully.",
        f"Her response was _____ and very thoughtful indeed.",
        f"The _____ quality made it truly special and unique.",
        f"It seemed _____ to all who witnessed the event firsthand.",
        f"The _____ aspect was clear from the very beginning of the story.",
    ]
    
    # Fill remaining slots
    while len(sentences) < 10:
        for pattern in generic_patterns:
            if pattern not in sentences and len(sentences) < 10:
                sentences.append(pattern)
            if len(sentences) >= 10:
                break
    
    return sentences[:10]


def generate_noun_sentences(word: str, meaning: str, example: str, synonym: str, antonym: str) -> List[str]:
    """Generate 10 varied sentences for nouns."""
    sentences = []
    word_lower = word.lower()
    
    # Use example sentence if available
    if example and word.lower() in example.lower():
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate contextually rich noun sentences
    meaning_lower = meaning.lower()
    
    # Context-specific sentences based on meaning
    if "staying the same" in meaning_lower or "uniformity" in meaning_lower:
        sentences.extend([
            f"The _____ in her practice schedule helped her improve steadily.",
            f"Maintaining _____ in your studies leads to better results over time.",
            f"His _____ in following the rules impressed all his teachers.",
        ])
    elif "limit" in meaning_lower or "restriction" in meaning_lower:
        sentences.extend([
            f"Time _____ meant they couldn't finish the entire project.",
            f"The budget _____ prevented them from buying everything they wanted.",
            f"Working within the _____ helped them focus on what was most important.",
        ])
    elif "conclusion reached by reasoning" in meaning_lower:
        sentences.extend([
            f"Her _____ about who had taken the missing book was absolutely correct.",
            f"Through careful observation, he made a logical _____ about the problem.",
            f"The detective's _____ helped solve the mystery completely.",
        ])
    elif "respectful behaviour" in meaning_lower:
        sentences.extend([
            f"The students showed great _____ to their elderly teacher.",
            f"Her _____ towards her grandparents was admirable and kind.",
            f"They listened with _____ to the headteacher's important announcement.",
        ])
    elif "bold resistance" in meaning_lower:
        sentences.extend([
            f"His _____ of the school rules resulted in a serious detention.",
            f"The student's _____ showed she wasn't afraid to stand up for herself.",
            f"Her act of _____ surprised everyone who knew her quiet nature.",
        ])
    elif "being moved to a lower position" in meaning_lower:
        sentences.extend([
            f"His _____ from team captain came as a complete shock to everyone.",
            f"The _____ was unexpected and disappointed many of his supporters.",
        ])
    elif "mocking treatment" in meaning_lower or "scorn" in meaning_lower:
        sentences.extend([
            f"His suggestion was met with _____ from the rest of the group.",
            f"The _____ hurt her feelings and made her feel embarrassed.",
        ])
    elif "difference between things" in meaning_lower:
        sentences.extend([
            f"There was a clear _____ between the two different reports.",
            f"The _____ in their accounts made the teacher suspicious.",
        ])
    elif "length of time" in meaning_lower:
        sentences.extend([
            f"The _____ of the school play was exactly two hours long.",
            f"During the _____ of the lesson, they covered three important topics.",
        ])
    elif "outpouring of emotion" in meaning_lower:
        sentences.extend([
            f"His _____ of gratitude embarrassed the modest helper greatly.",
            f"The _____ of joy from the crowd was overwhelming and exciting.",
        ])
    elif "ability to speak well" in meaning_lower:
        sentences.extend([
            f"Her _____ impressed everyone at the school debate competition.",
            f"The speaker's _____ moved the entire audience to tears.",
        ])
    elif "people who criticise" in meaning_lower:
        sentences.extend([
            f"Despite his _____, the singer remained popular and successful.",
            f"The author ignored her _____ and continued writing her stories.",
        ])
    elif "something that discourages" in meaning_lower:
        sentences.extend([
            f"The high fence acted as a strong _____ to potential intruders.",
            f"The strict rules served as a _____ to misbehaviour in class.",
        ])
    
    # Generic noun patterns
    generic_patterns = [
        f"The _____ was clear to everyone present at the important meeting.",
        f"She understood the _____ of the situation immediately and completely.",
        f"His _____ surprised those around him greatly and unexpectedly.",
        f"The _____ became evident very quickly to all careful observers.",
        f"Everyone noticed the _____ in the way he spoke and behaved.",
        f"The _____ provided important context for understanding the story.",
        f"Her _____ was obvious from her actions and words.",
        f"The _____ helped explain what had happened during the incident.",
        f"People discussed the _____ at length during their conversation.",
        f"The _____ was the key to understanding everything that occurred.",
        f"Everyone was aware of the _____ in the room during the meeting.",
        f"The _____ became the main focus of their detailed discussion.",
        f"She explained the _____ to everyone clearly and thoroughly.",
        f"The _____ revealed important information about the situation.",
        f"His understanding of the _____ was impressive and accurate.",
    ]
    
    # Fill remaining slots
    while len(sentences) < 10:
        for pattern in generic_patterns:
            if pattern not in sentences and len(sentences) < 10:
                sentences.append(pattern)
            if len(sentences) >= 10:
                break
    
    return sentences[:10]


def generate_sentences_for_word(word: str, meaning: str, example: str, synonym: str, antonym: str) -> List[str]:
    """Generate 10 quiz sentences for a word based on its part of speech."""
    pos = determine_part_of_speech(word, meaning)
    
    if pos == "verb":
        return generate_verb_sentences(word, meaning, example, synonym, antonym)
    elif pos == "adjective":
        return generate_adjective_sentences(word, meaning, example, synonym, antonym)
    else:
        return generate_noun_sentences(word, meaning, example, synonym, antonym)


def main():
    """Main function to generate quiz sentences."""
    print("=" * 70)
    print("GENERATE QUIZ SENTENCES FOR LEVEL 3 BATCH 2")
    print("=" * 70)
    print()
    
    # Setup paths
    base_dir = Path(__file__).parent.parent
    input_file = base_dir / 'data' / 'level3_batch2.txt'
    output_file = base_dir / 'data' / 'level3_batch2.csv'
    
    if not input_file.exists():
        print(f"❌ Error: Input file not found: {input_file}")
        return
    
    print(f"📖 Reading words from: {input_file}")
    
    # Read words
    words_data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            word, meaning, example, synonym, antonym = parse_word_line(line)
            if word:
                words_data.append((word, meaning, example, synonym, antonym))
            else:
                print(f"⚠️  Warning: Could not parse line {line_num}: {line}")
    
    print(f"✅ Found {len(words_data)} words")
    print()
    
    # Generate sentences
    print("📝 Generating quiz sentences...")
    all_sentences = []
    
    for idx, (word, meaning, example, synonym, antonym) in enumerate(words_data, 1):
        print(f"  [{idx}/{len(words_data)}] Generating sentences for: {word}")
        sentences = generate_sentences_for_word(word, meaning, example, synonym, antonym)
        
        for sentence in sentences:
            all_sentences.append({
                'level': '3',
                'word': word,
                'sentence': sentence
            })
    
    print()
    print(f"✅ Generated {len(all_sentences)} sentences total")
    print()
    
    # Write to CSV
    print(f"💾 Writing to: {output_file}")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['level', 'word', 'sentence'])
        writer.writeheader()
        writer.writerows(all_sentences)
    
    print()
    print("=" * 70)
    print(f"✅ Level 3 Batch 2 complete: {len(all_sentences)} sentences")
    print("=" * 70)


if __name__ == '__main__':
    main()
