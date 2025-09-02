"""
Knowledge Service for AI-powered sexual health knowledge search and updates
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from app.core.logging import get_logger
from app.db.session import SessionLocal
from app.services.ai_service import AIService

logger = get_logger(__name__)


class KnowledgeService:
    """Service for AI-powered knowledge search and database updates."""

    def __init__(self):
        self.ai_service = AIService()
        self.search_topics = [
            "sexual health education",
            "contraception methods",
            "STI prevention",
            "reproductive health",
            "consent education",
            "sexual anatomy",
            "pregnancy prevention",
            "sexual safety"
        ]

    async def search_and_update_knowledge(self, manual_query: Optional[str] = None) -> Dict[str, Any]:
        """Search for new sexual health knowledge and update database."""
        db = SessionLocal()
        
        try:
            # Create update record
            update_record = {
                'update_type': 'manual' if manual_query else 'scheduled',
                'search_query': manual_query or 'automated_search',
                'status': 'running',
                'started_at': datetime.utcnow()
            }
            
            # Insert update record
            db.execute(
                "INSERT INTO knowledge_updates (update_type, search_query, status, started_at) VALUES (:update_type, :search_query, :status, :started_at)",
                update_record
            )
            db.commit()
            
            # Get the update ID
            update_id = db.execute("SELECT lastval()").scalar()
            
            entries_added = 0
            entries_updated = 0
            
            # Search topics to query
            topics = [manual_query] if manual_query else self.search_topics
            
            for topic in topics:
                try:
                    # Generate knowledge content using AI
                    knowledge_data = await self._generate_knowledge_content(topic)
                    
                    for entry in knowledge_data:
                        # Check if entry exists
                        existing = db.execute(
                            "SELECT id FROM knowledge_entries WHERE title = :title AND language = :language",
                            {'title': entry['title'], 'language': entry['language']}
                        ).fetchone()
                        
                        if existing:
                            # Update existing entry
                            db.execute(
                                """UPDATE knowledge_entries SET 
                                   content = :content, summary = :summary, keywords = :keywords,
                                   quality_score = :quality_score, updated_at = :updated_at
                                   WHERE id = :id""",
                                {**entry, 'id': existing[0], 'updated_at': datetime.utcnow()}
                            )
                            entries_updated += 1
                        else:
                            # Insert new entry
                            db.execute(
                                """INSERT INTO knowledge_entries 
                                   (title, content, summary, category, language, keywords, quality_score, source_type, created_at, updated_at)
                                   VALUES (:title, :content, :summary, :category, :language, :keywords, :quality_score, :source_type, :created_at, :updated_at)""",
                                {**entry, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()}
                            )
                            entries_added += 1
                    
                    await asyncio.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"Error processing topic {topic}: {e}")
                    continue
            
            # Update completion record
            db.execute(
                """UPDATE knowledge_updates SET 
                   entries_added = :entries_added, entries_updated = :entries_updated,
                   status = :status, completed_at = :completed_at
                   WHERE id = :id""",
                {
                    'entries_added': entries_added,
                    'entries_updated': entries_updated,
                    'status': 'completed',
                    'completed_at': datetime.utcnow(),
                    'id': update_id
                }
            )
            db.commit()
            
            result = {
                'status': 'success',
                'entries_added': entries_added,
                'entries_updated': entries_updated,
                'topics_processed': len(topics),
                'update_id': update_id
            }
            
            logger.info(f"Knowledge update completed: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Knowledge update failed: {e}")
            # Update error status
            if 'update_id' in locals():
                db.execute(
                    "UPDATE knowledge_updates SET status = :status, error_message = :error, completed_at = :completed_at WHERE id = :id",
                    {'status': 'failed', 'error': str(e), 'completed_at': datetime.utcnow(), 'id': update_id}
                )
                db.commit()
            raise
        finally:
            db.close()

    async def _generate_knowledge_content(self, topic: str) -> List[Dict[str, Any]]:
        """Generate knowledge content for a specific topic using AI."""
        
        # Initialize AI service if needed
        if not self.ai_service.is_ready():
            await self.ai_service.initialize()
        
        # Generate content for both English and Chinese
        entries = []
        
        for language in ['en', 'zh-CN']:
            try:
                # Create knowledge generation prompt
                if language == 'en':
                    prompt = f"""Generate comprehensive, accurate sexual health education content about: {topic}

Please provide:
1. A clear, informative title
2. Detailed educational content (300-500 words)
3. A brief summary (50-100 words)
4. 5-8 relevant keywords
5. Category classification

Focus on:
- Medical accuracy
- Age-appropriate information
- Cultural sensitivity
- Safety and health
- Evidence-based information

Format as JSON with fields: title, content, summary, keywords, category"""
                else:
                    prompt = f"""生成关于以下主题的全面、准确的性健康教育内容：{topic}

请提供：
1. 清晰、信息丰富的标题
2. 详细的教育内容（300-500字）
3. 简要摘要（50-100字）
4. 5-8个相关关键词
5. 类别分类

重点关注：
- 医学准确性
- 适龄信息
- 文化敏感性
- 安全与健康
- 循证信息

格式为JSON，包含字段：title, content, summary, keywords, category"""

                # Generate response
                response = await self.ai_service.generate_response(prompt, language)
                
                # Parse AI response
                content_data = self._parse_ai_response(response['response'], topic, language)
                if content_data:
                    entries.append(content_data)
                    
            except Exception as e:
                logger.error(f"Error generating content for {topic} in {language}: {e}")
                continue
        
        return entries

    def _parse_ai_response(self, ai_response: str, topic: str, language: str) -> Optional[Dict[str, Any]]:
        """Parse AI response into structured knowledge entry."""
        try:
            # Try to extract JSON from response
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = ai_response[start_idx:end_idx]
                data = json.loads(json_str)
            else:
                # Fallback: create structured data from text
                data = {
                    'title': f"Sexual Health: {topic}",
                    'content': ai_response,
                    'summary': ai_response[:200] + "..." if len(ai_response) > 200 else ai_response,
                    'keywords': topic.split(),
                    'category': 'general'
                }
            
            # Ensure required fields and add metadata
            entry = {
                'title': data.get('title', f"Sexual Health: {topic}"),
                'content': data.get('content', ai_response),
                'summary': data.get('summary', data.get('content', '')[:200]),
                'category': data.get('category', 'general'),
                'language': language,
                'keywords': data.get('keywords', topic.split()),
                'quality_score': 0.8,  # Default quality score
                'source_type': 'ai_generated'
            }
            
            return entry
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return None

    async def get_knowledge_entries(self, 
                                  category: Optional[str] = None,
                                  language: Optional[str] = None,
                                  limit: int = 50) -> List[Dict[str, Any]]:
        """Get knowledge entries from database."""
        db = SessionLocal()
        
        try:
            query = "SELECT * FROM knowledge_entries WHERE is_active = true"
            params = {}
            
            if category:
                query += " AND category = :category"
                params['category'] = category
                
            if language:
                query += " AND language = :language"
                params['language'] = language
            
            query += " ORDER BY quality_score DESC, updated_at DESC LIMIT :limit"
            params['limit'] = limit
            
            result = db.execute(query, params).fetchall()
            
            entries = []
            for row in result:
                entries.append({
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'summary': row[3],
                    'category': row[4],
                    'language': row[5],
                    'keywords': row[8],
                    'quality_score': row[9],
                    'created_at': row[12],
                    'updated_at': row[13]
                })
            
            return entries
            
        finally:
            db.close()

    async def get_update_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get knowledge update history."""
        db = SessionLocal()
        
        try:
            result = db.execute(
                "SELECT * FROM knowledge_updates ORDER BY started_at DESC LIMIT :limit",
                {'limit': limit}
            ).fetchall()
            
            updates = []
            for row in result:
                updates.append({
                    'id': row[0],
                    'update_type': row[1],
                    'entries_added': row[2],
                    'entries_updated': row[3],
                    'search_query': row[4],
                    'status': row[5],
                    'error_message': row[6],
                    'started_at': row[7],
                    'completed_at': row[8]
                })
            
            return updates
            
        finally:
            db.close()