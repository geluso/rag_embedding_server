import requests

from document_payload import DocumentPayload

docs = [
    DocumentPayload("Dog", "https://en.wikipedia.org/wiki/Dog", "The dog (Canis familiaris or Canis lupus familiaris) is a domesticated descendant of the gray wolf. Also called the domestic dog, it was selectively bred from an extinct population of wolves during the Late Pleistocene by hunter-gatherers. The dog was the first species to be domesticated by humans, over 14,000 years ago and before the development of agriculture. Experts estimate that due to their long association with humans, dogs have gained the ability to thrive on a starch-rich diet that would be inadequate for other canids."),
    DocumentPayload("Cat", "https://en.wikipedia.org/wiki/Cat", "The cat (Felis catus), also referred to as the domestic cat, is a small domesticated carnivorous mammal. It is the only domesticated species of the family Felidae. Advances in archaeology and genetics have shown that the domestication of the cat occurred in the Near East around 7500 BC. It is commonly kept as a pet and farm cat, but also ranges freely as a feral cat avoiding human contact. It is valued by humans for companionship and its ability to kill vermin. Its retractable claws are adapted to killing small prey species such as mice and rats. It has a strong, flexible body, quick reflexes, and sharp teeth, and its night vision and sense of smell are well developed. It is a social species, but a solitary hunter and a crepuscular predator. Cat communication includes vocalizations—including meowing, purring, trilling, hissing, growling, and grunting—as well as body language."),
    DocumentPayload("Turtle", "https://en.wikipedia.org/wiki/Turtle", "Turtles are reptiles of the order Testudines, characterized by a special shell developed mainly from their ribs. Modern turtles are divided into two major groups, the Pleurodira (side necked turtles) and Cryptodira (hidden necked turtles), which differ in the way the head retracts. There are 360 living and recently extinct species of turtles, including land-dwelling tortoises and freshwater terrapins. They are found on most continents, some islands and, in the case of sea turtles, much of the ocean. Like other amniotes (reptiles, birds, and mammals) they breathe air and do not lay eggs underwater, although many species live in or around water."),
    DocumentPayload("Spy in the House of Love", "https://en.wikipedia.org/wiki/What_Up,_Dog%3F", "What Up, Dog? is the third studio album by Was (Not Was). It became the group's breakthrough album worldwide and was ranked #99 on the Rolling Stone magazine's list of the 100 Best Albums of the 1980s. The cover illustration was credited to Christoph Simon and Karen Kelly."),
    DocumentPayload("Cat Stevens", "https://en.wikipedia.org/wiki/Cat_Stevens", "Yusuf Islam (born Steven Demetre Georgiou; 21 July 1948),[1] commonly known by his stage names Cat Stevens, Yusuf, and Yusuf / Cat Stevens, is a British singer-songwriter and musician. He has sold more than 100 million records and has more than two billion streams.[2] His musical style consists of folk, rock, pop, and, later in his career, Islamic music. Following two decades in which he performed only music which met strict religious standards, he returned to making secular music in 2006.[3][4][5] He was inducted into the Rock and Roll Hall of Fame in 2014.[6] He has received two honorary doctorates and awards for promoting peace as well as other humanitarian awards."),
    DocumentPayload("Adverse possession", "https://en.wikipedia.org/wiki/Adverse_possession", "Adverse possession in common law, and the related civil law concept of usucaption (also acquisitive prescription or prescriptive acquisition), are legal mechanisms under which a person who does not have legal title to a piece of property, usually real property, may acquire legal ownership based on continuous possession or occupation without the permission (licence) of its legal owner.[1]")
]

law_url = "https://law.justia.com/codes/georgia/title-34/chapter-8/article-4/section-34-8-125/"
text = open("./georgia_data_law.txt").read()
print(text)


localhost = "http://localhost:8080"
ngrok_url = "https://4cb3-2601-602-8b82-92b0-64d0-4b7b-a51a-85fb.ngrok-free.app"
base_url = ngrok_url
url_add_document = base_url + "/add_document/"
url_search = base_url + "/search/"

for doc in docs:
    response = requests.post(url_add_document, json=doc.to_dict())
    print(response.text)

#query = "What are the legal implications of breach of contract?"
#response = requests.get(url_search + "?q=" + query)
#print(response.text)
