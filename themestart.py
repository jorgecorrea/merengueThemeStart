# Copyright (c) 2010 by Yaco Sistemas <jcorrea@yaco.es>
#
# This file is part of Merengue.
#
# Merengue is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Merengue is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Merengue.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from django.conf import settings
from django.core.management import call_command

from merengue.base.management.base import MerengueCommand
from merengue.pluggable.utils import get_plugins_dir
from merengue.theming.checker import check_themes
from merengue.theming.models import Theme
import shutil


class Command(MerengueCommand):
    help = "Generate a theme width a default design"

    def handle(self, *args, **options):
        usage = "Example of theme creation: ./manage.py themestart mytheme"
        if len(sys.argv) < 3:
            print usage
        else:
            themestart="merengue/base/management/commands/themestart"
            theme_name = sys.argv[2]
            mediadir = os.path.join(settings.MEDIA_ROOT, 'themes')
            os.makedirs(os.path.join(mediadir, theme_name, 'css'))
            os.makedirs(os.path.join(mediadir, theme_name, 'img'))
            os.makedirs(os.path.join(mediadir, theme_name, 'js'))
            templatedir =  os.path.join(settings.BASEDIR, 'templates/themes')
            os.mkdir(os.path.join(templatedir, theme_name))
            shutil.copy2(themestart + '/base.html', templatedir + '/' + theme_name + '/base.html')
            shutil.copy2(themestart + '/layout.css', mediadir + '/' + theme_name + '/css/layout.css')
            portalwidth = int(input("Select portal width (0 = full screen, or a value for portal width tipical values are between 800 and 1024): "))
            leftcolumn = int(input("Select left column width (0 = widthout left column: "))
            rightcolumn = int(input("Select right column width (0 = widthout right column: "))
            dpadding = int(input("Select default main blocks paddings: "))
            dmargin = int(input("Select default main blocks margin: "))
            color1 = raw_input("Select the main text color (black, blue, #dedede) :")
            color2 = raw_input("Select the body background color :")
            color3 = raw_input("Select link color: ")
            color4 = raw_input("Select link hover color: ")

            columns =  leftcolumn  + rightcolumn
            maincolumn = portalwidth - columns - dmargin*2 - dpadding*2
            leftcontent = '0'
            rightcontent = '0'
            if (leftcolumn == 0):
                leftcolumn = '0px; display: none; visibility: hidden'
                shutil.copy2(themestart + '/inc.rightsidebar.html', templatedir + '/' + theme_name + '/inc.rightsidebar.html')
            else:
                leftcontent = str(leftcolumn-dpadding*2-2) + 'px'
                leftcolumn = str(leftcolumn) + 'px'
                maincolumn = maincolumn - dmargin*2

            if (rightcolumn == 0):
                rightcolumn = '0px; display: none; visibility: hidden'
                shutil.copy2(themestart + '/inc.leftsidebar.html', templatedir + '/' + theme_name + '/inc.leftsidebar.html')
            else:
                rightcontent = str(rightcolumn-dpadding*2-2) + 'px'
                rightcolumn = str(rightcolumn) + 'px'
                maincolumn = maincolumn - dmargin*2

            if (portalwidth==0):
                portalwidth = '100%'
            else:
                portalwidth = str(portalwidth) + 'px'

            dpadding = str(dpadding) + 'px'
            dmargin = str(dmargin) + 'px'
            maincolumn = str(maincolumn) +'px'

            print 'Creating theme'
            f = open(themestart + "/default.css")
            o = open(mediadir + '/' + theme_name + "/css/default.css", "w")

            for line in f.readlines():
                line = line.replace("portalwidth", portalwidth)
                line = line.replace("leftcolumn", leftcolumn)
                line = line.replace("leftcontent", leftcontent)
                line = line.replace("rightcolumn", rightcolumn)
                line = line.replace("rightcontent", rightcontent)
                line = line.replace("maincolumn", maincolumn)
                line = line.replace("dpadding", dpadding)
                line = line.replace("dmargin", dmargin)
                line = line.replace("color1", color1)
                line = line.replace("color2", color2)
                line = line.replace("color3", color3)
                line = line.replace("color4", color4)
                o.write(line)
            o.close()
            check_themes() #this line add the new theme to theming table in the project BD
            Theme.objects.filter(active=True).update(active=False)
            Theme.objects.filter(name=theme_name).update(active=True)
            print 'To start using your new theme restart your aplication server'
            print 'To change your theme design you could edit css in: ' +  os.path.join(mediadir, theme_name) + '/css/'
            print 'To add or modify custom templates you could go: ' + os.path.join(templatedir, theme_name)
