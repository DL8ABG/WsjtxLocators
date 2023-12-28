#!/usr/bin/python3
#
# evaluating logbook of wsjt-x and gain information on worked locator squares
#
# Infos from https://de.wikipedia.org/wiki/QTH-Locator
#
# Frank Hänsel, DL8ABG
# 
# Changelog:
#
# 27.12.2023
# - more html implementation
#   (background color for table cells)
#
# 26.12.2023
# - started implementing html output
#
# 23.12.2023
# - output file for locator output in console during startup
#
# 14.09.2021
# - Initial setup of file
# - optimisation of prior version
#
# Ideas:
# - implement program options:
#   -t use txt output (html is default)
#   -o <file> write output to <file> rather than default name
#   -l <file> read log from <file> rather than from default file name
#   -h <field> define my home field
#   -c <call> give my own call to be printed in output
# - in html: background color for worked field/squares in light/dark brown, rest light blue (earth/ocean)

# use regular expressions
import re

# this is the square of the user to be shown as a special character
MYSQUARE="JO52"

MYCALL="DL8ABG"

WSJTXLOG="wsjtx.log"

# file to print the output to
# well be completed by "." and OUTMODE as suffix
LOCOUTPUT="locatormap"

# OUTMODE="txt"
OUTMODE="html"

# background color for own sware in html table
BGCOLOR_OWN="#FF0000"

# background color for empty field in html table (blue ocean)
BGCOLOR_EMPTY="#CCEEFF"

# background color for empty field in html table (light brown earth)
BGCOLOR_FIELD="#DFAF9F"

# background color for empty field in html table (dark brown earth)
BGCOLOR_SQUARE="#994D33"



# name parts of fields and squares to iterate over (west to east)
fieldsWE = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"]

# name parts of fields and squares to iterate over (north to south)
fieldsNS = ["R", "Q", "P", "O", "N", "M", "L", "K", "J", "I", "H", "G", "F", "E", "D", "C", "B", "A"]

# Square numbers west to east
squaresWE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# square numbers north to south
squaresNS = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# Print info to the user
print("reading log file " + WSJTXLOG)
print("writing locator mat to " + LOCOUTPUT + "." + OUTMODE)

############
# Read log file
############

# open the log file
wlog = open(WSJTXLOG, "r")

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

############
# Sort data
############

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
        

############
# Write output file
############

# open output file
lo = open(LOCOUTPUT + "." + OUTMODE, "w")

# show progress to the user
print("processing ", end="", flush=True)


# print header for html file and table
if ("html" == OUTMODE):
    lo.write("<html>\n")
    lo.write("<head></head>\n")
    lo.write("<body>\n")
    lo.write("Worked squares and fields by "+MYCALL+" in WSJT-X\n<p/>\n")
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
lo.write(str(len(FIELDS)) + " fields, " + str(len(SQUARES)) + " squares\n")

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

