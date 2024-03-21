from functools import lru_cache
import inspect
import datetime
from pprint import pformat

from pydantic_settings import BaseSettings, SettingsConfigDict

@lru_cache
class Settings_DBG(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    DEBUG_LOG: bool = False
    DEBUG_LOG_ON_CONSOLE: bool = False
    DEBUG_LOG_IN_FILE: bool = False
    DEBUG_LOG_FILE_NAME: str = "backend_debug_log.txt"

settings_dbg = Settings_DBG()

def object_description(obj):
    """Generate a detailed and pretty-printed description of an object."""
    if hasattr(obj, "__dict__"):  # Check if the object is a class instance with attributes
        class_name = obj.__class__.__name__
        # Use pformat to pretty-print the attributes of the object
        attributes_pretty = pformat(obj.__dict__, indent=4, width=1)
        return f"{class_name} with attributes: {attributes_pretty}"
    else:
        return pformat(obj, indent=4, width=1)  # Pretty print any object


# Usage: debug_print(test_obj)
#        debug_print(f"Object dump: {test_obj}")
def debug_print(*args):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    frame = inspect.currentframe().f_back
    file_name = frame.f_globals["__file__"]
    line_number = frame.f_lineno
    function_name = frame.f_code.co_name
    
    # Prepare the message based on the number and type of args
    if len(args) == 1 and not isinstance(args[0], str):
        # For a single non-string argument, generate a detailed description
        message = object_description(args[0])
    else:
        # For other cases, format the string with args or handle a single string
        message = " ".join([object_description(arg) if not isinstance(arg, str) else arg for arg in args])
    
     # Combine everything into a debug string
    debug_string = f"==> {current_time} - {file_name}:{line_number} ({function_name}) - {message}\n"

    # Print the debug string
    if settings_dbg.DEBUG_LOG:
        if settings_dbg.DEBUG_LOG_IN_FILE:
            with open(settings_dbg.DEBUG_LOG_FILE_NAME, "a") as file:
                file.write(debug_string + "\n")
                file.flush()

        if settings_dbg.DEBUG_LOG_ON_CONSOLE:
            print(debug_string)