import pygame
import os

class SoundManager:
    """Manages all game sounds with fallback for missing files"""
    
    def __init__(self):
        # Check if mixer is already initialized, if not initialize it
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        self.sounds = {}
        self.enabled = True
        self.sounds_loaded = False
        
        # Try to load sound files
        self._load_sounds()
    
    def _load_sounds(self):
        """Load sound files with error handling"""
        # Get the directory where the script is running from
        # Try multiple possible paths
        possible_paths = [
            'sounds/',  # If running from project root
            '../sounds/',  # If running from game/ folder
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sounds/')  # Absolute path from this file
        ]
        
        sound_files = {
            'paddle_hit': 'paddle_hit.wav',
            'wall_bounce': 'wall_bounce.wav',
            'score': 'score.wav'
        }
        
        # Find the correct sounds directory
        sounds_dir = None
        for path in possible_paths:
            test_file = os.path.join(path, 'paddle_hit.wav')
            if os.path.exists(test_file):
                sounds_dir = path
                break
        
        loaded_count = 0
        print("\n=== Sound Manager Initialization ===")
        
        if sounds_dir:
            print(f"Found sounds directory: {os.path.abspath(sounds_dir)}")
        else:
            print("⚠ Could not locate sounds directory!")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Script location: {os.path.dirname(__file__)}")
        
        for sound_name, filename in sound_files.items():
            loaded = False
            
            # Try each possible path
            for base_path in possible_paths:
                file_path = os.path.join(base_path, filename)
                
                if os.path.exists(file_path):
                    try:
                        self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                        # Set volumes (0.0 to 1.0)
                        if sound_name == 'paddle_hit':
                            self.sounds[sound_name].set_volume(0.5)
                        elif sound_name == 'wall_bounce':
                            self.sounds[sound_name].set_volume(0.3)
                        elif sound_name == 'score':
                            self.sounds[sound_name].set_volume(0.6)
                        print(f"✓ Loaded: {file_path}")
                        loaded_count += 1
                        loaded = True
                        break
                    except pygame.error as e:
                        print(f"✗ Error loading {file_path}: {e}")
            
            if not loaded:
                print(f"✗ Missing: {filename}")
                self.sounds[sound_name] = None
        
        if loaded_count > 0:
            self.sounds_loaded = True
            print(f"\nSound system ready! ({loaded_count}/3 sounds loaded)")
        else:
            print("\n⚠ No sound files found! Game will run silently.")
            print("To add sounds, create a 'sounds/' folder in the project root with:")
            print("  - paddle_hit.wav")
            print("  - wall_bounce.wav")
            print("  - score.wav")
        
        print("===================================\n")
    
    def play(self, sound_name):
        """Play a sound if it exists and sounds are enabled"""
        if self.enabled and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except pygame.error as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def toggle(self):
        """Toggle sounds on/off"""
        self.enabled = not self.enabled
        return self.enabled