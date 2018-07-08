from base64 import b85decode as d

#Each 64x8 chunk is 10 and 4/6 characters wide;
#Each 32x8 chunk is 5 and 2/6 characters wide

f68enc=lambda s, bold=False: b''.join((font68 if not bold else font68_bold)[b] for b in s.encode())

font68 = {
  0x0d :	d("00000000"), # \r CARRIAGE RETURN
  0x20 :	d("00000000"), # \u0020 SPACE
  0x21 :	d("0000_000"), # !
  0x22 :	d("000L72LJ"), # "
  0x23 :	d("02F@|e-r"), # #
  0x24 :	d("03<4ZDiQ"), # $
  0x25 :	d("03#C!WMT"), # %
  0x26 :	d("05(ZgB2W"), # &
  0x27 :	d("000F8000"), # '
  0x28 :	d("000~!K>z"), # (
  0x29 :	d("002QE8~^"), # )
  0x2a :	d("02By52ow"), # *
  0x2b :	d("00;;^2nY"), # +
  0x2c :	d("002-h000"), # ,
  0x2d :	d("00;;O2nY"), # -
  0x2e :	d("003ZM000"), # .
  0x2f :	d("03Z+u1Of"), # /
  0x30 :	d("06tMkMLq"), # 0
  0x31 :	d("002UNKmY"), # 1
  0x32 :	d("0779=Nk#"), # 2
  0x33 :	d("03ks|OEC"), # 3
  0x34 :	d("02mY!e-H"), # 4
  0x35 :	d("053^NNih"), # 5
  0x36 :	d("06a=bNiY"), # 6
  0x37 :	d("00D6c1p@"), # 7
  0x38 :	d("05(ZUNj3"), # 8
  0x39 :	d("00v1(DIN"), # 9
  0x3a :	d("001^N000"), # :
  0x3b :	d("0034t000"), # ;
  0x3c :	d("00<N!K>z"), # <
  0x3d :	d("02CAy6ch"), # =
  0x3e :	d("06`)Y2mk"), # >
  0x3f :	d("00IF~2?h"), # ?
  0x40 :	d("05VB=K|T"), # @
  0x41 :	d("0Dch>5q<"), # A
  0x42 :	d("0DnnINj3"), # B
  0x43 :	d("06sxMK_U"), # C
  0x44 :	d("0DnP2A{+"), # D
  0x45 :	d("0DnnINkI"), # E
  0x46 :	d("0DlPy2>}"), # F
  0x47 :	d("06sxUNqP"), # G
  0x48 :	d("0DlMw2!8"), # H
  0x49 :	d("002RMK>z"), # I
  0x4a :	d("03bj?KLG"), # J
  0x4b :	d("0DlM+B0&"), # K
  0x4c :	d("0DnM0KtK"), # L
  0x4d :	d("0Dl4u0)G"), # M
  0x4e :	d("0DlAs5Pt"), # N
  0x4f :	d("06sxMK|T"), # O
  0x50 :	d("0DlPy2?h"), # P
  0x51 :	d("06sxcAzl"), # Q
  0x52 :	d("0DlP?DMk"), # R
  0x53 :	d("07gkkNih"), # S
  0x54 :	d("009Ai0Ra"), # T
  0x55 :	d("06#!LKtB"), # U
  0x56 :	d("03RSgARh"), # V
  0x57 :	d("06#!DKtB"), # W
  0x58 :	d("0Amyg6k`"), # X
  0x59 :	d("00#(g2nP"), # Y
  0x5a :	d("0AW!{MMD"), # Z
  0x5b :	d("004hMK>z"), # [
  0x5c :	d("02LN|78L"), # \u005c BACKSLASH
  0x5d :	d("002Qje*g"), # ]
  0x5e :	d("00aU70t5"), # ^
  0x5f :	d("06;)MKtK"), # _
  0x60 :	d("000331ON"), # `
  0x61 :	d("03cLURCo"), # a
  0x62 :	d("0DnkCL^u"), # b
  0x63 :	d("060WML?8"), # c
  0x64 :	d("060WMNPh"), # d
  0x65 :	d("060`sR2T"), # e
  0x66 :	d("00@2w0Rj"), # f
  0x67 :	d("02rjCq<j"), # g
  0x68 :	d("0DlMs1b6"), # h
  0x69 :	d("002aNKmY"), # i
  0x6a :	d("03bj_Jpc"), # j
  0x6b :	d("004gwC`1"), # k
  0x6c :	d("002RMKmY"), # l
  0x6d :	d("0DJ@(1b6"), # m
  0x6e :	d("0DJ@l1b6"), # n
  0x6f :	d("060WML^u"), # o
  0x70 :	d("0Q@8*Bp3"), # p
  0x71 :	d("02m}BDEt"), # q
  0x72 :	d("0DK4p1PA"), # r
  0x73 :	d("07z6+R3H"), # s
  0x74 :	d("00cioKp+"), # t
  0x75 :	d("06aiIAbb"), # u
  0x76 :	d("030AdARG"), # v
  0x77 :	d("06ah-Ks*"), # w
  0x78 :	d("07NJdC`1"), # x
  0x79 :	d("01Qx2P&@"), # y
  0x7a :	d("07PU|Ohf"), # z
  0x7b :	d("000O!K>z"), # {
  0x7c :	d("0001g000"), # |
  0x7d :	d("002QY2mk"), # }
  0x7e :	d("00;;w90&"), # \u2192 RIGHTWARDS ARROW
  0x7f :	d("00<l^2nY"), # \u2190 LEFTWARDS ARROW
  0xb0 :	d("000LC2LJ"), # \u00b0 DEGREE SYMBOL
  0xe1 :	d("03cOVRd@"), # \u00e4 LOWERCASE A WITH DIAERESIS
  0xe2 :	d("0Dc7}B^m"), # \u03b2 GREEK LOWERCASE BETA
  0xef :	d("060ZNMK}"), # \u00f6 LOWERCASE O WITH DIAERESIS
  0xf5 :	d("06alJA$$"), # \u00dc LOWERCASE U WITH DIAERESIS
}

font68_bold = {
  0x0d :	d("00000000"), # \r CARRIAGE RETURN
  0x20 :	d("00000000"), # \u0020 SPACE
  0x21 :	d("002)<000"), # !
  0x22 :	d("00##E2L}"), # "
  0x23 :	d("02F@|e-r"), # #
  0x24 :	d("03<4ZDiQ"), # $
  0x25 :	d("ATt{bW?}"), # %
  0x26 :	d("05*SFCUy"), # &
  0x27 :	d("00ajE000"), # '
  0x28 :	d("031GJK>z"), # (
  0x29 :	d("06}9u8~^"), # )
  0x2a :	d("02By52ow"), # *
  0x2b :	d("00=%l2mk"), # +
  0x2c :	d("002O6FaQ"), # ,
  0x2d :	d("00;;O2nY"), # -
  0x2e :	d("003ZM000"), # .
  0x2f :	d("ATSsV1_A"), # /
  0x30 :	d("06u>~e?9"), # 0
  0x31 :	d("002UNe?R"), # 1
  0x32 :	d("0Ah1lPeu"), # 2
  0x33 :	d("03l&Te>("), # 3
  0x34 :	d("02mw=dwB"), # 4
  0x35 :	d("055Mzc`*"), # 5
  0x36 :	d("06cz6c`y"), # 6
  0x37 :	d("00DV@2Lk"), # 7
  0x38 :	d("05*R~e>M"), # 8
  0x39 :	d("07g$~KOO"), # 9
  0x3a :	d("001^N000"), # :
  0x3b :	d("06=y&000"), # ;
  0x3c :	d("00<m5V?h"), # <
  0x3d :	d("02CAy6ch"), # =
  0x3e :	d("06}9m90&"), # >
  0x3f :	d("00L844+a"), # ?
  0x40 :	d("05W?)e?9"), # @
  0x41 :	d("0DgZFe|`"), # A
  0x42 :	d("0Dpf;e>M"), # B
  0x43 :	d("06u>~V<G"), # C
  0x44 :	d("0DpgDJ{$"), # D
  0x45 :	d("0Dpf;NkI"), # E
  0x46 :	d("0Dpf82>}"), # F
  0x47 :	d("06u>~dwK"), # G
  0x48 :	d("0Dpf7e}4"), # H
  0x49 :	d("06~9$K>z"), # I
  0x4a :	d("03cvNe?I"), # J
  0x4b :	d("0DpfRcVh"), # K
  0x4c :	d("0Dpf#KtK"), # L
  0x4d :	d("0DpcAet!"), # M
  0x4e :	d("0Dpc6KYs"), # N
  0x4f :	d("06u>~e?9"), # O
  0x50 :	d("0Dpf84+a"), # P
  0x51 :	d("06u>~KW+"), # Q
  0x52 :	d("0DpfOe`W"), # R
  0x53 :	d("07g$qc`*"), # S
  0x54 :	d("0Rex10Ra"), # T
  0x55 :	d("06%{~e?I"), # U
  0x56 :	d("03SbKKOX"), # V
  0x57 :	d("0DnIiKYs"), # W
  0x58 :	d("0C#@~e|G"), # X
  0x59 :	d("07p-7KOX"), # Y
  0x5a :	d("0AYDuPeT"), # Z
  0x5b :	d("0Dpf$K>z"), # [
  0x5c :	d("02LN|78L"), # \u00a5 YEN SIGN
  0x5d :	d("002Qje}4"), # ]
  0x5e :	d("00agD1_S"), # ^
  0x5f :	d("06;)MKtK"), # _
  0x60 :	d("009FA1ON"), # `
  0x61 :	d("03dW!e0T"), # a
  0x62 :	d("0Dpf(d^i"), # b
  0x63 :	d("062U^Y$y"), # c
  0x64 :	d("062U^e}4"), # d
  0x65 :	d("062V9To?"), # e
  0x66 :	d("00@462>}"), # f
  0x67 :	d("02sWa{Co"), # g
  0x68 :	d("0Dpf3e0T"), # h
  0x69 :	d("07QL#KmY"), # i
  0x6a :	d("03cvQeLV"), # j
  0x6b :	d("0DpfFd~5"), # k
  0x6c :	d("06~9$KmY"), # l
  0x6d :	d("0DOEHe0T"), # m
  0x6e :	d("0DOD|e0T"), # n
  0x6f :	d("062U^d^i"), # o
  0x70 :	d("0Q~$UJQx"), # p
  0x71 :	d("02n+Z{QL"), # q
  0x72 :	d("0DOE13<L"), # r
  0x73 :	d("07zU^bR+"), # s
  0x74 :	d("00cjOL;w"), # t
  0x75 :	d("06cs^e0%"), # u
  0x76 :	d("031AEJRA"), # v
  0x77 :	d("0DL?UJbV"), # w
  0x78 :	d("0Bn2^d~5"), # x
  0x79 :	d("01RAEd^`"), # y
  0x7a :	d("0AzGrOhf"), # z
  0x7b :	d("00=&JK>z"), # {
  0x7c :	d("004h~000"), # |
  0x7d :	d("002REJ_r"), # }
  0x7e :	d("00=5R90&"), # \u2192 RIGHWARDS ARROW
  0x7f :	d("00<mDDhL"), # \u2190 LEFTWARDS ARROW
  0xb0 :	d("00##J2L}"), # \u00b0 DEGREE SYMBOL
  0xe1 :	d("03mf$eR%"), # \u00e4 LOWERCASE A WITH DIAERESIS
  0xe2 :	d("0DgZZKN<"), # \u03b2 GREEK LOWERCASE BETA
  0xef :	d("06Bd`eK`"), # \u00f6 LOWERCASE O WITH DIAERESIS
  0xf5 :	d("06l#`eSH"), # \u00dc LOWERCASE U WITH DIAERESIS
}

#import codecs
#
#class Codec(codecs.Codec):
#	def encode(self,input,errors='strict'):
#		return codecs.charmap_encode(input,errors,font68)
#	def decode(self, input, errors='strict'):
#		raise NotImplementedError
#
#class IncrementalEncoder(codecs.IncrementalEncoder):
#	def encode(self, input, final=False):
#		return codecs.charmap_encode(input,errors,font68)[0]
#
#def getregentry():
#	return codecs.CodecInfo(
#	 name='font68',
#	 encode=Codec.encode,
#	 incrementalencoder=IncrementalEncoder,
#	)
