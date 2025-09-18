#!/usr/bin/env python3
import json
import os
import glob

def remove_scene_field_from_json(file_path):
    """Remove 'scene' field from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if 'cases' field exists
        if 'cases' in data:
            modified = False
            for case in data['cases']:
                if 'scene' in case:
                    del case['scene']
                    modified = True
            
            if modified:
                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✅ Removed 'scene' field from {file_path}")
            else:
                print(f"ℹ️  No 'scene' field found in {file_path}")
        else:
            print(f"⚠️  No 'cases' field found in {file_path}")
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

def main():
    # Find all JSON files in data directory
    json_files = glob.glob('data/**/*.json', recursive=True)
    
    print(f"Found {len(json_files)} JSON files to process:")
    for file_path in json_files:
        print(f"  - {file_path}")
    
    print("\nProcessing files...")
    for file_path in json_files:
        remove_scene_field_from_json(file_path)
    
    print("\n✅ All JSON files processed!")

if __name__ == "__main__":
    main()
