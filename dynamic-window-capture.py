import obspython as obs
import win32gui
import win32process
import psutil
import os
import re
# ------------------------------------------------------------

def script_description():
    return "Window capture for dynamic window titles"

def script_properties():
    """
    Called to define user properties associated with the script. These
    properties are used to define how to show settings properties to a user.
    """
    props = obs.obs_properties_create()
    p = obs.obs_properties_add_list(props, "source", "Window Capture Source",
                                    obs.OBS_COMBO_TYPE_LIST,
                                    obs.OBS_COMBO_FORMAT_STRING)

    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            if source_id == "window_capture":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)

    obs.obs_properties_add_text(props, "executable", "Executable to Match (e.g. whatsapp.exe)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "window_match", "Regex for Title to Match (e.g. .*video call", obs.OBS_TEXT_DEFAULT)

    return props


def script_update(settings):
    """
    Called when the script’s settings (if any) have been changed by the user.
    """
    global config_source_name, config_executable, config_window_match, config_class
    print("Settings updated")
    config_source_name = obs.obs_data_get_string(settings, "source")
    config_executable = obs.obs_data_get_string(settings, "executable")
    config_window_match = obs.obs_data_get_string(settings, "window_match")
    #config_class = obs.obs_data_get_string(settings, "class")

def enum_windows():
    def callback(handle, data):
        tid, pid = win32process.GetWindowThreadProcessId(handle)
        windows.append({
          "title": win32gui.GetWindowText(handle),
          "class": win32gui.GetClassName(handle),
          "executable": os.path.basename(psutil.Process(pid).exe())
        })

    windows = []
    win32gui.EnumWindows(callback, None)
    return windows

def match_window(executable, re_title):
    exec_lower = executable.lower()
    print("Matching executable %s and window title: %s" % (executable, re_title))
    for window in enum_windows():
        if window["executable"].lower() == exec_lower and re.match(re_title, window["title"]) is not None:
            return window

    return None

def on_event(event):
    global config_source_name, config_executable, config_window_match
    if event == obs.OBS_FRONTEND_EVENT_SCENE_CHANGED:
        print("Scene change")

        current_scene = obs.obs_frontend_get_current_scene()

        scene = obs.obs_scene_from_source(current_scene)
        scene_items = obs.obs_scene_enum_items(scene)
        for scene_item in scene_items:
            cur_source =  obs.obs_sceneitem_get_source(scene_item)
            if (obs.obs_source_get_unversioned_id(cur_source) == "window_capture" and
                obs.obs_source_get_name(cur_source) == config_source_name):
                print("Source matched: %s" % (obs.obs_source_get_name(cur_source)))
                cur_settings = obs.obs_source_get_settings(cur_source)
                new_window = match_window(config_executable, config_window_match)
                if (new_window is not None):
                    old_window_text = obs.obs_data_get_string(cur_settings, "window")
                    new_window_text = "%s:%s:%s" % (new_window["title"],
                                                    new_window["class"],
                                                    new_window["executable"])
                    if (old_window_text != new_window_text):
                        print("Update source window to %s" % (new_window_text))
                        obs.obs_data_set_string(cur_settings, "window", new_window_text)
                        obs.obs_source_update(cur_source, cur_settings)

                obs.obs_data_release(cur_settings)

        obs.sceneitem_list_release(scene_items)


def script_load(settings):
    print("Script loaded")
    obs.obs_frontend_add_event_callback(on_event)
