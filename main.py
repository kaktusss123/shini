from source import tiravto, shintorg, avtolyalya
from source.agropiese import agropiese
from source.coleso import coleso
from source.masterlux import masterlux
from source.rezina import rezinacc
from source.tiraspol import tiraspol
from source.shiniod import shiniod

if __name__ == '__main__':
    print('-----------------------------TIRAVTO----------------------------')
    tiravto.write(tiravto.parse())
    print('----------------------------SHINTORG----------------------------')
    shintorg.write(shintorg.parse())
    print('-----------------------------REZINA-----------------------------')
    rezinacc.write(rezinacc.parse())
    print('----------------------------MASTERLUX---------------------------')
    masterlux.write(masterlux.parse())
    print('----------------------------SHINI-TIRASPOL----------------------')
    tiraspol.write(tiraspol.parse())
    print('-----------------------------COLESO-----------------------------')
    coleso.write(coleso.parse())
    print('----------------------------AGROPIESE---------------------------')
    agropiese.write(agropiese.parse())
    print('-----------------------------AVTOLYALYA-------------------------')
    avtolyalya.write(avtolyalya.parse())
    print('------------------------------SHINI.OD--------------------------')
    shiniod.write(shiniod.parse())
    print('------------------------------Done!-----------------------------')
