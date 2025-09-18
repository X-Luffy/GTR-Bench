# Development Guide for GTR-Bench

This guide is for team members working on the GTR-Bench project.

## 🚀 Quick Start

### 1. Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/X-Luffy/GTR-Bench.git
cd GTR-Bench

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### 2. Development Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
# ... your development work ...

# Commit changes
git add .
git commit -m "Add: your feature description"

# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## 🏗️ Project Architecture

### Core Components
- **`app.py`**: Main Streamlit application
- **`utils/`**: Utility modules (data loading, video processing, scoring)
- **`components/`**: Reusable UI components
- **`data/`**: Assessment data and media files

### Key Functions
- **Data Loading**: `utils/data_loader.py`
- **Video Processing**: `utils/video_processor.py`
- **Scoring System**: `utils/scoring.py`
- **Question Display**: `components/question_display.py`
- **Result Display**: `components/result_display.py`

## 🧪 Testing Guidelines

### Manual Testing
1. **Start the application**: `streamlit run app.py`
2. **Test all task types**: Load different scenarios and task types
3. **Test navigation**: Use previous/next buttons
4. **Test scoring**: Submit answers and verify scoring
5. **Test data export**: Export results to CSV

### Code Testing
```bash
# Check imports
python -c "import streamlit, cv2, PIL, numpy, pandas"

# Run linting
pip install flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## 📊 Data Structure

### JSON Data Format
```json
{
  "cases": [
    {
      "task_id": "MotionState",
      "case_id": "unique_id",
      "map_image_path": "./map/image.png",
      "question": "Question text",
      "choices": ["Option1", "Option2", "Option3", "Option4"],
      "correct_cam_name": ["CorrectAnswer"],
      "correct_time_str": ["HH:MM:SS.mmm"],
      "camera_images": [...]
    }
  ]
}
```

### Media Files
- **Raw videos**: `data/{scenario}/raw_video/`
- **Cropped videos**: `data/{scenario}/crop_video/`
- **Map images**: `data/{scenario}/map/`

## 🔧 Common Development Tasks

### Adding New Task Types
1. Update task mappings in `app.py`
2. Add display logic in `components/question_display.py`
3. Update scoring logic in `utils/scoring.py`
4. Add sample data in appropriate scenario folder

### Modifying UI Components
1. Update components in `components/` directory
2. Test with different task types
3. Ensure responsive design
4. Update documentation if needed

### Data Processing
1. Use scripts in `scripts/` directory for data processing
2. Follow existing naming conventions
3. Update JSON structure if needed
4. Test with sample data

## 🐛 Debugging Tips

### Common Issues
1. **Video files not found**: Check file paths in JSON data
2. **Import errors**: Ensure all dependencies are installed
3. **UI not updating**: Check Streamlit session state
4. **Scoring errors**: Verify answer format and scoring logic

### Debug Tools
```bash
# Check file paths
python -c "import os; print(os.path.exists('path/to/file'))"

# Test JSON loading
python -c "import json; data=json.load(open('data/outdoor/outdoor_MotionState_30.json')); print(len(data['cases']))"

# Check Streamlit version
streamlit --version
```

## 📝 Code Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions
- Keep functions under 50 lines when possible

### Git Workflow
- Use descriptive commit messages
- Create feature branches for new features
- Test before pushing
- Use pull requests for code review

### Documentation
- Update README.md for major changes
- Add comments for complex logic
- Document new features
- Keep examples up to date

## 🚨 Important Notes

### Data Security
- Never commit sensitive data
- Use environment variables for configuration
- Follow data privacy guidelines
- Test with sample data only

### Performance
- Cache expensive operations
- Optimize video processing
- Monitor memory usage
- Test with large datasets

## 📞 Getting Help

### Resources
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check README.md and code comments
- **Team Chat**: Use your team communication platform
- **Code Review**: Ask for feedback on pull requests

### Team Communication
- Use GitHub issues for technical discussions
- Create pull requests for code review
- Document decisions in commit messages
- Share knowledge through code comments

---

Happy coding! 🎉
