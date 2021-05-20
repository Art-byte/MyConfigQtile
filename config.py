import os
import re
import socket
import subprocess
from libqtile.widget import base
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook 
from libqtile.lazy import lazy
from typing import List, Sized  # noqa: F401

mod = "mod4"
control = "control"
alt = "alt"                             # Sets mod key to SUPER/WINDOWS
myTerm = "xfce4-terminal"                             # My terminal of choice

__all__ = ['Volume']
re_vol = re.compile(r'\[(\d?\d?\d?)%\]')

keys = [
    # The essentials
    Key([mod], "t",
        lazy.spawn(myTerm),
        desc='Launches My Terminal'
        ),
    Key([mod, "shift"], "Return",
        lazy.spawn("dmenu_run -p 'Run: '"),
        desc='Run Launcher'
        ),
    Key([mod], "Tab",
        lazy.next_layout(),
        desc='Toggle through layouts'
        ),
    Key([mod, "shift"], "c",
        lazy.window.kill(),
        desc='Kill active window'
        ),
    Key([mod, "shift"], "r",
        lazy.restart(),
        desc='Restart Qtile'
        ),
    Key([mod, "shift"], "q",
        lazy.shutdown(),
        desc='Shutdown Qtile'
        ),
    Key(["control", "shift"], "e",
        lazy.spawn("emacsclient -c -a emacs"),
        desc='Doom Emacs'
        ),
    # Switch focus to specific monitor (out of three)
    Key([mod], "w",
        lazy.to_screen(0),
        desc='Keyboard focus to monitor 1'
        ),
    Key([mod], "b",
        lazy.to_screen(1),
        desc='Keyboard focus to monitor 2'
        ),

    Key([mod], "e",
        lazy.spawn("pcmanfm")
        ),

    Key([mod], "r",
        lazy.to_screen(2),
        desc='Keyboard focus to monitor 3'
        ),
    # Switch focus of monitors
    Key([mod], "period",
        lazy.next_screen(),
        desc='Move focus to next monitor'
        ),
    Key([mod], "comma",
        lazy.prev_screen(),
        desc='Move focus to prev monitor'
        ),
    # Treetab controls
    Key([mod, "shift"], "h",
        lazy.layout.move_left(),
        desc='Move up a section in treetab'
        ),
    Key([mod, "shift"], "l",
        lazy.layout.move_right(),
        desc='Move down a section in treetab'
        ),
    # Window controls
    Key([mod], "j",
        lazy.layout.down(),
        desc='Move focus down in current stack pane'
        ),
    Key([mod], "k",
        lazy.layout.up(),
        desc='Move focus up in current stack pane'
        ),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down(),
        desc='Move windows down in current stack'
        ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up(),
        desc='Move windows up in current stack'
        ),
    Key([mod], "h",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
        ),
    Key([mod], "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
        ),
    Key([mod], "n",
        lazy.layout.normalize(),
        desc='normalize window size ratios'
        ),
    Key([mod], "m",
        lazy.layout.maximize(),
        desc='toggle window between minimum and maximum sizes'
        ),
    Key([mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'
        ),
    Key([mod], "f",
        lazy.window.toggle_fullscreen(),
        desc='toggle fullscreen'
        ),
    # Stack controls
    Key([mod, "shift"], "Tab",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc='Switch which side main pane occupies (XmonadTall)'
        ),
    Key([mod], "space",
        lazy.layout.next(),
        desc='Switch window focus to other pane(s) of stack'
        ),
    Key([mod, "shift"], "space",
        lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack'
        ),

    # Emacs programs launched using the key chord CTRL+e followed by 'key'
    KeyChord(["control"], "e", [
             Key([], "e",
                 lazy.spawn("emacsclient -c -a 'emacs'"),
                 desc='Launch Emacs'
                 ),
             Key([], "b",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(ibuffer)'"),
                 desc='Launch ibuffer inside Emacs'
                 ),
             Key([], "d",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(dired nil)'"),
                 desc='Launch dired inside Emacs'
                 ),
             Key([], "i",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(erc)'"),
                 desc='Launch erc inside Emacs'
                 ),
             Key([], "m",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(mu4e)'"),
                 desc='Launch mu4e inside Emacs'
                 ),
             Key([], "n",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(elfeed)'"),
                 desc='Launch elfeed inside Emacs'
                 ),
             Key([], "s",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(eshell)'"),
                 desc='Launch the eshell inside Emacs'
                 ),
             Key([], "v",
                 lazy.spawn(
                     "emacsclient -c -a 'emacs' --eval '(+vterm/here nil)'"),
                 desc='Launch vterm inside Emacs'
                 )
             ]),


    # Dmenu scripts launched using the key chord SUPER+p followed by 'key'
    KeyChord([mod], "p", [
             Key([], "e",
                 lazy.spawn("./dmscripts/dmconf"),
                 desc='Choose a config file to edit'
                 ),
             Key([], "i",
                 lazy.spawn("./dmscripts/dmscrot"),
                 desc='Take screenshots via dmenu'
                 ),
             Key([], "k",
                 lazy.spawn("./dmscripts/dmkill"),
                 desc='Kill processes via dmenu'
                 ),
             Key([], "l",
                 lazy.spawn("./dmscripts/dmlogout"),
                 desc='A logout menu'
                 ),
             Key([], "m",
                 lazy.spawn("./dmscripts/dman"),
                 desc='Search manpages in dmenu'
                 ),
             Key([], "o",
                 lazy.spawn("./dmscripts/dmqute"),
                 desc='Search your qutebrowser bookmarks and quickmarks'
                 ),
             Key([], "r",
                 lazy.spawn("./dmscripts/dmred"),
                 desc='Search reddit via dmenu'
                 ),
             Key([], "s",
                 lazy.spawn("./dmscripts/dmsearch"),
                 desc='Search various search engines via dmenu'
                 ),
             Key([], "p",
                 lazy.spawn("passmenu"),
                 desc='Retrieve passwords with dmenu'
                 )
             ])
]

# Se necesita font Nerd en el Sistema para leer estos iconos
#"   ", "   ", "   ", "   ", "   ", "   ", "   ", "   ", "   ",

group_names = [("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'})
               ]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    # Switch to another group
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    # Send current window to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "#110a14",
                "border_normal": "#110a14"
                }

layouts = [
    layout.MonadWide(**layout_theme),
    # layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    # layout.Columns(**layout_theme),
    # layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme,),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
        font="Ubuntu",
        fontsize=10,
        sections=["FIRST", "SECOND", "THIRD", "FOURTH"],
        section_fontsize=10,
        border_width=2,
        bg_color="1c1f24",
        active_bg="c678dd",
        active_fg="000000",
        inactive_bg="a9a1e1",
        inactive_fg="1c1f24",
        padding_left=0,
        padding_x=0,
        padding_y=5,
        section_top=10,
        section_bottom=30,
        level_shift=8,
        vspace=3,
        panel_width=300,
        hidden=60
    ),
    layout.Floating(**layout_theme)
]

colors = [["#000000", "#000000"],  # 0 panel background
          ["#434758", "#434758"],  # 1 background for current screen tab
          ["#cfcaca", "#cfcaca"],  # 2 font color for group names
          ["#CB3030", "#CB3030"],  # 3 border line color for current tab


          # border line color for 'other tabs' and color for 'odd widgets'
          ["#74438f", "#74438f"],  # 4
          ["#247fc7", "#247fc7"],  # 5 color for the 'even widgets'RRR
          ["#ffffff", "#ffffff"],  # 6 window name
          ["#ecbbfb", "#ecbbfb"],  # 7
          ["#b82323", "#b82323"],  # 8 Color Red
          ["#3d5175", "#3d5175"],  # 9 Color Purple
          ["#aab512", "#aab512"],  # 10 Color yellow
          ["#002157", "#002157"],  # 11 Color Azul verde
          ["#168714", "#168714"],  # 12 Color verde
          ["#1f3461", "#1f3461"],  # 13 Color Vino
          ["#942c2c", "#942c2c"],  # 14 Color Vino,
          ["#6f7370", "#6f7370"],    # 15 Gris Oscuro
          ["#989c99", "#989c99"],  # 16 Gris claro
          ["#911783", "#911783"]    # 17 Naranja

          ]  # backbround for inactive screens

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Nerd",
    fontsize=11,
    padding=2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [

        widget.Sep(
            linewidth=0,
            padding=6,
            foreground=colors[2],
            background=colors[0]
        ),
        widget.Image(
            filename="/home/art/.config/qtile/icons/pacman1.png",
            scale="False",
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(myTerm)},
            background=colors[0]
        ),

        widget.Image(
            filename="/home/art/.config/qtile/icons/FantasmaAmarillo.png",
            scale="False",
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(myTerm)},
            background=colors[0]
        ),
        widget.Image(
            filename="/home/art/.config/qtile/icons/FantasmaRojo.png",
            scale="False",
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(myTerm)},
            background=colors[0]
        ),
        widget.Image(
            filename="/home/art/.config/qtile/icons/FantasmaAzul.png",
            scale="False",
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(myTerm)},
            background=colors[0]
        ),


        widget.Sep(
            linewidth=0,
            padding=10,
            foreground=colors[2],
            background=colors[0]
        ),
        widget.GroupBox(
            font="Nerd",
            fontsize=15,
            margin_y=3,
            margin_x=14,
            padding_y=5,
            padding_x=5,
            borderwidth=1,
            active=colors[2],
            inactive=colors[2],
            rounded=False,
            highlight_color=colors[0],
            highlight_method="text",
            this_current_screen_border=colors[6],
            this_screen_border=colors[4],
            other_current_screen_border=colors[6],
            other_screen_border=colors[4],
            foreground=colors[2],
            background=colors[0]
        ),


        widget.Prompt(
            prompt=prompt,
            font="Nerd Black",
            padding=10,
            foreground=colors[3],
            background=colors[1]
        ),


        widget.Sep(
            linewidth=0,
            padding=30,
            foreground=colors[2],
            background=colors[0]
        ),

        widget.WindowName(
            font = "Nerd Black",
            foreground=colors[2],
            background=colors[0],
            padding=0
        ),

        widget.Sep(
            linewidth=0,
            padding=30,
            foreground=colors[0],
            background=colors[0]
        ),

        widget.TextBox(
            text=' | ',
            background=colors[0],
            foreground=colors[9],
            padding=0,
            fontsize=15
        ),


        widget.TextBox(
            text=" 🖬",
            foreground=colors[2],
            background=colors[0],
            padding=0,
            fontsize=14
        ),
        widget.Memory(
            foreground=colors[2],
            background=colors[0],
            font='Nerd Black',
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e bashtop')},
            padding=3
        ),


        widget.TextBox(
            text=' | ',
            background=colors[0],
            foreground=colors[9],
            padding=0,
            fontsize=15
        ),

        # Icono de bateria
        widget.TextBox(
            text="",
            padding=0,
            foreground=colors[2],
            background=colors[0],
            font='Nerd Black',
            fontsize=12
        ),

        widget.Battery(
            foreground=colors[2],
            background=colors[0],
            font='Nerd Black',
            battery=0,
            low_porcentage=0.1,
            low_foreground="#00b02f",
            format=" {percent:2.0%}",
            empty_char="x"
        ),


        widget.TextBox(
            text=' | ',
            background=colors[0],
            foreground=colors[9],
            padding=0,
            fontsize=15
        ),

        widget.TextBox(
            text="",
            foreground=colors[2],
            background=colors[0],
            padding=0
        ),

        widget.Volume(
            foreground=colors[2],
            background=colors[0],
            font='Nerd Black',
            padding=5,
            volume_down_command="amixer set Master 5%-",
            volume_up_command="amixer set Master 10%+",
            update_interval=0.2,
            step=2
        ),

        widget.TextBox(
            text=' | ',
            background=colors[0],
            foreground=colors[9],
            padding=0,
            fontsize=15
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser(
                "/home/art/.config/qtile/icons/")],
            foreground=colors[0],
            background=colors[0],
            padding=0,
            scale=0.7
        ),
        widget.CurrentLayout(
            foreground=colors[2],
            background=colors[0],
            font='Nerd Black',

            padding=5
        ),
        widget.TextBox(
            text=' | ',
            background=colors[0],
            foreground=colors[9],
            padding=0,
            fontsize=15
        ),
        widget.Clock(
            foreground=colors[2],
            background=colors[0],
            font='Nerd Black',
            format=" %A, %B %d - %H:%M ",
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e tty-clock')},
        ),

        widget.TextBox(
            text=' | ',
            background=colors[0],
            foreground=colors[9],
            padding=0,
            fontsize=15,
        ),


        widget.Systray(
            background=colors[0],
            padding=5,
            icon_size=25
        ),
        widget.Sep(
            linewidth=0,
            padding=10,
            foreground=colors[2],
            background=colors[0]
        )

    ]
    return widgets_list


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    # Slicing removes unwanted widgets (systray) on Monitors 1,3
    del widgets_screen1[7:8]
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    # Monitor 2 will display all widgets in widgets_list
    return widgets_screen2


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]


if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()


def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]




def clear(self, colour):
      self.set_source_rgb(colour)
      self.ctx.rectangle(0, 0, self.width, self.height)
      self.ctx.fill()
      self.ctx.stroke()

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


autostart = [
    "feh --bg-fill /home/art/.config/qtile/background/palmeras.jpg",
    "picom --no-vsync &",
    "nm-applet &"
]

for x in autostart:
    os.system(x)
