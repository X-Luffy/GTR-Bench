# Changelog

All notable changes to the Human-Level Visual Reasoning Assessment System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- Initial release of the Human-Level Visual Reasoning Assessment System
- Support for outdoor (CityFlow) and indoor (MTMMC) scenarios
- 7 different reasoning task types:
  - MotionState (motion state reasoning)
  - GeoLocation (geographic location reasoning)
  - ArrivalTimeInterval (arrival time interval reasoning)
  - CasualReordering (causal reordering reasoning)
  - TrajectoryForecasting (trajectory prediction)
  - NextSpotForecasting (next location forecasting)
  - MultiTrajectoryForecasting (multi-trajectory forecasting)
- Video frame extraction with bounding box visualization
- Time IoU calculation for temporal reasoning tasks
- Real-time scoring system based on accuracy and response time
- Comprehensive result analysis and statistics
- Data export functionality (CSV format)
- Streamlit-based web interface
- Question navigation with previous/next buttons
- Sidebar navigation with question slider
- Automatic video path resolution
- Map image display with proper path handling
- Session state management for assessment progress

### Technical Features
- Modular architecture with separate utility modules
- Video processing using OpenCV
- Image processing with Pillow
- Data handling with Pandas and NumPy
- Responsive UI design
- Error handling and user feedback
- Performance optimization with caching

### Data Structure
- JSON-based question format
- Support for multiple camera views per question
- Time-based video segments
- Map visualization integration
- Flexible answer format support

### User Interface
- Clean, intuitive design
- Real-time feedback
- Progress tracking
- Result visualization
- Export capabilities

## [Unreleased]

### Planned Features
- Unit test coverage
- Additional video format support
- Enhanced error handling
- Performance optimizations
- Accessibility improvements
- Multi-language support
- Batch processing capabilities
- Advanced analytics dashboard

### Known Issues
- Large video files may cause performance issues
- Browser compatibility varies across different versions
- Session data is lost on page refresh

---

## Version History

- **1.0.0**: Initial release with core functionality

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
