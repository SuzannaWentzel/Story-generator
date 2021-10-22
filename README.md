# Story-generator
This project generates stories based on author styles using NLP models. This project was made for the final project of the course Natural Language Processing at University of Twente.

# Preprocess your stories
The file ```preprocessing.py``` will preprocess the text of your language by applying POS. We might still change this and remove punctuation.

# Run story generator
The file ```text_generation.py``` will read the preprocessed files and will ask for an input sentence. It will then complete your sentence untill it has generated an entire alinea in the style of a specific author (Tolkien for now, but we are adding George R. R. Martin).
