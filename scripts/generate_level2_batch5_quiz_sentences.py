#!/usr/bin/env python3
"""
Generate high-quality quiz sentences for Level 2 Batch 5 vocabulary words.
Creates 10 contextually rich sentences per word with strong contextual clues.
"""

import csv
import re
from pathlib import Path


def create_blank_sentence(sentence: str, word: str) -> str:
    """Replace the word in a sentence with _____."""
    # Case-insensitive replacement
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    return pattern.sub("_____", sentence)


def generate_sentences_for_word(word: str, meaning: str, example: str, synonym: str, antonym: str) -> list:
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
        "having", "showing", "expressing", "characterised by", "characterized by",
        "very", "extremely", "slightly", "not", "belonging to", "relating to"
    ])
    is_noun = not is_verb and not is_adjective
    
    # 1. Use example sentence if available
    if example:
        blank_example = create_blank_sentence(example, word)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # Generate contextually rich sentences based on word meaning
    # Each word gets custom sentences that demonstrate its specific meaning
    
    word_sentences = {
        "risqué": [
            "The comedian's _____ jokes were not suitable for the school assembly.",
            "Her parents asked her to avoid watching _____ programmes on television.",
            "The _____ content in the film meant it wasn't appropriate for children.",
            "He felt uncomfortable telling such a _____ story in front of his teachers.",
            "The _____ humour made some audience members leave the theatre.",
            "She was shocked by the _____ nature of the conversation.",
            "The _____ magazine was kept on the top shelf away from children.",
            "His _____ comments embarrassed everyone at the family gathering.",
            "The teacher explained why _____ language wasn't allowed in school.",
            "The _____ scene in the play was edited out for the school performance."
        ],
        "rueful": [
            "She gave a _____ smile after realising she had forgotten her homework.",
            "His _____ expression showed he regretted breaking his friend's toy.",
            "The _____ look on his face revealed he knew he had made a mistake.",
            "She felt _____ about not studying harder for the important test.",
            "His _____ apology showed he truly understood what he had done wrong.",
            "The _____ tone in her voice indicated she wished she had listened to advice.",
            "He wore a _____ expression after losing the game through his own error.",
            "Her _____ glance at the broken vase showed her regret.",
            "The _____ way he spoke suggested he had learned from his mistake.",
            "She looked _____ when she realised she had hurt her friend's feelings."
        ],
        "ruffian": [
            "The _____ was arrested by the police for causing trouble in the park.",
            "Everyone avoided the _____ who was known for starting fights.",
            "The _____ intimidated the younger children with his aggressive behaviour.",
            "She was frightened when the _____ approached her in the dark alley.",
            "The _____ vandalised the school playground during the night.",
            "His reputation as a _____ made other pupils avoid him.",
            "The _____ was caught stealing from the local shop.",
            "Nobody wanted to sit near the _____ who disrupted every lesson.",
            "The _____ threatened the shopkeeper when he was asked to leave.",
            "The police warned the _____ about his violent behaviour."
        ],
        "rummage": [
            "She had to _____ through her school bag to find her missing pen.",
            "He began to _____ in the drawer looking for his lost key.",
            "The children were told to _____ through the toy box to find their favourite game.",
            "She started to _____ through the wardrobe searching for her uniform.",
            "He had to _____ through piles of papers to locate the important document.",
            "The detective began to _____ through the suspect's belongings.",
            "She decided to _____ through the charity shop for second-hand books.",
            "He had to _____ through his pockets to find enough change for the bus.",
            "The children loved to _____ through the treasure chest at the school fair.",
            "She began to _____ through the library shelves looking for her book."
        ],
        "rupture": [
            "The old pipe began to _____ under the extreme pressure.",
            "The balloon would _____ if they continued to inflate it further.",
            "The dam threatened to _____ after days of heavy rainfall.",
            "The doctor warned that the injury could _____ if not treated properly.",
            "The tyre began to _____ when it hit the sharp object on the road.",
            "The water main would _____ if the pressure wasn't reduced immediately.",
            "The seam of her dress started to _____ during the performance.",
            "The container would _____ if they didn't release some of the pressure.",
            "The old hose began to _____ after years of use in the garden.",
            "The doctor explained how the muscle could _____ during strenuous exercise."
        ],
        "sarcasm": [
            "Her _____ was lost on those who didn't understand irony.",
            "He used _____ to make his point about the unfair situation.",
            "The teacher's _____ confused the pupils who took her words literally.",
            "She couldn't tell if he was being serious or using _____.",
            "His _____ made everyone laugh except those who didn't understand it.",
            "The _____ in her voice was obvious to everyone who knew her well.",
            "He replied with heavy _____ when asked about his test results.",
            "The _____ in his comment was so subtle that many people missed it.",
            "She was known for her sharp _____ and quick wit.",
            "His _____ was misunderstood and caused offence unintentionally."
        ],
        "savoury": [
            "She preferred _____ snacks like crisps and cheese to sweet treats.",
            "The _____ pie was filled with meat and vegetables rather than fruit.",
            "He chose the _____ option from the menu instead of dessert.",
            "The _____ biscuits were perfect for serving with soup.",
            "She made _____ pancakes with cheese and ham for breakfast.",
            "The _____ flavour of the soup appealed to his taste buds.",
            "He enjoyed _____ foods much more than sugary sweets.",
            "The _____ smell of the roast dinner filled the kitchen.",
            "She packed _____ sandwiches for the picnic instead of cakes.",
            "The _____ taste of the sauce complemented the meat perfectly."
        ],
        "scenic": [
            "They took the _____ route through the mountains to enjoy the views.",
            "The _____ countryside was perfect for their weekend walk.",
            "She painted a picture of the _____ landscape she had visited.",
            "The _____ drive along the coast was breathtaking.",
            "They stopped at a _____ viewpoint to take photographs.",
            "The _____ beauty of the lake attracted many visitors.",
            "He chose the _____ path through the forest for their hike.",
            "The _____ railway journey passed through beautiful valleys.",
            "She described the _____ route they had taken on their holiday.",
            "The _____ overlook provided stunning views of the valley below."
        ],
        "secular": [
            "The _____ school did not include religious education in its curriculum.",
            "The _____ government separated church and state completely.",
            "She preferred _____ music to hymns during the ceremony.",
            "The _____ organisation welcomed people of all faiths and none.",
            "He attended a _____ university that had no religious affiliation.",
            "The _____ celebration focused on community rather than religion.",
            "She worked for a _____ charity that helped people regardless of belief.",
            "The _____ approach meant everyone felt included regardless of faith.",
            "He enjoyed the _____ nature of the school's celebrations.",
            "The _____ event brought together people from different backgrounds."
        ],
        "serene": [
            "The _____ lake reflected the mountains perfectly in its calm waters.",
            "She found the _____ garden a perfect place to read quietly.",
            "The _____ atmosphere in the library helped her concentrate.",
            "He felt _____ after spending time in the peaceful countryside.",
            "The _____ expression on her face showed she was at peace.",
            "They enjoyed the _____ beauty of the sunset over the sea.",
            "The _____ music helped create a calm atmosphere.",
            "She described the _____ feeling she had while watching the sunrise.",
            "The _____ morning was perfect for a quiet walk.",
            "He found the _____ setting ideal for meditation and reflection."
        ],
        "servile": [
            "His _____ behaviour towards his boss embarrassed his colleagues.",
            "She found his _____ attitude difficult to respect.",
            "The _____ way he followed orders without question worried her.",
            "He was criticised for being too _____ and not standing up for himself.",
            "Her _____ manner made others feel uncomfortable.",
            "The _____ employee never questioned unfair treatment.",
            "He showed a _____ willingness to do anything asked of him.",
            "The _____ nature of his response suggested he lacked confidence.",
            "She was concerned about his _____ acceptance of poor working conditions.",
            "His _____ behaviour made it clear he was afraid to speak his mind."
        ],
        "severe": [
            "The _____ weather caused school closures across the county.",
            "She received a _____ warning about her behaviour from the headteacher.",
            "The _____ storm damaged many buildings in the area.",
            "He faced _____ consequences for breaking the school rules.",
            "The _____ winter made it difficult to travel anywhere.",
            "She gave him a _____ look that made him stop immediately.",
            "The _____ punishment seemed harsh but was necessary.",
            "He suffered _____ injuries in the accident and needed hospital treatment.",
            "The _____ drought caused crops to fail across the region.",
            "She was known for her _____ but fair approach to discipline."
        ],
        "shallow": [
            "The _____ water was warm and perfect for paddling.",
            "Her _____ understanding of the topic became obvious during the discussion.",
            "The _____ end of the pool was safe for young children.",
            "He realised his knowledge was too _____ to answer the difficult question.",
            "The _____ stream was easy to cross without getting wet.",
            "She was criticised for her _____ analysis of the complex problem.",
            "The _____ dish was perfect for serving the appetiser.",
            "His _____ breathing indicated he was feeling anxious.",
            "The _____ conversation didn't address any important issues.",
            "They waded through the _____ water to reach the other side."
        ],
        "shrewd": [
            "The _____ businessman made excellent deals that benefited everyone.",
            "Her _____ observation helped solve the mystery quickly.",
            "The _____ detective noticed details others had missed.",
            "He made a _____ decision that saved the company money.",
            "The _____ student always knew the right questions to ask.",
            "She showed _____ judgement in choosing her friends carefully.",
            "The _____ negotiator reached an agreement that satisfied both sides.",
            "His _____ understanding of people helped him succeed.",
            "The _____ teacher knew exactly how to motivate her pupils.",
            "She made a _____ choice that proved to be exactly right."
        ],
        "shrill": [
            "The _____ sound of the fire alarm woke everyone immediately.",
            "Her _____ voice could be heard above all the other noise.",
            "The _____ whistle signalled the end of the match.",
            "He covered his ears at the _____ noise from the machinery.",
            "The _____ cry of the bird echoed across the valley.",
            "She let out a _____ scream when she saw the spider.",
            "The _____ tone of her voice showed she was very upset.",
            "The _____ alarm continued until someone turned it off.",
            "His _____ laughter was unpleasant to listen to.",
            "The _____ sound of the brakes made everyone jump."
        ],
        "simile": [
            "\"As brave as a lion\" is an example of a _____.",
            "The teacher explained that a _____ compares two things using 'like' or 'as'.",
            "She wrote a beautiful _____ comparing clouds to cotton wool.",
            "The _____ helped the reader picture the scene more clearly.",
            "He struggled to understand the difference between a _____ and a metaphor.",
            "The _____ made the description more vivid and interesting.",
            "She used a _____ to describe how fast the runner moved.",
            "The _____ \"as cold as ice\" helped describe the winter weather.",
            "He wrote a _____ comparing the moon to a silver coin.",
            "The _____ added colour and interest to her creative writing."
        ],
        "slacken": [
            "The wind began to _____ as the storm moved away.",
            "She felt the rope _____ slightly as the weight decreased.",
            "The rain started to _____ after hours of heavy downpour.",
            "He noticed his grip _____ as he grew tired.",
            "The teacher's strict rules began to _____ as term progressed.",
            "The tension in the room began to _____ after the good news.",
            "She felt the pressure _____ once the deadline passed.",
            "The speed of the car began to _____ as they approached the junction.",
            "His enthusiasm began to _____ after several setbacks.",
            "The tight knot started to _____ after being in water."
        ],
        "slander": [
            "She sued the newspaper for _____ after they printed false stories.",
            "The _____ spread quickly through the school causing much harm.",
            "He was accused of spreading _____ about his classmate.",
            "The _____ damaged her reputation even though it wasn't true.",
            "She learned that _____ was different from expressing an opinion.",
            "The _____ in the gossip column hurt many people's feelings.",
            "He realised that spreading _____ was wrong and apologised.",
            "The _____ caused arguments between friends who believed it.",
            "She was careful not to engage in _____ about others.",
            "The _____ proved to be completely false when investigated."
        ],
        "solicit": [
            "The charity began to _____ donations from the public.",
            "She decided to _____ help from her neighbours for the project.",
            "The club would _____ new members at the school fair.",
            "He was not allowed to _____ business in the school grounds.",
            "The organisation would _____ volunteers for the community event.",
            "She needed to _____ opinions from everyone before making a decision.",
            "The campaign would _____ support from local businesses.",
            "He was careful how he would _____ feedback from his classmates.",
            "The group would _____ ideas from all members for the project.",
            "She began to _____ advice from experienced teachers."
        ],
        "sombre": [
            "The _____ news cast a shadow over the entire school.",
            "The _____ atmosphere in the room matched everyone's mood.",
            "She wore _____ colours to the memorial service.",
            "The _____ music reflected the sad occasion.",
            "His _____ expression showed he understood the seriousness.",
            "The _____ tone of the speech made everyone listen carefully.",
            "She found the _____ weather matched her feelings perfectly.",
            "The _____ mood affected everyone at the gathering.",
            "His _____ words warned them about the difficult times ahead.",
            "The _____ lighting in the room created a serious atmosphere."
        ],
        "sonnet": [
            "Shakespeare wrote many famous _____ that are still studied today.",
            "She had to memorise a _____ for her English literature exam.",
            "The _____ had exactly fourteen lines as required by the form.",
            "He wrote a beautiful _____ about nature for his homework.",
            "The teacher explained the structure of a _____ to the class.",
            "She analysed the _____ line by line to understand its meaning.",
            "The _____ followed a specific rhyme scheme and pattern.",
            "He struggled to write a _____ that met all the requirements.",
            "The _____ expressed deep emotions in just fourteen lines.",
            "She performed the _____ from memory at the school assembly."
        ],
        "sphere": [
            "The Earth is approximately a _____ in shape.",
            "She held the glass _____ carefully in her hands.",
            "The _____ rolled down the hill gathering speed.",
            "He learned that a _____ has no edges or corners.",
            "The crystal _____ reflected light in beautiful patterns.",
            "She drew a perfect _____ in her geometry lesson.",
            "The _____ was used as a model of the planet.",
            "He calculated the volume of the _____ using a formula.",
            "The _____ balanced precariously on the narrow surface.",
            "She studied the properties of a _____ in mathematics."
        ],
        "squalor": [
            "The family lived in _____ in the run-down house.",
            "The _____ of the abandoned building shocked the visitors.",
            "She was appalled by the _____ she saw in the neglected area.",
            "The _____ made it clear that nobody had lived there for years.",
            "He couldn't believe anyone could live in such _____.",
            "The _____ was a result of years of neglect and poverty.",
            "She worked hard to escape the _____ of her childhood home.",
            "The _____ in the room was overwhelming and unpleasant.",
            "He was determined to improve conditions and end the _____.",
            "The _____ served as a reminder of what could happen without care."
        ],
        "squeak": [
            "The door began to _____ when opened slowly.",
            "The mouse let out a tiny _____ when it saw the cat.",
            "Her new shoes started to _____ as she walked down the corridor.",
            "The rusty gate would _____ loudly whenever someone opened it.",
            "He heard a _____ coming from under the floorboards.",
            "The _____ of the brakes warned that they needed attention.",
            "She tried to _____ quietly so as not to wake anyone.",
            "The _____ sound indicated the wheel needed oiling.",
            "He could hear the _____ of the floorboards as someone crept upstairs.",
            "The _____ of the chalk on the board made everyone cringe."
        ],
        "stance": [
            "The boxer took a defensive _____ before the match began.",
            "Her _____ on the issue was clear from her speech.",
            "The politician's _____ on education was well-known.",
            "He adjusted his _____ to improve his balance.",
            "The teacher's _____ on homework was unpopular with pupils.",
            "She took a firm _____ against bullying in the school.",
            "His _____ showed he was ready for action.",
            "The _____ he adopted made it clear he wouldn't change his mind.",
            "She explained her _____ on the environmental issue.",
            "The athlete's _____ was perfect for the starting position."
        ],
        "stanza": [
            "Each _____ of the poem had four lines.",
            "She wrote a beautiful _____ about the changing seasons.",
            "The first _____ introduced the main character.",
            "He analysed each _____ of the poem separately.",
            "The _____ followed a specific rhyme pattern.",
            "She memorised the first _____ for her recitation.",
            "The _____ helped organise the poem into sections.",
            "He struggled to write a _____ that rhymed properly.",
            "The _____ conveyed a different emotion than the previous one.",
            "She counted the lines in each _____ to check the structure."
        ],
        "static": [
            "The population remained _____ for several decades.",
            "The _____ image on the screen wouldn't change.",
            "Her test scores were _____ showing no improvement.",
            "The _____ electricity made her hair stand on end.",
            "He found the _____ nature of the job boring.",
            "The _____ position meant nothing was moving.",
            "She preferred dynamic activities to _____ ones.",
            "The _____ display showed the same information all day.",
            "His interest in the subject remained _____ throughout the term.",
            "The _____ charge built up from rubbing the balloon."
        ],
        "stingy": [
            "The _____ man refused to donate anything to charity.",
            "Her _____ attitude meant she never shared her sweets.",
            "The _____ shopkeeper charged too much for everything.",
            "He was too _____ to buy his friend a birthday present.",
            "The _____ way he counted every penny annoyed his family.",
            "She was criticised for being _____ with her time.",
            "The _____ portion sizes left everyone feeling hungry.",
            "His _____ behaviour made him unpopular with classmates.",
            "The _____ approach meant they couldn't afford proper equipment.",
            "She realised that being _____ wasn't the same as being careful."
        ],
        "stolid": [
            "His _____ expression revealed nothing about his feelings.",
            "The _____ guard stood motionless at his post.",
            "She found his _____ response frustrating and unhelpful.",
            "The _____ way he reacted showed no emotion at all.",
            "His _____ nature made it difficult to know what he was thinking.",
            "The _____ appearance gave nothing away about his true feelings.",
            "She tried to get a reaction from his _____ face.",
            "The _____ response was typical of his unemotional character.",
            "His _____ behaviour made others think he didn't care.",
            "The _____ expression remained unchanged despite the good news."
        ],
        "stupefy": [
            "The complex problem seemed to _____ the students completely.",
            "The magician's trick would _____ the entire audience.",
            "The difficult question appeared to _____ the contestant.",
            "She watched the confusing film that seemed to _____ viewers.",
            "The unexpected news would _____ anyone who heard it.",
            "The complicated instructions began to _____ the new pupils.",
            "He found that the advanced mathematics would _____ most people.",
            "The strange behaviour seemed to _____ those watching.",
            "The complex puzzle would _____ even the cleverest solver.",
            "The unexpected turn of events seemed to _____ everyone present."
        ],
        "stupor": [
            "He fell into a _____ after the accident and couldn't respond.",
            "The medicine caused a _____ that lasted several hours.",
            "She was in a _____ and didn't notice what was happening.",
            "The shock put him into a _____ from which he slowly recovered.",
            "He remained in a _____ unable to understand what was said.",
            "The _____ made it impossible for him to make decisions.",
            "She emerged from the _____ feeling confused and disoriented.",
            "The _____ prevented him from remembering what had happened.",
            "He was in such a _____ that he didn't recognise his friends.",
            "The _____ lasted until the effects of the medication wore off."
        ],
        "sublime": [
            "The _____ music moved the entire audience to tears.",
            "She described the _____ beauty of the mountain sunset.",
            "The _____ performance received a standing ovation.",
            "He found the _____ poetry inspiring and beautiful.",
            "The _____ view from the top of the hill was breathtaking.",
            "She created a _____ work of art that impressed everyone.",
            "The _____ moment would stay with her forever.",
            "He experienced a _____ feeling of peace and contentment.",
            "The _____ quality of her writing was recognised by all.",
            "She achieved something _____ through hard work and dedication."
        ],
        "subside": [
            "The storm began to _____ as evening approached.",
            "The pain started to _____ after she took the medicine.",
            "The floodwaters would _____ once the rain stopped.",
            "His anger began to _____ as he calmed down.",
            "The fever started to _____ after proper treatment.",
            "The noise began to _____ as people left the building.",
            "The swelling would _____ with rest and ice.",
            "Her anxiety began to _____ once she understood the situation.",
            "The conflict started to _____ as both sides talked.",
            "The wind began to _____ making it safe to go outside."
        ],
        "sundry": [
            "The shop sold _____ items from around the world.",
            "She collected _____ objects that interested her.",
            "The _____ collection included everything from buttons to books.",
            "He found _____ items in the charity shop that caught his eye.",
            "The _____ assortment meant there was something for everyone.",
            "She organised the _____ belongings into different categories.",
            "The _____ goods filled the market stall completely.",
            "He enjoyed browsing through the _____ selection.",
            "The _____ nature of the collection made it fascinating.",
            "She sorted through the _____ items looking for treasures."
        ],
        "surly": [
            "The _____ waiter ignored their request completely.",
            "His _____ attitude made him unpopular with classmates.",
            "The _____ response showed he wasn't in a good mood.",
            "She avoided the _____ shopkeeper who was always grumpy.",
            "The _____ way he spoke offended everyone listening.",
            "His _____ behaviour made others avoid him.",
            "The _____ expression on his face warned people away.",
            "She found his _____ manner unpleasant and rude.",
            "The _____ reply was typical of his bad-tempered nature.",
            "His _____ disposition made it difficult to work with him."
        ],
        "surpass": [
            "Her performance would _____ all previous records.",
            "The new building would _____ the old one in every way.",
            "He hoped to _____ his own best time in the race.",
            "The student's work would _____ expectations completely.",
            "She managed to _____ her previous test score significantly.",
            "The achievement would _____ anything they had done before.",
            "He aimed to _____ the standards set by others.",
            "The quality would _____ what was normally expected.",
            "She worked hard to _____ her own personal best.",
            "The results would _____ all their hopes and dreams."
        ],
        "swallow": [
            "She had to _____ the bitter medicine despite its awful taste.",
            "He watched the bird _____ the worm whole.",
            "The pill was difficult to _____ without water.",
            "She tried to _____ her pride and apologise.",
            "He had to _____ his disappointment and congratulate the winner.",
            "The fish would _____ the bait if they weren't careful.",
            "She found it hard to _____ the large tablet.",
            "He watched her _____ nervously before speaking.",
            "The medicine was easier to _____ with a spoonful of honey.",
            "She had to _____ her fear and face the challenge."
        ],
        "synonym": [
            "\"Happy\" is a _____ for \"joyful\".",
            "She looked up the _____ in the thesaurus to improve her writing.",
            "The teacher asked them to find a _____ for the word \"big\".",
            "He learned that a _____ means the same as another word.",
            "The _____ helped her avoid repeating the same word.",
            "She used a _____ to make her writing more interesting.",
            "The _____ \"quick\" could replace \"fast\" in the sentence.",
            "He found a _____ that sounded better in his essay.",
            "The _____ expanded her vocabulary choices.",
            "She checked the _____ to find a more precise word."
        ],
        "tactile": [
            "The _____ experience of the soft fabric was pleasant.",
            "She enjoyed the _____ sensation of the smooth stone.",
            "The _____ learning style involved touching and feeling objects.",
            "He preferred _____ activities that used his hands.",
            "The _____ texture of the material was important to her.",
            "She found the _____ feedback helpful when learning.",
            "The _____ nature of the activity appealed to him.",
            "He enjoyed the _____ pleasure of working with clay.",
            "The _____ sense helped her understand the object better.",
            "She appreciated the _____ quality of the handmade item."
        ],
        "taxing": [
            "The _____ exam required hours of concentration.",
            "She found the _____ work exhausting but rewarding.",
            "The _____ journey left everyone feeling tired.",
            "He struggled with the _____ nature of the task.",
            "The _____ schedule meant she had little time to rest.",
            "She found the _____ challenge pushed her to improve.",
            "The _____ conditions made progress difficult.",
            "He prepared carefully for the _____ test ahead.",
            "The _____ work tested her abilities to the limit.",
            "She needed a break after the _____ day at school."
        ],
        "tedious": [
            "The _____ lecture seemed to last forever.",
            "She found the _____ task boring and repetitive.",
            "The _____ work made the day drag on slowly.",
            "He struggled to stay awake during the _____ presentation.",
            "The _____ process required patience and determination.",
            "She tried to make the _____ job more interesting.",
            "The _____ nature of the work tested her patience.",
            "He found the _____ routine monotonous and dull.",
            "The _____ task seemed never-ending.",
            "She looked for ways to make the _____ work more bearable."
        ],
        "temper": [
            "She lost her _____ when she heard the disappointing news.",
            "His quick _____ got him into trouble frequently.",
            "The teacher warned him about controlling his _____.",
            "She tried to keep her _____ despite the frustration.",
            "His bad _____ made others avoid him.",
            "She learned to manage her _____ through deep breathing.",
            "The _____ of the discussion became heated.",
            "He struggled to control his _____ when things went wrong.",
            "She found that exercise helped improve her _____.",
            "The _____ of the meeting was calm and professional."
        ],
        "tenant": [
            "The _____ paid rent to the landlord every month.",
            "She became a _____ of the flat after signing the agreement.",
            "The _____ complained about the broken heating system.",
            "He was a good _____ who always paid on time.",
            "The _____ looked after the property as if it were his own.",
            "She met the new _____ who would live next door.",
            "The _____ had rights that were protected by law.",
            "He was responsible for finding a new _____ for the house.",
            "The _____ reported the leak to the landlord immediately.",
            "She learned about the responsibilities of being a _____."
        ],
        "tenuous": [
            "There was only a _____ connection between the two events.",
            "The _____ link was too weak to prove anything.",
            "Her _____ grasp of the concept needed strengthening.",
            "The _____ relationship wouldn't last much longer.",
            "He had only a _____ understanding of the complex topic.",
            "The _____ evidence wasn't enough to convince anyone.",
            "She held onto the _____ hope that things would improve.",
            "The _____ thread was all that connected them.",
            "His _____ excuse wasn't believable.",
            "The _____ connection seemed to disappear completely."
        ],
        "thrive": [
            "The plants began to _____ in the sunny garden.",
            "She watched her confidence _____ as she practised more.",
            "The business would _____ if managed properly.",
            "He found that he could _____ in the supportive environment.",
            "The flowers would _____ with regular watering and care.",
            "She helped the charity _____ through her hard work.",
            "The school would _____ under the new headteacher's leadership.",
            "He discovered he could _____ when given the right opportunities.",
            "The garden would _____ in the warm summer weather.",
            "She watched her skills _____ with dedicated practice."
        ],
        "thwart": [
            "The bad weather threatened to _____ their plans completely.",
            "She tried to _____ the bully's attempts to hurt others.",
            "The security system would _____ any unauthorised entry.",
            "He worked hard to _____ the enemy's schemes.",
            "The obstacle would _____ their progress if not removed.",
            "She managed to _____ the plan before it caused harm.",
            "The delay would _____ their chances of success.",
            "He found a way to _____ the unfair treatment.",
            "The problem would _____ their efforts to finish on time.",
            "She hoped to _____ the negative effects of the decision."
        ],
        "tirade": [
            "He launched into a _____ about the unfair treatment.",
            "The teacher's _____ lasted for ten minutes without stopping.",
            "She listened patiently to his _____ about the problem.",
            "The _____ expressed all his pent-up frustration.",
            "He went on a _____ that nobody could interrupt.",
            "The _____ made everyone uncomfortable.",
            "She tried to calm him down after his long _____.",
            "The _____ covered every complaint he had.",
            "He delivered a _____ that left everyone speechless.",
            "The _____ showed how angry he really was."
        ],
        "turmoil": [
            "The country was in _____ after the unexpected election result.",
            "Her mind was in _____ trying to decide what to do.",
            "The school was in _____ following the sudden changes.",
            "He found it hard to think clearly in the _____.",
            "The _____ caused by the storm disrupted everything.",
            "She tried to remain calm despite the _____ around her.",
            "The _____ made it difficult to make any decisions.",
            "He worked to restore order after the period of _____.",
            "The _____ affected everyone in different ways.",
            "She hoped the _____ would settle down soon."
        ],
        "tyranny": [
            "The people rebelled against the _____ of the cruel ruler.",
            "She learned about the _____ that had oppressed the country.",
            "The _____ of the dictator made life miserable for everyone.",
            "He fought against the _____ that controlled his homeland.",
            "The _____ ended when the people stood up together.",
            "She read about the _____ in her history book.",
            "The _____ prevented people from expressing their opinions.",
            "He refused to accept the _____ any longer.",
            "The _____ was overthrown by a united resistance.",
            "She understood the importance of resisting _____."
        ],
        "uncanny": [
            "There was an _____ resemblance between the two strangers.",
            "The _____ similarity made everyone look twice.",
            "She found the _____ coincidence too strange to ignore.",
            "The _____ way he knew what she was thinking was spooky.",
            "He noticed the _____ timing of the events.",
            "The _____ accuracy of his prediction surprised everyone.",
            "She felt an _____ sense of having been there before.",
            "The _____ silence made everyone feel uncomfortable.",
            "He found the _____ connection between them mysterious.",
            "The _____ feeling that something was wrong persisted."
        ],
        "unfurl": [
            "The flag began to _____ in the strong wind.",
            "She watched the banner _____ as it was raised.",
            "The sail would _____ once they caught the wind.",
            "He saw the scroll _____ revealing the ancient writing.",
            "The flower petals began to _____ in the morning sun.",
            "She watched the map _____ showing the route ahead.",
            "The umbrella would _____ with the push of a button.",
            "He saw the banner _____ displaying the school's name.",
            "The leaves began to _____ as spring arrived.",
            "She watched the fabric _____ revealing the beautiful pattern."
        ],
        "unkempt": [
            "His _____ hair suggested he had just woken up.",
            "The _____ appearance made him look disorganised.",
            "She noticed his _____ uniform needed attention.",
            "The _____ garden showed signs of neglect.",
            "His _____ look was due to rushing out the door.",
            "The _____ room needed a thorough tidy.",
            "She tried to fix her _____ appearance before the photo.",
            "The _____ state of the building was obvious.",
            "His _____ hair stuck out in all directions.",
            "The _____ condition made everything look messy."
        ],
        "utopian": [
            "His _____ vision of society seemed impossible to achieve.",
            "She described a _____ world where everyone was equal.",
            "The _____ idea sounded perfect but unrealistic.",
            "He dreamed of a _____ future without any problems.",
            "The _____ plan was too idealistic to work in practice.",
            "She wrote about a _____ society in her essay.",
            "The _____ vision inspired many people to try.",
            "He realised his _____ dreams might never come true.",
            "The _____ concept was beautiful but impractical.",
            "She hoped for a _____ solution to all their problems."
        ],
        "vacuous": [
            "The _____ expression on his face showed he wasn't listening.",
            "Her _____ response suggested she hadn't understood.",
            "The _____ look made it clear his mind was elsewhere.",
            "He gave a _____ smile that meant nothing.",
            "The _____ comment added nothing to the discussion.",
            "She noticed the _____ stare and knew he wasn't paying attention.",
            "The _____ expression revealed an empty mind.",
            "He made a _____ remark that showed no thought.",
            "The _____ way he responded indicated no understanding.",
            "She found his _____ answers frustrating and unhelpful."
        ],
        "vantage": [
            "From this _____ point, we could see the entire valley.",
            "She found a perfect _____ to watch the parade.",
            "The high _____ provided an excellent view.",
            "He climbed to a better _____ to see the match.",
            "The _____ allowed them to see everything clearly.",
            "She chose a good _____ for taking photographs.",
            "The _____ point gave them an advantage.",
            "He moved to a different _____ to get a better angle.",
            "The _____ position helped them understand the layout.",
            "She appreciated the _____ that showed the whole scene."
        ],
        "various": [
            "She tried _____ methods to solve the problem.",
            "The shop sold _____ items from different countries.",
            "He collected _____ objects that interested him.",
            "The _____ colours made the display attractive.",
            "She met _____ people from different backgrounds.",
            "The _____ options gave them plenty of choice.",
            "He explored _____ ways to improve his work.",
            "The _____ activities kept everyone entertained.",
            "She considered _____ solutions before deciding.",
            "The _____ styles made the collection interesting."
        ],
        "verbose": [
            "His _____ explanation confused rather than helped.",
            "The _____ speech went on far too long.",
            "She found his _____ writing style difficult to follow.",
            "The _____ way he spoke used too many words.",
            "He was criticised for being too _____ in his reports.",
            "The _____ description included unnecessary details.",
            "She preferred concise writing to _____ prose.",
            "The _____ answer could have been much shorter.",
            "He realised his _____ style wasn't effective.",
            "The _____ nature of his speech bored the audience."
        ],
        "verdant": [
            "The _____ fields stretched for miles in every direction.",
            "She admired the _____ beauty of the countryside.",
            "The _____ grass was perfect for playing games.",
            "He walked through the _____ forest enjoying the nature.",
            "The _____ landscape was a joy to behold.",
            "She painted the _____ hills in her art lesson.",
            "The _____ vegetation showed the area received plenty of rain.",
            "He found the _____ scenery peaceful and calming.",
            "The _____ meadows were full of wildflowers.",
            "She described the _____ countryside in her story."
        ],
        "viable": [
            "The plan seemed _____ after careful consideration.",
            "She found a _____ solution to the difficult problem.",
            "The _____ option was the best one available.",
            "He determined that the idea was _____ and worth pursuing.",
            "The _____ approach would work if implemented properly.",
            "She explored whether the project was _____.",
            "The _____ alternative provided a good way forward.",
            "He realised the plan wasn't _____ without more resources.",
            "The _____ strategy had a good chance of success.",
            "She confirmed that the solution was _____ and practical."
        ],
        "vigour": [
            "Despite his age, he showed remarkable _____.",
            "She approached the task with great _____ and enthusiasm.",
            "The _____ of his performance impressed everyone.",
            "He attacked the problem with _____ and determination.",
            "The _____ of her response showed she was ready.",
            "She maintained her _____ throughout the long day.",
            "The _____ of the team inspired others to work harder.",
            "He found new _____ after the encouraging words.",
            "The _____ of her approach was evident to all.",
            "She brought _____ and energy to everything she did."
        ],
        "vilify": [
            "The newspaper tried to _____ the politician unfairly.",
            "She refused to _____ others even when criticised.",
            "The attempt to _____ her character failed.",
            "He didn't want to _____ anyone without evidence.",
            "The campaign to _____ the school was unjust.",
            "She learned that it was wrong to _____ people.",
            "The attempt to _____ his reputation was unsuccessful.",
            "He realised that to _____ others was harmful.",
            "The unfair attempt to _____ her work was rejected.",
            "She wouldn't _____ anyone based on rumours."
        ],
        "virtue": [
            "Patience is a _____ that takes time to develop.",
            "She believed that honesty was an important _____.",
            "The _____ of kindness should be practised daily.",
            "He learned that every _____ had its value.",
            "The _____ of hard work was instilled in him from childhood.",
            "She demonstrated the _____ of courage in difficult times.",
            "The _____ of generosity made her popular with friends.",
            "He tried to develop the _____ of self-control.",
            "The _____ of perseverance helped her succeed.",
            "She understood that _____ was its own reward."
        ],
        "vulgar": [
            "His _____ jokes offended many people in the audience.",
            "She found the _____ language inappropriate for school.",
            "The _____ behaviour embarrassed everyone present.",
            "He was told that _____ comments weren't acceptable.",
            "The _____ display showed a lack of good taste.",
            "She avoided _____ people who lacked manners.",
            "The _____ nature of the joke made people uncomfortable.",
            "He realised that _____ humour wasn't funny.",
            "The _____ way he spoke shocked his teachers.",
            "She was disappointed by the _____ standards shown."
        ],
        "wary": [
            "She was _____ of strangers approaching her in the park.",
            "The _____ look in his eyes showed he didn't trust them.",
            "He remained _____ after the previous bad experience.",
            "The _____ approach prevented her from making mistakes.",
            "She was _____ about accepting help from unknown people.",
            "The _____ attitude helped him avoid trouble.",
            "He became more _____ after learning about the risks.",
            "The _____ way she checked everything showed caution.",
            "She remained _____ even when things seemed safe.",
            "The _____ response was wise given the circumstances."
        ],
        "whining": [
            "His constant _____ annoyed everyone around him.",
            "She told him to stop _____ and solve the problem instead.",
            "The _____ tone in his voice was unpleasant to hear.",
            "He was known for _____ whenever things didn't go his way.",
            "The _____ complaints achieved nothing positive.",
            "She found his _____ behaviour childish and irritating.",
            "The _____ sound of the dog could be heard from next door.",
            "He realised that _____ wouldn't help the situation.",
            "The _____ way he spoke made others avoid him.",
            "She was tired of listening to his constant _____."
        ],
        "wicked": [
            "The _____ witch cast a spell on the princess.",
            "She read about the _____ stepmother in the fairy tale.",
            "The _____ plan was designed to cause harm.",
            "He realised that _____ deeds would have consequences.",
            "The _____ character in the story was eventually defeated.",
            "She learned that _____ actions were always wrong.",
            "The _____ scheme was discovered before it could succeed.",
            "He understood that being _____ would lead to trouble.",
            "The _____ behaviour shocked everyone who witnessed it.",
            "She found the _____ character in the book frightening."
        ],
        "wilful": [
            "The _____ child refused to listen to any advice.",
            "Her _____ behaviour caused problems for everyone.",
            "The _____ way he acted showed he wouldn't compromise.",
            "He was known for being _____ and stubborn.",
            "The _____ decision led to unfortunate consequences.",
            "She found his _____ attitude difficult to deal with.",
            "The _____ nature of his actions worried his parents.",
            "He realised that being _____ wasn't always a good thing.",
            "The _____ refusal to cooperate created difficulties.",
            "She tried to understand why he was so _____."
        ],
        "wistful": [
            "She gave a _____ smile as she remembered the past.",
            "The _____ look in his eyes showed he was thinking of happier times.",
            "He felt _____ when he saw the old photographs.",
            "The _____ expression revealed her longing for the past.",
            "She became _____ when thinking about her childhood home.",
            "The _____ tone in her voice showed she missed those days.",
            "He looked _____ at the places he used to visit.",
            "The _____ way she spoke about the past was touching.",
            "She felt _____ about the opportunities she had missed.",
            "The _____ smile appeared whenever she thought of her friends."
        ],
        "woeful": [
            "The _____ expression on his face showed his sadness.",
            "She found the _____ news difficult to accept.",
            "The _____ state of the building was obvious to all.",
            "He looked _____ after hearing the disappointing results.",
            "The _____ condition of the garden needed attention.",
            "She felt _____ about the situation they found themselves in.",
            "The _____ way he spoke revealed his unhappiness.",
            "He was in a _____ mood after the setback.",
            "The _____ appearance matched his feelings perfectly.",
            "She tried to cheer him up from his _____ state."
        ],
        "wretch": [
            "The poor _____ had nowhere to go and no one to help.",
            "She felt sorry for the _____ who had lost everything.",
            "The miserable _____ begged for food on the street corner.",
            "He looked like a _____ after being caught in the rain.",
            "The unfortunate _____ had made many bad decisions.",
            "She helped the _____ who was clearly in need.",
            "The _____ had been abandoned by everyone he knew.",
            "He felt like a _____ after failing the important test.",
            "The _____ appearance made people want to help.",
            "She couldn't help but feel pity for the poor _____."
        ],
        "yearned": [
            "She _____ for the summer holidays to begin.",
            "He _____ to see his family again after months away.",
            "The way she _____ for adventure was obvious to everyone.",
            "He _____ for the chance to prove himself.",
            "She _____ to visit the places she had read about.",
            "The way he _____ for approval showed his insecurity.",
            "She _____ for the freedom that adulthood would bring.",
            "He _____ to understand why things had gone wrong.",
            "The way she _____ for friendship touched everyone's hearts.",
            "He _____ to make things right after his mistake."
        ],
        "zealot": [
            "The religious _____ refused to compromise his beliefs.",
            "She was known as a _____ for environmental causes.",
            "The _____ wouldn't listen to any opposing views.",
            "He became a _____ for the new political movement.",
            "The _____ nature of his support made others uncomfortable.",
            "She found the _____ approach too extreme.",
            "The _____ refused to consider any alternatives.",
            "He was described as a _____ because of his uncompromising stance.",
            "The _____ way he promoted his ideas put people off.",
            "She realised that being a _____ wasn't always positive."
        ],
        "zealous": [
            "The _____ student worked hard to achieve her goals.",
            "Her _____ approach to learning impressed all her teachers.",
            "The _____ way he supported the team was inspiring.",
            "He was _____ about protecting the environment.",
            "The _____ effort she put into the project was remarkable.",
            "She showed _____ dedication to her studies.",
            "The _____ support he gave helped the team succeed.",
            "He was _____ in his pursuit of excellence.",
            "The _____ way she tackled challenges was admirable.",
            "She remained _____ despite facing many obstacles."
        ],
        "zestful": [
            "Her _____ approach to life was inspiring to everyone.",
            "The _____ way she tackled challenges was admirable.",
            "He brought a _____ energy to everything he did.",
            "The _____ attitude made the work enjoyable.",
            "She approached each day with _____ enthusiasm.",
            "The _____ way he participated encouraged others.",
            "He showed a _____ spirit that was contagious.",
            "The _____ nature of her personality was refreshing.",
            "She maintained her _____ approach despite setbacks.",
            "The _____ way she lived her life was an example to others."
        ]
    }
    
    # Get sentences for this word
    if word_lower in word_sentences:
        custom_sentences = word_sentences[word_lower]
        # Add custom sentences, ensuring we have exactly 10
        for sent in custom_sentences[:10]:
            if sent not in sentences:
                sentences.append(sent)
    
    # Fill up to 10 sentences if needed
    while len(sentences) < 10:
        # Generate additional sentences based on word type and meaning
        if is_verb:
            sentences.append(f"She had to _____ when the situation required action.")
        elif is_adjective:
            sentences.append(f"The _____ appearance was noticeable to everyone.")
        else:
            sentences.append(f"The _____ was important to understanding the topic.")
    
    return sentences[:10]


def main():
    """Generate quiz sentences for Level 2 Batch 5."""
    input_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level2_batch5.txt")
    output_file = Path("/Users/shakirali/iOSApps/vocabularyWizardAPI/data/level2_batch5.csv")
    
    # Read words from input file
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
    
    # Generate sentences and write to CSV
    total_sentences = 0
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['level', 'word', 'sentence'])
        
        for word, meaning, example, synonym, antonym in words_data:
            sentences = generate_sentences_for_word(word, meaning, example, synonym, antonym)
            for sentence in sentences:
                writer.writerow(['2', word, sentence])
                total_sentences += 1
    
    print(f"Level 2 Batch 5 complete: {total_sentences} sentences")


if __name__ == "__main__":
    main()
