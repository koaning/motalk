"""motalk - Widgets for talking to Python from a notebook"""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Python < 3.8
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("motalk")
except PackageNotFoundError:
    __version__ = "unknown"


import marimo as mo
from anywidget import AnyWidget
import traitlets


class WebkitSpeechToTextWidget(AnyWidget):
    # Define the widget's properties
    transcript = traitlets.Unicode("").tag(sync=True)
    listening = traitlets.Bool(False).tag(sync=True)

    # HTML/JS for the frontend
    _esm = """
    function render({ model, el }) {
      // Create elements
      const container = document.createElement('div');
      container.className = 'speech-container';

      const display = document.createElement('div');
      display.className = 'transcript-display';
      display.textContent = model.get('transcript') || 'Transcript will appear here...';

      const button = document.createElement('button');
      button.className = 'speech-button';
      button.textContent = 'Start Listening';

      const status = document.createElement('div');
      status.className = 'status-indicator';
      status.textContent = 'Not listening';

      // Append elements
      container.appendChild(status);
      container.appendChild(display);
      container.appendChild(button);
      el.appendChild(container);

      // Speech recognition setup
      let recognition = null;

      try {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onstart = () => {
          status.textContent = 'Listening...';
          status.classList.add('active');
          button.textContent = 'Stop Listening';
          model.set('listening', true);
          model.save_changes();
        };

        recognition.onresult = (event) => {
          let finalTranscript = '';
          let interimTranscript = '';

          for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
              finalTranscript += transcript;
            } else {
              interimTranscript += transcript;
            }
          }

          const fullTranscript = finalTranscript || interimTranscript;
          display.textContent = fullTranscript;
          model.set('transcript', fullTranscript);
          model.save_changes();
        };

        recognition.onerror = (event) => {
          console.error('Speech recognition error', event.error);
          status.textContent = `Error: ${event.error}`;
          status.classList.remove('active');
          button.textContent = 'Start Listening';
          model.set('listening', false);
          model.save_changes();
        };

        recognition.onend = () => {
          status.textContent = 'Not listening';
          status.classList.remove('active');
          button.textContent = 'Start Listening';
          model.set('listening', false);
          model.save_changes();
        };

      } catch (error) {
        console.error('Speech recognition not supported', error);
        status.textContent = 'Speech recognition not supported in this browser';
        button.disabled = true;
      }

      // Function to toggle listening state
      const toggleListening = () => {
        if (!recognition) return;

        const isListening = model.get('listening');
        if (isListening) {
          recognition.stop();
        } else {
          recognition.start();
        }
      };

      // Add event listener for button
      button.addEventListener('click', toggleListening);

      // Listen for trigger from Python
      model.on('change:trigger_listen', () => {
        if (model.get('trigger_listen')) {
          toggleListening();
          // Reset the trigger
          model.set('trigger_listen', false);
          model.save_changes();
        }
      });

      // Listen for direct changes to listening
      model.on('change:listening', () => {
        const isListening = model.get('listening');
        const currentlyListening = recognition && status.textContent === 'Listening...';

        // Only take action if there's a mismatch between the model and current state
        if (isListening !== currentlyListening) {
          if (isListening) {
            if (recognition) recognition.start();
          } else {
            if (recognition) recognition.stop();
          }
        }

        // Update UI to reflect current state
        button.textContent = isListening ? 'Stop Listening' : 'Start Listening';
        status.textContent = isListening ? 'Listening...' : 'Not listening';
        status.classList.toggle('active', isListening);
      });

      // Update display when transcript changes
      model.on('change:transcript', () => {
        display.textContent = model.get('transcript') || 'Transcript will appear here...';
      });
    }

    export default {render};
    """

    _css = """
    .speech-container {
      padding: 16px;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      background: #f8f9fa;
      max-width: 500px;
      text-align: center;
    }

    .transcript-display {
      font-size: 16px;
      margin: 16px 0;
      padding: 12px;
      min-height: 100px;
      border: 1px solid #ddd;
      border-radius: 4px;
      background: white;
      text-align: left;
      overflow-y: auto;
      color: #212529;
    }

    .speech-button {
      padding: 10px 20px;
      background: #4285f4;
      color: white;
      border: none;
      border-radius: 4px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.2s;
    }

    .speech-button:hover {
      background: #2b6cb0;
    }

    .speech-button:active {
      transform: scale(0.98);
    }

    .speech-button:disabled {
      background: #cccccc;
      cursor: not-allowed;
    }

    .status-indicator {
      font-size: 14px;
      color: #666;
      margin-bottom: 8px;
    }

    .status-indicator.active {
      color: #d23;
      font-weight: bold;
    }
    """
