import re
import random
import logging
from typing import Dict, List, Tuple, Set
from collections import Counter, defaultdict
import string

logger = logging.getLogger(__name__)

class HumanizerService:
    """
    Advanced humanizer targeting 80-90% LLM efficiency through sophisticated pattern recognition
    Uses context-aware transformations and multi-layered humanization techniques
    """
    
    def __init__(self):
        # Comprehensive AI pattern detection with context-aware replacements
        self.ai_patterns = {
            # Formal transitions with context sensitivity
            r'\bIn conclusion,?\s*': {
                'casual': ["So basically, ", "Bottom line - ", "To wrap up, ", "All in all, "],
                'confident': ["Here's what it comes down to: ", "The key takeaway? ", "What this means is "],
                'conversational': ["So there you have it - ", "At the end of the day, ", "When all's said and done, "]
            },
            r'\bFurthermore,?\s*': {
                'casual': ["Plus, ", "Also, ", "And, ", "What's more, "],
                'emphatic': ["And here's another thing - ", "On top of that, ", "Not only that, but "],
                'flow': ["Another point: ", "There's also ", "And don't forget "]
            },
            r'\bHowever,?\s*': {
                'casual': ["But, ", "Though, ", "Still, "],
                'contrasting': ["Here's the thing though - ", "But here's where it gets interesting: ", "Plot twist: "],
                'balanced': ["That said, ", "On the flip side, ", "But then again, "]
            },
            r'\bIt is important to note that\s*': {
                'direct': ["Keep in mind ", "Remember ", "Don't forget "],
                'casual': ["Here's the thing - ", "Quick note: ", "Oh, and "],
                'emphasis': ["This is crucial: ", "Pay attention to this - ", "Here's what matters: "]
            },
            r'\bAs we can see,?\s*': {
                'obvious': ["Clearly, ", "Obviously, ", "You can see "],
                'engaging': ["Notice how ", "Check this out - ", "Look at this: "],
                'analytical': ["This shows ", "This tells us ", "We're seeing "]
            }
        }
        
        # Context-sensitive word replacements with semantic awareness
        self.contextual_replacements = {
            'academic': {
                "utilize": ["use", "work with", "employ"],
                "demonstrate": ["show", "prove", "illustrate"],
                "ascertain": ["find out", "figure out", "determine"],
                "subsequently": ["then", "next", "after that"],
                "methodology": ["method", "approach", "way we do it"],
                "facilitate": ["help", "make easier", "enable"],
                "comprehensive": ["complete", "thorough", "full"],
                "implement": ["put in place", "use", "start using"],
                "advantageous": ["helpful", "beneficial", "good for"],
                "substantial": ["significant", "major", "big"],
            },
            'business': {
                "leverage": ["use", "take advantage of", "work with"],
                "synergies": ["benefits", "advantages", "good combinations"],
                "optimize": ["improve", "make better", "fine-tune"],
                "streamline": ["simplify", "make easier", "clean up"],
                "paradigm": ["model", "approach", "way of thinking"],
                "utilize": ["use", "work with", "employ"],
                "actionable": ["practical", "useful", "something you can do"],
                "scalable": ["can grow", "expandable", "flexible"],
            },
            'technical': {
                "parameters": ["settings", "options", "variables"],
                "configuration": ["setup", "arrangement", "how it's set up"],
                "optimization": ["improvement", "making it better", "fine-tuning"],
                "implementation": ["putting it in place", "setting it up", "making it work"],
                "architecture": ["structure", "design", "how it's built"],
                "framework": ["structure", "foundation", "basic setup"],
            }
        }
        
        # Advanced sentence transformation patterns
        self.sentence_transformers = [
            # Question-based engagement
            {
                'pattern': r'^([A-Z][^.!?]*\bis\b[^.!?]*\.)$',
                'transform': lambda m: f"Ever wonder {m.group(1).lower().replace(' is ', ' might be ')}?",
                'probability': 0.15
            },
            # Conversational interjections
            {
                'pattern': r'^(This|That|These|Those)\s+([^.!?]+\.)$',
                'transform': lambda m: f"You know what? {m.group(2).capitalize()}",
                'probability': 0.12
            },
            # Emphasis through restructuring
            {
                'pattern': r'^([^,]+),\s*which\s+([^.!?]+\.)$',
                'transform': lambda m: f"{m.group(1)}. And here's what's cool - it {m.group(2)}",
                'probability': 0.10
            }
        ]
        
        # Personality injection patterns with weighted selection
        self.personality_markers = {
            'confident': {
                'starters': ["Look, ", "Here's the deal - ", "The truth is, ", "Let me be clear: "],
                'hedges': ["I'm convinced that", "I'm pretty sure", "I'd bet that"],
                'weight': 0.3
            },
            'casual': {
                'starters': ["Honestly, ", "To be fair, ", "You know what? ", "Here's the thing - "],
                'hedges': ["I think", "seems like", "probably", "my guess is"],
                'weight': 0.4
            },
            'analytical': {
                'starters': ["Interestingly, ", "What's fascinating is ", "If you think about it, "],
                'hedges': ["appears to be", "suggests that", "indicates", "points to"],
                'weight': 0.3
            }
        }
        
        # Advanced burstiness with rhythm patterns
        self.rhythm_patterns = {
            'short_punch': ["Exactly.", "True.", "Bingo.", "Right?", "Makes sense.", "Obviously."],
            'medium_bridge': [
                "But here's where it gets interesting:",
                "Now, here's the key point:",
                "And this is where things get tricky:",
                "Here's what I mean by that:"
            ],
            'long_elaboration': [
                "What I find particularly fascinating about this whole situation is that",
                "If you really take a step back and look at the bigger picture, you'll notice that",
                "The thing that most people don't realize (and this is important) is that"
            ]
        }
        
        # Sophisticated flow connectors with emotional undertones
        self.flow_connectors = {
            'agreement': ["Absolutely", "Exactly", "That's right", "Precisely"],
            'contrast': ["But wait", "Hold on", "Here's the twist", "Plot twist"],
            'emphasis': ["Here's the kicker", "Get this", "Here's what's wild", "Check this out"],
            'transition': ["Speaking of which", "That reminds me", "On a related note", "While we're on the topic"]
        }
        
        # Natural contractions with context awareness
        self.smart_contractions = {
            r'\bdo not\b': "don't",
            r'\bwill not\b': "won't",
            r'\bcannot\b': "can't", 
            r'\byou are\b': "you're",
            r'\bwe are\b': "we're",
            r'\bthey are\b': "they're",
            r'\bit is\b': "it's",
            r'\bthat is\b': "that's",
            r'\bwhat is\b': "what's",
            r'\bwhere is\b': "where's",
            r'\bwho is\b': "who's",
            r'\bhow is\b': "how's",
            r'\blet us\b': "let's",
            r'\bwould have\b': "would've",
            r'\bcould have\b': "could've",
            r'\bshould have\b': "should've",
        }
        
        # Semantic clustering for intelligent word replacement
        self.semantic_clusters = {
            'positive_intensity': {
                'very good': ['excellent', 'outstanding', 'fantastic', 'amazing', 'brilliant'],
                'very bad': ['terrible', 'awful', 'horrible', 'atrocious', 'dreadful'],
                'very big': ['huge', 'massive', 'enormous', 'gigantic', 'colossal'],
                'very small': ['tiny', 'minuscule', 'microscopic', 'miniature']
            },
            'certainty_levels': {
                'definitely': ['absolutely', 'certainly', 'without a doubt', 'for sure'],
                'probably': ['likely', 'most likely', 'chances are', 'odds are'],
                'maybe': ['perhaps', 'possibly', 'might be', 'could be']
            }
        }

    def humanize_content(self, content: str, strength: str = "medium", personality: str = "balanced") -> Dict[str, str]:
        """
        Advanced humanization targeting 80-90% LLM efficiency
        
        Args:
            content: Text to humanize
            strength: "low", "medium", "high"
            personality: "casual", "confident", "analytical", "balanced"
        """
        try:
            if not content or len(content.strip()) < 20:
                return {"success": False, "error": "Content too short"}
            
            # Multi-pass humanization pipeline
            humanized = content
            context = self._analyze_content_context(humanized)
            
            # Phase 1: Core transformations (all levels)
            humanized = self._advanced_pattern_removal(humanized, context)
            humanized = self._contextual_word_replacement(humanized, context)
            humanized = self._smart_contractions(humanized, context)
            
            # Phase 2: Structural improvements (medium+)
            if strength in ["medium", "high"]:
                humanized = self._advanced_sentence_restructuring(humanized)
                humanized = self._inject_personality(humanized, personality)
                humanized = self._enhance_flow_and_rhythm(humanized)
                
            # Phase 3: Advanced techniques (high only)
            if strength == "high":
                humanized = self._semantic_enhancement(humanized)
                humanized = self._advanced_burstiness(humanized)
                humanized = self._natural_imperfection_injection(humanized)
                humanized = self._contextual_emphasis(humanized)
            
            # Final optimization
            humanized = self._final_polish(humanized)
            
            return {
                "success": True,
                "humanized_content": humanized,
                "context_detected": context,
                "transformations_applied": self._count_transformations(content, humanized),
                "message": f"Advanced humanization complete (strength: {strength}, personality: {personality})"
            }
            
        except Exception as e:
            logger.error(f"Advanced humanization failed: {e}")
            return {"success": False, "error": str(e)}

    def _analyze_content_context(self, text: str) -> Dict[str, float]:
        """Analyze content to determine context (academic, business, technical, casual)"""
        academic_indicators = ['research', 'study', 'analysis', 'methodology', 'framework', 'hypothesis']
        business_indicators = ['strategy', 'leverage', 'synergy', 'optimize', 'stakeholder', 'ROI']
        technical_indicators = ['system', 'implementation', 'configuration', 'architecture', 'parameters']
        
        text_lower = text.lower()
        word_count = len(text.split())
        
        academic_score = sum(text_lower.count(word) for word in academic_indicators) / word_count
        business_score = sum(text_lower.count(word) for word in business_indicators) / word_count
        technical_score = sum(text_lower.count(word) for word in technical_indicators) / word_count
        
        return {
            'academic': min(academic_score * 100, 1.0),
            'business': min(business_score * 100, 1.0),
            'technical': min(technical_score * 100, 1.0),
            'formality': self._calculate_formality_score(text)
        }

    def _calculate_formality_score(self, text: str) -> float:
        """Calculate formality score based on sentence structure and vocabulary"""
        formal_indicators = [
            r'\b(furthermore|moreover|additionally|consequently|therefore)\b',
            r'\b(utilize|implement|demonstrate|facilitate)\b',
            r'\b(it is important to note|it should be noted|as aforementioned)\b'
        ]
        
        formal_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in formal_indicators)
        avg_sentence_length = sum(len(s.split()) for s in re.split(r'[.!?]', text)) / max(len(re.split(r'[.!?]', text)), 1)
        
        return min((formal_count * 0.1 + avg_sentence_length * 0.05), 1.0)

    def _advanced_pattern_removal(self, text: str, context: Dict) -> str:
        """Context-aware AI pattern removal"""
        for pattern, replacements in self.ai_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                # Choose replacement style based on context
                if context['formality'] > 0.7:
                    style = 'confident'
                elif context['academic'] > 0.3:
                    style = 'analytical' if 'analytical' in replacements else 'casual'
                else:
                    style = 'casual'
                
                # Fallback to first available style
                if style not in replacements:
                    style = list(replacements.keys())[0]
                
                replacement = random.choice(replacements[style])
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE, count=1)
        
        return text

    def _contextual_word_replacement(self, text: str, context: Dict) -> str:
        """Replace words based on detected context"""
        # Determine primary context
        primary_context = max(context, key=lambda k: context[k] if k != 'formality' else 0)
        
        if primary_context in self.contextual_replacements:
            replacements = self.contextual_replacements[primary_context]
            
            for formal_word, alternatives in replacements.items():
                pattern = r'\b' + re.escape(formal_word) + r'\b'
                if re.search(pattern, text, re.IGNORECASE) and random.random() < 0.6:
                    replacement = random.choice(alternatives)
                    text = re.sub(pattern, replacement, text, flags=re.IGNORECASE, count=1)
        
        return text

    def _smart_contractions(self, text: str, context: Dict = None) -> str:
        """Apply contractions with context sensitivity"""
        if context is None:
            context = {}
        
        # More contractions in casual contexts
        contraction_probability = 0.8 if context.get('formality', 0) < 0.4 else 0.5
        
        for pattern, contraction in self.smart_contractions.items():
            if random.random() < contraction_probability:
                text = re.sub(pattern, contraction, text, flags=re.IGNORECASE)
        
        return text

    def _advanced_sentence_restructuring(self, text: str) -> str:
        """Apply sophisticated sentence transformations"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        modified_sentences = []
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            # Apply transformation patterns
            transformed = False
            for transformer in self.sentence_transformers:
                if random.random() < transformer['probability']:
                    match = re.match(transformer['pattern'], sentence)
                    if match:
                        sentence = transformer['transform'](match)
                        transformed = True
                        break
            
            # Smart sentence combining
            if (len(modified_sentences) > 0 and not transformed and 
                len(sentence.split()) < 10 and len(modified_sentences[-1].split()) < 12):
                
                if random.random() < 0.2:
                    connector = random.choice([" and ", " but ", " so ", " - and "])
                    combined = modified_sentences[-1].rstrip('.!?') + connector + sentence.lower()
                    modified_sentences[-1] = combined
                    continue
            
            modified_sentences.append(sentence)
        
        return ' '.join(modified_sentences)

    def _inject_personality(self, text: str, personality: str) -> str:
        """Inject personality markers based on selected style"""
        if personality == "balanced":
            # Mix of all personalities
            available_personalities = list(self.personality_markers.keys())
            personality = random.choices(available_personalities, 
                                       weights=[self.personality_markers[p]['weight'] for p in available_personalities])[0]
        
        if personality not in self.personality_markers:
            personality = 'casual'
        
        markers = self.personality_markers[personality]
        sentences = re.split(r'(?<=[.!?])\s+', text)
        modified_sentences = []
        
        for sentence in sentences:
            if not sentence.strip():
                continue
            
            # Add personality starters (10% chance)
            if random.random() < 0.1:
                starter = random.choice(markers['starters'])
                sentence = starter + sentence.lower()
            
            # Add hedging/confidence markers (8% chance)
            elif random.random() < 0.08:
                hedge = random.choice(markers['hedges'])
                words = sentence.split()
                if len(words) > 3:
                    insert_pos = random.randint(1, min(3, len(words)))
                    words.insert(insert_pos, hedge)
                    sentence = ' '.join(words)
            
            modified_sentences.append(sentence)
        
        return ' '.join(modified_sentences)

    def _enhance_flow_and_rhythm(self, text: str) -> str:
        """Enhance natural flow with rhythm patterns"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        enhanced_sentences = []
        
        i = 0
        while i < len(sentences):
            sentence = sentences[i]
            if not sentence.strip():
                i += 1
                continue
            
            word_count = len(sentence.split())
            
            # Add rhythm elements based on sentence length
            if word_count > 15 and random.random() < 0.15:
                # Add short punch after long sentence
                enhanced_sentences.append(sentence)
                punch = random.choice(self.rhythm_patterns['short_punch'])
                enhanced_sentences.append(punch)
            
            elif word_count < 8 and i < len(sentences) - 1 and random.random() < 0.12:
                # Add bridge before short sentence
                bridge = random.choice(self.rhythm_patterns['medium_bridge'])
                enhanced_sentences.append(bridge)
                enhanced_sentences.append(sentence)
            
            else:
                enhanced_sentences.append(sentence)
            
            i += 1
        
        return ' '.join(enhanced_sentences)

    def _semantic_enhancement(self, text: str) -> str:
        """Apply semantic clustering for intelligent replacements"""
        for cluster_type, clusters in self.semantic_clusters.items():
            for phrase, alternatives in clusters.items():
                pattern = r'\b' + re.escape(phrase) + r'\b'
                if re.search(pattern, text, re.IGNORECASE) and random.random() < 0.4:
                    replacement = random.choice(alternatives)
                    text = re.sub(pattern, replacement, text, flags=re.IGNORECASE, count=1)
        
        return text

    def _advanced_burstiness(self, text: str) -> str:
        """Create sophisticated sentence length variation"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        lengths = [len(s.split()) for s in sentences if s.strip()]
        
        if not lengths:
            return text
        
        avg_length = sum(lengths) / len(lengths)
        variation = max(lengths) - min(lengths)
        
        # If not enough variation, inject some
        if variation < 12:
            modified_sentences = []
            for i, sentence in enumerate(sentences):
                if not sentence.strip():
                    continue
                
                words = sentence.split()
                
                # Break very long sentences occasionally
                if len(words) > avg_length * 1.5 and random.random() < 0.3:
                    break_point = len(words) // 2
                    first_part = ' '.join(words[:break_point]) + '.'
                    second_part = ' '.join(words[break_point:])
                    if second_part[0].islower():
                        second_part = second_part[0].upper() + second_part[1:]
                    
                    modified_sentences.extend([first_part, second_part])
                else:
                    modified_sentences.append(sentence)
            
            return ' '.join(modified_sentences)
        
        return text

    def _natural_imperfection_injection(self, text: str) -> str:
        """Add subtle natural imperfections (very sparingly)"""
        # Add occasional hesitation markers
        hesitations = ["um, ", "well, ", "you know, ", "I mean, "]
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for i, sentence in enumerate(sentences):
            if random.random() < 0.03:  # Very rare
                hesitation = random.choice(hesitations)
                words = sentence.split()
                if len(words) > 4:
                    insert_pos = random.randint(1, 3)
                    words.insert(insert_pos, hesitation.strip())
                    sentences[i] = ' '.join(words)
        
        return ' '.join(sentences)

    def _contextual_emphasis(self, text: str) -> str:
        """Add contextual emphasis and engagement"""
        # Add occasional emphasis through italics/caps (simulated with markers)
        emphasis_words = ['really', 'very', 'extremely', 'absolutely', 'definitely']
        
        for word in emphasis_words:
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, text, re.IGNORECASE) and random.random() < 0.1:
                text = re.sub(pattern, word.upper(), text, flags=re.IGNORECASE, count=1)
        
        return text

    def _final_polish(self, text: str) -> str:
        """Final polishing and cleanup"""
        # Fix spacing and punctuation
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s+([.!?,:;])', r'\1', text)
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        # Ensure proper capitalization
        sentences = re.split(r'(?<=[.!?])\s+', text)
        polished_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence[0].islower():
                sentence = sentence[0].upper() + sentence[1:]
            polished_sentences.append(sentence)
        
        return ' '.join(polished_sentences).strip()

    def _count_transformations(self, original: str, transformed: str) -> int:
        """Count number of transformations applied"""
        # Simple diff-based counting
        orig_words = set(original.lower().split())
        trans_words = set(transformed.lower().split())
        return len(orig_words.symmetric_difference(trans_words))

    def check_api_status(self) -> Dict[str, bool]:
        """Enhanced API status check"""
        return {
            "success": True,
            "available": True,
            "efficiency_target": "80-90%",
            "advanced_features": [
                "Context-aware pattern detection",
                "Semantic clustering",
                "Personality injection",
                "Advanced burstiness",
                "Flow enhancement",
                "Natural imperfection simulation"
            ]
        }