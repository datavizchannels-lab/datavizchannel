import random
import os
from typing import Dict, List, Tuple

class TemplateManager:
    """Manage video templates to avoid content repetition"""
    
    def __init__(self):
        self.templates = {
            'backgrounds': {
                'black': {'type': 'solid', 'color': 'black'},
                'dark_blue': {'type': 'solid', 'color': '#0a0a2a'},
                'dark_purple': {'type': 'solid', 'color': '#1a0a2a'},
                'matrix': {'type': 'gradient', 'colors': ['#000000', '#001100', '#003300']},
                'sunset': {'type': 'gradient', 'colors': ['#1a0033', '#330066', '#660099']},
                'ocean': {'type': 'gradient', 'colors': ['#001a33', '#003366', '#004d99']}
            },
            'voices': [
                'en-US-JennyNeural',
                'en-US-GuyNeural', 
                'en-US-AriaNeural',
                'en-US-DavisNeural',
                'en-GB-SoniaNeural',
                'en-GB-RyanNeural'
            ],
            'chart_styles': {
                'neon_green': {'line': '#00ff88', 'fill': 'rgba(0, 255, 136, 0.1)'},
                'neon_blue': {'line': '#00aaff', 'fill': 'rgba(0, 170, 255, 0.1)'},
                'neon_purple': {'line': '#aa00ff', 'fill': 'rgba(170, 0, 255, 0.1)'},
                'fire_orange': {'line': '#ff6600', 'fill': 'rgba(255, 102, 0, 0.1)'},
                'electric_pink': {'line': '#ff0066', 'fill': 'rgba(255, 0, 102, 0.1)'}
            },
            'script_templates': {
                'bitcoin_focus': [
                    "Bitcoin is trading at ${price:,}, {change_direction} {abs_change:.1f} percent today.",
                    "Let's look at Bitcoin. Currently at ${price:,}, with a {change_direction} of {abs_change:.1f} percent.",
                    "Bitcoin update: ${price:,}, moving {change_direction} by {abs_change:.1f} percent in the last 24 hours.",
                    "Breaking down Bitcoin's performance: ${price:,}, {change_direction} {abs_change:.1f} percent today."
                ],
                'top_gainer': [
                    "{name} is the top performer today, trading at ${price:,}, up {change:.1f} percent.",
                    "Leading the gains is {name} at ${price:,}, with an impressive {change:.1f} percent increase.",
                    "{name} is on fire today, reaching ${price:,}, up {change:.1f} percent in 24 hours.",
                    "The biggest gainer: {name} at ${price:,}, soaring {change:.1f} percent higher."
                ],
                'market_summary': [
                    "Market update: Bitcoin at ${btc_price:,}, while {gainer_name} leads gains with {gainer_change:.1f} percent.",
                    "Today's crypto snapshot: Bitcoin {btc_change:+.1f} percent, top performer is {gainer_name} up {gainer_change:.1f} percent.",
                    "Crypto market recap: Bitcoin ${btc_price:,} ({btc_change:+.1f}%), {gainer_name} shining with {gainer_change:.1f} percent gains."
                ]
            },
            'title_templates': {
                'bitcoin': [
                    "🚨 Bitcoin {change_sign}{abs_change:.1f}% | Price Analysis {date}",
                    "Bitcoin Price Update: ${price:,} | {change_direction} {abs_change:.1f}% Today",
                    "📊 BTC Analysis: ${price:,} ({change_sign}{abs_change:.1f}%) | {date}",
                    "Bitcoin Market Update: {change_sign}{abs_change:.1f}% | ${price:,} Live"
                ],
                'gainer': [
                    "🚀 {name} EXPLODES {change:.1f}% | Crypto Analysis {date}",
                    "TOP GAINER: {name} +{change:.1f}% | Price ${price:,}",
                    "🔥 {name} Soars {change:.1f}% | Crypto Winner Today",
                    "{name} Rallies {change:.1f}% | Top Crypto Performer {date}"
                ]
            }
        }
    
    def get_random_template(self, template_type: str, category: str = None):
        """Get a random template from a category"""
        if category and category in self.templates.get(template_type, {}):
            return random.choice(self.templates[template_type][category])
        elif template_type in self.templates:
            return random.choice(list(self.templates[template_type].values()))
        return None
    
    def get_background_template(self):
        """Get random background template"""
        bg_name, bg_config = random.choice(list(self.templates['backgrounds'].items()))
        return bg_name, bg_config
    
    def get_voice_template(self):
        """Get random voice template"""
        return random.choice(self.templates['voices'])
    
    def get_chart_style(self):
        """Get random chart style"""
        style_name, style_config = random.choice(list(self.templates['chart_styles'].items()))
        return style_name, style_config
    
    def get_script_template(self, category: str):
        """Get random script template"""
        return random.choice(self.templates['script_templates'][category])
    
    def get_title_template(self, category: str):
        """Get random title template"""
        return random.choice(self.templates['title_templates'][category])
    
    def format_script(self, template: str, data: Dict) -> str:
        """Format script template with data"""
        try:
            return template.format(**data)
        except KeyError as e:
            print(f"❌ Missing key in template data: {e}")
            return template
    
    def format_title(self, template: str, data: Dict) -> str:
        """Format title template with data"""
        try:
            return template.format(**data)
        except KeyError as e:
            print(f"❌ Missing key in title data: {e}")
            return template

# SEO and content metadata generator
class SEOGenerator:
    """Generate SEO-friendly titles and metadata"""
    
    def __init__(self):
        self.trending_keywords = [
            "bitcoin", "crypto", "cryptocurrency", "blockchain", 
            "ethereum", "solana", "dogecoin", "cardano", "avalanche",
            "market analysis", "price prediction", "technical analysis",
            "crypto news", "defi", "nft", "web3"
        ]
        
        self.emojis = {
            'positive': ['🚀', '📈', '💰', '🔥', '⚡', '💎', '🌙'],
            'negative': ['📉', '⚠️', '🔻', '😰', '💔', '🌪️'],
            'neutral': ['📊', '📈', '💹', '🔄', '📱', '🎯']
        }
    
    def generate_seo_title(self, coin_data: Dict, video_type: str = 'bitcoin') -> str:
        """Generate SEO-optimized title"""
        name = coin_data.get('name', 'Unknown')
        symbol = coin_data.get('symbol', '').upper()
        price = coin_data.get('current_price', 0)
        change = coin_data.get('price_change_percentage_24h', 0)
        
        # Determine sentiment
        if change > 2:
            sentiment = 'positive'
            emoji = random.choice(self.emojis['positive'])
            words = ['EXPLODES', 'SOARS', 'ROCKETS', 'SURGES', 'PUMPS']
        elif change > 0:
            sentiment = 'positive' 
            emoji = random.choice(self.emojis['positive'])
            words = ['GAINS', 'RISES', 'CLIMBS', 'INCREASES']
        elif change < -2:
            sentiment = 'negative'
            emoji = random.choice(self.emojis['negative'])
            words = ['CRASHES', 'DUMPS', 'PLUMMETS', 'COLLAPSES', 'TANKS']
        else:
            sentiment = 'neutral'
            emoji = random.choice(self.emojis['neutral'])
            words = ['UPDATES', 'ANALYSIS', 'REVIEW', 'SNAPSHOT']
        
        action_word = random.choice(words)
        
        # Format title
        if video_type == 'bitcoin':
            title = f"{emoji} {name} {action_word} {abs(change):.1f}% | ${price:,.0f} Bitcoin Analysis"
        else:
            title = f"{emoji} {name} {action_word} {abs(change):.1f}% | Crypto Analysis {symbol}"
        
        # Add date
        from datetime import datetime
        date_str = datetime.now().strftime("%b %d")
        title += f" | {date_str}"
        
        return title
    
    def generate_tags(self, coin_data: Dict) -> List[str]:
        """Generate relevant tags"""
        tags = []
        
        # Basic crypto tags
        tags.extend(['cryptocurrency', 'bitcoin', 'ethereum', 'crypto news', 'trading'])
        
        # Coin-specific
        symbol = coin_data.get('symbol', '').upper()
        if symbol:
            tags.extend([symbol, f'{symbol} price', f'{symbol} news'])
        
        # Trending tags
        tags.extend(random.sample(self.trending_keywords, 3))
        
        # Performance-based
        change = coin_data.get('price_change_percentage_24h', 0)
        if change > 5:
            tags.extend(['crypto gains', 'altcoin season', 'bull run'])
        elif change < -5:
            tags.extend(['crypto crash', 'bear market', 'price drop'])
        
        return tags[:15]  # Limit to 15 tags