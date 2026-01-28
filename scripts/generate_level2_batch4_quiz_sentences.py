#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 2 Batch 4 vocabulary.
Creates 10 contextually rich sentences per word with strong clues for 11+ vocabulary.
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
            word_lower + 'er'
        ])
    
    # Replace word forms with blank
    result = sentence
    for pattern in sorted(set(patterns), key=len, reverse=True):
        regex = re.compile(r'\b' + re.escape(pattern) + r'\b', re.IGNORECASE)
        result = regex.sub("_____", result)
    
    return result


def parse_word_line(line: str) -> Tuple[str, str, str, str, str]:
    """Parse a line from the word file: word|meaning|example|synonym|antonym"""
    parts = line.strip().split('|')
    word = parts[0].strip() if len(parts) > 0 else ""
    meaning = parts[1].strip() if len(parts) > 1 else ""
    example = parts[2].strip() if len(parts) > 2 else ""
    synonym = parts[3].strip() if len(parts) > 3 else ""
    antonym = parts[4].strip() if len(parts) > 4 else ""
    return word, meaning, example, synonym, antonym


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
        "very", "extremely", "quite", "rather", "causing", "deserving", "slow to",
        "not", "a", "an"
    ]) and not is_verb
    is_noun = not is_verb and not is_adjective
    
    # 1. Use example sentence if available
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate contextually rich sentences based on word meaning
    # Create custom sentences that demonstrate the specific meaning
    
    # Word-specific sentence generation based on meaning
    if "negate" in word_lower:
        sentences.extend([
            "The new evidence seemed to _____ the previous theory completely.",
            "She tried to _____ the negative effects of the mistake.",
            "His apology could not _____ the hurt he had caused.",
            "The positive results _____ all our previous concerns.",
            "Nothing could _____ the importance of their friendship.",
            "The court ruling would _____ the earlier decision.",
            "He hoped his explanation would _____ their doubts.",
            "The discovery seemed to _____ everything we thought we knew.",
            "Her success helped to _____ the criticism she had received.",
            "The facts would _____ the rumours that were spreading."
        ])
    elif "nemesis" in word_lower:
        sentences.extend([
            "The detective finally caught his _____ after years of pursuit.",
            "She considered maths her greatest _____ at school.",
            "The hero faced his _____ in the final battle.",
            "He had been trying to defeat his _____ for months.",
            "The chess player met his _____ in the championship match.",
            "Her _____ had been causing trouble for years.",
            "The villain was the superhero's greatest _____.",
            "He finally overcame his _____ through hard work.",
            "The two rivals were each other's _____.",
            "She had to face her _____ in the competition."
        ])
    elif "nominal" in word_lower:
        sentences.extend([
            "There is only a _____ fee for admission to the museum.",
            "The charge was merely _____ and didn't cost much.",
            "He received a _____ payment for his help.",
            "The _____ amount was barely noticeable.",
            "They charged a _____ sum for the service.",
            "The _____ cost was much less than expected.",
            "She paid a _____ fee to join the club.",
            "The _____ price was affordable for everyone.",
            "It was only a _____ charge, not a real expense.",
            "The _____ payment was symbolic rather than significant."
        ])
    elif "novelty" in word_lower:
        sentences.extend([
            "The _____ of the new toy wore off quickly.",
            "The _____ of living in a new city soon faded.",
            "She enjoyed the _____ of trying something different.",
            "The _____ of the experience made it exciting.",
            "After a while, the _____ began to wear thin.",
            "The _____ of the situation intrigued everyone.",
            "He was attracted by the _____ of the idea.",
            "The _____ of the gadget made it popular initially.",
            "She appreciated the _____ of the unusual approach.",
            "The _____ of the new method soon became routine."
        ])
    elif "novice" in word_lower:
        sentences.extend([
            "The _____ made several mistakes on her first day.",
            "As a _____, he needed extra help and guidance.",
            "The _____ was eager to learn from experienced players.",
            "She was still a _____ at playing the piano.",
            "The _____ struggled with the difficult task.",
            "Even a _____ could see the obvious solution.",
            "The _____ needed patience and encouragement.",
            "He felt like a _____ compared to the experts.",
            "The _____ was nervous about making mistakes.",
            "She welcomed the _____ with helpful advice."
        ])
    elif "nuance" in word_lower:
        sentences.extend([
            "The actor captured every _____ of the character.",
            "She understood the subtle _____ of the situation.",
            "The _____ of his meaning was lost in translation.",
            "He appreciated the _____ of the different shades.",
            "The _____ between the two words was important.",
            "She noticed the fine _____ in his expression.",
            "The _____ of the argument was complex.",
            "He missed the subtle _____ of her comment.",
            "The _____ of the colour was barely noticeable.",
            "She explained the _____ to help them understand."
        ])
    elif "nullify" in word_lower:
        sentences.extend([
            "The court decided to _____ the unfair contract.",
            "The new law would _____ the previous agreement.",
            "She tried to _____ the negative effects.",
            "The evidence would _____ his entire argument.",
            "They hoped to _____ the damage that was done.",
            "The decision would _____ all their hard work.",
            "He wanted to _____ the mistake he had made.",
            "The change would _____ the original plan.",
            "She attempted to _____ the consequences.",
            "The ruling would _____ the earlier judgment."
        ])
    elif "oblong" in word_lower:
        sentences.extend([
            "The _____ table could seat more people than a square one.",
            "She drew an _____ shape on the paper.",
            "The _____ garden stretched along the side of the house.",
            "The _____ window was longer than it was wide.",
            "He preferred the _____ design to the round one.",
            "The _____ mirror hung on the wall.",
            "The _____ field was perfect for football.",
            "She cut the paper into an _____ piece.",
            "The _____ room had an unusual layout.",
            "The _____ box was difficult to wrap."
        ])
    elif "obtuse" in word_lower:
        sentences.extend([
            "He seemed _____ and missed the obvious clues.",
            "The _____ student needed extra explanation.",
            "She was being deliberately _____ about the problem.",
            "His _____ response showed he didn't understand.",
            "The _____ angle was greater than ninety degrees.",
            "She found his _____ attitude frustrating.",
            "The _____ remark showed a lack of insight.",
            "He appeared _____ to the subtle hints.",
            "The _____ comment revealed his confusion.",
            "She tried to explain to the _____ pupil."
        ])
    elif "ominous" in word_lower:
        sentences.extend([
            "The _____ dark clouds warned of a storm.",
            "The _____ silence made everyone nervous.",
            "She felt an _____ sense of danger approaching.",
            "The _____ music created a tense atmosphere.",
            "The _____ warning signs were everywhere.",
            "He noticed the _____ change in the weather.",
            "The _____ shadow loomed over the house.",
            "She heard an _____ sound in the distance.",
            "The _____ feeling grew stronger as night fell.",
            "The _____ prediction came true after all."
        ])
    elif "onerous" in word_lower:
        sentences.extend([
            "The _____ task of cleaning the entire house took all day.",
            "She found the _____ duties overwhelming.",
            "The _____ responsibility weighed heavily on him.",
            "He struggled with the _____ workload.",
            "The _____ job required many hours of work.",
            "She was burdened by the _____ obligations.",
            "The _____ assignment seemed impossible to complete.",
            "He complained about the _____ nature of the work.",
            "The _____ challenge tested their endurance.",
            "She felt exhausted by the _____ demands."
        ])
    elif "opaque" in word_lower:
        sentences.extend([
            "The _____ glass provided privacy from outside.",
            "The _____ liquid made it impossible to see through.",
            "The _____ material blocked all light.",
            "She couldn't understand his _____ explanation.",
            "The _____ window prevented anyone from looking in.",
            "The _____ substance was completely solid.",
            "His _____ reasoning was difficult to follow.",
            "The _____ barrier separated the two rooms.",
            "The _____ surface reflected the light.",
            "She found his answer _____ and confusing."
        ])
    elif "optimal" in word_lower:
        sentences.extend([
            "The _____ time to plant seeds is in the spring.",
            "She found the _____ solution to the problem.",
            "The _____ conditions helped the plants grow.",
            "He chose the _____ route to save time.",
            "The _____ temperature was perfect for baking.",
            "She achieved _____ results through careful planning.",
            "The _____ setting made everything work smoothly.",
            "He waited for the _____ moment to act.",
            "The _____ arrangement improved efficiency.",
            "She selected the _____ option from the choices."
        ])
    elif "orator" in word_lower:
        sentences.extend([
            "The famous _____ inspired the crowd with his powerful speech.",
            "She was known as a skilled _____ who could move audiences.",
            "The _____ spoke with great passion and conviction.",
            "He trained to become an accomplished _____.",
            "The _____ held everyone's attention throughout.",
            "She admired the _____ for his eloquence.",
            "The _____ delivered an inspiring message.",
            "He was considered one of the greatest _____s of his time.",
            "The _____ used gestures to emphasise his points.",
            "She listened intently to the _____'s words."
        ])
    elif "ordeal" in word_lower:
        sentences.extend([
            "The journey through the storm was a terrible _____.",
            "She survived the _____ with great courage.",
            "The _____ tested their strength and determination.",
            "He described the _____ as the worst experience of his life.",
            "The _____ lasted for several difficult days.",
            "She emerged from the _____ stronger than before.",
            "The _____ challenged them in many ways.",
            "He hoped never to face such an _____ again.",
            "The _____ taught them valuable lessons.",
            "She supported him through the difficult _____."
        ])
    elif "ornate" in word_lower:
        sentences.extend([
            "The _____ carving took months to complete.",
            "She admired the _____ decoration on the building.",
            "The _____ design featured intricate patterns.",
            "He preferred simple styles to _____ ones.",
            "The _____ furniture was beautifully crafted.",
            "She found the _____ details fascinating.",
            "The _____ architecture impressed all visitors.",
            "He thought the _____ style was too elaborate.",
            "The _____ frame enhanced the painting.",
            "She appreciated the _____ craftsmanship."
        ])
    elif "paltry" in word_lower:
        sentences.extend([
            "The _____ amount offered was insulting.",
            "She received only a _____ sum for her work.",
            "The _____ payment was hardly worth the effort.",
            "He dismissed the _____ excuse as inadequate.",
            "The _____ reward didn't match the achievement.",
            "She was disappointed by the _____ compensation.",
            "The _____ sum was barely enough to cover costs.",
            "He considered the _____ amount an insult.",
            "The _____ contribution was almost nothing.",
            "She refused the _____ offer indignantly."
        ])
    elif "panache" in word_lower:
        sentences.extend([
            "She performed the dance with great _____ and elegance.",
            "He completed the task with _____ and style.",
            "The _____ of her performance impressed everyone.",
            "She approached everything with _____ and confidence.",
            "His _____ made the routine look effortless.",
            "The _____ of her presentation was remarkable.",
            "She executed the move with perfect _____.",
            "His _____ set him apart from others.",
            "The _____ of her approach was admirable.",
            "She did everything with _____ and flair."
        ])
    elif "parable" in word_lower:
        sentences.extend([
            "The teacher told a _____ about kindness to help the children understand.",
            "She explained the moral lesson through a simple _____.",
            "The _____ taught an important life lesson.",
            "He understood the meaning behind the _____.",
            "The _____ illustrated the value of honesty.",
            "She found wisdom in the ancient _____.",
            "The _____ helped them grasp the concept.",
            "He retold the _____ to make a point.",
            "The _____ conveyed a deeper message.",
            "She learned from the _____'s moral."
        ])
    elif "paradox" in word_lower:
        sentences.extend([
            "It's a _____ that less can sometimes be more.",
            "The _____ confused everyone who heard it.",
            "She tried to understand the puzzling _____.",
            "The _____ seemed contradictory but was actually true.",
            "He explained the _____ carefully to the class.",
            "The _____ challenged their way of thinking.",
            "She found the _____ intriguing and thought-provoking.",
            "The _____ appeared to make no sense at first.",
            "He enjoyed exploring the _____ in his writing.",
            "The _____ revealed an unexpected truth."
        ])
    elif "paragon" in word_lower:
        sentences.extend([
            "She was a _____ of virtue, always helping others.",
            "He was considered a _____ of excellence.",
            "The _____ of kindness inspired everyone.",
            "She became a _____ of patience and understanding.",
            "He was held up as a _____ to follow.",
            "The _____ of dedication worked tirelessly.",
            "She was seen as a _____ of good behaviour.",
            "The _____ of wisdom shared valuable advice.",
            "He was a _____ of courage and bravery.",
            "The _____ of generosity gave freely to others."
        ])
    elif "parody" in word_lower:
        sentences.extend([
            "The comedy show featured a _____ of famous films.",
            "She wrote a humorous _____ of the popular book.",
            "The _____ made fun of the original in a clever way.",
            "He enjoyed watching the _____ of the serious play.",
            "The _____ was both funny and respectful.",
            "She created a _____ that everyone found amusing.",
            "The _____ imitated the style perfectly.",
            "He laughed at the clever _____.",
            "The _____ captured the essence humorously.",
            "She appreciated the wit of the _____."
        ])
    elif "partial" in word_lower:
        sentences.extend([
            "His _____ recovery meant he still needed rest.",
            "She had only a _____ understanding of the topic.",
            "The _____ payment was not enough to cover the bill.",
            "He showed _____ improvement but wasn't fully better.",
            "The _____ eclipse was visible from their location.",
            "She gave a _____ answer that didn't explain everything.",
            "The _____ success encouraged them to continue.",
            "He had a _____ view of the situation.",
            "The _____ solution helped but didn't solve everything.",
            "She made a _____ attempt that fell short."
        ])
    elif "pensive" in word_lower:
        sentences.extend([
            "She sat in _____ silence gazing out the window.",
            "His _____ expression showed he was deep in thought.",
            "The _____ mood made everyone quiet.",
            "She had a _____ look on her face.",
            "The _____ atmosphere encouraged reflection.",
            "He became _____ after hearing the news.",
            "The _____ moment allowed for contemplation.",
            "She was _____ about the important decision.",
            "The _____ silence was thoughtful and peaceful.",
            "He appeared _____ as he considered the options."
        ])
    elif "perjury" in word_lower:
        sentences.extend([
            "The witness was charged with _____ for lying in court.",
            "Committing _____ is a serious criminal offence.",
            "She was accused of _____ after giving false testimony.",
            "The _____ charge carried severe consequences.",
            "He was found guilty of _____ and sentenced accordingly.",
            "The _____ case shocked everyone in the courtroom.",
            "She understood that _____ was a serious crime.",
            "The _____ conviction damaged his reputation.",
            "He warned her about the dangers of committing _____.",
            "The _____ allegation was investigated thoroughly."
        ])
    elif "persona" in word_lower:
        sentences.extend([
            "He adopted a confident _____ at work, hiding his nervousness.",
            "She maintained a cheerful _____ despite feeling sad.",
            "The public _____ was different from his private self.",
            "He created a _____ that impressed others.",
            "She dropped her professional _____ when with friends.",
            "The _____ he showed was carefully constructed.",
            "She struggled to maintain her confident _____.",
            "The _____ masked his true feelings.",
            "He developed a _____ that suited the role.",
            "The _____ she presented was not entirely genuine."
        ])
    elif "phalanx" in word_lower:
        sentences.extend([
            "The soldiers advanced in a _____ formation.",
            "The _____ of troops moved forward together.",
            "He studied the ancient _____ battle tactics.",
            "The _____ created an impenetrable wall.",
            "She learned about the Greek _____ in history class.",
            "The _____ moved as one unified group.",
            "He admired the discipline of the _____.",
            "The _____ formation was highly effective.",
            "She saw the _____ advancing across the field.",
            "The _____ protected each soldier within it."
        ])
    elif "pillage" in word_lower:
        sentences.extend([
            "The invaders began to _____ the village.",
            "They would _____ everything valuable they found.",
            "The soldiers were ordered to _____ the enemy's supplies.",
            "She read about how armies would _____ conquered cities.",
            "The _____ of the town left it in ruins.",
            "He learned about the _____ that occurred during wars.",
            "The _____ destroyed everything in its path.",
            "She was horrified by the _____ of the peaceful village.",
            "The _____ left nothing behind.",
            "He condemned the _____ of innocent people's homes."
        ])
    elif "pining" in word_lower:
        sentences.extend([
            "She was _____ for her lost love.",
            "He spent days _____ for his missing pet.",
            "The _____ dog waited patiently for its owner.",
            "She found herself _____ for home.",
            "The _____ child missed her parents terribly.",
            "He was _____ away from lack of proper care.",
            "The _____ expression showed her sadness.",
            "She couldn't stop _____ for what she had lost.",
            "The _____ was evident in her eyes.",
            "He was _____ for the good old days."
        ])
    elif "pitfall" in word_lower:
        sentences.extend([
            "Be aware of the _____s of online shopping.",
            "She warned him about the potential _____s.",
            "The _____ caught many people by surprise.",
            "He avoided the common _____ through careful planning.",
            "The _____ was hidden and difficult to spot.",
            "She learned about the _____s from experience.",
            "The _____ could trap the unwary traveller.",
            "He identified the _____ before it caused problems.",
            "The _____ was a danger they hadn't anticipated.",
            "She helped others avoid the _____ she had encountered."
        ])
    elif "pivotal" in word_lower:
        sentences.extend([
            "This was a _____ moment in her career.",
            "The _____ decision changed everything.",
            "He played a _____ role in the success.",
            "The _____ point determined the outcome.",
            "She recognised the _____ importance of the event.",
            "The _____ moment arrived unexpectedly.",
            "He understood the _____ nature of the situation.",
            "The _____ choice would affect everyone.",
            "She was at a _____ stage in her life.",
            "The _____ factor made all the difference."
        ])
    elif "placate" in word_lower:
        sentences.extend([
            "She tried to _____ the upset customer.",
            "He attempted to _____ his angry friend.",
            "The apology helped to _____ their concerns.",
            "She hoped to _____ the worried parents.",
            "The gesture was meant to _____ the crowd.",
            "He tried to _____ her fears with reassurance.",
            "The explanation helped to _____ their doubts.",
            "She worked to _____ the frustrated students.",
            "The compromise helped to _____ both sides.",
            "He sought to _____ the disappointed supporters."
        ])
    elif "plenary" in word_lower:
        sentences.extend([
            "The _____ session included all members of the committee.",
            "She attended the _____ meeting with everyone present.",
            "The _____ assembly gathered for important decisions.",
            "He spoke at the _____ conference.",
            "The _____ gathering required full attendance.",
            "She participated in the _____ discussion.",
            "The _____ meeting was open to all members.",
            "He was required to attend the _____ session.",
            "The _____ assembly made final decisions.",
            "She presented her ideas at the _____ meeting."
        ])
    elif "pliant" in word_lower:
        sentences.extend([
            "The _____ branches bent easily in the wind.",
            "She found the _____ material easy to shape.",
            "The _____ young tree swayed gently.",
            "He preferred _____ materials that could bend.",
            "The _____ wire could be twisted into any shape.",
            "She admired the _____ nature of the flexible wood.",
            "The _____ stem moved with the breeze.",
            "He chose _____ branches for his project.",
            "The _____ material was perfect for crafting.",
            "She tested how _____ the new substance was."
        ])
    elif "plight" in word_lower:
        sentences.extend([
            "The charity helps those in desperate _____.",
            "She was moved by the _____ of the homeless.",
            "The _____ of the refugees touched everyone.",
            "He tried to improve their difficult _____.",
            "The _____ seemed hopeless at first.",
            "She worked to alleviate their terrible _____.",
            "The _____ required immediate attention.",
            "He was aware of their challenging _____.",
            "The _____ affected many families.",
            "She couldn't ignore their desperate _____."
        ])
    elif "plummet" in word_lower:
        sentences.extend([
            "The temperature _____ed overnight.",
            "Her confidence began to _____ after the mistake.",
            "The prices _____ed during the sale.",
            "He watched the bird _____ towards the ground.",
            "The stock market _____ed unexpectedly.",
            "Her spirits _____ed when she heard the news.",
            "The plane began to _____ through the clouds.",
            "His hopes _____ed as the situation worsened.",
            "The value _____ed rapidly.",
            "She felt her heart _____ at the sight."
        ])
    elif "ponder" in word_lower:
        sentences.extend([
            "She _____ed the question before answering.",
            "He would _____ over difficult problems for hours.",
            "The _____ing helped her reach a decision.",
            "He needed time to _____ the important choice.",
            "She would _____ the meaning of the poem.",
            "The _____ing led to new insights.",
            "He liked to _____ while walking in nature.",
            "She would _____ the consequences carefully.",
            "The _____ing was necessary before acting.",
            "He would _____ the possibilities before deciding."
        ])
    elif "porous" in word_lower:
        sentences.extend([
            "The _____ sponge quickly absorbed the water.",
            "The _____ rock allowed water to seep through.",
            "She studied the _____ material in science class.",
            "The _____ surface let air pass through easily.",
            "He noticed how _____ the soil was.",
            "The _____ membrane filtered the liquid.",
            "She tested how _____ different materials were.",
            "The _____ clay held water well.",
            "He explained why _____ materials were useful.",
            "The _____ nature made it perfect for filtering."
        ])
    elif "potent" in word_lower:
        sentences.extend([
            "The _____ medicine cured his illness quickly.",
            "She felt the _____ effects of the treatment.",
            "The _____ potion had powerful results.",
            "He warned about the _____ nature of the substance.",
            "The _____ smell filled the entire room.",
            "She recognised the _____ force of the argument.",
            "The _____ mixture required careful handling.",
            "He was impressed by the _____ solution.",
            "The _____ remedy worked immediately.",
            "She respected the _____ power of the medicine."
        ])
    elif "prattle" in word_lower:
        sentences.extend([
            "The children continued to _____ about their day.",
            "She would _____ on without saying anything important.",
            "The _____ing was pleasant but meaningless.",
            "He listened patiently to her _____ing.",
            "The _____ went on for hours without purpose.",
            "She would _____ about trivial matters.",
            "The constant _____ing became annoying.",
            "He tried to ignore the mindless _____ing.",
            "The _____ was cheerful but empty.",
            "She would _____ happily about nothing in particular."
        ])
    elif "prelude" in word_lower:
        sentences.extend([
            "The small argument was a _____ to a bigger conflict.",
            "The opening act served as a _____ to the main performance.",
            "She saw it as a _____ to more serious problems.",
            "The _____ set the tone for what followed.",
            "He recognised it as a _____ to trouble.",
            "The _____ introduced the main theme.",
            "She understood it was just a _____.",
            "The _____ prepared them for what was coming.",
            "He saw the _____ as a warning sign.",
            "The _____ was followed by the main event."
        ])
    elif "procure" in word_lower:
        sentences.extend([
            "She managed to _____ tickets for the sold-out concert.",
            "He worked hard to _____ the necessary supplies.",
            "The _____ment of resources took several days.",
            "She was able to _____ everything they needed.",
            "The _____ment process was complicated.",
            "He helped _____ the required materials.",
            "The _____ment required careful planning.",
            "She succeeded in _____ing the rare item.",
            "The _____ment was successful after many attempts.",
            "He was responsible for _____ing the equipment."
        ])
    elif "prodigy" in word_lower:
        sentences.extend([
            "Mozart was a musical _____.",
            "She was considered a maths _____ at school.",
            "The young _____ amazed everyone with her talent.",
            "He was recognised as a chess _____.",
            "The _____ showed exceptional ability from an early age.",
            "She became a _____ through hard work and talent.",
            "The _____'s skills were remarkable.",
            "He was hailed as a _____ in his field.",
            "The _____ achieved success at a young age.",
            "She was proud to be called a _____."
        ])
    elif "profane" in word_lower:
        sentences.extend([
            "Using _____ language in the church was inappropriate.",
            "She was shocked by the _____ words he used.",
            "The _____ language offended many people.",
            "He apologised for his _____ remarks.",
            "The _____ behaviour was not acceptable.",
            "She avoided _____ language in polite company.",
            "The _____ comments were disrespectful.",
            "He was warned about using _____ language.",
            "The _____ nature of the words was clear.",
            "She found the _____ language offensive."
        ])
    elif "profess" in word_lower:
        sentences.extend([
            "He _____ed his innocence despite the evidence.",
            "She would _____ her love for reading.",
            "The _____ion seemed sincere but was actually false.",
            "He would _____ to know more than he did.",
            "The _____ion of faith was important to her.",
            "She would _____ her beliefs openly.",
            "The _____ion didn't match his actions.",
            "He would _____ his commitment to the cause.",
            "The _____ion was met with scepticism.",
            "She would _____ her dedication to the project."
        ])
    elif "prosper" in word_lower:
        sentences.extend([
            "The business continued to _____ each year.",
            "She hoped her garden would _____ in the sunshine.",
            "The _____ity brought happiness to the family.",
            "He worked hard to make his venture _____.",
            "The _____ous times were enjoyed by all.",
            "She watched her plants _____ and grow.",
            "The _____ity was the result of careful planning.",
            "He wanted his children to _____ in life.",
            "The _____ous business created many jobs.",
            "She prayed for her family to _____."
        ])
    elif "proverb" in word_lower:
        sentences.extend([
            "\"A stitch in time saves nine\" is a well-known _____.",
            "She remembered the _____ her grandmother taught her.",
            "The ancient _____ contained wisdom.",
            "He quoted a _____ to make his point.",
            "The _____ offered valuable advice.",
            "She found truth in the old _____.",
            "The _____ was passed down through generations.",
            "He used a _____ to explain the concept.",
            "The _____ taught an important lesson.",
            "She lived by the _____ her parents shared."
        ])
    elif "prudent" in word_lower:
        sentences.extend([
            "It was _____ to save money for emergencies.",
            "She made a _____ decision after careful thought.",
            "The _____ choice prevented future problems.",
            "He showed _____ judgement in difficult situations.",
            "The _____ approach avoided unnecessary risks.",
            "She was known for her _____ planning.",
            "The _____ action saved them from trouble.",
            "He advised a _____ course of action.",
            "The _____ behaviour was wise and sensible.",
            "She demonstrated _____ thinking in her choices."
        ])
    elif "pungent" in word_lower:
        sentences.extend([
            "The _____ smell of garlic filled the kitchen.",
            "She noticed the _____ odour immediately.",
            "The _____ aroma was strong and distinctive.",
            "He found the _____ taste too intense.",
            "The _____ smell lingered in the air.",
            "She was surprised by the _____ flavour.",
            "The _____ scent was unmistakable.",
            "He wrinkled his nose at the _____ smell.",
            "The _____ odour was overpowering.",
            "She appreciated the _____ taste of the cheese."
        ])
    elif "quarry" in word_lower:
        sentences.extend([
            "The old _____ was now filled with water.",
            "They worked in the stone _____ all day.",
            "The _____ provided materials for building.",
            "She visited the abandoned _____ on the school trip.",
            "The _____ had been in use for many years.",
            "He learned about _____ing in geography class.",
            "The _____ was deep and dangerous.",
            "She saw the _____ from the hilltop.",
            "The _____ produced high-quality stone.",
            "He explored the old _____ with his friends."
        ])
    elif "raiment" in word_lower:
        sentences.extend([
            "The king's _____ was made of the finest silk.",
            "She admired the beautiful _____ in the museum.",
            "The _____ was ornate and expensive.",
            "He wore simple _____ compared to the others.",
            "The _____ reflected his high status.",
            "She studied the historical _____ in the exhibition.",
            "The _____ was carefully preserved.",
            "He changed into more formal _____.",
            "The _____ was fit for a royal occasion.",
            "She appreciated the quality of the fine _____."
        ])
    elif "ramble" in word_lower:
        sentences.extend([
            "They decided to _____ through the woods on Sunday.",
            "She loved to _____ along the country paths.",
            "The _____ took them through beautiful countryside.",
            "He enjoyed a peaceful _____ in the morning.",
            "The _____ was relaxing and enjoyable.",
            "She would _____ for hours without a destination.",
            "The _____ led them to a hidden stream.",
            "He preferred to _____ alone in nature.",
            "The _____ through the fields was pleasant.",
            "She invited her friends to _____ with her."
        ])
    elif "rampant" in word_lower:
        sentences.extend([
            "Crime became _____ in the neglected area.",
            "The weeds grew _____ throughout the garden.",
            "The _____ spread of rumours caused problems.",
            "She saw _____ growth everywhere she looked.",
            "The _____ inflation affected everyone.",
            "He noticed the _____ corruption in the system.",
            "The _____ disease spread quickly.",
            "She tried to control the _____ weeds.",
            "The _____ behaviour was out of control.",
            "He was concerned about the _____ problem."
        ])
    elif "rancour" in word_lower:
        sentences.extend([
            "There was still _____ between the two families.",
            "The _____ from the argument lingered for years.",
            "She felt deep _____ towards her former friend.",
            "The _____ poisoned their relationship.",
            "He tried to let go of the old _____.",
            "The _____ made reconciliation difficult.",
            "She couldn't hide her _____ any longer.",
            "The _____ was evident in their interactions.",
            "He hoped to overcome the _____ between them.",
            "The _____ had built up over many years."
        ])
    elif "ransack" in word_lower:
        sentences.extend([
            "Burglars _____ed the house looking for valuables.",
            "She watched them _____ the entire room.",
            "The _____ing left everything in disarray.",
            "He was horrified to find his room had been _____ed.",
            "The _____ing was thorough and destructive.",
            "She tried to prevent them from _____ing the place.",
            "The _____ing revealed nothing of value.",
            "He discovered the _____ing when he returned home.",
            "The _____ing caused extensive damage.",
            "She was shocked by the _____ing of her belongings."
        ])
    elif "ratify" in word_lower:
        sentences.extend([
            "The parliament voted to _____ the treaty.",
            "She hoped they would _____ the agreement.",
            "The _____ation was necessary for it to take effect.",
            "He worked to get the proposal _____ed.",
            "The _____ation process took several months.",
            "She was pleased when they decided to _____ it.",
            "The _____ation made the decision official.",
            "He needed their approval to _____ the contract.",
            "The _____ation was unanimous.",
            "She waited anxiously for them to _____ the deal."
        ])
    elif "raucous" in word_lower:
        sentences.extend([
            "The _____ crowd cheered loudly at the match.",
            "She was disturbed by the _____ noise.",
            "The _____ laughter filled the room.",
            "He found the _____ behaviour disruptive.",
            "The _____ celebration continued late into the night.",
            "She tried to quieten the _____ group.",
            "The _____ party annoyed the neighbours.",
            "He enjoyed the _____ atmosphere.",
            "The _____ sounds echoed through the building.",
            "She was used to the _____ environment."
        ])
    elif "recant" in word_lower:
        sentences.extend([
            "He was forced to _____ his statement.",
            "She decided to _____ her previous opinion.",
            "The _____ation was necessary to correct the error.",
            "He had to _____ what he had said earlier.",
            "The _____ation surprised everyone.",
            "She was pressured to _____ her views.",
            "The _____ation was made publicly.",
            "He refused to _____ despite the pressure.",
            "The _____ation changed everything.",
            "She was brave enough to _____ her mistake."
        ])
    elif "recede" in word_lower:
        sentences.extend([
            "The floodwaters began to _____ slowly.",
            "Her fear started to _____ as she gained confidence.",
            "The tide would _____ leaving the beach exposed.",
            "He watched the water _____ from the shore.",
            "The _____ing hairline was noticeable.",
            "She saw the danger _____ into the distance.",
            "The _____ing waves revealed hidden treasures.",
            "He noticed the pain beginning to _____.",
            "The _____ing flood left mud everywhere.",
            "She was relieved to see the water _____."
        ])
    elif "recluse" in word_lower:
        sentences.extend([
            "The old man was a _____ who rarely left his house.",
            "She had become a _____ after the incident.",
            "The _____ preferred solitude to company.",
            "He lived like a _____ in the remote cottage.",
            "The _____'s isolation was self-imposed.",
            "She understood why he had become a _____.",
            "The _____ avoided all social contact.",
            "He was known as the village _____.",
            "The _____'s lifestyle was mysterious.",
            "She tried to befriend the lonely _____."
        ])
    elif "recount" in word_lower:
        sentences.extend([
            "She began to _____ her adventures.",
            "He would _____ the story to anyone who listened.",
            "The _____ing took longer than expected.",
            "She loved to _____ her holiday experiences.",
            "The _____ was detailed and entertaining.",
            "He would _____ every detail carefully.",
            "The _____ing brought back fond memories.",
            "She asked him to _____ what had happened.",
            "The _____ was accurate and complete.",
            "He would _____ the events in order."
        ])
    elif "rectify" in word_lower:
        sentences.extend([
            "We need to _____ this mistake immediately.",
            "She worked hard to _____ the situation.",
            "The _____ication was necessary and urgent.",
            "He promised to _____ the error quickly.",
            "The _____ication process took time.",
            "She was determined to _____ the problem.",
            "The _____ication improved everything.",
            "He took steps to _____ the injustice.",
            "The _____ication was successful.",
            "She found a way to _____ the damage."
        ])
    elif "refute" in word_lower:
        sentences.extend([
            "The evidence _____ed his claims completely.",
            "She tried to _____ the false accusations.",
            "The _____ation was clear and convincing.",
            "He was able to _____ their arguments.",
            "The _____ation left no room for doubt.",
            "She prepared evidence to _____ the claims.",
            "The _____ation was thorough and detailed.",
            "He hoped to _____ the rumours.",
            "The _____ation proved his innocence.",
            "She managed to _____ every point they made."
        ])
    elif "relish" in word_lower:
        sentences.extend([
            "She _____ed the opportunity to travel.",
            "He would _____ every moment of the adventure.",
            "The _____ was tangy and delicious.",
            "She _____ed the challenge ahead.",
            "The _____ added flavour to the meal.",
            "He would _____ the chance to prove himself.",
            "The _____ was her favourite condiment.",
            "She _____ed the freedom of the open road.",
            "The _____ enhanced the taste.",
            "He would _____ the victory when it came."
        ])
    elif "remnant" in word_lower:
        sentences.extend([
            "Only a _____ of the ancient wall remained.",
            "She found a _____ of fabric from the old dress.",
            "The _____ was all that was left.",
            "He discovered a _____ from the past.",
            "The _____ reminded her of what had been.",
            "She kept the _____ as a souvenir.",
            "The _____ was small but significant.",
            "He examined the _____ carefully.",
            "The _____ was evidence of what once existed.",
            "She treasured the _____ of her grandmother's quilt."
        ])
    elif "remorse" in word_lower:
        sentences.extend([
            "He felt deep _____ for his unkind words.",
            "The _____ kept him awake at night.",
            "She showed genuine _____ for her actions.",
            "The _____ was evident in his expression.",
            "He expressed _____ to those he had hurt.",
            "The _____ful apology was sincere.",
            "She couldn't escape the feeling of _____.",
            "The _____ motivated him to make amends.",
            "He was filled with _____ after realising his mistake.",
            "The _____ was a sign of his good character."
        ])
    elif "replete" in word_lower:
        sentences.extend([
            "The book is _____ with beautiful illustrations.",
            "She found the garden _____ with flowers.",
            "The _____ meal satisfied everyone.",
            "He discovered a room _____ with treasures.",
            "The _____ nature of the collection was impressive.",
            "She saw a sky _____ with stars.",
            "The _____ supply met all their needs.",
            "He found the library _____ with books.",
            "The _____ garden was a joy to behold.",
            "She appreciated the _____ details in the artwork."
        ])
    elif "repress" in word_lower:
        sentences.extend([
            "He tried to _____ his anger.",
            "She had to _____ her laughter during the serious meeting.",
            "The _____ion of feelings was unhealthy.",
            "He learned to _____ his emotions.",
            "The _____ion caused internal stress.",
            "She struggled to _____ her excitement.",
            "The _____ion was difficult to maintain.",
            "He was taught to _____ his natural instincts.",
            "The _____ion led to later problems.",
            "She found it hard to _____ her true feelings."
        ])
    elif "reprove" in word_lower:
        sentences.extend([
            "The teacher had to _____ the student for cheating.",
            "She would _____ him gently but firmly.",
            "The _____al was necessary but unpleasant.",
            "He received a _____al for his behaviour.",
            "The _____al helped him understand his mistake.",
            "She didn't want to _____ him too harshly.",
            "The _____al was fair and constructive.",
            "He accepted the _____al without complaint.",
            "The _____al taught him an important lesson.",
            "She had to _____ the children for running indoors."
        ])
    elif "rescind" in word_lower:
        sentences.extend([
            "The company decided to _____ the offer.",
            "She hoped they would _____ the unfair rule.",
            "The _____ion was unexpected but welcome.",
            "He worked to get the decision _____ed.",
            "The _____ion took effect immediately.",
            "She was relieved when they decided to _____ it.",
            "The _____ion corrected the previous mistake.",
            "He requested that they _____ the order.",
            "The _____ion was necessary and justified.",
            "She celebrated when they chose to _____ the ban."
        ])
    elif "residue" in word_lower:
        sentences.extend([
            "A _____ of soap was left in the sink.",
            "She cleaned the _____ from the surface.",
            "The _____ was sticky and difficult to remove.",
            "He noticed a _____ on the window.",
            "The _____ remained after cleaning.",
            "She tried to remove every last _____.",
            "The _____ was evidence of what had been there.",
            "He found a _____ of paint on his clothes.",
            "The _____ was barely visible.",
            "She washed away the _____ completely."
        ])
    elif "respite" in word_lower:
        sentences.extend([
            "The rain provided a brief _____ from the heat.",
            "She welcomed the _____ from her busy schedule.",
            "The _____ gave them time to recover.",
            "He enjoyed the peaceful _____.",
            "The _____ was much needed and appreciated.",
            "She found a quiet _____ in the garden.",
            "The _____ allowed them to catch their breath.",
            "He took a _____ from his studies.",
            "The _____ was temporary but refreshing.",
            "She was grateful for the brief _____."
        ])
    elif "retort" in word_lower:
        sentences.extend([
            "She had a quick _____ for every criticism.",
            "His sharp _____ silenced the room.",
            "The clever _____ made everyone laugh.",
            "She prepared a witty _____ in response.",
            "The _____ was quick and clever.",
            "He couldn't think of a good _____.",
            "The _____ showed her intelligence.",
            "She delivered the _____ with confidence.",
            "The _____ was both funny and true.",
            "He admired her clever _____."
        ])
    elif "retract" in word_lower:
        sentences.extend([
            "The newspaper was forced to _____ the false story.",
            "She had to _____ her previous statement.",
            "The _____ion was necessary to correct the error.",
            "He decided to _____ his accusation.",
            "The _____ion was made publicly.",
            "She was willing to _____ her claim.",
            "The _____ion prevented further problems.",
            "He had no choice but to _____ what he said.",
            "The _____ion was the right thing to do.",
            "She quickly _____ed her mistaken comment."
        ])
    elif "revere" in word_lower:
        sentences.extend([
            "Many people _____ the ancient traditions.",
            "She _____ed her grandmother's wisdom.",
            "The _____d leader was respected by all.",
            "He learned to _____ nature and its beauty.",
            "The _____d teacher inspired generations.",
            "She _____ed the memory of her ancestors.",
            "The _____d hero was honoured everywhere.",
            "He came to _____ the simple things in life.",
            "The _____d place was treated with respect.",
            "She _____ed the values her parents taught."
        ])
    elif "revile" in word_lower:
        sentences.extend([
            "The angry mob began to _____ the politician.",
            "She was shocked by how they would _____ him.",
            "The _____ing was harsh and unfair.",
            "He didn't deserve to be _____d so cruelly.",
            "The _____ing continued for hours.",
            "She refused to _____ him despite the pressure.",
            "The _____ing words were hurtful.",
            "He tried to ignore the _____ing comments.",
            "The _____ing was uncalled for.",
            "She was appalled by the _____ing language."
        ])
    elif "rigueur" in word_lower or "rigeur" in word_lower:
        sentences.extend([
            "The de _____ dress code was strictly enforced.",
            "She followed the de _____ rules precisely.",
            "The de _____ standards were very high.",
            "He understood the de _____ requirements.",
            "The de _____ protocol was mandatory.",
            "She adhered to the de _____ guidelines.",
            "The de _____ procedure was essential.",
            "He respected the de _____ tradition.",
            "The de _____ expectations were clear.",
            "She met the de _____ criteria perfectly."
        ])
    else:
        # Generic fallback sentences based on word type
        if is_verb:
            sentences.extend([
                f"They had to _____ the situation before it got worse.",
                f"She decided to _____ the problem quickly and efficiently.",
                f"He tried to _____ what was happening, but it was difficult.",
                f"We need to _____ this matter carefully and thoughtfully.",
                f"You should _____ before making any important decisions.",
                f"It's crucial to _____ properly in such circumstances.",
                f"They managed to _____ successfully despite many obstacles.",
                f"She learned to _____ effectively through careful practice.",
                f"He refused to _____ without thinking it through completely.",
                f"We must _____ to resolve this challenging problem."
            ])
        elif is_adjective:
            sentences.extend([
                f"The situation was very _____ and quite concerning to everyone.",
                f"She showed a _____ attitude that impressed her teachers.",
                f"His behaviour was quite _____ and rather unexpected.",
                f"It was a _____ experience that everyone remembered fondly.",
                f"The _____ nature of the event surprised us all greatly.",
                f"They found it _____ and quite interesting to observe.",
                f"Her response was _____ and very thoughtful indeed.",
                f"The _____ quality made it truly special and unique.",
                f"It seemed _____ to all who witnessed the event.",
                f"The _____ aspect was clear from the very beginning."
            ])
        else:  # noun
            sentences.extend([
                f"The _____ was clear to everyone present at the meeting.",
                f"She understood the _____ of the situation immediately.",
                f"His _____ surprised those around him greatly.",
                f"The _____ became evident very quickly to all observers.",
                f"Everyone noticed the _____ in the way he spoke.",
                f"The _____ provided important context for the story.",
                f"Her _____ was obvious from her actions.",
                f"The _____ helped explain what had happened.",
                f"People discussed the _____ at length.",
                f"The _____ was the key to understanding everything."
            ])
    
    # Ensure we have exactly 10 sentences
    # Remove duplicates while preserving order
    seen = set()
    unique_sentences = []
    for s in sentences:
        if s not in seen:
            seen.add(s)
            unique_sentences.append(s)
    
    # Fill to 10 if needed
    while len(unique_sentences) < 10:
        if is_verb:
            unique_sentences.append(f"They needed to _____ the situation carefully.")
        elif is_adjective:
            unique_sentences.append(f"It was a very _____ moment indeed.")
        else:
            unique_sentences.append(f"The _____ was important to understand.")
    
    return unique_sentences[:10]


def main():
    """Main function to generate quiz sentences"""
    input_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level2_batch4.txt")
    output_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level2_batch4.csv")
    
    print("=" * 70)
    print("GENERATING QUIZ SENTENCES FOR LEVEL 2 BATCH 4")
    print("=" * 70)
    print()
    
    # Read words from input file
    words_data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                word, meaning, example, synonym, antonym = parse_word_line(line)
                if word:
                    words_data.append((word, meaning, example, synonym, antonym))
            except Exception as e:
                print(f"Warning: Could not parse line {line_num}: {e}")
                continue
    
    print(f"Found {len(words_data)} words to process")
    print()
    
    # Generate sentences for each word
    all_sentences = []
    for word, meaning, example, synonym, antonym in words_data:
        print(f"Generating sentences for: {word}")
        sentences = generate_sentences_for_word(word, meaning, example, synonym, antonym)
        for sentence in sentences:
            all_sentences.append(("2", word, sentence))
    
    # Write to CSV
    print()
    print(f"Writing {len(all_sentences)} sentences to {output_file}")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['level', 'word', 'sentence'])  # Header
        writer.writerows(all_sentences)
    
    print()
    print("=" * 70)
    print(f"Level 2 Batch 4 complete: {len(all_sentences)} sentences")
    print("=" * 70)


if __name__ == "__main__":
    main()
