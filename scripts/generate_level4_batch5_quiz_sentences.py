#!/usr/bin/env python3
"""
Generate quiz sentences for Level 4 Batch 5 vocabulary words.
Generates 10 contextually rich sentences per word following British English
and age-appropriate standards for 10-11 year olds.
"""

import csv
import re
from pathlib import Path
from typing import List, Tuple


def create_blank_sentence(sentence: str, word: str) -> str:
    """Replace word with blank, handling case variations."""
    # Use regex to replace word (case-insensitive) with blank
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    return pattern.sub("_____", sentence)


def determine_part_of_speech(meaning: str) -> str:
    """Determine if word is verb, adjective, or noun based on meaning."""
    meaning_lower = meaning.lower()
    
    if meaning_lower.startswith("to "):
        return "verb"
    elif any(marker in meaning_lower for marker in [
        "having", "showing", "full of", "characterised by", "characterized by",
        "very", "extremely", "quite", "rather", "causing", "deserving",
        "making", "relating to", "concerned with", "involving", "behaving",
        "not", "open to", "likely to", "prepared to", "willing to",
        "giving", "allowing", "occupying", "wanting", "devouring"
    ]):
        return "adjective"
    else:
        return "noun"


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
    pos = determine_part_of_speech(meaning)
    
    # 1. Use example sentence if available (best quality)
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate word-specific sentences based on meaning and context
    # Custom sentences for each word to ensure quality and variety
    
    if word_lower == "reverent":
        sentences.extend([
            "The _____ silence in the ancient cathedral showed deep respect.",
            "She spoke in a _____ tone when discussing the sacred text.",
            "His _____ attitude towards the elderly teacher was admirable.",
            "The _____ congregation bowed their heads in prayer.",
            "She showed a _____ respect for the traditions of her ancestors.",
            "The _____ atmosphere made everyone feel peaceful and respectful.",
            "He approached the memorial with _____ care and solemnity.",
            "The _____ way she handled the ancient artefact impressed the curator.",
            "Their _____ behaviour during the ceremony was noticed by all.",
            "The _____ expression on his face showed genuine admiration.",
        ])
    
    elif word_lower == "rhetorical":
        sentences.extend([
            "The speaker asked a _____ question that didn't require an answer.",
            "She used _____ devices to make her speech more persuasive.",
            "His _____ question was meant to make the audience think deeply.",
            "The teacher's _____ style helped students understand complex ideas.",
            "She employed _____ techniques to emphasise her main point.",
            "The _____ nature of his question was clear to everyone listening.",
            "He used _____ language to create a powerful effect.",
            "The _____ question made everyone pause and reflect.",
            "Her _____ approach made the presentation more engaging.",
            "The _____ device helped illustrate the point effectively.",
        ])
    
    elif word_lower == "rudimentary":
        sentences.extend([
            "He had only a _____ understanding of mathematics.",
            "The _____ tools were barely sufficient for the task.",
            "She showed _____ knowledge of the subject but needed to learn more.",
            "The _____ equipment was outdated and needed replacing.",
            "His _____ skills improved quickly with practice.",
            "The _____ system worked but wasn't very efficient.",
            "She possessed only _____ information about the topic.",
            "The _____ shelter provided basic protection from the elements.",
            "His _____ grasp of the language made communication difficult.",
            "The _____ design needed significant improvement.",
        ])
    
    elif word_lower == "sagacious":
        sentences.extend([
            "The _____ old man gave excellent advice to the young people.",
            "Her _____ decision saved the company from disaster.",
            "The _____ teacher always knew how to help struggling students.",
            "His _____ observations impressed everyone at the meeting.",
            "She showed _____ judgement in choosing her friends.",
            "The _____ leader made wise choices for the community.",
            "His _____ words of wisdom guided many through difficult times.",
            "The _____ advice came from years of experience.",
            "She was known for her _____ understanding of human nature.",
            "The _____ mentor helped shape many successful careers.",
        ])
    
    elif word_lower == "sanctimonious":
        sentences.extend([
            "His _____ attitude annoyed everyone in the room.",
            "The _____ speech made her seem insincere and self-righteous.",
            "She spoke in a _____ tone that put others off.",
            "His _____ behaviour made him unpopular with his peers.",
            "The _____ way she judged others was hypocritical.",
            "He had a _____ manner that made people avoid him.",
            "The _____ comments were unnecessary and unhelpful.",
            "Her _____ expression suggested she thought herself superior.",
            "The _____ lecture about morality was poorly received.",
            "His _____ attitude towards others was off-putting.",
        ])
    
    elif word_lower == "sanction":
        sentences.extend([
            "The government imposed _____ on the country for breaking the rules.",
            "She needed official _____ before she could proceed.",
            "The _____ was meant to encourage better behaviour.",
            "He received _____ to use the school facilities.",
            "The _____ prevented trade between the two countries.",
            "She sought _____ from her parents before making the decision.",
            "The _____ was a punishment for unacceptable actions.",
            "He needed proper _____ to access the restricted area.",
            "The _____ was lifted after the country complied with the rules.",
            "She gave her _____ for the school trip to proceed.",
        ])
    
    elif word_lower == "sanctity":
        sentences.extend([
            "The _____ of the temple was respected by all visitors.",
            "They honoured the _____ of the ancient burial ground.",
            "The _____ of marriage was important to them.",
            "She respected the _____ of the sacred ceremony.",
            "The _____ of human life should never be violated.",
            "They preserved the _____ of the historical site.",
            "The _____ of the moment was felt by everyone present.",
            "She understood the _____ of the promise she had made.",
            "The _____ of the holy place was protected by law.",
            "They maintained the _____ of the tradition for generations.",
        ])
    
    elif word_lower == "sanctuary":
        sentences.extend([
            "The wildlife _____ protected endangered species from harm.",
            "She found _____ in the quiet library corner.",
            "The bird _____ was a safe haven for migrating species.",
            "He sought _____ from the storm in the old church.",
            "The nature _____ was home to many rare animals.",
            "She created a peaceful _____ in her garden.",
            "The _____ provided protection for those in need.",
            "He found _____ in the mountains away from the city.",
            "The animal _____ rescued and cared for injured wildlife.",
            "She turned her room into a quiet _____ for reading.",
        ])
    
    elif word_lower == "satisfying":
        sentences.extend([
            "Completing the difficult puzzle was very _____.",
            "The _____ meal left everyone feeling content.",
            "She found the _____ conclusion to the story very rewarding.",
            "The _____ feeling of accomplishment made all the hard work worthwhile.",
            "He experienced a _____ sense of achievement after finishing the project.",
            "The _____ result exceeded everyone's expectations.",
            "She found it _____ to help others in need.",
            "The _____ moment came when she finally understood the problem.",
            "He found the _____ work very fulfilling.",
            "The _____ experience made her want to do it again.",
        ])
    
    elif word_lower == "scarcity":
        sentences.extend([
            "The _____ of water became a serious problem during the drought.",
            "The _____ of resources forced them to be more careful.",
            "She noticed the _____ of books in the small library.",
            "The _____ of food worried the villagers.",
            "The _____ of opportunities made it difficult to find work.",
            "He was concerned about the _____ of clean drinking water.",
            "The _____ of information made the investigation challenging.",
            "She experienced the _____ of time during exam week.",
            "The _____ of materials delayed the building project.",
            "The _____ of qualified teachers affected the school.",
        ])
    
    elif word_lower == "sceptical":
        sentences.extend([
            "She was _____ about the claims in the advertisement.",
            "His _____ attitude made him question everything he heard.",
            "The _____ scientist wanted proof before believing the theory.",
            "She remained _____ until she saw evidence.",
            "His _____ nature made him a good detective.",
            "The _____ student asked many challenging questions.",
            "She was _____ of the stranger's promises.",
            "His _____ response showed he didn't trust the information.",
            "The _____ journalist investigated the story thoroughly.",
            "She was _____ about the weather forecast.",
        ])
    
    elif word_lower == "scholastic":
        sentences.extend([
            "His _____ achievements were impressive and well-recognised.",
            "The _____ competition tested students' knowledge and skills.",
            "She excelled in _____ pursuits throughout her school years.",
            "The _____ awards ceremony celebrated academic excellence.",
            "His _____ performance improved significantly this term.",
            "The _____ environment encouraged learning and discovery.",
            "She received recognition for her _____ accomplishments.",
            "The _____ programme helped students prepare for university.",
            "His _____ interests extended beyond the classroom.",
            "The _____ standards were high but achievable.",
        ])
    
    elif word_lower == "scintillating":
        sentences.extend([
            "The _____ conversation kept everyone engaged and interested.",
            "Her _____ performance on stage captivated the audience.",
            "The _____ wit of the speaker made the lecture enjoyable.",
            "He delivered a _____ speech that inspired everyone.",
            "The _____ discussion covered many fascinating topics.",
            "Her _____ personality made her popular at social events.",
            "The _____ dialogue in the play was clever and entertaining.",
            "He showed _____ intelligence in solving the complex problem.",
            "The _____ presentation held everyone's attention throughout.",
            "Her _____ humour made even serious topics enjoyable.",
        ])
    
    elif word_lower == "scrupulous":
        sentences.extend([
            "He was _____ about following the rules exactly.",
            "The _____ attention to detail impressed her supervisor.",
            "She maintained _____ standards in all her work.",
            "The _____ examination revealed no errors.",
            "He showed _____ care in handling the fragile items.",
            "The _____ teacher checked every answer carefully.",
            "She was _____ in her research methods.",
            "The _____ investigation uncovered important facts.",
            "He kept _____ records of all transactions.",
            "The _____ approach ensured accuracy and reliability.",
        ])
    
    elif word_lower == "scrutinise":
        sentences.extend([
            "The inspector began to _____ every detail of the report.",
            "She needed to _____ the contract before signing it.",
            "The detective would _____ the evidence carefully.",
            "He decided to _____ the proposal thoroughly.",
            "The teacher would _____ each student's work.",
            "She had to _____ the document for any mistakes.",
            "The committee would _____ the application before deciding.",
            "He took time to _____ the painting for authenticity.",
            "The scientist would _____ the results of the experiment.",
            "She would _____ the budget to find savings.",
        ])
    
    elif word_lower == "scrutinize":
        sentences.extend([
            "The detective began to _____ the evidence carefully.",
            "She needed to _____ the document before approving it.",
            "The inspector would _____ every detail of the building.",
            "He decided to _____ the proposal thoroughly.",
            "The teacher would _____ each student's essay.",
            "She had to _____ the contract for any errors.",
            "The committee would _____ the application before accepting it.",
            "He took time to _____ the artwork for quality.",
            "The scientist would _____ the data from the experiment.",
            "She would _____ the accounts to find discrepancies.",
        ])
    
    elif word_lower == "scurrilous":
        sentences.extend([
            "The _____ rumours spread quickly through the school.",
            "She was upset by the _____ comments about her family.",
            "The _____ accusations were completely false.",
            "He spread _____ gossip that damaged reputations.",
            "The _____ article contained many untrue statements.",
            "She refused to listen to _____ talk about her friends.",
            "The _____ remarks were inappropriate and hurtful.",
            "He was known for making _____ statements.",
            "The _____ nature of the claims was obvious.",
            "She was shocked by the _____ language used.",
        ])
    
    elif word_lower == "seclusion":
        sentences.extend([
            "She sought _____ in the quiet library corner.",
            "The _____ of the mountain cabin appealed to him.",
            "He enjoyed the _____ of his study room.",
            "The _____ provided peace and quiet for reflection.",
            "She found _____ in the garden away from the noise.",
            "The _____ of the remote island was perfect for writing.",
            "He valued the _____ of his private workspace.",
            "The _____ helped her concentrate on her studies.",
            "She appreciated the _____ of the countryside.",
            "The _____ of the monastery attracted those seeking peace.",
        ])
    
    elif word_lower == "sedentary":
        sentences.extend([
            "A _____ lifestyle can cause health problems.",
            "The _____ job required sitting at a desk all day.",
            "She tried to avoid _____ activities and stay active.",
            "The _____ nature of the work worried the doctor.",
            "He changed his _____ habits to improve his fitness.",
            "The _____ routine wasn't good for her health.",
            "She encouraged her children to avoid _____ pastimes.",
            "The _____ position made his back ache.",
            "He realised his _____ lifestyle needed to change.",
            "The _____ workday left little time for exercise.",
        ])
    
    elif word_lower == "self-deprecating":
        sentences.extend([
            "His _____ humour made him very likeable.",
            "The _____ comment showed her modesty.",
            "She used _____ jokes to put others at ease.",
            "The _____ remark made everyone laugh.",
            "His _____ attitude prevented him from seeming arrogant.",
            "The _____ way she spoke about her achievements was charming.",
            "She had a _____ sense of humour that others appreciated.",
            "The _____ comment showed he didn't take himself too seriously.",
            "His _____ jokes made him popular with his classmates.",
            "The _____ manner made her seem approachable and friendly.",
        ])
    
    elif word_lower == "self-effacing":
        sentences.extend([
            "The _____ author rarely gave interviews.",
            "Her _____ nature made her avoid the spotlight.",
            "The _____ way she accepted praise showed true humility.",
            "He was _____ about his accomplishments.",
            "The _____ teacher never sought recognition for her work.",
            "She remained _____ despite her many achievements.",
            "The _____ manner made her seem modest and unassuming.",
            "His _____ attitude prevented him from boasting.",
            "The _____ response showed genuine humility.",
            "She was _____ in her approach to success.",
        ])
    
    elif word_lower == "self-righteous":
        sentences.extend([
            "His _____ attitude made him unpopular.",
            "The _____ speech annoyed everyone who heard it.",
            "She had a _____ manner that put others off.",
            "The _____ way he judged others was hypocritical.",
            "His _____ behaviour made people avoid him.",
            "The _____ comments were unnecessary and unhelpful.",
            "She spoke in a _____ tone that was off-putting.",
            "The _____ attitude showed he thought himself superior.",
            "His _____ nature made him difficult to work with.",
            "The _____ lecture about morality was poorly received.",
        ])
    
    elif word_lower == "serendipity":
        sentences.extend([
            "Finding the lost ring was pure _____.",
            "The _____ of meeting her old friend was delightful.",
            "She discovered the solution through _____ rather than planning.",
            "The _____ of the situation made her smile.",
            "He experienced _____ when he found the perfect book.",
            "The _____ encounter led to a wonderful friendship.",
            "She appreciated the _____ of the unexpected discovery.",
            "The _____ of finding the answer by chance was remarkable.",
            "He valued the _____ moments that life sometimes brings.",
            "The _____ of the happy coincidence was wonderful.",
        ])
    
    elif word_lower == "serenity":
        sentences.extend([
            "The _____ of the garden helped her relax.",
            "She found _____ in the peaceful countryside.",
            "The _____ of the lake was soothing and calming.",
            "He sought _____ after a stressful day.",
            "The _____ of the moment was beautiful.",
            "She experienced _____ while watching the sunset.",
            "The _____ of the quiet library was perfect for studying.",
            "He found _____ in meditation and reflection.",
            "The _____ of the scene brought peace to her mind.",
            "She appreciated the _____ of the early morning hours.",
        ])
    
    elif word_lower == "severity":
        sentences.extend([
            "The _____ of the punishment shocked everyone.",
            "She was surprised by the _____ of the storm.",
            "The _____ of the situation became clear to all.",
            "He understood the _____ of the problem.",
            "The _____ of the consequences worried her.",
            "She realised the _____ of her mistake.",
            "The _____ of the illness concerned the doctors.",
            "He was aware of the _____ of the challenge ahead.",
            "The _____ of the damage was extensive.",
            "She recognised the _____ of the warning.",
        ])
    
    elif word_lower == "significant":
        sentences.extend([
            "The discovery was a _____ breakthrough in science.",
            "She made a _____ contribution to the project.",
            "The _____ improvement in her grades pleased her parents.",
            "He noticed a _____ change in the weather.",
            "The _____ event changed everything.",
            "She played a _____ role in organising the event.",
            "The _____ difference was obvious to everyone.",
            "He achieved _____ success in his chosen field.",
            "The _____ impact of the decision was felt by all.",
            "She received _____ recognition for her achievements.",
        ])
    
    elif word_lower == "silhouette":
        sentences.extend([
            "The _____ of the castle stood against the evening sky.",
            "She could see the _____ of a bird flying overhead.",
            "The _____ against the sunset was beautiful.",
            "He recognised her _____ from across the room.",
            "The _____ of the mountains was dramatic.",
            "She drew the _____ of the tree against the moon.",
            "The _____ was clear even from a distance.",
            "He saw the _____ of someone approaching.",
            "The _____ created a striking image.",
            "She admired the _____ of the old building.",
        ])
    
    elif word_lower == "solemnity":
        sentences.extend([
            "The _____ of the occasion was marked by silence.",
            "She felt the _____ of the memorial service.",
            "The _____ of the moment made everyone pause.",
            "He understood the _____ of the promise he was making.",
            "The _____ of the ceremony was appropriate.",
            "She respected the _____ of the situation.",
            "The _____ of the occasion required formal dress.",
            "He appreciated the _____ of the traditional ritual.",
            "The _____ of the vow was clear to all.",
            "She maintained the _____ throughout the proceedings.",
        ])
    
    elif word_lower == "sophisticated":
        sentences.extend([
            "The _____ machinery needed expert handling.",
            "She had a _____ understanding of the complex problem.",
            "The _____ system was difficult to operate.",
            "He showed _____ taste in art and literature.",
            "The _____ technology impressed everyone.",
            "She used _____ methods to solve the puzzle.",
            "The _____ approach yielded better results.",
            "He appreciated _____ humour and clever wordplay.",
            "The _____ design was both beautiful and functional.",
            "She developed a _____ strategy for the competition.",
        ])
    
    elif word_lower == "spendthrift":
        sentences.extend([
            "The _____ quickly ran through his inheritance.",
            "She was known as a _____ who wasted money.",
            "The _____ habits worried his family.",
            "He was a _____ who never saved anything.",
            "The _____ spent money without thinking.",
            "She warned him not to be a _____.",
            "The _____ behaviour led to financial problems.",
            "He realised he had been a _____ for too long.",
            "The _____ nature of his spending was obvious.",
            "She tried to help the _____ manage money better.",
        ])
    
    elif word_lower == "spontaneity":
        sentences.extend([
            "The _____ of their decision made it exciting.",
            "She valued _____ in her creative work.",
            "The _____ of the moment was wonderful.",
            "He enjoyed the _____ of unplanned adventures.",
            "The _____ added joy to the occasion.",
            "She appreciated the _____ of children's play.",
            "The _____ of the response surprised everyone.",
            "He missed the _____ of his younger days.",
            "The _____ made the experience more memorable.",
            "She encouraged _____ in her students' writing.",
        ])
    
    elif word_lower == "spontaneous":
        sentences.extend([
            "The _____ applause surprised the performer.",
            "She made a _____ decision to help.",
            "The _____ reaction was genuine and heartfelt.",
            "He showed _____ generosity to the stranger.",
            "The _____ gesture was much appreciated.",
            "She had a _____ nature that others admired.",
            "The _____ offer to help was kind.",
            "He gave a _____ speech that moved everyone.",
            "The _____ act of kindness was touching.",
            "She enjoyed _____ moments of fun.",
        ])
    
    elif word_lower == "spoonerism":
        sentences.extend([
            "Saying 'well-boiled icicle' instead of 'well-oiled bicycle' is a _____.",
            "The _____ made everyone laugh.",
            "She accidentally made a _____ when she was nervous.",
            "The _____ 'tons of soil' instead of 'sons of toil' was amusing.",
            "He created a _____ without realising it.",
            "The _____ 'you have hissed my mystery lectures' was funny.",
            "She found the _____ entertaining.",
            "The _____ showed how easy it is to mix up words.",
            "He laughed at his own _____.",
            "The _____ 'a blushing crow' instead of 'a crushing blow' was clever.",
        ])
    
    elif word_lower == "stereotype":
        sentences.extend([
            "We should challenge harmful _____.",
            "The _____ about teenagers was unfair.",
            "She refused to accept the _____.",
            "The _____ didn't reflect reality.",
            "He fought against the _____.",
            "The _____ was based on prejudice.",
            "She worked to break down the _____.",
            "The _____ limited people's understanding.",
            "He rejected the _____ completely.",
            "The _____ was outdated and incorrect.",
        ])
    
    elif word_lower == "stimulating":
        sentences.extend([
            "The _____ discussion kept everyone engaged.",
            "She found the _____ conversation very interesting.",
            "The _____ lecture inspired many students.",
            "He enjoyed the _____ challenge of the puzzle.",
            "The _____ activity made her think deeply.",
            "She appreciated the _____ nature of the debate.",
            "The _____ book kept her reading late into the night.",
            "He found the _____ environment motivating.",
            "The _____ experience broadened her horizons.",
            "She valued the _____ exchange of ideas.",
        ])
    
    elif word_lower == "stipulatory":
        sentences.extend([
            "The _____ terms had to be met before approval.",
            "She reviewed the _____ conditions carefully.",
            "The _____ requirements were clearly stated.",
            "He understood the _____ nature of the agreement.",
            "The _____ clause was important.",
            "She checked all the _____ details.",
            "The _____ provisions had to be followed.",
            "He met all the _____ conditions.",
            "The _____ terms were non-negotiable.",
            "She ensured the _____ requirements were satisfied.",
        ])
    
    elif word_lower == "stupidity":
        sentences.extend([
            "The _____ of his actions was obvious to everyone.",
            "She was frustrated by the _____ of the mistake.",
            "The _____ of the decision became clear later.",
            "He regretted the _____ of his behaviour.",
            "The _____ of the plan was evident.",
            "She couldn't believe the _____ of the situation.",
            "The _____ of the error was costly.",
            "He was embarrassed by the _____ of his comment.",
            "The _____ of the approach was clear.",
            "She warned against the _____ of such actions.",
        ])
    
    elif word_lower == "subordinate":
        sentences.extend([
            "She treated her _____ with respect.",
            "The _____ position meant he had less authority.",
            "He was a _____ to the manager.",
            "The _____ role required following instructions.",
            "She worked as a _____ in the organisation.",
            "The _____ staff member reported to the supervisor.",
            "He understood his _____ status in the hierarchy.",
            "The _____ officer followed orders from above.",
            "She respected her _____ colleagues.",
            "The _____ worker completed the assigned tasks.",
        ])
    
    elif word_lower == "subservient":
        sentences.extend([
            "The _____ assistant never questioned his boss.",
            "She refused to be _____ to anyone.",
            "The _____ attitude was not respected.",
            "He showed a _____ manner that worried others.",
            "The _____ behaviour was inappropriate.",
            "She disliked the _____ way he acted.",
            "The _____ position made him uncomfortable.",
            "He was too _____ to stand up for himself.",
            "The _____ nature of the role was clear.",
            "She encouraged him not to be so _____.",
        ])
    
    elif word_lower == "substantial":
        sentences.extend([
            "She made a _____ contribution to the fund.",
            "The _____ amount of money surprised everyone.",
            "He received _____ support from his friends.",
            "The _____ improvement was noticeable.",
            "She had a _____ collection of books.",
            "The _____ meal satisfied everyone.",
            "He made _____ progress in his studies.",
            "The _____ building dominated the skyline.",
            "She provided _____ evidence for her claim.",
            "The _____ difference was significant.",
        ])
    
    elif word_lower == "substantiate":
        sentences.extend([
            "He could not _____ his claims with evidence.",
            "She needed to _____ her argument with facts.",
            "The scientist tried to _____ the theory.",
            "He was asked to _____ his statement.",
            "She worked hard to _____ her research findings.",
            "The lawyer needed to _____ the case.",
            "He failed to _____ his accusations.",
            "She provided documents to _____ her story.",
            "The evidence helped _____ the claim.",
            "He struggled to _____ his hypothesis.",
        ])
    
    elif word_lower == "subterfuge":
        sentences.extend([
            "He used _____ to avoid telling the truth.",
            "The _____ was discovered quickly.",
            "She saw through the _____ immediately.",
            "The _____ didn't fool anyone.",
            "He resorted to _____ when honesty failed.",
            "The _____ was clever but dishonest.",
            "She was skilled at detecting _____.",
            "The _____ was unnecessary and wrong.",
            "He regretted using _____ instead of being direct.",
            "The _____ was exposed by the investigation.",
        ])
    
    elif word_lower == "suggestible":
        sentences.extend([
            "Children are often more _____ than adults.",
            "The _____ person believed everything he heard.",
            "She was too _____ to make independent decisions.",
            "The _____ nature made him easy to influence.",
            "He was _____ and easily persuaded.",
            "The _____ student followed peer pressure.",
            "She warned him not to be so _____.",
            "The _____ attitude was a concern.",
            "He realised he had been too _____.",
            "The _____ person needed to think for themselves.",
        ])
    
    elif word_lower == "supercilious":
        sentences.extend([
            "His _____ attitude made him unpopular.",
            "The _____ look on her face was off-putting.",
            "She spoke in a _____ tone that annoyed others.",
            "The _____ manner made people avoid him.",
            "He had a _____ way of looking down on others.",
            "The _____ comment was unnecessary.",
            "She showed a _____ disregard for others' opinions.",
            "The _____ behaviour was arrogant and rude.",
            "He maintained a _____ expression throughout.",
            "The _____ attitude showed he thought himself superior.",
        ])
    
    elif word_lower == "superficial":
        sentences.extend([
            "The _____ wound healed quickly.",
            "She had only a _____ understanding of the topic.",
            "The _____ examination missed important details.",
            "He made a _____ attempt to help.",
            "The _____ analysis wasn't thorough enough.",
            "She gave a _____ answer that didn't address the question.",
            "The _____ knowledge wasn't sufficient.",
            "He had a _____ interest in the subject.",
            "The _____ treatment didn't solve the problem.",
            "She realised her understanding was too _____.",
        ])
    
    elif word_lower == "superiority":
        sentences.extend([
            "His sense of _____ annoyed his classmates.",
            "The _____ of her argument was clear.",
            "She showed an attitude of _____ that was off-putting.",
            "The _____ complex made him difficult to work with.",
            "He felt a sense of _____ over others.",
            "The _____ of the product was obvious.",
            "She displayed _____ in her behaviour.",
            "The _____ attitude was unwelcome.",
            "He demonstrated _____ in his skills.",
            "The _____ of the method was proven.",
        ])
    
    elif word_lower == "supplicate":
        sentences.extend([
            "They had to _____ for mercy from the king.",
            "She would _____ for help in times of need.",
            "The people would _____ for relief from the drought.",
            "He had to _____ for forgiveness.",
            "She would _____ for guidance from her teacher.",
            "The villagers would _____ for protection.",
            "He had to _____ for permission to proceed.",
            "She would _____ for understanding.",
            "The group would _____ for assistance.",
            "He had to _____ for clemency.",
        ])
    
    elif word_lower == "surreptitious":
        sentences.extend([
            "He made a _____ glance at the answers.",
            "The _____ meeting was kept secret.",
            "She took a _____ look at her phone.",
            "The _____ activity was discovered.",
            "He made _____ notes during the lecture.",
            "The _____ way he moved was suspicious.",
            "She had a _____ conversation in the corner.",
            "The _____ glance revealed his true feelings.",
            "He made _____ arrangements without telling anyone.",
            "The _____ nature of the action was clear.",
        ])
    
    elif word_lower == "susceptible":
        sentences.extend([
            "Children are _____ to colds in winter.",
            "The material was _____ to damage.",
            "She was _____ to suggestion.",
            "The area was _____ to flooding.",
            "He was _____ to peer pressure.",
            "The system was _____ to errors.",
            "She was _____ to the disease.",
            "The structure was _____ to collapse.",
            "He was _____ to flattery.",
            "The plant was _____ to frost damage.",
        ])
    
    elif word_lower == "sweltering":
        sentences.extend([
            "The _____ heat made it difficult to work outside.",
            "She found the _____ weather unbearable.",
            "The _____ temperature in the room was uncomfortable.",
            "He struggled in the _____ conditions.",
            "The _____ day made everyone seek shade.",
            "She couldn't sleep in the _____ bedroom.",
            "The _____ climate was exhausting.",
            "He avoided going out in the _____ weather.",
            "The _____ afternoon made everyone tired.",
            "She longed for relief from the _____ heat.",
        ])
    
    elif word_lower == "sycophancy":
        sentences.extend([
            "His _____ towards the teacher was obvious to everyone.",
            "The _____ made others uncomfortable.",
            "She was disgusted by the _____.",
            "The _____ was insincere and self-serving.",
            "He used _____ to gain favour.",
            "The _____ didn't fool anyone.",
            "She saw through the _____ immediately.",
            "The _____ was inappropriate and obvious.",
            "He was known for his _____.",
            "The _____ behaviour was transparent.",
        ])
    
    elif word_lower == "sympathiser":
        sentences.extend([
            "The _____ helped the refugees find shelter.",
            "She was a _____ who supported the cause.",
            "The _____ provided assistance to those in need.",
            "He was a _____ who understood their struggle.",
            "The _____ offered help and encouragement.",
            "She acted as a _____ for the movement.",
            "The _____ showed compassion and support.",
            "He was a loyal _____ of the idea.",
            "The _____ provided resources and aid.",
            "She was a dedicated _____ of the cause.",
        ])
    
    elif word_lower == "synecdoche":
        sentences.extend([
            "Using 'wheels' to refer to a car is an example of _____.",
            "The _____ 'all hands on deck' means everyone should help.",
            "She explained the _____ to the class.",
            "The _____ 'the crown' refers to the monarchy.",
            "He used a _____ when he said 'sails' for ships.",
            "The _____ was a figure of speech.",
            "She recognised the _____ in the poem.",
            "The _____ 'bread' can mean food in general.",
            "He understood the _____ in the text.",
            "The _____ made the writing more interesting.",
        ])
    
    elif word_lower == "tantamount":
        sentences.extend([
            "His refusal was _____ to an admission of guilt.",
            "The action was _____ to betrayal.",
            "She realised it was _____ to giving up.",
            "The decision was _____ to accepting defeat.",
            "He knew it was _____ to admitting he was wrong.",
            "The statement was _____ to a confession.",
            "She understood it was _____ to surrender.",
            "The behaviour was _____ to accepting the terms.",
            "He saw it was _____ to agreeing.",
            "The response was _____ to approval.",
        ])
    
    elif word_lower == "tautology":
        sentences.extend([
            "'Free gift' is a _____ because gifts are always free.",
            "The _____ was unnecessary repetition.",
            "She noticed the _____ in the statement.",
            "The _____ 'round circle' was redundant.",
            "He pointed out the _____ in the phrase.",
            "The _____ made the writing less effective.",
            "She avoided using _____ in her essay.",
            "The _____ 'exact same' was repetitive.",
            "He corrected the _____ in the text.",
            "The _____ weakened the argument.",
        ])
    
    elif word_lower == "tenacity":
        sentences.extend([
            "Her _____ helped her overcome all obstacles.",
            "The _____ of the athlete was impressive.",
            "She showed great _____ in pursuing her goals.",
            "The _____ paid off in the end.",
            "He demonstrated _____ in difficult times.",
            "The _____ of her efforts was remarkable.",
            "She admired his _____ and determination.",
            "The _____ helped them succeed.",
            "He showed _____ despite many setbacks.",
            "The _____ was the key to her success.",
        ])
    
    elif word_lower == "tentative":
        sentences.extend([
            "They made a _____ plan to meet next week.",
            "The _____ agreement was subject to change.",
            "She gave a _____ answer to the question.",
            "The _____ schedule might be adjusted.",
            "He made a _____ suggestion that needed approval.",
            "The _____ arrangement was not final.",
            "She spoke in a _____ voice.",
            "The _____ nature of the plan was clear.",
            "He approached the problem with a _____ attitude.",
            "The _____ proposal required further discussion.",
        ])
    
    elif word_lower == "termination":
        sentences.extend([
            "The _____ of the agreement came as a surprise.",
            "She received notice of the _____ of her contract.",
            "The _____ of the project was disappointing.",
            "He was sad about the _____ of the friendship.",
            "The _____ was effective immediately.",
            "She understood the reasons for the _____.",
            "The _____ of the service affected many people.",
            "He regretted the _____ of the partnership.",
            "The _____ was announced officially.",
            "She accepted the _____ gracefully.",
        ])
    
    elif word_lower == "threadbare":
        sentences.extend([
            "His _____ coat showed years of wear.",
            "The _____ carpet needed replacing.",
            "She wore a _____ jumper that was too old.",
            "The _____ fabric was thin and worn.",
            "He noticed the _____ condition of the rug.",
            "The _____ curtains let in too much light.",
            "She replaced the _____ blanket.",
            "The _____ material was no longer useful.",
            "He threw away the _____ shirt.",
            "The _____ state of the cloth was obvious.",
        ])
    
    elif word_lower == "tormenting":
        sentences.extend([
            "The _____ memories kept him awake at night.",
            "She found the _____ thoughts difficult to ignore.",
            "The _____ experience haunted her for years.",
            "He suffered from _____ nightmares.",
            "The _____ pain was unbearable.",
            "She tried to forget the _____ incident.",
            "The _____ feeling wouldn't go away.",
            "He was troubled by _____ worries.",
            "The _____ nature of the situation was clear.",
            "She sought help for the _____ thoughts.",
        ])
    
    elif word_lower == "tranquility":
        sentences.extend([
            "The _____ of the lake was soothing.",
            "She found _____ in the peaceful garden.",
            "The _____ of the moment was beautiful.",
            "He sought _____ after a busy day.",
            "The _____ helped her relax completely.",
            "She appreciated the _____ of the countryside.",
            "The _____ of the scene was calming.",
            "He found _____ in meditation.",
            "The _____ was disturbed by noise.",
            "She valued the _____ of her quiet room.",
        ])
    
    elif word_lower == "tranquillity":
        sentences.extend([
            "The _____ of the garden helped her relax.",
            "She found _____ in the peaceful setting.",
            "The _____ of the moment was wonderful.",
            "He sought _____ away from the city.",
            "The _____ helped her feel calm.",
            "She appreciated the _____ of nature.",
            "The _____ of the scene was perfect.",
            "He found _____ in the quiet library.",
            "The _____ was peaceful and serene.",
            "She valued the _____ of the early morning.",
        ])
    
    elif word_lower == "transcendent":
        sentences.extend([
            "The _____ beauty of the sunset took her breath away.",
            "She experienced a _____ moment of understanding.",
            "The _____ quality of the music moved everyone.",
            "He achieved a _____ level of skill.",
            "The _____ nature of the experience was profound.",
            "She felt a _____ connection with nature.",
            "The _____ achievement was remarkable.",
            "He reached a _____ state of awareness.",
            "The _____ moment was unforgettable.",
            "She appreciated the _____ beauty of the art.",
        ])
    
    elif word_lower == "transient":
        sentences.extend([
            "The _____ happiness soon faded.",
            "She realised the feeling was _____.",
            "The _____ nature of the situation was clear.",
            "He understood it was a _____ problem.",
            "The _____ visitor stayed only briefly.",
            "She found the _____ joy was temporary.",
            "The _____ phase would pass quickly.",
            "He knew the _____ difficulty wouldn't last.",
            "The _____ emotion was fleeting.",
            "She accepted the _____ nature of the moment.",
        ])
    
    elif word_lower == "transparent":
        sentences.extend([
            "The _____ glass allowed them to see inside.",
            "She appreciated the _____ honesty of his explanation.",
            "The _____ material was easy to see through.",
            "He valued the _____ communication.",
            "The _____ process was clear to everyone.",
            "She made the decision-making process _____.",
            "The _____ container showed its contents.",
            "He preferred _____ methods over secretive ones.",
            "The _____ nature of the organisation was admirable.",
            "She ensured the system was completely _____.",
        ])
    
    elif word_lower == "treacherous":
        sentences.extend([
            "The _____ soldier betrayed his country.",
            "She found the _____ path dangerous to walk.",
            "The _____ weather made travel difficult.",
            "He discovered the _____ plot against him.",
            "The _____ conditions required careful navigation.",
            "She was shocked by the _____ act.",
            "The _____ road was slippery and unsafe.",
            "He warned about the _____ nature of the situation.",
            "The _____ behaviour was unforgivable.",
            "She avoided the _____ area completely.",
        ])
    
    elif word_lower == "trepidation":
        sentences.extend([
            "She approached the exam with _____.",
            "The _____ made her nervous about the outcome.",
            "He felt _____ before the important meeting.",
            "The _____ was understandable given the circumstances.",
            "She tried to overcome her _____.",
            "The _____ affected her performance.",
            "He experienced _____ before the presentation.",
            "The _____ was mixed with excitement.",
            "She felt _____ about the unknown future.",
            "The _____ made her hesitate before acting.",
        ])
    
    elif word_lower == "turbulence":
        sentences.extend([
            "The plane experienced _____ during the flight.",
            "She felt nervous during the _____.",
            "The _____ made the journey uncomfortable.",
            "He was prepared for the _____.",
            "The _____ in the air was unexpected.",
            "She held on tight during the _____.",
            "The _____ caused some passengers to worry.",
            "He remained calm despite the _____.",
            "The _____ was brief but intense.",
            "She was relieved when the _____ ended.",
        ])
    
    elif word_lower == "ubiquitous":
        sentences.extend([
            "Mobile phones have become _____ in modern society.",
            "The _____ presence of technology was obvious.",
            "She noticed how _____ social media had become.",
            "The _____ nature of the problem was concerning.",
            "He found the _____ advertising annoying.",
            "The _____ use of computers was evident.",
            "She realised how _____ the trend had become.",
            "The _____ appearance of the logo was everywhere.",
            "He commented on the _____ nature of the phenomenon.",
            "The _____ presence was impossible to ignore.",
        ])
    
    elif word_lower == "unanimous":
        sentences.extend([
            "The decision was _____ among all members.",
            "She was pleased with the _____ agreement.",
            "The _____ vote showed complete agreement.",
            "He received _____ support for his proposal.",
            "The _____ choice was clear to everyone.",
            "She achieved _____ approval for the plan.",
            "The _____ decision was reached quickly.",
            "He was surprised by the _____ response.",
            "The _____ agreement was rare but welcome.",
            "She valued the _____ support she received.",
        ])
    
    elif word_lower == "unforgiving":
        sentences.extend([
            "The _____ teacher never accepted late work.",
            "She found the _____ nature of the rules harsh.",
            "The _____ terrain was difficult to cross.",
            "He faced an _____ opponent in the competition.",
            "The _____ climate made survival challenging.",
            "She struggled with the _____ conditions.",
            "The _____ attitude made compromise impossible.",
            "He encountered an _____ situation.",
            "The _____ environment tested everyone's limits.",
            "She found the _____ standards too strict.",
        ])
    
    elif word_lower == "uniformity":
        sentences.extend([
            "The _____ of the buildings made the street look dull.",
            "She noticed the _____ in the design.",
            "The _____ was boring and uninteresting.",
            "He preferred variety over _____.",
            "The _____ of the responses was surprising.",
            "She found the _____ monotonous.",
            "The _____ made everything look the same.",
            "He valued diversity over _____.",
            "The _____ was intentional but uninspiring.",
            "She broke the _____ with her unique style.",
        ])
    
    elif word_lower == "universal":
        sentences.extend([
            "The desire for happiness is _____.",
            "She found the _____ appeal of the story interesting.",
            "The _____ nature of the problem affected everyone.",
            "He recognised the _____ truth in the statement.",
            "The _____ acceptance of the idea was remarkable.",
            "She appreciated the _____ themes in the book.",
            "The _____ application of the rule was fair.",
            "He understood the _____ importance of education.",
            "The _____ agreement was unprecedented.",
            "She valued the _____ principles of kindness.",
        ])
    
    elif word_lower == "unprecedented":
        sentences.extend([
            "The _____ heatwave broke all records.",
            "She experienced _____ success in her field.",
            "The _____ event shocked everyone.",
            "He achieved _____ results in the competition.",
            "The _____ nature of the situation was clear.",
            "She faced _____ challenges that year.",
            "The _____ achievement was celebrated widely.",
            "He encountered _____ difficulties.",
            "The _____ scale of the problem was enormous.",
            "She made _____ progress in her studies.",
        ])
    
    elif word_lower == "unpretentious":
        sentences.extend([
            "Despite his wealth, he remained _____ and friendly.",
            "She appreciated his _____ manner.",
            "The _____ approach made her feel comfortable.",
            "He was _____ about his accomplishments.",
            "The _____ style was refreshing.",
            "She valued his _____ attitude.",
            "The _____ way he spoke was genuine.",
            "He maintained an _____ lifestyle.",
            "The _____ nature made him approachable.",
            "She found his _____ personality charming.",
        ])
    
    elif word_lower == "unrequited":
        sentences.extend([
            "She suffered from _____ love for years.",
            "The _____ feelings were painful.",
            "He experienced _____ affection that wasn't returned.",
            "The _____ nature of the relationship was clear.",
            "She tried to move on from the _____ love.",
            "The _____ emotions were difficult to handle.",
            "He accepted that his feelings were _____.",
            "The _____ situation was frustrating.",
            "She learned to cope with _____ love.",
            "The _____ nature of his feelings was obvious.",
        ])
    
    elif word_lower == "unscrupulous":
        sentences.extend([
            "The _____ businessman cheated his customers.",
            "She was shocked by the _____ behaviour.",
            "The _____ methods were unethical.",
            "He was known for his _____ practices.",
            "The _____ nature of the scheme was clear.",
            "She avoided dealing with _____ people.",
            "The _____ actions were condemned.",
            "He was exposed as an _____ individual.",
            "The _____ behaviour had consequences.",
            "She warned others about the _____ tactics.",
        ])
    
    elif word_lower == "unwarranted":
        sentences.extend([
            "His _____ criticism hurt her feelings.",
            "The _____ attack was unfair.",
            "She felt the _____ suspicion was unjust.",
            "The _____ accusations were false.",
            "He received _____ blame for the mistake.",
            "The _____ punishment was too harsh.",
            "She resented the _____ interference.",
            "The _____ concern was unnecessary.",
            "He found the _____ attention annoying.",
            "The _____ nature of the comment was clear.",
        ])
    
    elif word_lower == "ventriloquist":
        sentences.extend([
            "The _____ made the dummy seem to speak.",
            "She was amazed by the _____'s skill.",
            "The _____ entertained the audience with his act.",
            "He learned to be a _____ as a hobby.",
            "The _____'s performance was impressive.",
            "She watched the _____ with fascination.",
            "The _____ made it look like the puppet was talking.",
            "He practised to become a better _____.",
            "The _____'s technique was flawless.",
            "She was curious about how the _____ did it.",
        ])
    
    elif word_lower == "veracity":
        sentences.extend([
            "The _____ of his statement was questioned.",
            "She doubted the _____ of the claim.",
            "The _____ of the information was verified.",
            "He confirmed the _____ of the report.",
            "The _____ of the story was uncertain.",
            "She checked the _____ of the facts.",
            "The _____ of his account was proven.",
            "He maintained the _____ of his testimony.",
            "The _____ of the evidence was clear.",
            "She appreciated the _____ of his explanation.",
        ])
    
    elif word_lower == "vernacular":
        sentences.extend([
            "She wrote in the _____ to reach more readers.",
            "The _____ language was easier to understand.",
            "He spoke in the local _____.",
            "The _____ made the text accessible.",
            "She preferred using _____ over formal language.",
            "The _____ expression was colourful and vivid.",
            "He understood the regional _____.",
            "The _____ helped connect with the audience.",
            "She appreciated the _____ style of writing.",
            "The _____ was appropriate for the context.",
        ])
    
    elif word_lower == "vigorously":
        sentences.extend([
            "She shook the bottle _____ before opening it.",
            "The team defended their position _____.",
            "He protested _____ against the unfair decision.",
            "The exercise was done _____ to build strength.",
            "She argued _____ for her point of view.",
            "The debate was conducted _____.",
            "He worked _____ to complete the task.",
            "The campaign was promoted _____.",
            "She cleaned the room _____.",
            "The team trained _____ for the competition.",
        ])
    
    elif word_lower == "vindictive":
        sentences.extend([
            "His _____ nature made him seek revenge.",
            "The _____ behaviour was concerning.",
            "She avoided the _____ person.",
            "The _____ actions were motivated by spite.",
            "He showed a _____ attitude after the argument.",
            "The _____ nature of the response was clear.",
            "She was shocked by the _____ comments.",
            "The _____ behaviour was unacceptable.",
            "He acted in a _____ manner.",
            "The _____ nature of his actions was obvious.",
        ])
    
    elif word_lower == "vivacious":
        sentences.extend([
            "Her _____ personality made her popular at parties.",
            "The _____ young woman was full of energy.",
            "She had a _____ spirit that was infectious.",
            "The _____ character brought life to the story.",
            "He was attracted to her _____ nature.",
            "The _____ performance was entertaining.",
            "She maintained her _____ attitude despite challenges.",
            "The _____ way she spoke was engaging.",
            "He appreciated her _____ sense of humour.",
            "The _____ energy made everyone feel happy.",
        ])
    
    elif word_lower == "vociferous":
        sentences.extend([
            "The _____ protesters demanded change.",
            "She was _____ in her opposition to the plan.",
            "The _____ complaints were heard by everyone.",
            "He made _____ objections to the proposal.",
            "The _____ nature of the protest was clear.",
            "She was _____ about her rights.",
            "The _____ debate continued for hours.",
            "He was _____ in defending his position.",
            "The _____ crowd made their opinions known.",
            "She remained _____ throughout the discussion.",
        ])
    
    elif word_lower == "voluminous":
        sentences.extend([
            "The _____ report took hours to read.",
            "She wore a _____ dress to the party.",
            "The _____ book contained thousands of pages.",
            "He had _____ notes from the lecture.",
            "The _____ collection filled several rooms.",
            "She wrote a _____ letter explaining everything.",
            "The _____ documentation was extensive.",
            "He produced _____ amounts of work.",
            "The _____ nature of the material was overwhelming.",
            "She was impressed by the _____ research.",
        ])
    
    elif word_lower == "voracious":
        sentences.extend([
            "The _____ reader finished three books in one day.",
            "She had a _____ appetite for learning.",
            "The _____ student devoured every book in the library.",
            "He was a _____ collector of stamps.",
            "The _____ nature of her reading was impressive.",
            "She showed a _____ interest in science.",
            "The _____ appetite was remarkable.",
            "He had a _____ desire for knowledge.",
            "The _____ way she consumed information was amazing.",
            "She was a _____ learner who never stopped studying.",
        ])
    
    elif word_lower == "voyeuristic":
        sentences.extend([
            "His _____ behaviour was inappropriate.",
            "The _____ nature of the activity was concerning.",
            "She found the _____ interest disturbing.",
            "The _____ behaviour violated privacy.",
            "He was accused of _____ conduct.",
            "The _____ nature of the act was wrong.",
            "She was uncomfortable with the _____ attention.",
            "The _____ behaviour was unacceptable.",
            "He showed _____ tendencies that worried others.",
            "The _____ nature of his actions was clear.",
        ])
    
    elif word_lower == "whimsical":
        sentences.extend([
            "The _____ story delighted the children.",
            "She had a _____ sense of humour.",
            "The _____ decorations made the room cheerful.",
            "He appreciated her _____ nature.",
            "The _____ artwork was playful and fun.",
            "She wrote in a _____ style.",
            "The _____ character was endearing.",
            "He enjoyed the _____ elements of the tale.",
            "The _____ nature of the design was charming.",
            "She loved the _____ quality of the music.",
        ])
    
    # Ensure we have exactly 10 sentences
    # Fill remaining slots with contextually appropriate sentences if needed
    while len(sentences) < 10:
        if pos == "verb":
            sentences.append(f"They needed to _____ the situation carefully.")
        elif pos == "adjective":
            sentences.append(f"The _____ nature of the situation was clear.")
        else:  # noun
            sentences.append(f"The _____ was important to understand.")
    
    return sentences[:10]


def main():
    """Main function to generate quiz sentences."""
    input_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level4_batch5.txt")
    output_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level4_batch5.csv")
    
    print("=" * 70)
    print("GENERATING QUIZ SENTENCES FOR LEVEL 4 BATCH 5")
    print("=" * 70)
    print()
    
    # Read input file
    words_data = []
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
                words_data.append((word, meaning, example, synonym, antonym))
    
    print(f"Found {len(words_data)} words to process")
    print()
    
    # Generate sentences
    all_sentences = []
    for word, meaning, example, synonym, antonym in words_data:
        sentences = generate_sentences_for_word(word, meaning, example, synonym, antonym)
        for sentence in sentences:
            all_sentences.append(("4", word, sentence))
        print(f"Generated 10 sentences for: {word}")
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["level", "word", "sentence"])
        writer.writerows(all_sentences)
    
    print()
    print("=" * 70)
    print(f"Level 4 Batch 5 complete: {len(all_sentences)} sentences")
    print(f"Output written to: {output_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
