import Quartz
import AppKit
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def send_cgevent_paste() -> bool:
    """
    Send CGEvent Cmd+V to simulate paste operation using Carbon events.
    
    Returns:
        bool: True if paste was successful, False otherwise
    """
    try:
        # Create key down event for Command key
        cmd_key = Quartz.CGKeyCode.kVK_Command
        cmd_down = Quartz.CGEventCreateKeyboardEvent(None, cmd_key, True)
        Quartz.CGEventSetFlags(cmd_down, Quartz.CGEventFlagsMaskCommand)
        
        # Create key down event for 'v' key
        v_key = Quartz.CGKeyCode.kVK_ANSI_V
        v_down = Quartz.CGEventCreateKeyboardEvent(None, v_key, True)
        Quartz.CGEventSetFlags(v_down, Quartz.CGEventFlagsMaskCommand)
        
        # Create key up events
        cmd_up = Quartz.CGEventCreateKeyboardEvent(None, cmd_key, False)
        Quartz.CGEventSetFlags(cmd_up, Quartz.CGEventFlagsMaskCommand)
        v_up = Quartz.CGEventCreateKeyboardEvent(None, v_key, False)
        Quartz.CGEventSetFlags(v_up, Quartz.CGEventFlagsMaskCommand)
        
        # Create event queue and post events
        event_queue = Quartz.CGEventCreateSourceFromName("surrogate-1-paste")
        Quartz.CGEventPostToSource(Quartz.kCGSessionEventTap, cmd_down, event_queue)
        Quartz.CGEventPostToSource(Quartz.kCGSessionEventTap, v_down, event_queue)
        Quartz.CGEventPostToSource(Quartz.kCGSessionEventTap, v_up, event_queue)
        Quartz.CGEventPostToSource(Quartz.kCGSessionEventTap, cmd_up, event_queue)
        
        logger.info("CGEvent Cmd+V paste sent successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send CGEvent Cmd+V paste: {e}")
        return False