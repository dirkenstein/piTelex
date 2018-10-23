#!/usr/bin/python
"""
Telex Code Conversion
Baudot-Code = CCITT-1
Baudot-Murray-Code = CCITT-2

CCITT-2:
543.21      LTRS    FIGS
======      ==========================
000.00	    undef	
000.01	    E   	3
000.10	    <LF>    <LF>
000.11	    A   	-
001.00	    <SPACE> <SPACE>
001.01	    S   	'
001.10	    I   	8
001.11	    U   	7
010.00	    <CR>    <CR>
010.01	    D   	WRU?
010.10	    R   	4
010.11	    J   	BELL <BEL>
011.00	    N   	,
011.01	    F   	undef, $, Ä, %
011.10	    C   	:
011.11	    K   	(
100.00	    T   	5
100.01	    Z   	+
100.10	    L   	)
100.11	    W   	2
101.00	    H   	undef, #, Ü, Pound
101.01	    Y   	6
101.10	    P   	0
101.11	    Q   	1
110.00	    O   	9
110.01	    B   	?
110.10	    G   	undef, &, Ö, @
110.11	    FIGS    FIGS	
111.00	    M   	.
111.01	    X   	/
111.10	    V   	=
111.11	    LTRS    LTRS	

http://rabbit.eng.miami.edu/info/baudot.html   <<< wrong figs order!
http://www.baudot.net/docs/smith--teletype-codes.pdf
"""
__author__      = "Jochen Krapf"
__email__       = "jk@nerd2nerd.org"
__copyright__   = "Copyright 2018, JK"
__license__     = "GPL3"
__version__     = "0.0.1"

#######

'''
 MurrayLTRS.index('A') -> 3
 MurrayLTRS[3] -> 'A'
'''

class BaudotMurrayCode:
    _MurrayLUT = ['\x80E\nA SIU\rDRJNFCKTZLWHYPQOBG\x82MXV\x81', '\x803\n- \'87\r#4\a,\x80:(5+)2\x806019?\x80\x82./=\x81']
    _MurraySwitchLUT = [0x1F, 0x1B]

    def __init__(self):
        self._ModeA2M = None
        self._ModeM2A = 0   # letters
        
    def encode(self, ansi:str) -> list:
        ''' convert an ansi string to a list of baudot-murray-coded bytes '''
        ret = []

        ansi = ansi.upper()

        if self._ModeA2M == None:
            self._ModeA2M = 0   # letters
            ret.append(self._MurraySwitchLUT[self._ModeA2M])

        for a in ansi:
            try:
                m = self._MurrayLUT[self._ModeA2M].index(a)
                ret.append(m)
            except:
                try:
                    m = self._MurrayLUT[1-self._ModeA2M].index(a)
                    self._ModeA2M = 1 - self._ModeA2M
                    ret.append(self._MurraySwitchLUT[self._ModeA2M])
                    ret.append(m)
                except:
                    pass

        return ret


    def decode(self, murray:list) -> str:
        ''' convert a list/bytearray of baudot-murray-coded bytes to an ansi string '''
        ret = ''

        for m in murray:
            try:
                a = self._MurrayLUT[self._ModeM2A][m]
                if ord(a) >= 0x80:
                    if ord(a) == 0x81:
                        self._ModeM2A = 0   # letters
                    if ord(a) == 0x82:
                        self._ModeM2A = 1   # numbers
                else:
                    ret += a
            except:
                pass

        return ret

#######