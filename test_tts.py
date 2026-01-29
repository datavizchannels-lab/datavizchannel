#!/usr/bin/env python3
"""
Test TTS functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.tts_generator import generate_audio_sync

def main():
    print("🎤 Testing TTS Generation...")
    
    # Test script
    test_script = "Bitcoin is trading at $88,000, up 2.1 percent today. The biggest gainer is Solana with a 15.3 percent increase."
    
    # Generate audio
    audio_path = generate_audio_sync(test_script, output_filename="test_bitcoin_audio.mp3")
    
    if audio_path:
        print(f"✅ TTS test successful! Audio saved to: {audio_path}")
        return True
    else:
        print("❌ TTS test failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)