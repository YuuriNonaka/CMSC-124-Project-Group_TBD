import re
from enum import Enum

class TokenType(Enum):
    #program structure
    HAI = "HAI"
    KTHXBYE = "KTHXBYE"
    WAZZUP = "WAZZUP"
    BUHBYE = "BUHBYE"
    
    #variable declaration
    I_HAS_A = "I HAS A"
    ITZ = "ITZ"
    
    #assignment
    R = "R"
    
    #input/output
    VISIBLE = "VISIBLE"
    GIMMEH = "GIMMEH"
    
    #arithmetic operators
    SUM_OF = "SUM OF"
    DIFF_OF = "DIFF OF"
    PRODUKT_OF = "PRODUKT OF"
    QUOSHUNT_OF = "QUOSHUNT OF"
    MOD_OF = "MOD OF"
    BIGGR_OF = "BIGGR OF"
    SMALLR_OF = "SMALLR OF"
    
    #boolean operators
    BOTH_OF = "BOTH OF"
    EITHER_OF = "EITHER OF"
    WON_OF = "WON OF"
    NOT = "NOT"
    ALL_OF = "ALL OF"
    ANY_OF = "ANY OF"
    
    #comparison operators
    BOTH_SAEM = "BOTH SAEM"
    DIFFRINT = "DIFFRINT"
    
    #concatenation
    SMOOSH = "SMOOSH"
    
    #typecasting
    MAEK = "MAEK"
    IS_NOW_A = "IS NOW A"
    A = "A"
    
    #conditionals
    O_RLY = "O RLY?"
    YA_RLY = "YA RLY"
    MEBBE = "MEBBE"
    NO_WAI = "NO WAI"
    OIC = "OIC"
    
    #switch-case
    WTF = "WTF?"
    OMG = "OMG"
    OMGWTF = "OMGWTF"
    
    #loops
    IM_IN_YR = "IM IN YR"
    IM_OUTTA_YR = "IM OUTTA YR"
    UPPIN = "UPPIN"
    NERFIN = "NERFIN"
    YR = "YR"
    TIL = "TIL"
    WILE = "WILE"
    
    #functions
    HOW_IZ_I = "HOW IZ I"
    IF_U_SAY_SO = "IF U SAY SO"
    I_IZ = "I IZ"
    FOUND_YR = "FOUND YR"
    
    #break/return
    GTFO = "GTFO"
    
    #separator
    AN = "AN"
    MKAY = "MKAY"
    
    #data types
    NUMBR = "NUMBR Literal"
    NUMBAR = "NUMBAR Literal"
    YARN = "YARN Literal"
    TROOF = "TROOF Literal"
    NOOB = "NOOB Literal"
    
    #type keywords
    TYPE_NUMBR = "NUMBR"
    TYPE_NUMBAR = "NUMBAR"
    TYPE_YARN = "YARN"
    TYPE_TROOF = "TROOF"
    TYPE_NOOB = "NOOB"
    
    #identifiers
    VARIDENT = "Variable Identifier"
    FUNCIDENT = "Function Identifier"
    LABEL = "Loop Label"

    #special tokens
    LINEBREAK = "Line Break"
    
    #comments (for tracking, but ignored in output)
    COMMENT = "Comment"
    
    #unknown
    UNKNOWN = "Unknown"


#regex patterns for tokens (order matters - longest/most specific first)
TOKEN_PATTERNS = [
    #multiword keywords first (most specific)
    (r'\bI\s+HAS\s+A\b', TokenType.I_HAS_A),
    (r'\bSUM\s+OF\b', TokenType.SUM_OF),
    (r'\bDIFF\s+OF\b', TokenType.DIFF_OF),
    (r'\bPRODUKT\s+OF\b', TokenType.PRODUKT_OF),
    (r'\bQUOSHUNT\s+OF\b', TokenType.QUOSHUNT_OF),
    (r'\bMOD\s+OF\b', TokenType.MOD_OF),
    (r'\bBIGGR\s+OF\b', TokenType.BIGGR_OF),
    (r'\bSMALLR\s+OF\b', TokenType.SMALLR_OF),
    (r'\bBOTH\s+OF\b', TokenType.BOTH_OF),
    (r'\bEITHER\s+OF\b', TokenType.EITHER_OF),
    (r'\bWON\s+OF\b', TokenType.WON_OF),
    (r'\bALL\s+OF\b', TokenType.ALL_OF),
    (r'\bANY\s+OF\b', TokenType.ANY_OF),
    (r'\bBOTH\s+SAEM\b', TokenType.BOTH_SAEM),
    (r'\bIS\s+NOW\s+A\b', TokenType.IS_NOW_A),
    (r'\bO\s+RLY\?', TokenType.O_RLY),
    (r'\bYA\s+RLY\b', TokenType.YA_RLY),
    (r'\bNO\s+WAI\b', TokenType.NO_WAI),
    (r'\bIM\s+IN\s+YR\b', TokenType.IM_IN_YR),
    (r'\bIM\s+OUTTA\s+YR\b', TokenType.IM_OUTTA_YR),
    (r'\bHOW\s+IZ\s+I\b', TokenType.HOW_IZ_I),
    (r'\bIF\s+U\s+SAY\s+SO\b', TokenType.IF_U_SAY_SO),
    (r'\bI\s+IZ\b', TokenType.I_IZ),
    (r'\bFOUND\s+YR\b', TokenType.FOUND_YR),
    (r'\bWTF\?', TokenType.WTF),
    
    #single keywords
    (r'\bHAI\b', TokenType.HAI),
    (r'\bKTHXBYE\b', TokenType.KTHXBYE),
    (r'\bWAZZUP\b', TokenType.WAZZUP),
    (r'\bBUHBYE\b', TokenType.BUHBYE),
    (r'\bITZ\b', TokenType.ITZ),
    (r'\bR\b', TokenType.R),
    (r'\bVISIBLE\b', TokenType.VISIBLE),
    (r'\bGIMMEH\b', TokenType.GIMMEH),
    (r'\bDIFFRINT\b', TokenType.DIFFRINT),
    (r'\bNOT\b', TokenType.NOT),
    (r'\bSMOOSH\b', TokenType.SMOOSH),
    (r'\bMAEK\b', TokenType.MAEK),
    (r'\bMEBBE\b', TokenType.MEBBE),
    (r'\bOIC\b', TokenType.OIC),
    (r'\bOMG\b', TokenType.OMG),
    (r'\bOMGWTF\b', TokenType.OMGWTF),
    (r'\bUPPIN\b', TokenType.UPPIN),
    (r'\bNERFIN\b', TokenType.NERFIN),
    (r'\bYR\b', TokenType.YR),
    (r'\bTIL\b', TokenType.TIL),
    (r'\bWILE\b', TokenType.WILE),
    (r'\bGTFO\b', TokenType.GTFO),
    (r'\bAN\b', TokenType.AN),
    (r'\bMKAY\b', TokenType.MKAY),
    
    #literals (before type keywords)
    (r'-?\d+\.\d+', TokenType.NUMBAR),  #float
    (r'-?\d+', TokenType.NUMBR),  #integer
    (r'"[^"]*"', TokenType.YARN),  #string
    (r'\b(WIN|FAIL)\b', TokenType.TROOF),  #boolean
    (r'\bNOOB\b', TokenType.NOOB),  #noob literal and type keyword
    
    #type keywords (after noob literal)
    (r'\bNUMBR\b', TokenType.TYPE_NUMBR),
    (r'\bNUMBAR\b', TokenType.TYPE_NUMBAR),
    (r'\bYARN\b', TokenType.TYPE_YARN),
    (r'\bTROOF\b', TokenType.TYPE_TROOF),
    (r'\bA\b', TokenType.A),
    
    #identifiers (last, catches everything else that looks like a variable)
    (r'[a-zA-Z][a-zA-Z0-9_]*', TokenType.VARIDENT),
]


def compile_patterns():
    #compile all regex patterns for efficiency
    return [(re.compile(pattern), token_type) for pattern, token_type in TOKEN_PATTERNS]


COMPILED_PATTERNS = compile_patterns()