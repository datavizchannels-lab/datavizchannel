#!/usr/bin/env python3
"""
Complete DataViz Video Generator
Generates automated financial content videos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.coingecko_api import CoingeckoAPI
from src.chart_generator import QuickChartGenerator
from src.tts_generator import generate_audio_sync
from src.video_composer import VideoComposer

def generate_bitcoin_video():
    """Generate a complete Bitcoin video"""
    print("🚀 Starting Complete Bitcoin Video Generation...")
    
    # Initialize components
    coingecko = CoingeckoAPI()
    chart_gen = QuickChartGenerator()
    video_composer = VideoComposer()
    
    # Get Bitcoin data
    print("📊 Fetching Bitcoin data...")
    markets = coingecko.get_coin_markets(per_page=1, sparkline=False)
    
    if not markets:
        print("❌ Failed to fetch Bitcoin data")
        return False
    
    bitcoin = markets[0]
    print(f"✅ Bitcoin: ${bitcoin['current_price']:,.2f} ({bitcoin['price_change_percentage_24h']:+.2f}%)")
    
    # Get price history
    print("📈 Getting 7-day price history...")
    price_history = coingecko.get_coin_price_history('bitcoin', days=7)
    
    if not price_history:
        print("❌ Failed to get price history")
        return False
    
    # Generate chart
    print("🎨 Generating chart...")
    chart_data = chart_gen.create_sparkline_chart(
        data=price_history,
        coin_name='bitcoin',
        price_change_24h=bitcoin['price_change_percentage_24h'],
        width=800, height=400
    )
    
    if not chart_data:
        print("❌ Failed to generate chart")
        return False
    
    chart_path = chart_gen.save_chart(chart_data, "bitcoin_complete_chart", "bitcoin")
    if not chart_path:
        print("❌ Failed to save chart")
        return False
    
    # Generate audio
    print("🎤 Generating audio narration...")
    script = f"Bitcoin is trading at ${bitcoin['current_price']:,.0f}, {'up' if bitcoin['price_change_percentage_24h'] >= 0 else 'down'} {abs(bitcoin['price_change_percentage_24h']):.1f} percent today."
    audio_path = generate_audio_sync(script, output_filename="bitcoin_complete_audio.mp3")
    
    if not audio_path:
        print("❌ Failed to generate audio")
        return False
    
    # Compose video
    print("🎬 Composing final video...")
    video_path = video_composer.compose_video(
        chart_path=chart_path,
        audio_path=audio_path,
        coin_name='bitcoin',
        price_change=bitcoin['price_change_percentage_24h'],
        duration=15
    )
    
    if video_path:
        print(f"🎉 Complete Bitcoin video generated: {video_path}")
        return True
    else:
        print("❌ Failed to compose video")
        return False

def generate_top_gainers_video():
    """Generate video for top gainers"""
    print("🚀 Starting Top Gainers Video Generation...")
    
    # Initialize components
    coingecko = CoingeckoAPI()
    video_composer = VideoComposer()
    
    # Get top gainers
    print("📊 Fetching top gainers...")
    gainers = coingecko.get_top_gainers(limit=1)
    
    if not gainers:
        print("❌ Failed to fetch top gainers")
        return False
    
    # Generate video using the video composer
    video_path = video_composer.create_top_gainers_video(gainers, duration=15)
    
    if video_path:
        print(f"🎉 Top gainers video generated: {video_path}")
        return True
    else:
        print("❌ Failed to generate top gainers video")
        return False

def main():
    """Main function with video type selection"""
    if len(sys.argv) > 1:
        video_type = sys.argv[1].lower()
    else:
        video_type = "bitcoin"  # Default
    
    print(f"🎬 Generating {video_type} video...")
    
    if video_type == "bitcoin":
        success = generate_bitcoin_video()
    elif video_type == "gainers":
        success = generate_top_gainers_video()
    elif video_type == "all":
        print("🔄 Generating both Bitcoin and Top Gainers videos...")
        success1 = generate_bitcoin_video()
        success2 = generate_top_gainers_video()
        success = success1 and success2
    else:
        print(f"❌ Unknown video type: {video_type}")
        print("Available options: bitcoin, gainers, all")
        return False
    
    if success:
        print("✅ Video generation completed successfully!")
        return True
    else:
        print("❌ Video generation failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)