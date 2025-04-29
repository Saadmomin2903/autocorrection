import streamlit as st
from symspellpy import SymSpell, Verbosity  
import os

sym_spell = SymSpell(max_dictionary_edit_distance=3, prefix_length=7)

dict_path = "frequency_dictionary_en_82_765.txt"
if not os.path.exists(dict_path):
    st.error("Dictionary file not found! Please ensure it's in the same directory.")
else:
    sym_spell.load_dictionary(dict_path, term_index=0, count_index=1)

def get_top5_suggestions(word):
    """Get top 5 spelling suggestions"""
    suggestions = sym_spell.lookup(
        word.lower(), 
        Verbosity.CLOSEST, 
        max_edit_distance=3,
        include_unknown=False  
    )
    return [suggestion.term for suggestion in suggestions[:5]]

def correct_text(input_text):
    words = input_text.split()
    corrected_words = []
    suggestions_dict = {}

    for word in words:
        # Check if word exists in dictionary (exact match)
        if not sym_spell.lookup(word, Verbosity.TOP, max_edit_distance=0):
            candidates = get_top5_suggestions(word.lower())
            best_correction = candidates[0] if candidates else word
            corrected_words.append(best_correction)
            suggestions_dict[word] = candidates
        else:
            corrected_words.append(word)

    return " ".join(corrected_words), suggestions_dict


# Streamlit UI
st.title("Autocorrect System")
st.write("Enter text to see corrections and suggestions!")

user_input = st.text_area("Input text:", height=200)

if st.button("Correct"):
    if not user_input.strip():
        st.warning("Please enter some text!")
    else:
        with st.spinner("Analyzing..."):
            corrected, suggestions = correct_text(user_input)
        
        st.subheader("Corrected Text:")
        st.success(corrected)
        
        if suggestions:
            st.subheader("Suggestions:")
            for wrong, options in suggestions.items():
                st.markdown(f"**{wrong}**: {', '.join(options)}")
        else:
            st.info("No spelling issues found!")

st.markdown("---")

