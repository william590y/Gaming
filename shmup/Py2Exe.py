import cx_Freeze
import os.path
import os

os.environ['TCL_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tk8.6"

executables = [cx_Freeze.Executable('shmup.py')]
files = ['background.png','Explosion.wav','Laser_Shoot.wav','Laser_Shoot2.wav'
,'Laser_Shoot3.wav','laser.png','laser.wav','music.ogg','ship.png']
mob = ['mob{}.png'.format(i) for i in range(1,11)]
explode = ['regularExplosion0{}.png'.format(i) for i in range(9)]
files = files+mob+explode

cx_Freeze.setup(
        name = 'shmup',
        options = {
                'build_exe':{'packages':['pygame'],
                             'include_files':files}}
        ,executables = executables
        ,version = '1.0.0')
