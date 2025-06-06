import marimo

__generated_with = "0.13.15"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    from motalk import WebkitSpeechToTextWidget

    speech_widget = mo.ui.anywidget(WebkitSpeechToTextWidget())
    speech_widget
    return (speech_widget,)


@app.cell
def _(speech_widget):
    speech_widget.transcript
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
