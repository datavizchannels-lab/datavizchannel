import subprocess
import os
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class VideoComposer:
    def __init__(self):
        self.output_dir = os.getenv('OUTPUT_DIR', './assets/output')
        self.backgrounds_dir = os.getenv('BACKGROUNDS_DIR', './assets/backgrounds')
        self.audio_dir = os.getenv('AUDIO_DIR', './assets/audio')
        self.charts_dir = os.getenv('CHARTS_DIR', './assets/charts')
        
        # Video dimensions for vertical format (9:16)
        self.width = int(os.getenv('VIDEO_WIDTH', 1080))
        self.height = int(os.getenv('VIDEO_HEIGHT', 1920))
        
        # Ensure directories exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.backgrounds_dir, exist_ok=True)
        
    def check_ffmpeg(self):
        """Check if FFmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ FFmpeg not found. Please install FFmpeg.")
            return False
    
    def create_sample_background(self):
        """Create an animated background with subtle effects"""
        background_path = os.path.join(self.backgrounds_dir, 'animated_bg.mp4')
        
        if os.path.exists(background_path):
            return background_path
        
        # Create animated background with gradient and particles
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', 'color=black:size=1080x1920:duration=15:rate=30',
            '-f', 'lavfi',
            '-i', 'cellauto=c=0:s=1080x1920:m=0:ratio=0.1:f=15',
            '-filter_complex', 
            '[0:v][1:v]blend=all_mode=multiply:all_opacity=0.3[bg1];[bg1]eq=brightness=0.1:contrast=1.2:saturation=1.5[bg]',
            '-map', '[bg]',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-t', '15',
            background_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Animated background created: {background_path}")
            return background_path
        except subprocess.CalledProcessError as e:
            # Fallback to simple black background
            print(f"⚠️ Falling back to simple background: {e}")
            return self.create_simple_background()
    
    def create_simple_background(self):
        """Create a simple black background as fallback"""
        background_path = os.path.join(self.backgrounds_dir, 'simple_bg.mp4')
        
        if os.path.exists(background_path):
            return background_path
        
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', 'color=black:size=1080x1920:duration=15:rate=30',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-t', '15',
            background_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return background_path
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating background: {e}")
            return None
    
    def compose_video(self, chart_path, audio_path, coin_name, price_change, 
                      background_path=None, duration=15):
        """
        Compose final video with chart, audio, and background
        """
        if not self.check_ffmpeg():
            return None
        
        # Create background if not provided
        if not background_path:
            background_path = self.create_sample_background()
            if not background_path:
                return None
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{coin_name}_{timestamp}_video.mp4"
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Determine color based on price change
        if price_change >= 0:
            text_color = '#00ff88'
            emoji = '🚀'
        else:
            text_color = '#ff4444'
            emoji = '📉'
        
        # FFmpeg command to compose video with working fade animations
        filter_complex = [
            # Background video
            '[0:v]scale=1080:1920[bg]',
            # Chart overlay with fade-in
            f'[1:v]scale=800:400,fade=t=in:st=0:d=1[chart_fade]',
            # Compose background and faded chart
            '[bg][chart_fade]overlay=(W-w)/2:(H-h)/2-100[comp1]',
            # Add title without fade to avoid errors
            f'[comp1]drawtext=text=\'{coin_name.upper()}\':fontcolor=white:fontsize=80:x=(W-w)/2:y=100:fontfile=/System/Library/Fonts/Helvetica.ttc[final]'
        ]
        
        cmd = [
            'ffmpeg', '-y',
            '-i', background_path,      # Background video
            '-i', chart_path,           # Chart image
            '-i', audio_path,           # Audio narration
            '-filter_complex', ','.join(filter_complex),
            '-map', '[final]',
            '-map', '2:a',              # Map audio from input 2
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-preset', 'fast',
            '-crf', '23',
            '-t', str(duration),
            '-shortest',                # End when shortest input ends
            output_path
        ]
        
        try:
            print(f"🎬 Composing video...")
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Video composed successfully: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"❌ Error composing video: {e}")
            print(f"FFmpeg stderr: {e.stderr.decode() if e.stderr else 'No stderr'}")
            return None
    
    def create_top_gainers_video(self, gainers_data, duration=15):
        """
        Create video for top gainers
        """
        if not gainers_data:
            print("❌ No gainers data provided")
            return None
        
        # Use top gainer
        top_gainer = gainers_data[0]
        coin_name = top_gainer['id']
        price_change = top_gainer['price_change_percentage_24h']
        
        # Generate chart for this coin
        from src.coingecko_api import CoingeckoAPI
        from src.chart_generator import QuickChartGenerator
        from src.tts_generator import generate_audio_sync
        
        coingecko = CoingeckoAPI()
        chart_gen = QuickChartGenerator()
        
        # Get price history
        price_history = coingecko.get_coin_price_history(coin_name, days=7)
        if not price_history:
            return None
        
        # Generate chart
        chart_data = chart_gen.create_sparkline_chart(
            data=price_history,
            coin_name=coin_name,
            price_change_24h=price_change,
            width=800, height=400
        )
        
        if not chart_data:
            return None
        
        # Save chart
        chart_path = chart_gen.save_chart(chart_data, f"{coin_name}_chart", coin_name)
        if not chart_path:
            return None
        
        # Generate audio
        script = f"{top_gainer['name']} is the top performer today, trading at ${top_gainer['current_price']:,.0f}, up {price_change:.1f} percent in the last 24 hours."
        audio_path = generate_audio_sync(script, output_filename=f"{coin_name}_gainer_audio.mp3")
        
        if not audio_path:
            return None
        
        # Compose video
        return self.compose_video(chart_path, audio_path, coin_name, price_change, duration=duration)