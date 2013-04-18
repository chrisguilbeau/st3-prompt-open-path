# python imports
from os import listdir
from os import sep
from os.path import commonprefix
from os.path import dirname
from os.path import expanduser
from os.path import isdir
from os.path import join
from os.path import normpath
from os.path import split
import rlcompleter

# sublime imports
from sublime import error_message
from sublime import message_dialog
from sublime import Region
from sublime import status_message
from sublime_plugin import TextCommand
from sublime_plugin import WindowCommand
from sublime_plugin import EventListener

class CompletePath(TextCommand):
    def run(self, edit, text):
        baseDir, partialPath = split(text)
        panel = self.view
        newText = join(baseDir, partialPath)
        region = Region(0, panel.size())
        options = [name for name in listdir(baseDir) if name.startswith(partialPath)]
        status_message(' ,'.join(options))
        if not options:
            newText = text
        else:
            newText = join(baseDir, commonprefix(options))
        # Add a trailing slash if you are tabbing into a directory
        if len(options) == 1 and isdir(newText):
            newText = join(newText, '')
        panel.replace(edit, region, newText)

class St3PromptOpenPath(WindowCommand):
    '''Prompts for path of file or directory to open'''
    def run(self):
        window = self.window
        activeView = self.window.active_view()
        homeDir = expanduser('~')
        currentDir = dirname(activeView.file_name()) if activeView and activeView.file_name() else homeDir
        self.panel = self.window.show_input_panel(
            "Open path:",
            join(currentDir, ''),
            self.on_done,
            self.on_change,
            None
        )
    def on_change(self, text):
        # for some reason, on_change get's called when self.panel is not set
        if not getattr(self, 'panel', None):
            return
        self.panel.settings().set('tab_completion', False)
        if text.endswith('\t'):
            self.panel.run_command('complete_path', dict(text=text.strip()))
    def on_done(self, text):
        if isdir(text):
            window = self.window
            if text not in window.folders():
                projectData = window.project_data() or dict()
                folders = projectData.get('folders', [])
                folders.append(dict(path=normpath(text)))
                projectData['folders'] = folders
                self.window.set_project_data(projectData)
            return
        try:
            self.window.open_file(text)
        except:
            error_message('Unable to open "%s"' % text)
