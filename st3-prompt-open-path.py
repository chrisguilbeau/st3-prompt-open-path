# python imports
from os.path import expanduser
from os.path import dirname
from os.path import isdir

# sublime imports
from sublime_plugin import WindowCommand
from sublime import error_message
from sublime import message_dialog

class St3PromptOpenPath(WindowCommand):
    '''Prompts for path of file or directory to open'''
    def run(self):
        window = self.window
        activeView = self.window.active_view()
        homeDir = expanduser('~')
        currentDir = dirname(activeView.file_name()) if activeView else homeDir
        self.panel = self.window.show_input_panel(
            "Open file:",
            currentDir,
            self.on_done,
            self.on_change,
            None
        )
    def on_change(self, text):
        panel = self.panel
        edit = panel.begin_edit()
        allTextRegion = panel.full_line(0)
        newPath = 'Chris is cool'
        panel.replace(edit, allTextRegion, newPath)
        panel.end_edit(edit)
    def on_done(self, text):
        if isdir(text):
            message_dialog('Can not open directories')
            return
        try:
            self.window.open_file(text)
        except:
            error_message('Unable to open "%s"' % text)

# class SetMabPathCommand(sublime_plugin.TextCommand):
#     _input = None
#     settings = sublime.load_settings('Mab.sublime-settings')

#     def run(self, edit, key='', val='', save=True):
#         if not self._input:
#             path = self.settings.get('mab_path')
#             self._input = sublime.active_window().show_input_panel('input',
#                 path, self.on_done, self.on_change, self.on_close)
#             self.on_change(path)

#     def on_done(self, text):
#         if os.path.exists(text):
#             self.settings.set('mab_path', text)
#             sublime.save_settings('Mab.sublime-settings')
#         else:
#             sublime.error_message('Path %s does not exists' % text)

#     def on_close(self):
#         self._input = None

#     def on_change(self, text):
#         if self._input:
#             if os.path.exists(text):
#                 scope = 'constant'
#             else:
#                 scope= 'constant.character.escape'
#             self._input.add_regions('regs', [sublime.Region(0, self._input.size())], scope)
