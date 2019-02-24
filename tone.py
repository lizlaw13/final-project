import indicoio

# This function will return a number between 0 and 1. This number is a probability representing the likelihood that the analyzed text 
# is positive or negative. Values greater than 0.5 indicate positive sentiment, while values less than 0.5 indicate negative sentiment.

indicoio.config.api_key = '08ab282670a12fabb9e9fcf8219955f5'

print(indicoio.sentiment(['hello today i am very sad']))

