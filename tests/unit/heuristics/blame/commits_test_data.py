#!/usr/bin/env python
# -*- coding: utf-8 -*-
removed_one_line = """
commit 39f808fcd3f24554c7d10aa41aecc5f28e962299
Author: Commiter Commiter <commiter@commiter.com>
Date:   Sat May 24 11:36:58 2014 +0200

    removed sixth line

diff --git a/aa.txt b/aa.txt
index 414fb2d..dee101b 100644
--- a/aa.txt
+++ b/aa.txt
@@ -6 +5,0 @@ Fiveth Line
-Sixth Line
"""

replace_line_new_one = """
commit 253c2fa5f30a36217b02f8a8d11e410dc447f836
Author: Commiter Commiter <commiter@commiter.com>
Date:   Sat May 24 11:38:27 2014 +0200

    replace sixth line new one

diff --git a/aa.txt b/aa.txt
index 414fb2d..0e3a941 100644
--- a/aa.txt
+++ b/aa.txt
@@ -6 +6 @@ Fiveth Line
-Sixth Line
+New Sixth Line
"""

replace_line_two_ones = """
commit b06374f3b06a8359f85f7beafafff8de5b5f904c
Author: Commiter Commiter <commiter@commiter.com>
Date:   Sat May 24 11:40:14 2014 +0200

    replace one line, two ones

diff --git a/aa.txt b/aa.txt
index 414fb2d..fb299ff 100644
--- a/aa.txt
+++ b/aa.txt
@@ -6 +6,2 @@ Fiveth Line
-Sixth Line
+New Sixth Line
+New One Yet
"""


replace_line_two_ones_removed_one_line_add_one = """
commit 4db35f2bdf44a43bf1c821e6701cb4924524f45d
Author: Commiter Commiter <commiter@commiter.com>
Date:   Sat May 24 11:42:48 2014 +0200

    removed one line, added 2 lines, removed one line and added one

diff --git a/aa.txt b/aa.txt
index 414fb2d..49b0466 100644
--- a/aa.txt
+++ b/aa.txt
@@ -6 +6,2 @@ Fiveth Line
-Sixth Line
+New Sixth Line
+New Sixth Lien again
@@ -9 +10 @@ Eigth Line
-Nineth Line
+New Nineth Line
"""
