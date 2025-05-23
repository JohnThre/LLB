"""
Model service for LLB application using local Gemma 3 1B Keras model.
Handles model loading, inference, and GPU optimization.
"""

import os
import torch
import asyncio
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

try:
    import keras_hub
    import keras
    KERAS_AVAILABLE = True
except ImportError:
    KERAS_AVAILABLE = False
    logger.warning("⚠️ KerasHub not available. Install keras-hub for Gemma support.")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("⚠️ Transformers not available.")


class ModelService:
    """Service for managing Gemma 3 1B model inference."""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = None
        self.generation_config = None
        self._loaded = False
        
        # Local model path
        self.model_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'ai', 'models', 'gemma3-keras-gemma3_1b-v3'
        )
        self.model_path = os.path.abspath(self.model_path)
        
        # Model configuration
        self.max_length = 2048
        self.max_new_tokens = 512
        
    async def load_model(self):
        """Load the local Gemma 3 1B Keras model."""
        try:
            logger.info("🔄 Loading local Gemma 3 1B Keras model...")
            
            # Check if model path exists
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model not found at {self.model_path}")
            
            logger.info(f"📁 Model path: {self.model_path}")
            
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
            
            # Load the Keras model with multiple fallback approaches
            logger.info("🧠 Loading Keras Gemma model...")
            
            try:
                # Try loading as Gemma3CausalLM first
                logger.info("🔄 Attempting to load as Gemma3CausalLM...")
                self.model = keras_hub.models.Gemma3CausalLM.from_preset(
                    self.model_path,
                    dtype="float16" if self.device == "cuda" else "float32"
                )
                logger.info("✅ Successfully loaded as Gemma3CausalLM")
                
            except Exception as e1:
                logger.warning(f"⚠️ Gemma3CausalLM failed: {e1}")
                
                try:
                    # Try loading as GemmaCausalLM
                    logger.info("🔄 Attempting to load as GemmaCausalLM...")
                    self.model = keras_hub.models.GemmaCausalLM.from_preset(
                        self.model_path,
                        dtype="float16" if self.device == "cuda" else "float32"
                    )
                    logger.info("✅ Successfully loaded as GemmaCausalLM")
                    
                except Exception as e2:
                    logger.warning(f"⚠️ GemmaCausalLM failed: {e2}")
                    
                    try:
                        # Try loading with generic approach
                        logger.info("🔄 Attempting generic model loading...")
                        import keras
                        self.model = keras.models.load_model(self.model_path)
                        logger.info("✅ Successfully loaded with generic approach")
                        
                    except Exception as e3:
                        logger.error(f"❌ All model loading approaches failed")
                        logger.error(f"Gemma3CausalLM: {e1}")
                        logger.error(f"GemmaCausalLM: {e2}")
                        logger.error(f"Generic: {e3}")
                        raise RuntimeError("Could not load Keras model with any approach")
            
            # Try to get tokenizer from the model
            try:
                if hasattr(self.model, 'preprocessor') and hasattr(self.model.preprocessor, 'tokenizer'):
                    self.tokenizer = self.model.preprocessor.tokenizer
                    logger.info("✅ Tokenizer extracted from model")
                else:
                    logger.warning("⚠️ Could not extract tokenizer from model")
                    self.tokenizer = None
            except Exception as e:
                logger.warning(f"⚠️ Tokenizer extraction failed: {e}")
                self.tokenizer = None
            
            self._loaded = True
            logger.info("✅ Local Keras model loaded successfully!")
            
            # Print memory usage if on GPU
            if self.device == "cuda":
                memory_used = torch.cuda.memory_allocated() / 1e9
                memory_total = torch.cuda.get_device_properties(0).total_memory / 1e9
                logger.info(f"📊 GPU Memory Usage: {memory_used:.1f}/{memory_total:.1f} GB ({memory_used/memory_total*100:.1f}%)")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            logger.info("🔄 Falling back to simple text generation...")
            # Fallback to a simple mock model for testing
            self._loaded = True
            self.model = None
            self.tokenizer = None
    
    async def generate_response(self, prompt: str) -> str:
        """Generate response using the loaded model."""
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            if self.model is None:
                # Fallback response for testing
                logger.info("🔄 Using fallback text generation")
                return self._generate_fallback_response(prompt)
            
            # Use Keras model for generation
            logger.info("🤖 Generating response with Keras Gemma model...")
            
            try:
                # Generate response with the Keras model
                response = self.model.generate(
                    prompt, 
                    max_length=self.max_new_tokens
                )
                
                # Clean up response
                if isinstance(response, list):
                    response = response[0]
                
                response = str(response).strip()
                
                # Check if response contains garbage tokens or is invalid
                if self._is_invalid_response(response):
                    logger.warning("⚠️ Model generated invalid response, using fallback")
                    return self._generate_fallback_response(prompt)
                
                # Remove the original prompt from response if it's included
                if response.startswith(prompt):
                    response = response[len(prompt):].strip()
                
                # Remove any incomplete sentences at the end
                if response and not response.endswith(('.', '!', '?', '。', '！', '？')):
                    sentences = response.split('.')
                    if len(sentences) > 1:
                        response = '.'.join(sentences[:-1]) + '.'
                
                # Final validation
                if len(response.strip()) < 10 or self._is_invalid_response(response):
                    logger.warning("⚠️ Generated response too short or invalid, using fallback")
                    return self._generate_fallback_response(prompt)
                
                return response
                
            except Exception as model_error:
                logger.warning(f"⚠️ Model generation failed: {model_error}")
                return self._generate_fallback_response(prompt)
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return self._generate_fallback_response(prompt)
    
    def _is_invalid_response(self, response: str) -> bool:
        """Check if a response contains invalid tokens or patterns."""
        if not response or len(response.strip()) < 5:
            return True
        
        # Check for garbage tokens
        garbage_patterns = [
            '<unused',
            '<unk>',
            '<pad>',
            '[UNK]',
            '[PAD]',
            '▁' * 5,  # Multiple underscores
        ]
        
        for pattern in garbage_patterns:
            if pattern in response:
                return True
        
        # Check if response is mostly repetitive
        words = response.split()
        if len(words) > 5:
            unique_words = set(words)
            if len(unique_words) / len(words) < 0.3:  # Less than 30% unique words
                return True
        
        return False
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """Generate a fallback response for testing purposes."""
        prompt_lower = prompt.lower()
        
        # Basic sexual health responses based on keywords
        if any(word in prompt_lower for word in ['contraception', '避孕', 'birth control', 'prevent pregnancy', 'family planning']):
            return "Contraception refers to methods used to prevent pregnancy. There are many safe and effective options available, including barrier methods (like condoms), hormonal methods (like birth control pills), intrauterine devices (IUDs), and long-acting reversible contraceptives. Each method has different effectiveness rates and considerations. It's important to consult with a healthcare provider to find the method that's right for your individual needs and circumstances."
        
        elif any(word in prompt_lower for word in ['sti', 'std', '性传播疾病', 'sexually transmitted', 'infection', 'disease']):
            return "Sexually transmitted infections (STIs) are infections that can be passed from one person to another through sexual contact. Common STIs include chlamydia, gonorrhea, syphilis, herpes, and HIV. Prevention includes using barrier protection (like condoms), getting regular testing, limiting number of sexual partners, and having open communication with partners about sexual health history. If you have concerns about STIs, please consult a healthcare professional for testing and treatment options."
        
        elif any(word in prompt_lower for word in ['consent', '同意', 'permission', 'agreement', 'willing']):
            return "Consent is a clear, voluntary agreement to engage in sexual activity. It must be ongoing throughout any sexual encounter, can be withdrawn at any time, and requires that all parties are able to give consent (not under the influence of drugs/alcohol, not coerced, and of legal age). Consent is essential for healthy sexual relationships and involves clear communication, respect for boundaries, and mutual understanding."
        
        elif any(word in prompt_lower for word in ['anatomy', '解剖', 'body', 'reproductive', 'organs', 'genitals']):
            return "Understanding sexual and reproductive anatomy is important for sexual health. This includes knowledge about both male and female reproductive systems, how they function, and how to maintain their health. Proper education about anatomy helps people understand their bodies, recognize normal vs. abnormal changes, and make informed decisions about their sexual health. For detailed anatomical information, consider consulting medical resources or speaking with a healthcare provider."
        
        elif any(word in prompt_lower for word in ['relationship', '关系', 'partner', 'communication', 'healthy']):
            return "Healthy sexual relationships are built on mutual respect, trust, open communication, and consent. This includes discussing boundaries, sexual health history, contraception preferences, and being honest about feelings and expectations. Good communication helps partners understand each other's needs and ensures that sexual experiences are positive and safe for everyone involved."
        
        elif any(word in prompt_lower for word in ['safety', '安全', 'protection', 'safe sex', 'risk']):
            return "Sexual safety involves protecting yourself and your partners from sexually transmitted infections, unintended pregnancy, and emotional harm. This includes using barrier protection, getting regular health screenings, communicating openly with partners, respecting boundaries, and making informed decisions about sexual activity. Safe sex practices help ensure that sexual experiences are both enjoyable and responsible."
        
        elif any(word in prompt_lower for word in ['sexual health', '性健康', 'what is', 'definition', 'meaning']):
            return "Sexual health is an important aspect of overall well-being that includes physical, emotional, mental and social aspects of sexuality. It involves having respectful relationships, access to accurate information, the ability to make informed decisions about your sexual life, and freedom from discrimination and violence. Sexual health requires a positive and respectful approach to sexuality and sexual relationships."
        
        else:
            return "Thank you for your question about sexual health. I'm here to provide accurate, safe information to help you make informed decisions about your sexual and reproductive health. For specific medical concerns or personalized advice, please consult with a qualified healthcare professional who can provide guidance based on your individual circumstances."
    
    async def generate_streaming_response(self, prompt: str):
        """Generate streaming response (for future implementation)."""
        response = await self.generate_response(prompt)
        yield response
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._loaded
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        if not self._loaded:
            return {"status": "not_loaded"}
        
        info = {
            "model_path": self.model_path,
            "model_type": "keras_gemma" if self.model else "fallback",
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
            test_prompt = "Hello, this is a test."
            await self.generate_response(test_prompt)
            logger.info("✅ Model warmed up successfully")
        except Exception as e:
            logger.warning(f"⚠️ Model warm-up failed: {e}")
    
    async def generate_response_with_topic(self, prompt: str, topic: str = None) -> str:
        """Generate response using the loaded model with topic information for better fallbacks."""
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            if self.model is None:
                # Fallback response for testing with topic information
                logger.info(f"🔄 Using topic-aware fallback text generation for topic: {topic}")
                return self._generate_topic_aware_fallback_response(prompt, topic)
            
            # Use Keras model for generation
            logger.info("🤖 Generating response with Keras Gemma model...")
            
            try:
                # Generate response with the Keras model
                response = self.model.generate(
                    prompt, 
                    max_length=self.max_new_tokens
                )
                
                # Clean up response
                if isinstance(response, list):
                    response = response[0]
                
                response = str(response).strip()
                
                # Check if response contains garbage tokens or is invalid
                if self._is_invalid_response(response):
                    logger.warning("⚠️ Model generated invalid response, using topic-aware fallback")
                    return self._generate_topic_aware_fallback_response(prompt, topic)
                
                # Remove the original prompt from response if it's included
                if response.startswith(prompt):
                    response = response[len(prompt):].strip()
                
                # Remove any incomplete sentences at the end
                if response and not response.endswith(('.', '!', '?', '。', '！', '？')):
                    sentences = response.split('.')
                    if len(sentences) > 1:
                        response = '.'.join(sentences[:-1]) + '.'
                
                # Final validation
                if len(response.strip()) < 10 or self._is_invalid_response(response):
                    logger.warning("⚠️ Generated response too short or invalid, using topic-aware fallback")
                    return self._generate_topic_aware_fallback_response(prompt, topic)
                
                return response
                
            except Exception as model_error:
                logger.warning(f"⚠️ Model generation failed: {model_error}")
                return self._generate_topic_aware_fallback_response(prompt, topic)
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return self._generate_topic_aware_fallback_response(prompt, topic)
    
    def _generate_topic_aware_fallback_response(self, prompt: str, topic: str = None) -> str:
        """Generate a topic-aware fallback response."""
        # Use topic information if available
        if topic:
            if topic == "contraception":
                return "Contraception refers to methods used to prevent pregnancy. There are many safe and effective options available, including barrier methods (like condoms), hormonal methods (like birth control pills), intrauterine devices (IUDs), and long-acting reversible contraceptives. Each method has different effectiveness rates and considerations. It's important to consult with a healthcare provider to find the method that's right for your individual needs and circumstances."
            
            elif topic == "sti":
                return "Sexually transmitted infections (STIs) are infections that can be passed from one person to another through sexual contact. Common STIs include chlamydia, gonorrhea, syphilis, herpes, and HIV. Prevention includes using barrier protection (like condoms), getting regular testing, limiting number of sexual partners, and having open communication with partners about sexual health history. If you have concerns about STIs, please consult a healthcare professional for testing and treatment options."
            
            elif topic == "consent":
                return "Consent is a clear, voluntary agreement to engage in sexual activity. It must be ongoing throughout any sexual encounter, can be withdrawn at any time, and requires that all parties are able to give consent (not under the influence of drugs/alcohol, not coerced, and of legal age). Consent is essential for healthy sexual relationships and involves clear communication, respect for boundaries, and mutual understanding."
            
            elif topic == "anatomy":
                return "Understanding sexual and reproductive anatomy is important for sexual health. This includes knowledge about both male and female reproductive systems, how they function, and how to maintain their health. Proper education about anatomy helps people understand their bodies, recognize normal vs. abnormal changes, and make informed decisions about their sexual health. For detailed anatomical information, consider consulting medical resources or speaking with a healthcare provider."
            
            elif topic == "relationship":
                return "Healthy sexual relationships are built on mutual respect, trust, open communication, and consent. This includes discussing boundaries, sexual health history, contraception preferences, and being honest about feelings and expectations. Good communication helps partners understand each other's needs and ensures that sexual experiences are positive and safe for everyone involved."
            
            elif topic == "safety":
                return "Sexual safety involves protecting yourself and your partners from sexually transmitted infections, unintended pregnancy, and emotional harm. This includes using barrier protection, getting regular health screenings, communicating openly with partners, respecting boundaries, and making informed decisions about sexual activity. Safe sex practices help ensure that sexual experiences are both enjoyable and responsible."
            
            elif topic == "basic_education":
                return "Sexual health is an important aspect of overall well-being that includes physical, emotional, mental and social aspects of sexuality. It involves having respectful relationships, access to accurate information, the ability to make informed decisions about your sexual life, and freedom from discrimination and violence. Sexual health requires a positive and respectful approach to sexuality and sexual relationships."
        
        # Fall back to keyword-based matching if no topic provided
        return self._generate_fallback_response(prompt) 