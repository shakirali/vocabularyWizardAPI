#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 4 Batch 3 vocabulary.
Creates 10 contextually rich sentences per word with strong clues.
"""

import csv
import re
from pathlib import Path


def create_blank_sentence(sentence: str, word: str) -> str:
    """Convert a sentence with the word into fill-in-the-blank format"""
    if not sentence or not word:
        return ""
    
    word_lower = word.lower()
    
    # Create patterns for different word forms
    patterns = [word, word_lower, word.capitalize(), word.title()]
    
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
    elif word_lower.endswith('ent'):
        patterns.extend([
            word_lower + 'ly',
            word_lower + 's'
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
        "impossible", "difficult", "easy", "able", "unable", "worthy",
        "relating to", "consisting of", "motivated", "done", "existing",
        "certain", "well-known", "not suitable", "too great", "not producing",
        "lazy", "hardworking", "unfairness", "unavoidable", "unexplainable"
    ]) or word_lower.endswith(('able', 'ible', 'ent', 'ant', 'ous', 'ive', 'ful', 'less', 'ish', 'ly'))
    is_noun = not is_verb and not is_adjective
    
    # 1. Use the example sentence (convert to blank format)
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate sentences based on word meaning and part of speech
    if is_verb:
        # Verb sentences - action-based contexts
        if "infiltrate" in word_lower:
            verb_sentences = [
                "The spy managed to _____ the enemy headquarters without being detected.",
                "They planned to _____ the organisation to gather secret information.",
                "The detective tried to _____ the criminal gang to catch them.",
                "She attempted to _____ the exclusive club by pretending to be a member.",
                "The journalist wanted to _____ the company to expose corruption.",
                "He managed to _____ the secure building using a clever disguise.",
                "The agent was trained to _____ enemy territory undetected.",
                "They hoped to _____ the meeting to learn about the plans.",
                "The undercover officer tried to _____ the smuggling ring.",
                "She attempted to _____ the private event without an invitation."
            ]
        elif "interrogate" in word_lower:
            verb_sentences = [
                "The detective began to _____ the suspect about the crime.",
                "The police officer had to _____ the witness to get more details.",
                "She watched as they _____ the prisoner for information.",
                "The investigator needed to _____ everyone who was present.",
                "He was trained to _____ suspects without using force.",
                "The lawyer prepared to _____ the witness in court.",
                "They decided to _____ the suspect about his alibi.",
                "The officer began to _____ the driver about the accident.",
                "She had to _____ her brother about where he had been.",
                "The teacher needed to _____ the students about the incident."
            ]
        elif "intimidate" in word_lower:
            verb_sentences = [
                "The bully tried to _____ the younger children in the playground.",
                "She refused to let anyone _____ her into giving up.",
                "The gang attempted to _____ the shopkeeper into paying them.",
                "He didn't want to _____ anyone, but his size made people nervous.",
                "The teacher warned them not to _____ other students.",
                "She felt that the older students were trying to _____ her.",
                "The criminal attempted to _____ the witness into silence.",
                "He wouldn't let anyone _____ him into changing his mind.",
                "The boss tried to _____ the workers into working longer hours.",
                "She refused to be _____ by the difficult challenge ahead."
            ]
        elif "obliterate" in word_lower:
            verb_sentences = [
                "The explosion would _____ the entire building in seconds.",
                "The flood threatened to _____ all evidence of the crime.",
                "She tried to _____ all traces of her mistake from the document.",
                "The fire would _____ everything in its path.",
                "He wanted to _____ the memory of that embarrassing moment.",
                "The earthquake could _____ the entire village.",
                "She attempted to _____ the incorrect data from the system.",
                "The storm would _____ any hope of finding the lost items.",
                "He tried to _____ all records of the failed experiment.",
                "The war threatened to _____ the peaceful way of life."
            ]
        else:
            # Generic verb sentences
            verb_sentences = [
                f"They had to _____ when the situation became dangerous.",
                f"She decided to _____ after realising it was necessary.",
                f"He refused to _____ even when everyone suggested it.",
                f"The team worked together to _____ the difficult challenge.",
                f"Nobody wanted to _____ in such circumstances.",
                f"She managed to _____ despite facing many obstacles.",
                f"They were forced to _____ when they had no other option.",
                f"He learned to _____ after many years of practice.",
                f"We should _____ before it's too late.",
                f"The captain ordered the crew to _____ immediately."
            ]
        
        for sent in verb_sentences:
            if len(sentences) < 10:
                blank_sent = create_blank_sentence(sent, word)
                if blank_sent and "_____" in blank_sent and blank_sent not in sentences:
                    sentences.append(blank_sent)
    
    elif is_adjective:
        # Adjective sentences - descriptive contexts
        if "indolent" in word_lower:
            adj_sentences = [
                "The _____ cat spent the entire day sleeping in the sun.",
                "His _____ attitude towards homework worried his parents.",
                "She was too _____ to help with the chores around the house.",
                "The _____ student never completed his assignments on time.",
                "His _____ behaviour showed he preferred doing nothing.",
                "The _____ worker was always finding excuses to avoid tasks.",
                "She found his _____ approach to life frustrating.",
                "The _____ teenager refused to get out of bed before noon.",
                "His _____ nature meant he avoided any form of exercise.",
                "The _____ employee was eventually let go from the company."
            ]
        elif "indomitable" in word_lower:
            adj_sentences = [
                "Her _____ spirit helped her overcome every obstacle.",
                "The team showed _____ determination throughout the match.",
                "His _____ will to succeed inspired everyone around him.",
                "She possessed an _____ courage that never wavered.",
                "The _____ athlete refused to give up despite the injury.",
                "His _____ resolve made him unstoppable.",
                "The _____ explorer faced every challenge with bravery.",
                "She had an _____ optimism that nothing could destroy.",
                "The _____ warrior fought until the very end.",
                "His _____ character made him a natural leader."
            ]
        elif "industrious" in word_lower:
            adj_sentences = [
                "The _____ students finished their work early every day.",
                "Her _____ nature meant she was always busy with projects.",
                "The _____ worker was promoted for his dedication.",
                "His _____ approach to studying paid off in the exams.",
                "She was known for being _____ and reliable.",
                "The _____ ant worked tirelessly to gather food.",
                "His _____ efforts resulted in excellent grades.",
                "The _____ employee stayed late to finish the project.",
                "She showed an _____ attitude towards all her tasks.",
                "The _____ craftsman took pride in his detailed work."
            ]
        elif "inevitable" in word_lower:
            adj_sentences = [
                "Making mistakes when learning is _____.",
                "The _____ outcome was clear from the start.",
                "Her success seemed _____ given her hard work.",
                "The _____ delay frustrated everyone.",
                "His failure was _____ after he stopped trying.",
                "The _____ result surprised no one.",
                "She knew the _____ conclusion would be difficult.",
                "The _____ change came sooner than expected.",
                "His _____ victory was celebrated by all.",
                "The _____ problem needed immediate attention."
            ]
        elif "inevitably" in word_lower:
            adj_sentences = [
                "The project _____ took longer than planned.",
                "She _____ arrived late due to traffic.",
                "The situation _____ got worse over time.",
                "He _____ made mistakes when rushing.",
                "The weather _____ changed during the day.",
                "She _____ succeeded after all her effort.",
                "The problem _____ required a solution.",
                "He _____ found the answer after thinking.",
                "The team _____ won after their hard work.",
                "She _____ improved with practice."
            ]
        elif "inexplicable" in word_lower:
            adj_sentences = [
                "The _____ disappearance remained unsolved.",
                "Her _____ behaviour confused everyone.",
                "The _____ mystery puzzled the detectives.",
                "His _____ success surprised all his teachers.",
                "The _____ event had no logical explanation.",
                "She found the situation completely _____.",
                "The _____ nature of the problem frustrated them.",
                "His _____ talent appeared from nowhere.",
                "The _____ coincidence seemed too strange to be real.",
                "She was troubled by the _____ turn of events."
            ]
        elif "inedible" in word_lower:
            adj_sentences = [
                "Some mushrooms are _____ and can be poisonous if eaten.",
                "The food had become _____ after being left out too long.",
                "She realised the berries were _____ when she tasted them.",
                "The _____ plants were clearly marked with warning signs.",
                "He discovered that the fruit was _____ due to contamination.",
                "The _____ substance was removed from the kitchen immediately.",
                "She warned them that the mushrooms were _____ and dangerous.",
                "The _____ leftovers were thrown away immediately.",
                "He found that the berries were _____ and should not be consumed.",
                "The _____ food was clearly marked as unsafe to eat."
            ]
        elif "ineffable" in word_lower:
            adj_sentences = [
                "The beauty of the sunset was _____ and beyond description.",
                "She felt an _____ joy that words could not express.",
                "The _____ beauty of the mountain view left them speechless.",
                "He experienced an _____ sense of peace in the garden.",
                "The _____ wonder of the night sky amazed everyone.",
                "She had an _____ feeling that something wonderful was about to happen.",
                "The _____ majesty of the ancient cathedral impressed all visitors.",
                "He felt an _____ connection with nature during the walk.",
                "The _____ perfection of the moment could not be captured in words.",
                "She experienced an _____ sense of awe at the natural wonder."
            ]
        elif "ineffectual" in word_lower:
            adj_sentences = [
                "His _____ attempts to fix the problem only made it worse.",
                "The _____ medicine did nothing to help her headache.",
                "She found his _____ efforts frustrating and unhelpful.",
                "The _____ plan failed to achieve its intended goal.",
                "His _____ leadership led to the team's poor performance.",
                "The _____ solution didn't address the real problem.",
                "She realised her _____ approach wasn't working.",
                "The _____ policy failed to improve the situation.",
                "His _____ response showed he didn't understand the issue.",
                "The _____ treatment had no effect on the patient's condition."
            ]
        elif "infamous" in word_lower:
            adj_sentences = [
                "The _____ villain terrorised the neighbourhood for months.",
                "His _____ reputation made everyone avoid him.",
                "The _____ criminal was finally caught by the police.",
                "She was known for her _____ temper and sharp tongue.",
                "The _____ pirate was feared throughout the Caribbean.",
                "His _____ deeds were recorded in history books.",
                "The _____ gang leader was eventually brought to justice.",
                "She had an _____ reputation for being difficult.",
                "The _____ character in the story was truly evil.",
                "His _____ actions led to his eventual downfall."
            ]
        elif "infernal" in word_lower:
            adj_sentences = [
                "The _____ noise from the building site never stopped.",
                "She complained about the _____ racket from next door.",
                "The _____ heat made it impossible to sleep.",
                "His _____ temper caused problems wherever he went.",
                "The _____ machine kept breaking down at the worst times.",
                "She was fed up with the _____ delays on the train.",
                "The _____ smell from the factory polluted the air.",
                "His _____ behaviour annoyed everyone around him.",
                "The _____ traffic jam made them late for the meeting.",
                "She couldn't stand the _____ noise any longer."
            ]
        elif "influential" in word_lower:
            adj_sentences = [
                "She was an _____ figure in the local community.",
                "The _____ politician had many supporters.",
                "His _____ book changed how people thought about the subject.",
                "The _____ teacher inspired generations of students.",
                "She became an _____ voice in the environmental movement.",
                "The _____ scientist made groundbreaking discoveries.",
                "His _____ ideas shaped the future of technology.",
                "The _____ leader brought about positive changes.",
                "She was recognised as an _____ expert in her field.",
                "The _____ writer's works were studied in schools."
            ]
        elif "ingenious" in word_lower:
            adj_sentences = [
                "The _____ solution solved the problem instantly.",
                "She came up with an _____ way to save time.",
                "The _____ invention revolutionised the industry.",
                "His _____ plan helped them escape from danger.",
                "The _____ design was both beautiful and practical.",
                "She showed an _____ understanding of the complex issue.",
                "The _____ method was much more efficient than the old one.",
                "His _____ approach surprised everyone with its simplicity.",
                "The _____ device made life much easier for everyone.",
                "She had an _____ mind that could solve any puzzle."
            ]
        elif "innocuous" in word_lower:
            adj_sentences = [
                "The _____ remark was misunderstood by everyone.",
                "She thought the question was _____ and harmless.",
                "The _____ comment caused unexpected offence.",
                "His _____ joke was taken the wrong way.",
                "The _____ plant looked safe but was actually poisonous.",
                "She made an _____ observation that no one noticed.",
                "The _____ substance seemed harmless but wasn't.",
                "His _____ behaviour was actually quite suspicious.",
                "The _____ question led to an important discovery.",
                "She found the _____ comment more significant than it appeared."
            ]
        elif "inopportune" in word_lower:
            adj_sentences = [
                "He arrived at an _____ moment during the important meeting.",
                "The _____ timing of the phone call interrupted their conversation.",
                "She chose an _____ time to ask for a favour.",
                "The _____ rain ruined their outdoor picnic plans.",
                "His _____ comment made everyone uncomfortable.",
                "The _____ interruption came at the worst possible moment.",
                "She picked an _____ moment to bring up the difficult topic.",
                "The _____ arrival of the guests surprised everyone.",
                "His _____ question disrupted the flow of the presentation.",
                "The _____ timing of the announcement caused confusion."
            ]
        elif "inquisitive" in word_lower:
            adj_sentences = [
                "The _____ child asked questions about everything.",
                "Her _____ nature made her an excellent student.",
                "The _____ student always wanted to know more.",
                "His _____ mind led him to make many discoveries.",
                "The _____ reporter asked probing questions.",
                "She had an _____ personality that loved learning.",
                "The _____ scientist investigated every possibility.",
                "His _____ approach helped him understand complex topics.",
                "The _____ explorer wanted to see what lay beyond.",
                "She showed an _____ interest in how things worked."
            ]
        elif "insatiable" in word_lower:
            adj_sentences = [
                "He had an _____ appetite for adventure and excitement.",
                "Her _____ curiosity led her to read hundreds of books.",
                "The _____ desire for knowledge drove him to study constantly.",
                "She had an _____ hunger for learning new things.",
                "His _____ thirst for success made him work day and night.",
                "The _____ need for attention made him behave badly.",
                "She showed an _____ interest in collecting stamps.",
                "His _____ love of chocolate meant he could never have enough.",
                "The _____ demand for the new toy made it sell out quickly.",
                "She had an _____ passion for music that never faded."
            ]
        elif "insidious" in word_lower:
            adj_sentences = [
                "The _____ disease spread without anyone noticing.",
                "She warned them about the _____ nature of the problem.",
                "The _____ influence of bad habits was hard to detect.",
                "His _____ plan worked slowly but effectively.",
                "The _____ effects of pollution became clear over time.",
                "She recognised the _____ threat before it was too late.",
                "The _____ propaganda affected people's thinking gradually.",
                "His _____ behaviour undermined the team's trust.",
                "The _____ problem grew worse without anyone realising.",
                "She was aware of the _____ danger lurking beneath the surface."
            ]
        elif "insightful" in word_lower:
            adj_sentences = [
                "Her _____ comments added depth to the discussion.",
                "The _____ analysis helped everyone understand the problem.",
                "His _____ observations revealed important truths.",
                "The _____ teacher helped students see things differently.",
                "She made an _____ remark that changed everyone's perspective.",
                "The _____ book provided new ways of thinking.",
                "His _____ questions led to important discoveries.",
                "The _____ advice helped her make better decisions.",
                "She showed an _____ understanding of human nature.",
                "The _____ comment revealed what others had missed."
            ]
        elif "insignificant" in word_lower:
            adj_sentences = [
                "The difference in price was _____ and didn't matter.",
                "She felt her contribution was _____ compared to others.",
                "The _____ detail turned out to be crucial later.",
                "His _____ mistake caused major problems.",
                "The _____ amount of rain didn't help the drought.",
                "She thought the problem was _____ but it grew worse.",
                "The _____ change made a huge difference in the end.",
                "His _____ role became important as the story developed.",
                "The _____ error led to a complete system failure.",
                "She realised that no detail was truly _____."
            ]
        elif "insistent" in word_lower:
            adj_sentences = [
                "He was _____ that we follow the rules exactly.",
                "The _____ knocking at the door wouldn't stop.",
                "She was _____ about finishing her homework before playing.",
                "The _____ demands of the job were exhausting.",
                "His _____ questions made everyone uncomfortable.",
                "The _____ ringing of the phone interrupted their meal.",
                "She remained _____ that she was telling the truth.",
                "The _____ pressure to succeed was overwhelming.",
                "His _____ nature meant he never gave up easily.",
                "The _____ need for attention made him disruptive."
            ]
        elif "insolent" in word_lower:
            adj_sentences = [
                "The _____ student was sent to the headteacher.",
                "His _____ behaviour shocked everyone in the room.",
                "The _____ remark offended all who heard it.",
                "She was punished for her _____ attitude towards the teacher.",
                "The _____ child refused to follow any instructions.",
                "His _____ response showed complete disrespect.",
                "The _____ comment was completely inappropriate.",
                "She couldn't believe his _____ behaviour.",
                "The _____ teenager was grounded for a week.",
                "His _____ manner made him very unpopular."
            ]
        elif "instructive" in word_lower:
            adj_sentences = [
                "The museum visit was very _____ and educational.",
                "Her _____ comments helped everyone understand better.",
                "The _____ book taught valuable life lessons.",
                "His _____ approach made learning enjoyable.",
                "The _____ video explained the process clearly.",
                "She found the experience _____ and helpful.",
                "The _____ lesson covered all the important points.",
                "His _____ guidance was much appreciated.",
                "The _____ workshop taught practical skills.",
                "She made the presentation _____ and interesting."
            ]
        elif "insufferable" in word_lower:
            adj_sentences = [
                "His _____ arrogance annoyed everyone around him.",
                "The _____ heat made it impossible to work.",
                "She found his _____ attitude completely unbearable.",
                "The _____ noise from the construction site drove her mad.",
                "His _____ behaviour made him very unpopular.",
                "The _____ delay caused everyone to miss their appointments.",
                "She couldn't stand his _____ boasting any longer.",
                "The _____ smell made everyone leave the room.",
                "His _____ rudeness shocked everyone.",
                "The _____ situation seemed to have no solution."
            ]
        elif "insurmountable" in word_lower:
            adj_sentences = [
                "The challenge seemed _____ at first, but they persevered.",
                "She faced what appeared to be an _____ obstacle.",
                "The _____ problem required creative thinking to solve.",
                "His _____ determination helped him overcome the difficulty.",
                "The _____ wall blocked their path completely.",
                "She refused to accept that the problem was _____.",
                "The _____ odds didn't stop them from trying.",
                "His _____ courage inspired others to continue.",
                "The _____ barrier seemed impossible to cross.",
                "She found a way around the _____ challenge."
            ]
        elif "intangible" in word_lower:
            adj_sentences = [
                "Love is an _____ but powerful emotion.",
                "The _____ benefits of exercise are important too.",
                "She felt an _____ connection with the place.",
                "The _____ quality of happiness is hard to measure.",
                "His _____ sense of unease grew stronger.",
                "The _____ value of friendship cannot be calculated.",
                "She experienced an _____ feeling of peace.",
                "The _____ atmosphere of the room was calming.",
                "His _____ influence affected everyone around him.",
                "The _____ nature of trust makes it precious."
            ]
        elif "integral" in word_lower:
            adj_sentences = [
                "Hard work is _____ to success in any field.",
                "The _____ part of the machine was missing.",
                "She was an _____ member of the team.",
                "The _____ component couldn't be replaced easily.",
                "His role was _____ to the project's completion.",
                "The _____ nature of the problem required immediate attention.",
                "She played an _____ role in organising the event.",
                "The _____ connection between the parts was crucial.",
                "His contribution was _____ to their victory.",
                "The _____ importance of education cannot be overstated."
            ]
        elif "intermittent" in word_lower:
            adj_sentences = [
                "The _____ rain made planning the picnic difficult.",
                "She heard _____ sounds coming from the next room.",
                "The _____ signal made the phone call frustrating.",
                "His _____ attendance at school worried his teachers.",
                "The _____ power cuts disrupted their work.",
                "She experienced _____ headaches throughout the week.",
                "The _____ noise kept waking her up.",
                "His _____ interest in the subject was concerning.",
                "The _____ service made the journey unreliable.",
                "She noticed _____ flashes of light in the distance."
            ]
        elif "intractable" in word_lower:
            adj_sentences = [
                "The _____ problem required a creative solution.",
                "She found the situation completely _____.",
                "The _____ child refused to cooperate.",
                "His _____ attitude made compromise impossible.",
                "The _____ issue seemed to have no solution.",
                "She faced an _____ challenge that tested her patience.",
                "The _____ nature of the problem frustrated everyone.",
                "His _____ behaviour made him difficult to work with.",
                "The _____ dispute lasted for many years.",
                "She refused to give up on the _____ case."
            ]
        elif "intrinsic" in word_lower:
            adj_sentences = [
                "Hard work has _____ value beyond the rewards.",
                "The _____ beauty of the place was undeniable.",
                "She believed in the _____ worth of every person.",
                "The _____ nature of the problem was complex.",
                "His _____ motivation came from within.",
                "The _____ quality of the material made it valuable.",
                "She recognised the _____ importance of the task.",
                "The _____ value of education extends beyond exams.",
                "His _____ talent was evident from an early age.",
                "The _____ characteristics of the species were fascinating."
            ]
        elif "introspective" in word_lower:
            adj_sentences = [
                "She was an _____ person who enjoyed quiet reflection.",
                "His _____ nature made him seem distant sometimes.",
                "The _____ student spent hours thinking about life.",
                "Her _____ approach helped her understand herself better.",
                "The _____ mood made him thoughtful and quiet.",
                "She had an _____ personality that valued self-awareness.",
                "The _____ character in the book was complex.",
                "His _____ nature led him to write poetry.",
                "The _____ moment helped her make an important decision.",
                "She found the _____ exercise very helpful."
            ]
        elif "intuitive" in word_lower:
            adj_sentences = [
                "He had an _____ understanding of how the machine worked.",
                "Her _____ sense told her something was wrong.",
                "The _____ solution came to her immediately.",
                "His _____ grasp of mathematics impressed his teachers.",
                "She made an _____ decision that proved to be correct.",
                "The _____ approach worked better than the logical one.",
                "His _____ nature helped him read people well.",
                "The _____ feeling guided her through the maze.",
                "She had an _____ ability to solve puzzles quickly.",
                "The _____ answer seemed obvious once she thought about it."
            ]
        elif "invaluable" in word_lower:
            adj_sentences = [
                "Her experience proved _____ during the crisis.",
                "The _____ advice helped him make the right decision.",
                "She found the information _____ for her research.",
                "The _____ support from her friends got her through difficult times.",
                "His _____ contribution to the project was recognised.",
                "The _____ resource was used by students everywhere.",
                "She considered the book _____ for understanding the topic.",
                "The _____ help from volunteers made the event successful.",
                "His _____ knowledge saved them from making a mistake.",
                "The _____ tool made the work much easier."
            ]
        elif "irascible" in word_lower:
            adj_sentences = [
                "The _____ man shouted at everyone who annoyed him.",
                "His _____ temper made him difficult to work with.",
                "The _____ teacher frightened the students.",
                "She avoided the _____ neighbour whenever possible.",
                "His _____ nature meant he argued about everything.",
                "The _____ character in the story was always angry.",
                "She found his _____ behaviour completely unacceptable.",
                "The _____ boss made the workplace unpleasant.",
                "His _____ response surprised everyone.",
                "The _____ customer complained about everything."
            ]
        elif "irrational" in word_lower:
            adj_sentences = [
                "Her _____ fear of spiders began in childhood.",
                "The _____ decision led to disastrous consequences.",
                "His _____ behaviour worried his friends.",
                "The _____ argument made no sense at all.",
                "She realised her _____ thoughts were unfounded.",
                "The _____ fear prevented her from enjoying the trip.",
                "His _____ anger was out of proportion to the situation.",
                "The _____ belief was based on superstition.",
                "She tried to overcome her _____ anxiety.",
                "The _____ response showed a lack of logic."
            ]
        elif "irrelevant" in word_lower:
            adj_sentences = [
                "That information is completely _____ to the discussion.",
                "The _____ comment confused everyone.",
                "His _____ question interrupted the flow of the lesson.",
                "The _____ detail distracted from the main point.",
                "She found the information _____ to her research.",
                "The _____ remark was ignored by everyone.",
                "His _____ argument didn't address the real issue.",
                "The _____ fact was interesting but not useful.",
                "She dismissed the _____ suggestion immediately.",
                "The _____ topic took up valuable time."
            ]
        elif "irreproachable" in word_lower:
            adj_sentences = [
                "Her _____ behaviour earned her the respect of all.",
                "The _____ record showed years of excellent service.",
                "His _____ character made him trustworthy.",
                "The _____ conduct set an example for others.",
                "She maintained an _____ reputation throughout her career.",
                "The _____ standards were difficult to maintain.",
                "His _____ honesty was well-known.",
                "The _____ performance impressed the judges.",
                "She had an _____ record of achievement.",
                "The _____ quality of the work was outstanding."
            ]
        elif "irresolute" in word_lower:
            adj_sentences = [
                "He was _____ about which path to take.",
                "Her _____ attitude made decision-making difficult.",
                "The _____ leader couldn't make up his mind.",
                "His _____ nature caused delays in the project.",
                "The _____ response showed uncertainty.",
                "She felt _____ about accepting the offer.",
                "The _____ approach led to confusion.",
                "His _____ behaviour frustrated everyone.",
                "The _____ decision-making process was slow.",
                "She remained _____ despite having all the information."
            ]
        elif "irreverent" in word_lower:
            adj_sentences = [
                "The _____ comment offended many people.",
                "His _____ attitude towards tradition shocked the elders.",
                "The _____ humour appealed to younger audiences.",
                "She made an _____ remark that caused controversy.",
                "The _____ approach challenged established beliefs.",
                "His _____ behaviour was seen as disrespectful.",
                "The _____ tone of the article angered readers.",
                "She had an _____ sense of humour.",
                "The _____ joke was inappropriate for the occasion.",
                "His _____ comments showed a lack of respect."
            ]
        elif "lucrative" in word_lower:
            adj_sentences = [
                "The _____ business earned millions each year.",
                "She found a _____ opportunity to make money.",
                "The _____ deal was too good to refuse.",
                "His _____ investment paid off handsomely.",
                "The _____ contract secured their future.",
                "She pursued a _____ career in finance.",
                "The _____ venture attracted many investors.",
                "His _____ idea made him wealthy.",
                "The _____ market was highly competitive.",
                "She discovered a _____ way to earn extra income."
            ]
        elif "magnanimous" in word_lower:
            adj_sentences = [
                "The _____ winner praised his opponent graciously.",
                "Her _____ gesture surprised everyone.",
                "The _____ act of forgiveness showed great character.",
                "His _____ nature made him popular.",
                "The _____ decision benefited everyone involved.",
                "She showed a _____ spirit in victory.",
                "The _____ leader shared credit with the team.",
                "His _____ behaviour earned him respect.",
                "The _____ offer was generous and kind.",
                "She had a _____ heart that forgave easily."
            ]
        elif "malevolent" in word_lower:
            adj_sentences = [
                "The _____ witch cast a terrible spell.",
                "His _____ intentions were clear from the start.",
                "The _____ character in the story was truly evil.",
                "She sensed a _____ presence in the old house.",
                "The _____ plan was designed to cause harm.",
                "His _____ smile frightened everyone.",
                "The _____ force seemed to control everything.",
                "She recognised the _____ nature of the threat.",
                "The _____ influence spread throughout the land.",
                "His _____ actions showed his true character."
            ]
        elif "manageable" in word_lower:
            adj_sentences = [
                "The task seemed large but was actually quite _____.",
                "She broke the project into _____ chunks.",
                "The _____ workload allowed time for breaks.",
                "His _____ schedule left room for hobbies.",
                "The _____ size of the class enabled individual attention.",
                "She found the problem _____ with the right approach.",
                "The _____ amount of homework was reasonable.",
                "His _____ expectations were realistic.",
                "The _____ challenge was within their abilities.",
                "She made the difficult task _____ through planning."
            ]
        elif "meditative" in word_lower:
            adj_sentences = [
                "She sat in a _____ pose, thinking deeply about the problem.",
                "The _____ music helped her relax.",
                "His _____ nature made him thoughtful.",
                "The _____ atmosphere of the garden was peaceful.",
                "She found the _____ exercise very calming.",
                "The _____ practice helped her focus.",
                "His _____ approach to life brought inner peace.",
                "The _____ state allowed creative thinking.",
                "She enjoyed the _____ quality of the early morning.",
                "The _____ moment gave her clarity."
            ]
        elif "melancholic" in word_lower:
            adj_sentences = [
                "The _____ music made everyone feel sombre.",
                "Her _____ mood matched the rainy weather.",
                "The _____ poem expressed deep sadness.",
                "His _____ expression showed his unhappiness.",
                "The _____ atmosphere of the old house was haunting.",
                "She felt a _____ sense of loss.",
                "The _____ melody brought tears to her eyes.",
                "His _____ nature made him seem distant.",
                "The _____ story touched everyone's hearts.",
                "She wrote _____ poetry about her experiences."
            ]
        elif "mercenary" in word_lower:
            adj_sentences = [
                "His _____ attitude meant he only cared about profit.",
                "The _____ soldier fought for money, not loyalty.",
                "Her _____ motives were clear to everyone.",
                "The _____ approach prioritised money over principles.",
                "His _____ behaviour showed a lack of values.",
                "The _____ company only cared about making money.",
                "She recognised his _____ intentions immediately.",
                "The _____ nature of the deal was obvious.",
                "His _____ outlook on life was disappointing.",
                "The _____ pursuit of wealth corrupted him."
            ]
        elif "methodical" in word_lower:
            adj_sentences = [
                "She approached the problem in a _____ way, step by step.",
                "The _____ worker completed tasks efficiently.",
                "His _____ nature made him reliable.",
                "The _____ approach ensured nothing was missed.",
                "She had a _____ system for organising her notes.",
                "The _____ process took time but produced good results.",
                "His _____ planning prevented mistakes.",
                "The _____ investigation uncovered all the facts.",
                "She followed a _____ routine every morning.",
                "The _____ method was slow but thorough."
            ]
        elif "meticulous" in word_lower:
            adj_sentences = [
                "Her _____ work impressed everyone.",
                "The _____ attention to detail was remarkable.",
                "His _____ planning ensured success.",
                "The _____ craftsman took pride in his work.",
                "She was _____ about checking every detail.",
                "The _____ preparation paid off in the end.",
                "His _____ nature made him perfect for the job.",
                "The _____ examination revealed the truth.",
                "She showed _____ care in her research.",
                "The _____ approach left no room for error."
            ]
        elif "mischievous" in word_lower:
            adj_sentences = [
                "The _____ puppy chewed up the slippers.",
                "Her _____ grin showed she was up to something.",
                "The _____ child played harmless pranks.",
                "His _____ behaviour was annoying but not harmful.",
                "The _____ look in her eyes warned of trouble.",
                "She had a _____ sense of humour.",
                "The _____ student disrupted the class playfully.",
                "His _____ nature made him fun to be around.",
                "The _____ cat knocked things off the shelf.",
                "She couldn't help her _____ curiosity."
            ]
        elif "monochrome" in word_lower:
            adj_sentences = [
                "The old photograph was in _____, showing only shades of grey.",
                "She preferred _____ images to colourful ones.",
                "The _____ painting had a dramatic effect.",
                "His _____ design was elegant and simple.",
                "The _____ television showed programmes in black and white.",
                "She created a _____ artwork using only charcoal.",
                "The _____ scheme gave the room a modern look.",
                "His _____ photography captured mood beautifully.",
                "The _____ print was striking despite lacking colour.",
                "She loved the _____ aesthetic of the old films."
            ]
        elif "monotonous" in word_lower:
            adj_sentences = [
                "The _____ work made the day drag slowly.",
                "Her _____ voice put everyone to sleep.",
                "The _____ routine became boring after a while.",
                "His _____ speech lacked any excitement.",
                "The _____ landscape stretched for miles.",
                "She found the _____ task very tedious.",
                "The _____ sound of the machine was annoying.",
                "His _____ lifestyle needed more variety.",
                "The _____ repetition made her lose interest.",
                "She tried to break the _____ pattern."
            ]
        elif "nonchalant" in word_lower:
            adj_sentences = [
                "He seemed _____ about the difficult exam.",
                "Her _____ attitude surprised everyone.",
                "The _____ response showed no concern.",
                "His _____ manner hid his true feelings.",
                "The _____ shrug indicated he didn't care.",
                "She appeared _____ despite the pressure.",
                "The _____ comment seemed dismissive.",
                "His _____ behaviour was unexpected.",
                "The _____ approach seemed careless.",
                "She tried to act _____ but was actually nervous."
            ]
        elif "nonplussed" in word_lower:
            adj_sentences = [
                "She was _____ by his unexpected question.",
                "The _____ expression showed complete confusion.",
                "His _____ reaction surprised everyone.",
                "The _____ student didn't know how to respond.",
                "She felt _____ by the strange situation.",
                "The _____ look on his face was amusing.",
                "His _____ state made him speechless.",
                "The _____ response showed he was lost for words.",
                "She was completely _____ by the turn of events.",
                "The _____ silence lasted for several minutes."
            ]
        elif "noteworthy" in word_lower:
            adj_sentences = [
                "His achievement was particularly _____ given his age.",
                "The _____ performance earned her a standing ovation.",
                "The _____ discovery changed scientific understanding.",
                "Her _____ contribution was recognised by all.",
                "The _____ accomplishment impressed everyone.",
                "She made a _____ improvement in her grades.",
                "The _____ event was reported in the news.",
                "His _____ talent was evident from the start.",
                "The _____ achievement deserved celebration.",
                "She received recognition for her _____ work."
            ]
        elif "obligatory" in word_lower:
            adj_sentences = [
                "Wearing a helmet is _____ when cycling.",
                "The _____ attendance at the meeting was required.",
                "Her _____ duties included supervising the students.",
                "The _____ course had to be completed by everyone.",
                "His _____ role was to ensure safety.",
                "The _____ requirement couldn't be avoided.",
                "She found the _____ task tedious but necessary.",
                "The _____ procedure had to be followed exactly.",
                "His _____ presence was needed for the vote.",
                "The _____ nature of the task made it important."
            ]
        else:
            # Generic adjective sentences
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
                f"The _____ garden attracted many visitors."
            ]
        
        for sent in adj_sentences:
            if len(sentences) < 10:
                blank_sent = create_blank_sentence(sent, word)
                if blank_sent and "_____" in blank_sent and blank_sent not in sentences:
                    sentences.append(blank_sent)
    
    else:
        # Noun sentences
        noun_sentences = []  # Initialize to avoid UnboundLocalError
        
        if "ineptitude" in word_lower:
            noun_sentences = [
                "His _____ with technology was well known.",
                "The _____ of the team led to their failure.",
                "She was frustrated by his _____ in basic tasks.",
                "The _____ became obvious during the test.",
                "His _____ with numbers made maths difficult.",
                "The _____ of the plan was clear from the start.",
                "She couldn't believe his _____ in such simple matters.",
                "The _____ showed a lack of proper training.",
                "His _____ was a source of constant problems.",
                "The _____ became apparent when things went wrong."
            ]
        elif "inequity" in word_lower:
            noun_sentences = [
                "The _____ in pay between men and women must be addressed.",
                "She fought against the _____ in the system.",
                "The _____ of the situation angered everyone.",
                "His speech highlighted the _____ in society.",
                "The _____ became clear when comparing the results.",
                "She worked to eliminate the _____ in education.",
                "The _____ was obvious to all who looked closely.",
                "His research exposed the _____ in healthcare.",
                "The _____ needed to be corrected immediately.",
                "She couldn't accept the _____ any longer."
            ]
        elif "inference" in word_lower:
            noun_sentences = [
                "Her _____ from the data proved to be correct.",
                "The _____ was based on careful observation.",
                "His _____ about what happened was accurate.",
                "The _____ drawn from the evidence was logical.",
                "She made an _____ that surprised everyone.",
                "The _____ helped solve the mystery.",
                "His _____ was supported by the facts.",
                "The _____ led to an important discovery.",
                "She based her decision on a logical _____.",
                "The _____ seemed reasonable given the circumstances."
            ]
        elif "inhabitant" in word_lower:
            noun_sentences = [
                "The island had fewer than a hundred _____.",
                "Each _____ of the village knew everyone else.",
                "The _____ of the town were friendly and welcoming.",
                "She was a long-time _____ of the area.",
                "The _____ of the building complained about the noise.",
                "Every _____ had a story to tell.",
                "The _____ of the remote village lived simply.",
                "She became an _____ of the city after moving.",
                "The _____ of the island were self-sufficient.",
                "Each _____ contributed to the community."
            ]
        elif "innovation" in word_lower:
            noun_sentences = [
                "The smartphone was one of the greatest _____.",
                "Her _____ revolutionised the industry.",
                "The _____ changed how people worked.",
                "His _____ solved a major problem.",
                "The _____ was welcomed by everyone.",
                "She was known for her creative _____.",
                "The _____ improved efficiency dramatically.",
                "His _____ earned him recognition.",
                "The _____ transformed daily life.",
                "She introduced an _____ that became standard."
            ]
        elif "insurgent" in word_lower:
            noun_sentences = [
                "The _____ fought against the government forces.",
                "The _____ were determined to bring change.",
                "His role as an _____ was dangerous.",
                "The _____ organised secretly to avoid detection.",
                "She learned about the _____ from history books.",
                "The _____ had strong support from the people.",
                "His actions as an _____ were controversial.",
                "The _____ fought for their beliefs.",
                "She studied the _____ movement in detail.",
                "The _____ were eventually defeated."
            ]
        elif "intimidation" in word_lower or "intimidate" in word_lower:
            # Handle as verb above
            noun_sentences = []  # Skip - handled as verb
        elif "intuition" in word_lower:
            noun_sentences = [
                "Her _____ told her something was wrong.",
                "The _____ proved to be correct.",
                "His _____ guided him through the maze.",
                "The _____ was stronger than logic sometimes.",
                "She trusted her _____ in making decisions.",
                "The _____ helped her avoid danger.",
                "His _____ about people was usually accurate.",
                "The _____ came from years of experience.",
                "She followed her _____ rather than the evidence.",
                "The _____ led her to the right answer."
            ]
        elif "isolation" in word_lower:
            noun_sentences = [
                "The _____ of the remote island made it peaceful.",
                "She felt a sense of _____ after moving away.",
                "The _____ from friends was difficult.",
                "His _____ was self-imposed but necessary.",
                "The _____ helped her focus on her work.",
                "She struggled with the _____ of living alone.",
                "The _____ of the mountain cabin appealed to him.",
                "His _____ from the group was temporary.",
                "The _____ gave her time to think.",
                "She found peace in the _____ of nature."
            ]
        elif "justification" in word_lower:
            noun_sentences = [
                "There was no _____ for his rude behaviour.",
                "The _____ for the decision was clear.",
                "Her _____ seemed reasonable to everyone.",
                "The _____ didn't convince the judge.",
                "He provided a strong _____ for his actions.",
                "The _____ was accepted by all.",
                "She couldn't find any _____ for the mistake.",
                "The _____ explained everything clearly.",
                "His _____ was weak and unconvincing.",
                "The _____ satisfied everyone's concerns."
            ]
        elif "listlessness" in word_lower:
            noun_sentences = [
                "The hot weather caused a feeling of _____ among the students.",
                "Her _____ made it hard to concentrate.",
                "The _____ was due to lack of sleep.",
                "His _____ worried his parents.",
                "The _____ affected everyone's productivity.",
                "She tried to overcome her _____ with exercise.",
                "The _____ made the day seem longer.",
                "His _____ was a sign of boredom.",
                "The _____ disappeared after a good rest.",
                "She felt a sense of _____ after the long journey."
            ]
        elif "litigation" in word_lower:
            noun_sentences = [
                "The company faced expensive _____ after the accident.",
                "The _____ lasted for several years.",
                "Her involvement in the _____ was stressful.",
                "The _____ was settled out of court.",
                "His _____ against the company was successful.",
                "The _____ process was complicated and lengthy.",
                "She avoided _____ by reaching an agreement.",
                "The _____ cost both sides a lot of money.",
                "His _____ was necessary to protect his rights.",
                "The _____ finally came to an end."
            ]
        elif "luminary" in word_lower:
            noun_sentences = [
                "The scientist was a _____ in the field of physics.",
                "She became a _____ in the world of literature.",
                "The _____ inspired generations of students.",
                "His status as a _____ was well-deserved.",
                "The _____ gave a fascinating lecture.",
                "She met the _____ at a conference.",
                "The _____'s work changed the field forever.",
                "His reputation as a _____ grew over time.",
                "The _____ was honoured for lifetime achievement.",
                "She aspired to become a _____ in her field."
            ]
        elif "malapropism" in word_lower:
            noun_sentences = [
                "Saying 'dance a flamingo' instead of 'dance a flamenco' is a _____.",
                "Her frequent _____ made everyone laugh.",
                "The _____ showed her confusion with words.",
                "His _____ was unintentionally funny.",
                "The _____ revealed a misunderstanding.",
                "She was known for her amusing _____.",
                "The _____ confused everyone in the room.",
                "His _____ became a running joke.",
                "The _____ was quickly corrected.",
                "She made a _____ that everyone noticed."
            ]
        elif "masculinity" in word_lower:
            noun_sentences = [
                "The film explored different ideas of _____.",
                "His traditional view of _____ was outdated.",
                "The _____ portrayed in the story was complex.",
                "She wrote about changing concepts of _____.",
                "The _____ shown in the character was admirable.",
                "His understanding of _____ evolved over time.",
                "The _____ in the film challenged stereotypes.",
                "She discussed _____ in her research paper.",
                "The _____ displayed was both strong and gentle.",
                "His _____ was not defined by aggression."
            ]
        elif "materialism" in word_lower:
            noun_sentences = [
                "His _____ led him to care more about money than friendships.",
                "The _____ of modern society worried her.",
                "The _____ was evident in his behaviour.",
                "She rejected the _____ of her peers.",
                "The _____ made people forget what mattered.",
                "His _____ blinded him to true happiness.",
                "The _____ of the culture was concerning.",
                "She wrote about the dangers of _____.",
                "The _____ affected everyone around him.",
                "His _____ was a source of conflict."
            ]
        elif "mediocrity" in word_lower:
            noun_sentences = [
                "He refused to accept _____ and always strived for excellence.",
                "The _____ of the work was disappointing.",
                "Her _____ was due to lack of effort.",
                "The _____ became obvious when compared to others.",
                "His _____ frustrated his teachers.",
                "The _____ was not acceptable for the project.",
                "She worked hard to avoid _____.",
                "The _____ showed a lack of commitment.",
                "His _____ was a choice, not a limitation.",
                "The _____ needed to be addressed immediately."
            ]
        elif "melancholy" in word_lower:
            noun_sentences = [
                "A _____ mood settled over her after the news.",
                "The _____ of the music matched her feelings.",
                "His _____ was evident in his poetry.",
                "The _____ made the day seem darker.",
                "She felt a deep sense of _____.",
                "The _____ was temporary but intense.",
                "His _____ inspired his best writing.",
                "The _____ lifted after she talked to friends.",
                "She couldn't shake the feeling of _____.",
                "The _____ was a natural response to loss."
            ]
        elif "misanthrope" in word_lower:
            noun_sentences = [
                "The _____ preferred the company of animals to people.",
                "His reputation as a _____ was well-known.",
                "The _____ avoided social gatherings completely.",
                "She wondered if he was truly a _____ or just shy.",
                "The _____'s dislike of people was obvious.",
                "His _____ made him difficult to be around.",
                "The _____ found solace in solitude.",
                "She tried to understand the _____'s perspective.",
                "The _____'s views were extreme but consistent.",
                "His _____ was a defence mechanism."
            ]
        elif "misogynist" in word_lower:
            noun_sentences = [
                "His _____ views made him unpopular with his female colleagues.",
                "The _____'s comments were completely unacceptable.",
                "The _____ refused to work with women.",
                "She recognised the _____ immediately.",
                "The _____'s attitude belonged in the past.",
                "His _____ was evident in everything he said.",
                "The _____ was removed from his position.",
                "She wouldn't tolerate the _____'s behaviour.",
                "The _____'s views were outdated and wrong.",
                "His _____ made the workplace uncomfortable."
            ]
        elif "monochrome" in word_lower:
            # Handle as adjective above
            noun_sentences = []  # Skip - handled as adjective
        elif "munificence" in word_lower:
            noun_sentences = [
                "The _____ of the donor helped build the new library.",
                "Her _____ was legendary in the community.",
                "The _____ shown was truly remarkable.",
                "His _____ helped many people in need.",
                "The _____ of the gift surprised everyone.",
                "She was known for her _____ towards charities.",
                "The _____ made a real difference.",
                "His _____ was appreciated by all.",
                "The _____ was unexpected but welcome.",
                "She showed great _____ in her donations."
            ]
        elif "narrative" in word_lower:
            noun_sentences = [
                "The _____ follows a young hero's journey.",
                "Her _____ was engaging and well-written.",
                "The _____ of the film was complex.",
                "His _____ told an important story.",
                "The _____ unfolded slowly but beautifully.",
                "She crafted a compelling _____.",
                "The _____ had unexpected twists.",
                "His _____ captured everyone's attention.",
                "The _____ was both entertaining and meaningful.",
                "She wove an intricate _____."
            ]
        elif "nobility" in word_lower:
            noun_sentences = [
                "She showed great _____ in forgiving those who had wronged her.",
                "The _____ of his character was evident.",
                "The _____ of the act impressed everyone.",
                "His _____ set an example for others.",
                "The _____ shown was truly admirable.",
                "She displayed _____ in difficult circumstances.",
                "The _____ of her spirit was inspiring.",
                "His _____ earned him respect.",
                "The _____ was a mark of true character.",
                "She possessed a natural _____."
            ]
        elif "nonentity" in word_lower:
            noun_sentences = [
                "He felt like a _____ in the large company.",
                "The _____ was ignored by everyone.",
                "Her role as a _____ frustrated her.",
                "The _____ had no influence whatsoever.",
                "He refused to remain a _____.",
                "The _____'s opinion didn't matter.",
                "She worked hard to avoid being a _____.",
                "The _____ was completely overlooked.",
                "His status as a _____ was temporary.",
                "She wouldn't accept being treated as a _____."
            ]
        elif "nouveau-riche" in word_lower:
            noun_sentences = [
                "The _____ family tried to fit in with the established elite.",
                "The _____ were often looked down upon.",
                "Her status as _____ was obvious from her behaviour.",
                "The _____ spent money extravagantly.",
                "His _____ background was a source of pride.",
                "The _____ tried too hard to impress.",
                "She was considered _____ by the old families.",
                "The _____'s wealth was newly acquired.",
                "His _____ status made him an outsider.",
                "The _____ family lacked the refinement of old money."
            ]
        elif "nurseryman" in word_lower:
            noun_sentences = [
                "The _____ helped us choose the best plants for our garden.",
                "The _____ knew everything about growing flowers.",
                "Her father was a skilled _____.",
                "The _____'s advice was invaluable.",
                "He worked as a _____ for thirty years.",
                "The _____ showed us how to care for the plants.",
                "Her expertise as a _____ was well-known.",
                "The _____ grew the most beautiful roses.",
                "He learned the trade from an experienced _____.",
                "The _____'s garden was a work of art."
            ]
        else:
            # Generic noun sentences
            noun_sentences = [
                f"The _____ was clear from the context.",
                f"She showed great _____ in the situation.",
                f"His _____ surprised everyone around him.",
                f"The _____ became evident as the story unfolded.",
                f"They demonstrated _____ throughout the challenge.",
                f"Her _____ was obvious to all who watched.",
                f"The situation required _____ from everyone involved.",
                f"His _____ made a significant difference.",
                f"The _____ was apparent in their actions.",
                f"She expressed _____ in her response."
            ]
        
        if noun_sentences:  # Only process if noun_sentences is not empty
            for sent in noun_sentences:
                if len(sentences) < 10:
                    blank_sent = create_blank_sentence(sent, word)
                    if blank_sent and "_____" in blank_sent and blank_sent not in sentences:
                        sentences.append(blank_sent)
    
    # Fill up to 10 sentences if needed
    while len(sentences) < 10:
        # Create additional contextually appropriate sentences
        if is_verb:
            additional = f"Everyone agreed they needed to _____ before the deadline."
        elif is_adjective:
            additional = f"The _____ quality of the work impressed the judges."
        else:
            additional = f"The importance of the _____ could not be overstated."
        
        blank_additional = create_blank_sentence(additional, word)
        if blank_additional and "_____" in blank_additional and blank_additional not in sentences:
            sentences.append(blank_additional)
        else:
            break
    
    return sentences[:10]


def main():
    """Main function to generate quiz sentences"""
    input_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level4_batch3.txt")
    output_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level4_batch3.csv")
    
    # Read input file
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
    
    # Generate sentences and write to CSV
    total_sentences = 0
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['level', 'word', 'sentence'])
        
        for word, meaning, example, synonym, antonym in words_data:
            sentences = generate_quiz_sentences(word, meaning, example, synonym, antonym)
            for sentence in sentences:
                writer.writerow(['4', word, sentence])
                total_sentences += 1
    
    print(f"Level 4 Batch 3 complete: {total_sentences} sentences")


if __name__ == "__main__":
    main()
