import asyncio
import edge_tts
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class TTSGenerator:
    def __init__(self):
        self.audio_dir = os.getenv('AUDIO_DIR', './assets/audio')
        os.makedirs(self.audio_dir, exist_ok=True)
        
        # Available voices - using high-quality English voices
        self.voices = [
            'en-US-JennyNeural',      # Female, natural
            'en-US-GuyNeural',        # Male, natural  
            'en-US-AriaNeural',       # Female, expressive
            'en-US-DavisNeural',      # Male, professional
            'en-GB-SoniaNeural',      # British female
            'en-GB-RyanNeural',       # British male
        ]
    
    async def generate_audio(self, text, voice=None, output_filename=None):
        """
        Generate audio from text using Edge TTS
        """
        if voice is None:
            voice = self.voices[0]  # Default to Jenny
        
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"tts_{timestamp}.mp3"
        
        output_path = os.path.join(self.audio_dir, output_filename)
        
        try:
            # Clean text for better TTS
            clean_text = text.replace('$', ' dollars ').replace('%', ' percent ')
            communicate = edge_tts.Communicate(clean_text, voice)
            await communicate.save(output_path)
            
            # Verify file was created
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"🎤 Audio generated: {output_path}")
                return output_path
            else:
                print(f"❌ Audio file not created or empty")
                return None
                
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            return None
    
    def generate_market_summary_script(self, coin_data, top_gainers=None, top_losers=None):
        """
        Generate a script for market summary narration
        """
        script_parts = []
        
        # Main coin (Bitcoin) summary
        main_coin = coin_data[0] if coin_data else None
        if main_coin:
            price = main_coin['current_price']
            change = main_coin['price_change_percentage_24h']
            
            if change >= 0:
                script_parts.append(f"Bitcoin is trading at ${price:,.0f}, up {abs(change):.1f} percent today.")
            else:
                script_parts.append(f"Bitcoin is trading at ${price:,.0f}, down {abs(change):.1f} percent today.")
        
        # Top gainers
        if top_gainers and len(top_gainers) > 0:
            top_gainer = top_gainers[0]
            script_parts.append(f"The biggest gainer is {top_gainer['name']} with a {top_gainer['price_change_percentage_24h']:.1f} percent increase.")
        
        # Top losers  
        if top_losers and len(top_losers) > 0:
            top_loser = top_losers[0]
            script_parts.append(f"The biggest loser is {top_loser['name']} with a {top_loser['price_change_percentage_24h']:.1f} percent decrease.")
        
        return " ".join(script_parts)
    
    def generate_coin_focus_script(self, coin_data):
        """
        Generate script for single coin focus video
        """
        coin = coin_data[0] if coin_data else None
        if not coin:
            return "Market data unavailable."
        
        price = coin['current_price']
        change = coin['price_change_percentage_24h']
        market_cap = coin.get('market_cap', 0)
        
        if change >= 0:
            script = f"{coin['name']} is performing strong today, trading at ${price:,.0f}, up {abs(change):.1f} percent."
        else:
            script = f"{coin['name']} is facing pressure today, trading at ${price:,.0f}, down {abs(change):.1f} percent."
        
        if market_cap > 0:
            script += f" With a market cap of ${market_cap/1e9:.1f} billion."
        
        return script

# Helper function to run async code
def generate_audio_sync(text, voice=None, output_filename=None):
    """
    Synchronous wrapper for async audio generation
    """
    tts = TTSGenerator()
    return asyncio.run(tts.generate_audio(text, voice, output_filename))