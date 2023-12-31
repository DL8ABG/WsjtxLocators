#!/usr/bin/python3
#
# Evaluating the WSJT-X logbook to gain information on worked locator squares.
# The result is given as "locator map" file in html or txt format.
#
# Frank Hänsel, DL8ABG
#
# CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
#
###################################
# Changelog:
#
# Dec/2023
# - option for command line parameters
# - exception handling on file opens
# - more html implementation
#   (background color for table cells)
# - started implementing html output
# - output file for locator output in console during startup
#
# Sep/2021
# - Initial setup of file
# - optimisation of prior version
#
###################################
# Ideas:
# - filter by band and/or mode
#
###################################


###################################
# import the packages we need
###################################

# for sys.exit
import sys

# use regular expressions
import re

# Use the parser for command line arguments
from argparse import ArgumentParser

###################################
# Defintion of standard values
###################################

# name of output file
# will be completed by "." and OUTMODE as suffix
DEF_LOCOUTPUT="locatormap"

# name of WSJT-X logfile
DEF_WSJTXLOG="wsjtx.log"

# home quare
DEF_MYSQUARE="JO52"

# own callsign
DEF_MYCALL="DL8ABG"



# background color for own square in html table
BGCOLOR_OWN="#FF0000"

# background color for empty field in html table (blue ocean)
BGCOLOR_EMPTY="#CCEEFF"

# background color for worked field in html table (light brown earth)
BGCOLOR_FIELD="#DFAF9F"

# background color for worked squares in html table (dark brown earth)
BGCOLOR_SQUARE="#994D33"



# name parts of fields and squares to iterate over (west to east)
fieldsWE = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"]

# name parts of fields and squares to iterate over (north to south)
fieldsNS = ["R", "Q", "P", "O", "N", "M", "L", "K", "J", "I", "H", "G", "F", "E", "D", "C", "B", "A"]

# Square numbers west to east
squaresWE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# square numbers north to south
squaresNS = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]



###################################
# evaluate command line parameters
###################################

## use the argumentparser

# instanciate the parser
parser = ArgumentParser(description="Generate an overview of worked locators from your wsjt-x logfile",
                        epilog="\nby DL8ABG")

# choose text output instead of html
parser.add_argument("-t", "--txt",
                    action="store_true",
                    help="use text output instead of html")

# define output file name
parser.add_argument("-o", "--outfile",
                    metavar="file",
                    help="name of output file, the suffix .txt or .html will be added through the output format (default " + DEF_LOCOUTPUT+ ")",
                    default=DEF_LOCOUTPUT)

# define name of logfile
#   -l <file> read log from <file> rather than from default file name
parser.add_argument("-l", "--logfile",
                    metavar="file",
                    help="name of wsjt-x logfile (default " + DEF_WSJTXLOG + ")",
                    default=DEF_WSJTXLOG)

# define your home square
#   -s <square> define my home field
parser.add_argument("-s", "--square",
                    metavar="SQUARE",
                    help="your home square (default " + DEF_MYSQUARE + ")",
                    default=DEF_MYSQUARE)


# define your callsign
#   -c <call> give my own call to be printed in output
parser.add_argument("-c", "--call",
                    metavar="CALL",
                    help="your callsign (default " + DEF_MYCALL + ")",
                    default=DEF_MYCALL)

# extract the results
args = vars(parser.parse_args())

# print(args)

## Store arguemnts/results in specific variables

LOCOUTPUT = args["outfile"]
WSJTXLOG  = args["logfile"]
MYSQUARE  = args["square"].upper()
MYCALL    = args["call"].upper()

if (args["txt"]):
    OUTMODE="txt"
else:
    OUTMODE="html"

## test validity of parameters

# test if locator is correct
if (not re.fullmatch(r"[A-R][A-R][0-9][0-9]", MYSQUARE)):
    print(f"Locator not in correct format (must be e.g. JO52)")
    sys.exit(1)


## Print info to the user

print("reading log file " + WSJTXLOG)
print("writing locator mat to " + LOCOUTPUT + "." + OUTMODE)
print("own callsign is " + MYCALL)
print("home square is " + MYSQUARE)

###################################
# read the log file
###################################

# open the log file
try:
    wlog = open(WSJTXLOG, "r")
except FileNotFoundError:
    print(f"File " + WSJTXLOG + " not found.")
    sys.exit(1)
except OSError:
    print(f"OS error occurred trying to open " + WSJTXLOG)
    sys.exit(1)
except Exception as err:
    print(f"Unexpected error opening " + WSJTXLOG + " is",repr(err))
    sys.exit(1)  
    
# here the raw information (squares) from wsjtx log are stored
LOCS_LOG = [ ]

loglines = 0

# read each line of the log fole
for line in wlog:
    # split the line by comma
    e = line.split(",")
    # the field is element 5 (starting with 0) in the list e
    loc = e[5]
    # check if loc is empty. If not empty, append to locator list
    if 0 != len(loc):
        LOCS_LOG.append(loc)
        loglines += 1
    
    # print("loc: ", loc, "\n")

# close the log file after reading
wlog.close()

print("found " + str(loglines) + " QSOs in log")

###################################
# sort the data
###################################

print("now checking worked squares")

# remove multiple worked sqares 
SQUARES = [ ]
FIELDS = [ ]

for l in LOCS_LOG:
    # remember worked squares
    if l not in SQUARES:
        SQUARES.append(l)

    # remember worked fields
    if l[:2] not in FIELDS:
        FIELDS.append(l[:2])
        

###################################
# write output file
###################################

# open output file
try:
    lo = open(LOCOUTPUT + "." + OUTMODE, "w")
except FileNotFoundError:
    # this is no error as we want to write the file
    pass
except OSError:
    print(f"OS error occurred trying to open " + LOCOUTPUT)
    sys.exit(1)
except Exception as err:
    print(f"Unexpected error opening " + LOCOUTPUT + " is",repr(err))
    sys.exit(1)  


# show progress to the user
print("processing ", end="", flush=True)


# print header for html file and table
if ("html" == OUTMODE):
    lo.write("<html>\n")
    lo.write("<head></head>\n")
    lo.write("<body>\n")

lo.write("Worked squares and fields by "+MYCALL+" in WSJT-X in " + MYSQUARE +"\n\n")

if ("html" == OUTMODE):
    lo.write("<p/>\n")
    lo.write("<table cellspacing=\"0\" cellpadding=\"2\">\n")
    # define colgroup - there are 10*18 + 2 columns, each should be same with
    lo.write("<colgroup width=\"1*\" span=\"182\">\n")
    lo.write("</colgroup>\n")
    
    
# write orientation line above map

# the first element of the first line must be a blank
# because the first column gives the coordinates
if ("txt" == OUTMODE):
    lo.write(" ")

# start html table row
if ("html" == OUTMODE):
    lo.write("<tr>\n")
    lo.write("<td style=\"border-bottom: 1px solid #000000;\">&nbsp;</td>")
    
for we in fieldsWE:
    # iterate over all fields
    for wec in squaresWE:
        # iterate over all squares
        if ("html" == OUTMODE):
            lo.write("<td")
            if (0 == wec):
                lo.write(" style=\"border-left: 1px solid #000000; border-bottom: 1px solid #000000;\"")
            else:
                lo.write(" style=\"border-bottom: 1px solid #000000;\"")
               
            lo.write(">")
        #if (0 == wec) or (1 == wec) or (8 == wec) or (9 == wec):
        #    lo.write(str(wec))
        #elif (5 == wec):
        #    lo.write(str(we))
        #else:
        #  lo.write(".")
        if (5 != wec):
            lo.write(str(wec))
        else:
            lo.write(str(we))
          
        if ("html" == OUTMODE):
            lo.write("</td>")
          
# end the line
if ("txt" == OUTMODE):
    lo.write("\n")
    
# end the html row
if ("html" == OUTMODE):
    lo.write("<td style=\"border-left: 1px solid #000000; border-bottom: 1px solid #000000;\">&nbsp;</td>")
    lo.write("</tr>\n")


# iterate over all squares from north to south
for ns in fieldsNS:
    # iterate over all squares in field from north to south
    for nsl in squaresNS:
        # start new line

        # start html table row
        if ("html" == OUTMODE):
            lo.write("<tr>\n")
            lo.write("<!- ns="+ns+" - nsl="+str(nsl)+" ->\n")
            lo.write("<td")
            if (0 == nsl) & (0 == wec):
                lo.write(" style=\"border-bottom: 1px solid #000000; border-left: 1px solid #000000;\"")
            elif (0 == nsl):
                lo.write(" style=\"border-bottom: 1px solid #000000;\"")
            elif (0 == wec):
                lo.write(" style=\"border-left: 1px solid #000000;\"")

            lo.write(">")
                
        # write orientation at beginning of line
        # give the field numbers - only in the middle (pos 5) give the character
        if (5 != nsl):
            lo.write(str(nsl))
        else:
            lo.write(str(ns))

        # end first data tag
        if ("html" == OUTMODE):
            lo.write("</td>")
          
        # iterate over all fields from west to east
        for we in fieldsWE:
            # iterate over all squares in field from west to east
            for wec in squaresWE:
                # this is the current sqare
                square = we + ns + str(wec) + str(nsl)
                field = we + ns

                #print("'"+ square + "' ", end="")
                #print(square == MYSQUARE, end="")
                #print(" - mysquare " + MYSQUARE)

                style = ""
                
                # start html table data
                if ("html" == OUTMODE):
                    #if (0 == nsl) & (0 == wec):
                    #    style = "border-bottom: 1px solid #000000; border-left: 1px solid #000000;\"")
                    if (0 == nsl):
                        style = style + " border-bottom: 1px solid #000000;"
                    if (0 == wec):
                        style = style + " border-left: 1px solid #000000;"
                
                # test, if this square has been worked
                if square == MYSQUARE:
                    # this is my on square. Show it by special character
                    if ("html" == OUTMODE):
                        style = style + " background-color:" + BGCOLOR_OWN + ";"
                    if square in SQUARES:
                        outtext = "#"
                    else:
                        outtext = "O"
                elif square in SQUARES:
                    # this square is worked
                    if ("html" == OUTMODE):
                        style = style + " background-color:" + BGCOLOR_SQUARE + ";"
                    outtext = "X"
                elif field in FIELDS:
                    # this field is worked                    
                    if ("html" == OUTMODE):
                        style = style + " background-color:" + BGCOLOR_FIELD + ";"
                    outtext = "."
                else:
                    # neither square nor field is yet worked
                    if ("html" == OUTMODE):
                        style = style + " background-color:" + BGCOLOR_EMPTY + ";"
                    outtext = " "

                # TODO: evaluate the FIELD and write a "." for worked field

                # start data tag
                if ("html" == OUTMODE):
                    lo.write("<td style=\""+style+"\">")

                lo.write(outtext)
                
                # end data tag
                if ("html" == OUTMODE):
                    lo.write("</td>")
                    
                    
                
        # start html table data
        if ("html" == OUTMODE):
            lo.write("<td")
            
            if (0 == nsl):
                lo.write(" style=\"border-bottom: 1px solid #000000; border-left: 1px solid #000000;\"")
            else:
                lo.write(" style=\"border-left: 1px solid #000000;\"")
            
            lo.write(">")
            
        # write orientation at end of line
        if (5 != nsl):
            lo.write(str(nsl))
        else:
            lo.write(str(ns))
        
        # end the line
        if ("txt" == OUTMODE):
            lo.write("\n")
            
        # end last data tag and row
        if ("html" == OUTMODE):
            lo.write("</td>\n")
            lo.write("</tr>\n")
            
        # show some progress to the user
        print(".", end="", flush=True)


# write orientation line below map

# the first element of the first line must be a blank
# because the first column gives the coordinates
if ("txt" == OUTMODE):
    lo.write(" ")

# start html table row
if ("html" == OUTMODE):
    lo.write("<tr>\n")
    lo.write("<td>&nbsp;</td>")
    
for we in fieldsWE:
    # iterate over all fields
    for wec in squaresWE:
        # iterate over all squares
        if ("html" == OUTMODE):
            lo.write("<td")
            if (0 == wec):
                lo.write(" style=\"border-left: 1px solid #000000\"")
                
            lo.write(">")
            
        # write field number - only in the middle write square character
        if (5 != wec):
            lo.write(str(wec))
        else:
            lo.write(str(we))
          
        if ("html" == OUTMODE):
            lo.write("</td>")
          
# end the line
if ("txt" == OUTMODE):
    lo.write("\n")
    
# end the html row
if ("html" == OUTMODE):
    lo.write("<td style=\"border-left: 1px solid #000000\">&nbsp;</td>")
    lo.write("</tr>\n")


    
# close the html table
if ("html" == OUTMODE):
    lo.write("</table>\n")
    lo.write("<p/>\n")

# output statistics
lo.write("\n" + str(len(FIELDS)) + " fields, " + str(len(SQUARES)) + " squares\n")

# close the html tags
if ("html" == OUTMODE):
    lo.write("</body>\n")
    lo.write("</html>\n")

# close output file
lo.close()

# print out some final statemens 
print("")
print(str(len(FIELDS)) + " fields, " + str(len(SQUARES)) + " squares")
print("done")

