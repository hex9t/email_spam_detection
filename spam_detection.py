import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

def spam_detection(text):
    # Load the spam dataset
    df = pd.read_csv('balanced_dataset.csv')
    df['Category'] = df['Category'].map({'ham': 0, 'spam': 1})
    # Filter the DataFrame to get only the "ham" rows
    ham_df = df[df['Category'] == 'ham']

# Calculate the number of rows to remove (30% of ham rows)
    remove_count = int(len(ham_df))

# Randomly select the rows to be removed
    rows_to_remove = ham_df.sample(n=remove_count, random_state=42).index

# Remove the selected rows from the DataFrame
    df = df.drop(rows_to_remove)

    
    X = df['Message']
    y = df['Category']

    # Initialize the CountVectorizer
    cv = CountVectorizer()
    print(df.describe())

    # Transform the text data into feature vectors
    X = cv.fit_transform(X)

    # Initialize the spam detection model (Multinomial Naive Bayes)
    model = MultinomialNB()

    # Train the model
    model.fit(X, y)

    # Transform the input text into a feature vector
    text_vector = cv.transform([text])

    # Make the prediction
    prediction = model.predict(text_vector)

    # Return the prediction result
    return prediction[0]

def is_spam(text):
    for word in spam_words:
        if word in text.lower():
            return True
    return False

spam_words = [
    "buy",
    "discount",
    "free",
    "limited time",
    "money back",
    "offer",
    "prize",
    "guaranteed",
    "click here",
    "unsubscribe",
    "urgent",
    "act now",
    "earn money",
    "cash",
    "earn extra income",
    "income from home",
    "opportunity",
    "winner",
    "$$$",
    "investment",
    "viagra",
    "cialis",
    "replica",
    "enlargement",
    "debt",
    "mortgage",
    "credit card offers",
    "online pharmacy",
    "weight loss",
    "lose weight fast",
    "multi-level marketing",
    "MLM",
    "work from home",
    "meet singles",
    "dating",
    "gambling",
    "casino",
    "adult content",
    "XXX",
    "porn",
    "nigerian prince",
    "inheritance",
    "lottery",
    "riches",
    "refund",
    "bank account",
    "loan",
    "insurance",
    "recovery",
    "stock pick",
    "miracle",
    "investment advice",
    "promise",
    "congratulations",
    "trial",
    "cancel at any time",
    "cheap",
    "lowest price",
    "hidden",
    "miracle",
    "weight loss",
    "weight loss patch",
    "prescription",
    "weight",
    "viagra",
    "pharmacy",
    "online pharmacy",
    "online degree",
    "university diploma",
    "college degree",
    "diploma",
    "million dollars",
    "limited time offer",
    "no credit check",
    "meet singles",
    "meet hot singles",
    "amazing",
    "stop snoring",
    "work at home",
    "no catch",
    "order now",
    "meet singles",
    "free access",
    "be your own boss",
    "opportunity",
    "new customers only",
    "call now",
    "cash bonus",
    "deal",
    "click below",
    "click here",
    "get started now",
    "compare",
    "money back guarantee",
    "hidden charges",
    "apply now",
    "free gift",
    "giveaway",
    "limited supply",
    "order today",
    "promise you",
    "risk-free",
    "serious cash",
    "you're a winner",
    "winner",
    "social security number",
    "this isn't a scam",
    "no fees",
    "no credit check",
    "no hidden",
    "no-obligation",
    "no purchase necessary",
    "no strings attached",
    "only $",
    "opportunity",
    "please read",
    "potential earnings",
    "problem",
    "removal",
    "remove",
    "request",
    "reverses",
    "risk free",
    "sales",
    "satisfaction",
    "save big money",
    "score",
    "serious cash",
    "stop",
    "success",
    "teen",
    "trial",
    "unsecured credit",
    "unsolicited",
    "valium",
    "viagra",
    "vicodin",
    "win",
    "winner",
    "work at home",
    "xanax",
    "you are a winner",
    "you have been selected",
    "your income",
    "valuable",
    "trouble",
    "urgent",
    "weight loss",
    "what are you waiting for?",
    "while supplies last",
    "while you sleep",
    "will not believe your eyes",
    "win",
    "winner",
    "winning",
    "work at home",
    "work from home",
    "xanax",
    "you are a winner",
    "you have been selected",
    "your income",
]


