# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2018 Roosembert Palacios (Orbstheorem)
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for TreeNode."""

import pytest

from qutebrowser.utils import usertypes


def test_constructor_parent_adopts_node():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(a)

    assert b in a.children


def test_constructor_reparents_childs():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(a)
    c = usertypes.TreeNode(None, children = [a, b])

    assert c == a.parent
    assert c == b.parent


def test_reparent_root():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(None)
    a.reparent(b)

    assert b == a.parent
    assert a in b.children


def test_reparent_to_root():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(a)
    b.reparent(None)

    assert None == b.parent
    assert b not in a.children


def test_reparent_child():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(a)
    c = usertypes.TreeNode(a)
    c.reparent(b)

    assert c not in a.children
    assert b in a.children
    assert c in b.children
    assert b == c.parent


def test_disown_child():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(a)
    a.disown(b)

    assert b not in a.children
    assert not b.parent


def test_adopt_child():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(None)
    a.adopt(b)

    assert a == b.parent
    assert b in a.children


def test_promote_first():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(a)
    c = usertypes.TreeNode(a)
    a.promote(b)

    assert b == a.children[0]


def test_promote():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(a)
    c = usertypes.TreeNode(a)
    a.promote(c)

    assert c == a.children[0]


def test_demote_last():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(a)
    c = usertypes.TreeNode(a)
    a.demote(c)

    assert c == a.children[-1]


def test_demote():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(a)
    c = usertypes.TreeNode(a)
    a.demote(b)

    assert b == a.children[-1]


def test_render_test_data_1():
    a = usertypes.TreeNode(None)
    b = usertypes.TreeNode(a)
    c = usertypes.TreeNode(a)
    d = usertypes.TreeNode(None, [a])
    e = usertypes.TreeNode(b)
    f = usertypes.TreeNode(c)
    # d -> a -> [b -> e, c -> f]

    actual = usertypes.TreeNode.render(d)
    expected = ['', '└─ ', '   ├─ ', '   │  └─ ', '   └─ ', '      └─ ']

    assert actual == expected
