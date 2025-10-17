"""
WorldWatcher - Signal Detection System
Monitors global developer activity and detects patterns/needs

This is the "senses" layer that feeds GENESIS-SOVEREIGN's autonomous creation engine.
"""

import asyncio
import feedparser
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, AsyncGenerator
from collections import Counter
import os

try:
    from github import Github
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

try:
    import praw
    REDDIT_AVAILABLE = True
except ImportError:
    REDDIT_AVAILABLE = False


class WorldWatcher:
    """
    Watches developer activity across multiple sources and detects needs.
    Transforms passive data streams into actionable creation signals.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.signal_buffer = []
        self.pattern_tracker = Counter()

        # Initialize APIs
        self.github_client = None
        self.reddit_client = None

        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize API clients with available credentials"""
        # GitHub
        github_token = self.config.get('github_token') or os.getenv('GITHUB_TOKEN')
        if github_token and GITHUB_AVAILABLE:
            try:
                self.github_client = Github(github_token)
                print("✓ GitHub API connected")
            except Exception as e:
                print(f"⚠️  GitHub API failed: {e}")

        # Reddit
        reddit_id = self.config.get('reddit_client_id') or os.getenv('REDDIT_CLIENT_ID')
        reddit_secret = self.config.get('reddit_client_secret') or os.getenv('REDDIT_CLIENT_SECRET')
        if reddit_id and reddit_secret and REDDIT_AVAILABLE:
            try:
                self.reddit_client = praw.Reddit(
                    client_id=reddit_id,
                    client_secret=reddit_secret,
                    user_agent="GENESIS-SOVEREIGN/1.0"
                )
                print("✓ Reddit API connected")
            except Exception as e:
                print(f"⚠️  Reddit API failed: {e}")

    async def monitor_signals(self, interval: int = 60) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Main monitoring loop - continuously watches for signals

        Args:
            interval: Seconds between checks

        Yields:
            Signal dictionaries when patterns are detected
        """
        print(f"\n🌐 WorldWatcher activated - monitoring global developer signals")
        print(f"   Check interval: {interval}s")

        iteration = 0
        while True:
            iteration += 1
            print(f"\n[Scan {iteration}] {datetime.now().strftime('%H:%M:%S')}")

            # Gather signals from all sources
            github_signals = await self.check_github_trending()
            hn_signals = await self.check_hackernews()
            so_signals = await self.check_stackoverflow()
            reddit_signals = await self.check_reddit_programming()

            # Combine and analyze
            all_signals = github_signals + hn_signals + so_signals + reddit_signals

            if all_signals:
                # Detect patterns
                pattern = self.detect_need_pattern(all_signals)

                if pattern and pattern['confidence'] >= 0.6:
                    signal = {
                        'type': 'developer_need',
                        'pattern': pattern,
                        'sources': all_signals,
                        'timestamp': datetime.now().isoformat(),
                        'confidence': pattern['confidence']
                    }

                    print(f"📡 SIGNAL DETECTED: {pattern['summary']}")
                    print(f"   Confidence: {pattern['confidence']:.1%}")

                    yield signal

            await asyncio.sleep(interval)

    async def check_github_trending(self) -> List[Dict[str, Any]]:
        """Check GitHub trending repositories"""
        signals = []

        try:
            if not self.github_client:
                return signals

            # Get trending repos (starred in last 7 days)
            query = f"created:>{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} stars:>100"
            repos = self.github_client.search_repositories(query=query, sort='stars', order='desc')

            for repo in list(repos)[:10]:  # Top 10
                signals.append({
                    'source': 'github',
                    'type': 'trending_repo',
                    'name': repo.full_name,
                    'description': repo.description,
                    'stars': repo.stargazers_count,
                    'language': repo.language,
                    'topics': repo.get_topics()
                })

            print(f"  GitHub: {len(signals)} trending repos")

        except Exception as e:
            print(f"  GitHub error: {e}")

        return signals

    async def check_hackernews(self) -> List[Dict[str, Any]]:
        """Check HackerNews front page"""
        signals = []

        try:
            # Get top stories
            response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=10)
            story_ids = response.json()[:20]  # Top 20

            for story_id in story_ids:
                story_response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json', timeout=5)
                story = story_response.json()

                if story and story.get('title'):
                    signals.append({
                        'source': 'hackernews',
                        'type': 'trending_story',
                        'title': story['title'],
                        'url': story.get('url', ''),
                        'score': story.get('score', 0),
                        'comments': story.get('descendants', 0)
                    })

            print(f"  HackerNews: {len(signals)} stories")

        except Exception as e:
            print(f"  HackerNews error: {e}")

        return signals

    async def check_stackoverflow(self) -> List[Dict[str, Any]]:
        """Check StackOverflow recent questions"""
        signals = []

        try:
            response = requests.get(
                'https://api.stackexchange.com/2.3/questions',
                params={
                    'order': 'desc',
                    'sort': 'activity',
                    'site': 'stackoverflow',
                    'pagesize': 20,
                    'tagged': 'python;javascript;api;rest'
                },
                timeout=10
            )

            data = response.json()

            for question in data.get('items', []):
                signals.append({
                    'source': 'stackoverflow',
                    'type': 'question',
                    'title': question['title'],
                    'tags': question['tags'],
                    'score': question['score'],
                    'views': question['view_count']
                })

            print(f"  StackOverflow: {len(signals)} questions")

        except Exception as e:
            print(f"  StackOverflow error: {e}")

        return signals

    async def check_reddit_programming(self) -> List[Dict[str, Any]]:
        """Check programming subreddits"""
        signals = []

        try:
            if not self.reddit_client:
                return signals

            # Check multiple programming subreddits
            subreddits = ['programming', 'python', 'javascript', 'webdev']

            for subreddit_name in subreddits:
                subreddit = self.reddit_client.subreddit(subreddit_name)

                for post in subreddit.hot(limit=10):
                    signals.append({
                        'source': 'reddit',
                        'subreddit': subreddit_name,
                        'title': post.title,
                        'score': post.score,
                        'comments': post.num_comments,
                        'url': post.url
                    })

            print(f"  Reddit: {len(signals)} posts")

        except Exception as e:
            print(f"  Reddit error: {e}")

        return signals

    def detect_need_pattern(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze signals to detect developer needs/patterns

        Returns pattern with confidence score
        """
        if not signals:
            return None

        # Extract keywords from all signals
        keywords = []
        for signal in signals:
            title = signal.get('title', '') or signal.get('description', '') or signal.get('name', '')
            keywords.extend(title.lower().split())

        # Find most common themes
        keyword_freq = Counter(keywords)
        top_keywords = keyword_freq.most_common(10)

        # Calculate confidence based on frequency and diversity
        total_signals = len(signals)
        max_freq = top_keywords[0][1] if top_keywords else 0
        confidence = min(max_freq / total_signals, 1.0)

        # Generate summary
        if top_keywords:
            top_words = [word for word, _ in top_keywords[:5] if len(word) > 3]
            summary = f"Multiple developers discussing: {', '.join(top_words[:3])}"
        else:
            summary = "General developer activity detected"

        return {
            'summary': summary,
            'keywords': dict(top_keywords[:5]),
            'confidence': confidence,
            'signal_count': total_signals,
            'sources': list(set(s['source'] for s in signals))
        }

    def extract_actionable_need(self, pattern: Dict[str, Any]) -> str:
        """
        Convert a detected pattern into an actionable project specification

        Args:
            pattern: Detected pattern from detect_need_pattern()

        Returns:
            Project specification string
        """
        keywords = list(pattern.get('keywords', {}).keys())

        # Simple heuristics to generate project ideas
        if 'api' in keywords or 'rest' in keywords:
            return "Create a REST API microservice with authentication and CRUD operations"
        elif 'auth' in keywords or 'jwt' in keywords:
            return "Create a JWT authentication system with refresh tokens"
        elif 'database' in keywords or 'sql' in keywords:
            return "Create a database migration tool with versioning support"
        elif 'docker' in keywords or 'container' in keywords:
            return "