from gi.repository import Gtk, Gio, GdkPixbuf
from io import BytesIO, StringIO, TextIOWrapper
import numpy as np
from PIL import Image
import csv

def get_data(path):
  return Gio.resources_lookup_data(path, 0).get_data()

def get_bytes(path):
  return BytesIO(get_data(path))

def get_string(path):
  return TextIOWrapper(BytesIO(get_data(path)))

def tsv2dict(path):
  with get_string(path) as f:
    reader = csv.reader(f, delimiter='\t')
    lex = {}

    next(f)

    for row in reader:
      lex[row[0]] = int(row[1])

    return lex

def buf2imgarray(buf):
    buf.seek(0)

    return np.asarray(Image.open(buf))

def imgarray2pixbuf(imgarray):
    tinggi, lebar, channel = imgarray.shape

    return GdkPixbuf.Pixbuf.new_from_data(
        imgarray.flatten(),
        GdkPixbuf.Colorspace.RGB,
        channel == 4, 8, lebar, tinggi, channel*lebar)


def orient_box_from_window(win, box, sw, min_width):
    if win.props.maximized:
        width = win.get_allocation().width
    else:
        width = win.props.default_width

    if width < min_width:
        sw.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        box.set_orientation(Gtk.Orientation.VERTICAL)
    else:
        sw.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        box.set_orientation(Gtk.Orientation.HORIZONTAL)

dialog = Gtk.MessageDialog(
    message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CANCEL,
    modal=True
)

dialog.connect("response", lambda x, y: dialog.hide())

def tampilkan_dialog(win, teks1, teks2):
    global dialog

    dialog.set_transient_for(win)

    dialog.props.text = teks1
    dialog.props.secondary_text = teks2

    dialog.show()
