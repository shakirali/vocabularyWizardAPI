#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 2 Batch 1 vocabulary.
Creates 10 contextually rich sentences per word with varied structures.
"""

import csv
import re
from pathlib import Path

def create_blank_sentence(sentence: str, word: str) -> str:
    """Convert a sentence with the word into a fill-in-the-blank format."""
    word_patterns = [
        word,
        word.capitalize(),
        word.upper(),
        word + "s",
        word + "ed",
        word + "ing",
        word + "ly",
        word + "ness",
        word + "ful",
        word + "less",
    ]
    
    # Handle words ending in 'e'
    if word.endswith('e'):
        word_patterns.extend([
            word[:-1] + "ed",
            word[:-1] + "ing",
        ])
    
    # Handle doubling consonants
    if len(word) > 2 and word[-1] not in 'aeiou' and word[-2] in 'aeiou':
        word_patterns.extend([
            word + word[-1] + "ed",
            word + word[-1] + "ing",
        ])
    
    # Handle words ending in 'y'
    if word.endswith('y'):
        word_patterns.extend([
            word[:-1] + "ied",
            word[:-1] + "ies",
            word[:-1] + "ier",
            word[:-1] + "iest",
        ])
    
    result = sentence
    for pattern in word_patterns:
        regex = re.compile(re.escape(pattern), re.IGNORECASE)
        result = regex.sub("_____", result)
    
    return result

def generate_quiz_sentences(word: str, meaning: str, example: str, synonym: str, antonym: str) -> list:
    """
    Generate 10 high-quality quiz sentences for a word.
    Uses varied structures and strong contextual clues.
    """
    sentences = []
    word_lower = word.lower()
    meaning_lower = meaning.lower()
    
    # Determine part of speech
    is_verb = meaning_lower.startswith("to ")
    # Special case: "cherished" is a verb based on example sentence
    if word_lower == "cherished":
        is_verb = True
        is_adjective = False
    else:
        is_adjective = any(marker in meaning_lower for marker in [
            "having", "showing", "full of", "characterised by", "characterized by",
            "very", "extremely", "quite", "rather", "causing", "deserving", 
            "embarrassed", "ashamed", "attractive", "tempting", "difficult", 
            "bad", "poor", "sharp", "critical", "refusing", "eager", "confused",
            "puzzled", "threatening", "pleasant", "likeable", "loved", "valued",
            "mild", "funny", "amusing", "involved", "skilled", "simple", "busy",
            "clumsy", "confused", "unfairly", "openly", "surrounded", "joined",
            "connected", "complete", "total"
        ])
    is_noun = not is_verb and not is_adjective
    
    # 1. Use the example sentence (convert to blank format)
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate additional sentences based on part of speech and meaning
    if is_verb:
        # Verb sentences with varied structures
        verb_sentences = [
            f"They had to _____ when the situation became dangerous.",
            f"She decided to _____ after realising it was the best choice.",
            f"He refused to _____ even when everyone else suggested it.",
            f"The team worked together to _____ the difficult challenge.",
            f"Nobody wanted to _____ in such circumstances.",
            f"She managed to _____ despite facing many obstacles.",
            f"They were forced to _____ when they had no other option.",
            f"He learned to _____ after many years of practice.",
            f"We should _____ before it's too late.",
            f"The captain ordered the crew to _____ immediately.",
        ]
        
        # Customize based on word meaning
        if "leave" in meaning_lower or "give up" in meaning_lower:
            verb_sentences = [
                f"The sailors had to _____ the sinking ship before it went under.",
                f"They decided to _____ their plan when it became impossible.",
                f"She had to _____ her hopes of winning when she fell behind.",
                f"He refused to _____ his dream despite the setbacks.",
                f"The explorers were forced to _____ their camp during the storm.",
                f"They chose to _____ the old car and buy a new one.",
                f"She couldn't bear to _____ her pet when moving house.",
                f"The team had to _____ the match due to bad weather.",
                f"He was told to _____ his bad habits for better health.",
                f"They were advised to _____ the dangerous path.",
            ]
        elif "make familiar" in meaning_lower or "familiarise" in meaning_lower:
            verb_sentences = [
                f"It took time to _____ herself to the new school routine.",
                f"He needed to _____ himself with the new computer system.",
                f"She tried to _____ her dog to the sound of fireworks.",
                f"They worked hard to _____ themselves to the cold weather.",
                f"The teacher helped students _____ themselves with the rules.",
                f"He gradually began to _____ himself to waking up early.",
                f"She found it difficult to _____ herself to the new schedule.",
                f"They needed to _____ themselves to working as a team.",
                f"He managed to _____ himself to eating healthier foods.",
                f"She had to _____ herself to speaking in front of the class.",
            ]
        elif "make less severe" in meaning_lower or "ease" in meaning_lower:
            verb_sentences = [
                f"The medicine helped to _____ her headache.",
                f"He tried to _____ his friend's worries about the test.",
                f"The cool breeze helped to _____ the heat of the day.",
                f"She used ice to _____ the swelling on her ankle.",
                f"The teacher tried to _____ the students' fears about the exam.",
                f"He hoped the explanation would _____ their confusion.",
                f"The music helped to _____ her stress after a long day.",
                f"They worked to _____ the traffic problems in the area.",
                f"The apology helped to _____ the tension between them.",
                f"She tried to _____ her brother's disappointment.",
            ]
        elif "make larger" in meaning_lower or "increase" in meaning_lower:
            verb_sentences = [
                f"She decided to _____ her pocket money by doing extra chores.",
                f"He tried to _____ his collection by buying more stamps.",
                f"The company planned to _____ its workforce next year.",
                f"They wanted to _____ the size of their garden.",
                f"She hoped to _____ her savings by working part-time.",
                f"He tried to _____ his knowledge by reading more books.",
                f"The school decided to _____ the number of computers.",
                f"They planned to _____ their holiday fund with extra jobs.",
                f"She wanted to _____ her vocabulary by learning new words.",
                f"He tried to _____ his confidence by practising daily.",
            ]
        elif "gather" in meaning_lower or "put together" in meaning_lower:
            verb_sentences = [
                f"The students began to _____ in the school hall.",
                f"She helped to _____ the pieces of the jigsaw puzzle.",
                f"They needed to _____ all the equipment before starting.",
                f"He watched the crowd _____ in the town square.",
                f"The team worked together to _____ the model aeroplane.",
                f"She tried to _____ her thoughts before speaking.",
                f"They began to _____ the ingredients for the cake.",
                f"He helped to _____ the furniture for the party.",
                f"The children were asked to _____ in a circle.",
                f"She needed to _____ her courage before the performance.",
            ]
        elif "agree" in meaning_lower:
            verb_sentences = [
                f"After much discussion everyone _____ to the new plan.",
                f"She finally _____ to help with the school project.",
                f"He reluctantly _____ to the terms of the agreement.",
                f"They all _____ to meet at the park on Saturday.",
                f"The committee _____ to the proposal unanimously.",
                f"She quickly _____ to the idea of going to the cinema.",
                f"He had to _____ to the rules before joining the club.",
                f"They _____ to work together on the science project.",
                f"She _____ to take part in the school play.",
                f"He finally _____ to let his sister borrow his bike.",
            ]
        elif "confuse" in meaning_lower:
            verb_sentences = [
                f"The complicated instructions _____ everyone in the class.",
                f"The strange map began to _____ the explorers.",
                f"His confusing explanation only served to _____ them more.",
                f"The puzzle's difficulty started to _____ the children.",
                f"The foreign language signs began to _____ the tourists.",
                f"Her contradictory statements managed to _____ everyone.",
                f"The complex rules of the game began to _____ the players.",
                f"The sudden change of plans started to _____ the team.",
                f"The difficult maths problem began to _____ the students.",
                f"The unclear directions served to _____ the visitors.",
            ]
        elif "criticise" in meaning_lower:
            verb_sentences = [
                f"The committee voted to _____ the member for his behaviour.",
                f"The headteacher had to _____ the students for their lateness.",
                f"They decided to _____ the team's poor performance.",
                f"The newspaper article began to _____ the council's decision.",
                f"She felt it necessary to _____ his careless attitude.",
                f"The teacher had to _____ the class for not doing homework.",
                f"They voted to _____ the proposal for being too expensive.",
                f"The review began to _____ the film for its poor plot.",
                f"He felt compelled to _____ the unfair treatment.",
                f"The report decided to _____ the company's policies.",
            ]
        elif "leave in will" in meaning_lower or "bequeath" in word_lower:
            verb_sentences = [
                f"He decided to _____ his book collection to the library.",
                f"She planned to _____ her jewellery to her granddaughter.",
                f"They wanted to _____ their house to their children.",
                f"He chose to _____ his paintings to the art gallery.",
                f"She decided to _____ her savings to charity.",
                f"They planned to _____ their garden to the local community.",
                f"He wanted to _____ his stamp collection to the museum.",
                f"She chose to _____ her recipes to her daughter.",
                f"They decided to _____ their land to the nature trust.",
                f"He planned to _____ his tools to his grandson.",
            ]
        elif "wave" in meaning_lower or "threat" in meaning_lower:
            verb_sentences = [
                f"The knight _____ his sword at the approaching enemy.",
                f"She watched him _____ the flag to signal the start.",
                f"He began to _____ his stick menacingly at the dog.",
                f"The pirate would _____ his cutlass before attacking.",
                f"She saw him _____ the torch to get their attention.",
                f"He started to _____ his weapon in a threatening manner.",
                f"The guard began to _____ his baton at the intruders.",
                f"She watched him _____ the banner proudly in the wind.",
                f"He would _____ his fist when he was angry.",
                f"The warrior began to _____ his spear at the enemy.",
            ]
        elif "loved" in meaning_lower and "valued" in meaning_lower and "cherished" in word_lower:
            verb_sentences = [
                f"She _____ the photo of her grandmother.",
                f"He _____ his grandfather's old watch.",
                f"They _____ the memories of their childhood.",
                f"She _____ the friendship they had built together.",
                f"He _____ the time spent with his family.",
                f"She _____ the handmade gift from her friend.",
                f"They _____ the traditions passed down through generations.",
                f"He _____ the advice his teacher had given him.",
                f"She _____ the moments they shared together.",
                f"He _____ the opportunity to learn new things.",
            ]
        
        # Add unique sentences up to 10
        for sent in verb_sentences:
            if len(sentences) < 10:
                blank_sent = create_blank_sentence(sent, word)
                if blank_sent not in sentences:
                    sentences.append(blank_sent)
    
    elif is_adjective:
        # Default adjective sentences with varied structures
        adj_sentences = [
            f"She felt _____ when she realised her mistake.",
            f"The _____ situation made everyone uncomfortable.",
            f"His _____ attitude surprised all his friends.",
            f"The _____ weather made it perfect for a picnic.",
            f"Her _____ response showed her true feelings.",
            f"The _____ performance impressed the audience.",
            f"His _____ behaviour worried his parents.",
            f"The _____ smell filled the entire room.",
            f"She looked _____ after hearing the news.",
            f"The _____ garden attracted many visitors.",
        ]
        
        # Track if we've customized the sentences
        customized = False
        
        # Customize based on word meaning
        if "embarrassed" in meaning_lower or "ashamed" in meaning_lower:
            customized = True
            adj_sentences = [
                f"She felt _____ when she realised she had forgotten her friend's birthday.",
                f"He looked _____ after tripping over in front of everyone.",
                f"The _____ expression on her face showed her embarrassment.",
                f"She was _____ when she realised she had the wrong answer.",
                f"His _____ reaction made everyone notice his mistake.",
                f"She felt _____ about forgetting to bring her homework.",
                f"The _____ look on his face revealed his embarrassment.",
                f"He was _____ when he realised he had mispronounced the word.",
                f"Her _____ expression showed she was ashamed of her actions.",
                f"They felt _____ after being caught breaking the rules.",
            ]
        elif "attractive" in meaning_lower or "tempting" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The _____ smell of fresh bread filled the bakery.",
                f"She found the _____ display in the shop window irresistible.",
                f"The _____ colours of the sunset amazed everyone.",
                f"He was drawn to the _____ offer of free sweets.",
                f"The _____ melody made everyone want to dance.",
                f"She couldn't resist the _____ smell of chocolate cake.",
                f"The _____ garden was full of beautiful flowers.",
                f"He found the _____ invitation too tempting to refuse.",
                f"The _____ view from the hilltop was breathtaking.",
                f"She was captivated by the _____ sound of the music.",
            ]
        elif "complete" in meaning_lower or "total" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The judge demanded _____ silence in the courtroom.",
                f"She showed _____ dedication to her studies.",
                f"He had _____ confidence in his team's ability.",
                f"The _____ darkness made it impossible to see.",
                f"Her _____ honesty impressed everyone who knew her.",
                f"They needed _____ cooperation to complete the project.",
                f"The _____ truth was finally revealed.",
                f"He showed _____ commitment to helping others.",
                f"The _____ silence in the library was unusual.",
                f"She demonstrated _____ mastery of the subject.",
            ]
        elif "deeply interested" in meaning_lower or "engaged" in meaning_lower or "absorbed" in word_lower:
            customized = True
            adj_sentences = [
                f"She was so _____ in her book that she missed her bus stop.",
                f"He became completely _____ in the fascinating documentary.",
                f"The _____ student forgot to eat lunch while studying.",
                f"She was _____ in solving the difficult puzzle.",
                f"He was so _____ in the game that he didn't hear his name called.",
                f"The _____ reader didn't notice the time passing.",
                f"She became _____ in learning about ancient history.",
                f"He was completely _____ in watching the football match.",
                f"The _____ artist worked on her painting for hours.",
                f"She was so _____ in the story that she read all night.",
            ]
        elif "difficult to understand" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The professor's _____ lecture confused most of the students.",
                f"She found the _____ text impossible to comprehend.",
                f"The _____ explanation only made things more confusing.",
                f"He struggled with the _____ mathematical concepts.",
                f"The _____ language in the book was hard to follow.",
                f"She was puzzled by the _____ instructions.",
                f"The _____ theory was beyond most people's understanding.",
                f"He found the _____ philosophy too complex to grasp.",
                f"The _____ scientific paper was difficult to read.",
                f"She was confused by the _____ technical terms.",
            ]
        elif "extremely bad" in meaning_lower or "poor" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The team's _____ performance led to their defeat.",
                f"She received _____ marks on her test.",
                f"The _____ weather ruined their picnic plans.",
                f"His _____ behaviour resulted in detention.",
                f"The _____ conditions made it impossible to play outside.",
                f"She was disappointed by the _____ quality of the work.",
                f"The _____ service at the restaurant upset the customers.",
                f"His _____ attitude towards homework worried his teacher.",
                f"The _____ state of the building needed urgent repair.",
                f"She was shocked by the _____ state of the garden.",
            ]
        elif "sharp" in meaning_lower or "critical" in meaning_lower:
            customized = True
            adj_sentences = [
                f"His _____ remarks hurt the feelings of his teammates.",
                f"She was known for her _____ sense of humour.",
                f"The _____ comment made everyone uncomfortable.",
                f"His _____ wit often got him into trouble.",
                f"The _____ tone of her voice showed her anger.",
                f"He was famous for his _____ observations.",
                f"The _____ review criticised the film harshly.",
                f"Her _____ words stung more than she intended.",
                f"He had a reputation for _____ comments.",
                f"The _____ criticism upset the young performer.",
            ]
        elif "refusing to change" in meaning_lower:
            customized = True
            adj_sentences = [
                f"He was _____ that he would finish the race despite his injury.",
                f"She remained _____ about her decision to leave.",
                f"His _____ refusal surprised everyone.",
                f"She was _____ that she was right about the answer.",
                f"His _____ insistence on the point annoyed others.",
                f"She stayed _____ despite all the arguments against her.",
                f"His _____ determination impressed his coach.",
                f"She was _____ that she would not give up.",
                f"His _____ stance on the issue was well-known.",
                f"She remained _____ about her choice of university.",
            ]
        elif "eager to fight" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The _____ knight was always ready for battle.",
                f"His _____ nature made him unpopular with others.",
                f"The _____ warrior charged into the fight.",
                f"His _____ attitude caused many arguments.",
                f"The _____ soldier was always looking for conflict.",
                f"His _____ behaviour worried his parents.",
                f"The _____ general was known for starting wars.",
                f"His _____ response to criticism was aggressive.",
                f"The _____ boxer was always ready to fight.",
                f"His _____ personality made him difficult to befriend.",
            ]
        elif "confused" in meaning_lower or "puzzled" in meaning_lower:
            customized = True
            adj_sentences = [
                f"He looked _____ when asked to explain the rules of the game.",
                f"Her _____ expression showed she didn't understand.",
                f"The _____ student raised his hand to ask a question.",
                f"She appeared _____ by the complicated instructions.",
                f"His _____ face revealed his confusion.",
                f"The _____ look on her face was obvious to everyone.",
                f"He seemed _____ by the sudden change of plans.",
                f"Her _____ reaction showed she was lost.",
                f"The _____ expression on his face was comical.",
                f"She looked _____ when she couldn't find her way.",
            ]
        elif "unfairly favouring" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The _____ referee made several unfair decisions.",
                f"Her _____ opinion showed she wasn't being fair.",
                f"The _____ judge favoured one team over the other.",
                f"His _____ comments upset the losing team.",
                f"The _____ report didn't tell the whole story.",
                f"Her _____ attitude made others feel excluded.",
                f"The _____ treatment was obvious to everyone.",
                f"His _____ views were well-known.",
                f"The _____ article only showed one side of the story.",
                f"Her _____ behaviour caused arguments.",
            ]
        elif "extremely happy" in meaning_lower:
            customized = True
            adj_sentences = [
                f"They spent a _____ afternoon playing in the sunshine.",
                f"Her _____ smile showed how happy she was.",
                f"The _____ expression on his face was wonderful to see.",
                f"She felt _____ after receiving the good news.",
                f"The _____ day was perfect in every way.",
                f"Her _____ laughter filled the room with joy.",
                f"The _____ moment would stay with them forever.",
                f"She was in a _____ mood after winning the competition.",
                f"The _____ atmosphere made everyone feel happy.",
                f"Her _____ state of mind was obvious to all.",
            ]
        elif "bragging" in meaning_lower:
            customized = True
            adj_sentences = [
                f"Nobody liked his _____ comments about his achievements.",
                f"Her _____ attitude made others feel uncomfortable.",
                f"His _____ nature made him unpopular.",
                f"The _____ student couldn't stop talking about his grades.",
                f"Her _____ behaviour annoyed her classmates.",
                f"His _____ remarks were met with eye rolls.",
                f"The _____ athlete was always talking about his wins.",
                f"Her _____ personality made others avoid her.",
                f"His _____ comments showed his arrogance.",
                f"The _____ child couldn't stop boasting.",
            ]
        elif "thinking deeply" in meaning_lower or "worrying" in meaning_lower:
            customized = True
            adj_sentences = [
                f"He sat in _____ silence after receiving the bad news.",
                f"Her _____ expression showed she was worried.",
                f"The _____ look on his face revealed his concerns.",
                f"She remained _____ for hours after the argument.",
                f"His _____ mood worried his friends.",
                f"The _____ atmosphere in the room was tense.",
                f"She looked _____ as she considered the problem.",
                f"His _____ silence made everyone uncomfortable.",
                f"The _____ expression showed her deep thoughts.",
                f"He was in a _____ mood after the disappointing result.",
            ]
        elif "clumsy" in meaning_lower or "confused" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The _____ waiter dropped three plates during dinner.",
                f"His _____ attempts at juggling made everyone laugh.",
                f"The _____ assistant kept making mistakes.",
                f"Her _____ movements caused several accidents.",
                f"The _____ character in the play was very funny.",
                f"His _____ behaviour was endearing but frustrating.",
                f"The _____ worker struggled with the simple task.",
                f"Her _____ approach to the problem didn't help.",
                f"The _____ student kept dropping his books.",
                f"His _____ manner made him seem friendly but unreliable.",
            ]
        elif "busy" in meaning_lower or "activity" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The _____ market was full of people buying and selling.",
                f"Her _____ schedule left no time for relaxation.",
                f"The _____ street was crowded with shoppers.",
                f"His _____ day included many different activities.",
                f"The _____ town centre was always full of life.",
                f"Her _____ lifestyle kept her constantly occupied.",
                f"The _____ kitchen was full of cooks preparing meals.",
                f"His _____ routine started early each morning.",
                f"The _____ playground was full of playing children.",
                f"Her _____ household was never quiet.",
            ]
        elif "pleasant" in meaning_lower or "likeable" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The _____ village attracted many tourists.",
                f"Her _____ personality made her popular.",
                f"The _____ smile on his face was welcoming.",
                f"Her _____ manner put everyone at ease.",
                f"The _____ atmosphere made the party enjoyable.",
                f"His _____ behaviour made him well-liked.",
                f"The _____ garden was a pleasure to visit.",
                f"Her _____ voice was pleasant to listen to.",
                f"The _____ setting was perfect for a picnic.",
                f"His _____ character made him a good friend.",
            ]
        elif "loved" in meaning_lower or "valued" in meaning_lower:
            customized = True
            # Note: "cherished" is a verb, but this pattern handles past participle adjectives
            adj_sentences = [
                f"His _____ possession was his grandfather's watch.",
                f"His _____ possession was his grandfather's watch.",
                f"The _____ memory would stay with her forever.",
                f"She kept the _____ letter in a special box.",
                f"His _____ toy had been with him since childhood.",
                f"The _____ moment was captured in a photograph.",
                f"She held the _____ gift close to her heart.",
                f"His _____ book was falling apart from use.",
                f"The _____ tradition was passed down through generations.",
                f"She treasured the _____ friendship above all others.",
            ]
        elif "mild" in meaning_lower or "pleasant weather" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The _____ weather made it perfect for a picnic.",
                f"Her _____ nature made her easy to work with.",
                f"The _____ breeze was refreshing on the hot day.",
                f"His _____ response showed his gentle character.",
                f"The _____ climate was ideal for growing flowers.",
                f"Her _____ manner calmed everyone down.",
                f"The _____ conditions were perfect for sailing.",
                f"His _____ temperament made him popular.",
                f"The _____ temperature was comfortable for everyone.",
                f"Her _____ attitude made the situation easier.",
            ]
        elif "funny" in meaning_lower or "amusing" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The clown's _____ performance made everyone laugh.",
                f"His _____ jokes kept the audience entertained.",
                f"The _____ situation made everyone smile.",
                f"Her _____ antics were hilarious to watch.",
                f"The _____ play had the whole audience laughing.",
                f"His _____ expression was very entertaining.",
                f"The _____ story made everyone chuckle.",
                f"Her _____ behaviour lightened the mood.",
                f"The _____ film was perfect for a family evening.",
                f"His _____ remarks made the meeting more enjoyable.",
            ]
        elif "suitable" in meaning_lower or "fitting" in meaning_lower:
            customized = True
            adj_sentences = [
                f"Her new hairstyle was very _____ and suited her well.",
                f"The _____ dress was perfect for the occasion.",
                f"His _____ behaviour showed good manners.",
                f"The _____ choice of words impressed everyone.",
                f"Her _____ response was exactly what was needed.",
                f"The _____ decoration matched the room perfectly.",
                f"His _____ attitude was appropriate for the situation.",
                f"The _____ gift was thoughtful and appreciated.",
                f"Her _____ manner was perfect for the job.",
                f"The _____ solution solved the problem elegantly.",
            ]
        elif "threatening" in meaning_lower or "harm" in meaning_lower:
            customized = True
            adj_sentences = [
                f"The witch gave a _____ look to the travellers passing by.",
                f"His _____ expression frightened the children.",
                f"The _____ storm clouds gathered overhead.",
                f"Her _____ tone made everyone nervous.",
                f"The _____ shadow loomed in the darkness.",
                f"His _____ glare stopped them in their tracks.",
                f"The _____ atmosphere made everyone uneasy.",
                f"Her _____ words were meant to intimidate.",
                f"The _____ figure appeared suddenly.",
                f"His _____ presence made everyone uncomfortable.",
            ]
        elif "joined" in meaning_lower or "connected" in meaning_lower or "attached" in word_lower:
            customized = True
            adj_sentences = [
                f"She was very _____ to her old teddy bear.",
                f"He felt deeply _____ to his hometown.",
                f"The _____ document contained important information.",
                f"Her _____ relationship with her grandmother was special.",
                f"The _____ file was too large to email.",
                f"He was emotionally _____ to the old house.",
                f"The _____ photo showed her family.",
                f"She remained _____ to her childhood friends.",
                f"The _____ note explained everything clearly.",
                f"He was closely _____ to the project.",
            ]
        
        # Add unique sentences up to 10
        for sent in adj_sentences:
            if len(sentences) < 10:
                blank_sent = create_blank_sentence(sent, word)
                if blank_sent not in sentences:
                    sentences.append(blank_sent)
    
    else:  # is_noun
        # Noun sentences with varied structures
        noun_sentences = [
            f"Her _____ from school was noticed by all her teachers.",
            f"The _____ was clear from the context.",
            f"She showed great _____ in the situation.",
            f"The _____ became evident as the story unfolded.",
            f"His _____ surprised everyone around him.",
            f"The _____ was obvious to all who watched.",
            f"The situation required _____ from everyone involved.",
            f"His _____ made a significant difference.",
            f"The _____ was apparent in their actions.",
            f"She expressed _____ in her response.",
        ]
        
        # Customize based on word meaning
        if "away" in meaning_lower or "not present" in meaning_lower:
            noun_sentences = [
                f"Her _____ from school was noticed by all her teachers.",
                f"His _____ from the meeting was unexpected.",
                f"The _____ of any explanation made things confusing.",
                f"Her _____ from the team was felt by everyone.",
                f"The _____ of evidence made the case difficult.",
                f"His _____ from the party was disappointing.",
                f"The _____ of noise made the room peaceful.",
                f"Her _____ from the list was a mistake.",
                f"The _____ of clouds meant a sunny day.",
                f"His _____ from the group was noticeable.",
            ]
        elif "idea" in meaning_lower or "concept" in meaning_lower or "abstract" in word_lower:
            noun_sentences = [
                f"Love and happiness are _____ concepts that are hard to define.",
                f"The _____ of freedom is important to everyone.",
                f"She struggled to understand the _____ of infinity.",
                f"The _____ of justice varies between cultures.",
                f"He found the _____ of time travel fascinating.",
                f"The _____ of friendship means different things to different people.",
                f"She explored the _____ of courage in her essay.",
                f"The _____ of beauty is subjective.",
                f"He discussed the _____ of responsibility with his teacher.",
                f"The _____ of truth is complex and philosophical.",
            ]
        elif "award" in meaning_lower or "praise" in meaning_lower:
            noun_sentences = [
                f"Winning the prize was the highest _____ of her career.",
                f"The _____ for bravery was presented at the ceremony.",
                f"She received the _____ for outstanding achievement.",
                f"The _____ recognised his years of service.",
                f"He was honoured to receive such a prestigious _____.",
                f"The _____ was displayed proudly in the school hall.",
                f"She felt proud to earn the _____ for excellence.",
                f"The _____ celebrated her contribution to the community.",
                f"He treasured the _____ he received for his work.",
                f"The _____ was the highlight of the awards ceremony.",
            ]
        elif "abbreviation" in meaning_lower or "first letters" in meaning_lower:
            noun_sentences = [
                f"NASA is an _____ for National Aeronautics and Space Administration.",
                f"She explained that BBC is an _____ for British Broadcasting Corporation.",
                f"The _____ UN stands for United Nations.",
                f"He learned that RSVP is an _____ from French.",
                f"The _____ FAQ means Frequently Asked Questions.",
                f"She recognised the _____ ASAP meant as soon as possible.",
                f"The _____ DIY stands for do it yourself.",
                f"He discovered that LOL is an _____ for laugh out loud.",
                f"The _____ UK is short for United Kingdom.",
                f"She explained that the _____ NHS stands for National Health Service.",
            ]
        elif "illness" in meaning_lower or "health problem" in meaning_lower:
            noun_sentences = [
                f"The herbal tea was said to cure many common _____.",
                f"She suffered from a minor _____ that kept her home.",
                f"The _____ prevented him from playing football.",
                f"Her grandmother's _____ worried the whole family.",
                f"The doctor diagnosed the _____ quickly.",
                f"He recovered from the _____ after a week of rest.",
                f"The _____ was not serious but needed treatment.",
                f"She took medicine to help with her _____.",
                f"The _____ spread quickly through the school.",
                f"He hoped the _____ would clear up soon.",
            ]
        elif "attacker" in meaning_lower or "starts conflict" in meaning_lower:
            noun_sentences = [
                f"The _____ was quickly stopped by the playground supervisor.",
                f"The _____ started the fight without provocation.",
                f"She identified the _____ from the security footage.",
                f"The _____ was known for causing trouble.",
                f"He was labelled the _____ in the dispute.",
                f"The _____ showed no remorse for his actions.",
                f"She tried to avoid the _____ on the playground.",
                f"The _____ was removed from the game.",
                f"He was clearly the _____ in the argument.",
                f"The _____ was punished for starting the conflict.",
            ]
        elif "barrier" in meaning_lower or "block" in meaning_lower:
            noun_sentences = [
                f"The protesters built a _____ across the street.",
                f"The _____ prevented cars from entering the area.",
                f"She saw the _____ blocking the road ahead.",
                f"The _____ was made from wooden planks and barrels.",
                f"He helped to move the _____ out of the way.",
                f"The _____ protected the workers from traffic.",
                f"She noticed the _____ had been damaged.",
                f"The _____ was set up for the demonstration.",
                f"He climbed over the _____ to get through.",
                f"The _____ was removed once the event ended.",
            ]
        elif "support" in meaning_lower or "strengthen" in meaning_lower:
            noun_sentences = [
                f"The flying _____ supported the ancient cathedral walls.",
                f"The stone _____ held up the heavy archway.",
                f"She noticed the _____ had been added to strengthen the building.",
                f"The architectural _____ was both functional and beautiful.",
                f"He studied how the _____ distributed the weight.",
                f"The _____ prevented the wall from collapsing.",
                f"She admired the Gothic _____ on the old church.",
                f"The _____ was essential for the building's stability.",
                f"He learned about the _____ in his history lesson.",
                f"The _____ was a masterpiece of medieval engineering.",
            ]
        elif "seeking job" in meaning_lower or "position" in meaning_lower:
            noun_sentences = [
                f"Three _____ applied for the teaching position.",
                f"The _____ prepared carefully for the interview.",
                f"She was the strongest _____ for the role.",
                f"The _____ submitted their applications last week.",
                f"He was selected as the best _____ for the job.",
                f"The _____ had impressive qualifications.",
                f"She interviewed each _____ individually.",
                f"The _____ waited nervously for the results.",
                f"He was chosen from among many _____.",
                f"The _____ demonstrated their skills during the interview.",
            ]
        elif "material" in meaning_lower or "seal" in meaning_lower:
            noun_sentences = [
                f"The _____ around the window stopped draughts coming in.",
                f"She applied the _____ to fill the gaps.",
                f"The _____ prevented water from leaking in.",
                f"He used the _____ to seal the bathroom tiles.",
                f"The _____ was white and flexible.",
                f"She needed more _____ to finish the job.",
                f"The _____ dried quickly after application.",
                f"He checked the _____ for any cracks.",
                f"The _____ kept the room warm and dry.",
                f"She replaced the old _____ with new material.",
            ]
        elif "record" in meaning_lower or "events" in meaning_lower:
            noun_sentences = [
                f"The book was a _____ of the king's reign.",
                f"She kept a _____ of all her daily activities.",
                f"The _____ detailed the events of the war.",
                f"He wrote a _____ of his travels abroad.",
                f"The historical _____ provided valuable information.",
                f"She read the _____ of the ancient civilisation.",
                f"The _____ recorded every important event.",
                f"He studied the _____ to understand the past.",
                f"The _____ was written by a famous historian.",
                f"She found the _____ fascinating and informative.",
            ]
        elif "quality" in meaning_lower or "feature" in meaning_lower:
            noun_sentences = [
                f"Kindness is an _____ that everyone admires.",
                f"Her greatest _____ was her patience.",
                f"The _____ of honesty is important in friendship.",
                f"He possessed the _____ of leadership.",
                f"The positive _____ made her popular.",
                f"She valued the _____ of loyalty above all.",
                f"The _____ of courage helped him succeed.",
                f"His best _____ was his sense of humour.",
                f"The _____ of determination drove her forward.",
                f"She admired the _____ of generosity in others.",
            ]
        elif "story" in meaning_lower or "amusing" in meaning_lower:
            noun_sentences = [
                f"He entertained the guests with an _____ about his travels.",
                f"The _____ made everyone laugh.",
                f"She shared an _____ from her childhood.",
                f"The amusing _____ was retold many times.",
                f"He began the _____ with great enthusiasm.",
                f"The _____ illustrated an important point.",
                f"She remembered the _____ fondly.",
                f"The personal _____ was very entertaining.",
                f"He used the _____ to explain his point.",
                f"The _____ added humour to the conversation.",
            ]
        elif "different from normal" in meaning_lower or "irregularity" in meaning_lower:
            noun_sentences = [
                f"The warm winter day was an _____ in the usually cold season.",
                f"The _____ in the test results puzzled the scientists.",
                f"She noticed an _____ in the pattern.",
                f"The _____ was unexpected and unusual.",
                f"He discovered an _____ in the data.",
                f"The _____ stood out from the rest.",
                f"She investigated the _____ carefully.",
                f"The _____ was difficult to explain.",
                f"He found the _____ interesting.",
                f"The _____ was the only one of its kind.",
            ]
        elif "medicine" in meaning_lower or "poison" in meaning_lower:
            noun_sentences = [
                f"The doctor gave the patient an _____ for the snake bite.",
                f"She needed an _____ to counteract the poison.",
                f"The _____ worked quickly to neutralise the toxin.",
                f"He searched for an _____ to the problem.",
                f"The _____ saved the patient's life.",
                f"She administered the _____ immediately.",
                f"The _____ was the only cure available.",
                f"He hoped the _____ would work in time.",
                f"The _____ was kept in the hospital emergency room.",
                f"She learned about the _____ in her science lesson.",
            ]
        elif "opposite" in meaning_lower:
            noun_sentences = [
                f"The _____ of 'happy' is 'sad'.",
                f"She learned that 'hot' is the _____ of 'cold'.",
                f"The teacher explained what an _____ was.",
                f"He found the _____ in the dictionary.",
                f"The _____ helped her understand the word better.",
                f"She used the _____ to clarify the meaning.",
                f"The _____ was clearly explained in the lesson.",
                f"He struggled to find the _____ of the word.",
                f"The _____ showed the contrast clearly.",
                f"She memorised the _____ for her vocabulary test.",
            ]
        elif "lack of interest" in meaning_lower or "enthusiasm" in meaning_lower:
            noun_sentences = [
                f"His _____ towards schoolwork worried his parents.",
                f"The student's _____ was obvious to everyone.",
                f"Her _____ about the project was disappointing.",
                f"The _____ of the crowd was noticeable.",
                f"He showed complete _____ towards the subject.",
                f"The _____ made it difficult to motivate the class.",
                f"Her _____ was a cause for concern.",
                f"The _____ towards the event was surprising.",
                f"He displayed _____ about joining the team.",
                f"The _____ affected the whole group's performance.",
            ]
        elif "skilled worker" in meaning_lower or "hand" in meaning_lower:
            noun_sentences = [
                f"The _____ created beautiful pottery by hand.",
                f"She admired the work of the local _____.",
                f"The _____ spent years perfecting his craft.",
                f"He was a master _____ in woodworking.",
                f"The _____ sold her creations at the market.",
                f"She learned from an experienced _____.",
                f"The _____ took pride in his handmade items.",
                f"He visited the _____'s workshop regularly.",
                f"The _____'s skill was evident in every piece.",
                f"She hoped to become a skilled _____ one day.",
            ]
        elif "no government" in meaning_lower:
            noun_sentences = [
                f"The _____ protested against all forms of authority.",
                f"She read about the _____ in her history book.",
                f"The _____ believed in complete freedom.",
                f"He was known as an _____ for his views.",
                f"The _____ rejected all government control.",
                f"She learned about the _____ movement in class.",
                f"The _____'s ideas were controversial.",
                f"He studied the philosophy of the _____.",
                f"The _____ wanted to abolish all rules.",
                f"She found the _____'s beliefs interesting.",
            ]
        elif "rearranging letters" in meaning_lower:
            noun_sentences = [
                f"The word 'listen' is an _____ of 'silent'.",
                f"She enjoyed solving the _____ puzzle.",
                f"The _____ challenged her to rearrange the letters.",
                f"He found the _____ difficult to solve.",
                f"The _____ was a fun word game.",
                f"She created an _____ from her name.",
                f"The _____ required careful letter arrangement.",
                f"He solved the _____ quickly.",
                f"The _____ was part of the crossword puzzle.",
                f"She loved playing the _____ game.",
            ]
        elif "lizard" in meaning_lower or "changes colour" in meaning_lower:
            noun_sentences = [
                f"The _____ changed colour to match the green leaves.",
                f"She watched the _____ blend into its surroundings.",
                f"The _____ is a fascinating reptile.",
                f"He learned that the _____ can change its appearance.",
                f"The _____'s ability to camouflage is amazing.",
                f"She saw the _____ in the zoo's reptile house.",
                f"The _____ adapted to its environment perfectly.",
                f"He studied the _____ in his science class.",
                f"The _____'s colour change was incredible to watch.",
                f"She found the _____ one of the most interesting animals.",
            ]
        elif "pretends to have skills" in meaning_lower or "fraud" in meaning_lower:
            noun_sentences = [
                f"The _____ claimed to be a doctor but had no qualifications.",
                f"She exposed the _____ for what he really was.",
                f"The _____ fooled many people with his lies.",
                f"He was revealed as a _____ when his methods failed.",
                f"The _____'s deception was eventually discovered.",
                f"She warned others about the _____ in town.",
                f"The _____ pretended to have medical knowledge.",
                f"He was nothing more than a clever _____.",
                f"The _____'s false claims were dangerous.",
                f"She saw through the _____'s disguise immediately.",
            ]
        elif "uncivilised" in meaning_lower or "savage" in meaning_lower:
            noun_sentences = [
                f"The _____ warriors invaded the peaceful village.",
                f"She read about the _____ in her history book.",
                f"The _____ tribes were feared by everyone.",
                f"He learned about the _____ in ancient times.",
                f"The _____'s attack was swift and brutal.",
                f"She studied how the _____ lived.",
                f"The _____ were known for their fierce fighting.",
                f"He imagined what life was like for the _____.",
                f"The _____'s customs were very different.",
                f"She found the _____'s history fascinating.",
            ]
        elif "drink" in meaning_lower:
            noun_sentences = [
                f"Tea is the most popular hot _____ in Britain.",
                f"She ordered a cold _____ from the café.",
                f"The _____ was refreshing on the hot day.",
                f"He preferred hot _____ to cold ones.",
                f"The _____ menu offered many choices.",
                f"She enjoyed the fizzy _____ at the party.",
                f"The _____ was served in a tall glass.",
                f"He chose his favourite _____ from the list.",
                f"The _____ was made from fresh fruit.",
                f"She sipped her _____ slowly.",
            ]
        elif "involved in wrongdoing" in meaning_lower:
            noun_sentences = [
                f"He was _____ in the plan to cheat on the test.",
                f"She was found to be _____ in the scheme.",
                f"The _____ student was punished along with the others.",
                f"His _____ role was discovered by the teacher.",
                f"The _____ party shared in the blame.",
                f"She denied being _____ in the wrongdoing.",
                f"His _____ behaviour shocked his friends.",
                f"The _____ individual was held responsible.",
                f"She was accused of being _____ in the plot.",
                f"His _____ actions disappointed everyone.",
            ]
        elif "jumping playfully" in meaning_lower or "frolicking" in meaning_lower:
            noun_sentences = [
                f"The lambs were _____ in the spring meadow.",
                f"She watched the puppies _____ in the garden.",
                f"The children enjoyed _____ in the park.",
                f"He saw the kittens _____ with a ball of wool.",
                f"The _____ of the young animals was joyful.",
                f"She loved watching the foals _____ in the field.",
                f"The _____ made everyone smile.",
                f"He joined in the _____ with his friends.",
                f"The _____ was full of energy and fun.",
                f"She captured the _____ on camera.",
            ]
        elif "moving fast" in meaning_lower or "uncontrolled" in meaning_lower:
            noun_sentences = [
                f"The car came _____ down the hill out of control.",
                f"She watched the ball go _____ across the field.",
                f"The _____ movement was dangerous.",
                f"He saw the bike go _____ down the slope.",
                f"The _____ speed frightened everyone.",
                f"She tried to stop the _____ motion.",
                f"The _____ vehicle was heading for disaster.",
                f"He watched the _____ progress with concern.",
                f"The _____ movement was unstoppable.",
                f"She managed to avoid the _____ object.",
            ]
        
        # Add unique sentences up to 10
        for sent in noun_sentences:
            if len(sentences) < 10:
                blank_sent = create_blank_sentence(sent, word)
                if blank_sent not in sentences:
                    sentences.append(blank_sent)
    
    # Ensure we have exactly 10 sentences with proper part of speech
    while len(sentences) < 10:
        # Generate contextually appropriate sentences based on meaning
        if is_verb:
            # Verb fallback sentences
            verb_fallbacks = [
                f"They needed to _____ to solve the problem.",
                f"She decided to _____ when she realised it was necessary.",
                f"He had to _____ to complete the task.",
                f"They worked together to _____ the challenge.",
                f"She managed to _____ despite the difficulties.",
            ]
            for generic in verb_fallbacks:
                if len(sentences) >= 10:
                    break
                blank_generic = create_blank_sentence(generic, word)
                if blank_generic not in sentences:
                    sentences.append(blank_generic)
        elif is_adjective:
            # Adjective fallback sentences
            adj_fallbacks = [
                f"She felt _____ about the situation.",
                f"His _____ attitude was noticeable to everyone.",
                f"The _____ expression on her face showed her feelings.",
                f"He looked _____ after hearing the news.",
                f"The _____ response surprised everyone.",
            ]
            for generic in adj_fallbacks:
                if len(sentences) >= 10:
                    break
                blank_generic = create_blank_sentence(generic, word)
                if blank_generic not in sentences:
                    sentences.append(blank_generic)
        else:
            # Noun fallback sentences
            noun_fallbacks = [
                f"The _____ was important to understand.",
                f"She studied the _____ carefully.",
                f"The _____ became clear as the story unfolded.",
                f"His _____ made a significant difference.",
                f"The _____ was obvious to everyone.",
            ]
            for generic in noun_fallbacks:
                if len(sentences) >= 10:
                    break
                blank_generic = create_blank_sentence(generic, word)
                if blank_generic not in sentences:
                    sentences.append(blank_generic)
    
    return sentences[:10]  # Return exactly 10

def main():
    """Generate quiz sentences for all words in level2_batch1.txt"""
    input_file = Path(__file__).parent.parent / "data" / "level2_batch1.txt"
    output_file = Path(__file__).parent.parent / "data" / "level2_batch1.csv"
    
    sentences_data = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('|')
            if len(parts) < 3:
                continue
            
            word = parts[0].strip()
            meaning = parts[1].strip()
            example = parts[2].strip() if len(parts) > 2 else ""
            synonym = parts[3].strip() if len(parts) > 3 else ""
            antonym = parts[4].strip() if len(parts) > 4 else ""
            
            # Generate 10 sentences for this word
            quiz_sentences = generate_quiz_sentences(word, meaning, example, synonym, antonym)
            
            # Add each sentence to the output
            for sentence in quiz_sentences:
                sentences_data.append({
                    'level': '2',
                    'word': word.capitalize(),
                    'sentence': sentence
                })
    
    # Write to CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['level', 'word', 'sentence'])
        writer.writeheader()
        writer.writerows(sentences_data)
    
    total_sentences = len(sentences_data)
    print(f"Level 2 Batch 1 complete: {total_sentences} sentences")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    main()
