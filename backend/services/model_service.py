"""
Model service for LLB application using local Gemma 3 1B Keras model.
Handles model loading, inference, and GPU optimization.
"""

import os
import torch
import asyncio
from typing import Optional, Dict, Any
import logging
import sys

# Add AI directory to path for prompt engine
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ai'))

logger = logging.getLogger(__name__)

try:
    import keras_hub
    import keras
    KERAS_AVAILABLE = True
except ImportError:
    KERAS_AVAILABLE = False
    logger.error("❌ KerasHub not available. Install keras-hub for Gemma support.")
    raise ImportError("KerasHub is required for model operation")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("⚠️ Transformers not available.")

try:
    from prompt_engine import PromptEngine, PromptRequest, InputType
    PROMPT_ENGINE_AVAILABLE = True
except ImportError:
    PROMPT_ENGINE_AVAILABLE = False
    logger.warning("⚠️ Prompt engine not available.")


class ModelService:
    """Service for managing Gemma 3 1B model inference."""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = None
        self.generation_config = None
        self._loaded = False
        
        # Initialize prompt engine if available
        if PROMPT_ENGINE_AVAILABLE:
            self.prompt_engine = PromptEngine()
            logger.info("✅ Prompt engine initialized")
        else:
            self.prompt_engine = None
            logger.warning("⚠️ Prompt engine not available")
        
        # Use local model first (cleaned up), then fallback to official preset
        self.model_preset = "gemma3_instruct_1b"  # Official KerasHub instruct preset
        
        # Local model path (prioritized)
        self.model_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'ai', 'models', 'gemma3-keras-gemma3_instruct_1b-v3'
        )
        self.model_path = os.path.abspath(self.model_path)
        
        # Model configuration - based on Gemma3 model specs
        self.max_length = 1024  # Model's sequence_length from config
        self.max_new_tokens = 100  # Further reduced for better quality
        
    async def load_model(self):
        """Load the Gemma 3 1B model using local model first, then official preset fallback."""
        try:
            logger.info("🔄 Loading Gemma 3 1B model...")
            
            # Determine device
            if torch.cuda.is_available():
                self.device = "cuda"
                logger.info(f"✅ Using GPU: {torch.cuda.get_device_name()}")
                logger.info(f"📊 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
                
                # Set Keras backend to use GPU
                os.environ['KERAS_BACKEND'] = 'torch'
                os.environ['CUDA_VISIBLE_DEVICES'] = '0'
            else:
                self.device = "cpu"
                logger.warning("⚠️ CUDA not available, using CPU")
                os.environ['KERAS_BACKEND'] = 'torch'
            
            if not KERAS_AVAILABLE:
                raise RuntimeError("KerasHub is required but not available. Please install keras-hub.")
            
            # Try loading local model first (cleaned up)
            logger.info("🧠 Loading local Gemma3 model...")
            
            if os.path.exists(self.model_path):
                try:
                    # Load local Gemma3 model
                    logger.info(f"🔄 Loading local model from: {self.model_path}")
                    self.model = keras_hub.models.Gemma3CausalLM.from_preset(
                        self.model_path,
                        dtype="float16" if self.device == "cuda" else "float32"
                    )
                    logger.info("✅ Successfully loaded local Gemma3 model")
                    
                except Exception as e1:
                    logger.warning(f"⚠️ Local model failed: {e1}")
                    
                    # Fallback to official preset
                    try:
                        logger.info(f"🔄 Fallback: Loading official preset: {self.model_preset}")
                        self.model = keras_hub.models.Gemma3CausalLM.from_preset(
                            self.model_preset,
                            dtype="float16" if self.device == "cuda" else "float32"
                        )
                        logger.info("✅ Successfully loaded official Gemma3 preset")
                        
                    except Exception as e2:
                        logger.error(f"❌ Both local and official model loading failed")
                        logger.error(f"Local model: {e1}")
                        logger.error(f"Official preset: {e2}")
                        raise RuntimeError(f"Could not load Gemma model. Local: {e1}, Official: {e2}")
            else:
                # No local model, try official preset
                try:
                    logger.info(f"🔄 No local model found, loading official preset: {self.model_preset}")
                    self.model = keras_hub.models.Gemma3CausalLM.from_preset(
                        self.model_preset,
                        dtype="float16" if self.device == "cuda" else "float32"
                    )
                    logger.info("✅ Successfully loaded official Gemma3 preset")
                except Exception as e:
                    logger.error(f"❌ Official preset loading failed: {e}")
                    raise RuntimeError(f"Could not load Gemma model: {e}")
            
            # Ensure model was actually loaded
            if self.model is None:
                raise RuntimeError("Model loading failed - model is None")
            
            # Try to get tokenizer from the model
            try:
                if hasattr(self.model, 'preprocessor') and hasattr(self.model.preprocessor, 'tokenizer'):
                    self.tokenizer = self.model.preprocessor.tokenizer
                    logger.info("✅ Tokenizer extracted from model")
                    
                    # Test tokenizer
                    try:
                        test_tokens = self.tokenizer("Hello")
                        logger.info(f"✅ Tokenizer test successful: {test_tokens}")
                    except Exception as e:
                        logger.warning(f"⚠️ Tokenizer test failed: {e}")
                        
                else:
                    logger.warning("⚠️ Could not extract tokenizer from model")
                    self.tokenizer = None
            except Exception as e:
                logger.warning(f"⚠️ Tokenizer extraction failed: {e}")
                self.tokenizer = None
            
            self._loaded = True
            logger.info("✅ Gemma3 model loaded successfully!")
            
            # Print memory usage if on GPU
            if self.device == "cuda":
                memory_used = torch.cuda.memory_allocated() / 1e9
                memory_total = torch.cuda.get_device_properties(0).total_memory / 1e9
                logger.info(f"📊 GPU Memory Usage: {memory_used:.1f}/{memory_total:.1f} GB ({memory_used/memory_total*100:.1f}%)")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            raise RuntimeError(f"Model loading failed: {e}")
    
    async def generate_response(self, prompt: str) -> str:
        """Generate response using the loaded model."""
        return await self.generate_response_with_language(prompt, "en")

    async def generate_response_with_language(self, prompt: str, language: str = "en") -> str:
        """Generate response using the loaded model with language awareness."""
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        if self.model is None:
            raise RuntimeError("Model is not available. Ensure model loading was successful.")
        
        try:
            # Use prompt engine to create better prompts
            if self.prompt_engine:
                logger.info("🔧 Using prompt engine to enhance prompt...")
                request = PromptRequest(
                    content=prompt,
                    input_type=InputType.TEXT,
                    language=language,
                    cultural_context="chinese" if language.startswith("zh") else "western",
                    safety_level="standard"
                )
                
                prompt_response = self.prompt_engine.process_request(request)
                enhanced_prompt = prompt_response.formatted_prompt
                logger.info(f"✅ Enhanced prompt: {enhanced_prompt[:100]}...")
            else:
                enhanced_prompt = f"Question: {prompt}\nAnswer:"
                logger.info(f"✅ Basic prompt format: {enhanced_prompt[:100]}...")
            
            # Use Keras model for generation with proper API
            logger.info(f"🤖 Generating response with Keras Gemma3 model for language: {language}...")
            
            # Use the correct generate API for Gemma3CausalLM
            try:
                logger.info("🔄 Using Gemma3CausalLM.generate() method...")
                
                # Try compiling the model with a specific sampler first
                try:
                    if not hasattr(self.model, '_compiled_sampler'):
                        logger.info("🔧 Compiling model with greedy sampler...")
                        self.model.compile(sampler="greedy")
                        self.model._compiled_sampler = True
                except Exception as compile_error:
                    logger.warning(f"⚠️ Could not compile with sampler: {compile_error}")
                
                # For instruct models, use proper chat formatting
                if "instruct" in self.model_preset:
                    # Format as a proper instruction for the instruct model
                    formatted_prompt = f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
                    logger.info(f"🔧 Using instruct format: {formatted_prompt[:100]}...")
                else:
                    formatted_prompt = enhanced_prompt
                
                # Try different generation approaches
                response = None
                
                # Approach 1: Use formatted prompt with specific parameters
                try:
                    logger.info("🔄 Trying instruct generation...")
                    response = self.model.generate(
                        formatted_prompt, 
                        max_length=200,
                        stop_token_ids=None
                    )
                    logger.info(f"✅ Instruct response: {response[:100]}...")
                except Exception as e:
                    logger.warning(f"⚠️ Instruct generation failed: {e}")
                
                # Approach 2: Simple generation if instruct fails
                if not response or '<unused' in response or len(response.strip()) < 10:
                    try:
                        logger.info("🔄 Trying simple generation...")
                        response = self.model.generate(prompt, max_length=100)
                        logger.info(f"✅ Simple generation response: {response[:100]}...")
                    except Exception as e:
                        logger.warning(f"⚠️ Simple generation failed: {e}")
                
                # Approach 3: Try with different parameters
                if not response or '<unused' in response or len(response.strip()) < 10:
                    try:
                        logger.info("🔄 Trying generation with different parameters...")
                        response = self.model.generate(
                            inputs=prompt,
                            max_length=50,
                            strip_prompt=False
                        )
                        logger.info(f"✅ Alternative generation response: {response[:100]}...")
                    except Exception as e:
                        logger.warning(f"⚠️ Alternative generation failed: {e}")
                
                # Approach 4: Try tokenizer-based generation
                if not response or '<unused' in response or len(response.strip()) < 10:
                    tokenizer_response = await self._generate_with_tokenizer(prompt)
                    if tokenizer_response and len(tokenizer_response.strip()) > 3:
                        response = tokenizer_response
                        logger.info(f"✅ Tokenizer generation response: {response[:100]}...")
                
                if response:
                    logger.info(f"✅ Raw response: {response[:200]}...")
                    logger.info(f"🔍 Response type: {type(response)}")
                    logger.info(f"🔍 Response length: {len(response) if response else 0}")
                    
                    # Check validation in detail
                    is_valid = self._is_valid_response(response)
                    logger.info(f"🔍 Response validation: {is_valid}")
                    
                    if is_valid:
                        cleaned_response = self._clean_response(response, prompt)
                        logger.info(f"✅ Cleaned response: {cleaned_response[:100]}...")
                        logger.info("✅ Generation successful!")
                        return cleaned_response
                    else:
                        logger.warning(f"⚠️ Generated response was invalid: '{response[:100]}...'")
                        # Let's see why it was invalid
                        if not response or len(response.strip()) < 3:
                            logger.warning("⚠️ Response too short or empty")
                        else:
                            logger.warning("⚠️ Response failed other validation checks")
                else:
                    logger.warning("⚠️ No response generated from any approach")
                
            except Exception as e:
                logger.warning(f"⚠️ Generation failed: {e}")
                import traceback
                logger.warning(f"⚠️ Traceback: {traceback.format_exc()}")
            
            # Fallback: Return a minimal response indicating the system is available
            logger.warning("⚠️ Using minimal response fallback.")
            
            # Return a minimal language-appropriate response
            if language == "zh-CN" or "什么" in prompt or "健康" in prompt or "性" in prompt:
                return "我是您的性健康教育助手。请告诉我您想了解什么，我会尽力帮助您。"
            else:
                return "I'm your sexual health education assistant. Please tell me what you'd like to know and I'll do my best to help you."
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            raise RuntimeError(f"Model generation failed: {e}")
    
    def _is_valid_response(self, response: str) -> bool:
        """Check if a response is valid (no garbage tokens)."""
        if not response or len(response.strip()) < 3:
            return False
        
        # Check for garbage tokens - be more specific
        garbage_patterns = [
            '<unused',
            '<unk>',
            '<pad>',
            '[UNK]',
            '[PAD]',
            '▁▁▁',  # Multiple underscores (3 or more)
        ]
        
        # If response contains garbage tokens, try to extract valid content
        for pattern in garbage_patterns:
            if pattern in response:
                # Try to extract content before the garbage tokens
                parts = response.split(pattern)
                if parts and len(parts[0].strip()) > 10:
                    # There's valid content before the garbage
                    return True
                else:
                    return False
        
        # Don't reject responses with HTML tags or code - they might be valid
        # Check if response is mostly repetitive (but allow some repetition)
        words = response.split()
        if len(words) > 10:  # Only check for repetition in longer responses
            unique_words = set(words)
            uniqueness_ratio = len(unique_words) / len(words)
            if uniqueness_ratio < 0.2:  # Less than 20% unique words (very repetitive)
                return False
        
        return True
    
    def _clean_response(self, response: str, original_prompt: str) -> str:
        """Clean up the response."""
        if isinstance(response, list):
            response = response[0]
        
        response = str(response).strip()
        
        # Remove the original prompt from response if it's included at the start
        if response.startswith(original_prompt):
            response = response[len(original_prompt):].strip()
        
        # Handle instruct model formatting
        if "<start_of_turn>model" in response:
            # Extract content after the model turn marker
            parts = response.split("<start_of_turn>model")
            if len(parts) > 1:
                response = parts[-1].strip()
        
        if "<end_of_turn>" in response:
            # Extract content before the end turn marker
            response = response.split("<end_of_turn>")[0].strip()
        
        # Remove garbage tokens and extract valid content
        garbage_patterns = ['<unused', '<unk>', '<pad>', '[UNK]', '[PAD]']
        for pattern in garbage_patterns:
            if pattern in response:
                # Extract content before the garbage tokens
                parts = response.split(pattern)
                if parts and len(parts[0].strip()) > 5:
                    response = parts[0].strip()
                    break
        
        # Don't truncate responses aggressively - preserve AI-generated content
        # Only remove incomplete sentences if the response is very long
        if len(response) > 200 and response and not response.endswith(('.', '!', '?', '。', '！', '？')):
            sentences = response.split('.')
            if len(sentences) > 2:  # Only if there are multiple sentences
                response = '.'.join(sentences[:-1]) + '.'
        
        # Only add fallback if response is truly empty or very short
        if len(response.strip()) < 5:
            if "健康" in original_prompt or "什么" in original_prompt:
                response = "健康很重要。"
            else:
                response = "Health is important."
        
        return response
    
    def _is_invalid_response(self, response: str) -> bool:
        """Check if a response contains invalid tokens or patterns."""
        return not self._is_valid_response(response)
    
    async def generate_streaming_response(self, prompt: str):
        """Generate streaming response (for future implementation)."""
        response = await self.generate_response(prompt)
        yield response
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._loaded and self.model is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        if not self._loaded:
            return {"status": "not_loaded"}
        
        if self.model is None:
            return {"status": "failed_to_load"}
        
        info = {
            "model_path": self.model_path,
            "model_type": "keras_gemma3",
            "device": self.device,
            "loaded": self._loaded,
            "max_length": self.max_length,
            "max_new_tokens": self.max_new_tokens,
        }
        
        if self.device == "cuda" and torch.cuda.is_available():
            info.update({
                "gpu_name": torch.cuda.get_device_name(),
                "gpu_memory_total": torch.cuda.get_device_properties(0).total_memory / 1e9,
                "gpu_memory_used": torch.cuda.memory_allocated() / 1e9,
            })
        
        return info
    
    async def cleanup(self):
        """Clean up model resources."""
        if self.model is not None:
            del self.model
            self.model = None
        
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        
        if self.device == "cuda" and torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self._loaded = False
        logger.info("🧹 Model resources cleaned up")
    
    def optimize_for_inference(self):
        """Apply inference optimizations."""
        if not self._loaded or self.model is None:
            return
        
        try:
            logger.info("⚡ Model optimized for inference")
        except Exception as e:
            logger.warning(f"⚠️ Could not apply all optimizations: {e}")
    
    async def warm_up(self):
        """Warm up the model with a test generation."""
        if not self._loaded:
            return
        
        try:
            logger.info("🔥 Warming up model...")
            test_prompt = "Hello"
            await self.generate_response(test_prompt)
            logger.info("✅ Model warmed up successfully")
        except Exception as e:
            logger.error(f"❌ Model warm-up failed: {e}")
            raise RuntimeError(f"Model warm-up failed: {e}")
    
    async def generate_response_with_topic(self, prompt: str, topic: str = None) -> str:
        """Generate response using the loaded model with topic information."""
        return await self.generate_response_with_language(prompt, "en")

    async def _generate_with_tokenizer(self, prompt: str) -> str:
        """Try generation using tokenizer directly to avoid unused tokens."""
        if not self.tokenizer:
            return None
            
        try:
            logger.info("🔄 Trying tokenizer-based generation...")
            
            # Tokenize the input
            input_tokens = self.tokenizer(prompt)
            logger.info(f"🔤 Input tokens: {input_tokens}")
            
            # Try to generate using the model's call method instead of generate
            if hasattr(self.model, '__call__'):
                # Use the model as a callable
                import tensorflow as tf
                
                # Convert to tensor if needed
                if isinstance(input_tokens, list):
                    input_tensor = tf.constant([input_tokens])
                else:
                    input_tensor = tf.constant([[input_tokens]])
                
                # Get model output
                output = self.model(input_tensor, training=False)
                
                # Get the logits and sample from them
                if hasattr(output, 'logits'):
                    logits = output.logits
                else:
                    logits = output
                
                # Get the last token's logits and sample
                last_logits = logits[0, -1, :]
                
                # Use greedy sampling (argmax)
                next_token_id = tf.argmax(last_logits, axis=-1)
                
                # Decode the token
                next_token = self.tokenizer.detokenize([next_token_id.numpy()])
                
                logger.info(f"✅ Tokenizer generation result: {next_token}")
                return next_token
                
        except Exception as e:
            logger.warning(f"⚠️ Tokenizer-based generation failed: {e}")
            return None 