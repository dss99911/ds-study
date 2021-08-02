import re

#%%
import numpy as np
import pandas as pd
df = pd.read_csv('/Users/hyun.kim/Downloads/Untitled3.csv')


# predicted = df["predicted_message_type"].astype('string')
# correct = df["message_type"].astype('string')
transaction_columns = ["RECEIVE", "DEPOSIT", "REPAY", "WITHDRAWAL", "TRANSFER", "PAY"]
df["predicted_is_transaction"] = np.isin(df["msg_type_prediction"], transaction_columns)
df["is_transaction"] = np.isin(df["msg_type"], transaction_columns)
df["correct"] = df["msg_type_prediction"] == df["msg_type"]
df["correct_transaction"] = df["predicted_is_transaction"] == df["is_transaction"]

count = df.groupby(["correct"]).count()["message"]
count_transaction = df.groupby(["correct_transaction"]).count()["message"]

#%%

import numpy as np
import pandas as pd

df = pd.read_excel('/Users/hyun.kim/Downloads/List_SMS_Headers_16062020_0.xlsx')
df.to_csv("/Users/hyun.kim/Downloads/List_SMS_Headers_16062020_0.csv")

#%%
def is_same_name(upi_id_name: str, contact_name: str):
    upi_id_name = upi_id_name.upper()
    upi_id_name = re.sub(r'[AEIOUH]', '', upi_id_name)
    upi_id_name = re.sub(r' +', ' ', upi_id_name).strip()
    upi_id_name = re.sub(r'[^A-Z ]', '', upi_id_name)
    upi_id_words = upi_id_name.split(" ")

    contact_name = contact_name.strip().upper()
    contact_name = contact_name.replace(".", " ")
    contact_name = re.sub(r'\b[A-Z]+&[A-Z]+\b', '', contact_name)
    contact_name = re.sub(r'[^A-Z ]', '', contact_name)
    contact_name = re.sub(r'\b(?:HYD|PERIKEEDU|JIO|SIR|BRO|LAPTOP|JI|RAIPUR|HYDERABAD|MY|DEAR|ANNA|BHAU|PANDIT)\b', '', contact_name)
    contact_name = re.sub(r'[AEIOUH]', '', contact_name)
    contact_name = re.sub(r' +', ' ', contact_name).strip()
    contact_words = contact_name.split(" ")

    if len(contact_words) == 1:
        if len(contact_words[0]) < 4:
            return False
        return contact_words[0] in upi_id_name.replace(" ", "")

    contact_words.sort(key=len, reverse=True)

    matched_contact_words=[]
    for contact_word in contact_words:
        for i in range(len(upi_id_words)):
            upi_id_word = upi_id_words[i]
            if upi_id_word.startswith(contact_word):
                matched_contact_words.append(contact_word)
                del upi_id_words[i]
                break

    if len(upi_id_words) == 0:
        return True

    if len(list(filter(lambda w: len(w)>=4, matched_contact_words))) >= 2:
        return True

    if len(matched_contact_words) == len(contact_words):
        return True
    return False

result = is_same_name("Md Salim Sk", "Selim Laptop")