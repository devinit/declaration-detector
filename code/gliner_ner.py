from gliner import GLiNER

model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

text = """

Sudan declares state of emergency as record flooding kills 99 people
Floods caused by heavy seasonal rains have damaged more than 100,000 homes, says minister

Nicola Slawson
Sat 5 Sep 2020 07.04 EDT
Sudan has declared a three-month state of emergency after flooding that has killed 99 people this year, according to the country’s state news agency.

The Sudanese minister of labour and social development said that in addition to the deaths, the floods had affected more than half a million people, injuring 46, and had damaged more than 100,000 homes.

Much of the flooding was triggered by heavy seasonal rains, mainly in neighbouring Ethiopia, which caused the Nile River to rise to nearly 17.5 metres (about 57ft) at the end of August – the highest level in 100 years, according to the authorities.

The rates of floods and rain for this year exceeded the records set in 1946 and 1988, with expectations of continued rising indicators, Lena el-Sheikh added.

The states of Khartoum, Blue Nile and River Nile are among the hardest-hit by the floods, while damage has also been reported in the Gezira, Gadarif, West Kordofan and South Darfur regions, according to the UN.

The UN said it was supporting the national response with emergency shelter and household supplies, together with water, sanitation and hygiene assistance, food, health services and vector control.

The UN reported that it was able to respond quickly as supplies to meet the needs of 250,000 people had been pre-positioned before the rains started.

But with stocks “being depleted rapidly”, the UN is calling for wider support from the international community.
"""

labels = ["location", "date", "disaster", "declaration"]

entities = model.predict_entities(text, labels)

for entity in entities:
    print(entity["text"], "=>", entity["label"])