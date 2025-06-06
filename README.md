# motalk

Widgets for talking to/with Python from a notebook.

## Live Demo

If you want to see a live demo, check out the Github Pages of this project. 

https://koaning.github.io/motalk/

## Overview

motalk provides interactive speech-to-text widgets for Python notebooks, built on top of [anywidget](https://anywidget.dev/). It enables voice input capabilities directly in your notebook environment, making it easy to capture spoken text and use it in your Python code. It uses the Webkit Speech API from your browser too, which means you don't have to worry about API keys. Be ware though: different browsers may have different levels of support for this feature.

## Installation

```bash
pip install motalk
```

## Quick Start

```python
import motalk

# Create a speech-to-text widget
widget = motalk.WebkitSpeechToTextWidget()

# Display the widget
widget
```

After interacting with the widget you will be able to grab the transcript from:

```
widget.transcript
```
