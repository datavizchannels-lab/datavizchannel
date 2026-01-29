#!/usr/bin/env python3
"""
Advanced DataViz Video Generator with Templates and SEO
Generates varied, SEO-optimized financial content videos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.coingecko_api import CoingeckoAPI
from src.chart_generator import QuickChartGenerator
from src.tts_generator import generate_audio_sync
from src.video_composer import VideoComposer
from src.template_manager import TemplateManager, SEOGenerator

def generate_advanced_video(video_type='bitcoin'):
    """Generate video with random templates and SEO optimization"""
    print(f"🚀 Starting Advanced {video_type.title()} Video Generation...")
    
    # Initialize components
    coingecko = CoingeckoAPI()
    chart_gen = QuickChartGenerator()
    video_composer = VideoComposer()
    template_manager = TemplateManager()
    seo_generator = SEOGenerator()
    
    # Get random templates
    bg_name, bg_config = template_manager.get_background_template()
    voice = template_manager.get_voice_template()
    style_name, style_config = template_manager.get_chart_style()
    
    print(f"🎨 Using templates: BG={bg_name}, Voice={voice}, Chart={style_name}")
    
    # Fetch data based on video type
    if video_type == 'bitcoin':
        markets = coingecko.get_coin_markets(per_page=1, sparkline=False)
        if not markets:
            return False
        coin_data = markets[0]
        price_history = coingecko.get_coin_price_history('bitcoin', days=7)
        script_category = 'bitcoin_focus'
    elif video_type == 'gainers':
        gainers = coingecko.get_top_gainers(limit=1)
        if not gainers:
            return False
        coin_data = gainers[0]
        price_history = coingecko.get_coin_price_history(coin_data['id'], days=7)
        script_category = 'top_gainer'
    else:
        print(f"❌ Unknown video type: {video_type}")
        return False
    
    if not price_history:
        print("❌ Failed to get price history")
        return False
    
    # Generate chart with random style
    print("🎨 Generating styled chart...")
    chart_data = chart_gen.create_sparkline_chart(
        data=price_history,
        coin_name=coin_data['id'],
        price_change_24h=coin_data['price_change_percentage_24h'],
        width=800, height=400
    )
    
    # Apply custom colors from template
    if chart_data and style_config:
        # Note: QuickChart colors are set in the create_sparkline_chart method
        # We would need to modify that method to accept custom colors
        pass
    
    chart_path = chart_gen.save_chart(chart_data, f"{coin_data['id']}_{style_name}_chart", coin_data['id'])
    if not chart_path:
        return False
    
    # Generate script with template
    print("📝 Generating script with template...")
    script_template = template_manager.get_script_template(script_category)
    
    # Prepare script data
    script_data = {
        'price': coin_data['current_price'],
        'abs_change': abs(coin_data['price_change_percentage_24h']),
        'change_direction': 'up' if coin_data['price_change_percentage_24h'] >= 0 else 'down',
        'name': coin_data['name'],
        'change': coin_data['price_change_percentage_24h']
    }
    
    script = template_manager.format_script(script_template, script_data)
    print(f"📜 Script: {script}")
    
    # Generate audio with random voice
    print("🎤 Generating audio with random voice...")
    # Use simpler filename to avoid issues
    audio_filename = f"{coin_data['id']}_audio.mp3"
    audio_path = generate_audio_sync(script, voice=voice, output_filename=audio_filename)
    
    if not audio_path:
        return False
    
    # Compose video
    print("🎬 Composing final video...")
    video_path = video_composer.compose_video(
        chart_path=chart_path,
        audio_path=audio_path,
        coin_name=coin_data['id'],
        price_change=coin_data['price_change_percentage_24h'],
        duration=15
    )
    
    if video_path:
        # Generate SEO metadata
        seo_title = seo_generator.generate_seo_title(coin_data, video_type)
        seo_tags = seo_generator.generate_tags(coin_data)
        
        print(f"🎉 Advanced video generated!")
        print(f"📹 Video: {video_path}")
        print(f"🏷️ SEO Title: {seo_title}")
        print(f"🏷️ SEO Tags: {', '.join(seo_tags)}")
        
        # Save metadata
        metadata_path = video_path.replace('.mp4', '_metadata.txt')
        with open(metadata_path, 'w') as f:
            f.write(f"TITLE: {seo_title}\n")
            f.write(f"TAGS: {', '.join(seo_tags)}\n")
            f.write(f"DESCRIPTION: {script}\n")
            f.write(f"TEMPLATES: BG={bg_name}, Voice={voice}, Chart={style_name}\n")
        
        return True
    else:
        return False

def generate_batch_videos(count=3):
    """Generate multiple videos with different types"""
    print(f"🔄 Generating batch of {count} videos...")
    
    video_types = ['bitcoin', 'gainers']
    success_count = 0
    
    for i in range(count):
        # Alternate between video types
        video_type = video_types[i % len(video_types)]
        
        print(f"\n--- Video {i+1}/{count} ({video_type}) ---")
        if generate_advanced_video(video_type):
            success_count += 1
    
    print(f"\n✅ Batch complete: {success_count}/{count} videos generated successfully")
    return success_count == count

def main():
    """Main function with options"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        command = "single"  # Default
    
    if command == "single":
        video_type = sys.argv[2] if len(sys.argv) > 2 else "bitcoin"
        success = generate_advanced_video(video_type)
    elif command == "batch":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        success = generate_batch_videos(count)
    elif command == "test":
        # Test all template combinations
        print("🧪 Testing template system...")
        template_manager = TemplateManager()
        
        for i in range(5):
            bg_name, _ = template_manager.get_background_template()
            voice = template_manager.get_voice_template()
            style_name, _ = template_manager.get_chart_style()
            print(f"Test {i+1}: BG={bg_name}, Voice={voice}, Chart={style_name}")
        
        success = True
    else:
        print(f"❌ Unknown command: {command}")
        print("Available: single, batch, test")
        return False
    
    if success:
        print("✅ Operation completed successfully!")
        return True
    else:
        print("❌ Operation failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)