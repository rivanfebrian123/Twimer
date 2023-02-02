# MIT License
#
# Copyright (c) 2023 马·里文
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# SPDX-License-Identifier: MIT

from threading import Thread
from gi.repository import Adw, Gtk, GLib
from . import model, utils

@Gtk.Template(resource_path='/org/gnome/Example/window.ui')
class TwimerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'TwimerWindow'
    stack = Gtk.Template.Child()
    ani = Gtk.Template.Child()
    budi = Gtk.Template.Child()
    bibi = Gtk.Template.Child()
    tono = Gtk.Template.Child()
    posy = Gtk.Template.Child()
    negy = Gtk.Template.Child()
    snow = Gtk.Template.Child()
    aha = Gtk.Template.Child()
    elu = Gtk.Template.Child()
    loco = Gtk.Template.Child()
    model = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("notify::default-width", self.on_ukuran)
        self.connect("state-flags-changed", self.on_ukuran)

    def on_ukuran(self, widget, pspec):
        utils.orient_box_from_window(self, self.bibi, self.snow, 640)

    def present(self, **kwargs):
        super().present(**kwargs)

        if not self.model:
            self.model = model.Model()

    def analisis(self):
        self.loco.get_style_context().add_class("muter")
        self.aha.set_sensitive(False)
        self.elu.set_sensitive(False)
        self.snow.get_vadjustment().set_value(0)

        try:
            self.model.analisis(self.aha.get_text())

            self.tono.set_from_pixbuf(utils.imgarray2pixbuf(self.model.pie()))
            self.posy.set_from_pixbuf(utils.imgarray2pixbuf(
                self.model.wordcloud_pos()))
            self.negy.set_from_pixbuf(utils.imgarray2pixbuf(
                self.model.wordcloud_neg()))

            self.stack.set_visible_child(self.ani)
            self.aha.set_text('')
        except:
            GLib.idle_add(lambda: utils.tampilkan_dialog(
                self, "Maaf, analisis gagal",
                "Mungkin kendala jaringan atau kata kunci salah"))
            self.elu.set_sensitive(True)
        finally:
            self.loco.get_style_context().remove_class("muter")
            self.aha.set_sensitive(True)

    @Gtk.Template.Callback()
    def on_analisis(self, widget):
        Thread(target=self.analisis).start()

    @Gtk.Template.Callback()
    def on_buat_baru(self, widget):
        self.stack.set_visible_child(self.budi)

    @Gtk.Template.Callback()
    def on_ngetik(self, widget):
        self.elu.set_sensitive(widget.get_text() != '')
