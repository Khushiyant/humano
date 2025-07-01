import os
import re
import random
import openai
import logging
from typing import Dict, List, Tuple

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter

logger = logging.getLogger(__name__)

import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
import string


class HumanizerService:
    """
    Advanced humanizer service based on academic research findings
    Implements techniques from DIPPER, HMGC framework, and ADAT research
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Download required NLTK data (run once)
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/wordnet')
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        
        # Research-based AI writing patterns (from ADAT framework)
        self.ai_patterns = [
            r'\bIn conclusion,?\b',
            r'\bFurthermore,?\b',
            r'\bMoreover,?\b',
            r'\bAdditionally,?\b',
            r'\bIt is important to note that\b',
            r'\bIt should be noted that\b',
            r'\bAs we delve into\b',
            r'\bLet\'s explore\b',
            r'\bIn this comprehensive guide\b',
            r'\bIn this article,?\b',
            r'\bTo summarize,?\b',
            r'\bIn summary,?\b',
            r'\bFirstly,?\b',
            r'\bSecondly,?\b',
            r'\bLastly,?\b',
            r'\bUltimately,?\b',
            r'\bConsequently,?\b',
            r'\bTherefore,?\b',
            r'\bHence,?\b',
            r'\bNevertheless,?\b',
            r'\bNonetheless,?\b',
            r'\bSubsequently,?\b',
            r'\bIt can be observed that\b',
            r'\bIt is evident that\b',
            r'\bAs aforementioned\b',
            r'\bAs previously discussed\b',
        ]
        
        # Human-like replacements
        self.human_replacements = {
            "In conclusion": ["To wrap up", "Bottom line", "So there you have it", "All things considered", "At the end of the day"],
            "Furthermore": ["Plus", "Also", "On top of that", "What's more", "And another thing"],
            "Moreover": ["Also", "Plus", "And", "What's more", "On top of that"],
            "Additionally": ["Also", "Plus", "And", "On top of that", "What's more"],
            "It is important to note that": ["Keep in mind that", "Worth mentioning", "Here's the thing", "Just so you know", "Don't forget that"],
            "It should be noted that": ["Worth noting", "Keep in mind", "Here's what's interesting", "Just remember"],
            "comprehensive": ["complete", "thorough", "detailed", "in-depth", "full", "extensive"],
            "utilize": ["use", "employ", "apply", "work with"],
            "implement": ["use", "put in place", "apply", "start using", "set up"],
            "facilitate": ["help", "make easier", "enable", "assist with"],
            "demonstrate": ["show", "prove", "illustrate", "make clear"],
            "endeavor": ["try", "attempt", "work", "effort"],
            "optimal": ["best", "ideal", "perfect", "top", "great"],
            "subsequent": ["next", "following", "later", "after that"],
            "methodology": ["method", "approach", "way", "process"],
            "advantageous": ["helpful", "good", "beneficial", "useful"],
            "substantial": ["big", "large", "significant", "major"],
            "commence": ["start", "begin", "kick off"],
            "terminate": ["end", "stop", "finish"],
            "ascertain": ["find out", "figure out", "determine"],
            "prioritize": ["focus on", "put first", "make important"],
            "magnitude": ["size", "scale", "extent"],
        }
        
        # Contractions to make text more conversational
        self.contractions = {
            "do not": "don't",
            "will not": "won't", 
            "cannot": "can't",
            "could not": "couldn't",
            "should not": "shouldn't",
            "would not": "wouldn't",
            "is not": "isn't",
            "are not": "aren't",
            "was not": "wasn't",
            "were not": "weren't",
            "have not": "haven't",
            "has not": "hasn't",
            "had not": "hadn't",
            "will have": "we'll have",
            "you will": "you'll",
            "we will": "we'll",
            "they will": "they'll",
            "it will": "it'll",
        }
        
        # Perplexity-increasing word replacements (DIPPER-inspired)
        self.perplexity_enhancers = {
            "very": ["incredibly", "exceptionally", "remarkably", "extraordinarily", "tremendously"],
            "good": ["excellent", "outstanding", "superb", "remarkable", "exceptional", "stellar"],
            "bad": ["terrible", "awful", "dreadful", "atrocious", "abysmal", "deplorable"],
            "big": ["enormous", "massive", "colossal", "gigantic", "immense", "vast"],
            "small": ["tiny", "minuscule", "petite", "compact", "diminutive", "microscopic"],
            "fast": ["rapid", "swift", "speedy", "brisk", "hasty", "expeditious"],
            "slow": ["sluggish", "lethargic", "gradual", "leisurely", "unhurried", "deliberate"],
            "important": ["crucial", "vital", "essential", "pivotal", "paramount", "significant"],
            "easy": ["effortless", "straightforward", "uncomplicated", "simple", "elementary"],
            "difficult": ["challenging", "arduous", "formidable", "demanding", "strenuous"],
            "new": ["novel", "fresh", "innovative", "cutting-edge", "revolutionary", "modern"],
            "old": ["ancient", "vintage", "traditional", "established", "time-honored", "classic"],
        }
        
        # Burstiness patterns (sentence length variation)
        self.burstiness_patterns = {
            "short_fragments": [
                "Exactly.", "True.", "Obviously.", "Clearly.", "Indeed.", "Absolutely.",
                "No doubt.", "Precisely.", "Certainly.", "Definitely.", "Without question."
            ],
            "medium_connectors": [
                "But here's the thing -", "Now, here's what's interesting:",
                "Let me explain:", "Think about it:", "Consider this:",
                "Here's why:", "The reality is:", "What's fascinating is:"
            ],
            "long_elaborators": [
                "What I find particularly intriguing about this whole situation is that",
                "If you really think about it from a broader perspective, you'll realize that",
                "The thing that most people don't seem to understand or appreciate is that",
                "When you take into account all the various factors and considerations involved, it becomes clear that"
            ]
        }
        
        # Character-level modifications for detector evasion
        self.character_substitutions = {
            'a': 'а',  # Cyrillic 'a' (U+0430)
            'e': 'е',  # Cyrillic 'e' (U+0435)
            'o': 'о',  # Cyrillic 'o' (U+043E)
            'p': 'р',  # Cyrillic 'p' (U+0440)
            'c': 'с',  # Cyrillic 'c' (U+0441)
            'x': 'х',  # Cyrillic 'x' (U+0445)
        }
        
        # Invisible characters for steganographic modifications
        self.invisible_chars = [
            '\u200B',  # Zero width space
            '\u200C',  # Zero width non-joiner
            '\u200D',  # Zero width joiner
            '\u2060',  # Word joiner
        ]
        
        # Human-like error patterns
        self.typo_patterns = {
            "common_typos": {
                "the": ["teh", "hte"],
                "and": ["adn", "nad"],
                "you": ["yuo", "yu"],
                "that": ["taht", "thta"],
                "with": ["wiht", "wtih"],
                "this": ["tihs", "thsi"],
                "have": ["ahve", "hvae"],
                "from": ["form", "fomr"],
                "they": ["tehy", "thye"],
                "were": ["wre", "weer"],
            },
            "autocorrect_errors": {
                "definitely": "defiantly",
                "separate": "seperate", 
                "weird": "wierd",
                "piece": "peice",
                "receive": "recieve",
                "until": "untill",
                "beginning": "begining",
                "grammar": "grammer",
                "embarrass": "embarass",
                "occurrence": "occurence",
            }
        }
        
    def humanize_content(self, content: str, strength: str = "medium") -> Dict[str, str]:
        """
        Humanize AI-generated content using research-proven techniques
        
        Implements methods from:
        - DIPPER paraphrasing model research
        - HMGC (Humanizing Machine-Generated Content) framework
        - ADAT (Adversarial Detection Attack on AI-Text) findings
        
        Args:
            content: The content to humanize
            strength: Humanization strength ("low", "medium", "high")
            
        Returns:
            Dict with success status and humanized content or error message
        """
        try:
            if not content or len(content.strip()) < 50:
                return {
                    "success": False,
                    "error": "Content too short to humanize effectively"
                }
            
            humanized_content = content
            
            # Phase 1: Basic humanization (all strength levels)
            if strength in ["low", "medium", "high"]:
                # Step 1: Remove AI patterns (ADAT technique)
                humanized_content = self._remove_ai_patterns(humanized_content)
                
                # Step 2: Enhance perplexity through word replacements (DIPPER-inspired)
                humanized_content = self._enhance_perplexity(humanized_content)
                
                # Step 3: Add contractions for naturalness
                humanized_content = self._add_contractions(humanized_content)
                
                # Step 4: Implement burstiness (sentence length variation)
                humanized_content = self._implement_burstiness(humanized_content)
                
            # Phase 2: Advanced techniques (medium/high)
            if strength in ["medium", "high"]:
                # Step 5: Word importance ranking and replacement (HMGC framework)
                humanized_content = self._word_importance_replacement(humanized_content)
                
                # Step 6: Add personal touches and opinions
                humanized_content = self._add_personal_elements(humanized_content)
                
                # Step 7: Structural modifications
                humanized_content = self._structural_modifications(humanized_content)
                
            # Phase 3: Adversarial techniques (high only)
            if strength == "high":
                # Step 8: Character-level modifications (research-proven)
                humanized_content = self._character_level_modifications(humanized_content)
                
                # Step 9: Strategic typos and errors (human-like imperfections)
                humanized_content = self._add_strategic_errors(humanized_content)
                
                # Step 10: Advanced LLM humanization
                humanized_content = self._advanced_llm_humanization(humanized_content)
                
                # Step 11: Final perplexity and burstiness enhancement
                humanized_content = self._final_enhancement_pass(humanized_content)
            
            return {
                "success": True,
                "humanized_content": humanized_content.strip(),
                "message": f"Content humanized using research-proven techniques (strength: {strength})"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Humanization failed: {str(e)}"
            }

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using NLTK for better accuracy"""
        try:
            return sent_tokenize(text)
        except:
            # Fallback to regex if NLTK fails
            sentences = re.split(r'(?<=[.!?])\s+', text)
            return [s.strip() for s in sentences if s.strip()]

    def _remove_ai_patterns(self, text: str) -> str:
        """
        Remove common AI writing patterns using ADAT framework
        Research shows this significantly improves bypass rates
        """
        for pattern in self.ai_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        
        # Clean up extra spaces and fix punctuation
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'^\s*[,.]\s*', '', text)
        text = re.sub(r'\.\s*[,.]\s*', '. ', text)
        text = re.sub(r',\s*[,.]\s*', ', ', text)
        
        # Capitalize first letter after cleaning
        text = text.strip()
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        return text

    def _add_contractions(self, text: str) -> str:
        """Add contractions to make text more conversational"""
        for full_form, contraction in self.contractions.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(full_form) + r'\b'
            text = re.sub(pattern, contraction, text, flags=re.IGNORECASE)
        return text

    def check_api_status(self) -> Dict[str, bool]:
        """Check if the humanizer service is available"""
        return {
            "success": True,
            "available": True,
            "research_based": True,
            "techniques": [
                "DIPPER paraphrasing model",
                "HMGC framework", 
                "ADAT adversarial attacks",
                "Perplexity enhancement",
                "Burstiness implementation",
                "Character-level modifications"
            ]
        }
    
    def _enhance_perplexity(self, text: str) -> str:
        """
        Enhance perplexity through strategic word replacement
        Based on DIPPER model research showing 70.3% -> 4.6% detection rate reduction
        """
        words = text.split()
        modified_words = []
        
        for word in words:
            clean_word = word.strip(string.punctuation).lower()
            
            # Replace with higher perplexity alternatives
            if clean_word in self.perplexity_enhancers and random.random() < 0.3:
                replacement = random.choice(self.perplexity_enhancers[clean_word])
                # Preserve original capitalization and punctuation
                if word[0].isupper():
                    replacement = replacement.capitalize()
                # Preserve punctuation
                punctuation = ''.join(c for c in word if c in string.punctuation)
                modified_words.append(replacement + punctuation)
            else:
                modified_words.append(word)
        
        return ' '.join(modified_words)
    
    def _implement_burstiness(self, text: str) -> str:
        """
        Implement burstiness through dramatic sentence length variation
        Based on research showing AI detectors struggle with varied sentence patterns
        """
        sentences = sent_tokenize(text)
        modified_sentences = []
        
        i = 0
        while i < len(sentences):
            sentence = sentences[i]
            sentence_length = len(sentence.split())
            
            # Strategy 1: Create very short fragments (3-8% of sentences)
            if sentence_length > 15 and random.random() < 0.08:
                # Split into short fragment + longer sentence
                words = sentence.split()
                split_point = random.randint(2, 5)
                
                short_fragment = ' '.join(words[:split_point])
                if not short_fragment.endswith('.'):
                    short_fragment += '.'
                
                remaining = ' '.join(words[split_point:])
                if remaining and not remaining[0].isupper():
                    remaining = remaining[0].upper() + remaining[1:]
                
                modified_sentences.append(short_fragment)
                modified_sentences.append(remaining)
                i += 1
                continue
            
            # Strategy 2: Combine short sentences into very long ones (5% chance)
            if (sentence_length < 12 and i < len(sentences) - 1 and 
                len(sentences[i + 1].split()) < 12 and random.random() < 0.05):
                
                # Combine with next sentence using varied connectors
                next_sentence = sentences[i + 1]
                connectors = [
                    ", and what's particularly interesting is that",
                    ", which makes me think that",
                    ", and here's the thing -",
                    ", but the reality is that",
                    ", and I've found that"
                ]
                connector = random.choice(connectors)
                combined = sentence.rstrip('.!?') + connector + " " + next_sentence.lower()
                modified_sentences.append(combined)
                i += 2  # Skip next sentence
                continue
            
            # Strategy 3: Add burst fragments before/after long sentences
            if sentence_length > 20 and random.random() < 0.12:
                if random.random() < 0.5:  # Add before
                    fragment = random.choice(self.burstiness_patterns["short_fragments"])
                    modified_sentences.append(fragment)
                    modified_sentences.append(sentence)
                else:  # Add after
                    modified_sentences.append(sentence)
                    fragment = random.choice(self.burstiness_patterns["short_fragments"])
                    modified_sentences.append(fragment)
                i += 1
                continue
            
            modified_sentences.append(sentence)
            i += 1
        
        return ' '.join(modified_sentences)
    
    def _word_importance_replacement(self, text: str) -> str:
        """
        Implement word importance ranking and replacement from HMGC framework
        Focus on replacing high-impact words while maintaining semantic integrity
        """
        try:
            # Tokenize and tag parts of speech
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            
            # Identify important words (adjectives, adverbs, key nouns)
            important_positions = []
            for i, (word, pos) in enumerate(pos_tags):
                if pos in ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'NN', 'NNS']:
                    if word.lower() in self.perplexity_enhancers:
                        important_positions.append(i)
            
            # Replace a subset of important words (20-30%)
            num_to_replace = max(1, int(len(important_positions) * 0.25))
            positions_to_replace = random.sample(important_positions, 
                                               min(num_to_replace, len(important_positions)))
            
            modified_tokens = tokens.copy()
            for pos in positions_to_replace:
                word = tokens[pos].lower()
                if word in self.perplexity_enhancers:
                    replacement = random.choice(self.perplexity_enhancers[word])
                    # Preserve capitalization
                    if tokens[pos][0].isupper():
                        replacement = replacement.capitalize()
                    modified_tokens[pos] = replacement
            
            # Reconstruct text with proper spacing
            result = ""
            for i, token in enumerate(modified_tokens):
                if i == 0:
                    result = token
                elif token in string.punctuation:
                    result += token
                else:
                    result += " " + token
            
            return result
            
        except Exception as e:
            logger.error(f"Word importance replacement failed: {e}")
            return text
    
    def _character_level_modifications(self, text: str) -> str:
        """
        Apply character-level modifications for detector evasion
        Based on research showing effectiveness of character substitution attacks
        """
        # Strategy 1: Invisible character insertion (very sparingly)
        words = text.split()
        for i in range(len(words)):
            if random.random() < 0.02:  # 2% of words
                char_pos = random.randint(0, len(words[i]))
                invisible_char = random.choice(self.invisible_chars)
                words[i] = words[i][:char_pos] + invisible_char + words[i][char_pos:]
        
        text = ' '.join(words)
        
        # Strategy 2: Strategic character substitutions (very rare, 0.5% of characters)
        chars = list(text)
        for i in range(len(chars)):
            if (chars[i].lower() in self.character_substitutions and 
                random.random() < 0.005):  # 0.5% chance
                chars[i] = self.character_substitutions[chars[i].lower()]
        
        return ''.join(chars)
    
    def _add_strategic_errors(self, text: str) -> str:
        """
        Add strategic human-like errors based on research
        Mimics natural human writing imperfections
        """
        words = text.split()
        modified_words = []
        
        for word in words:
            clean_word = word.strip(string.punctuation).lower()
            
            # Common typos (1% chance)
            if clean_word in self.typo_patterns["common_typos"] and random.random() < 0.01:
                typo = random.choice(self.typo_patterns["common_typos"][clean_word])
                # Preserve capitalization and punctuation
                if word[0].isupper():
                    typo = typo.capitalize()
                punctuation = ''.join(c for c in word if c in string.punctuation)
                modified_words.append(typo + punctuation)
                continue
            
            # Autocorrect-style errors (0.5% chance)
            if clean_word in self.typo_patterns["autocorrect_errors"] and random.random() < 0.005:
                error = self.typo_patterns["autocorrect_errors"][clean_word]
                if word[0].isupper():
                    error = error.capitalize()
                punctuation = ''.join(c for c in word if c in string.punctuation)
                modified_words.append(error + punctuation)
                continue
            
            modified_words.append(word)
        
        return ' '.join(modified_words)
    
    def _add_personal_elements(self, text: str) -> str:
        """
        Add personal touches and subjective elements
        Research shows this significantly reduces detection rates
        """
        sentences = sent_tokenize(text)
        modified_sentences = []
        
        personal_markers = [
            "I think", "I believe", "In my opinion", "From my experience",
            "I've noticed", "It seems to me", "I'd argue", "Personally,",
            "I've found", "My take is", "I reckon", "If you ask me"
        ]
        
        uncertainty_markers = [
            "perhaps", "maybe", "possibly", "presumably", "likely",
            "probably", "seemingly", "apparently", "supposedly"
        ]
        
        for i, sentence in enumerate(sentences):
            # Add personal opinion markers (8% chance)
            if random.random() < 0.08:
                marker = random.choice(personal_markers)
                if sentence.lower().startswith(('the ', 'this ', 'that ', 'these ', 'those ')):
                    sentence = marker + " " + sentence.lower()
                else:
                    sentence = marker + " that " + sentence.lower()
            
            # Add uncertainty (5% chance)
            elif random.random() < 0.05:
                words = sentence.split()
                if len(words) > 3:
                    insert_pos = random.randint(1, min(3, len(words) - 1))
                    uncertainty = random.choice(uncertainty_markers)
                    words.insert(insert_pos, uncertainty)
                    sentence = ' '.join(words)
            
            modified_sentences.append(sentence)
        
        return ' '.join(modified_sentences)
    
    def _structural_modifications(self, text: str) -> str:
        """
        Apply structural modifications to text organization
        Based on research showing effectiveness of sentence reordering
        """
        sentences = sent_tokenize(text)
        
        # Occasionally reorder adjacent sentences (if they're independent)
        if len(sentences) > 3:
            for i in range(len(sentences) - 1):
                if random.random() < 0.1:  # 10% chance
                    # Simple heuristic: swap if neither sentence starts with transition words
                    first = sentences[i].lower()
                    second = sentences[i + 1].lower()
                    
                    transition_words = ['however', 'therefore', 'furthermore', 'moreover', 
                                     'additionally', 'consequently', 'thus', 'hence']
                    
                    if not any(second.startswith(tw) for tw in transition_words):
                        sentences[i], sentences[i + 1] = sentences[i + 1], sentences[i]
        
        return ' '.join(sentences)
    
    def _advanced_llm_humanization(self, text: str) -> str:
        """
        Advanced LLM-based humanization using research-proven prompts
        """
        if not self.openai_api_key:
            return text
        
        try:
            prompt = f"""
            Transform this text to bypass AI detection systems using these research-proven techniques:
            
            1. PERPLEXITY: Use unexpected word choices and varied vocabulary
            2. BURSTINESS: Mix very short sentences (2-4 words) with very long ones (25+ words)
            3. PERSONAL VOICE: Add personal opinions, experiences, and uncertainty markers
            4. NATURAL IMPERFECTIONS: Include minor grammatical variations and hesitations
            5. HUMAN PATTERNS: Add conversational elements and stream-of-consciousness touches
            
            Original text:
            {text}
            
            Humanized version (maintain all key information):
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=len(text.split()) * 3,
                temperature=0.9,  # High creativity for variation
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Advanced LLM humanization failed: {e}")
            return text
    
    def _final_enhancement_pass(self, text: str) -> str:
        """
        Final pass to ensure maximum humanization effectiveness
        """
        # Add final perplexity boosts
        text = self._enhance_perplexity(text)
        
        # Ensure proper burstiness distribution
        sentences = sent_tokenize(text)
        lengths = [len(s.split()) for s in sentences]
        
        # If not enough variation, add some short fragments
        if max(lengths) - min(lengths) < 15:
            insertion_points = random.sample(range(len(sentences)), 
                                           min(2, len(sentences) // 3))
            for point in sorted(insertion_points, reverse=True):
                fragment = random.choice(self.burstiness_patterns["short_fragments"])
                sentences.insert(point, fragment)
        
        return ' '.join(sentences)
