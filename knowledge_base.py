"""
Knowledge Base Module - User research storage and AI-powered querying
Stores notes, articles, and research with semantic search capabilities
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeBase:
    """Personal investment research knowledge base with AI-powered search"""
    
    def __init__(self, storage_dir: str = "./data/knowledge_base"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.notes_file = self.storage_dir / "notes.json"
        self.articles_file = self.storage_dir / "articles.json"
        self.research_file = self.storage_dir / "research.json"
        
        # Initialize storage
        self._init_storage()
    
    def _init_storage(self):
        """Initialize storage files if they don't exist"""
        files = [self.notes_file, self.articles_file, self.research_file]
        
        for file_path in files:
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump([], f, indent=2)
                logger.info(f"Initialized {file_path}")
    
    def add_note(self, title: str, content: str, tags: List[str] = None, 
                  related_tickers: List[str] = None) -> str:
        """
        Add a personal note to the knowledge base
        
        Args:
            title (str): Note title
            content (str): Note content
            tags (List[str]): Optional tags for categorization
            related_tickers (List[str]): Related stock tickers
            
        Returns:
            str: Note ID
        """
        try:
            note_id = str(uuid.uuid4())
            note = {
                'id': note_id,
                'type': 'note',
                'title': title,
                'content': content,
                'tags': tags or [],
                'related_tickers': related_tickers or [],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            notes = self._load_data(self.notes_file)
            notes.append(note)
            self._save_data(self.notes_file, notes)
            
            logger.info(f"Added note: {title}")
            return note_id
            
        except Exception as e:
            logger.error(f"Error adding note: {str(e)}")
            raise
    
    def add_article(self, title: str, url: str, summary: str = None, 
                    content: str = None, tags: List[str] = None,
                    related_tickers: List[str] = None) -> str:
        """
        Add an article or research link to the knowledge base
        
        Args:
            title (str): Article title
            url (str): Article URL
            summary (str): Optional summary
            content (str): Optional extracted content
            tags (List[str]): Optional tags
            related_tickers (List[str]): Related stock tickers
            
        Returns:
            str: Article ID
        """
        try:
            article_id = str(uuid.uuid4())
            article = {
                'id': article_id,
                'type': 'article',
                'title': title,
                'url': url,
                'summary': summary,
                'content': content,
                'tags': tags or [],
                'related_tickers': related_tickers or [],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            articles = self._load_data(self.articles_file)
            articles.append(article)
            self._save_data(self.articles_file, articles)
            
            logger.info(f"Added article: {title}")
            return article_id
            
        except Exception as e:
            logger.error(f"Error adding article: {str(e)}")
            raise
    
    def add_research(self, title: str, content: str, source: str = None,
                     tags: List[str] = None, related_tickers: List[str] = None) -> str:
        """
        Add research or analysis to the knowledge base
        
        Args:
            title (str): Research title
            content (str): Research content
            source (str): Source of research
            tags (List[str]): Optional tags
            related_tickers (List[str]): Related stock tickers
            
        Returns:
            str: Research ID
        """
        try:
            research_id = str(uuid.uuid4())
            research = {
                'id': research_id,
                'type': 'research',
                'title': title,
                'content': content,
                'source': source,
                'tags': tags or [],
                'related_tickers': related_tickers or [],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            research_items = self._load_data(self.research_file)
            research_items.append(research)
            self._save_data(self.research_file, research_items)
            
            logger.info(f"Added research: {title}")
            return research_id
            
        except Exception as e:
            logger.error(f"Error adding research: {str(e)}")
            raise
    
    def search_knowledge_base(self, query: str, search_type: str = "all", 
                             ticker: str = None, tags: List[str] = None) -> List[Dict]:
        """
        Search the knowledge base for relevant information
        
        Args:
            query (str): Search query
            search_type (str): Type of content to search ('all', 'notes', 'articles', 'research')
            ticker (str): Filter by related ticker
            tags (List[str]): Filter by tags
            
        Returns:
            List[Dict]: Matching items
        """
        try:
            results = []
            
            # Determine which collections to search
            collections = []
            if search_type == "all" or search_type == "notes":
                collections.append(("notes", self.notes_file))
            if search_type == "all" or search_type == "articles":
                collections.append(("articles", self.articles_file))
            if search_type == "all" or search_type == "research":
                collections.append(("research", self.research_file))
            
            # Search each collection
            for collection_name, file_path in collections:
                items = self._load_data(file_path)
                
                for item in items:
                    if self._matches_search(item, query, ticker, tags):
                        # Add relevance score
                        item['relevance_score'] = self._calculate_relevance(item, query)
                        item['collection'] = collection_name
                        results.append(item)
            
            # Sort by relevance score
            results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            logger.info(f"Search returned {len(results)} results for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
            return []
    
    def _matches_search(self, item: Dict, query: str, ticker: str = None, 
                       tags: List[str] = None) -> bool:
        """Check if an item matches the search criteria"""
        query_lower = query.lower()
        
        # Check if query matches title or content
        title_match = query_lower in item.get('title', '').lower()
        content_match = query_lower in item.get('content', '').lower()
        summary_match = query_lower in item.get('summary', '').lower()
        
        # Check ticker filter
        ticker_match = True
        if ticker:
            ticker_match = ticker.upper() in [t.upper() for t in item.get('related_tickers', [])]
        
        # Check tags filter
        tags_match = True
        if tags:
            item_tags = [t.lower() for t in item.get('tags', [])]
            search_tags = [t.lower() for t in tags]
            tags_match = any(tag in item_tags for tag in search_tags)
        
        return (title_match or content_match or summary_match) and ticker_match and tags_match
    
    def _calculate_relevance(self, item: Dict, query: str) -> float:
        """Calculate relevance score for search results"""
        query_terms = query.lower().split()
        score = 0.0
        
        # Title matches get highest weight
        title = item.get('title', '').lower()
        for term in query_terms:
            if term in title:
                score += 3.0
        
        # Content matches get medium weight
        content = item.get('content', '').lower()
        for term in query_terms:
            if term in content:
                score += 1.0
        
        # Summary matches get medium weight
        summary = item.get('summary', '').lower()
        for term in query_terms:
            if term in summary:
                score += 1.5
        
        # Recency bonus
        try:
            created_at = datetime.fromisoformat(item.get('created_at', ''))
            days_old = (datetime.now() - created_at).days
            if days_old < 30:
                score += 0.5
            elif days_old < 90:
                score += 0.2
        except:
            pass
        
        return score
    
    def get_item(self, item_id: str, item_type: str = None) -> Optional[Dict]:
        """Get a specific item by ID"""
        try:
            if item_type == "notes" or item_type is None:
                notes = self._load_data(self.notes_file)
                for note in notes:
                    if note['id'] == item_id:
                        return note
            
            if item_type == "articles" or item_type is None:
                articles = self._load_data(self.articles_file)
                for article in articles:
                    if article['id'] == item_id:
                        return article
            
            if item_type == "research" or item_type is None:
                research_items = self._load_data(self.research_file)
                for research in research_items:
                    if research['id'] == item_id:
                        return research
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting item {item_id}: {str(e)}")
            return None
    
    def update_item(self, item_id: str, updates: Dict, item_type: str) -> bool:
        """Update an existing item"""
        try:
            if item_type == "notes":
                file_path = self.notes_file
            elif item_type == "articles":
                file_path = self.articles_file
            elif item_type == "research":
                file_path = self.research_file
            else:
                return False
            
            items = self._load_data(file_path)
            
            for i, item in enumerate(items):
                if item['id'] == item_id:
                    # Update fields
                    for key, value in updates.items():
                        if key in item:
                            item[key] = value
                    
                    # Update timestamp
                    item['updated_at'] = datetime.now().isoformat()
                    
                    self._save_data(file_path, items)
                    logger.info(f"Updated {item_type}: {item_id}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating item {item_id}: {str(e)}")
            return False
    
    def delete_item(self, item_id: str, item_type: str) -> bool:
        """Delete an item from the knowledge base"""
        try:
            if item_type == "notes":
                file_path = self.notes_file
            elif item_type == "articles":
                file_path = self.articles_file
            elif item_type == "research":
                file_path = self.research_file
            else:
                return False
            
            items = self._load_data(file_path)
            original_count = len(items)
            
            items = [item for item in items if item['id'] != item_id]
            
            if len(items) < original_count:
                self._save_data(file_path, items)
                logger.info(f"Deleted {item_type}: {item_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deleting item {item_id}: {str(e)}")
            return False
    
    def get_all_items(self, item_type: str = "all") -> List[Dict]:
        """Get all items of a specific type"""
        try:
            if item_type == "notes":
                return self._load_data(self.notes_file)
            elif item_type == "articles":
                return self._load_data(self.articles_file)
            elif item_type == "research":
                return self._load_data(self.research_file)
            elif item_type == "all":
                all_items = []
                all_items.extend(self._load_data(self.notes_file))
                all_items.extend(self._load_data(self.articles_file))
                all_items.extend(self._load_data(self.research_file))
                return all_items
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting all items: {str(e)}")
            return []
    
    def _load_data(self, file_path: Path) -> List[Dict]:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {str(e)}")
            return []
    
    def _save_data(self, file_path: Path, data: List[Dict]):
        """Save data to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving data to {file_path}: {str(e)}")
            raise

# Convenience functions
def create_knowledge_base(storage_dir: str = "./data/knowledge_base") -> KnowledgeBase:
    """Create a new knowledge base instance"""
    return KnowledgeBase(storage_dir)

if __name__ == "__main__":
    # Test the knowledge base
    kb = create_knowledge_base()
    
    # Add some test data
    note_id = kb.add_note(
        title="Apple Q4 Earnings Analysis",
        content="Apple reported strong Q4 earnings with iPhone sales up 15%...",
        tags=["earnings", "technology", "analysis"],
        related_tickers=["AAPL"]
    )
    
    article_id = kb.add_article(
        title="Tech Sector Outlook 2024",
        url="https://example.com/tech-outlook-2024",
        summary="Analysis of technology sector trends and investment opportunities",
        tags=["sector analysis", "technology", "outlook"],
        related_tickers=["AAPL", "MSFT", "GOOGL"]
    )
    
    # Search the knowledge base
    results = kb.search_knowledge_base("Apple earnings", ticker="AAPL")
    print(f"Found {len(results)} results:")
    for result in results:
        print(f"- {result['title']} (Score: {result.get('relevance_score', 0):.2f})")
