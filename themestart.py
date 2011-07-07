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


def create_default_css(themestart, mediadir, theme_name, templatedir, valuesDic):
      columns =  valuesDic['leftcolumn']  + valuesDic['rightcolumn']
      maincolumn = valuesDic['portalwidth'] - columns - valuesDic['dmargin']*2 -valuesDic['dpadding']*2
      valuesDic['leftcontent'] = '0px'
      valuesDic['rightcontent'] = '0px'
      metric =  'px'
      minrest = 2
      if (valuesDic['portalwidth']==0):
          valuesDic['portalwidth'] = '100'
          maincolumn = 99.35 + maincolumn
          metric =  '%'
          minrest = 0

      if (valuesDic['leftcolumn'] == 0):
          valuesDic['leftcolumn'] = '0px; display: none; visibility: hidden'
          shutil.copy2(themestart + '/inc.rightsidebar.html', templatedir + '/' + theme_name + '/inc.rightsidebar.html')
      else:
          valuesDic['leftcontent'] = valuesDic['leftcolumn']-valuesDic['dpadding']*2 - minrest
          maincolumn = maincolumn  - valuesDic['dmargin']*2
          valuesDic['leftcolumn'] =   valuesDic['leftcolumn'] - valuesDic['dmargin']*2

      if (valuesDic['rightcolumn'] == 0):
          valuesDic['rightcolumn'] = '0px; display: none; visibility: hidden'
          shutil.copy2(themestart + '/inc.leftsidebar.html', templatedir + '/' + theme_name + '/inc.leftsidebar.html')
      else:
          valuesDic['rightcontent'] = valuesDic['rightcolumn'] - valuesDic['dpadding']*2-minrest
          maincolumn = maincolumn - valuesDic['dmargin']*2
          valuesDic['rightcolumn']= valuesDic['rightcolumn'] - valuesDic['dmargin']*2

      valuesDic['maincolumn'] = maincolumn
      print 'Creating theme'
      contents = open(themestart + "/default.css", "r").read()
      o = open(mediadir + '/' + theme_name + "/css/default.css", "w")
      if (metric=='px'):
          contents = open(themestart + "/default.css", "r").read()
      else:
          contents = open(themestart + "/defaultfluid.css", "r").read()
      contents = contents.replace("portalwidth", str(valuesDic['portalwidth']) + metric )
      contents = contents.replace("leftcolumn", str(valuesDic['leftcolumn']) + metric)
      contents = contents.replace("rightcolumn", str(valuesDic['rightcolumn']) + metric)
      if (metric=='px'):
          contents = contents.replace("leftcontent", str(valuesDic['leftcontent']) + metric)
          contents = contents.replace("rightcontent", str(valuesDic['rightcontent']) + metric)
      else:
          contents = contents.replace("leftcontent", 'auto');
          contents = contents.replace("rightcontent", 'auto');
      contents = contents.replace("maincolumn", str(valuesDic['maincolumn'])+ metric)
      contents = contents.replace("dpadding", str(valuesDic['dpadding']) + metric)
      contents = contents.replace("dmargin", str(valuesDic['dmargin']) + metric)
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
            if(valuesDic['portalwidth']==0):
                valuesDic['leftcolumn'] = int(input("Select left column percentaje width (0 = widthout left column, othercase (12 to 20 %)): "))
                valuesDic['rightcolumn'] = int(input("Select right column percentaje width (0 = widthout right column, othercase (12 to 20 %)): "))
                valuesDic['dpadding'] = 2
                valuesDic['dmargin'] = 2
                #valuesDic['dpadding'] = int(input("Select default main blocks paddings (between 0 and 3): "))
                #valuesDic['dmargin'] = int(input("Select default main blocks margin (between 0 and 3): "))
            else:
                valuesDic['leftcolumn'] = int(input("Select left column width (0 = widthout left column): "))
                valuesDic['rightcolumn'] = int(input("Select right column width (0 = widthout right column): "))
                valuesDic['dpadding'] = int(input("Select default main blocks paddings: "))
                valuesDic['dmargin'] = int(input("Select default main blocks margin: "))
            valuesDic['color1'] = raw_input("Select the main text color (black, blue, #dedede) :")
            valuesDic['color2'] = raw_input("Select the body background color :")
            valuesDic['color3'] = raw_input("Select link color: ")
            valuesDic['color4'] = raw_input("Select link hover color: ")

            
            create_default_css(themestart, mediadir, theme_name, templatedir, valuesDic)
            check_themes() #this line add the new theme to theming table in the project BD
            print 'To start using your new theme activate it in your admin'
            print 'To change your theme design you could edit css in: ' +  os.path.join(mediadir, theme_name) + '/css/'
            print 'To add or modify custom templates you could go: ' + os.path.join(templatedir, theme_name)
