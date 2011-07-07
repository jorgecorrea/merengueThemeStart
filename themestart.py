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
from django.core.management.base import CommandError
from merengue.base.management.base import MerengueCommand

from merengue.theming.checker import check_themes
import shutil


def create_default_css(themestart, mediadir, theme_name, valuesDic):
      columns =  valuesDic['leftcolumn']  + valuesDic['rightcolumn']
      maincolumn = valuesDic['portalwidth'] - columns - valuesDic['dmargin']*2 -valuesDic['dpadding']*2
      valuesDic['leftcontent'] = '0px'
      valuesDic['rightcontent'] = '0px'
      if (valuesDic['leftcolumn'] == 0):
          valuesDic['leftcolumn'] = '0px; display: none; visibility: hidden'
          shutil.copy2(themestart + '/inc.rightsidebar.html', templatedir + '/' + theme_name + '/inc.rightsidebar.html')
      else:
          valuesDic['leftcontent'] = str(valuesDic['leftcolumn']-valuesDic['dpadding']*2-2) + 'px'
          valuesDic['leftcolumn']  = str(valuesDic['leftcolumn']) + 'px'
          maincolumn = maincolumn - valuesDic['dmargin']*2

      if (valuesDic['rightcolumn'] == 0):
          valuesDic['rightcolumn'] = '0px; display: none; visibility: hidden'
          shutil.copy2(themestart + '/inc.leftsidebar.html', templatedir + '/' + theme_name + '/inc.leftsidebar.html')
      else:
          valuesDic['rightcontent'] = str(valuesDic['rightcolumn'] - valuesDic['dpadding']*2-2) + 'px'
          valuesDic['rightcolumn'] = str(valuesDic['rightcolumn']) + 'px'
          maincolumn = maincolumn - valuesDic['dmargin']*2
      
      if (valuesDic['portalwidth']==0):
          valuesDic['portalwidth'] = '100%'
      else:
          valuesDic['portalwidth'] = str(valuesDic['portalwidth']) + 'px'

      valuesDic['maincolumn'] = str(maincolumn) +'px'
      print 'Creating theme'
      contents = open(themestart + "/default.css", "r").read()
      o = open(mediadir + '/' + theme_name + "/css/default.css", "w")
      contents = contents.replace("portalwidth", valuesDic['portalwidth'])
      contents = contents.replace("leftcolumn", valuesDic['leftcolumn'])
      contents = contents.replace("leftcontent", valuesDic['leftcontent'])
      contents = contents.replace("rightcolumn", valuesDic['rightcolumn'])
      contents = contents.replace("rightcontent", valuesDic['rightcontent'])
      contents = contents.replace("maincolumn", valuesDic['maincolumn'])
      contents = contents.replace("dpadding", str(valuesDic['dpadding']) + 'px')
      contents = contents.replace("dmargin", str(valuesDic['dmargin']) + 'px')
      contents = contents.replace("color1", valuesDic['color1'])
      contents = contents.replace("color2", valuesDic['color2'])
      contents = contents.replace("color3", valuesDic['color3'])
      contents = contents.replace("color4", valuesDic['color4'])
      o.write(contents)
      o.close()

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
            try:
                os.makedirs(os.path.join(mediadir, theme_name, 'css'))
            except OSError:
                raise CommandError("This theme already exists, please try another name")
            
            os.makedirs(os.path.join(mediadir, theme_name, 'img'))
            os.makedirs(os.path.join(mediadir, theme_name, 'js'))
            templatedir =  os.path.join(settings.BASEDIR, 'templates/themes')
            os.mkdir(os.path.join(templatedir, theme_name))
            shutil.copy2(themestart + '/base.html', templatedir + '/' + theme_name + '/base.html')
            shutil.copy2(themestart + '/layout.css', mediadir + '/' + theme_name + '/css/layout.css')
            valuesDic = {}
            valuesDic['portalwidth'] = int(input("Select portal width (0 = full screen, or a value for portal width tipical values are between 800 and 1024): "))
            valuesDic['leftcolumn'] = int(input("Select left column width (0 = widthout left column: "))
            valuesDic['rightcolumn'] = int(input("Select right column width (0 = widthout right column: "))
            valuesDic['dpadding'] = int(input("Select default main blocks paddings: "))
            valuesDic['dmargin'] = int(input("Select default main blocks margin: "))
            valuesDic['color1'] = raw_input("Select the main text color (black, blue, #dedede) :")
            valuesDic['color2'] = raw_input("Select the body background color :")
            valuesDic['color3'] = raw_input("Select link color: ")
            valuesDic['color4'] = raw_input("Select link hover color: ")

            
            create_default_css(themestart, mediadir, theme_name, valuesDic)
            check_themes() #this line add the new theme to theming table in the project BD
            print 'To start using your new theme activate it in your admin'
            print 'To change your theme design you could edit css in: ' +  os.path.join(mediadir, theme_name) + '/css/'
            print 'To add or modify custom templates you could go: ' + os.path.join(templatedir, theme_name)
