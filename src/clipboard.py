import wx


class UnsupportedOperation(Exception):
    """This exception is thrown in case an operation cannot be performed on the system"""

    def __init__(self, msg):
        super(UnsupportedOperation, self).__init__(msg)


def copy(content: str):
    """Write some text to the clipboard"""
    try:
        if not wx.TheClipboard.IsOpened():
            wx.TheClipboard.Open()
            wx.TheClipboard.SetData(wx.TextDataObject(content))
            wx.TheClipboard.Close()
    except:
        raise UnsupportedOperation("Your system does not have clipboard support")


def paste() -> str:
    """Read some text"""
    try:
        text_data = wx.TextDataObject()
        if not wx.TheClipboard.IsOpened():
            wx.TheClipboard.Open()
            success = wx.TheClipboard.GetData(text_data)
            wx.TheClipboard.Close()
        if success:
            return text_data.GetText()
        else:
            return None
    except:
        raise UnsupportedOperation("Your system does not have clipboard support")


def clear():
    if not wx.TheClipboard.IsOpened():
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(wx.TextDataObject(""))
        wx.TheClipboard.Flush()
        wx.TheClipboard.Close()
